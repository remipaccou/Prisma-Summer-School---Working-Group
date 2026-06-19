# Slide bullet points

## Slide 1 — CO₂ emissions: SCI ensemble vs observed 2010–2025

- SCI 2025 ensemble: 1,564 pathways from 65 models, projected 2010–2100
- Observed CO₂ from Global Carbon Budget 2025 at four checkpoints (2010, 2015, 2020, 2025)
- Shaded bands: 5th–95th percentile range of NZ2070 (orange) and non-NZ (blue) scenarios
- Hindcast: compare where the ensemble expected us to be vs where we actually are

## Slide 2 — CO₂ error distribution: NZ2070 vs non-NZ scenarios

- For each scenario: compute ε = observed − projected, averaged over 2010–2025 (family-weighted)
- Split into two groups: 497 NZ2070 vs 1,094 non-NZ
- Histogram shows the distribution of per-scenario mean error for each group
- Dashed lines: weighted group means; vertical black line at zero = perfect forecast

## Slide 3 — Forecast skill: ensemble vs linear extrapolation at 2025

- Benchmark: fit a linear trend on 2010–2015 observed data, extrapolate to 2025
- Skill ratio = |ensemble error| / |rule error| — above 1 means the rule wins
- Six variables tested: CO₂, coal, solar PV, wind, nuclear, GDP
- Three naive rules compared (random walk, linear, log-linear); best one retained per variable

## Slide 4 — Variable separation: NZ vs non-NZ across six observables

- For each variable: normalised MAE for every scenario, split NZ vs non-NZ
- Box plots show the two distributions side by side
- Separation score (sep): normalised distance between group medians, akin to Cohen's d
- LASSO logistic regression confirms which variables carry discriminating power

## Slide 5 — PV cost projection to 2070: Wright's law

- Wright's law: cost declines as a power of cumulative production (learning rate via OLS log-log)
- Historical PV cost data 2010–2024 fitted; learning rate b ≈ −0.39 with standard error
- Each group's (NZ / non-NZ) median capacity trajectory used to project cost forward
- Shaded bands: ±2 s.e. on the learning rate, propagated through the projection
