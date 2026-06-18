# Part A.1 — Findings (hindcast: bias)

## Overview

We evaluate the SCI 2025 ensemble (1,564 scenarios, 65 models, 41 projects) against observed data for six variables over 2010–2025. For each scenario we compute the forecast error ε = y_obs − ŷ_proj, summarised as ME (bias), MAE (typical magnitude), and RMSE. A positive ε means the scenario **underestimated** reality.

One framing point governs everything below. Each pathway is a *conditional* forecast — emissions *given* an assumed policy/technology path — not a draw from a distribution of futures. So the hindcast can say "trajectories premised on an early turn that has not begun are now the least consistent with observation"; it cannot say "the model computes badly." We keep that distinction throughout.

The ensemble is rebalanced using family weights (1/n_f, 17 families) to correct for the dominance of prolific teams (REMIND, MESSAGE alone = 44% of scenarios).

## Observed data

| Variable | 2010 | 2015 | 2020 | 2025 | Source |
|---|---|---|---|---|---|
| CO₂ emissions (Mt CO₂/yr) | 33,400 | 35,400 | 34,800 | 38,100 | GCB 2025 |
| Coal primary energy (EJ/yr) | 148 | 155 | 152 | 164 | EI StatReview 2025 |
| Solar PV capacity (GW) | 40 | 227 | 714 | 2,392 | IRENA 2026 |
| Wind capacity (GW) | 198 | 433 | 733 | 1,291 | IRENA 2026 |
| Nuclear capacity (GW) | 375 | 383 | 393 | 377 | IAEA PRIS |
| GDP PPP (B US$2010/yr) | 87,774 | 100,690 | 107,100 | 122,000 | IMF/WB |

## Finding 1 — The ensemble undershoots 2025, and 2020 ≠ 2025

The ensemble is well calibrated in 2010–2015 (ME ≈ 0 for CO₂). Two later errors appear, and they have **different causes**.

**CO₂ (family-weighted):**

| Year | ME | MAE | RMSE |
|---|---|---|---|
| 2010 | +405 | 750 | 970 |
| 2015 | +15 | 732 | 1,023 |
| 2020 | −1,572 | 1,860 | 2,433 |
| 2025 | +2,582 | 3,550 | 4,537 |

- **2020 (−1,572) is COVID, not model failure.** The observed 34,800 is artificially low (lockdowns). Against a COVID-free 2020 — interpolating 2015→2025 (≈ 36,750) or extending the 2010–2015 trend (≈ 37,400) — the error flips sign to +378 / +1,028. Roughly three-quarters of the 2020 gap is the shock, and it washes out by 2025.
- **2025 (+2,582) is structural, and it is the load-bearing number.** There is no dip to remove: 38,100 sits almost exactly on the pre-COVID trend (~39,400 extrapolated). Reality did nothing surprising — it kept rising on trend. It is the ensemble that bent away: its median assumed a peak around 2020 and a decline that never came. This is **structural optimism**, and it survives every way of removing COVID. (The 2025 miss is *not* a rebound overshoot — reality is slightly *below* its own pre-COVID trend.)

**Coal:** only 32% of scenarios project coal within ±10% of the observed 2025 record of 164 EJ; the ensemble median projected ~140 EJ.

→ Figure: `figures/partA1_fig1_by_year.png`

## Finding 2 — Net-zero scenarios are biased low (a bias, not imprecision)

Scenarios reaching NZ2070 sit systematically below reality.

**CO₂ (family-weighted, per-scenario metrics averaged over time):**

| Group | ME_j | MAE_j | n |
|---|---|---|---|
| NZ2070 | +607 | 2,165 | 497 |
| non-NZ | −23 | 1,746 | 1,094 |

Three points keep this honest:

1. **It is a bias, not imprecision.** The *typical* error size (MAE) is close, ~6% vs ~5% of a ~35,000 Mt total; the groups are not far apart in *how wrong* they are, only in *direction* (NZ always too low). The net-zero cloud is mis-centred, not less sharp.
2. **It is partly true by construction.** Reaching net zero by 2070 forces a pathway to bend emissions down early; reality did not bend, so an early-bending pathway *must* under-project 2025. The bias is half a definition. A pathway that decarbonises *late* (flat to ~2030, then crashes) is indistinguishable from non-NZ over 2010–2025 — the hindcast only catches early movers.
3. **It is robust.** The NZ−non-NZ gap holds under every weighting (gap of +434 / +837 / +1,281 under family / scenario / project weighting).

*Significance caveat.* A raw KS test gives p < 10⁻¹⁶, but with n ≈ 500/1,100 it is significant for a small effect, and overlapping scenarios make the errors serially dependent — a naive p-value overstates significance (a surrogate-dataset test would be the rigorous check). Read the result as "biased low, robustly," not "dramatically more wrong."

