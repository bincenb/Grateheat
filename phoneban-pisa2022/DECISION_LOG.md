# Decision log

Each entry is dated and gives what was decided and why.

**2026-10-13 · Dataset: PISA 2022 (student + school questionnaire files).**
Reasons: public and free; large probability samples with official weights and BRR replicate weights; documented codebook and technical report; it has a validated adolescent health measure (HBSC Symptom Checklist in the optional Well-Being Questionnaire) and school-level policy items from principals. Alternatives considered: YRBS (no school policy or tutoring items), HBSC microdata (access by request, not instant), NSCH (no school policy items), HSLS:09 (older cohort; no phone policy).

**2026-10-13 · First question (tutoring → psychosomatic complaints) dropped.**
The literature search found no cross-national study of it. But the supervisor's ongoing project uses the same tutoring exposure (ST297) in the same dataset and already lists psychosomatic complaints as an exploratory outcome. To keep the two projects clearly separate, no ST297 or ST016 variable is used anywhere in this study.

**2026-10-13 · Final question: school phone ban (SC190Q02JA) → psychosomatic complaints (WB154).**
Reasons: (1) high policy relevance, with many bans passed in 2023–26; (2) the exposure is a school policy rather than an individual choice, which removes one layer of self-selection; (3) the gap found in `LITERATURE_CHECK.md`; (4) no overlap with the supervisor's variables.

**2026-10-13 · Feasibility check (exposure only, before the freeze).**
WBQ systems: ARE, BRA, CRI, ESP, FRA, HKG, HUN, IRL, MAC, MEX, NLD, NZL, PAN, SAU, SVN. That is 135,348 students in 4,881 schools. Weighted % of students in ban schools: NLD 7.8, CRI 12.7, NZL 17.6, HUN 19.4, MEX 21.9, FRA 23.4, BRA 37.5, PAN 43.3, SVN 45.0, MAC 46.3, IRL 55.5, HKG 67.0, ESP 67.4, SAU 71.6, ARE 77.0. Students with missing exposure: 0–30% by system (school non-response), so multiple imputation is planned. No outcome data were examined.

**2026-10-13 · Primary outcome is the continuous 9-item mean, not the binary MHC.**
It keeps all the information, and the standard HBSC binary cut-off is reported as secondary O2.

**2026-10-13 · Outcome not imputed.**
Students with fewer than 7 of 9 symptom items answered mostly skipped the optional questionnaire. Imputing their outcome would add noise and no information (von Hippel 2007, "multiple imputation, then deletion").
