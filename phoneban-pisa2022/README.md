# School phone bans and psychosomatic complaints in PISA 2022

Secondary analysis of public PISA 2022 microdata. Question: in the 14 education systems where students answered the HBSC symptom checklist (PISA 2022 Well-Being Questionnaire), do students in schools that ban cell phones on the premises report psychosomatic complaints less often than comparable students in schools without a ban?

| File | What it is |
|---|---|
| `PROTOCOL.md` | Pre-analysis plan, frozen at commit `430d8a0` before any outcome model was run |
| `DEVIATIONS.md` | Every change made after the freeze, with reasons |
| `DECISION_LOG.md` | Dataset choice, why the first idea was dropped, feasibility check |
| `LITERATURE_CHECK.md` | Prior-work searches and what they found |
| `DAG.md` | Causal diagram behind the adjustment set |
| `MANUSCRIPT.md` | Draft paper (STROBE-structured) |
| `STROBE.md` | STROBE checklist with locations |
| `output/tables/` | All results as CSV |
| `output/figures/` | Figures (PDF + 300 dpi PNG) |
| `output/analysis_log.txt` | Console log of the full analysis run |

## Run order

Python 3.11+ with `numpy pandas scipy statsmodels patsy pyreadstat matplotlib`. Run from this folder:

```bash
bash   code/00_download.sh        # OECD files -> data_raw/, checksum, unzip, read-only (~700 MB)
python3 code/01_prepare.py        # recode, exclusions, missingness table  (~30 s)
python3 code/02_qc_reproduce.py   # reproduce OECD mean math scores; stops if it fails
python3 code/03_impute.py         # two-level MICE-PMM, M = 20, seed 20221  (~1.5 min)
python3 code/04_analysis.py       # all models, BRR x 20 imputations       (~50 min on 4 cores)
python3 code/05_figures.py        # figures
python3 code/06_session_info.py   # package versions
```

`code/brr.py` contains the survey helpers (Fay BRR variance, Rubin's rules, DerSimonian–Laird, E-value). Nothing is edited by hand. Intermediate files go to `data_work/`, which is not tracked.

## Data licence and citation

PISA data are released by the OECD for research. Raw files are not redistributed here. Cite: OECD (2023). *PISA 2022 Database*. OECD Publishing, Paris.

## Still to do (author)

- Written non-human-subjects / exempt determination from the sponsor or school.
- Register `PROTOCOL.md` (at commit `430d8a0`) on OSF Registries.
- A second person reruns `code/` from the raw files and compares `output/tables/results_all.csv`.
- Fuller literature search (Scopus/Web of Science, ERIC, forward citations); see `LITERATURE_CHECK.md`.
