# Group Work — Complete Summary

## Part A1 — Hindcast evaluation

**What we do**
- Compare 1,564 scenarios (65 models, 41 projects, 17 families) against observed 2010–2025 data on 6 variables
- ε = observed − projected. Positive = the scenario projected too little
- Three metrics: ME (directional bias), MAE (typical error), RMSE (penalises large deviations) *(bias estimation)*
- Family weighting (1/n_f) to correct ensemble imbalance (REMIND + MESSAGE = 44% of scenarios) *(sampling-bias correction)*

**The ensemble undershoots 2025**
- CO₂: ε = +2,582 Mt (models projected 35,518, reality is 38,100)
- Coal: 2025 record at 164 EJ, ensemble median at 140 EJ, 68% of scenarios outside ±10%
- The 2020 error (−1,572) is COVID — exogenous shock, excusable
- The 2025 error (+2,582) is structural: emissions returned to the pre-COVID trend; the ensemble bet on a decline that never came

**NZ scenarios diverge further from reality**
- NZ: ME_j = +607 (systematically project less emissions than observed)
- Non-NZ: ME_j = −23 (nearly centred on reality)
- Gap is significant *(KS test, p < 10⁻¹⁶)*
- Important nuance: this does not mean NZ models are "bad" — it means the policy and transformation assumptions embedded in NZ trajectories have not materialised over 2010–2025. This is a statement about the world, not about model mechanics

**Economy models vs energy models**
- Economy (REMIND, WITCH, AIM, GEM-E3, IMACLIM, EPPA, CGEM, MERGE — 8 families, 701 scenarios): persistent positive bias +613, structurally more optimistic about decarbonisation *(conditional group means, family-weighted)*
- Energy (MESSAGE, IMAGE, POLES, COFFEE, GCAM, TIAM, PROMETHEUS — 7 families, 883 scenarios): centred (−41) but miss COVID more severely (−2,164 vs −1,264)
- In 2025 both classes err equally (~+2,600) — the post-COVID rebound is a shared blind spot

**Vintage does not save recent models — it indicts them**
- Scenarios do not all start from the same information: an SSP scenario (2015) projects 2025 at 10 years; an ENGAGE scenario (2022) projects 2025 at 3 years
- Late (2021+) are better calibrated in 2010 (MAE 685 vs 1,141) — they had the answer
- But they are MORE wrong in 2025 (ME +3,280 vs +466) — despite more information and a shorter horizon
- Explanation: post-Paris, post-Green Deal projects embedded more ambitious climate policy assumptions that have not materialised in emissions data
- The SCI ensemble reflects the research agenda as much as the physics of the system

**The NZ vs non-NZ gap is robust**
- Persists across all weightings (scenario, model, family)
- Persists within every vintage group (early, mid, late)
- Persists within every model type (economy, energy)

---

## Part A2 — Error diagnostics

**Finding 5 — Energy addition**
- Models underestimate fossil AND renewable deployment simultaneously in 2025
- Coal: +26 EJ (record not anticipated, ensemble median = 140 vs 164 observed)
- Solar PV: +1,004 GW (reality = 2× the median projection: 2,392 vs 1,169 GW)
- Wind: +153 GW (also underestimated)
- Nuclear: −70 GW (overestimated — models expected more nuclear than the post-Fukushima reality)
- GDP: −13,400 B$ (overestimated — models expected more growth)
- The world adds renewables without retiring fossil fuels → addition, not substitution

**Finding 6 — Models embed a substitution worldview**
- Corr(ε_coal, ε_solar) = −0.28 *(Pearson, n ≈ 1,065)*: within the ensemble, more solar → less coal
- The anti-correlation is stronger for NZ (−0.30) than non-NZ (−0.17) — NZ scenarios have a more aggressive substitution logic
- But ME is positive for both → reality sits in a corner of the cloud (top-right: lots of fossil AND lots of solar) where models do not go
- The addition finding comes from the ME (levels); the substitution diagnosis comes from the correlation (internal model structure)

