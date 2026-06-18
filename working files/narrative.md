# Narrative — the project's argument, step by step

Running, incremental record of the argument. Each step is a factual claim plus the
evidence behind it. No commentary. English only. Append new steps at the bottom.

---

## The question

- **General question (organisers):** What can we conclude about reaching global net-zero CO₂ by 2070?
- **Our research question:** Confronting the 1,564 SCI scenarios with observed reality 2010–2025, (a) are they a credible basis for a probability of net-zero by 2070, and (b) does accounting for their historical accuracy change the share of net-zero pathways?
- **Our answer (one line):** The 2025 world tracks the low-action scenarios, not the net-zero ones; the naive 32% is not a probability (it ranges 20–48% under defensible filters); the required turn has not begun, though a *late* net-zero remains indistinguishable today.

---

## Step 1 — The naive number is a count, not a probability

- 1,564 scenarios; 497 reach net-zero CO₂ by 2070 → 497/1564 ≈ **32%**.
- This is the *share of scenarios* modelling teams chose to run, not a likelihood of the world.
- It is unstable to its own definition:

| "net-zero by…" | share |
|---|---|
| 2060 | 16% |
| 2070 | 31% |
| 2080 | 43% |
| ever (≤2100) | 57% |

→ A number that moves from 16% to 57% with its own definition cannot be read as a probability.

## Step 2 — Observed CO₂ 2010–2025

Global CO₂, energy + industry (Global Carbon Budget 2025), Gt/yr:

| 2010 | 2015 | 2020 | 2025 |
|---|---|---|---|
| 33.4 | 35.4 | 34.8 (COVID dip) | 38.1 |

## Step 3 — The ensemble undershoots 2025

Ensemble mean error (observed − projected), family-weighted, Mt CO₂:

| Year | ME | reading |
|---|---|---|
| 2010 | +405 | calibrated |
| 2015 | +15 | calibrated |
| 2020 | −1,572 | COVID (over-projection) |
| 2025 | **+2,582** | structural under-projection |

Positive = scenarios projected *less* CO₂ than reality.

## Step 4 — The 2020 miss is COVID; the 2025 miss is not

- **2020:** removing the COVID dip flips the error from −1,572 to +378 (interpolated) / +1,028 (forward trend). ~76% of the 2020 bias is COVID. Without COVID the ensemble was near-correct in 2020.
- **2025:** 38.1 Gt is real, with no dip to remove. The pre-COVID trend (+0.31 Gt/yr) extrapolates 2025 to 39.4 Gt; reality (38.1) is on that trend (slightly below). The +2,582 gap is the ensemble assuming a **decline** that did not happen.
- **The 2025 number is the load-bearing one and it survives detrending.**

## Step 5 — Reality sits high in the cloud (calibration)

Percentile of the observed value within the scenario cloud (CO₂):

| Year | percentile | reading |
|---|---|---|
| 2015 | 52nd | calibrated |
| 2020 | 13th | COVID |
| 2025 | **75th** | only 25% of scenarios project as high as reality |

→ The ensemble is biased low in 2025.

## Step 6 — Net-zero scenarios miss more, and miss low

Per-scenario CO₂ error, family-weighted:

| group | mean error | n |
|---|---|---|
| net-zero by 2070 | **+607** | 497 |
| non-net-zero | −23 | 1,094 |

→ Net-zero pathways project systematically less CO₂ than observed. Non-net-zero are near-unbiased.
The gap is robust to scenario / family / project weighting.

## Step 7 — The miss is the assumption, not the model

- Error at 2025 is ordered almost monotonically by assumed climate ambition (AR6 category):

| C1 (1.5°) | C3 (2°) | C6 (<3°) | C7 (<4°) | C8 (>4°) |
|---|---|---|---|---|
| +8,353 | +4,377 | +720 | −2,005 | −6,481 |

