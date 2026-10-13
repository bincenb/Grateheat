# School mobile-phone bans and adolescent psychosomatic complaints: a pre-registered cross-sectional analysis of 111,616 students in 14 education systems (PISA 2022)

[Author], [affiliation]. Draft, 13 October 2026.

## Abstract

**Background.** Many governments have banned mobile phones in schools since 2023, partly on health grounds, but evidence on students' health is limited to single-jurisdiction studies.

**Methods.** Pre-registered cross-sectional analysis of PISA 2022 in the 14 education systems that administered the HBSC Symptom Checklist (111,616 students aged 15 in 4,520 schools across Europe, Latin America, Asia, the Middle East and Oceania). Exposure: the principal's report that phones are not allowed on school premises. Primary outcome: mean frequency of nine psychosomatic complaints over six months (1 = rarely or never, 5 = about every day). Weighted regression with system fixed effects, adjustment for student and school socioeconomic and demographic characteristics, balanced repeated replication variance, and multiple imputation of the missing exposure and covariates (20 datasets).

**Results.** 42% of students (system average; range 8% in the Netherlands to 76% in the United Arab Emirates) attended a school with a phone ban. The adjusted difference in psychosomatic complaints between ban and no-ban schools was +0.001 points (95% CI −0.020 to 0.022; p = 0.91), or 0.001 SD. The confidence interval excludes differences larger than 0.022 SD in either direction. There were no differences in multiple health complaints (−0.3 percentage points, −1.3 to 0.7, on a base of 42%), difficulty getting to sleep (−0.014, −0.045 to 0.017), psychological or somatic subscales, or self-rated health. System-specific estimates were consistent (I² = 5%). Every sensitivity analysis of the primary estimate gave values between −0.006 and +0.007, and a negative-control outcome (height) was null. An apparent difference by sex in the pooled interaction model disappeared in sex-stratified and within-system analyses.

**Conclusions.** Fifteen-year-olds in schools that ban phones reported psychosomatic complaints and sleep-onset difficulty as often as similar students in schools without bans. The precision of the estimate rules out all but very small associations. Policies that ban phones in school are unlikely to improve these health outcomes on their own, though cross-sectional data cannot exclude effects masked by schools adopting bans in response to student problems.

## Introduction

Since 2023, governments across Europe, Latin America, Asia and Australasia have restricted or banned mobile phones in schools. The Netherlands, England, Brazil, several Australian states and many US states are among them. The stated reasons usually include classroom distraction and student health: less phone use during the school day is expected to reduce anxiety, cyberbullying and sleep problems. The evidence on the health side is thin. In England, the SMART Schools study compared 30 schools with restrictive or permissive policies and found no difference in mental wellbeing (Goodyear et al., 2025). A natural experiment in South Australia found a small reduction in psychological distress one year after a statewide ban (Baggio et al., 2025). Both are single-jurisdiction studies of about 1,000 to 1,200 students.

PISA 2022 has two features that make a larger test possible. Principals in every participating school reported whether "the use of cell phones is not allowed on the school premises", and 15 education systems also gave students the optional Well-Being Questionnaire, which includes the 9-item symptom checklist from the Health Behaviour in School-aged Children study (HBSC-SCL). Analyses of PISA 2022 so far have linked phone bans to classroom distraction, to anxiety when the phone is not nearby, to switching off notifications at night, and to achievement (OECD, 2024; Inter-American Development Bank, n.d.). As far as we found, none has used a general, validated measure of health complaints that does not mention phones.

We asked whether students in schools with a phone ban report psychosomatic complaints less often than comparable students in schools without one. The hypothesis, the outcome, the adjustment set and all sensitivity analyses were fixed in a pre-analysis plan before any outcome was examined.

## Methods

### Design and data

This is a secondary, cross-sectional analysis of the PISA 2022 student and school questionnaire files (OECD, 2023), collected in 2022. PISA draws a two-stage stratified sample: schools with probability proportional to size, then up to 42 students aged 15 years 3 months to 16 years 2 months within each school. The pre-analysis plan (`PROTOCOL.md`) was committed to a public repository at commit `430d8a0` before any exposure–outcome model was run. Changes after that point are listed in `DEVIATIONS.md`. Reporting follows STROBE.

### Participants

Fifteen systems administered the Well-Being Questionnaire. France did not administer the symptom checklist, which left 14 systems: United Arab Emirates, Brazil, Costa Rica, Spain, Hong Kong (China), Hungary, Ireland, Macao (China), Mexico, the Netherlands, New Zealand, Panama, Saudi Arabia and Slovenia. Students were included if they answered at least 7 of the 9 symptom items. There was no sample-size calculation; all eligible students were used.

### Measures

