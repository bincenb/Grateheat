# Manuscript draft: Methods and Results

Draft text for the paper. Numbers come from `results/all_estimates.csv`, `results/summary.json`, `results/table1.csv` and `results/system_estimates.csv`. Square brackets mark things you have to fill in or check. Check every reference against the original source before submitting.

**Working title:** Satisfied but anxious? Additional mathematics instruction and adolescent wellbeing in 72 education systems

---

## Methods

### Design and data source

This is a cross-sectional secondary analysis of the Programme for International Student Assessment (PISA) 2022 public-use database (OECD, 2023a). PISA samples 15-year-old students in two stages: schools are drawn with probability proportional to size within explicit strata, and then students are drawn within schools (OECD, 2024). Students completed a mathematics assessment and a background questionnaire. We used the student and school questionnaire files (SPSS format), downloaded from the OECD file server on 13 October 2026. SHA-256 checksums of the raw files are recorded in the project repository. The study is reported following the STROBE guidelines for cross-sectional studies (von Elm et al., 2007).

The analysis plan was written and committed to a public repository before any association between the exposure and an outcome was estimated (commit 4ffaa1a, 13 October 2026) [and registered on OSF after the analysis: link]. Deviations from the plan are listed in Supplementary Table S[x].

### Ethics

The data are publicly available and de-identified, and no attempt was made to identify individuals or schools. [Name of body] determined that this analysis did not constitute human-subjects research [or: was exempt from review] on [date].

### Sample

Of the 80 education systems in the public-use file, 73 administered both the additional-instruction item and the life-satisfaction item to at least half of their students. Australia, Belgium, Canada, Israel, Norway, Singapore and the United States did not include the life-satisfaction item. Costa Rica was excluded because the index of economic, social and cultural status (ESCS) was missing for all students. The analytic sample therefore contained 538,815 students in 18,764 schools in 72 systems, 30 of them OECD members. The median sample per system was 6,471 students. No students were excluded on the basis of their responses.

### Measures

**Exposure.** Students were asked: "This school year, which types of <additional mathematics instruction> do you participate in? (Please select all that apply.)" (item ST297). The bracketed term was adapted by each country. The options were one-on-one tutoring with a person; internet or computer tutoring with a programme or application; video-recorded instruction by a person; small-group study or practice (2 to 7 students); large-group study or practice (8 or more students); and "I do not participate in <additional mathematics instruction>". A student was coded as a participant if they ticked at least one form of instruction and did not tick the non-participation option. A student was coded as a non-participant if they ticked only the non-participation option. Three other response patterns were treated as missing: ticking nothing (n = 86,218), ticking one to four forms together with the non-participation option (n = 36,100), and ticking all six options (n = 25,455), which we took as a sign of careless responding. A further 26,019 students had no response to the item. Intensity was measured as the number of forms used (1, 2, or 3 or more), because PISA 2022 did not ask about hours.

**Primary outcome.** Life satisfaction was measured with a single item: "Overall, how satisfied are you with your life as a whole these days?", answered on a scale from 0 (not at all satisfied) to 10 (completely satisfied) (item ST016). It was analysed as a continuous variable. Standardized effects were obtained by dividing by the pooled within-system standard deviation (2.56).

**Secondary outcomes.** Mathematics anxiety was measured with the PISA index ANXMAT, built from six agree/disagree items (for example, "I feel anxious about failing in mathematics") and scaled so that the OECD mean is 0 and the standard deviation 1. Psychosomatic complaints were measured in the 13 systems that ran the optional well-being questionnaire, as the mean frequency of nine symptoms over the past six months (headache, stomach pain, back pain, feeling depressed, irritability, feeling nervous, difficulty getting to sleep, dizziness, feeling anxious). Each symptom was rated from 1 (rarely or never) to 5 (about every day), and at least five of the nine items had to be answered.

**Negative-control outcome.** Students' sense of safety (index FEELSAFE) is based on four items about feeling safe on the way to and from school, in classrooms and elsewhere at school. We chose it because it is likely to share the socioeconomic and school-level confounding of the main analysis, but there is no clear way for mathematics instruction to change it (Lipsitch et al., 2010).

