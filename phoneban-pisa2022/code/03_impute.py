"""Two-level multiple imputation by chained equations with predictive mean matching
(protocol 7.5). M = 20, 15 iterations, 5 donors, seed 20221.

Stage A (school level): ban, stmt, tchrules, private, commsize, lschsize, sch_escs,
  given system and school means of the student variables (incl. the outcome).
Stage B (student level): female, grade, escs, immig, repeat, given system, the
  stage-A school variables, the outcomes and log final weight.
The outcome is never imputed. Output: data_work/imputations.pkl (list of M frames).
"""
import numpy as np
import pandas as pd

M, ITERS, K, SEED = 20, 15, 5, 20221

a = pd.read_pickle("data_work/analytic.pkl")
rng = np.random.default_rng(SEED)


def pmm_draw(y_obs, X_obs, X_mis, rng):
    """One Bayesian-bootstrap-free PMM step (type-1 matching, as in mice::mice.impute.pmm)."""
    XtX = X_obs.T @ X_obs + 1e-6 * np.eye(X_obs.shape[1])
    beta = np.linalg.solve(XtX, X_obs.T @ y_obs)
    resid = y_obs - X_obs @ beta
    df = max(len(y_obs) - X_obs.shape[1], 1)
    sigma2 = resid @ resid / rng.chisquare(df)
    L = np.linalg.cholesky(np.linalg.inv(XtX) * sigma2 + 1e-12 * np.eye(X_obs.shape[1]))
    beta_star = beta + L @ rng.standard_normal(X_obs.shape[1])
    yhat_obs = X_obs @ beta
    yhat_mis = X_mis @ beta_star
    order = np.argsort(yhat_obs)
    sorted_obs = yhat_obs[order]
    pos = np.searchsorted(sorted_obs, yhat_mis)
    cand = np.clip(pos[:, None] + np.arange(-K, K)[None, :], 0, len(sorted_obs) - 1)
    dist = np.abs(sorted_obs[cand] - yhat_mis[:, None])
    nearest = np.take_along_axis(cand, np.argsort(dist, axis=1)[:, :K], axis=1)
    pick = nearest[np.arange(len(yhat_mis)), rng.integers(0, K, len(yhat_mis))]
    return y_obs[order][pick]


def fill_system_missing(df, targets, log=None):
    """A variable that is missing for every unit in a system cannot be imputed from
    within-system information (the system dummy has no observed rows). Fill it with a
    constant (0) instead; the system fixed effect absorbs the constant, so that system
    is simply not adjusted for the variable. See DEVIATIONS.md."""
    df = df.copy()
    for v in targets:
        allmiss = df.groupby("CNT")[v].transform(lambda x: x.isna().all())
        if allmiss.any():
            if log is not None:
                log.add((v, tuple(sorted(df.loc[allmiss, "CNT"].unique()))))
            df.loc[allmiss, v] = 0.0
    return df


def mice(df, targets, fixed, rng, iters=ITERS):
    """Chained-equations PMM. df: DataFrame; targets: columns to impute; fixed: complete predictors."""
    df = df.copy()
    miss = {v: df[v].isna().to_numpy() for v in targets}
    for v in targets:  # start from random observed values
        obs = df.loc[~miss[v], v].to_numpy()
        df.loc[miss[v], v] = rng.choice(obs, miss[v].sum())
    F = np.column_stack([np.ones(len(df)), df[fixed].to_numpy(float)])
    for _ in range(iters):
        for v in targets:
            if not miss[v].any():
                continue
            others = [t for t in targets if t != v]
            X = np.column_stack([F, df[others].to_numpy(float)])
            y = df[v].to_numpy(float)
            m = miss[v]
            df.loc[m, v] = pmm_draw(y[~m], X[~m], X[m], rng)
    return df


cnt_d = pd.get_dummies(a.CNT, prefix="c", drop_first=True, dtype=float)
a = pd.concat([a, cnt_d], axis=1)
CNTD = list(cnt_d.columns)

# ---------- stage A: one row per school ----------
a["immig_nn"] = (a.immig > 1).astype(float).where(a.immig.notna())
sch = a.groupby("CNTSCHID").agg(
    CNT=("CNT", "first"), ban=("ban", "first"), stmt=("stmt", "first"),
    tchrules=("tchrules", "first"), private=("private", "first"),
    commsize=("commsize", "first"), lschsize=("lschsize", "first"),
    sch_escs=("sch_escs", "first"), m_psc=("psc", "mean"), m_female=("female", "mean"),
    m_age=("age", "mean"), m_grade=("grade", "mean"), m_repeat=("repeat", "mean"),
    m_immig=("immig_nn", "mean"), n=("psc", "size")).reset_index()
sch = pd.concat([sch, pd.get_dummies(sch.CNT, prefix="c", drop_first=True, dtype=float)], axis=1)
sch["log_n"] = np.log(sch.n)
for c in ["m_female", "m_age", "m_grade", "m_repeat", "m_immig"]:
    sch[c] = sch[c].fillna(sch.groupby("CNT")[c].transform("mean"))
SCH_T = ["ban", "stmt", "tchrules", "private", "commsize", "lschsize", "sch_escs"]
SCH_F = CNTD + ["m_psc", "m_female", "m_age", "m_grade", "m_repeat", "m_immig", "log_n"]

# ---------- stage B ----------
STU_T = ["female", "grade", "escs", "immig", "repeat"]
STU_F = CNTD + SCH_T + ["age", "psc", "psych", "soma", "mhc", "lw"]
a["lw"] = np.log(a.W_FSTUWT)

SYSMISS = set()
sch = fill_system_missing(sch, SCH_T, SYSMISS)
a = fill_system_missing(a, STU_T, SYSMISS)
print("Filled as constant (system-wide missing):", sorted(SYSMISS))
pd.DataFrame(sorted(SYSMISS), columns=["variable", "systems"]).to_csv(
    "output/tables/system_missing_covariates.csv", index=False)

imps = []
for m in range(M):
    r = np.random.default_rng(rng.integers(1 << 32))
    s_imp = mice(sch[["CNTSCHID", "CNT"] + SCH_T + SCH_F], SCH_T, SCH_F, r)
    b = a.drop(columns=SCH_T).merge(s_imp[["CNTSCHID"] + SCH_T], on="CNTSCHID", how="left")
    assert len(b) == len(a) and (b.CNTSTUID.to_numpy() == a.CNTSTUID.to_numpy()).all()
    b = mice(b, STU_T, STU_F, r)
    keep = ["CNT", "CNTSCHID", "CNTSTUID"] + SCH_T + ["female", "age", "grade", "escs", "immig",
                                                      "repeat", "oecd"]
    imps.append(b[keep].copy())
    print(f"imputation {m + 1}/{M}: ban share {b.ban.mean():.3f}, escs mean {b.escs.mean():.3f}")

pd.to_pickle(imps, "data_work/imputations.pkl")

# diagnostics: observed vs imputed means for each imputed variable
diag = []
for v in SCH_T + STU_T:
    obs = a[v].dropna()
    mis = a[v].isna()
    if mis.any():
        imp_vals = np.concatenate([im.loc[mis.to_numpy(), v].to_numpy() for im in imps])
        diag.append(dict(variable=v, n_missing=int(mis.sum()), observed_mean=round(obs.mean(), 3),
                         imputed_mean=round(float(np.mean(imp_vals)), 3)))
pd.DataFrame(diag).to_csv("output/tables/imputation_diagnostics.csv", index=False)
print(pd.DataFrame(diag).to_string(index=False))
