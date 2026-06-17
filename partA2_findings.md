# Part A.2 — Findings

## Overview

Part A.1 established that the ensemble undershoots 2025 and that NZ scenarios are more wrong. Part A.2 asks three deeper questions about the *structure* of those errors.

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
| Nuclear | 377 GW | 437 GW | −70 | Models expected more nuclear expansion |
| GDP PPP | 122,000 B$ | 135,538 B$ | −13,400 | Models expected higher growth |

Solar PV observed capacity is **double** the ensemble median. Yet coal also reached a record high. The world is not substituting renewables for fossils at the pace models assume — it is *adding* renewables on top of persistent fossil consumption. This is the energy addition phenomenon.

The nuclear overestimate is consistent: post-Fukushima stagnation and slow new build timelines were not captured by models that projected nuclear expansion. The GDP overestimate suggests models assumed stronger global growth than materialised.

→ Figure: `figures/partA2_fig1_diagnostics.png` (panel 2: ME at 2025)

## Finding 6 — Models embed a substitution worldview

The cross-variable error correlation matrix at 2025 reveals a clear structure:

| Pair | Corr(ε) | Interpretation |
|---|---|---|
| Coal ↔ CO₂ | **+0.80** | Strong — physically linked |
| Solar ↔ Wind | **+0.62** | Strong — renewables move together |
| Coal ↔ Wind | **−0.56** | Strong negative — substitution logic |
| Coal ↔ Solar | **−0.28** | Moderate negative — substitution logic |
| CO₂ ↔ Solar | **−0.34** | Moderate negative |
| Coal ↔ Nuclear | −0.03 | Weak — independent |
| Nuclear ↔ GDP | +0.06 | Weak — independent |

Within the ensemble, scenarios that project more renewables also project less coal (negative correlation). This is the substitution worldview embedded in the models. But Finding 5 showed that the *level* is wrong for both: reality has more coal AND more solar than the median model expects.

The substitution signal is stronger in NZ scenarios (Coal-Solar: −0.303) than in non-NZ (−0.172). Net-zero pathways rely more heavily on the assumption that renewables displace fossil fuels — an assumption that reality is not confirming at the expected pace.

Nuclear and GDP errors are largely independent of the fossil-renewable axis — they are driven by different structural assumptions.

→ Figure: `figures/partA2_fig1_diagnostics.png` (panel 1: correlation heatmap)

## Finding 7 — Energy errors are non-structural, GDP errors are persistent

Temporal autocorrelation ρ(ε₂₀₁₀, ε₂₀₂₅) across scenarios:

| Variable | ρ(2010,2015) | ρ(2010,2025) | Interpretation |
|---|---|---|---|
| CO₂ | +0.624 | **+0.056** | Error evolves — not locked in at base year |
| Coal | +0.565 | **−0.080** | Same — error accumulates with horizon |
| Solar PV | +0.431 | +0.113 | Same |
| Wind | +0.312 | −0.091 | Same |
| Nuclear | +0.593 | +0.146 | Weakly persistent |
| **GDP** | **+0.898** | **+0.701** | **Strongly persistent — structural bias** |

For energy and emissions variables, errors decay with horizon: a model that's wrong in 2010 is not necessarily wrong in 2025. The error comes from the trajectory (how fast things change), not the starting point. This means filtering by base-year accuracy alone would miss the real problem.

GDP is the exception: ρ = +0.70 means GDP errors are locked in at the base year and persist. A model calibrated too high on GDP stays too high. This is consistent with GDP being an exogenous assumption in most models rather than an endogenous outcome.

→ Figure: `figures/partA2_fig1_diagnostics.png` (panel 3: autocorrelation bars)

## Key takeaway

The models think in substitution but the world acts in addition. This is the central structural insight of Part A. It reframes the question: the issue is not just that NZ scenarios are "too optimistic" — it's that they rely on a substitution dynamic (renewables displacing fossils) that is not happening at the expected pace, even though renewable deployment itself exceeds expectations.

## What to test next (→ Part B and C)

**Q4 — Which variables best predict historical accuracy?** We now know 6 variables and their error patterns. But which ones are most *discriminating* — i.e., which ones separate accurate from inaccurate scenarios most cleanly? Coal and Solar PV are candidates (both have large errors and clear addition signal), but we need box plots or LASSO to confirm. → Part B.

**Q5 — How does P(NZ2070) change when we filter?** If we remove scenarios that miss coal by >20% or miss solar by >50%, how many NZ scenarios survive? Does P(NZ2070) drop from 32% to 20%? 10%? The shape of P(NZ2070|threshold) as a function of the filtering criterion is the quantitative punchline. → Part C1.

**Q6 — Can we build a better PV forecast?** The ensemble median for Solar PV 2025 was 1,169 GW vs 2,392 GW observed. A logistic fit on 2010–2025 data + Wright's law for cost would give an independent PV trajectory. Scenarios consistent with this trajectory inherit credibility. → Part C2.

**Q7 — Is the substitution failure regional?** If the addition pattern is driven by Asia (China adding coal AND solar), while OECD countries do substitute, then the ensemble might be right about OECD but wrong about Asia. → R5 regional analysis (optional).

## Files

| File | Description |
|---|---|
| `scripts/partA2_diagnostics.py` | Diagnostics script (addition test, correlations, autocorrelation) |
| `figures/partA2_fig1_diagnostics.png` | 3-panel figure: heatmap + ME bars + autocorrelation |
