# Part A.1 — Findings

## Overview

We evaluate the SCI 2025 ensemble (1,564 scenarios, 65 models, 41 projects) against observed data for six variables over 2010–2025. We compute forecast errors $\varepsilon = y^{obs} - \hat{y}^{proj}$, summarised as ME (bias), MAE (typical magnitude), and RMSE. Positive $\varepsilon$ means the scenario underestimates reality.

The ensemble is rebalanced using family weights ($1/n_f$, 17 families) to correct for the dominance of prolific modelling teams (REMIND, MESSAGE alone = 44% of scenarios).

## Observed data

| Variable | 2010 | 2015 | 2020 | 2025 | Source |
|---|---|---|---|---|---|
| CO₂ emissions (Mt CO₂/yr) | 33,400 | 35,400 | 34,800 | 38,100 | GCB 2025 |
| Coal primary energy (EJ/yr) | 148 | 155 | 152 | 164 | EI StatReview 2025 |
| Solar PV capacity (GW) | 40 | 227 | 714 | 2,392 | IRENA 2026 |
| Wind capacity (GW) | 198 | 433 | 733 | 1,291 | IRENA 2026 |
| Nuclear capacity (GW) | 375 | 383 | 393 | 377 | IAEA PRIS |
| GDP PPP (B US$2010/yr) | 87,774 | 100,690 | 107,100 | 122,000 | IMF/WB |

## Finding 1 — The ensemble undershoots 2025

The ensemble is well calibrated in 2010–2015 (ME ≈ 0 for CO₂). In 2020, models overshoot (they missed the COVID dip). In 2025, models undershoot: the post-COVID rebound and continued fossil fuel use exceeded what most scenarios anticipated.

**CO₂ (family-weighted):**

| Year | ME | MAE | RMSE |
|---|---|---|---|
| 2010 | +405 | 750 | 970 |
| 2015 | +15 | 732 | 1,023 |
| 2020 | −1,572 | 1,860 | 2,433 |
| 2025 | +2,582 | 3,550 | 4,537 |

**Coal:** only 32% of scenarios project coal within ±10% of the observed 2025 record of 164 EJ. The ensemble median projected ~140 EJ.

→ Figure: `figures/partA1_fig1_by_year.png`

## Finding 2 — Net-zero scenarios are more wrong

Scenarios reaching NZ2070 carry systematically larger errors than non-NZ scenarios:

**CO₂ (family-weighted, per-scenario metrics averaged over time):**

| Group | ME_j | MAE_j | n |
|---|---|---|---|
| NZ2070 | +607 | 2,165 | 497 |
| non-NZ | −23 | 1,746 | 1,094 |

The difference is significant (KS test p < 10⁻¹⁶). NZ scenarios project less CO₂ than observed — they assumed faster decarbonisation than has occurred. Non-NZ scenarios are nearly unbiased.

→ Figure: `figures/partA1_fig2_mae_nz.png`

## Finding 3 — Economy models are more optimistic

We classify model families by economic structure:
- **Economy** (endogenous macro): REMIND, WITCH, MERGE, AIM, GEM-E3, IMACLIM, EPPA, CGEM (8 families, 701 scenarios)
- **Energy** (partial equilibrium): MESSAGE, IMAGE, POLES, COFFEE, GCAM, TIAM, PROMETHEUS (7 families, 883 scenarios)

**CO₂ (family-weighted):**

| Class | ME (overall) | ME 2020 | ME 2025 |
|---|---|---|---|
| Economy | +613 | −1,264 | +2,717 |
| Energy | −41 | −2,164 | +2,541 |

Economy models carry a persistent positive bias: they consistently project lower emissions than observed. Energy models are centred overall but miss the COVID dip more severely (bottom-up energy-system models track technical trajectories, not macro shocks). Both classes undershoot 2025 comparably.

→ Figure: `figures/partA1_fig3_dashboard.png` (panel 2)

## Finding 4 — Vintage does not explain the bias

