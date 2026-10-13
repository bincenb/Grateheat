"""Primary, secondary, exploratory and sensitivity analyses (protocol sections 7.2-7.6).
Every model: weighted least squares, each system's weights rescaled to sum to 1 within
the analysis sample, Fay-BRR variance (80 replicates), Rubin's rules over M = 20
imputations. Writes output/tables/*.csv and output/results.pkl.
"""
import os
import sys
import time
from multiprocessing.pool import ThreadPool

import numpy as np
import pandas as pd
import patsy

sys.path.insert(0, os.path.dirname(__file__))
from brr import REPW, brr_fit, rubin, wmean, wsd, dersimonian_laird, evalue_from_d  # noqa: E402

T = "output/tables"
a = pd.read_pickle("data_work/analytic.pkl")
imps = pd.read_pickle("data_work/imputations.pkl")
M = len(imps)
for im in imps:
    assert (im.CNTSTUID.to_numpy() == a.CNTSTUID.to_numpy()).all()

W0 = a.W_FSTUWT.to_numpy()
WR = a[REPW].to_numpy()
CNT = a.CNT.to_numpy()
SYSTEMS = sorted(a.CNT.unique())
OUTCOMES = ["psc", "mhc", "sleep", "psych", "soma", "srh", "height_z"]


def design(D, extra=(), fe=True, spline=False, with_ban=True):
    """Design matrix: intercept, ban, pre-specified covariates, system FE, extra columns."""
    cols = {"const": np.ones(len(D))}
    if with_ban:
        cols["ban"] = D.ban.to_numpy(float)
    cols["female"] = D.female.to_numpy(float)
    cols["grade_below"] = (D.grade < 0).to_numpy(float)
    cols["grade_above"] = (D.grade > 0).to_numpy(float)
    cols["immig2"] = (D.immig == 2).to_numpy(float)
    cols["immig3"] = (D.immig == 3).to_numpy(float)
    cols["repeat"] = D.repeat.to_numpy(float)
    cols["private"] = D.private.to_numpy(float)
    for k in (2, 3, 4, 5):
        cols[f"comm{k}"] = (D.commsize == k).to_numpy(float)
    cols["lschsize"] = D.lschsize.to_numpy(float)
    if spline:
        for v in ("escs", "age", "sch_escs"):
            B = np.asarray(patsy.dmatrix(f"cr(x, df=4) - 1", {"x": D[v].to_numpy(float)}))
            for j in range(B.shape[1] - 1):  # drop one column: intercept already in model
                cols[f"{v}_s{j}"] = B[:, j]
    else:
        cols["escs"] = D.escs.to_numpy(float)
        cols["age"] = D.age.to_numpy(float)
        cols["sch_escs"] = D.sch_escs.to_numpy(float)
    if fe:
        for c in SYSTEMS[1:]:
            cols[f"c_{c}"] = (D.CNT == c).to_numpy(float)
    for name, vec in extra:
        cols[name] = np.asarray(vec, float)
    return np.column_stack(list(cols.values())), list(cols.keys())


def scaled_weights(mask):
    w = W0[mask].copy()
    Wr = WR[mask].copy()
    cn = CNT[mask]
    for c in np.unique(cn):
        s = cn == c
        f = 1.0 / w[s].sum()
        w[s] *= f
        Wr[s] *= f
    return w, Wr


def full_frame(m):
    D = imps[m].copy()
    for v in OUTCOMES + ["allfive"] + [f"PV{i}MATH" for i in range(1, 11)]:
        D[v] = a[v].to_numpy()
    return D


FRAMES = None


def _init():
    global FRAMES
    FRAMES = [full_frame(m) for m in range(M)]


def _one(args):
    m, spec = args
    D = FRAMES[m] if spec.get("cc") is None else spec["cc"]
    y = D[spec["y"]].to_numpy(float)
    mask = ~np.isnan(y)
    if spec.get("subset") is not None:
        mask &= spec["subset"](D, m)
    extra = spec.get("extra", lambda D, m: [])(D, m)
    X, names = design(D, extra=extra, fe=spec.get("fe", True), spline=spec.get("spline", False),
                      with_ban=spec.get("with_ban", True))
    mask &= ~np.isnan(X).any(axis=1)
    w, Wr = scaled_weights(mask)
    est, var = brr_fit(X[mask], y[mask], w, Wr)
    idx = [names.index(t) for t in spec["terms"]]
    return est[idx], var[idx], int(mask.sum()), int(D.loc[mask, "CNTSCHID"].nunique())


def run(pool, label, spec, group, scale=1.0):
    t0 = time.time()
    ms = [0] if spec.get("cc") is not None else range(M)
    res = pool.map(_one, [(m, spec) for m in ms])
    rows = []
    for j, term in enumerate(spec["terms"]):
        r = rubin([x[0][j] * scale for x in res], [x[1][j] * scale ** 2 for x in res])
        rows.append(dict(group=group, analysis=label, outcome=spec["y"], term=term,
                         n=res[0][2], schools=res[0][3], **r))
    print(f"{label:<55s} {rows[0]['est']:+.4f} ({rows[0]['lo']:+.4f}, {rows[0]['hi']:+.4f}) "
          f"p={rows[0]['p']:.3g}  n={rows[0]['n']}  [{time.time() - t0:.0f}s]", flush=True)
    return rows


