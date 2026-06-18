# Horizon & vintage — closing two side threads

Settles the two axes we set aside: the **economy-vs-energy** split and the **vintage / forecast
horizon** of a scenario. Both converge on the same conclusion as the rest of the project: the
miss is the *assumption*, not the model class and not the forecasting distance.

## Economy vs energy models — demoted, not revived

Tested and dropped. At 2025 the two model classes undershoot almost equally (+2,717 vs +2,541 Mt);
the apparent "economy more optimistic" gap is driven by 2020 (energy models missed COVID harder)
and is confounded with vintage. It is subsumed by the stronger decomposition: the assumed climate
ambition explains ~50% of the 2025 error variance, the model identity ~27%. Not worth a figure.

## Horizon & vintage are one axis — and ambition dominates it

A pathway published in year *P* and read at 2025 forecasts over a horizon of `2025 − P`. SSP (2017)
reaches 2025 from 8 years out; IAM COMPACT (2024) from 1. Farmer & Lafond's forecast-error variance
σ²(τ + τ²/m) predicts that longer horizons should miss by more. **The record does not show it.**

| Horizon to 2025 (yr) | n | mean \|error\| % | mean ambition (AR6 C#) |
|---|---|---|---|
| 1 | 35 | 5% | 3.6 |
| 3 | 168 | 9% | 3.7 |
| 4 | 818 | 10% | 3.8 |
| 7 | 145 | 11% | 4.7 |
| 8 | 161 | 11% | 4.9 |

- **Horizon barely matters.** Mean \|error\| at 2025 hovers ~10% across all horizons; raw slope
  **+0.28 %/yr** (corr horizon↔\|error\| = +0.06). Distance to target does not separate accurate
  from inaccurate pathways.
- **Ambition is the driver, and it is confounded with vintage.** corr(horizon, ambition) = **+0.20**:
  newer cohorts forecast 2025 from *closer* yet miss it by *more*, because they loaded more
  decarbonisation. corr(horizon, signed error) = −0.20 (shorter horizon → more undershoot).
- **The Lafond growth is real but faint once ambition is fixed.** Within climate category the
  \|error\|–horizon slope rises to **+0.45 %/yr** — the horizon effect reappears, but stays small
  against the ambition gradient that masks it.

→ Figure: `horizon_vs_ambition.png`

## The limit is the result → AR5

Every horizon here is short (1–8 yr), one project (ENGAGE) supplies more than half the scenarios at
horizon 4, and the entire ensemble is AR6-vintage (post-2017). This dataset is too compressed in time
to exercise the horizon dimension. The genuine long-horizon test lies outside it: the **IIASA AR5
scenarios of ~2014, forecasting 2025 from 11 years out**, would load the forecast-error law as this
ensemble never can. (Publication years here are assigned by project and approximate.)

---

## Ready-to-paste paragraph (academic register, for `narrative.md` if wanted)

> Two threads we set aside deserve a verdict. The publication date of a scenario and its forecast
> horizon are one axis seen twice: a pathway published in year *P* and read at 2025 forecasts over a
> horizon of 2025 minus *P*, so the SSP runs of 2017 reach 2025 from eight years out while the IAM
> COMPACT runs of 2024 reach it from one. The forecast-error variance of Farmer and Lafond grows with
> that horizon, which predicts that older scenarios should miss 2025 by more. The record does not show
> it. Across the one-to-eight-year horizons available, the mean absolute CO₂ error at 2025 hovers near
> ten percent and grows by 0.28 points per year of horizon, a slope indistinguishable from flat.
> Distance to the target is not what separates an accurate pathway from an inaccurate one. What
> separates them is again the premise: newer scenarios forecast 2025 from closer and miss it by more,
> because vintage and ambition move together, and holding the climate category fixed restores only a
> faint horizon effect of 0.45 points per year. The horizon axis is real but inert here, because every
> horizon in this ensemble is short and every cohort is an AR6 cohort. That last point is the limit,
> not a flourish. The genuine test lies outside the data, in the AR5 scenarios of around 2014 that
> forecast 2025 from eleven years out and would put the forecast-error law under a load this dataset
> never applies.
