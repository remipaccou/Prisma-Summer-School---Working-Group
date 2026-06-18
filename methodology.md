# Hindcast Evaluation of IAM Scenario Ensembles: Method

## 1. Context and Research Question

The Scenario Compass Initiative (SCI 2025) assembles 1,564 integrated assessment model (IAM) pathways from 65 models. Of these, 497 reach global net zero CO₂ emissions by 2070.

A naive reading divides one count by another, P(NZ2070) = 497/1564 ≈ 32%, and calls it a probability. It is not. **Each IAM pathway is a *conditional* forecast** — a statement of the form "*if* policy, technology cost, and demand follow this path, *then* emissions follow that path." A probabilistic forecast is an *unconditional* predictive distribution: the probability that the outcome falls below a level, given the information available at the forecast origin. **One cannot manufacture an unconditional probability by counting conditional forecasts**: the share reaching net zero is determined by which scenarios modelling teams chose to run, not by the likelihood of the world. This is the single most important framing decision of the project, and it reshapes the question.

We therefore replace "revise the probability" with three nested, answerable questions:

- **Q-A (Calibration).** Read as an implied predictive distribution, is the SCI ensemble *calibrated* against observed 2010–2025 outcomes, or is it biased and overconfident? *Calibration*: events assigned probability p should occur a fraction p of the time. *Sharpness*: conditional on calibration, narrower intervals are better. A narrow interval that misses too often is overconfident.
- **Q-B (Skill).** Does the ensemble *beat a trivial, empirically validated benchmark* (a geometric random walk with drift, or an experience curve)? An ensemble with no skill against a naive rule cannot be trusted to discriminate futures.
- **Q-C (Sensitivity & decision).** Treating each pathway as a conditional forecast, how sensitive is the *share* of net-zero-by-2070 pathways to conditioning on historical credibility — and what is the **irreducible floor** that a 15-year backtest cannot resolve?

We deliver calibration, skill, and a sensitivity curve — **not** an unconditional P(NZ2070). The three project deliverables follow this structure: (1) a calibration assessment of the ensemble (§3); (2) an empirically validated benchmark forecast for the key observables (§5.2); (3) the policy-conditional view via Wright's law (§5.3).

### 1.1 The forecasting object (vocabulary)

| Term | Meaning |
|---|---|
| Predictive distribution | the full distribution over the future outcome, given the information at the forecast origin |
| Horizon τ | how far ahead the forecast reaches |
| Conditional forecast | the outcome *given* that the drivers follow a stated path (an IAM scenario) |
| Unconditional forecast | the outcome marginally, integrating over the drivers (a probability) |
| Calibration | coverage matches the nominal level (an α-quantile is exceeded a fraction α of the time) |
| Sharpness | width of the predictive interval (smaller is better, given calibration) |
| PIT | probability integral transform: where the realised value falls in the predicted distribution |
| Skill | accuracy relative to a naive benchmark; skill > 1 means the benchmark wins |

## 2. Notation

| Symbol | Definition |
|--------|-----------|
| y(v,t) | Observed value of variable v at time t |
| ŷ(j,v,t) | Projected value by scenario j for variable v at time t |
| ε(j,v,t) | Forecast error: y − ŷ |
| J | Total number of scenarios (1,564) |
| T | Set of evaluation years: {2010, 2015, 2020, 2025} |
| N | Set of scenarios reaching net zero CO₂ by 2070 (\|N\| = 497) |
| C(τ) | Set of historically credible scenarios (defined in §5) |
| τ, m | Forecast horizon; training-window length (§5.2) |

Sign convention: a positive ε means the scenario **underestimated** the observed value (projected less CO₂, less coal, less solar than actually occurred). A negative ε means it overestimated.

## 3. Part A — Hindcast as a Backtest

### 3.1 Rationale and a framing caveat

For 2010–2025, observed data are available (Global Carbon Budget, IEA, Energy Institute, IRENA, IAEA). Comparing each pathway's projection to the realised trajectory is a **backtest**: we place ourselves at a past origin, read off the forecast, and score it against what happened.

One caution, stated up front. Because IAM pathways are conditional forecasts, a net-zero pathway that "misses" 2025 may be missing because the *assumed policy did not occur*, not because the *model is wrong*. The defensible claim is therefore not "net-zero models are bad," but: **trajectories premised on an early decarbonisation that has not begun are now less consistent with observation.** This is a statement about the world (policy has not turned), conditioned through the model — and it is what the backtest can legitimately support.

### 3.2 Error metrics and calibration metrics

For each scenario j, variable v, and year t in T, the error is ε = y − ŷ.

**Accuracy (magnitude / bias).**

- **ME** (mean error) = the average of ε over scenarios (or over years) — captures *systematic bias*, the consistent direction of the miss.
- **MAE** (mean absolute error) = the average of |ε| — the *typical magnitude*, regardless of sign.
- **RMSE** (root mean square error) = the square root of the average of ε² — penalises occasional large misses more heavily.

RMSE penalises occasional large misses more than MAE: a scenario perfect three times and off by 4,000 once has the same MAE as one consistently off by 1,000, but a larger RMSE.

