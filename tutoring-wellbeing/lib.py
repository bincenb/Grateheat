"""Shared statistics for the PISA 2022 analysis.

- BRR (Fay, k = 0.5, 80 replicates) weighted least squares
- Rubin's rules (multiple imputation) and the PISA plausible-value combination
- Predictive-mean-matching chained-equations imputation
- International average and random-effects pooling across systems
"""
import numpy as np
import pandas as pd

N_REP = 80
FAY_K = 0.5
REP_FACTOR = 1.0 / (N_REP * (1 - FAY_K) ** 2)  # = 1/20
WCOLS = ["W_FSTUWT"] + [f"W_FSTURWT{i}" for i in range(1, N_REP + 1)]


# ---------------------------------------------------------------- BRR WLS
def brr_wls(X, y, W):
    """Weighted least squares with full weight and 80 replicate weights.

    X: (n, p) design, y: (n,), W: (n, 81) with column 0 the final weight.
    Returns (beta (p,), sampling variance (p,), replicate betas (80, p)).
    """
    WX = W.T[:, :, None] * X[None, :, :]          # (81, n, p)
    XtWX = np.matmul(WX.transpose(0, 2, 1), X)    # (81, p, p)
    XtWy = np.matmul(WX.transpose(0, 2, 1), y)    # (81, p)
    try:
        B = np.linalg.solve(XtWX, XtWy[..., None])[..., 0]  # (81, p)
    except np.linalg.LinAlgError:
        B = np.stack([np.linalg.pinv(a) @ b for a, b in zip(XtWX, XtWy)])
    beta, reps = B[0], B[1:]
    var = REP_FACTOR * ((reps - beta) ** 2).sum(axis=0)
    return beta, var, reps


def brr_mean(y, W):
    """Weighted mean with BRR sampling variance."""
    m = (W * y[:, None]).sum(0) / W.sum(0)
    return m[0], REP_FACTOR * ((m[1:] - m[0]) ** 2).sum()


def combine(estimates, variances):
    """Rubin's rules; also the PISA PV rule (same formula with M = 10).

    estimates, variances: arrays of shape (M, ...). Returns (Q, T): the
    combined estimate and its total variance.
    """
    q = np.asarray(estimates, float)
    u = np.asarray(variances, float)
    M = q.shape[0]
    Q = q.mean(0)
    U = u.mean(0)
    Bv = q.var(0, ddof=1) if M > 1 else np.zeros_like(Q)
    T = U + (1 + 1 / M) * Bv
    return Q, T


# ---------------------------------------------------------------- pooling across systems
def international_average(est, var):
    """PISA international average: each system counts equally."""
    est, var = np.asarray(est), np.asarray(var)
    C = len(est)
    return est.mean(), np.sqrt(var.sum()) / C


def dersimonian_laird(est, var, X=None):
    """Random-effects pooling (or meta-regression on X) by DerSimonian–Laird.

    Returns dict with coefficients, SEs, tau2, I2, Q.
    """
    y = np.asarray(est, float)
    v = np.asarray(var, float)
    k = len(y)
    Xm = np.ones((k, 1)) if X is None else np.column_stack([np.ones(k), X])
    w = 1 / v
    XtW = Xm.T * w
    b_fe = np.linalg.solve(XtW @ Xm, XtW @ y)
    resid = y - Xm @ b_fe
    Q = float((w * resid ** 2).sum())
    P = np.diag(w) - (XtW.T @ np.linalg.solve(XtW @ Xm, XtW))
    df = k - Xm.shape[1]
    tau2 = max(0.0, (Q - df) / np.trace(P))
    ws = 1 / (v + tau2)
    XtWs = Xm.T * ws
    cov = np.linalg.inv(XtWs @ Xm)
    b = cov @ XtWs @ y
    I2 = max(0.0, (Q - df) / Q) if Q > 0 else 0.0
    return {"coef": b, "se": np.sqrt(np.diag(cov)), "tau2": tau2, "tau": np.sqrt(tau2), "I2": I2, "Q": Q, "df": df}


# ---------------------------------------------------------------- imputation
def _pmm_draw(rng, Xo, yo, Xm, k=5):
    """One Bayesian PMM draw (type-1 matching) for the missing rows."""
    n, p = Xo.shape
    XtX = Xo.T @ Xo + 1e-6 * np.eye(p)
    XtX_inv = np.linalg.inv(XtX)
    bhat = XtX_inv @ Xo.T @ yo
    resid = yo - Xo @ bhat
    df = max(n - p, 1)
    sigma2 = (resid @ resid) / rng.chisquare(df)
    bstar = bhat + np.linalg.cholesky(sigma2 * XtX_inv + 1e-12 * np.eye(p)) @ rng.standard_normal(p)
    pred_o = Xo @ bhat
    pred_m = Xm @ bstar
    order = np.argsort(pred_o)
    so = pred_o[order]
    pos = np.searchsorted(so, pred_m)
    # take 2k candidates around the insertion point, keep the k closest
    offs = np.arange(-k, k)
    cand = np.clip(pos[:, None] + offs[None, :], 0, len(so) - 1)
    dist = np.abs(so[cand] - pred_m[:, None])
    nearest = np.take_along_axis(cand, np.argsort(dist, axis=1)[:, :k], axis=1)
    pick = nearest[np.arange(len(pred_m)), rng.integers(0, k, len(pred_m))]
    return yo[order][pick]


def mice_pmm(df, impute_cols, aux_cols, m, iters, seed):
    """Chained-equations PMM. Returns a list of m completed copies of impute_cols.

    Every column in impute_cols and aux_cols is numeric. Aux columns with
    missing values are mean-filled and given a missing indicator, and are
    used as predictors only.
    """
    rng = np.random.default_rng(seed)
    data = df[impute_cols].to_numpy(float).copy()
    miss = np.isnan(data)
    aux = []
    for c in aux_cols:
        a = df[c].to_numpy(float)
        na = np.isnan(a)
        a = np.where(na, np.nanmean(a) if (~na).any() else 0.0, a)
        aux.append(a)
        if na.any() and (~na).any():
            aux.append(na.astype(float))
    aux = np.column_stack(aux) if aux else np.zeros((len(df), 0))
    out = []
    for _ in range(m):
        cur = data.copy()
        # start from random observed values
        for j in range(cur.shape[1]):
            obs = cur[~miss[:, j], j]
            if miss[:, j].any():
                cur[miss[:, j], j] = rng.choice(obs, miss[:, j].sum())
        for _ in range(iters):
            for j in range(cur.shape[1]):
                mj = miss[:, j]
                if not mj.any():
                    continue
                others = np.delete(cur, j, axis=1)
                X = np.column_stack([np.ones(len(cur)), others, aux])
                cur[mj, j] = _pmm_draw(rng, X[~mj], cur[~mj, j], X[mj])
        out.append(pd.DataFrame(cur, columns=impute_cols, index=df.index))
    return out


# ---------------------------------------------------------------- reporting helpers
def ci(est, se, z=1.959964):
    return est - z * se, est + z * se


def pval(est, se):
    from scipy.stats import norm
    return 2 * norm.sf(abs(est / se))


def evalue_from_d(d, lo, hi):
    """E-value for a standardized mean difference (VanderWeele & Ding 2017)."""
    def ev(x):
        rr = np.exp(0.91 * abs(x))
        return rr + np.sqrt(rr * (rr - 1))
    point = ev(d)
    near = 0.0 if lo <= 0 <= hi else (lo if d > 0 else hi)
    return point, (1.0 if near == 0.0 else ev(near))