def descriptives():
    """Table 1 (observed data, each system weighted equally) and per-system table."""
    w, _ = scaled_weights(np.ones(len(a), bool))
    D = a.copy()
    D["w"] = w
    D["grade_below"] = (D.grade < 0).astype(float).where(D.grade.notna())
    D["immig_any"] = (D.immig > 1).astype(float).where(D.immig.notna())
    D["bigcity"] = (D.commsize == 5).astype(float).where(D.commsize.notna())
    D["schsize"] = np.exp(D.lschsize)
    rows = [("Students (unweighted n)", "n"), ("Schools (unweighted n)", "schools"),
            ("Female, %", "female"), ("Age, years", "age"), ("Below modal grade, %", "grade_below"),
            ("ESCS", "escs"), ("Immigrant background, %", "immig_any"), ("Repeated a grade, %", "repeat"),
            ("Private school, %", "private"), ("City >1 million, %", "bigcity"),
            ("School enrolment", "schsize"), ("School mean ESCS", "sch_escs"),
            ("Psychosomatic score (1-5)", "psc"), ("Multiple health complaints, %", "mhc"),
            ("Difficulty getting to sleep (1-5)", "sleep"), ("Psychological subscale (1-5)", "psych"),
            ("Somatic subscale (1-5)", "soma"), ("Self-rated health (1 excellent-4 poor)", "srh")]
    pct = {"female", "grade_below", "immig_any", "repeat", "private", "bigcity", "mhc"}
    groups = {"All": D, "Ban": D[D.ban == 1], "No ban": D[D.ban == 0], "Ban missing": D[D.ban.isna()]}
    out = []
    for lab, v in rows:
        r = {"variable": lab}
        for g, G in groups.items():
            if v == "n":
                r[g] = len(G)
            elif v == "schools":
                r[g] = G.CNTSCHID.nunique()
            else:
                x = wmean(G[v].to_numpy(float), G.w.to_numpy())
                r[g] = round(100 * x, 1) if v in pct else round(x, 2)
        r["% missing"] = "" if v in ("n", "schools") else round(100 * D[v].isna().mean(), 1)
        out.append(r)
    t1 = pd.DataFrame(out)
    t1.to_csv(f"{T}/table1_descriptives.csv", index=False)
    print(t1.to_string(index=False))

    per = []
    for c, G in D.groupby("CNT"):
        ww = G.W_FSTUWT.to_numpy()
        per.append(dict(system=c, oecd=int(G.oecd.iloc[0]), students=len(G), schools=G.CNTSCHID.nunique(),
                        ban_pct=round(100 * wmean(G.ban.to_numpy(float), ww), 1),
                        ban_missing_pct=round(100 * G.ban.isna().mean(), 1),
                        psc_mean=round(wmean(G.psc.to_numpy(float), ww), 2),
                        mhc_pct=round(100 * wmean(G.mhc.to_numpy(float), ww), 1),
                        sleep_mean=round(wmean(G.sleep.to_numpy(float), ww), 2)))
    per = pd.DataFrame(per)
    per.to_csv(f"{T}/table2_by_system.csv", index=False)
    print(per.to_string(index=False))
    return wsd(a.psc.to_numpy(float), w)