**Covariates.** Covariates were chosen in advance from a directed acyclic graph (Supplementary Figure S[x]). They were sex; age in years, centred at 15.75; grade relative to the modal grade in the country (below, at, above); ESCS; immigrant background (native, second generation, first generation); whether the student had ever repeated a grade, as a proxy for earlier low achievement; school type (public, private), from the school questionnaire; and school location (village or rural area, small town, town, city, large city or megacity). Mathematics achievement, mathematics anxiety, homework time and sense of belonging were not adjusted for in the primary model, because additional instruction may affect them. A covariate missing for more than half of the students in a system was left out of that system's model. This applied to grade in Austria, Iceland and Sweden; immigrant background and grade repetition in Japan; school type in Iceland, Ireland, Macao, Montenegro and Sweden; and school location in Sweden.

### Statistical analysis

All analyses were run separately within each system and then pooled. Within system *c*, we fitted

LS_i = β₀ + β₁·ANY_i + γ′X_i + ε_i,

by weighted least squares, where ANY is the participation indicator and X the covariates, using the final student weight. Standard errors were estimated with the 80 balanced repeated replication (BRR) weights supplied with PISA, using Fay's adjustment with k = 0.5 (Judkins, 1990; OECD, 2009). The sampling variance of a coefficient is then (1/20) Σᵣ(β̂ᵣ − β̂)². The replicate weights reflect the stratified, school-clustered design, so standard errors account for clustering of students within schools.

The primary estimate is the international average of the 72 system-specific β̂₁, in which each system counts equally. Its standard error is the square root of the sum of the system sampling variances divided by the number of systems (OECD, 2009). We also report the average across the 30 OECD systems. There was one pre-specified primary test (two-sided, α = 0.05). All other analyses are exploratory and are reported as estimates with 95% confidence intervals.

**Missing data.** Of the 538,815 students, 42.8% were missing at least one analysis variable. Most of this came from the exposure (32.3%). The outcome was missing for 5.0%, and covariates for between 0% and 9.1% (Supplementary Table S[x]). Because more than 5% of data were missing, the primary analysis used multiple imputation by chained equations with predictive mean matching (van Buuren, 2018), run separately in each system. Each variable was imputed from all other analysis variables plus four auxiliary variables: mathematics anxiety, sense of belonging, the school mean of ESCS and the log of the final student weight. For each missing value, we drew regression coefficients from their approximate posterior and picked the observed value of one of the five closest donors at random. We created 20 imputed datasets with 20 iterations each, using seed 20221 plus the system's index. The participation indicator was derived from the imputed number of forms. Each imputed dataset was analysed with the BRR procedure, and results were combined with Rubin's rules (Rubin, 1987).

**Plausible values.** Mathematics achievement was used only in sensitivity analysis S7. There, the model was fitted once with each of the 10 plausible values, and the results were combined as recommended for PISA: the final estimate is the mean over plausible values, and the variance is the mean sampling variance plus 1.1 times the variance between plausible values (OECD, 2009). Plausible values were never averaged into a single score.

**Heterogeneity across systems.** We pooled the system estimates with a DerSimonian–Laird random-effects model (DerSimonian & Laird, 1986), reporting τ, I² and an approximate 95% prediction interval. In an exploratory meta-regression, we regressed the system estimates on the weighted share of students taking part in additional instruction (per 10 percentage points), with and without OECD membership as a second predictor.

**Sensitivity analyses.** These were specified in advance: complete-case analysis (S1); number of forms as categories (S2); students in the modal grade only (S3); excluding students who used four or five forms (S4), in place of excluding extreme hours, which PISA 2022 did not measure; the negative-control outcome (S5); the E-value (S6), computed from the standardized difference *d* with the approximation RR ≈ exp(0.91·*d*) (VanderWeele & Ding, 2017); additional adjustment for mathematics achievement (S7); random-effects pooling (S8); three alternative codings of the exposure (S9); and excluding systems where more than 40% of students had a missing exposure (S10). S5, S7 and S9 used complete cases, so they should be compared with S1.

