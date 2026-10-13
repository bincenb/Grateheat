# Decision log

Dated record of choices made before and during the analysis. Newest last.

## 2026-10-13. Choosing a dataset (data first)

Approach: start from data that exists and is usable, then ask what it can answer that hasn't been asked, then check novelty.

Candidates considered:

| Dataset | Tutoring measure | Wellbeing measure | Verdict |
|---|---|---|---|
| **PISA 2022** | ST297, forms of additional math instruction, all 80 systems | ST016 life satisfaction (73 systems); WB154 psychosomatic complaints (14 systems); ANXMAT | **Chosen.** First PISA cycle with tutoring forms in the core questionnaire, alongside life satisfaction, in ~70 systems. |
| PISA 2018 | Out-of-school lessons only in some systems | ST016 life satisfaction | Already used (Hong Kong study, Liang et al. 2022); narrower tutoring coverage. |
| TIMSS 2019/2023 | Extra lessons/tutoring in math, grade 8 | Little wellbeing beyond bullying and belonging | No good wellbeing outcome. |
| HBSC | None | Strong | No exposure. |
| China CEPS / Korean panels | Strong | Strong | Single-country; question well studied (see novelty scan). |

Feasibility gates passed:

1. Files downloadable from `webfs.oecd.org` (the OECD landing page returned 403, but the file server worked). ✔
2. Exposure and outcome both present in ≥50% of students in 73 systems. ✔
3. Weights and 80 BRR replicates present. ✔
4. Core covariates present (ESCS missing entirely in CRI, so CRI is dropped). ✔

## 2026-10-13. Choosing the outcome

Life satisfaction (ST016) over mathematics anxiety (ANXMAT) as primary. Math tutoring targets mathematics directly, so math anxiety has the strongest reverse-causation problem (anxious students get sent to tutoring). Life satisfaction is broader, policy-relevant, and comparable with the HBSC/OECD wellbeing literature. ANXMAT becomes a secondary outcome (E4).

## 2026-10-13. Exposure coding

ST297 is check-all-that-apply. The response patterns were tabulated (no outcome data used) and showed:

- 188,499 ticked only "I do not participate"
- 233,044 ticked ≥1 form and not "do not participate"
- 94,408 ticked nothing
- 39,122 ticked 1–4 forms *and* "do not participate"
- 26,830 ticked all five forms *and* "do not participate" (straight-lining)
- 31,841 missing the whole item

Only the first two groups are treated as valid. The others are set to missing for the primary analysis and imputed, with alternatives in S9.

## 2026-10-13. Intensity

PISA 2022 has no hours-of-tutoring item. Intensity = number of forms used. The "drop extreme hours" check becomes "drop students using 4–5 forms" (S4).

## 2026-10-13. Pooling across systems

The PISA convention (simple average of system estimates, each system counting equally) is used for the primary estimate so that it is comparable with OECD reporting. Random-effects pooling is a sensitivity analysis (S8).

## 2026-10-13. Imputation

32% of the exposure is missing, mostly from response patterns that look like careless responding, so missingness may not be at random. MI (PMM, M = 20) assumes MAR given the imputation model. Complete-case (S1) and the alternative codings (S9) show how much this matters.