We classify projects by vintage:
- **Early** (≤2017): SSP, ADVANCE, EMF30, EMF33 — 289 scenarios
- **Mid** (2018–2020): CD-LINKS, COMMIT, Deep-Mitigation, etc. — 232 scenarios
- **Late** (2021–2024): ENGAGE, NAVIGATE, NGFS, IAM COMPACT, etc. — 1,070 scenarios

| Vintage | n | ME 2010 | ME 2025 | MAE_j |
|---|---|---|---|---|
| Early | 289 | +1,117 | +466 | 2,374 |
| Mid | 232 | +622 | +2,840 | 1,879 |
| Late | 1,070 | +426 | +3,280 | 1,943 |

Newer scenarios are better calibrated at their base year (MAE 2010: 685 for late vs 1,141 for early). But they undershoot 2025 **more** (+3,280 vs +466) because they baked in more ambitious decarbonisation assumptions that have not materialised.

Crucially, the NZ vs non-NZ gap persists within every vintage group:

| Vintage | NZ ME_j | NZ MAE_j | non-NZ ME_j | non-NZ MAE_j |
|---|---|---|---|---|
| Early | +991 | 2,631 | −584 | 2,310 |
| Mid | +790 | 2,229 | +32 | 1,632 |
| Late | +781 | 2,324 | +134 | 1,764 |

The structural optimism of NZ scenarios is not an artefact of when they were built.

→ Figure: `figures/partA1_fig3_dashboard.png` (panel 3)

## Key takeaway

The world in 2025 looks more like the non-NZ ensemble than the NZ one. The naive $P(NZ2070) \approx 32\%$ treats all scenarios as equally credible, but scenarios that reach net zero are the ones that most poorly track recent reality. This suggests the naive estimate is biased upward.

## Caveats

1. **COVID shock**: 2020–2025 includes an unprecedented exogenous event that no scenario was designed to capture. Some of the measured error is attributable to this shock, not to structural model deficiencies.
2. **Hindcast ≠ forecast**: accuracy over 15 years does not guarantee accuracy over 45 years. A model that correctly tracks coal in 2025 may still be wrong about 2070.
3. **GDP unit**: the GDP PPP observed values assume US$2010 base; some models may use US$2005 — to be verified.
4. **Nuclear and GDP results** need verification in the script output (CO₂ and Coal fully validated).

## Open questions for Part A.2

The findings above are descriptive and largely expected. Three non-trivial questions emerge that require deeper analysis:

### Q1 — Addition vs substitution

Models underestimate coal in 2025. But do they also underestimate solar PV? If ME > 0 for both coal AND solar simultaneously, the real world is in an **energy addition** mode — renewables grow fast but fossil fuels persist — rather than the substitution dynamic embedded in most models (renewables replace fossils). This would be a structural finding about the models' worldview, not just a calibration error.

**Test:** check the sign of ME at 2025 for all 6 variables simultaneously.

### Q2 — Cross-variable error correlation

Do scenarios that overestimate coal also underestimate solar? If errors are anti-correlated (coal↑ ↔ solar↓), the models have a coherent substitution logic that's wrong in both directions. If errors are positively correlated (both↑ or both↓), the error is more of a global scale factor. The correlation matrix of ε across variables tells us whether the bias is a "worldview" problem or a "level" problem.

**Test:** compute Corr(ε_coal, ε_solar), Corr(ε_coal, ε_CO2), etc. across scenarios at 2025.

### Q3 — Regional decomposition

Is the coal error concentrated in Asia (China/India driving the record 2025 levels) or distributed globally? The R5 regional data is available. If the error is Asia-specific, models may capture OECD dynamics correctly but miss non-OECD growth. This has implications for which scenarios to trust regionally.

**Test:** repeat the hindcast on R5 emissions/energy files.

---

| File | Description |
|---|---|
| `scripts/partA1_hindcast.py` | Main script (6 variables, weighting, all analyses) |
| `data/observed.xlsx` | Observed data |
| `figures/partA1_fig1_by_year.png` | 6×3 grid: all variables × ME/MAE/RMSE by year |
| `figures/partA1_fig2_mae_nz.png` | 6 histograms: MAE NZ vs non-NZ |
| `figures/partA1_fig3_dashboard.png` | Dashboard: NZ + economy/energy + vintage |