**Calibration (the metric the accuracy scores miss).** MAE does not tell us whether the *ensemble spread* is honest. We add, treating the cross-scenario distribution at each year as an implied predictive distribution:

- **PIT** — the percentile of the observed value within the ensemble at year t (the fraction of scenarios that fall below the observed value). A calibrated ensemble places the realised value near the 50th percentile, with PIT values uniform across origins.
- **Coverage** — does the ensemble's central (1−α) band contain the realised value at the nominal rate?

A consistently high PIT (realised value in the upper tail) diagnoses a low-biased, overconfident ensemble — directly answering Q-A.

### 3.3 Why both families of metric

Accuracy without calibration is misleading: an ensemble can have small median error yet be badly overconfident (narrow band, realised value in its tail). Calibration is the property that matters for any probabilistic statement about NZ2070, so it is reported alongside ME/MAE/RMSE rather than instead of them.

### 3.4 Error diagnostics

**Autocorrelation (base-year bias vs trajectory error).** The correlation, across scenarios, between a variable's errors at two different years. High autocorrelation across horizons indicates a *structural* bias locked in at the base year (likely to persist); low autocorrelation indicates a *trajectory* error (the model got the level right but the rate wrong). This distinction governs whether filtering on base-year accuracy is even useful.

**Cross-variable correlation (the embedded worldview).** The correlation, across scenarios, between two variables' errors. If scenarios that overproject coal underproject renewables, the ensemble embeds a *substitution* worldview. This matters for variable selection: filtering on a single variable can be fooled by **compensating errors** (a scenario right on CO₂ but wrong on both coal and solar in offsetting directions).

**Credibility vs NZ2070 status (the central test).** Regress each scenario's error magnitude |ε| on a net-zero dummy (1 if the scenario reaches NZ2070). A positive coefficient means net-zero pathways are historically less accurate. *Caveat (backtesting):* overlapping and reused samples make scored errors serially dependent, so naive significance tests (e.g. a raw KS p-value) overstate significance. Where a hard claim rests on significance, the null should be assessed with **surrogate datasets** (synthetic histories generated under a stated null model and run through the identical procedure), not an off-the-shelf p-value.

### 3.5 Skill against a naive benchmark (Q-B)

A standard first test asks whether the model beats a random walk with drift. We benchmark the ensemble against a trivial forecast trained only on pre-COVID information (2010–2015): a linear trend or a geometric random walk. For each variable,

> **skill = |ensemble error| / |naive-rule error|** — skill > 1 means the naive rule wins.

We also report the share of individual scenarios beaten by the rule. An ensemble that a trivial rule beats on most variables has, by this standard, no demonstrated forecasting skill — and its implied NZ2070 share carries correspondingly little weight.

## 4. Part B — Which Observables Carry the Signal

### 4.1 Rationale

The SCI contains thousands of variables. Part B identifies the few whose realised values most cleanly separate accurate from inaccurate pathways — i.e. *what to monitor in the real world*, and *what to filter on* in Part C. Part A's diagnostics already point to **coal and solar PV** as the discriminating pair (largest, structurally coherent errors; the addition signal). Part B confirms and, critically, motivates a **multivariate** filter so that compensating errors (§3.4) cannot buy a scenario undeserved credibility on CO₂ alone.

### 4.2 Box-plot separation (non-parametric)

Split scenarios into accurate vs inaccurate (MAE below/above a threshold) and, for each candidate variable at 2025, compare the two distributions with side-by-side box plots. Clear separation → informative variable; heavy overlap → uninformative. This is a visual, assumption-light form of forecast encompassing and is the primary Part B deliverable.

### 4.3 Optional: LASSO and PCA

LASSO regression of |ε| on all projected variables (an L1 penalty that shrinks most coefficients to zero) gives an automatic, collinearity-aware ranking of informative variables. **Leakage caveat:** regressing the CO₂ error on the projected CO₂ is near-circular; predict *late-period* error from *early-period* projections, or use variables other than the target. PCA/SVD on the projection matrix can reveal a latent "fossil-intensity" dimension. Both are reported only if they change the coal+solar conclusion; otherwise Part B reduces to the box plots and the multivariate-filter motivation.

## 5. Part C — Sensitivity of the Conditional-Forecast Share, and an Honest Benchmark Forecast

### 5.1 Credibility filtering and the sensitivity curve

We define a multivariate credibility set C(τ) on the variables selected in Part B: the scenarios whose MAE is below the threshold τ on **every** selected variable. We then report the **share** of net-zero pathways surviving the filter:

> **s(τ) = (net-zero scenarios in the credible set) / (all scenarios in the credible set).**

This curve **is** the project's central figure. We label it the *sensitivity of the net-zero share to credibility filtering*, **not** "the revised probability" (§1): it is a sensitivity analysis over a set of conditional forecasts, and reporting it as a probability would repeat the category error the project exposes.