if __name__ == "__main__":
    sd_psc = descriptives()
    print(f"\nWeighted SD of psc (each system weighted equally): {sd_psc:.4f}\n")

    # complete-case frame for S1 (observed values only; system-wide missing stays missing)
    cc_frame = a
    res = []
    _init()
    with ThreadPool(4) as pool:
        P = dict(y="psc", terms=["ban"])
        # ---- primary ----
        res += run(pool, "PRIMARY: ban -> psychosomatic score (1-5)", P, "primary")
        prim = res[-1]
        # ---- secondary outcomes ----
        res += run(pool, "O2 multiple health complaints (pp)", dict(y="mhc", terms=["ban"]), "secondary", 100)
        res += run(pool, "O3 difficulty getting to sleep (1-5)", dict(y="sleep", terms=["ban"]), "secondary")
        res += run(pool, "O4a psychological subscale (1-5)", dict(y="psych", terms=["ban"]), "secondary")
        res += run(pool, "O4b somatic subscale (1-5)", dict(y="soma", terms=["ban"]), "secondary")
        res += run(pool, "O5 self-rated health (1-4, higher=worse)", dict(y="srh", terms=["ban"]), "secondary")
        # ---- exploratory: effect modification ----
        res += run(pool, "E1a ban x female", dict(y="psc", terms=["ban_x_female", "ban"],
                   extra=lambda D, m: [("ban_x_female", D.ban * D.female)]), "exploratory")
        res += run(pool, "E1b ban x ESCS (CRI excluded)", dict(y="psc", terms=["ban_x_escs", "ban"],
                   subset=lambda D, m: (D.CNT != "CRI").to_numpy(),
                   extra=lambda D, m: [("ban_x_escs", D.ban * D.escs)]), "exploratory")
        res += run(pool, "E1c ban x modal grade", dict(y="psc", terms=["ban_x_modal", "ban"],
                   extra=lambda D, m: [("ban_x_modal", D.ban * (D.grade == 0))]), "exploratory")
        res += run(pool, "E2a ban x OECD member", dict(y="psc", terms=["ban_x_oecd", "ban"],
                   extra=lambda D, m: [("ban_x_oecd", D.ban * D.oecd)]), "exploratory")
        res += run(pool, "E3 policy combination (ref: no ban, no statement)",
                   dict(y="psc", terms=["ban_stmt", "ban_nostmt", "noban_stmt"],
                        extra=lambda D, m: [("ban_stmt", D.ban * D.stmt), ("ban_nostmt", D.ban * (1 - D.stmt)),
                                            ("noban_stmt", (1 - D.ban) * D.stmt)], with_ban=False),
                   "exploratory")
        # ---- per-system (E2b forest plot, S9) ----
        per = []
        for c in SYSTEMS:
            r = run(pool, f"E2b system {c}", dict(y="psc", terms=["ban"], fe=False,
                    subset=lambda D, m, c=c: (D.CNT == c).to_numpy()), "system")
            r[0]["system"] = c
            per += r
        res += per
        for oy, lab in (("sleep", "sleep"), ("mhc", "mhc")):
            for c in SYSTEMS:
                r = run(pool, f"E2c system {c} ({lab})", dict(y=oy, terms=["ban"], fe=False,
                        subset=lambda D, m, c=c: (D.CNT == c).to_numpy()), f"system_{lab}",
                        100 if oy == "mhc" else 1)
                r[0]["system"] = c
                res += r
        # ---- sensitivity ----
        res += run(pool, "S1 complete case", dict(y="psc", terms=["ban"], cc=cc_frame), "sensitivity")
        res += run(pool, "S2 splines for ESCS, age, school ESCS", dict(y="psc", terms=["ban"], spline=True), "sensitivity")
        res += run(pool, "S3 modal grade only", dict(y="psc", terms=["ban"],
                   subset=lambda D, m: (D.grade == 0).to_numpy()), "sensitivity")
        res += run(pool, "S4 drop all-9-symptoms-daily responders", dict(y="psc", terms=["ban"],
                   subset=lambda D, m: (D.allfive != 1).to_numpy()), "sensitivity")
        res += run(pool, "S5 negative control: height (z)", dict(y="height_z", terms=["ban"]), "sensitivity")
        for c in SYSTEMS:
            res += run(pool, f"S7 leave out {c}", dict(y="psc", terms=["ban"],
                       subset=lambda D, m, c=c: (D.CNT != c).to_numpy()), "loo")
        res += run(pool, "S8 + other device-policy items", dict(y="psc", terms=["ban"],
                   extra=lambda D, m: [("stmt", D.stmt), ("tchrules", D.tchrules)]), "sensitivity")
        res += run(pool, "S10 public schools only", dict(y="psc", terms=["ban"],
                   subset=lambda D, m: (D.private == 0).to_numpy()), "sensitivity")
        res += run(pool, "S11 + mathematics achievement (PVs)", dict(y="psc", terms=["ban"],
                   extra=lambda D, m: [("math", D[f"PV{m % 10 + 1}MATH"] / 100)]), "sensitivity")
        res += run(pool, "S12 drop CRI, MAC, NZL", dict(y="psc", terms=["ban"],
                   subset=lambda D, m: (~D.CNT.isin(["CRI", "MAC", "NZL"])).to_numpy()), "sensitivity")

    R = pd.DataFrame(res)
    # S9 random-effects pooling of system estimates
    ps = R[R.group == "system"]
    dl = dersimonian_laird(ps.est.to_numpy(), ps.se.to_numpy())
    R = pd.concat([R, pd.DataFrame([dict(group="sensitivity", analysis="S9 random-effects pooling (DL)",
                                         outcome="psc", term="ban", n=int(ps.n.sum()),
                                         schools=int(ps.schools.sum()), est=dl["est"], se=dl["se"],
                                         lo=dl["lo"], hi=dl["hi"], p=dl["p"])])], ignore_index=True)
    het = {k: dl[k] for k in ("tau2", "I2", "Q", "pQ", "k")}
    print("S9 DL:", {k: round(v, 4) for k, v in dl.items()})
    # S6 E-value
    d, dlo, dhi = prim["est"] / sd_psc, prim["lo"] / sd_psc, prim["hi"] / sd_psc
    ev, ev_ci = evalue_from_d(d, dlo, dhi)
    summary = dict(sd_psc=sd_psc, d=d, d_lo=dlo, d_hi=dhi, evalue=ev, evalue_ci=ev_ci, heterogeneity=het)
    print("Standardised primary effect d =", round(d, 4), (round(dlo, 4), round(dhi, 4)),
          " E-value:", round(ev, 3), "CI:", round(ev_ci, 3))
    R.to_csv(f"{T}/results_all.csv", index=False)
    pd.to_pickle(dict(results=R, summary=summary), "output/results.pkl")
