"""Survey estimation helpers for PISA 2022.

Fay's BRR with 80 replicates and k = 0.5 (PISA 2022 Technical Report, ch. 9):
    V = 1 / (G * (1 - k)^2) * sum_r (theta_r - theta)^2 = 0.05 * sum_r (...)
Rubin's rules combine estimates over imputations or plausible values.
"""
import numpy as np
from scipy import stats

G = 80
FAY = 1.0 / (G * (1 - 0.5) ** 2)
REPW = [f"W_FSTURWT{i}" for i in range(1, G + 1)]


def wls_all(X, y, W):
    """Weighted least squares for each column of W (n x R). Returns R x p coefficients."""
    out = np.empty((W.shape[1], X.shape[1]))
    for r in range(W.shape[1]):
        Xw = X * W[:, r, None]
        out[r] = np.linalg.lstsq(X.T @ Xw, Xw.T @ y, rcond=None)[0]
    return out


def brr_fit(X, y, w, Wrep):
    """Point estimate with final weight w, BRR variance from replicate weights Wrep (n x 80)."""
    b = wls_all(X, y, np.column_stack([w, Wrep]))
    est = b[0]
    var = FAY * ((b[1:] - est) ** 2).sum(axis=0)
    return est, var


def brr_stat(fun, w, Wrep):
    """Any scalar/vector statistic fun(weights) with BRR variance."""
    est = np.asarray(fun(w))
    reps = np.array([fun(Wrep[:, r]) for r in range(Wrep.shape[1])])
    return est, FAY * ((reps - est) ** 2).sum(axis=0)


def rubin(ests, vars_, df_com=G):
    """Combine M estimates and sampling variances. Returns dict with est, se, ci, p, df.
    Barnard-Rubin small-sample degrees of freedom with complete-data df = 80."""
    ests, vars_ = np.asarray(ests, float), np.asarray(vars_, float)
    M = len(ests)
    q = ests.mean()
    u = vars_.mean()
    if M == 1:
        t, df = u, df_com
    else:
        b = ests.var(ddof=1)
        t = u + (1 + 1 / M) * b
        lam = (1 + 1 / M) * b / t if t > 0 else 0.0
        df_old = (M - 1) / lam ** 2 if lam > 0 else np.inf
        df_obs = (df_com + 1) / (df_com + 3) * df_com * (1 - lam)
        df = 1 / (1 / df_old + 1 / df_obs)
    se = np.sqrt(t)
    tq = stats.t.ppf(0.975, df)
    p = 2 * stats.t.sf(abs(q / se), df) if se > 0 else np.nan
    return dict(est=q, se=se, lo=q - tq * se, hi=q + tq * se, p=p, df=df,
                fmi=((1 + 1 / M) * ests.var(ddof=1) / t) if M > 1 else 0.0)


def wmean(x, w):
    m = ~np.isnan(x)
    return np.sum(x[m] * w[m]) / np.sum(w[m])


def wsd(x, w):
    m = ~np.isnan(x)
    mu = np.sum(x[m] * w[m]) / np.sum(w[m])
    return np.sqrt(np.sum(w[m] * (x[m] - mu) ** 2) / np.sum(w[m]))


def dersimonian_laird(est, se):
    est, se = np.asarray(est), np.asarray(se)
    w = 1 / se ** 2
    fe = np.sum(w * est) / w.sum()
    Q = np.sum(w * (est - fe) ** 2)
    k = len(est)
    C = w.sum() - np.sum(w ** 2) / w.sum()
    tau2 = max(0.0, (Q - (k - 1)) / C)
    wr = 1 / (se ** 2 + tau2)
    re = np.sum(wr * est) / wr.sum()
    se_re = np.sqrt(1 / wr.sum())
    I2 = max(0.0, (Q - (k - 1)) / Q) if Q > 0 else 0.0
    pQ = stats.chi2.sf(Q, k - 1)
    return dict(est=re, se=se_re, lo=re - 1.96 * se_re, hi=re + 1.96 * se_re,
                p=2 * stats.norm.sf(abs(re / se_re)), tau2=tau2, I2=I2, Q=Q, pQ=pQ, k=k)


def evalue_from_d(d, lo, hi):
    """E-value for a standardised mean difference (VanderWeele & Ding 2017): RR ~ exp(0.91 d)."""
    def ev(rr):
        rr = rr if rr >= 1 else 1 / rr
        return rr + np.sqrt(rr * (rr - 1))
    e_point = ev(np.exp(0.91 * d))
    if lo <= 0 <= hi:
        e_ci = 1.0
    else:
        near = lo if d > 0 else hi
        e_ci = ev(np.exp(0.91 * near))
    return e_point, e_ci