**Exploratory analyses.** These examined effect modification by ESCS, sex and grade, using product terms (E1). An interaction term was estimated in a system only if every exposure-by-subgroup cell had at least 30 observed students. This rule was added after a first run produced unstable estimates. We also estimated associations by form of instruction, in a single model containing all five forms (E2). The meta-regression on participation rate is E3, and the secondary outcomes are E4.

**Pipeline check and software.** Before analysing outcomes, we reproduced the published mean mathematics scores of all 79 systems with available reference values (OECD, 2023a). All agreed to within one score point, and the differences were due to rounding. Analyses were run in Python 3.13 with NumPy 2.5, pandas 3.0, SciPy 1.18, statsmodels 0.15 and pyreadstat 1.3. The code, run order and session information are available at [repository URL].

---

## Results

### Sample characteristics

Among students with a valid exposure response, 206,566 reported taking part in some form of additional mathematics instruction and 158,457 reported none. The weighted participation rate averaged 58% across systems, ranging from 16% in Denmark to 84% in Malaysia. Compared with non-participants, participants had slightly higher mean ESCS (−0.33 vs −0.40). They were more likely to have repeated a grade (9.4% vs 7.0%) and to be below the modal grade (16.5% vs 13.8%), and they scored lower in mathematics (438 vs 458 points). They also reported more mathematics anxiety (0.33 vs 0.16) and slightly higher life satisfaction (6.99 vs 6.81) (Table 1).

### Primary result

Participation in additional mathematics instruction was associated with slightly higher life satisfaction. The adjusted international average difference was 0.17 points on the 0–10 scale (95% CI 0.15 to 0.19; p < 0.001). This corresponds to a standardized difference of 0.07 (95% CI 0.06 to 0.08). The direction is opposite to the one we expected in advance. The average across OECD systems was about half as large: 0.09 points (95% CI 0.05 to 0.12). Adjustment changed the estimate little; the unadjusted difference was 0.18 points (95% CI 0.16 to 0.20).

System estimates ranged from −0.21 in Austria to 0.58 in the Dominican Republic (Figure 1). Of the 72 systems, 59 had a positive point estimate. The 95% confidence interval excluded zero in 29 systems with positive estimates and in 2 with negative estimates (Austria, −0.21; Spain, −0.12). Heterogeneity was substantial (τ = 0.16 points; I² = 76%; Q = 299.3, df = 71), and the approximate 95% prediction interval for a new system ran from −0.15 to 0.47. The largest positive associations were in systems in Latin America, Southeast Asia and North Africa. Estimates were close to zero in Hong Kong, Korea, Macao and Chinese Taipei, and negative in several Western European systems.

### Sensitivity analyses

The primary estimate was stable across the pre-specified sensitivity analyses (Table 2). Complete-case analysis gave 0.18 (0.16 to 0.20). Restricting to students in the modal grade gave 0.17 (0.14 to 0.20; 69 systems), and excluding students who used four or five forms gave 0.16 (0.13 to 0.18). Additional adjustment for mathematics achievement left the estimate almost unchanged at 0.17 (0.14 to 0.19), and random-effects pooling gave 0.16 (0.12 to 0.20). The three alternative exposure codings gave estimates from 0.14 to 0.21. Restricting to the 53 systems with no more than 40% missing exposure data gave 0.14 (0.12 to 0.17). The association rose with the number of forms used: 0.14 for one form (0.11 to 0.17), 0.16 for two (0.13 to 0.20) and 0.23 for three or more (0.19 to 0.27), relative to none.

The negative-control outcome was not null. Participants reported a slightly higher sense of safety at school, by 0.02 standard deviations (0.01 to 0.03; 67 systems). That is about one third of the standardized primary estimate. The E-value was 1.32 for the point estimate and 1.29 for the lower confidence limit. An unmeasured confounder associated with both participation and life satisfaction by a risk ratio of 1.32 each, beyond the measured covariates, could therefore account for the whole association.

### Exploratory analyses

Participation was associated with more mathematics anxiety, by 0.17 standard deviations (0.16 to 0.18; 66 systems; positive and significant in 40). It was also associated with more frequent psychosomatic complaints, by 0.06 points on the 1–5 scale (0.04 to 0.08; 13 systems) (Table 3).

