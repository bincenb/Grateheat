# Additional mathematics instruction and life satisfaction: PISA 2022

A pre-registered secondary analysis of public PISA 2022 data asking whether 15-year-olds who take additional mathematics instruction (tutoring, online or video instruction, group study) are more or less satisfied with their lives, across 72 education systems.

- `PROTOCOL.md`: the frozen pre-registration (committed before any outcome analysis)
- `DECISION_LOG.md`: why this dataset, outcome and exposure coding
- `DEVIATIONS.md`: what changed after the freeze
- `novelty/NOVELTY.md`: the prior-work check and its limits
- `dag.txt`: causal diagram behind the covariate choice
- `results/`: tables (`all_estimates.csv`, `summary.json`, `system_estimates.csv`, `validation.csv`, `missingness*.csv`)
- `figures/`: forest plot and participation-rate plot
- `RESULTS.md`: plain-language summary of findings

## Run order

The raw data (about 2.7 GB unzipped) are **not** in this repository. The OECD licence and file size both rule it out. `00_download.sh` fetches them.

```bash
pip install numpy pandas scipy statsmodels pyreadstat pyarrow matplotlib
./run_all.sh            # or run the steps below one at a time
```

| Step | Script | What it does | Time* |
|---|---|---|---|
| 0 | `00_download.sh` | Downloads the student and school files to `../../pisa_raw`, checks SHA-256 against `raw_checksums.txt`, makes them read-only | ~5 min |
| 1 | `01_prepare.py` | All recodes and exclusions; writes `work/analytic.parquet` and the missingness tables | 1 min |
| 2 | `02_validate.py` | Reproduces published country mean math scores (pipeline check) | 1 min |
| 3 | `03_analysis.py` | Per-system multiple imputation + BRR models (primary, sensitivity, exploratory) | ~30 min on 4 cores |
| 4 | `04_summarize.py` | International averages, random effects, meta-regression, E-value | seconds |
| 5 | `05_figures.py` | Figures | seconds |
| 6 | `06_session_info.py` | Package versions and seed | seconds |

\*On a 4-core machine. Set `PISA_RAW=/path/to/raw` if the raw files live elsewhere. `PROCS` sets the number of worker processes.

**Second-person check (protocol §9):** on a fresh machine, run `./run_all.sh` and compare `results/all_estimates.csv` with the committed copy. MI uses fixed seeds, so the numbers should match to the last digit given the same package versions (`results/session_info.txt`).

## Data citation

OECD (2023). *PISA 2022 Database*. https://www.oecd.org/en/data/datasets/pisa-2022-database.html
