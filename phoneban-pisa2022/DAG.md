# Causal diagram (drawn before analysis)

```
                 System (laws, culture, survey language)  ──────────────┐
                        │                                               │
                        ▼                                               ▼
   School type (public/private), community size, school size,      Psychosomatic
   school mean ESCS  ───────────────►  SCHOOL PHONE BAN ─ ─ ─ ─ ─►   complaints
                        │                    │                          ▲
                        │                    ├──► in-school phone use ──┤ (mediators:
                        │                    ├──► distraction, cyberbullying ─┤  NOT adjusted)
                        │                    └──► (bedtime use?) ──► sleep ───┤
                        ▼                                               │
   Student: sex, age, grade, ESCS, immigrant background, grade repetition ──┘
   (affect which school a student attends AND complaints)

   Unmeasured: school ethos/strictness, prior student mental-health problems
   at the school (could prompt a ban: reverse causation), principal reporting style.
```

**Adjustment set:** system FE + school type + community size + log school size + school mean ESCS + student sex, age, grade, ESCS, immigrant background, grade repetition.

**Deliberately not adjusted:** phone/ICT use, distraction, bullying, belonging, anxiety, sleep and achievement. They lie on or after the path from the ban, so adjusting would block part of the effect or open collider paths.

**Negative-control outcome:** self-reported height. It shares the socioeconomic and regional confounders but cannot be affected by a phone ban.