*Exposure.* The school principal's answer to "The use of [cell phones] is not allowed on the school premises" (SC190Q02JA; yes = 1, no = 0), assigned to all sampled students in the school.

*Primary outcome.* The mean of the nine HBSC-SCL items (headache, stomach ache, back ache, feeling low, irritability, nervousness, difficulty getting to sleep, dizziness, anxiety) over the past six months, each scored 1 (rarely or never) to 5 (about every day). Higher scores mean more frequent complaints.

*Secondary outcomes.* Multiple health complaints, the standard HBSC cut-off of at least two symptoms more than once a week; the difficulty-getting-to-sleep item on its own; psychological (5 items) and somatic (4 items) subscales; and self-rated health (1 excellent to 4 poor).

*Covariates.* These were chosen from a causal diagram (`DAG.md`) as plausible common causes of a school's phone policy and its students' complaints. Student level: sex, age, grade relative to the national modal grade (below, modal, above), the PISA index of economic, social and cultural status (ESCS), immigrant background, and grade repetition. School level: public or private, community size (5 levels), log enrolment, and school mean ESCS. All models include system fixed effects, so every comparison is between schools in the same system. Students' phone use, distraction, bullying, sleep, anxiety and achievement were not adjusted for because they may lie on the path from a ban to complaints.

### Statistical analysis

The primary model was a weighted linear regression of the symptom score on the ban indicator, the covariates and system fixed effects. Final student weights were rescaled so that each system contributed equally. Standard errors used the 80 Fay balanced repeated replication weights (k = 0.5), as specified for PISA, which account for stratification and the clustering of students in schools. One primary test was pre-specified (two-sided α = 0.05). All other estimates are reported with 95% confidence intervals and are described as secondary or exploratory.

Before fitting any model, we checked the pipeline by reproducing the OECD's published mean mathematics score for all 15 systems from the 10 plausible values and the replicate weights. Every value was within 0.5 points (`output/tables/qc_math_means.csv`).

### Missing data

The exposure was missing for 12.0% of students, mainly because some schools did not return the questionnaire. Covariates and the exposure were multiply imputed (20 datasets) by two-level chained equations with predictive mean matching. School variables were imputed first at the school level, using school means of the student variables and the outcome; student variables were imputed next. Estimates were combined with Rubin's rules. The outcome was not imputed. Three covariates were missing for an entire system: ESCS in Costa Rica, school type in Macao and school size in New Zealand. These cannot be imputed from within-system information, so they were set to a constant absorbed by the system fixed effect. In practice those systems are not adjusted for that covariate, and sensitivity analysis S12 drops them (`DEVIATIONS.md` D3–D4).

### Sensitivity and exploratory analyses

Pre-specified sensitivity analyses: complete cases (S1); splines for ESCS, age and school ESCS (S2); modal-grade students only (S3); dropping students who reported all nine symptoms daily (S4); a negative-control outcome, self-reported height standardised within system and sex, which a phone ban cannot affect (S5); an E-value (S6); leaving out each system in turn (S7); further adjustment for two other school device policies (S8); random-effects pooling of system-specific estimates (S9); public schools only (S10); further adjustment for mathematics achievement using all 10 plausible values (S11); and, added before results, dropping the three systems with a wholly missing covariate (S12). Exploratory analyses tested interactions of the ban with sex, ESCS, modal grade and OECD membership, estimated the association separately in each system, and compared combinations of a ban with a written school statement on device use. After the pre-specified results were seen, the sex interaction was followed up with sex-stratified and within-system models (post hoc; `DEVIATIONS.md` D8).

### Tables and figures

- Table 1: `output/tables/table1_descriptives.csv`. Table 2: `output/tables/table2_by_system.csv`.
- Figure 1 (`output/figures/fig1_forest_by_system.png`): adjusted difference in psychosomatic score in each system, with the share of students in ban schools in brackets; pooled fixed-effects and random-effects estimates. Lines are 95% CIs.
- Figure 2 (`output/figures/fig2_outcomes_sensitivity.png`): (a) primary and secondary outcomes on their original scales; (b) the primary estimate under each sensitivity analysis. The negative control (height) is in SD units; the psychosomatic score's SD is 1.01, so its units are almost the same. Lines are 95% CIs.
- Figure S1 (`output/figures/figS1_sleep_mhc_by_system.png`): system-specific estimates for (a) difficulty getting to sleep and (b) multiple health complaints.

## Results

### Participants

Of the 135,348 students in the 15 systems that administered the Well-Being Questionnaire, 6,770 were in France, which did not include the symptom checklist, and 16,962 answered fewer than 7 of the 9 items. The analytic sample was 111,616 students in 4,520 schools in 14 systems (`output/tables/flow.csv`). The exposure was missing for 12.0% of students and the other variables for between 0% and 15.3% (Table 1).

