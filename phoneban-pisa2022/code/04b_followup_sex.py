"""POST HOC follow-up of the exploratory ban x sex interaction (E1a). Not pre-specified;
see DEVIATIONS.md D8. Decomposes E1a into sex-specific associations and checks whether
it survives (i) fully sex-stratified models, which let every covariate and every system
fixed effect differ by sex, (ii) adjustment for the school's share of girls (single-sex
schools), and (iii) system by system. F4 repeats (iii) for the ban x ESCS interaction (E1b).
"""
import os
import sys
from multiprocessing.pool import ThreadPool

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(__file__))
import importlib  # noqa: E402
A = importlib.import_module("04_analysis")  # reuse design, weights and runner  # noqa: E402

A._init()
share_f = A.a.groupby("CNTSCHID").female.transform("mean").to_numpy()
res = []
with ThreadPool(4) as pool:
    for sex, val in (("girls", 1), ("boys", 0)):
        sub = (lambda D, m, v=val: (D.female == v).to_numpy())
        for y, lab, sc in (("psc", "psychosomatic score", 1), ("sleep", "difficulty getting to sleep", 1),
                           ("mhc", "multiple health complaints (pp)", 100), ("psych", "psychological subscale", 1),
                           ("soma", "somatic subscale", 1)):
            res += A.run(pool, f"F1 {sex}: {lab}", dict(y=y, terms=["ban"], subset=sub), f"F1_{sex}", sc)
        res += A.run(pool, f"F2 {sex}: psychosomatic, + school share of girls",
                     dict(y="psc", terms=["ban"], subset=sub, extra=lambda D, m: [("share_f", share_f)]),
                     f"F2_{sex}")
        res += A.run(pool, f"F2b {sex}: psychosomatic, mixed-sex schools only",
                     dict(y="psc", terms=["ban"],
                          subset=lambda D, m, v=val: ((D.female == v) & (share_f > 0.05) & (share_f < 0.95)).to_numpy()),
                     f"F2b_{sex}")
    for c in A.SYSTEMS:
        r = A.run(pool, f"F3 system {c}: ban x female",
                  dict(y="psc", terms=["ban_x_female"], fe=False,
                       subset=lambda D, m, c=c: (D.CNT == c).to_numpy(),
                       extra=lambda D, m: [("ban_x_female", D.ban * D.female)]), "F3_system")
        r[0]["system"] = c
        res += r
    # F4: the same within-system check for the exploratory ban x ESCS interaction (E1b)
    for c in [c for c in A.SYSTEMS if c != "CRI"]:
        r = A.run(pool, f"F4 system {c}: ban x ESCS",
                  dict(y="psc", terms=["ban_x_escs"], fe=False,
                       subset=lambda D, m, c=c: (D.CNT == c).to_numpy(),
                       extra=lambda D, m: [("ban_x_escs", D.ban * D.escs)]), "F4_system")
        r[0]["system"] = c
        res += r

R = pd.DataFrame(res)
f4 = R[R.group == "F4_system"]
dl4 = A.dersimonian_laird(f4.est.to_numpy(), f4.se.to_numpy())
print("F4 random-effects pooled ban x ESCS:", {k: round(v, 4) for k, v in dl4.items()})
R = pd.concat([R, pd.DataFrame([dict(group="F4_pooled", analysis="F4 RE-pooled ban x ESCS",
                                     outcome="psc", term="ban_x_escs", est=dl4["est"], se=dl4["se"],
                                     lo=dl4["lo"], hi=dl4["hi"], p=dl4["p"])])], ignore_index=True)
f3 = R[R.group == "F3_system"]
dl = A.dersimonian_laird(f3.est.to_numpy(), f3.se.to_numpy())
print("F3 random-effects pooled ban x female:", {k: round(v, 4) for k, v in dl.items()})
R = pd.concat([R, pd.DataFrame([dict(group="F3_pooled", analysis="F3 RE-pooled ban x female",
                                     outcome="psc", term="ban_x_female", est=dl["est"], se=dl["se"],
                                     lo=dl["lo"], hi=dl["hi"], p=dl["p"])])], ignore_index=True)
print("systems with negative interaction:", int((f3.est < 0).sum()), "of", len(f3))
R.to_csv("output/tables/results_followup_sex.csv", index=False)
