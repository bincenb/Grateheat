"""Read the raw PISA 2022 files, apply the pre-registered recodes and
exclusions, and write the analysis file plus a missingness table.

Every recode and exclusion is here; nothing is edited by hand.
"""
import os
import re
import numpy as np
import pandas as pd
import pyreadstat

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.environ.get("PISA_RAW", os.path.join(HERE, "..", "..", "pisa_raw"))
WORK = os.path.join(HERE, "work")
RES = os.path.join(HERE, "results")
os.makedirs(WORK, exist_ok=True)
os.makedirs(RES, exist_ok=True)

FORMS = {"ST297Q01JA": "one_on_one", "ST297Q03JA": "online", "ST297Q05JA": "video",
         "ST297Q06JA": "small_group", "ST297Q07JA": "large_group"}
NONE = "ST297Q09JA"

stu_path = os.path.join(RAW, "CY08MSP_STU_QQQ.SAV")
_, meta = pyreadstat.read_sav(stu_path, metadataonly=True)
names = meta.column_names
keep = ["CNT", "CNTSCHID", "CNTSTUID", "OECD", "ST004D01T", "AGE", "GRADE", "IMMIG", "ESCS", "REPEAT",
        "ST016Q01NA", "ANXMAT", "BELONG", "FEELSAFE", NONE, *FORMS]
keep += [c for c in names if re.match(r"WB154Q0\dHA$", c)]
keep += [c for c in names if re.match(r"W_FSTURWT\d+$", c)] + ["W_FSTUWT"]
keep += [c for c in names if re.match(r"PV\d+MATH$", c)]
stu, _ = pyreadstat.read_sav(stu_path, usecols=keep)  # user-missing codes -> NaN
sch, _ = pyreadstat.read_sav(os.path.join(RAW, "CY08MSP_SCH_QQQ.SAV"), usecols=["CNTSCHID", "SC013Q01TA", "SC001Q01TA"])
df = stu.merge(sch, on="CNTSCHID", how="left")
n_raw = len(df)

# ---- exposure (protocol §4)
f = df[list(FORMS)]
nforms = (f == 1).sum(axis=1)
none = df[NONE] == 1
item_missing = df[[*FORMS, NONE]].isna().all(axis=1)
pattern = np.select(
    [item_missing, (nforms == 0) & none, (nforms > 0) & ~none, (nforms == 0) & ~none, (nforms == 5) & none],
    ["item_missing", "valid_none", "valid_some", "nothing_ticked", "straightline"],
    default="contradictory")
df["ST297_PATTERN"] = pattern
valid = np.isin(pattern, ["valid_none", "valid_some"])
df["ANYADD"] = np.where(valid, (nforms > 0).astype(float), np.nan)
df["NFORMS"] = np.where(valid, nforms, np.nan)
for c, name in FORMS.items():
    df[f"FORM_{name}"] = np.where(valid, (df[c] == 1).astype(float), np.nan)
df["NFORMS_ALL"] = nforms.where(~item_missing)  # raw count, used only for S9

# ---- outcome and covariates
df["LS"] = df["ST016Q01NA"]
df["FEMALE"] = (df["ST004D01T"] == 1).astype(float).where(df["ST004D01T"].notna())
df["GRADE3"] = np.sign(df["GRADE"])  # -1 below, 0 modal, +1 above modal grade
df["PRIVATE"] = (df["SC013Q01TA"] == 2).astype(float).where(df["SC013Q01TA"].notna())
df["LOC5"] = df["SC001Q01TA"].clip(upper=5)  # megacity merged with large city
wb = [c for c in df.columns if re.match(r"WB154Q0\dHA$", c)]
wbn = df[wb].notna().sum(axis=1)
df["PSYSOM"] = df[wb].mean(axis=1).where(wbn >= int(np.ceil(len(wb) / 2)))

# ---- exclusions (protocol §6)
cov = df.groupby("CNT").agg(st297=("ST297_PATTERN", lambda s: (s != "item_missing").mean()),
                           ls=("LS", lambda s: s.notna().mean()),
                           escs=("ESCS", lambda s: s.notna().mean()),
                           sex=("FEMALE", lambda s: s.notna().mean()),
                           age=("AGE", lambda s: s.notna().mean()))
eligible = cov[(cov.st297 >= .5) & (cov.ls >= .5)]
core_ok = eligible[(eligible.escs > 0) & (eligible.sex > 0) & (eligible.age > 0)]
log = [f"raw students: {n_raw}, systems: {cov.shape[0]}",
       f"systems with >=50% ST297 and ST016: {len(eligible)}",
       f"dropped for an entirely missing core covariate: {sorted(set(eligible.index) - set(core_ok.index))}",
       f"analysis systems: {len(core_ok)}"]
df = df[df.CNT.isin(core_ok.index)].copy()
log.append(f"analysis students: {len(df)}")

# school-level covariates missing for >50% of a system's students are dropped from that system's model
school_drop = {}
for c in ["PRIVATE", "LOC5"]:
    share = df.groupby("CNT")[c].apply(lambda s: s.isna().mean())
    school_drop[c] = sorted(share[share > .5].index)
    log.append(f"{c} omitted (>50% missing) in: {school_drop[c]}")
pd.Series({k: ",".join(v) for k, v in school_drop.items()}).to_csv(os.path.join(WORK, "school_cov_drop.csv"))

# auxiliary for imputation: school mean ESCS
df["SCH_ESCS"] = df.groupby("CNTSCHID")["ESCS"].transform("mean")
df["LOGW"] = np.log(df["W_FSTUWT"])

# ---- missingness table
analytic = ["LS", "ANYADD", "FEMALE", "AGE", "GRADE3", "ESCS", "IMMIG", "REPEAT", "PRIVATE", "LOC5"]
miss = df[analytic].isna().mean().mul(100).round(2).rename("pct_missing").to_frame()
miss.loc["any_of_the_above"] = round(df[analytic].isna().any(axis=1).mean() * 100, 2)
miss.to_csv(os.path.join(RES, "missingness.csv"))
pat = df["ST297_PATTERN"].value_counts().rename("n").to_frame()
pat.to_csv(os.path.join(RES, "exposure_patterns.csv"))
df.groupby("CNT")[analytic].apply(lambda g: g.isna().mean().mul(100).round(1)).to_csv(os.path.join(RES, "missingness_by_system.csv"))

out_cols = (["CNT", "CNTSCHID", "CNTSTUID", "OECD", "ST297_PATTERN", "NFORMS_ALL", "NFORMS", "ANYADD",
             *[f"FORM_{v}" for v in FORMS.values()], *analytic[2:], "LS", "ANXMAT", "BELONG", "FEELSAFE",
             "PSYSOM", "SCH_ESCS", "LOGW"]
            + [c for c in df.columns if re.match(r"PV\d+MATH$", c)] + ["W_FSTUWT"]
            + [f"W_FSTURWT{i}" for i in range(1, 81)])
out_cols = list(dict.fromkeys(out_cols))
df[out_cols].to_parquet(os.path.join(WORK, "analytic.parquet"))
open(os.path.join(RES, "prepare_log.txt"), "w").write("\n".join(log) + "\n")
print("\n".join(log))
print(miss.to_string())
print(pat.to_string())