The association with life satisfaction weakened as ESCS rose: the interaction was −0.05 per ESCS unit (−0.07 to −0.02). There was no clear modification by sex (0.03; −0.01 to 0.08) or by being below (0.06; −0.02 to 0.14; 54 systems) or above (−0.03; −0.13 to 0.07; 40 systems) the modal grade.

In a model including all five forms, the association was concentrated in group formats: large-group study, 0.18 (0.14 to 0.21), and small-group study, 0.11 (0.08 to 0.13). It was smaller for online tutoring, 0.06 (0.03 to 0.09), and one-on-one tutoring, 0.03 (0.01 to 0.06), and absent for video-recorded instruction, −0.01 (−0.04 to 0.02).

System estimates were more positive where participation was more common: 0.047 points per 10 percentage points of participation (0.022 to 0.073; p < 0.001; Figure 2). When OECD membership was added to the model, the slope fell to 0.032 (SE 0.016; p = 0.04).

---

## Tables

**Table 1. Characteristics of students by participation in additional mathematics instruction.** Values are international averages of within-system weighted means or percentages. Only students with a valid exposure response are included.

| | No additional instruction | Any additional instruction |
|---|---|---|
| Students, unweighted n | 158,457 | 206,566 |
| Life satisfaction (0–10), mean | 6.81 | 6.99 |
| Female, % | 53.0 | 54.6 |
| ESCS, mean | −0.40 | −0.33 |
| Immigrant background, % | 9.2 | 9.5 |
| Repeated a grade, % | 7.0 | 9.4 |
| Below modal grade, % | 13.8 | 16.5 |
| Above modal grade, % | 9.5 | 8.8 |
| Private school, % | 20.5 | 18.8 |
| Mathematics anxiety (index), mean | 0.16 | 0.33 |
| Feeling safe (index), mean | −0.10 | −0.08 |
| Mathematics score (10 plausible values), mean | 458 | 438 |

**Table 2. Primary and sensitivity estimates.** Adjusted difference in life satisfaction (0–10), participants minus non-participants, as the international average of system estimates.

| Analysis | Systems | Difference (95% CI) | Standardized |
|---|---|---|---|
| **Primary (multiple imputation)** | 72 | **0.17 (0.15 to 0.19)** | 0.07 |
| Unadjusted, complete case | 72 | 0.18 (0.16 to 0.20) | 0.07 |
| S1 Complete case | 72 | 0.18 (0.16 to 0.20) | 0.07 |
| S2 One form vs none | 72 | 0.14 (0.11 to 0.17) | 0.06 |
| S2 Two forms vs none | 72 | 0.16 (0.13 to 0.20) | 0.06 |
| S2 Three or more forms vs none | 72 | 0.23 (0.19 to 0.27) | 0.09 |
| S3 Modal grade only | 69 | 0.17 (0.14 to 0.20) | 0.07 |
| S4 Excluding 4–5 forms | 72 | 0.16 (0.13 to 0.18) | 0.06 |
| S7 Adjusted for mathematics achievement | 72 | 0.17 (0.14 to 0.19) | 0.07 |
| S8 Random-effects pooling | 72 | 0.16 (0.12 to 0.20) | 0.06 |
| S9a Ticked nothing = non-participant | 72 | 0.14 (0.12 to 0.16) | 0.05 |
| S9b Contradictory = participant | 72 | 0.16 (0.14 to 0.19) | 0.06 |
| S9c Ticked all = participant | 72 | 0.21 (0.18 to 0.23) | 0.08 |
| S10 Systems with ≤40% missing exposure | 53 | 0.14 (0.12 to 0.17) | 0.06 |
| S5 Negative control: feeling safe (SD units) | 67 | 0.02 (0.01 to 0.03) | 0.02 |
| S6 E-value (point / lower CI limit) | | 1.32 / 1.29 | |

**Table 3. Exploratory estimates.**