Averaged over systems, 42% of students attended a school whose principal reported a phone ban. The range ran from 8% in the Netherlands to 76% in the United Arab Emirates (Table 2). Schools with a ban were more often private (27% vs 16% of students) and in cities of over a million people (24% vs 15%), and enrolled more students of immigrant background (22% vs 16%). They had similar average socioeconomic status (ESCS −0.20 vs −0.19). The mean psychosomatic score was 2.30 (SD 1.01), and 41.7% of students met the criterion for multiple health complaints. Unadjusted, the scores were 2.29 in ban schools and 2.30 in no-ban schools.

### Primary outcome

After adjustment, students in schools with a ban had a psychosomatic score 0.001 points higher than students in schools without one (95% CI −0.020 to 0.022; p = 0.91). In SD units this is 0.001 (−0.020 to 0.022). The fraction of missing information due to imputation was 0.11. The E-value was 1.03 for the point estimate, and 1.00 for the confidence limit because the interval includes zero.

### Secondary outcomes

None of the secondary outcomes differed (Figure 2a): multiple health complaints −0.30 percentage points (−1.33 to 0.74); difficulty getting to sleep −0.014 (−0.045 to 0.017); psychological subscale −0.002 (−0.026 to 0.021); somatic subscale 0.006 (−0.015 to 0.026); self-rated health 0.001 (−0.018 to 0.020).

### Differences between systems

System-specific estimates ranged from −0.084 in the Netherlands (−0.184 to 0.016) to 0.083 in Costa Rica (−0.031 to 0.197). None had a confidence interval that excluded zero, and heterogeneity was low (I² = 5%, τ² = 0.0001, Q = 13.7 on 13 df, p = 0.39; Figure 1). Pooling the system estimates with random effects gave −0.001 (−0.020 to 0.018). The association did not differ between OECD and partner systems (interaction −0.020, −0.061 to 0.022). For sleep-onset difficulty, one system had an interval that excluded zero: Macao, −0.092 (−0.171 to −0.013). With 14 tests, about 0.7 such results are expected by chance (Figure S1).

### Sensitivity analyses

All pre-specified sensitivity analyses agreed with the primary estimate (Figure 2b). The estimates ranged from −0.006 to 0.007: complete cases 0.000 (−0.026 to 0.026; n = 82,627); splines 0.002; modal grade only 0.001; excluding extreme responders −0.005; adjusting for the school's other device policies 0.001; public schools only −0.001; adjusting for mathematics achievement 0.002; dropping the three systems with a wholly missing covariate −0.001; leaving out one system at a time −0.006 to 0.007. The negative-control outcome, height, was also null (−0.008 SD, −0.029 to 0.014).

### Exploratory analyses

A written school statement on device use made no difference, with or without a ban. Compared with schools that had neither, the estimates were: ban and statement −0.002 (−0.040 to 0.036); ban without statement −0.017 (−0.066 to 0.032); statement without ban −0.008 (−0.044 to 0.029). The association did not differ by grade (interaction −0.002, −0.035 to 0.031).

The pooled interaction model suggested that the association differed by sex (ban × female −0.088, −0.124 to −0.051). It also suggested a small difference by socioeconomic status (ban × ESCS −0.022, −0.040 to −0.005). Both models constrain the sex gap, or the ESCS gradient, in complaints to be the same in every system. Because ban prevalence differs between systems, any between-system variation in those gaps can load onto the interaction term. We therefore ran post-hoc checks that relax this constraint (`DEVIATIONS.md` D8). In fully sex-stratified models, which let every covariate and system effect differ by sex, the association was −0.005 (−0.037 to 0.028) in girls and 0.010 (−0.013 to 0.033) in boys. Adding the school's share of girls, or restricting to mixed-sex schools, did not change this. Estimated within each system and pooled, the sex interaction was −0.015 (−0.054 to 0.024). Only 2 of 14 systems had intervals excluding zero, and they pointed in opposite directions (United Arab Emirates −0.103; Costa Rica 0.182). The within-system ESCS interaction was −0.017 (−0.035 to 0.001; I² = 0%). We read the pooled interactions as artefacts of the model, with at most a weak hint that bans go with slightly fewer complaints among better-off students.

## Discussion

In 111,616 adolescents from 14 education systems on five continents, attending a school that bans mobile phones was not associated with how often students reported psychosomatic complaints, sleep-onset difficulty or poorer self-rated health. The estimate is close to zero and precise. The 95% confidence interval excludes differences larger than about 0.02 SD in either direction, a tenth of the size usually called "small". It held across every pre-specified sensitivity analysis, every system, and both sexes.

