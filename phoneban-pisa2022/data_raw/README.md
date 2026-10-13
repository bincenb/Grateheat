# Raw data (not in git)

Run `bash code/00_download.sh` from the project folder. It downloads these files from the OECD server into this folder, checks them against `SHA256SUMS`, unzips them and makes them read-only:

- `STU_QQQ_SPSS.zip` → `CY08MSP_STU_QQQ.SAV` (student questionnaire, 682 MB zipped)
- `SCH_QQQ_SPSS.zip` → `CY08MSP_SCH_QQQ.SAV` (school questionnaire)
- `CY08MSP_CODEBOOK_27thJune24.xlsx` (codebook, saved as `codebook.xlsx`)

The OECD terms of use apply. Do not redistribute the raw files.