- Reality falls between C6 and C7 → a "<3–4°C, low-action" world.
- Variance of the 2025 error explained by the **assumption** (category) ≈ 50%; by the **model** identity ≈ 27%.
- The *same* model, switched from a reference (≥4°C) to an ambitious (≤1.5°C) assumption, swings its 2025 error by **+8,652 Mt** on average — larger than any model-to-model difference.

→ A net-zero scenario "fails" 2025 because the assumed policy did not occur, not because the model computes badly.

## Step 8 — The world is adding, not substituting

Observed vs ensemble median at 2025:

| variable | observed | median proj | ratio |
|---|---|---|---|
| Coal | 164 EJ | 140 EJ | 1.17× |
| Solar PV | 2,392 GW | 1,169 GW | **2.05×** |
| CO₂ | 38.1 Gt | 35.6 Gt | 1.07× |

- Coal AND solar are both under-projected: the world added renewables *on top of* persistent fossils.
- Models embed a **substitution** worldview (cross-scenario error correlation coal↔solar ≈ −0.28): in the models, more renewables means less coal. Reality contradicted the level for both.
- Caveat: 72% under-project both coal and solar, but this ≈ independence (0.82 × 0.90); the signal is in the marginals + the negative correlation, not the joint fraction.

## Step 9 — A trivial rule beats the ensemble on most variables (skill)

Forecast 2025 from 2010–2015 only; skill = |ensemble error| / |rule error| (>1 → rule wins):

| variable | skill | % scenarios beaten |
|---|---|---|
| CO₂ | 2.0 | 81% |
| Coal | 4.7 | 91% |
| Nuclear | 9.9 | 95% |
| GDP | 3.0 | 77% |
| Solar PV | 0.7 | 6% |
| Wind | 0.6 | 34% |

→ On 4 of 6 variables a naive rule beats the whole ensemble. On solar/wind the ensemble wins but is still massively wrong (51% error on PV) — the case for a dedicated forecast.

## Step 10 — Filtering for credibility does not give a stable number

Keep the 25% most accurate scenarios over 2010–2025, then measure the net-zero share:

| filter variable | net-zero share |
|---|---|
| CO₂ | 19% ↓ |
| CO₂ + coal + solar | 22% ↓ |
| Solar | 48% ↑ |

- The corrected share moves in **opposite directions** depending on a defensible variable choice.
- Mechanism: net-zero scenarios were *right* on solar (they foresaw the boom) and *wrong* on CO₂/coal (no decarbonisation) — the "addition" signature at the credibility level.
- **The non-robustness is the result:** there is no single "corrected probability."

## Step 11 — The irreducible floor

- A scenario that decarbonises *late* (after ~2030) tracks 2010–2025 just like a non-net-zero scenario, yet still reaches net-zero by 2070.
- Such late movers cannot be filtered out by a 15-year backtest.
- Hence the net-zero share cannot be pushed below the late-mover floor (~20%): that residual is the irreducible uncertainty.

## Step 12 — The ensemble is overconfident, not just biased (solar)

- An honest empirical forecast (Farmer–Lafond, from 2016) puts solar 2025 in a wide band [2.0–18.0 thousand GW] that **contains** the realised 2,392 GW.
- The IAM ensemble puts the realised outcome at its ~**90th percentile** — a near-impossible high case — and 90% of scenarios sit below reality.
- Caveat: the Farmer–Lafond *central* forecast overshoots (+149%) because solar is an S-shaped diffusion, not a pure exponential. The contribution is the **honest uncertainty**, not the point forecast.

---

## Bottom line (current)

1. The naive 32% is not a probability (Step 1, 10).
2. The 2025 world matches low-action scenarios; net-zero scenarios assumed a turn that has not begun (Steps 3–7).
3. The mechanism is addition, not substitution (Step 8).
4. Correcting for accuracy gives no stable number, with a hard floor (~20%) set by indistinguishable late movers (Steps 10–11).
5. The ensemble is biased low and overconfident, and a trivial rule often beats it (Steps 9, 12).
