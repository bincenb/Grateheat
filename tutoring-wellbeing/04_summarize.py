"""Pool system estimates and write result tables (protocol §7)."""
import json
import os

import numpy as np
import pandas as pd

from lib import WCOLS, brr_wls, international_average, dersimonian_laird, ci, pval, evalue_from_d

HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(HERE, "work")
RES = os.path.join(HERE, "results")
R = json.load(open(os.path.join(WORK, "system_results.json")))
sysdf = pd.DataFrame([{k: r[k] for k in ("CNT", "OECD", "n", "n_cc", "prev", "prev_var", "ls_mean", "ls_sd", "n_exposure_missing_pct")} for r in R])
POOLED_SD = float(np.sqrt((sysdf.ls_sd ** 2).mean()))


def collect(src, model, term):
    rows = []
    for r in R:
        f = r[src].get(model)
        if f and term in f:
            rows.append((r["CNT"], r["OECD"], f[term][0], f[term][1]))
    return pd.DataFrame(rows, columns=["CNT", "OECD", "est", "var"])


def summarize(label, src, model, term, scale_sd=POOLED_SD, subset=None):
    d = collect(src, model, term)
    if subset is not None:
        d = d[d.CNT.isin(subset)]
    if d.empty:
        return None
    est, se = international_average(d.est, d["var"])
    lo, hi = ci(est, se)
    oe, ose = international_average(d[d.OECD == 1].est, d[d.OECD == 1]["var"]) if (d.OECD == 1).any() else (np.nan, np.nan)
    return {"analysis": label, "source": "MI" if src == "mi" else "complete case", "model": model, "term": term,
            "systems": len(d), "estimate": est, "se": se, "ci_low": lo, "ci_high": hi, "p": pval(est, se),
            "std_estimate": est / scale_sd if scale_sd else np.nan,
            "oecd_systems": int((d.OECD == 1).sum()), "oecd_estimate": oe, "oecd_se": ose,
            "systems_negative_sig": int(((d.est + 1.96 * np.sqrt(d["var"])) < 0).sum()),
            "systems_positive_sig": int(((d.est - 1.96 * np.sqrt(d["var"])) > 0).sum())}


def unadjusted():
    """Unadjusted weighted difference in life satisfaction (STROBE item 16), complete case, BRR."""
    d = pd.read_parquet(os.path.join(WORK, "analytic.parquet"), columns=["CNT", "OECD", "LS", "ANYADD", *WCOLS])
    d = d.dropna(subset=["LS", "ANYADD"])
    out = []
    for cnt, g in d.groupby("CNT"):
        X = np.column_stack([np.ones(len(g)), g.ANYADD.to_numpy(float)])
        b, v, _ = brr_wls(X, g.LS.to_numpy(float), g[WCOLS].to_numpy(float))
        out.append((cnt, int(g.OECD.max()), b[1], v[1]))
    return pd.DataFrame(out, columns=["CNT", "OECD", "est", "var"])


UNADJ = unadjusted()
rows = []
add = lambda *a, **k: rows.append(summarize(*a, **k))
add("PRIMARY: any additional math instruction -> life satisfaction", "mi", "primary", "ANY")
_u_est, _u_se = international_average(UNADJ.est, UNADJ["var"])
rows.append({"analysis": "Unadjusted difference (complete case)", "source": "complete case", "model": "unadjusted", "term": "ANY",
             "systems": len(UNADJ), "estimate": _u_est, "se": _u_se, "ci_low": ci(_u_est, _u_se)[0], "ci_high": ci(_u_est, _u_se)[1],
             "p": pval(_u_est, _u_se), "std_estimate": _u_est / POOLED_SD,
             "systems_negative_sig": int(((UNADJ.est + 1.96 * np.sqrt(UNADJ["var"])) < 0).sum()),
             "systems_positive_sig": int(((UNADJ.est - 1.96 * np.sqrt(UNADJ["var"])) > 0).sum())})
add("S1 complete case", "cc", "S1_complete_case", "ANY")
for t, lab in [("NF1", "1 form"), ("NF2", "2 forms"), ("NF3P", "3+ forms")]:
    add(f"S2/E2 dose: {lab} vs none", "mi", "S2_dose", t)
