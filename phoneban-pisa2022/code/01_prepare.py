"""Read the raw PISA 2022 files, keep the 15 Well-Being Questionnaire systems,
recode every analysis variable, apply the pre-specified exclusions, and save
data_work/wbq_all.pkl (all WBQ students) and data_work/analytic.pkl.
Run from the project folder:  python3 code/01_prepare.py
"""
import os
import sys
import numpy as np
import pandas as pd
import pyreadstat

sys.path.insert(0, os.path.dirname(__file__))
from brr import REPW  # noqa: E402

RAW = "data_raw"
WORK = "data_work"
OUT = "output/tables"
os.makedirs(WORK, exist_ok=True)
os.makedirs(OUT, exist_ok=True)

SYM = [f"WB154Q0{i}HA" for i in range(1, 10)]
PSYCH = ["WB154Q04HA", "WB154Q05HA", "WB154Q06HA", "WB154Q07HA", "WB154Q09HA"]
SOMA = ["WB154Q01HA", "WB154Q02HA", "WB154Q03HA", "WB154Q08HA"]
PVS = [f"PV{i}MATH" for i in range(1, 11)]

stu_cols = (["CNT", "CNTSCHID", "CNTSTUID", "OECD", "Option_WBQ", "W_FSTUWT"] + REPW
            + ["ST004D01T", "AGE", "GRADE", "ESCS", "IMMIG", "REPEAT"]
            + SYM + ["WB150Q01HA", "WB152Q01HA"] + PVS)
sch_cols = ["CNT", "CNTSCHID", "SC190Q01JA", "SC190Q02JA", "SC190Q06JA",
            "PRIVATESCH", "SC013Q01TA", "SC001Q01TA", "SCHSIZE"]

stu, _ = pyreadstat.read_sav(f"{RAW}/CY08MSP_STU_QQQ.SAV", usecols=stu_cols)
sch, _ = pyreadstat.read_sav(f"{RAW}/CY08MSP_SCH_QQQ.SAV", usecols=sch_cols)
n_all = len(stu)
stu = stu[stu.Option_WBQ == 1].copy()
print(f"PISA 2022 students: {n_all:,}; in WBQ systems: {len(stu):,}")

d = stu.merge(sch, on=["CNT", "CNTSCHID"], how="left", validate="m:1")
assert len(d) == len(stu)


def yn(s):  # 1 = Yes, 2 = No -> 1/0
    return s.map({1.0: 1.0, 2.0: 0.0})


# exposure and other school policy items
d["ban"] = yn(d.SC190Q02JA)
d["stmt"] = yn(d.SC190Q01JA)
d["tchrules"] = yn(d.SC190Q06JA)

# school covariates
priv = d.PRIVATESCH.astype(str).str.strip().str.lower()
d["private"] = np.where(priv == "private", 1.0, np.where(priv == "public", 0.0, np.nan))
# fallback to the principal's own answer (1 public, 2 private) where the sampling-frame
# variable is missing (all of HUN and SVN); see DEVIATIONS.md
d["private"] = d["private"].fillna(d.SC013Q01TA.map({1.0: 0.0, 2.0: 1.0}))
d["commsize"] = d.SC001Q01TA.clip(upper=5)          # 6 = megacity merged into 5 = large city+
d["lschsize"] = np.log(d.SCHSIZE.where(d.SCHSIZE > 0))
# school mean ESCS over all sampled students in the school (observed values)
d["sch_escs"] = d.groupby(["CNT", "CNTSCHID"]).ESCS.transform("mean")

# student covariates
d["female"] = d.ST004D01T.map({1.0: 1.0, 2.0: 0.0})
d["age"] = d.AGE
d["grade"] = d.GRADE.where(d.GRADE.abs() <= 4)
d["escs"] = d.ESCS
d["immig"] = d.IMMIG                                 # 1 native, 2 second gen, 3 first gen
d["repeat"] = d.REPEAT
d["oecd"] = d.OECD

# outcomes
S = d[SYM]
n_ans = S.notna().sum(axis=1)
d["n_sym"] = n_ans
d["psc"] = S.mean(axis=1).where(n_ans >= 7)
d["mhc"] = ((S >= 4).sum(axis=1) >= 2).astype(float).where(n_ans >= 7)
d["sleep"] = d.WB154Q07HA
d["psych"] = d[PSYCH].mean(axis=1).where(n_ans >= 7)
d["soma"] = d[SOMA].mean(axis=1).where(n_ans >= 7)
d["srh"] = d.WB150Q01HA
d["allfive"] = ((S == 5).sum(axis=1) == 9).astype(float)
h = d.WB152Q01HA.where(d.WB152Q01HA.between(120, 220))


def zgrp(g):
    w = d.loc[g.index, "W_FSTUWT"]
    m = g.notna()
    if m.sum() < 30:          # item not administered in this system
        return g * np.nan
    mu = np.average(g[m], weights=w[m])
    sd = np.sqrt(np.average((g[m] - mu) ** 2, weights=w[m]))
    return (g - mu) / sd


d["height_z"] = h.groupby([d.CNT, d.female]).transform(zgrp)

keep = (["CNT", "CNTSCHID", "CNTSTUID", "W_FSTUWT"] + REPW + PVS
        + ["ban", "stmt", "tchrules", "private", "commsize", "lschsize", "sch_escs",
           "female", "age", "grade", "escs", "immig", "repeat", "oecd",
           "n_sym", "psc", "mhc", "sleep", "psych", "soma", "srh", "allfive", "height_z"])
d = d[keep].reset_index(drop=True)
d.to_pickle(f"{WORK}/wbq_all.pkl")

# exclusion: valid outcome (>= 7 of 9 symptom items)
flow = [("PISA 2022 students, all systems", n_all, None),
        ("Students in the 15 WBQ systems", len(d), d.CNTSCHID.nunique())]
a = d[d.psc.notna()].reset_index(drop=True)
flow.append(("With valid psychosomatic score (>=7 of 9 items)", len(a), a.groupby("CNT").CNTSCHID.nunique().sum()))
pd.DataFrame(flow, columns=["step", "students", "schools"]).to_csv(f"{OUT}/flow.csv", index=False)
print(pd.DataFrame(flow, columns=["step", "students", "schools"]).to_string(index=False))

# missingness in the analytic sample
vars_ = ["ban", "stmt", "tchrules", "private", "commsize", "lschsize", "sch_escs",
         "female", "age", "grade", "escs", "immig", "repeat",
         "psc", "mhc", "sleep", "psych", "soma", "srh", "height_z"]
miss = pd.DataFrame({"variable": vars_,
                     "n_missing": [int(a[v].isna().sum()) for v in vars_],
                     "pct_missing": [round(100 * a[v].isna().mean(), 2) for v in vars_]})
miss.to_csv(f"{OUT}/missingness.csv", index=False)
print(miss.to_string(index=False))
a.to_pickle(f"{WORK}/analytic.pkl")
