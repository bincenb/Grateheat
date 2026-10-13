"""Pipeline check: reproduce published PISA 2022 country mean mathematics scores
(OECD 2023, PISA 2022 Results Vol. I, Table I.B1.2.1, as tabulated on the English
Wikipedia PISA article, read 2026-10-13) using 10 plausible values and BRR.
Moldova is set to 414, the OECD figure; Wikipedia lists 417, which is a transcription error.
Differences of 1 point arise where the estimate sits on a .5 rounding boundary.
"""
import os
import numpy as np
import pandas as pd
import pyreadstat
from lib import WCOLS, brr_mean, combine

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.environ.get("PISA_RAW", os.path.join(HERE, "..", "..", "pisa_raw"))

PUBLISHED = {"SGP": 575, "MAC": 552, "TAP": 547, "HKG": 540, "JPN": 536, "KOR": 527, "EST": 510, "CHE": 508,
             "CAN": 497, "NLD": 493, "IRL": 492, "BEL": 489, "DNK": 489, "GBR": 489, "POL": 489, "AUS": 487,
             "AUT": 487, "CZE": 487, "SVN": 485, "FIN": 484, "LVA": 483, "SWE": 482, "NZL": 479, "DEU": 475,
             "LTU": 475, "FRA": 474, "ESP": 473, "HUN": 473, "PRT": 472, "ITA": 471, "VNM": 469, "NOR": 468,
             "MLT": 466, "USA": 465, "SVK": 464, "HRV": 463, "ISL": 459, "ISR": 458, "TUR": 453, "BRN": 442,
             "SRB": 440, "ARE": 431, "GRC": 430, "ROU": 428, "KAZ": 425, "MNG": 425, "BGR": 417, "MDA": 414,
             "QAT": 414, "CHL": 412, "URY": 409, "MYS": 409, "MNE": 406, "QAZ": 397, "MEX": 395, "THA": 394,
             "PER": 391, "GEO": 390, "MKD": 389, "SAU": 389, "CRI": 385, "COL": 383, "BRA": 379, "ARG": 378,
             "JAM": 377, "ALB": 368, "IDN": 366, "PSE": 366, "MAR": 365, "UZB": 364, "JOR": 361, "PAN": 357,
             "KSV": 355, "PHL": 355, "GTM": 344, "SLV": 343, "DOM": 339, "PRY": 338, "KHM": 336}

pvs = [f"PV{i}MATH" for i in range(1, 11)]
df, _ = pyreadstat.read_sav(os.path.join(RAW, "CY08MSP_STU_QQQ.SAV"), usecols=["CNT", *pvs, *WCOLS])
rows = []
for cnt, g in df.groupby("CNT"):
    W = g[WCOLS].to_numpy()
    est, var = zip(*(brr_mean(g[p].to_numpy(), W) for p in pvs))
    m, t = combine(np.array(est), np.array(var))
    rows.append({"CNT": cnt, "mean": round(m, 1), "se": round(float(np.sqrt(t)), 2), "published": PUBLISHED.get(cnt)})
res = pd.DataFrame(rows)
res["diff"] = (res["mean"].round() - res["published"])
os.makedirs(os.path.join(HERE, "results"), exist_ok=True)
res.to_csv(os.path.join(HERE, "results", "validation.csv"), index=False)
chk = res.dropna(subset=["published"])
print(res.to_string(index=False))
print(f"\nCompared {len(chk)} systems; exact match after rounding: {(chk['diff'] == 0).sum()}; max |diff|: {chk['diff'].abs().max()}")
