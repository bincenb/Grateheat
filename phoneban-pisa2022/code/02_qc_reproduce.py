"""Quality check: reproduce the OECD's published PISA 2022 mean mathematics scores
for the 15 WBQ systems (PISA 2022 Results Vol. I, Table I.B1.2.1 / OECD ranking
table) with 10 plausible values, the final student weight and 80 BRR-Fay replicates.
Tolerance from the protocol: +-1 score point.
"""
import os
import sys
import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(__file__))
from brr import REPW, brr_stat, rubin, wmean  # noqa: E402

PUBLISHED = {"ARE": 431, "BRA": 379, "CRI": 385, "ESP": 473, "FRA": 474, "HKG": 540,
             "HUN": 473, "IRL": 492, "MAC": 552, "MEX": 395, "NLD": 493, "NZL": 479,
             "PAN": 357, "SAU": 389, "SVN": 485}

d = pd.read_pickle("data_work/wbq_all.pkl")
rows = []
for cnt, g in d.groupby("CNT"):
    w = g.W_FSTUWT.to_numpy()
    W = g[REPW].to_numpy()
    ests, vars_ = [], []
    for i in range(1, 11):
        pv = g[f"PV{i}MATH"].to_numpy()
        e, v = brr_stat(lambda ww: wmean(pv, ww), w, W)
        ests.append(float(e)); vars_.append(float(v))
    r = rubin(ests, vars_)
    rows.append(dict(CNT=cnt, mean=round(r["est"], 1), se=round(r["se"], 2),
                     published=PUBLISHED[cnt], diff=round(r["est"] - PUBLISHED[cnt], 1)))
qc = pd.DataFrame(rows)
qc["within_tolerance"] = qc["diff"].abs() <= 1.0
qc.to_csv("output/tables/qc_math_means.csv", index=False)
print(qc.to_string(index=False))
assert qc.within_tolerance.all(), "QC failed: pipeline does not reproduce OECD means"
print("QC passed: all 15 systems within +-1 point of the published means.")