**Finding 7 — GDP is the only structural bias**
- For CO₂, coal, solar, wind: ρ(2010, 2025) ≈ 0 *(Pearson autocorrelation across scenarios)* → the initial error does not predict the final error. Error accumulates along the trajectory, not at the starting point
- For GDP: ρ = +0.70 → bias locked in from the start and persistent (GDP is an exogenous input in most models)
- Consequence: filtering on 2010 accuracy is uninformative for energy variables (ρ ≈ 0), but meaningful for GDP (ρ = 0.70)

→ Figure: `figures/partA2_fig1_diagnostics.png` (3 panels: correlation heatmap + ME bars + autocorrelation)

---

## §2.5 — Skill vs naive rule

**Why we do this**
- Test whether the ensemble adds value over a trivial extrapolation (straight line from 2010–2015) *(forecast skill ratio)*
- If the ruler wins, the ensemble cannot be trusted as a forecast

**Result**
- The trivial rule beats the ensemble on 4/6 variables: CO₂ (skill 2.0), coal (4.7), nuclear (9.9), GDP (3.0)
- The ensemble beats the rule on 2/6: solar (0.7), wind (0.6)
- This is NOT a new finding: the rule wins where reality stayed on trend and the ensemble bet on an inflection — same root cause as the NZ bias
- The ensemble wins on solar/wind because growth is non-linear (exponential) — a straight line cannot capture that, models can
- Nuclear (skill = 9.9) is hollow: nuclear went from 375 to 377 GW in 15 years, "nothing changes" wins by construction

**What it closes**
- The argument "the ensemble is biased but still beats a simple extrapolation" → false on 4/6 variables

→ Figure: `figures/co2_benchmark.png`

---

## §2.6 — Calibration (PIT)

**Why we do this**
- Test whether the ensemble is a well-calibrated probability distribution *(PIT — probability integral transform)* — if reality falls near the median, the ensemble can serve as a probability distribution
- If reality falls in the extremes, one cannot read P(NZ2070) from it

**Result: percentile of observed 2025 in the ensemble**
- GDP: 1st percentile → ensemble massively overestimates GDP
- Nuclear: 20th → overestimated
- CO₂: 75th → underestimated
- Wind: 75th → underestimated
- Coal: 79th → underestimated
- Solar: 90th → strongly underestimated
- Reality is NEVER near the 50th percentile → the cloud is systematically shifted

**Limitations**
- Only one point per variable (2025) — a diagnostic, not a formal PIT test (would need many points at different dates)
- 75th–79th is upper-middle, not a tail — only GDP (1st) and solar (90th) are true extremes

**What it closes**
- The argument "32% is approximate but in the right ballpark" → no, the ensemble is not calibrated, one cannot read a probability from it

→ Figure: `figures/calibration_pit.png`

---

## Part B — Variable selection

