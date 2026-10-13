# Protocol: Additional mathematics instruction and adolescent life satisfaction in PISA 2022

**Status:** frozen before any exposure–outcome association was estimated. The git commit that adds this file serves as the timestamp. Register a copy on OSF (osf.io/registries) before submission; the commit is a stand-in, not a registration.

**Working title:** *Additional mathematics instruction and life satisfaction among 15-year-olds in 72 education systems: a pre-registered secondary analysis of PISA 2022*

---

## 1. Question and hypotheses

**Primary question.** Among 15-year-old students in the PISA 2022 education systems that administered both the additional-mathematics-instruction item and the life-satisfaction item, is taking part in additional mathematics instruction in the past 12 months associated with life satisfaction, after adjustment for pre-specified confounders?

**Primary hypothesis.** One exposure against one outcome:

- Exposure: any additional mathematics instruction in the past 12 months (yes/no; `ANYADD`, defined in §4).
- Outcome: life satisfaction, 0–10 (`ST016Q01NA`).
- H0: the international average of the system-specific adjusted mean differences is 0. Two-sided test, α = 0.05.
- Expected direction (stated in advance, not tested one-sided): lower life satisfaction among participants (the "pressure" account). Prior single-country findings are mixed: Hong Kong PISA 2018 found higher wellbeing among participants; Chinese and Korean panels found more depressive symptoms. A two-sided test is therefore used.

**Why this is new.** PISA 2022 is the first cycle to ask every participating system about the *forms* of additional mathematics instruction (ST297). The tutoring–wellbeing link has so far been studied only within single East Asian systems. See `novelty/NOVELTY.md` for the prior-work scan and its limits.

**Secondary questions (labelled exploratory; no confirmatory claims):**

- E1. Effect modification by household socioeconomic status (ESCS), sex, and grade (below / at / above the modal grade).
- E2. Tutoring intensity. PISA 2022 has no hours item, so intensity is measured as the number of forms used (0, 1, 2, 3+). Separate estimates are also given for each form: one-on-one tutoring, internet/computer tutoring, video-recorded instruction, small group, and large group.
- E3. System-level context: does the system-specific association vary with how common additional instruction is in that system (weighted participation rate)? This is a meta-regression across systems and tests the "normative context" idea: where tutoring is the norm, taking part may signal less about the student.
- E4. Secondary outcomes: mathematics anxiety (`ANXMAT`, all systems that have it), and psychosomatic complaints (WB154 items, the 14 systems that ran the optional well-being questionnaire).

## 2. Ethics and permissions

- The data are the public-use, de-identified PISA 2022 files released by the OECD. Analysis of public de-identified data is normally not human-subjects research, but **a written determination must be obtained from the sponsor or school (or its IRB) before submission.** Template wording for the manuscript: *"This study is a secondary analysis of publicly available, de-identified data and was determined to be exempt from review by [body] on [date]."*
- Licence: the files are released under the OECD's terms and conditions. The OECD website returned HTTP 403 from the analysis environment, so the exact terms could not be checked automatically. **Read and record them by hand.** In the meantime, the raw files are not redistributed (this repository holds code and derived summary tables only), no attempt is made to identify any student or school, and the dataset is cited as: OECD (2023), *PISA 2022 Database*, https://www.oecd.org/en/data/datasets/pisa-2022-database.html.

## 3. Dataset selection checklist

A dataset qualifies only if all of these are true (see `DECISION_LOG.md`):

