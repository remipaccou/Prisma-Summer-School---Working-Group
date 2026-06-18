# Part A.2 — Findings (error structure & forecast quality)

## Overview

Part A.1 established that the ensemble undershoots 2025 and that net-zero pathways are biased low. Part A.2 asks two further questions: what is the *structure* of those errors (addition/substitution, cross-variable, over time), and is the ensemble *any good as a forecast* (skill, calibration)?

## Finding 5 — Energy addition, not substitution

Models underestimate fossil AND renewable deployment simultaneously at 2025:

| Variable | Obs 2025 | Median proj | ME 2025 | Ratio obs/proj |
|---|---|---|---|---|
| Coal | 164 EJ | 140 EJ | +26 | 1.17× |
| Solar PV | 2,392 GW | 1,169 GW | +1,004 | **2.05×** |
| Wind | 1,291 GW | 1,069 GW | +153 | 1.21× |
| CO₂ | 38,100 Mt | 35,559 Mt | +2,695 | 1.07× |

Two variables are overestimated:

| Variable | Obs 2025 | Median proj | ME 2025 | Interpretation |
|---|---|---|---|---|
| Nuclear | 377 GW | 437 GW | −70 | Models expected more nuclear |
| GDP PPP | 122,000 B$ | 135,538 B$ | −13,400 | Models expected higher growth |

Observed solar capacity is **double** the ensemble median, yet coal also hit a record. The world is not substituting renewables for fossils at the assumed pace — it is *adding* renewables on top of persistent fossils. This is the addition phenomenon, and it is the central structural insight of Part A.

*Caveat on the joint statistic.* 72% of scenarios under-project coal and solar jointly, but this is close to what independence alone predicts given the two marginals (0.82 × 0.90 ≈ 0.74). The addition signal lives in the *marginals* (both under-projected) and in the negative cross-correlation (Finding 6), not in the joint frequency.

→ Figure: `figures/partA2_fig1_diagnostics.png` (panel 2)

## Finding 6 — Models embed a substitution worldview

Cross-variable error correlation at 2025:

| Pair | Corr(ε) | Interpretation |
|---|---|---|
| Coal ↔ CO₂ | +0.80 | strong — physically linked |
| Solar ↔ Wind | +0.62 | strong — renewables move together |
| Coal ↔ Wind | −0.56 | strong negative — substitution logic |
| Coal ↔ Solar | −0.28 | moderate negative — substitution logic |
| CO₂ ↔ Solar | −0.34 | moderate negative |
| Coal ↔ Nuclear | −0.03 | weak — independent |

Within the ensemble, scenarios that project more renewables project less coal (negative correlation) — the substitution worldview. But Finding 5 showed the *level* is wrong for both: reality has more coal AND more solar than the median. The substitution signal is stronger in NZ scenarios (coal–solar −0.30) than non-NZ (−0.17): net-zero pathways lean harder on renewables displacing fossils, which reality is not confirming at the assumed pace.

→ Figure: `figures/partA2_fig1_diagnostics.png` (panel 1)

## Finding 7 — Energy errors decay with horizon; GDP errors persist

Temporal autocorrelation ρ(ε_2010, ε_2025) across scenarios:

| Variable | ρ(2010,2025) | Interpretation |
|---|---|---|
| CO₂ | +0.056 | error evolves — not locked in at base year |
| Coal | −0.080 | same |
| Solar PV | +0.113 | same |
| Wind | −0.091 | same |
| Nuclear | +0.146 | weakly persistent |
| **GDP** | **+0.701** | strongly persistent — structural |

For energy and emissions, errors decay with horizon: a model wrong in 2010 is not necessarily wrong in 2025 — the error comes from the *trajectory* (how fast things change), not the *starting point*. So filtering on base-year accuracy alone would miss the real problem. GDP is the exception: ρ = +0.70 means GDP error is locked in at the base year and persists, consistent with GDP being an exogenous assumption rather than an endogenous outcome.

→ Figure: `figures/partA2_fig1_diagnostics.png` (panel 3)