**What we look for**
- On which variables do NZ and non-NZ trajectories diverge from reality? Which carry information about the type of trajectory?
- Method 1: box plots + separation score sep = (median_NZ − median_nonNZ) / IQR *(normalised effect size, akin to Cohen's d)*
- Method 2: LASSO — L1 logistic regression computing P(NZ | errors), automatically dropping uninformative variables *(probabilistic classification model)*

**Finding 10 — Three variables discriminate, three do not**
- Coal: sep = +0.46 → NZ trajectories assumed coal decline that did not happen
- CO₂: sep = +0.39 → NZ trajectories assumed emissions decline that did not happen
- Solar PV: sep = −0.32 → NZ trajectories assumed a solar boom that DID happen (and reality exceeded it)
- Wind: sep = −0.08 → no separation
- Nuclear: sep = +0.08 → no separation
- GDP: sep = −0.05 → no separation

**Finding 11 — LASSO confirms exactly the same three, same signs**
- Coal: coefficient +0.34 (higher coal error → more likely NZ)
- CO₂: coefficient +0.22 (higher CO₂ error → more likely NZ)
- Solar: coefficient −0.18 (lower solar error → more likely NZ)
- Wind, Nuclear, GDP: coefficients = 0 (dropped by L1 penalty)
- Robust across regularisation strengths (C = 0.05 to 0.3)
- Not circular: the target (NZ status) is distinct from the predictors (hindcast errors)

**The twist — the three variables contradict each other**
- On coal and CO₂: NZ assumptions about fossil decline did not hold
- On solar: NZ assumptions about the technology boom did hold (and reality exceeded them)
- This is the addition finding seen from the angle of credibility: NZ trajectories are right about clean tech, wrong about fossil phase-out

**Conclusion Part B**
- What separates NZ from non-NZ trajectories against reality is specifically the coal → solar substitution rate. Not GDP, not nuclear, not wind
- Solar deployment exceeds expectations (NZ were right). Coal retirement is not happening (NZ were wrong). The bottleneck is not clean tech deployment — it's fossil phase-out
- One cannot say "NZ trajectories are credible" or "they are not" — they are both, depending on the variable
- Consequence for Part C: filtering on a single variable gives opposite results depending on the choice. Must filter on all three, and accept that the result is not a single number
- CO₂ alone is a trap (Kaya identity: GDP and carbon-intensity errors can cancel → a scenario can land on the right CO₂ for the wrong reasons)

→ Figures: `figures/partB1_boxplots.png`, `figures/partB2_lasso.png`

---

## Part C1 — Filtering and revised NZ share

**What we do**
- Keep the 25% most accurate scenarios (lowest MAE over 2010–2025) and recompute the NZ share
- Test sensitivity to the choice of filtering variable

**Finding 12 — No stable number; ~20% under sensible filters**

| Filter on... | NZ share after filtering | Direction |
|---|---|---|
| CO₂ | ~20% | ↓ drops |
| Coal + CO₂ + solar (multivariate) | ~22% | ↓ drops |
| Solar only | ~48% | ↑ rises |
| Naive (no filter) | ~32% | reference |

- Under any reasonable filter (CO₂ or multivariate): NZ share drops to **~20%** — one third below naive
- Under solar-only filter: rises to ~48% — but solar is the variable everyone misses (90th percentile), so "most accurate on solar" means "least catastrophically wrong among a uniformly wrong field"
- The honest statement is not "anything between 20% and 48%" but: **~20% under any sensible filter, and only a poorly motivated filter lifts it**

**The real result is the non-robustness itself**
- The NZ share depends on the conditioning variable — this is the empirical proof of Part 1's conceptual point
- One cannot extract an unconditional probability from conditional forecasts because the answer depends on the conditioning variable chosen
- We therefore relabel the object: not "the revised probability" but **the sensitivity of the NZ share to credibility filtering**

**Finding 13 — The irreducible floor (~20%)**
- A scenario that stays flat until ~2030 then decarbonises sharply to reach NZ by 2070 is indistinguishable from a non-NZ scenario over 2010–2025
- The 15-year hindcast cannot separate them → filtering cannot push below the late-mover share (~20%)
- This is genuine uncertainty that the record is structurally unable to resolve
- A true out-of-sample test would need older (AR5, ~2014) scenarios forecasting 2025 — absent from this ensemble

→ Figure: `figures/partC_sensitivity.png`

---

## Part C2 — Wright's law: the lock is substitution, not cost

**What we do**
- Fit Wright's law (cost ∝ cumulative capacity^−b) on historical PV cost data *(Wright's law — probabilistic technology forecasting)*
- Estimate the learning rate b with standard error → not a single number but a distribution *(OLS regression with uncertainty)*
- Project cost along each group's (NZ / non-NZ) capacity trajectory
- Produce prediction bands (±2 s.e. ≈ 95%) *(probabilistic forecast with quantified uncertainty)*

**Finding 14 — PV cost converges; NZ ≈ non-NZ**
- PV cost fell from ~2,440 $/kW (2010) to ~250 $/kW (2024) — a 90% drop in 14 years
- Wright's law projects ~38 $/kW by 2070 for NZ pathways, ~43 $/kW for non-NZ
- The two projections are **nearly identical** — clean tech becomes very cheap whether or not the world reaches net zero
- Even at the edges of the ±2 s.e. bands, NZ and non-NZ overlap → the "NZ ≈ non-NZ" reading is robust to learning-rate uncertainty

