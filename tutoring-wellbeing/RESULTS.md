# Results: additional mathematics instruction and life satisfaction, PISA 2022

**Suggested title:** *Satisfied but anxious? Additional mathematics instruction and adolescent wellbeing in 72 education systems (PISA 2022)*

All numbers come from `results/all_estimates.csv` and `results/summary.json`. Estimates are adjusted differences between students who took any additional mathematics instruction in the past 12 months and those who took none. Positive values mean higher life satisfaction (0–10 scale) among participants. CIs are 95%.

## Sample

- 72 education systems and 538,815 students (346,779 with complete data). Costa Rica was dropped (no ESCS); 7 systems did not ask the life-satisfaction item.
- On average 58% of students used some form of additional math instruction, ranging from 16% (Denmark) to 84% (Malaysia).
- Mean life satisfaction was 6.96; the pooled within-system SD was 2.56.
- Pipeline check: country mean math scores match the OECD's published values for all 79 systems, to within 1 point (rounding).

## Primary result (pre-registered, one test)

| | Estimate (points) | 95% CI | Standardized (d) |
|---|---|---|---|
| **International average, MI, adjusted** | **+0.169** | 0.145 to 0.194 | 0.066 |
| OECD average (30 systems) | +0.088 | 0.054 to 0.121 | 0.034 |
| Unadjusted, complete case | +0.181 | 0.160 to 0.202 | 0.071 |

- p < 10⁻⁴⁰. The direction is **opposite to the pre-stated expectation**: participants report slightly *higher*, not lower, life satisfaction.
- The effect is **small**: about one-sixth of a point on a 0–10 scale, or 0.07 SD.
- Across systems, 59 of 72 point estimates are positive; 29 are significantly positive and 2 significantly negative (Austria −0.21, Spain −0.12).
- Heterogeneity is large: I² = 76%, τ = 0.16 points. The approximate 95% prediction interval for a new system runs from −0.15 to +0.47.

## Sensitivity analyses

| Check | Estimate | 95% CI |
|---|---|---|
| S1 complete case | +0.180 | 0.158 to 0.202 |
| S3 modal grade only | +0.172 | 0.145 to 0.199 |
| S4 drop students using 4–5 forms | +0.158 | 0.134 to 0.183 |
| S7 also adjusted for math achievement (10 PVs) | +0.166 | 0.144 to 0.189 |
| S8 random-effects pooling | +0.160 | 0.117 to 0.202 |
| S9a "nothing ticked" counted as non-participant | +0.139 | 0.119 to 0.158 |
| S9b contradictory answers counted as participant | +0.165 | 0.143 to 0.186 |
| S9c straight-liners counted as participant | +0.206 | 0.184 to 0.228 |
| S10 systems with ≤40% exposure missing (53) | +0.145 | 0.120 to 0.170 |
| S2 dose: 1 / 2 / 3+ forms vs none | +0.141 / +0.164 / +0.230 | each CI excludes 0 |
| **S5 negative control: feeling safe (SD units)** | **+0.022** | 0.013 to 0.031 |
| **S6 E-value** | **1.32** (CI limit: 1.29) | |

How to read these:

- The estimate is stable across complete-case vs imputed data, grade restriction, achievement adjustment, pooling method and exposure coding. All variants fall between +0.14 and +0.21.
- **The negative control is not null.** Participants also report feeling slightly safer at school, which math tutoring has no obvious way to cause. That points to residual confounding or a general positive-reporting tendency. Its size (0.022 SD) is about a third of the primary effect (0.066 SD), so it does not by itself explain the result, but it does weaken it.
- **The E-value is small.** An unmeasured confounder associated with both tutoring and life satisfaction by a risk ratio of about 1.3 each could fully explain the association. Family support, student engagement and parental aspirations are plausible candidates of that size.

## Exploratory results (not confirmatory)

