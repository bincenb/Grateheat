"""Primary, secondary and sensitivity analyses (protocol §7).

Within each system: multiple imputation (PMM, M = 20, 20 iterations), then
BRR-weighted least squares on each completed dataset, combined by Rubin's
rules. Complete-case analyses use the same BRR models without imputation.
System estimates are pooled as the PISA international average.
"""
import json
import os
import sys
import zlib
from multiprocessing import Pool

import numpy as np
import pandas as pd

from lib import WCOLS, brr_wls, brr_mean, combine, international_average, dersimonian_laird, ci, pval, evalue_from_d, mice_pmm

HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(HERE, "work")
RES = os.path.join(HERE, "results")
SEED = 20221
M = int(os.environ.get("MI_M", 20))
ITERS = int(os.environ.get("MI_ITERS", 20))
FORMS = ["one_on_one", "online", "video", "small_group", "large_group"]
PVS = [f"PV{i}MATH" for i in range(1, 11)]

drop = pd.read_csv(os.path.join(WORK, "school_cov_drop.csv"), index_col=0).iloc[:, 0].fillna("")
SCHOOL_DROP = {k: set(v.split(",")) - {""} for k, v in drop.items()}


# ---------------------------------------------------------------- design
def covariates(d, cnt, grade=True):
    """Pre-registered covariate matrix (protocol §4)."""
    cols = {"FEMALE": d.FEMALE, "AGE": d.AGE - 15.75, "ESCS": d.ESCS}
    if cnt not in SCHOOL_DROP["REPEAT"]:
        cols["REPEAT"] = d.REPEAT
    if cnt not in SCHOOL_DROP["IMMIG"]:
        cols["IMMIG2"] = (d.IMMIG == 2) * 1.0
        cols["IMMIG3"] = (d.IMMIG == 3) * 1.0
    if grade and cnt not in SCHOOL_DROP["GRADE3"]:
        cols["GR_BELOW"] = (d.GRADE3 < 0) * 1.0
        cols["GR_ABOVE"] = (d.GRADE3 > 0) * 1.0
    if cnt not in SCHOOL_DROP["PRIVATE"]:
        cols["PRIVATE"] = d.PRIVATE
    if cnt not in SCHOOL_DROP["LOC5"]:
        for k in (2, 3, 4, 5):
            cols[f"LOC{k}"] = (d.LOC5 == k) * 1.0
    return pd.DataFrame(cols, index=d.index)


def fit(d, y, terms, cnt, grade=True):
    """BRR WLS of y on [terms] + covariates. Returns {term: (beta, var)}."""
    X = pd.concat([pd.DataFrame({"const": 1.0}, index=d.index), terms, covariates(d, cnt, grade)], axis=1)
    ok = X.notna().all(axis=1) & d[y].notna()
    X, yy, W = X[ok], d.loc[ok, y].to_numpy(float), d.loc[ok, WCOLS].to_numpy(float)
    X = X.loc[:, (X.std() > 0) | (X.columns == "const")]  # drop columns constant in this system
    keep = [t for t in terms.columns if t in X.columns]
    if len(yy) < 50 or len(keep) < len(terms.columns):
        return None, int(ok.sum())
    beta, var, _ = brr_wls(X.to_numpy(float), yy, W)
    idx = [X.columns.get_loc(t) for t in keep]
    return {t: (beta[i], var[i]) for t, i in zip(keep, idx)}, int(ok.sum())


MIN_CELL = 30  # interaction terms need >= 30 observed students in each exposure x subgroup cell


def cells_ok(g, group):
    """True if every exposure x subgroup cell has at least MIN_CELL observed students."""
    obs = g.ANYADD.notna() & group.notna()
    if not obs.any():
        return False
    tab = pd.crosstab(g.ANYADD[obs], group[obs])
    return tab.shape == (2, 2) and bool((tab >= MIN_CELL).all().all())


def model_set(d, cnt, ok):
    """Models run on each imputed dataset. Returns {name: {term: (b, v)}}."""
    out = {}
    A = pd.DataFrame({"ANY": d.ANYADD}, index=d.index)
    out["primary"], _ = fit(d, "LS", A, cnt)
    out["E1_escs"], _ = fit(d, "LS", A.assign(ANYxESCS=d.ANYADD * d.ESCS), cnt)
    out["E1_sex"], _ = fit(d, "LS", A.assign(ANYxFEMALE=d.ANYADD * d.FEMALE), cnt) if ok["sex"] else (None, 0)
    gr = {}
    if ok["below"]:
        gr["ANYxBELOW"] = d.ANYADD * (d.GRADE3 < 0)
    if ok["above"]:
        gr["ANYxABOVE"] = d.ANYADD * (d.GRADE3 > 0)
    out["E1_grade"], _ = fit(d, "LS", A.assign(**gr), cnt) if gr else (None, 0)
    nf = pd.DataFrame({"NF1": (d.NFORMS == 1) * 1.0, "NF2": (d.NFORMS == 2) * 1.0, "NF3P": (d.NFORMS >= 3) * 1.0}, index=d.index)
    out["S2_dose"], _ = fit(d, "LS", nf, cnt)
    modal = d[d.GRADE3 == 0]
    out["S3_modal_grade"], _ = fit(modal, "LS", A.loc[modal.index], cnt, grade=False)
    sub = d[d.NFORMS <= 3]
    out["S4_drop_4plus_forms"], _ = fit(sub, "LS", A.loc[sub.index], cnt)
    return out