| Criterion | PISA 2022 |
|---|---|
| Public and free, with documentation | Yes (OECD public-use files, codebook in SPSS metadata, technical report) |
| Exposure measured directly | Yes, ST297 (forms of additional math instruction); asked in all 80 systems in the public file |
| Outcome measured with an established item | Yes, ST016 life satisfaction 0–10; asked in 73 of 80 systems (not AUS, BEL, CAN, ISR, NOR, SGP, USA). Costa Rica has no ESCS, so 72 systems are eligible |
| Probability sample with weights and design information | Yes, final student weight `W_FSTUWT` and 80 Fay-BRR replicate weights |
| Enough sample for the primary test | Yes, about 545,000 students in the eligible systems |
| Confounders available | SES (ESCS), sex, grade, age, immigrant background, grade repetition, school type, school location |
| Not already answered for this question | Prior-work scan found no cross-national analysis (see `novelty/NOVELTY.md`) |

## 4. Variables (from the codebook, i.e. SPSS labels in `CY08MSP_STU_QQQ.SAV`)

**Exposure. `ANYADD`**, built from ST297 ("[Additional math instruction] received", check all that apply):

- 1 = at least one form ticked (Q01 one-on-one, Q03 internet/computer, Q05 video-recorded, Q06 small group, Q07 large group) **and** Q09 "I do not participate" not ticked.
- 0 = Q09 ticked and no form ticked.
- Missing: (a) nothing ticked (94,408 students); (b) one or more forms *and* Q09 ticked (39,122, contradictory); (c) all five forms *and* Q09 ticked (26,830, a straight-lining pattern); (d) item missing (31,841).
- Intensity (E2): `NFORMS` = number of forms ticked among valid participants, coded 1, 2, 3+; 0 for non-participants.

**Outcome. `ST016Q01NA`**: "Overall, how satisfied are you with your life as a whole these days?" 0 (not at all) to 10 (completely); higher is better. Analysed as continuous. Effects are reported in scale points and as a standardized difference (divided by the pooled within-system SD).

**Covariates, chosen in advance from a causal diagram (`dag.txt`):**

| Variable | Coding | Reason |
|---|---|---|
| Sex `ST004D01T` | female / male | Affects uptake and wellbeing |
| Age `AGE` | years, continuous | Pre-exposure |
| Grade `GRADE` | relative to modal grade: below / modal / above | Pre-exposure, linked to both |
| ESCS `ESCS` | continuous | Main confounder (family income, education, possessions) |
| Immigrant background `IMMIG` | native / second / first generation | Pre-exposure |
| Grade repetition `REPEAT` | yes / no | Proxy for earlier low achievement (repetition happened before the 12-month window) |
| School type `SC013Q01TA` | public / private | School-level confounder |
| School location `SC001Q01TA` | rural or village / small town / town / city / large city or megacity | School-level confounder |

**Not adjusted for in the primary model** (plausible mediators, or affected by tutoring): mathematics achievement (PVs), mathematics anxiety, homework time, sense of belonging, bullying. Mathematics achievement enters only in sensitivity analysis S7.

**Missing data.** The amount missing per variable is reported in `results/missingness.csv`. Before the freeze, the share of eligible students missing at least one analytic variable was about 43%, mostly the exposure (32%).

## 5. Pre-registration

This file. Deviations will be listed in `DEVIATIONS.md` with dates and reasons.

## 6. Data handling

- Raw files are downloaded by `00_download.sh` from `webfs.oecd.org`, stored outside the repository, set to read-only, and checked against SHA-256 checksums (`raw_checksums.txt`).
- All recodes and exclusions are done in code (`01_prepare.py`). Nothing is edited by hand.
- Exclusion rules, fixed now: (1) keep systems where ≥50% of students have non-missing ST297 and ST016; (2) drop a system if a core covariate (ESCS, sex, age) is entirely missing there; (3) within a system, a school-level covariate that is missing for more than 50% of students is left out of that system's model, and the omission is logged. No students are excluded for being outliers.

## 7. Analysis plan