| Analysis | Systems | Estimate (95% CI) |
|---|---|---|
| Mathematics anxiety (SD units) | 66 | 0.17 (0.16 to 0.18) |
| Psychosomatic complaints (1–5 scale) | 13 | 0.06 (0.04 to 0.08) |
| Interaction with ESCS (per unit) | 72 | −0.05 (−0.07 to −0.02) |
| Interaction with female sex | 72 | 0.03 (−0.01 to 0.08) |
| Interaction with below modal grade | 54 | 0.06 (−0.02 to 0.14) |
| Interaction with above modal grade | 40 | −0.03 (−0.13 to 0.07) |
| One-on-one tutoring | 72 | 0.03 (0.01 to 0.06) |
| Internet or computer tutoring | 72 | 0.06 (0.03 to 0.09) |
| Video-recorded instruction | 72 | −0.01 (−0.04 to 0.02) |
| Small-group study (2–7 students) | 72 | 0.11 (0.08 to 0.13) |
| Large-group study (8 or more) | 72 | 0.18 (0.14 to 0.21) |
| Meta-regression: participation rate (per 10 points) | 72 | 0.047 (0.022 to 0.073) |
| Same, adjusted for OECD membership | 72 | 0.032 (0.001 to 0.063) |

## Figure legends

**Figure 1.** Adjusted difference in life satisfaction (0–10) between students who did and did not take part in additional mathematics instruction during the school year, by education system. Squares are system estimates with 95% confidence intervals from balanced repeated replication and multiple imputation. Blue marks OECD members and grey partner systems. The diamond is the international average (each system weighted equally). The dashed line marks no difference.

**Figure 2.** System estimates from Figure 1 plotted against the weighted percentage of students in the system who took part in additional mathematics instruction. Marker area is proportional to the inverse of the sampling variance. The line is the random-effects meta-regression fit. Blue marks OECD members and grey partner systems.

## Supplement checklist

S1 deviations from the protocol (from `DEVIATIONS.md`); S2 missing data by variable and system (`results/missingness*.csv`); S3 exposure response patterns (`results/exposure_patterns.csv`); S4 all system estimates (`results/system_estimates.csv`); S5 the directed acyclic graph (`dag.txt`, drawn with dagitty); S6 validation against published means (`results/validation.csv`); S7 STROBE checklist (`STROBE.md`).

## References used above (check each one)

- DerSimonian, R., & Laird, N. (1986). Meta-analysis in clinical trials. *Controlled Clinical Trials, 7*(3), 177–188.
- Judkins, D. R. (1990). Fay's method for variance estimation. *Journal of Official Statistics, 6*(3), 223–239.
- Lipsitch, M., Tchetgen Tchetgen, E., & Cohen, T. (2010). Negative controls: A tool for detecting confounding and bias in observational studies. *Epidemiology, 21*(3), 383–388.
- OECD. (2009). *PISA data analysis manual: SPSS* (2nd ed.). OECD Publishing.
- OECD. (2023a). *PISA 2022 results (Volume I): The state of learning and equity in education*. OECD Publishing.
- OECD. (2024). *PISA 2022 technical report*. OECD Publishing.
- Rubin, D. B. (1987). *Multiple imputation for nonresponse in surveys*. Wiley.
- van Buuren, S. (2018). *Flexible imputation of missing data* (2nd ed.). CRC Press.
- VanderWeele, T. J., & Ding, P. (2017). Sensitivity analysis in observational research: Introducing the E-value. *Annals of Internal Medicine, 167*(4), 268–274.
- von Elm, E., Altman, D. G., Egger, M., Pocock, S. J., Gøtzsche, P. C., & Vandenbroucke, J. P. (2007). The Strengthening the Reporting of Observational Studies in Epidemiology (STROBE) statement. *The Lancet, 370*(9596), 1453–1457.
- For the introduction and discussion: Karakus et al. (2024), https://doi.org/10.1186/s40536-024-00228-5; Liang, Wang & Wu (2022), https://doi.org/10.3389/fpsyg.2022.860179; Zhang & Bray (2020), https://doi.org/10.1111/ejed.12413; PMID 35305796 (peers' tutoring and depression, Korea); PMID 33573032 (Taiwan); PMID 40723669 (China).
