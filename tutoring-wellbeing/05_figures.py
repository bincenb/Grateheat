"""Figure 1: system-specific adjusted differences (forest plot).
Figure 2: system difference against system participation rate (meta-regression)."""
import json
import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from figure_style import apply_figure_style, PALETTE
from lib import dersimonian_laird

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(HERE, "results")
FIG = os.path.join(HERE, "figures")
os.makedirs(FIG, exist_ok=True)
apply_figure_style(sizes=(9, 8, 7))

s = pd.read_csv(os.path.join(RES, "system_estimates.csv")).sort_values("primary_est").reset_index(drop=True)
summ = json.load(open(os.path.join(RES, "summary.json")))
pa = summ["primary_international_average"]
z = 1.959964

# ---- Figure 1: forest plot
fig, ax = plt.subplots(figsize=(88 / 25.4, 200 / 25.4))
y = np.arange(len(s)) + 2
lo, hi = s.primary_est - z * s.primary_se, s.primary_est + z * s.primary_se
col = np.where(s.OECD == 1, PALETTE["primary"], PALETTE["control"])
ax.hlines(y, lo, hi, color=col, lw=0.8)
ax.scatter(s.primary_est, y, marker="s", s=10, color=col, zorder=3)
ax.hlines(0, pa["ci_low"], pa["ci_high"], color=PALETTE["accent"], lw=1.4)
ax.scatter([pa["estimate"]], [0], marker="D", s=24, color=PALETTE["accent"], zorder=3)
ax.axvline(0, color=PALETTE["control"], ls="--", lw=0.8, zorder=0)
ax.set_yticks([0, *y], ["International average", *s.CNT])
ax.tick_params(axis="y", length=0, labelsize=6)
ax.spines["left"].set_visible(False)
ax.set_ylim(-1.2, y.max() + 1)
ax.set_xlabel("Adjusted difference in life satisfaction (0–10 points)")
ax.text(0.98, 0.02, "OECD", transform=ax.transAxes, ha="right", va="bottom", color=PALETTE["primary"], fontsize=7)
ax.text(0.98, 0.045, "Partner", transform=ax.transAxes, ha="right", va="bottom", color=PALETTE["control"], fontsize=7)
fig.savefig(os.path.join(FIG, "fig1_forest.pdf"))
fig.savefig(os.path.join(FIG, "fig1_forest.png"))

# ---- Figure 2: estimate vs participation rate
fig, ax = plt.subplots(figsize=(88 / 25.4, 70 / 25.4))
w = 1 / (s.primary_se ** 2)
ax.scatter(s.participation_rate * 100, s.primary_est, s=12 + 60 * w / w.max(), color=col, alpha=0.85, lw=0)
ax.axhline(0, color=PALETTE["control"], ls="--", lw=0.8, zorder=0)
xg = np.linspace(s.participation_rate.min(), s.participation_rate.max(), 50)
p = s.participation_rate
# meta-regression line: centred at the mean participation rate, slope per 10 percentage points
fit = dersimonian_laird(s.primary_est, s.primary_se ** 2, X=(p - p.mean()) * 10)
ax.plot(xg * 100, fit["coef"][0] + fit["coef"][1] * (xg - p.mean()) * 10, color=PALETTE["ink"], lw=1.0)
for _, r in s.iterrows():
    if abs(r.primary_est) > 0.45 or r.participation_rate > 0.75 or r.participation_rate < 0.12:
        ax.annotate(r.CNT, (r.participation_rate * 100, r.primary_est), xytext=(3, 0), textcoords="offset points",
                    fontsize=6, va="center", color=PALETTE["ink"])
ax.set_xlabel("Students using additional math instruction (%)")
ax.set_ylabel("Adjusted difference (points)")
fig.savefig(os.path.join(FIG, "fig2_prevalence.pdf"))
fig.savefig(os.path.join(FIG, "fig2_prevalence.png"))
print("figures saved")