1. **Weighted descriptives.** Per system: unweighted n, weighted participation rate in additional instruction, weighted mean life satisfaction, and missingness, with BRR standard errors.
2. **Primary model.** Within each system *c*: weighted least squares of `ST016` on `ANYADD` plus covariates, with final student weights. Standard errors come from the 80 Fay BRR replicate weights (k = 0.5, so variance = Σ(θᵣ − θ)² / 20). These replicates already encode the stratified, school-clustered design, so they account for clustering in schools. The primary estimate is the **international average**: the unweighted mean of the system coefficients, with SE = √(Σ SE²_c) / C, following the PISA convention (each system counts equally). The OECD average is reported alongside.
3. **Plausible values.** The primary model contains no PV variables. In S7, where mathematics achievement is a covariate, the model is fitted once per PV (10 PVs) and combined following the PISA Data Analysis Manual: final estimate = mean over PVs; variance = mean sampling variance + (1 + 1/10) × between-PV variance. PVs are never averaged into one score.
4. **Missing data.** Missingness exceeds 5%, so the primary analysis uses multiple imputation by chained equations with predictive mean matching (M = 20, 20 iterations, seed 20221). It is run separately in each system and includes all analysis variables, the outcome, the log final weight, school-mean ESCS, and the auxiliaries ANXMAT and BELONG. Each imputed dataset is analysed with the BRR procedure, then combined with Rubin's rules. Complete-case analysis is reported as sensitivity S1.
5. **Sensitivity checks** (all reported, none confirmatory):
   - S1. Complete-case analysis.
   - S2. Nonlinear dose-response: `NFORMS` as categories 0 / 1 / 2 / 3+.
   - S3. Restrict to students in the modal grade.
   - S4. Drop the most intensive participants (4–5 forms). This replaces "drop extreme tutoring hours", because PISA 2022 has no hours item.
   - S5. Negative-control outcome: feeling safe (`FEELSAFE`), in systems that have it. It shares the SES, school and neighbourhood confounding of the primary model, but there is no strong reason for mathematics tutoring to change it. A clear association would signal residual confounding.
   - S6. E-value for the primary estimate, converting the standardized difference d to an approximate risk ratio, RR ≈ exp(0.91·d) (VanderWeele & Ding 2017), for both the point estimate and the CI limit closer to the null.
   - S7. Additional adjustment for mathematics achievement (10 PVs, Rubin-type combination). This may over-adjust (achievement may be a mediator), so it is a bound, not a better estimate.
   - S8. Pooling by random-effects meta-analysis (DerSimonian–Laird) instead of the simple average, reporting τ and I².
   - S9. Alternative exposure codings: (a) "nothing ticked" counted as non-participant; (b) contradictory "form + do not participate" counted as participant; (c) straight-liners kept as participants.
   - S10. Leave out systems with >40% exposure missingness.
6. **Multiplicity.** There is one primary test. Everything else is exploratory and labelled as such. No p-value thresholds are applied to exploratory results; they are reported as estimates with 95% CIs.
7. **Reporting.** Effect sizes with 95% CIs, both in scale points and standardized, plus the number of systems and students.

## 8. Interpretation

The design is cross-sectional. Students who are struggling or distressed may be sent to tutoring (reverse causation), and family income, parental expectations and school pressure can drive both tutoring and wellbeing. Results will be described as "associated with", never "causes".

## 9. Quality checks

- Reproduce published OECD figures first: country mean mathematics scores (PISA 2022 Results Vol. I, Table I.B1.2.1) using PVs and BRR. Results are in `results/validation.csv`.
- A second person reruns `run_all.sh` from the raw files and compares `results/primary.csv`.
- The seed, package versions and session info are saved to `results/session_info.txt`.

## 10. Reporting

STROBE checklist for cross-sectional studies (`STROBE.md`). Code in a public repository with a README giving the run order. The limitations section covers self-report, single-item outcome, measurement differences across systems and languages (no invariance testing for a single item), no tutoring hours, no prior achievement, and unmeasured confounding.

## 11. Order of work

1. Pick the dataset and check the codebook. ✔
2. Finalize variables and the analysis plan. ✔ (this file)
3. Run the analysis.
4. Sensitivity checks.
5. Write up.