**The irreducible floor.** A 15-year backtest has limited power: a pathway that decarbonises *late* (after ~2030) tracks 2010–2025 just as well as a non-net-zero pathway, yet still reaches NZ2070. Such late movers are observationally indistinguishable from the historical record and **cannot be filtered out**. Hence s(τ) has a floor: it falls from the naive 32% toward, but not below, the late-mover share. Stating this floor is a result, not a footnote — it is the honest limit of what hindcasting can establish.

### 5.2 An empirically validated benchmark forecast (geometric random walk → diffusion)

To answer Q-A/Q-B for the observables that matter, we build our *own* probabilistic forecast — independent of the ensemble — and check that its intervals are calibrated against history.

**Baseline model — geometric random walk with drift.** Work in logs. The log-growth from year to year is a constant drift μ plus noise (mean 0, variance σ²). With a training window of m past growth rates, estimate the drift μ̂ as their mean; the central forecast extends it, ŷ(t+τ) = y(t) + μ̂·τ. The forecast-error variance (Farmer & Lafond 2016) is

> **Var(error) = σ²·(τ + τ²/m)**

— so the (1−α) predictive interval is the central forecast ± z·σ·√(τ + τ²/m) (in practice use the estimated σ̂ and a Student-t with m−1 degrees of freedom). With positive autocorrelation ρ in the noise, the variance scales by (1+ρ)²/(1+ρ²) — intervals widen even when the median is unchanged.

**Diffusion correction for solar PV.** Early exponential-looking data can be the front of an S-shaped diffusion. A pure random-walk (Moore) extrapolation of solar PV therefore *overshoots* at long horizons. We fit instead a one-parameter **Bertalanffy–Richards** S-curve,

> **Y(t) = L / [1 + exp(−β·k·(t − t₀))]^(1/β)**,  where β = 1 recovers the logistic,

backtested by refitting the asymptote L̂ on data up to several origins (e.g. when the curve has reached 5/10/25/50% of L̂) and forecasting forward, then scored by PIT / coverage. **Honest limitation:** the asymptote L is unknown and dominates the long-horizon forecast — results are reported with explicit sensitivity to L̂.

**Validation, not just a line.** The forecast is judged by calibration: do the predictive intervals cover the realised path at the nominal rate (PIT / coverage, proper scores such as CRPS), and how does the realised solar outcome sit relative to the *ensemble's* band? The expected finding — the empirical band contains reality while the IAM ensemble places it in its upper tail — is precisely the calibration failure of Q-A.

### 5.3 The policy-conditional view: Wright's law

Moore forecasts cost unconditionally from time; **Wright's law forecasts cost conditional on a deployment path**, which makes it the relevant tool for policy counterfactuals. Each IAM pathway *is* a deployment path. Writing X = the change in log cumulative production and Y = the change in log unit cost, the differenced model is Y = ω·X + noise, and the cost forecast is conditional on future experience: ŷ(t+τ) = y(t) + ω̂·(sum of future X). Applied to each scenario's solar deployment, this yields an implied cost trajectory; following Way, Ives, Mealy & Farmer (2022), faster deployment drives larger experience-curve cost declines, so pathways that assume an *expensive* transition can be inconsistent with their own deployment. **Caveat:** Wright's law is hard to establish as superior to Moore's law (causality, multicollinearity, co-evolution of cost and production); it is presented as the policy-relevant lens, not as a proven point predictor.

## 6. Data Sources

| Variable | Source | Resolution |
|----------|--------|-----------|
| CO₂ emissions (fossil + industrial) | Global Carbon Budget 2025 (Friedlingstein et al.) | Annual, 2010–2025 |
| CO₂ emissions (cross-check) | IEA Global Energy Review 2025/2026 | Annual |
| Primary energy by fuel (coal, gas, oil) | Energy Institute Statistical Review 2025 | Annual, 2010–2024 |
| Solar PV and wind capacity | IRENA Renewable Capacity Statistics 2025/2026 | Annual, by country |
| Nuclear capacity | IAEA PRIS | Annual |
| SCI scenario ensemble | Scenario Compass Initiative v1.0, IIASA | 5-year steps, 2010–2100 |

Observed data are compiled in `data/observed.xlsx` (and `data/observed_full.xlsx`). A genuine long-horizon, out-of-sample test (e.g. AR5-vintage scenarios from ~2014 forecasting 2025) requires the external **IIASA AR5 Scenario Database**, as the SCI ensemble contains no pre-2017 (pre-AR6) pathways.

## References

- Farmer, J.D. & Lafond, F. (2016). How predictable is technological progress? *Research Policy*, 45(3), 647–665.
- Way, R., Ives, M.C., Mealy, P. & Farmer, J.D. (2022). Empirically grounded technology forecasts and the energy transition. *Joule*, 6(9), 2057–2082.
- Friedlingstein, P. et al. (2026). Global Carbon Budget 2025. *Earth System Science Data*, 18.
- IEA (2026). *Global Energy Review 2026*. Paris: International Energy Agency.
- Energy Institute (2025). *Statistical Review of World Energy 2025*. London.
- Scenario Compass Initiative: https://scenariocompass.org
