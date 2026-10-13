# STROBE checklist (cross-sectional studies): where each item is covered

Fill in the "Manuscript" column with page numbers when the paper is drafted.

| # | Item | Where it is in this repository | Manuscript |
|---|---|---|---|
| 1 | Title/abstract: design named; balanced summary | `PROTOCOL.md` working title ("secondary analysis", "cross-sectional") | |
| 2 | Background/rationale | `novelty/NOVELTY.md` | |
| 3 | Objectives, pre-specified hypotheses | `PROTOCOL.md` §1 | |
| 4 | Study design | `PROTOCOL.md` §1, §8 | |
| 5 | Setting: locations, dates | PISA 2022, administered 2022 in 81 systems; 72 analysed (`results/prepare_log.txt`) | |
| 6 | Participants: eligibility, sampling | PISA two-stage stratified sample of 15-year-olds; exclusions in `PROTOCOL.md` §6 | |
| 7 | Variables: outcome, exposure, confounders, modifiers | `PROTOCOL.md` §4, `dag.txt` | |
| 8 | Data sources/measurement | Item wording in `PROTOCOL.md` §4 | |
| 9 | Bias | `PROTOCOL.md` §7 S5, S6; §8 | |
| 10 | Study size | `results/summary.json` | |
| 11 | Quantitative variables: handling, groupings | `PROTOCOL.md` §4 | |
| 12a | Statistical methods incl. confounding control | `PROTOCOL.md` §7 | |
| 12b | Subgroups and interactions | E1 | |
| 12c | Missing data | `PROTOCOL.md` §7.4, `results/missingness*.csv` | |
| 12d | Sampling strategy in analysis | BRR replicate weights, `lib.py` | |
| 12e | Sensitivity analyses | S1–S10 | |
| 13 | Participants: numbers at each stage, flow diagram | `results/prepare_log.txt`, `results/exposure_patterns.csv` | |
| 14 | Descriptive data; missing per variable | `results/system_estimates.csv`, `results/missingness.csv` | |
| 15 | Outcome data | `results/system_estimates.csv` (mean life satisfaction) | |
| 16 | Main results: unadjusted and adjusted estimates with CIs | `results/all_estimates.csv`; **add an unadjusted estimate in the manuscript table** | |
| 17 | Other analyses | `results/all_estimates.csv` | |
| 18 | Key results | `RESULTS.md` | |
| 19 | Limitations | `RESULTS.md` | |
| 20 | Interpretation | `RESULTS.md` | |
| 21 | Generalisability | `RESULTS.md` | |
| 22 | Funding | to be written | |
