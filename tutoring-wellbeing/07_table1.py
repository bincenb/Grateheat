"""Table 1: weighted characteristics by exposure status (observed exposure).
Each cell is the international average (each system counts equally) of
within-system weighted means or percentages."""
import os
import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
d = pd.read_parquet(os.path.join(HERE, "work", "analytic.parquet"))
d = d[d.ANYADD.notna()].copy()
d["IMMIG_ANY"] = (d.IMMIG > 1).astype(float).where(d.IMMIG.notna())
d["BELOW"] = (d.GRADE3 < 0).astype(float).where(d.GRADE3.notna())
d["ABOVE"] = (d.GRADE3 > 0).astype(float).where(d.GRADE3.notna())
for i in range(1, 11):
    d[f"M{i}"] = d[f"PV{i}MATH"]
rows = {"Life satisfaction (0–10), mean": ("LS", 1), "Female, %": ("FEMALE", 100), "ESCS, mean": ("ESCS", 1),
        "Immigrant background, %": ("IMMIG_ANY", 100), "Repeated a grade, %": ("REPEAT", 100),
        "Below modal grade, %": ("BELOW", 100), "Above modal grade, %": ("ABOVE", 100),
        "Private school, %": ("PRIVATE", 100), "Mathematics anxiety (WLE), mean": ("ANXMAT", 1),
        "Feeling safe (WLE), mean": ("FEELSAFE", 1)}
out = {}
for grp, lab in [(0, "No additional instruction"), (1, "Any additional instruction")]:
    g = d[d.ANYADD == grp]
    col = {"Students (unweighted n)": f"{len(g):,}"}
    for name, (v, k) in rows.items():
        per = []
        for _, s in g.groupby("CNT"):
            ok = s[v].notna()
            if ok.mean() > .5:
                per.append(np.average(s.loc[ok, v], weights=s.loc[ok, "W_FSTUWT"]) * k)
        col[name] = f"{np.mean(per):.2f}" if k == 1 else f"{np.mean(per):.1f}"
    pm = [np.mean([np.average(s[f"M{i}"], weights=s.W_FSTUWT) for i in range(1, 11)]) for _, s in g.groupby("CNT")]
    col["Mathematics score (10 PVs), mean"] = f"{np.mean(pm):.0f}"
    out[lab] = col
t = pd.DataFrame(out)
t.to_csv(os.path.join(HERE, "results", "table1.csv"))
print(t.to_string())