→ Figure: `figures/partA1_fig2_mae_nz.png`

## Finding 3 — The miss is the assumed ambition, not the model class

The 2025 error is ordered almost monotonically by the climate ambition a pathway assumes (AR6 category):

| C1 (≤1.5°) | C3 (≤2°) | C6 (≤3°) | C7 (≤4°) | C8 (>4°) |
|---|---|---|---|---|
| +8,353 | +4,377 | +720 | −2,005 | −6,481 |

Reality lands between C6 and C7 — a "below 3–4°C, low-action" world. Decomposing the variance of the 2025 error attributes **~50% to the assumed ambition and ~27% to the model identity**. The decisive test holds the model fixed: switching one model from a reference (≥4°C) premise to an ambitious (≤1.5°C) premise swings its 2025 error by **+8,652 Mt** on average — larger than any difference between two distinct models. A net-zero pathway misses 2025 because the policy it assumed did not arrive, not because the machine computed badly.

*Economy vs energy models (demoted).* Classifying families as endogenous-macro ("economy") vs partial-equilibrium ("energy") shows a gap *overall* (ME +613 vs −41) but **not at 2025**, where both undershoot comparably (+2,717 vs +2,541); the overall gap is driven by 2020 (energy models missed COVID harder) and is confounded with vintage. The economic-structure split does not bite at the horizon that matters and is not pursued.

→ Figure: `figures/partA1_fig3_dashboard.png` (panel 2)

## Finding 4 — Vintage acts on ambition, not calibration; and horizon barely matters

Classifying projects by vintage — early (≤2017), mid (2018–2020), late (2021–2024):

| Vintage | n | ME 2010 | ME 2025 | MAE_j |
|---|---|---|---|---|
| Early | 289 | +1,117 | +466 | 2,374 |
| Mid | 232 | +622 | +2,840 | 1,879 |
| Late | 1,070 | +426 | +3,280 | 1,943 |

Newer scenarios are better calibrated at their base year (MAE 2010: 685 late vs 1,141 early) but undershoot 2025 **more** (+3,280 vs +466) — they baked in more ambitious decarbonisation that did not materialise. So vintage acts on *assumed ambition*, not on *calibration*. And the NZ−non-NZ gap persists within every vintage group, so the structural optimism of NZ pathways is not a vintage artefact.

Reading vintage as a *forecast origin* (publication year → horizon to 2025) sharpens this: across the 1–8-year horizons here, the absolute CO₂ error at 2025 barely grows with horizon (~10% throughout, slope ~+0.3 %/yr). Distance to target does not separate accurate from inaccurate pathways — assumed ambition does. The ensemble is too time-compressed (all post-2017) to exercise the horizon dimension; a genuine long-horizon test would need the AR5 vintage (~2014 forecasting 2025), which this ensemble does not contain.

→ Figure: `figures/partA1_fig3_dashboard.png` (panel 3)

## Key takeaway

The 2025 world resembles the low-action ensemble, not the net-zero one, and the net-zero pathways are the ones that least track recent reality — because they assumed a turn that has not begun. Crucially, the naive P(NZ2070) ≈ 32% is **not a probability to be revised**: it is the share of scenarios modelling teams chose to run (a conditional-forecast count), and it is unstable to its own definition (16% by 2060, 57% ever). What Part A establishes is not a corrected number but a verdict on the ensemble *as a forecast* — biased low, and premised on a decarbonisation that has not started.

## What this sets up

- **Structure of the errors** (addition vs substitution, cross-variable correlation, autocorrelation) — Part A.2.
- **Forecast quality** (skill vs a naive rule; calibration) — Part A.2.
- **Variable selection** (which observables discriminate credible pathways) — Part B.
- **Filtering and the constructive forecast** (sensitivity of the net-zero share; the cost view) — Part C.

## Caveats

1. **COVID shock**: 2020 includes an unprecedented exogenous event; some 2020 error is the shock, not model deficiency (Finding 1 isolates it).
2. **Hindcast ≠ forecast**: accuracy over 15 years does not guarantee accuracy over 45; and these scenarios are all post-2017, so this is hindcast, not a true out-of-sample forecast.
3. **GDP unit**: observed values assume US$2010; some models may use US$2005.
4. **Nuclear and GDP results** need verification (CO₂ and coal fully validated).

## Files

| File | Description |
|---|---|
| `scripts/partA1_hindcast.py` | Main script (6 variables, weighting, all analyses) |
| `data/observed.xlsx` | Observed data |
| `figures/partA1_fig1_by_year.png` | 6×3 grid: all variables × ME/MAE/RMSE by year |
| `figures/partA1_fig2_mae_nz.png` | MAE NZ vs non-NZ |
| `figures/partA1_fig3_dashboard.png` | Dashboard: NZ + economy/energy + vintage |
