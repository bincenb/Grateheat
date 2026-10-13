"""Figures 1-2 and supplementary Figure S1 from output/results.pkl."""
import os
import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(__file__))
from figure_style import apply_figure_style, panel_letter, PALETTE  # noqa: E402

apply_figure_style(sizes=(8, 7, 6.5))
F = "output/figures"
os.makedirs(F, exist_ok=True)
obj = pd.read_pickle("output/results.pkl")
R, S = obj["results"], obj["summary"]
per = pd.read_csv("output/tables/table2_by_system.csv").set_index("system")
NAMES = {"ARE": "United Arab Emirates", "BRA": "Brazil", "CRI": "Costa Rica", "ESP": "Spain",
         "HKG": "Hong Kong (China)", "HUN": "Hungary", "IRL": "Ireland", "MAC": "Macao (China)",
         "MEX": "Mexico", "NLD": "Netherlands", "NZL": "New Zealand", "PAN": "Panama",
         "SAU": "Saudi Arabia", "SVN": "Slovenia"}


def row(label):
    return R[(R.analysis == label) & (R.term == R[R.analysis == label].term.iloc[0])].iloc[0]


def forest(ax, sys_rows, pooled, xlabel, unit_fmt="{:+.2f}"):
    sys_rows = sys_rows.sort_values("est")
    n = len(sys_rows)
    y = np.arange(n, 0, -1) + 1.5
    ax.hlines(y, sys_rows.lo, sys_rows.hi, color=PALETTE["control"], lw=0.8)
    ax.plot(sys_rows.est, y, "s", color=PALETTE["control"], ms=3.5)
    labels = [f"{NAMES[c]} ({per.loc[c, 'ban_pct']:.0f}%)" for c in sys_rows.system]
    py = [0.9, 0.0][:len(pooled)] if len(pooled) > 1 else [0.45]
    for (lab, p), yy in zip(pooled, py):
        ax.hlines(yy, p["lo"], p["hi"], color=PALETTE["primary"], lw=1.4)
        ax.plot(p["est"], yy, "D", color=PALETTE["primary"], ms=4.5)
    ax.set_yticks(list(y) + py)
    ax.set_yticklabels(labels + [p[0] for p in pooled])
    ax.axvline(0, color=PALETTE["control"], ls="--", lw=0.7, zorder=0)
    ax.spines["left"].set_visible(False)
    ax.tick_params(axis="y", length=0)
    ax.set_xlabel(xlabel)
    ax.set_ylim(-0.7, n + 2.2)


# ---------- Figure 1: system-specific estimates, primary outcome ----------
sysr = R[R.group == "system"].copy()
prim = R[R.analysis.str.startswith("PRIMARY")].iloc[0]
s9 = R[R.analysis.str.startswith("S9")].iloc[0]
fig, ax = plt.subplots(figsize=(88 / 25.4, 105 / 25.4))
forest(ax, sysr, [("Pooled, fixed effects", prim), ("Pooled, random effects", s9)],
       "Adjusted difference in psychosomatic score,\nban vs no ban (1–5 scale)")
het = S["heterogeneity"]
ax.text(1.0, 0.0, f"I² = {100 * het['I2']:.0f}%", transform=ax.transAxes, ha="right", va="bottom",
        fontsize=6.5, color=PALETTE["ink"])
fig.savefig(f"{F}/fig1_forest_by_system.pdf")
fig.savefig(f"{F}/fig1_forest_by_system.png")
plt.close(fig)

# ---------- Figure 2: outcomes (a) and sensitivity analyses (b) ----------
outs = [("PRIMARY: ban -> psychosomatic score (1-5)", "Psychosomatic score"),
        ("O4a psychological subscale (1-5)", "Psychological subscale"),
        ("O4b somatic subscale (1-5)", "Somatic subscale"),
        ("O3 difficulty getting to sleep (1-5)", "Difficulty getting to sleep"),
        ("O5 self-rated health (1-4, higher=worse)", "Poorer self-rated health")]
sens = [("PRIMARY: ban -> psychosomatic score (1-5)", "Primary (MI, n = 111,616)"),
        ("S1 complete case", "S1 Complete cases"),
        ("S2 splines for ESCS, age, school ESCS", "S2 Spline covariates"),
        ("S3 modal grade only", "S3 Modal grade only"),
        ("S4 drop all-9-symptoms-daily responders", "S4 Drop extreme responders"),
        ("S8 + other device-policy items", "S8 + Other device policies"),
        ("S9 random-effects pooling (DL)", "S9 Random-effects pooling"),
        ("S10 public schools only", "S10 Public schools only"),
        ("S11 + mathematics achievement (PVs)", "S11 + Mathematics score"),
        ("S12 drop CRI, MAC, NZL", "S12 Drop CRI, MAC, NZL"),
        ("S5 negative control: height (z)", "S5 Negative control: height (SD)")]
fig, axs = plt.subplots(1, 2, figsize=(180 / 25.4, 62 / 25.4), width_ratios=[1, 1.15])
for ax, items, letter in ((axs[0], outs, "a"), (axs[1], sens, "b")):
    rows = [row(k) for k, _ in items]
    y = np.arange(len(rows), 0, -1)
    for yy, r, (k, _) in zip(y, rows, items):
        col = PALETTE["primary"] if k.startswith("PRIMARY") else (
            PALETTE["control"] if k.startswith("S5") else PALETTE["secondary"])
        ax.hlines(yy, r["lo"], r["hi"], color=col, lw=1.2)
        ax.plot(r["est"], yy, "s", color=col, ms=4, mec=col)
    ax.set_yticks(y)
    ax.set_yticklabels([lab for _, lab in items])
    ax.axvline(0, color=PALETTE["control"], ls="--", lw=0.7, zorder=0)
    ax.spines["left"].set_visible(False)
    ax.tick_params(axis="y", length=0)
    ax.set_xlabel("Adjusted difference, ban vs no ban")
    ax.set_xlim(-0.05, 0.05)
    panel_letter(ax, letter, dx=-0.02)
fig.savefig(f"{F}/fig2_outcomes_sensitivity.pdf")
fig.savefig(f"{F}/fig2_outcomes_sensitivity.png")
plt.close(fig)

# ---------- Figure S1: system-specific estimates, sleep and MHC ----------
fig, axs = plt.subplots(1, 2, figsize=(180 / 25.4, 100 / 25.4))
for ax, grp, lab, key, letter in (
        (axs[0], "system_sleep", "Difficulty getting to sleep (1–5)", "O3 difficulty getting to sleep (1-5)", "a"),
        (axs[1], "system_mhc", "Multiple health complaints (percentage points)", "O2 multiple health complaints (pp)", "b")):
    forest(ax, R[R.group == grp].copy(), [("Pooled, fixed effects", row(key))], f"Adjusted difference,\n{lab}")
    panel_letter(ax, letter)
fig.savefig(f"{F}/figS1_sleep_mhc_by_system.pdf")
fig.savefig(f"{F}/figS1_sleep_mhc_by_system.png")
plt.close(fig)
print("figures written")