# ---------------------------------------------------------------- per system
def run_system(args):
    cnt, g, seed = args
    g = g.copy()
    res = {"CNT": cnt, "OECD": int(g.OECD.max()), "n": len(g)}
    W = g[WCOLS].to_numpy(float)

    # descriptives (observed data)
    obs = g.ANYADD.notna()
    res["prev"], res["prev_var"] = brr_mean(g.ANYADD[obs].to_numpy(float), W[obs.to_numpy()])
    lso = g.LS.notna()
    res["ls_mean"], res["ls_mean_var"] = brr_mean(g.LS[lso].to_numpy(float), W[lso.to_numpy()])
    w = g.W_FSTUWT[lso]
    res["ls_sd"] = float(np.sqrt(np.average((g.LS[lso] - np.average(g.LS[lso], weights=w)) ** 2, weights=w)))
    res["n_exposure_missing_pct"] = float((~obs).mean() * 100)

    # ---- complete-case analyses
    A = pd.DataFrame({"ANY": g.ANYADD}, index=g.index)
    cc = {}
    cc["S1_complete_case"], res["n_cc"] = fit(g, "LS", A, cnt)
    # S9 alternative exposure codings
    pat = g.ST297_PATTERN
    alt_a = np.where(pat == "nothing_ticked", 0.0, g.ANYADD)
    alt_b = np.where(pat == "contradictory", 1.0, g.ANYADD)
    alt_c = np.where(pat == "straightline", 1.0, g.ANYADD)
    for k, v in {"S9a_nothing_as_none": alt_a, "S9b_contradictory_as_some": alt_b, "S9c_straightline_as_some": alt_c}.items():
        cc[k], _ = fit(g, "LS", pd.DataFrame({"ANY": v}, index=g.index), cnt)
    # S5 negative-control outcome and E4 secondary outcomes
    for k, y in {"S5_negctrl_feelsafe": "FEELSAFE", "E4_anxmat": "ANXMAT", "E4_psysom": "PSYSOM"}.items():
        cc[k], _ = fit(g, y, A, cnt) if g[y].notna().mean() > .5 else (None, 0)
    # E2 by form (joint model, valid responders)
    forms = pd.DataFrame({f: g[f"FORM_{f}"] for f in FORMS}, index=g.index)
    cc["E2_forms"], _ = fit(g, "LS", forms, cnt)
    # S7 adjust for mathematics achievement, 10 PVs combined
    pv_fits = []
    for p in PVS:
        r, _ = fit(g.assign(MATH100=g[p] / 100), "LS", A.assign(MATH100=g[p] / 100), cnt)
        pv_fits.append(r)
    if all(r is not None for r in pv_fits):
        q, t = combine([r["ANY"][0] for r in pv_fits], [r["ANY"][1] for r in pv_fits])
        cc["S7_adjust_math_pv"] = {"ANY": (q, t)}
    res["cc"] = cc

    # ---- multiple imputation
    imp_cols = ["LS", "NFORMS", "ESCS"] + [c for c in ["GRADE3", "IMMIG", "REPEAT", "PRIVATE", "LOC5"] if cnt not in SCHOOL_DROP[c]]
    imp_cols = [c for c in imp_cols if g[c].notna().any()]
    aux = ["FEMALE", "AGE", "ANXMAT", "BELONG", "SCH_ESCS", "LOGW"]
    aux = [c for c in aux if g[c].notna().any()]
    completed = mice_pmm(g, imp_cols, aux, M, ITERS, seed)
    ok = {"sex": cells_ok(g, g.FEMALE), "below": cells_ok(g, (g.GRADE3 < 0).where(g.GRADE3.notna())),
          "above": cells_ok(g, (g.GRADE3 > 0).where(g.GRADE3.notna()))}
    per_imp = []
    for comp in completed:
        d = g.copy()
        d[imp_cols] = comp
        d["ANYADD"] = (d.NFORMS > 0) * 1.0
        per_imp.append(model_set(d, cnt, ok))
    mi = {}
    for name in per_imp[0]:
        fits = [p[name] for p in per_imp]
        if any(f is None for f in fits):
            mi[name] = None
            continue
        mi[name] = {}
        for term in fits[0]:
            q, t = combine([f[term][0] for f in fits], [f[term][1] for f in fits])
            mi[name][term] = (float(q), float(t))
    res["mi"] = mi
    return res


def main():
    df = pd.read_parquet(os.path.join(WORK, "analytic.parquet"))
    systems = sorted(df.CNT.unique())
    only = os.environ.get("ONLY")
    if only:
        systems = [s for s in systems if s in only.split(",")]
    jobs = [(c, df[df.CNT == c], SEED + i) for i, c in enumerate(sorted(df.CNT.unique())) if c in systems]
    del df
    procs = int(os.environ.get("PROCS", 4))
    with Pool(procs) as pool:
        results = []
        for r in pool.imap_unordered(run_system, jobs):
            results.append(r)
            print(f"done {r['CNT']} ({len(results)}/{len(jobs)})", flush=True)
    results.sort(key=lambda r: r["CNT"])

    def conv(o):
        if isinstance(o, (np.floating, np.integer)):
            return o.item()
        if isinstance(o, tuple):
            return list(o)
        raise TypeError(type(o))
    json.dump(results, open(os.path.join(WORK, "system_results.json"), "w"), default=conv)
    print("saved", len(results), "systems")


if __name__ == "__main__":
    main()
