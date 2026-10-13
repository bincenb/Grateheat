# School mobile-phone bans and adolescent psychosomatic complaints: a pre-registered cross-sectional analysis of 111,616 students in 14 education systems (PISA 2022)

[Author], [affiliation]. Draft, 13 October 2026.

## Abstract

<!-- ABSTRACT -->

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

Pre-specified sensitivity analyses: complete cases (S1); splines for ESCS, age and school ESCS (S2); modal-grade students only (S3); dropping students who reported all nine symptoms daily (S4); a negative-control outcome, self-reported height standardised within system and sex, which a phone ban cannot affect (S5); an E-value (S6); leaving out each system in turn (S7); further adjustment for two other school device policies (S8); random-effects pooling of system-specific estimates (S9); public schools only (S10); further adjustment for mathematics achievement using all 10 plausible values (S11); and, added before results, dropping the three systems with a wholly missing covariate (S12). Exploratory analyses tested interactions of the ban with sex, ESCS, modal grade and OECD membership, estimated the association separately in each system, and compared combinations of a ban with a written school statement on device use.

## Results

<!-- RESULTS -->

## Discussion

<!-- DISCUSSION -->

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
