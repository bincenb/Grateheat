#!/bin/bash
# Download the PISA 2022 student and school files and the codebook from the OECD,
# verify checksums, unzip, and make the raw files read-only.
# Run from the project folder:  bash code/00_download.sh
set -euo pipefail
cd "$(dirname "$0")/../data_raw"
BASE=https://webfs.oecd.org/pisa2022
UA="Mozilla/5.0"

get() {  # resumable download
  until curl -sS -A "$UA" -C - -o "$2" "$BASE/$1"; do sleep 5; done
}
[ -f STU_QQQ_SPSS.zip ] || get STU_QQQ_SPSS.zip STU_QQQ_SPSS.zip
[ -f SCH_QQQ_SPSS.zip ] || get SCH_QQQ_SPSS.zip SCH_QQQ_SPSS.zip
[ -f codebook.xlsx ]    || get CY08MSP_CODEBOOK_27thJune24.xlsx codebook.xlsx

sha256sum -c SHA256SUMS
[ -f CY08MSP_STU_QQQ.SAV ] || unzip -q STU_QQQ_SPSS.zip
[ -f CY08MSP_SCH_QQQ.SAV ] || unzip -q SCH_QQQ_SPSS.zip
chmod 444 ./*.zip ./*.SAV codebook.xlsx
ls -la