**What it means**
- If technology cost does not distinguish the NZ world from the non-NZ world, then **cost is not the barrier** to net zero
- The barrier is substitution: the failure to phase out fossil fuels even as renewables boom and cheapen
- NZ scenarios miss reality not because their technology optimism is wrong — it's actually too conservative (solar grew faster than they assumed) — but because they assume a fossil phase-out that is not happening

**Caveats**
- Wright's law is hard to prove strictly superior to a time trend (Moore's law) — cost and production co-evolve (multicollinearity)
- The projection is lines + bands on the learning rate only — trajectory uncertainty and system cost (grids, storage, permitting) are not captured
- The cost of the panel is not the cost of the delivered kWh

→ Figures: `figures/pv_wright_cost_projection_to_2070.png`, `figures/pv_wright_cost_projection_to_2070_log.png`

---

## Overall conclusion

**The 32% is not a probability.** It is a frequency in a convenience sample. It moves from 16% to 57% by sliding the deadline, and from 24% to 39% by changing the weighting.

**The ensemble is biased.** The hindcast shows NZ scenarios systematically diverge from observed reality on emissions and coal. This bias is robust to weighting, model type, and vintage.

**The bias is specifically a substitution bias.** Models underestimate fossil AND renewable deployment simultaneously (addition). They embed a substitution logic (coal-solar anti-correlation) that reality is not confirming.

**Three variables carry the signal, and they contradict.** Coal and CO₂ say "NZ assumptions have not held"; solar says "NZ assumptions were right." There is no neutral credibility filter.

**Filtering gives ~20% under sensible criteria.** But the number depends on the filtering variable (48% under solar only). The non-robustness IS the result: one cannot extract a single number.

**Cost is not the barrier.** Wright's law shows PV costs ~40 $/kW by 2070 whether the world reaches NZ or not. Clean technology is outperforming the models. The barrier is fossil phase-out — substitution, i.e. policy and system inertia, not engineering.

---

## All files

| File | Content |
|---|---|
| **Scripts** | |
| `scripts/partA1_hindcast.py` | 6 variables, weighting, economy/energy, vintage |
| `scripts/partA2_diagnostics.py` | Addition, cross-correlation, autocorrelation |
| `scripts/co2_finding1_simple.py` | CO₂ obs vs projections |
| `scripts/nz_bias.py` | NZ vs non-NZ bias |
| `scripts/co2_benchmark.py` | Skill vs trivial rule |
| `scripts/calibration_pit.py` | Calibration PIT |
| `scripts/co2_kaya.py` | Kaya decomposition |
| `scripts/co2_overview.py` | CO₂ overview |
| `scripts/partB1_boxplots.py` | Box plots + sep |
| `scripts/partB2_lasso.py` | LASSO variable selection |
| `scripts/partC_sensitivity.py` | NZ share vs filtering threshold |
| `scripts/analyse_pv_wind_wright_costs_vetted_log.py` | Wright's law PV + Wind cost |
| **Figures** | |
| `figures/partA1_fig1_by_year.png` | 6 vars × ME/MAE/RMSE by year |
| `figures/partA1_fig2_mae_nz.png` | 6 histograms NZ vs non-NZ |
| `figures/partA1_fig3_dashboard.png` | Dashboard NZ + economy + vintage |
| `figures/partA2_fig1_diagnostics.png` | Correlation + ME 2025 + autocorrelation |
| `figures/co2_finding1_simple.png` | COVID vs structural |
| `figures/nz_bias.png` | NZ bias |
| `figures/co2_benchmark.png` | Skill vs trivial rule |
| `figures/calibration_pit.png` | PIT percentiles |
| `figures/partB1_boxplots.png` | 6 box plots NZ/non-NZ separation |
| `figures/partB2_lasso.png` | LASSO coefficients |
| `figures/partC_sensitivity.png` | NZ share sensitivity to filter |
| `figures/pv_wright_cost_projection_to_2070.png` | PV cost projection (linear) |
| `figures/pv_wright_cost_projection_to_2070_log.png` | PV cost projection (log scale) |