add("S3 modal grade only", "mi", "S3_modal_grade", "ANY")
add("S4 drop 4-5 forms", "mi", "S4_drop_4plus_forms", "ANY")
add("S5 negative control: FEELSAFE (WLE units)", "cc", "S5_negctrl_feelsafe", "ANY", scale_sd=1.0)
add("S7 adjusted for math achievement (10 PVs)", "cc", "S7_adjust_math_pv", "ANY")
add("S9a 'nothing ticked' = non-participant", "cc", "S9a_nothing_as_none", "ANY")
add("S9b contradictory = participant", "cc", "S9b_contradictory_as_some", "ANY")
add("S9c straight-liners = participant", "cc", "S9c_straightline_as_some", "ANY")
low_miss = sysdf[sysdf.n_exposure_missing_pct <= 40].CNT
add("S10 systems with <=40% exposure missing", "mi", "primary", "ANY", subset=set(low_miss))
add("E1 interaction ANY x ESCS (per ESCS unit)", "mi", "E1_escs", "ANYxESCS")
add("E1 interaction ANY x female", "mi", "E1_sex", "ANYxFEMALE")
add("E1 interaction ANY x below modal grade", "mi", "E1_grade", "ANYxBELOW")
add("E1 interaction ANY x above modal grade", "mi", "E1_grade", "ANYxABOVE")
for f in ["one_on_one", "online", "video", "small_group", "large_group"]:
    add(f"E2 form: {f} (joint model)", "cc", "E2_forms", f)
add("E4 math anxiety ANXMAT (WLE units)", "cc", "E4_anxmat", "ANY", scale_sd=1.0)
add("E4 psychosomatic complaints (1-5 scale)", "cc", "E4_psysom", "ANY", scale_sd=None)
tab = pd.DataFrame([r for r in rows if r])
tab.to_csv(os.path.join(RES, "all_estimates.csv"), index=False, float_format="%.5g")

# ---- primary, E-value, random effects
prim = tab.iloc[0]
d_lo, d_hi = prim.ci_low / POOLED_SD, prim.ci_high / POOLED_SD
ev_point, ev_ci = evalue_from_d(prim.std_estimate, d_lo, d_hi)
p = collect("mi", "primary", "ANY").merge(sysdf, on=["CNT", "OECD"])
re = dersimonian_laird(p.est, p["var"])
mr = dersimonian_laird(p.est, p["var"], X=(p.prev - p.prev.mean()) * 10)  # per 10 percentage points
mr_oecd = dersimonian_laird(p.est, p["var"], X=np.column_stack([(p.prev - p.prev.mean()) * 10, p.OECD]))
summary = {
    "systems": int(len(p)), "students": int(sysdf.n.sum()), "students_complete_case": int(sysdf.n_cc.sum()),
    "pooled_within_system_sd_ls": POOLED_SD,
    "primary_international_average": {k: float(prim[k]) for k in ["estimate", "se", "ci_low", "ci_high", "p", "std_estimate", "oecd_estimate", "oecd_se"]},
    "primary_std_ci": [d_lo, d_hi],
    "evalue_point": ev_point, "evalue_ci": ev_ci,
    "S8_random_effects": {"estimate": float(re["coef"][0]), "se": float(re["se"][0]), "ci": list(ci(re["coef"][0], re["se"][0])),
                          "tau": re["tau"], "I2": re["I2"], "Q": re["Q"], "df": re["df"],
                          "prediction_interval_approx": [float(re["coef"][0] - 1.96 * np.sqrt(re["tau2"] + re["se"][0] ** 2)),
                                                         float(re["coef"][0] + 1.96 * np.sqrt(re["tau2"] + re["se"][0] ** 2))]},
    "E3_meta_regression_prevalence_per10pp": {"slope": float(mr["coef"][1]), "se": float(mr["se"][1]), "ci": list(ci(mr["coef"][1], mr["se"][1])),
                                               "p": float(pval(mr["coef"][1], mr["se"][1])), "tau_residual": mr["tau"]},
    "E3_meta_regression_prevalence_adj_oecd": {"slope": float(mr_oecd["coef"][1]), "se": float(mr_oecd["se"][1]),
                                                "p": float(pval(mr_oecd["coef"][1], mr_oecd["se"][1]))},
    "participation_rate": {"mean": float(p.prev.mean()), "min": [p.loc[p.prev.idxmin(), "CNT"], float(p.prev.min())],
                           "max": [p.loc[p.prev.idxmax(), "CNT"], float(p.prev.max())]},
    "mean_life_satisfaction": float(sysdf.ls_mean.mean()),
}
json.dump(summary, open(os.path.join(RES, "summary.json"), "w"), indent=1)
p["se"] = np.sqrt(p["var"])
p["prev_se"] = np.sqrt(p["prev_var"])
p[["CNT", "OECD", "n", "n_cc", "n_exposure_missing_pct", "prev", "prev_se", "ls_mean", "ls_sd", "est", "se"]].rename(
    columns={"est": "primary_est", "se": "primary_se", "prev": "participation_rate"}).to_csv(
    os.path.join(RES, "system_estimates.csv"), index=False, float_format="%.4f")
pd.set_option("display.width", 220)
print(tab[["analysis", "systems", "estimate", "ci_low", "ci_high", "p", "std_estimate", "systems_negative_sig", "systems_positive_sig"]].to_string(index=False, float_format=lambda x: f"{x:.3f}"))
print(json.dumps(summary, indent=1))
