#!/bin/bash
# Full pipeline, raw files to tables and figures. Run from this folder.
# PISA_RAW points to the folder holding the raw OECD files (default ../../pisa_raw).
set -euo pipefail
cd "$(dirname "$0")"
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
./00_download.sh
python3 01_prepare.py
python3 02_validate.py
python3 03_analysis.py
python3 04_summarize.py
python3 05_figures.py
python3 06_session_info.py
