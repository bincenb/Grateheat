#!/bin/bash
# Download the PISA 2022 public-use student and school questionnaire files (SPSS)
# into $PISA_RAW (default ../../pisa_raw, outside the repository), verify checksums,
# unzip, and make everything read-only.
set -euo pipefail
here=$(cd "$(dirname "$0")" && pwd)
raw=${PISA_RAW:-$here/../../pisa_raw}
mkdir -p "$raw" && cd "$raw"
for f in STU_QQQ_SPSS.zip SCH_QQQ_SPSS.zip; do
  [ -f "$f" ] || curl -fSL -A "Mozilla/5.0" -o "$f" "https://webfs.oecd.org/pisa2022/$f"
done
sha256sum -c "$here/raw_checksums.txt"
unzip -n -q STU_QQQ_SPSS.zip && unzip -n -q SCH_QQQ_SPSS.zip
chmod a-w ./*.zip ./*.SAV
ls -l
