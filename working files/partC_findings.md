# Part C — the "corrected net-zero share" is not robust

## The reframe (Lafond, slide 3: "scenarios = conditional forecasts")

An IAM scenario is a **conditional** forecast ("if policy follows this path, then…").
One cannot manufacture an **unconditional** probability by counting conditional forecasts.
So the naive `497/1564 ≈ 32%` is not a probability, and "revising
P(NZ2070)" is ill-posed. We rename it: **sensitivity of the net-zero SHARE to credibility filtering.**

## The result: the NZ share is not even directionally robust

By keeping the scenarios most accurate over 2010-2025, the net-zero share goes in **opposite**
directions depending on the credibility variable (naive = 34%, n=1205 with CO₂+coal+solar):

| Filter (keep 25% most accurate) | NZ share |
|---|---|
| **CO₂** | **19%** ⬇️ |
| balanced (CO₂+coal+solar, ranks) | 22% ⬇️ |
| **Solar** | **48%** ⬆️ |

→ The "corrected NZ share" can be worth **anything between 20% and 48%** depending on a
*defensible* choice of variable. **This non-robustness IS the result** (= slide 3 proven empirically).

## The mechanism (NZ vs non-NZ accuracy, normalized MAE)

| Variable | NZ | non-NZ | |
|---|---|---|---|
| CO₂ | 0.063 | 0.048 | NZ **less** accurate |
| Coal | 0.117 | 0.089 | NZ **less** accurate |
| Solar | 0.340 | 0.401 | NZ **MORE** accurate |

Reality proved **the NZ scenarios right on solar** (they predicted the boom) and **wrong on
CO₂/coal** (no decarbonization). This is the **"addition" signature** at the credibility level:
filtering on what the NZ scenarios missed (CO₂/coal) eliminates them; filtering on what they got right
(solar) keeps them. → `co2_kaya.png` shows the "why CO₂ alone is a trap" version
(GDP/intensity errors that cancel out).

## Consequence for the report

- Keep the `partC_sensitivity.png` figure, **labeled "share sensitivity", not "probability".**
- The **CO₂-only filter is misleading** (Kaya) → this is Part B in one sentence: filter multivariate.
- Next step (Lafond course): (1) ensemble calibration (PIT/coverage), (2) honest
  benchmark (CO₂ random walk; solar **Bertalanffy-Richards** diffusion curve, not Moore),
  (3) conditional view (Wright on each scenario's deployment).