- **E4, other wellbeing outcomes: the opposite direction.** Participants report *more* mathematics anxiety (+0.17 SD, CI 0.16 to 0.18; 66 systems, 40 significantly positive) and *more* psychosomatic complaints (+0.06 on a 1–5 scale, CI 0.04 to 0.08; 13 systems). Together with the primary result this is the "satisfied but anxious" pattern: slightly happier overall, more anxious about mathematics. Reverse causation (anxious students get sent to tutoring) can explain the anxiety finding.
- **E1, socioeconomic status:** the association is weaker for better-off students (interaction −0.045 per ESCS unit, CI −0.070 to −0.020). It is strongest for disadvantaged students. No clear modification by sex (+0.034, CI −0.007 to 0.076) or grade.
- **E2, form:** in a joint model, large-group study (+0.175) and small-group study (+0.107) carry most of the association. One-on-one tutoring (+0.033) and online tutoring (+0.062) are small, and video instruction is null (−0.010). Group formats are more often school-organized or free, so the positive association may reflect *engagement with school* more than paid "shadow" tutoring.
- **E3, context:** the association is more positive where additional instruction is more common: +0.047 points per 10 percentage points of participation (CI 0.022 to 0.073), correlation 0.40 across systems; see `figures/fig2_prevalence.png`. **Caveat:** adjusting for OECD membership shrinks this to +0.032 (p = 0.04). How common tutoring is goes together with a system's development level, and the two can't be separated with 72 systems. The pattern is clear in the forest plot: the largest positive associations are in Latin American, Southeast Asian and North African systems; East Asian systems (KOR, JPN, TAP, HKG, MAC) are near zero; several Western European systems (AUT, ESP, ITA, SWE) are negative.

## Interpretation (draft for the discussion section)

Across 72 education systems, students who take additional mathematics instruction report very slightly higher life satisfaction than similar students who do not, *and* more mathematics anxiety. The life-satisfaction association is small, varies greatly between systems, shrinks within the OECD, and is partly matched by a negative-control outcome. It should be read as "associated with", not as evidence that tutoring improves wellbeing. The most defensible contributions are:

1. The first cross-national test of tutoring and adolescent wellbeing, finding no evidence of a *general* life-satisfaction cost of additional instruction. This is relevant to policies such as China's 2021 "double reduction", which were justified partly on wellbeing grounds.
2. A divergence between global life satisfaction and subject-specific anxiety, which single-outcome studies would miss.
3. Strong context dependence: the association depends on where a student lives.

## Limitations (for the manuscript)

- Cross-sectional data, so cause and effect can't be separated. Struggling or anxious students may be sent to tutoring (reverse causation); families who pay for tutoring may differ in ways ESCS doesn't capture.
- Life satisfaction is a single self-reported item. Its meaning may differ across languages and cultures, and measurement invariance can't be tested for a single item. Within-system estimates avoid comparing levels across systems, but the size of associations may still differ for measurement reasons.
- The exposure measure is coarse: any form in 12 months, no hours, and not split by paid vs free or remedial vs enrichment.
- 32% of the exposure is missing, largely from patterns that suggest careless responding. MI assumes data are missing at random; the codings in S9 bracket the estimate (+0.14 to +0.21).
- There is no measure of prior achievement; grade repetition is a weak proxy.
- The negative-control outcome is not null, and the E-value is small.
- E3 is an ecological meta-regression with 72 points and is confounded by development level.
- Post-freeze deviations are listed in `DEVIATIONS.md`.

## Before submission

1. Register `PROTOCOL.md` on OSF, noting that it was frozen at commit `4ffaa1a` and that analysis has already been run (be open about this; OSF has a "secondary data, after analysis" option).
2. Get the written exemption determination from your sponsor/school (protocol §2) and check the OECD data terms by hand.
3. Rerun the novelty scan in Google Scholar or Scopus, plus ERIC/PsycINFO (`novelty/NOVELTY.md`, "Limits").
4. Have a second person run `./run_all.sh` from the raw files and compare `results/all_estimates.csv`.
5. Possible journals: *Large-scale Assessments in Education* (published the closest PISA 2022 tutoring paper), *Child Indicators Research*, *Journal of Youth and Adolescence*, *Comparative Education Review*.
