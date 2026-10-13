# Pre-analysis plan

**School mobile-phone bans and psychosomatic health complaints among 15-year-olds: a cross-sectional analysis of the 15 education systems that ran the PISA 2022 Well-Being Questionnaire**

Status: **frozen**. This file was committed to git before any model linking the exposure to an outcome was run. The commit hash and timestamp are the evidence of that. Anything changed after the freeze goes in `DEVIATIONS.md`, never here.

What had been looked at before the freeze: the codebook, the list of systems that ran the Well-Being Questionnaire (WBQ), and the weighted share of students in schools with a phone ban in each of those systems (exposure only, see `DECISION_LOG.md`). No outcome distributions and no exposure–outcome associations had been computed.

## 1. Question and hypotheses

**Primary question.** Among 15-year-old students in the 15 education systems that administered the optional PISA 2022 Well-Being Questionnaire, do students whose school does not allow cell phones on the school premises report psychosomatic complaints less often than comparable students in schools without such a rule?

**Primary hypothesis (H1).** One exposure, one outcome, one test.

- Exposure: principal-reported school phone ban (SC190Q02JA).
- Outcome: psychosomatic complaints score from the 9-item HBSC Symptom Checklist (WB154Q01HA–Q09HA).
- H0: the adjusted mean difference in the score between ban and no-ban schools is 0. Two-sided test at α = 0.05.
- Expected direction (stated, not used in the test): bans go with slightly *fewer* complaints. A null result is equally reportable.

**Secondary outcomes (pre-specified, reported with CIs, not confirmatory).**

- O2: multiple health complaints (MHC), meaning 2 or more of the 9 symptoms "more than once a week" or "about every day". Reported as a prevalence difference.
- O3: difficulty getting to sleep (WB154Q07HA, 1–5). This is the symptom most directly tied to phone use.
- O4: psychological subscale (depressed, irritable, nervous, sleep, anxious: Q04–Q07, Q09) and somatic subscale (headache, stomach, back, dizzy: Q01–Q03, Q08), each scored separately.
- O5: self-rated health (WB150Q01HA, 1 = excellent … 4 = poor).

**Exploratory (labelled as such everywhere).**

- E1: whether the association differs by student sex, by household socioeconomic status (ESCS, continuous), and by grade (modal grade vs not). Tested with product terms.
- E2: whether it differs between OECD and partner systems, and from system to system (system-specific estimates, forest plot, random-effects heterogeneity τ² and I²).
- E3: policy combinations: a ban with vs without a written school statement on general device use (SC190Q01JA), giving 4 groups.

The original template asked whether effects differ "by tutoring intensity". That item does not apply to this question. It was replaced with E3, the closest analogue (policy intensity).

## 2. Ethics and permissions

- PISA 2022 microdata are public and de-identified, and released by the OECD for secondary research. This analysis does not try to identify any person or school.
- **To do (author):** get a written determination from the sponsor or school that this is not human-subjects research, or is exempt. Put the statement in the manuscript.
- Licence: the OECD terms allow reuse with attribution. Raw files are not redistributed in this repository. `code/00_download.sh` fetches them from the OECD server.
- Dataset citation: OECD (2023/2024). *PISA 2022 Database.* OECD Publishing, Paris. https://www.oecd.org/en/data/datasets/pisa-2022-database.html

## 3. Dataset selection checklist

| Requirement | PISA 2022 student + school files |
|---|---|
| Public, free, documented | Yes. Codebook `CY08MSP_CODEBOOK_27thJune24.xlsx`, Technical Report |
| Contains the exposure | Yes. SC190Q02JA in the school questionnaire |
| Contains a validated health outcome | Yes. The HBSC Symptom Checklist in the WBQ (15 systems) |
| Probability sample with weights | Yes. Final student weight and 80 BRR-Fay replicate weights |
| Enough exposure variation | Yes. Weighted ban share is 8–77% across systems (`DECISION_LOG.md`) |
| Not already done | Yes, as far as searched (`LITERATURE_CHECK.md`) |
| Does not duplicate the supervisor's project | Yes. Their exposure is ST297 tutoring and their outcome is ST016 life satisfaction; neither is used here |

## 4. Variables

**Exposure.** `ban` = 1 if SC190Q02JA = 1 ("The use of [cell phones] is not allowed on the school premises": Yes), 0 if = 2 (No). Other codes are missing. This is a school-level variable assigned to every sampled student in the school.

**Primary outcome.** `psc` = mean of WB154Q01HA–Q09HA (1 = rarely or never, 2 = about every month, 3 = about every week, 4 = more than once a week, 5 = about every day). Higher means more frequent complaints. It is computed only when at least 7 of 9 items are answered. The effect is reported on the 1–5 scale and in SD units (divided by the weighted pooled SD of `psc` in the analytic sample).

**Covariates, fixed in advance.** Chosen from the causal diagram in `DAG.md`. Each one plausibly affects both whether a school bans phones and students' complaints, and none can be changed by the ban.

- Student: sex (ST004D01T), age (AGE), grade relative to modal grade (GRADE), ESCS, immigrant background (IMMIG: native / second / first generation), ever repeated a grade (REPEAT, a proxy for prior achievement).
- School: public/private (PRIVATESCH), community size (SC001Q01TA, 6 levels collapsed to village / small town / town / city / large city+), log school enrolment (SCHSIZE), school mean ESCS (mean over all sampled students in the school).
- System fixed effects (CNT dummies).

**Not adjusted for (possible mediators or descendants of the policy):** students' phone/device use, ICT distraction, sleep, bullying, sense of belonging, anxiety, math achievement. Achievement appears only in sensitivity S11.

