# Deviations from the protocol

The protocol was frozen at commit `4ffaa1a` (2026-10-13). Changes and clarifications made afterwards:

1. **Pipeline smoke test.** After the freeze, the analysis code was test-run on three systems (ESP, IRL, KOR) with a reduced imputation setting (M = 3, 5 iterations) to check that it worked. Nothing in the plan was changed as a result.
2. **Analyses where the method was not specified: complete case was used.** The protocol did not say whether some sensitivity and exploratory analyses use MI or complete cases. These are complete case:
   - S5 (negative-control outcome) and E4 (secondary outcomes). FEELSAFE and PSYSOM were not in the imputation model, so imputed exposures would carry no information about them and would bias these estimates toward zero.
   - S7 (adjustment for math PVs). Complete case keeps the PISA plausible-value rules exact rather than nesting PVs inside imputations.
   - S9 (alternative exposure codings) and the E2 per-form model, which uses the raw form indicators.

   These should be compared with S1 (complete-case primary), not with the MI primary estimate.
3. **Validation reference.** Published means were taken from the Wikipedia tabulation of OECD Table I.B1.2.1, because the OECD site returned 403. Moldova's value there (417) is wrong; the OECD figure is 414, which the pipeline reproduces (414.2).