The result agrees with the SMART Schools study in England, which found no difference in mental wellbeing between restrictive and permissive schools (Goodyear et al., 2025). It is less favourable than the South Australian natural experiment, which reported a 0.94-point reduction on the Kessler K10 (Baggio et al., 2025). Expressed in SD units, that reduction may lie outside our interval, but the two studies differ in design (before–after with one statewide policy), outcome (psychological distress over 30 days) and follow-up time. Earlier PISA 2022 analyses linked bans to less anxiety about being separated from one's phone (Inter-American Development Bank, n.d.). Our results suggest this phone-specific measure does not carry over to general health complaints.

Several explanations are possible, and these data cannot separate them. A ban that exists on paper may not be enforced, and the OECD has noted that bans reported in PISA 2022 are not always enforced effectively (OECD, 2024). Most phone and social-media use happens outside school hours, and evening and night-time use is the more plausible route to sleep problems and somatic complaints. A ban during the school day leaves that use untouched. Schools may also adopt bans because of existing problems, which would hide a real benefit. If so, the masking would have to be almost exactly as large as the benefit in every system, since the system estimates were consistent.

The exploratory analyses carry a methodological lesson. The pooled model's large interaction with sex disappeared once sex differences were allowed to vary by system. A cross-national study that reported only the pooled interaction would have concluded that bans protect girls. Interactions estimated across countries with fixed effects for country main effects only should be checked within countries.

### Strengths and limitations

The strengths are the size and spread of the sample, nationally representative sampling, a validated health measure that does not mention phones, a public pre-analysis plan, adherence to the official PISA variance methods, a pipeline checked against published OECD figures, and a negative-control outcome.

There are several limitations. First, the data are cross-sectional. The ban and the complaints were measured at the same time, and we do not know when each school adopted its policy or whether students' six-month symptom window falls after it. Second, the principal reports whether a rule exists, not whether it is enforced or how strict it is (all-day storage vs in-class only). Third, complaints are self-reported, and the HBSC-SCL was not tested for measurement invariance across the 14 languages here. Because all comparisons are within systems, this affects comparisons of effect sizes between systems more than the pooled estimate. Fourth, Costa Rica has no socioeconomic index in the public file, Macao has no school-type variable and New Zealand has no school size, so those systems were not adjusted for those covariates. Dropping them made no difference. Fifth, the 14 systems chose to run the optional questionnaire and are not a random sample of countries. They do not include the United States, the United Kingdom or Australia, where much of the policy debate is happening. Finally, PISA 2022 predates many recent national bans (the Netherlands from January 2024, for example), so it captures school-level policies that schools chose, not imposed national ones.

### Conclusion

Across 14 education systems, school phone bans were not associated with fewer psychosomatic complaints or sleep difficulties among 15-year-olds, and the data rule out more than a very small association. Governments that adopt bans should not expect them, on their own, to improve these aspects of adolescent health. Health claims for bans need direct evidence, ideally from staggered rollouts that allow before–after comparisons.

### Declarations

Ethics: [to complete: non-human-subjects determination]. Funding: [to complete]. Competing interests: none declared. Data: PISA 2022, OECD. Code and pre-analysis plan: [repository URL]. Pre-registration: `PROTOCOL.md`, commit `430d8a0`, [OSF link to add].

## References

- Baggio S, et al. (2025). Psychological consequences of school mobile phone bans: emulated trial of a natural experiment in South Australia. *Computers in Human Behavior*.
- Goodyear VA, et al. (2025). School phone policies and their association with mental wellbeing, phone use, and social media use (SMART Schools): a cross-sectional observational study. *Lancet Regional Health – Europe*.
- Haugland S, Wold B (2001). Subjective health complaints in adolescence: reliability and validity of survey methods. *Journal of Adolescence*, 24, 611–624.
- Inter-American Development Bank (n.d.). *Mobile Devices and Children's Development: The Case for School Restrictions.* [verify year and authors]
- OECD (2023). *PISA 2022 Database.* OECD Publishing, Paris.
- OECD (2024). *Students, Digital Devices and Success.* OECD Publishing, Paris.
- OECD (2024). *PISA 2022 Technical Report.* OECD Publishing, Paris.
- Rubin DB (1987). *Multiple Imputation for Nonresponse in Surveys.* Wiley.
- VanderWeele TJ, Ding P (2017). Sensitivity analysis in observational research: introducing the E-value. *Annals of Internal Medicine*, 167, 268–274.
- von Hippel PT (2007). Regression with missing Ys: an improved strategy for analyzing multiply imputed data. *Sociological Methodology*, 37, 83–117.
- Wood G, et al. (2023). SMART Schools Study protocol. *BMJ Open*.