**Missing data.** Missingness is reported for every analysis variable (`output/tables/missingness.csv`).

## 5. Pre-registration

This file, committed to the repository before analysis, is the pre-registration of record. **To do (author):** upload this exact file, with its commit hash, to OSF Registries before submission.

## 6. Data handling

- Raw files are kept read-only (`chmod 444`), with SHA-256 checksums in `data_raw/SHA256SUMS`.
- Every recode and exclusion is done in `code/`. Nothing is edited by hand.
- **Exclusion rules (fixed now):**
  1. Keep students in systems with Option_WBQ = 1.
  2. Drop students without a valid `psc`, i.e. fewer than 7 of 9 symptom items answered. The outcome is not imputed. Counts are reported.
  3. No other exclusions. Missing exposure and covariates are handled by multiple imputation.

## 7. Analysis plan

### 7.1 Weights and variance (PISA 2022 Technical Report)

- Final student weight W_FSTUWT, rescaled within each system so that every system has the same total weight in the analytic sample. Each system counts equally, as with senate weights. The 80 replicate weights W_FSTURWT1–80 get the same rescaling.
- Sampling variance uses Fay's BRR with k = 0.5: V = 1/(80·(1−0.5)²) · Σ_r (θ_r − θ)² = 0.05 · Σ_r (θ_r − θ)². This takes the stratified two-stage design, including clustering of students in schools, into account as the Technical Report prescribes.
- Plausible values (used only in the QC and in S11): each statistic is estimated separately with each of the 10 PVs and the results are combined with Rubin's rules. PVs are never averaged.

### 7.2 Weighted descriptives

Weighted n, means and percentages for every variable, overall and by exposure group, plus the unweighted N of students and schools per system (Table 1).

### 7.3 Primary model

Weighted least squares: `psc ~ ban + covariates + system FE`, with the rescaled final weight. The SE comes from the 80 BRR replicates and is combined over imputations with Rubin's rules (Barnard–Rubin degrees of freedom). Estimate: adjusted mean difference with a 95% CI and the p-value for H1.

### 7.4 Plausible values / replicate weights

As in 7.1.

### 7.5 Missing data

More than 5% of the exposure is expected to be missing because of school questionnaire non-response, so **multiple imputation is the primary analysis** and complete-case analysis is sensitivity S1.

- Two-level chained equations with predictive mean matching (5 donors), **M = 20** imputations, 15 iterations, seed 20221.
- Stage A, school level: impute ban, the other SC190 items, PRIVATESCH, community size and school size from system, school mean ESCS, school mean `psc`, school mean of each other student covariate, and the school's share of girls.
- Stage B, student level: impute the student covariates from all analysis variables, including the outcome, exposure, system and stage-A school variables.
- Each imputed dataset gets the full replicate-weight analysis, and estimates are combined with Rubin's rules.

### 7.6 Sensitivity checks (all pre-specified)

| ID | Check |
|---|---|
| S1 | Complete-case analysis |
| S2 | Flexible functional form: natural cubic splines (4 df) for ESCS, age and school mean ESCS |
| S3 | Modal-grade students only (GRADE = 0) |
| S4 | Drop implausible extreme responders: all 9 symptoms "about every day" |
| S5 | **Negative-control outcome:** self-reported height (WB152Q01HA, z-scored within system × sex; values outside 120–220 cm set missing). A ban cannot change height, but height shares socioeconomic and regional confounding. Expected ≈ 0 |
| S6 | **E-value** for the primary estimate and its CI limit closer to null. Standardised difference d is converted with RR ≈ exp(0.91·d) (VanderWeele & Ding 2017) |
| S7 | Leave-one-system-out: the pooled estimate re-run 15 times |
| S8 | Also adjust for the other device-governance items (SC190Q01JA written statement; SC190Q06JA teachers set rules for device use in lessons) |
| S9 | Random-effects (DerSimonian–Laird) pooling of system-specific estimates instead of the fixed-effects pooled model |
| S10 | Public schools only |
| S11 | Also adjust for mathematics achievement (10 PVs, Rubin's rules). It may be a mediator, so this is a sensitivity check only |

### 7.7 Multiplicity

There is one primary test (H1). Everything else is secondary or exploratory, is reported with 95% CIs, and is described as such. No p-value adjustment is applied to exploratory results, and they are not used for confirmatory claims.

### 7.8 Reporting

Effect sizes with 95% CIs everywhere, and p-values only alongside them.

## 8. Interpreting results

- The data are cross-sectional. The ban is a school policy measured at the same time as the outcome. Schools may adopt bans *because* of student problems (reverse causation), and school ethos and selection can drive both.
- Use "associated with", never "causes", "reduces" or "improves".
- The principal's report says whether a rule exists, not how well it is enforced.

## 9. Quality checks

- Reproduce published OECD figures before trusting the pipeline: mean mathematics score and SE for the 15 systems (PISA 2022 Results Vol. I, Table I.B1.2.1) using 10 PVs + BRR. Mismatch tolerance: ±1 score point for means.
- A second person reruns `code/` from the raw files (to do, author).
- Seed, package versions and session info are saved in `output/session_info.txt`.

## 10. Reporting

- STROBE checklist for cross-sectional studies (`STROBE.md`).
- Public code repository with a README that explains the run order.
- Limitations cover self-report, cross-country measurement differences (no invariance testing of the HBSC-SCL across languages here), principal-reported policy with unknown enforcement, the timing of the policy relative to the 6-month symptom window, and unmeasured confounding.

## 11. Order of work

1. Pick the dataset and check the codebook (done)
2. Finalise variables and analysis plan (this file, frozen)
3. Run QC reproduction, then the primary analysis
4. Sensitivity checks
5. Write up