## Finding 8 — A trivial rule beats the ensemble on most variables (skill)

A forecast earns trust by beating a naive rule. Standing in 2015 and using only 2010+2015, we predict 2025 with a trivial rule (random walk or linear trend) and with the ensemble median. Skill = |ensemble error| / |rule error| (> 1 means the rule won); "% beaten" is the share of individual scenarios the rule out-predicted.

| Variable | ensemble error | rule error | skill | % beaten |
|---|---|---|---|---|
| CO₂ | 7% | 3% | 2.0 | 81% |
| Coal | 14% | 3% | 4.7 | 91% |
| Nuclear | 16% | 2% | 9.9 | 95% |
| GDP | 11% | 4% | 3.0 | 77% |
| Solar PV | 51% | 75% | 0.7 | 6% |
| Wind | 17% | 30% | 0.6 | 34% |

On four of six variables a two-point rule beats the entire ensemble. Two honest qualifications keep this from over-claiming:

- **It is largely the same fact as Findings 1–3.** The rule wins on CO₂/coal/GDP *because reality stayed on its pre-2015 trend* while the ensemble assumed a departure (decarbonisation) that did not occur. The skill result re-expresses structural optimism; it is not a fully independent leg.
- **Nuclear (skill 9.9) is near-tautological.** Nuclear is essentially flat (375→377 GW), so "nothing changes" is almost perfect by construction and any assumed change loses. The headline number is large but hollow.

On solar/wind the ensemble wins yet is still ~50% wrong on PV — "everyone misses PV, the straight line more so" — which is exactly where a purpose-built method is needed (Part C). *Caveat:* with a single target year, "% beaten" is the robust statistic, not the point skill.

→ Figure: `working files/co2_benchmark.png`

## Finding 9 — The ensemble is biased low as a distribution (calibration)

Findings 1–3 judge the median; Finding 9 asks whether the *spread* is honest. The PIT test: at what percentile of the scenario cloud does observed 2025 fall? A calibrated ensemble would place reality near the 50th, scattered uniformly.

| Variable | percentile of observed 2025 | reading |
|---|---|---|
| GDP | 1st | ensemble far too high |
| Nuclear | 20th | too high |
| CO₂ | 75th | high-ish — low-biased |
| Wind | 75th | high-ish — low-biased |
| Coal | 79th | high-ish — low-biased |
| Solar PV | 90th | far too low |

Read honestly: reality sits **above the centre for every energy/emissions variable**, decisively so for solar (90th) and on the opposite edge for GDP (1st). For CO₂/coal/wind the 75th–79th is upper-middle, not a true tail — so the clean claim is **biased low**, with genuine overconfidence demonstrated for solar and GDP, not for all six. Calibration also drifts with horizon (CO₂ at the 52nd in 2015 → 75th in 2025).

*Method caveat.* With one observation per variable (six points) this is a calibration *diagnostic*, not a formal calibration test — the latter needs many forecast origins. It is suggestive, and consistent with the bias findings, but should be presented as such. Still, it makes the conceptual point: a cloud where reality routinely sits off-centre is not a probability distribution of futures, and ordinary error metrics (MAE) would miss it.

→ Figure: `working files/calibration_pit.png`

## Key takeaway

The models think in substitution; the world acts in addition — renewables exceed expectations while fossils persist. And the ensemble fails the basic forecast tests: a trivial rule beats it on the on-trend variables, and as a distribution it is biased low (overconfident where technology moved fastest). The structural insight (addition) and the forecast-quality verdict (low-biased, no demonstrated skill) point the same way: the net-zero pathways assume a fossil phase-out that is not happening.

## Files

| File | Description |
|---|---|
| `scripts/partA2_diagnostics.py` | Diagnostics (addition test, correlations, autocorrelation) |
| `figures/partA2_fig1_diagnostics.png` | 3-panel: heatmap + ME bars + autocorrelation |
| `working files/co2_benchmark.png` | Skill vs a naive rule |
| `working files/calibration_pit.png` | PIT (where reality falls in the cloud) |
