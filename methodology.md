# Hindcast Evaluation of IAM Scenario Ensembles: Method

## 1. Context and Research Question

The Scenario Compass Initiative (SCI 2025) assembles 1,564 integrated assessment model (IAM) pathways from 65 models. Of these, 497 reach global net zero CO$_2$ emissions by 2070.

A naive reading divides one count by another, $P(\text{NZ2070}) = 497/1564 \approx 32\%$, and calls it a probability. It is not. Following Lafond (PRISMA lectures; Farmer & Lafond 2016), **each IAM pathway is a *conditional* forecast** — a statement of the form "*if* policy, technology cost, and demand follow this path, *then* emissions follow that path." A probabilistic forecast is an *unconditional* predictive distribution, $F_{t,\tau}(y) = \mathbb{P}(Y_{t+\tau} \le y \mid \mathcal{I}_t)$. **One cannot manufacture an unconditional probability by counting conditional forecasts**: the share reaching net zero is determined by which scenarios modelling teams chose to run, not by the likelihood of the world. This is the single most important framing decision of the project, and it reshapes the question.

We therefore replace "revise the probability" with three nested, answerable questions:

- **Q-A (Calibration).** Read as an implied predictive distribution, is the SCI ensemble *calibrated* against observed 2010–2025 outcomes, or is it biased and overconfident? *Calibration*: events assigned probability $p$ should occur a fraction $p$ of the time. *Sharpness*: conditional on calibration, narrower intervals are better. A narrow interval that misses too often is overconfident (Lafond, calibration–sharpness).
- **Q-B (Skill).** Does the ensemble *beat a trivial, empirically validated benchmark* (a geometric random walk with drift, or an experience curve)? An ensemble with no skill against a naive rule cannot be trusted to discriminate futures.
- **Q-C (Sensitivity & decision).** Treating each pathway as a conditional forecast, how sensitive is the *share* of net-zero-by-2070 pathways to conditioning on historical credibility — and what is the **irreducible floor** that a 15-year backtest cannot resolve?

We deliver calibration, skill, and a sensitivity curve — **not** an unconditional $P(\text{NZ2070})$. The three project deliverables follow this structure: (1) a calibration assessment of the ensemble (§3); (2) an empirically validated benchmark forecast for the key observables (§5.2); (3) the policy-conditional view via Wright's law (§5.3).

### 1.1 The forecasting object (vocabulary)

| Term | Meaning |
|---|---|
| Predictive distribution $F_{t,\tau}$ | full distribution over $Y_{t+\tau}$ given information $\mathcal{I}_t$ at the forecast origin $t$ |
| Horizon $\tau$ | how far ahead the forecast reaches |
| Conditional forecast | $Y$ given that $X$ follows a stated path (an IAM scenario) |
| Unconditional forecast | $Y$ marginally, integrating over $X$ (a probability) |
| Calibration | coverage matches nominal level: $\mathbb{P}(Y_{t+\tau} \le q_{\alpha}) \approx \alpha$ |
| Sharpness | width of the predictive interval (smaller is better, given calibration) |
| PIT | probability integral transform: where the realised value falls in the predicted CDF |
| Skill | accuracy relative to a naive benchmark; skill $>1$ means the benchmark wins |

## 2. Notation

| Symbol | Definition |
|--------|-----------|
| $y_{v,t}$ | Observed value of variable $v$ at time $t$ |
| $\hat{y}_{j,v,t}$ | Projected value by scenario $j$ for variable $v$ at time $t$ |
| $\varepsilon_{j,v,t}$ | Forecast error: $y_{v,t} - \hat{y}_{j,v,t}$ |
| $J$ | Total number of scenarios (1,564) |
| $T$ | Set of evaluation years: $\{2010, 2015, 2020, 2025\}$ |
| $\mathcal{N}$ | Set of scenarios reaching net zero CO$_2$ by 2070 ($|\mathcal{N}| = 497$) |
| $\mathcal{C}_\tau$ | Set of historically credible scenarios (defined in §5) |
| $\tau$, $m$ | Forecast horizon; training-window length (Lafond model, §5.2) |

Sign convention: a positive $\varepsilon$ means the scenario **underestimated** the observed value (projected less CO$_2$, less coal, less solar than actually occurred). A negative $\varepsilon$ means it overestimated.

## 3. Part A — Hindcast as a Backtest

### 3.1 Rationale and a framing caveat

For 2010–2025, observed data are available (Global Carbon Budget, IEA, Energy Institute, IRENA, IAEA). Comparing each pathway's projection to the realised trajectory is a **backtest**: we place ourselves at a past origin, read off the forecast, and score it against what happened.

One caution, stated up front. Because IAM pathways are conditional forecasts, a net-zero pathway that "misses" 2025 may be missing because the *assumed policy did not occur*, not because the *model is wrong*. The defensible claim is therefore not "net-zero models are bad," but: **trajectories premised on an early decarbonisation that has not begun are now less consistent with observation.** This is a statement about the world (policy has not turned), conditioned through the model — and it is what the backtest can legitimately support.

### 3.2 Error metrics and calibration metrics

For each scenario $j$, variable $v$, and year $t \in T$, $\varepsilon_{j,v,t} = y_{v,t} - \hat{y}_{j,v,t}$.

**Accuracy (magnitude / bias).**

$$\text{ME}_{v,t} = \tfrac{1}{J}\!\sum_j \varepsilon_{j,v,t}, \qquad
\text{MAE}_{j,v} = \tfrac{1}{|T|}\!\sum_{t}|\varepsilon_{j,v,t}|, \qquad
\text{RMSE}_{j,v} = \sqrt{\tfrac{1}{|T|}\!\sum_{t}\varepsilon_{j,v,t}^2}.$$

ME captures systematic bias; MAE the typical magnitude; RMSE penalises occasional large misses more heavily (a scenario perfect three times and off by 4,000 once has the same MAE as one consistently off by 1,000, but a larger RMSE).

**Calibration (the metric the accuracy scores miss).** MAE does not tell us whether the *ensemble spread* is honest. We add, treating the cross-scenario distribution at each year as an implied predictive distribution:

- **PIT** — the percentile of the observed value within the ensemble at year $t$: $\text{PIT}_{v,t} = \tfrac{1}{J}\sum_j \mathbb{1}[\hat{y}_{j,v,t} < y_{v,t}]$. A calibrated ensemble places the realised value near the 50th percentile, with PIT values uniform across origins.
- **Coverage** — does the ensemble's central $1-\alpha$ band contain the realised value at the nominal rate?

A consistently high PIT (realised value in the upper tail) diagnoses a low-biased, overconfident ensemble — directly answering Q-A.

### 3.3 Why both families of metric

Accuracy without calibration is misleading: an ensemble can have small median error yet be badly overconfident (narrow band, realised value in its tail). Calibration is the property that matters for any probabilistic statement about NZ2070, so it is reported alongside ME/MAE/RMSE rather than instead of them.

### 3.4 Error diagnostics

**Autocorrelation (base-year bias vs trajectory error).** $\rho_v(t_0,t_1) = \mathrm{Corr}_j(\varepsilon_{j,v,t_0}, \varepsilon_{j,v,t_1})$. High autocorrelation across horizons indicates a *structural* bias locked in at the base year (likely to persist); low autocorrelation indicates a *trajectory* error (the model got the level right but the rate wrong). This distinction governs whether filtering on base-year accuracy is even useful.

**Cross-variable correlation (the embedded worldview).** $\rho(v_1,v_2) = \mathrm{Corr}_j(\varepsilon_{j,v_1,t}, \varepsilon_{j,v_2,t})$. If scenarios that overproject coal underproject renewables, the ensemble embeds a *substitution* worldview. This matters for variable selection: filtering on a single variable can be fooled by **compensating errors** (a scenario right on CO$_2$ but wrong on both coal and solar in offsetting directions).

**Credibility vs NZ2070 status (the central test).** $|\varepsilon_{j,v,t}| = \alpha + \beta\,\mathbb{1}[j \in \mathcal{N}] + u_j$. If $\beta > 0$, net-zero pathways are historically less accurate. *Caveat (Lafond, backtesting):* overlapping and reused samples make scored errors serially dependent, so naive significance tests (e.g. a raw KS $p$-value) overstate significance. Where a hard claim rests on significance, the null should be assessed with **surrogate datasets** (synthetic histories generated under a stated null model and run through the identical procedure), not an off-the-shelf $p$-value.

### 3.5 Skill against a naive benchmark (Q-B)

Following Lafond's opening test ("is the model better than a random walk with drift?"), we benchmark the ensemble against a trivial forecast trained only on pre-COVID information (2010–2015): a linear trend or a geometric random walk. For each variable,

$$\text{skill}_v = \frac{|\,\text{error}_\text{ensemble}\,|}{|\,\text{error}_\text{naive rule}\,|}, \qquad \text{skill} > 1 \Rightarrow \text{the naive rule wins.}$$

We also report the share of individual scenarios beaten by the rule. An ensemble that a trivial rule beats on most variables has, by Lafond's standard, no demonstrated forecasting skill — and its implied NZ2070 share carries correspondingly little weight.

## 4. Part B — Which Observables Carry the Signal

### 4.1 Rationale

The SCI contains thousands of variables. Part B identifies the few whose realised values most cleanly separate accurate from inaccurate pathways — i.e. *what to monitor in the real world*, and *what to filter on* in Part C. Part A's diagnostics already point to **coal and solar PV** as the discriminating pair (largest, structurally coherent errors; the addition signal). Part B confirms and, critically, motivates a **multivariate** filter so that compensating errors (§3.4) cannot buy a scenario undeserved credibility on CO$_2$ alone.

### 4.2 Box-plot separation (non-parametric)

Split scenarios into accurate vs inaccurate (MAE below/above a threshold) and, for each candidate variable at 2025, compare the two distributions with side-by-side box plots. Clear separation $\Rightarrow$ informative variable; heavy overlap $\Rightarrow$ uninformative. This is a visual, assumption-light form of forecast encompassing and is the primary Part B deliverable.

### 4.3 Optional: LASSO and PCA

LASSO regression of $|\varepsilon|$ on all projected variables (L1 penalty shrinking most coefficients to zero) gives an automatic, collinearity-aware ranking of informative variables. **Leakage caveat:** regressing $|\varepsilon_{\text{CO}_2}|$ on projected CO$_2$ is near-circular; predict *late-period* error from *early-period* projections, or use variables other than the target. PCA/SVD on the projection matrix can reveal a latent "fossil-intensity" dimension. Both are reported only if they change the coal+solar conclusion; otherwise Part B reduces to the box plots and the multivariate-filter motivation.

## 5. Part C — Sensitivity of the Conditional-Forecast Share, and an Honest Benchmark Forecast

### 5.1 Credibility filtering and the sensitivity curve

We define a multivariate credibility set on the variables selected in Part B,

$$\mathcal{C}_\tau = \{\, j : \text{MAE}_{j,v} \le \tau \ \ \forall\, v \in \mathcal{V}_{\text{selected}} \,\},$$

and report the **share** of net-zero pathways surviving the filter:

$$s(\tau) = \frac{|\mathcal{N} \cap \mathcal{C}_\tau|}{|\mathcal{C}_\tau|}.$$

This curve **is** the project's central figure. We label it the *sensitivity of the net-zero share to credibility filtering*, **not** "the revised probability" (§1): it is a sensitivity analysis over a set of conditional forecasts, and reporting it as a probability would repeat the category error the project exposes.

**The irreducible floor.** A 15-year backtest has limited power: a pathway that decarbonises *late* (after ~2030) tracks 2010–2025 just as well as a non-net-zero pathway, yet still reaches NZ2070. Such late movers are observationally indistinguishable from the historical record and **cannot be filtered out**. Hence $s(\tau)$ has a floor: it falls from the naive 32% toward, but not below, the late-mover share. Stating this floor is a result, not a footnote — it is the honest limit of what hindcasting can establish.

### 5.2 An empirically validated benchmark forecast (geometric random walk → diffusion)

To answer Q-A/Q-B for the observables that matter, we build our *own* probabilistic forecast — independent of the ensemble — and check that its intervals are calibrated against history (the "empirically validated probabilistic forecast" of Lafond's title).

**Baseline model — geometric random walk with drift.** Let $y_t = \ln(\cdot)$. Then $\Delta y_t = \mu + \varepsilon_t$, $\varepsilon_t \sim \mathcal{N}(0,\sigma^2)$. With a training window of $m$ growth rates, $\hat\mu = \tfrac1m\sum \Delta y_s$, and the central forecast is $\hat y_{t+\tau} = y_t + \hat\mu\tau$. The forecast-error variance (Farmer & Lafond 2016) is

$$\mathrm{Var}(\mathcal{E}_{t,\tau}) = \sigma^2\!\left(\tau + \frac{\tau^2}{m}\right),$$

giving the $1-\alpha$ predictive interval $y_t + \tau\hat\mu \pm z_{1-\alpha/2}\,\sigma\sqrt{\tau + \tau^2/m}$ (use $\hat\sigma$ and the $t_{m-1}$ distribution in practice). With positive autocorrelation $\rho$ in the noise, the variance scales by $(1+\rho)^2/(1+\rho^2)$ — intervals widen even when the median is unchanged.

**Diffusion correction for solar PV.** Early exponential-looking data can be the front of an S-shaped diffusion (Lafond, diffusion curves). A pure random-walk (Moore) extrapolation of solar PV therefore *overshoots* at long horizons. We fit instead a one-parameter **Bertalanffy–Richards** S-curve,

$$Y(t) = \frac{L}{\big[1 + \exp(-\beta k(t-t_0))\big]^{1/\beta}}, \qquad \beta = 1 \text{ recovers the logistic},$$

backtested by refitting the asymptote $\hat L$ on data up to several origins (e.g. 5/10/25/50% of $\hat L$) and forecasting forward, then scored by PIT/coverage. **Honest limitation:** the asymptote $L$ is unknown and dominates the long-horizon forecast — results are reported with explicit sensitivity to $\hat L$.

**Validation, not just a line.** The forecast is judged by calibration: do the predictive intervals cover the realised path at the nominal rate (PIT / coverage, proper scores such as CRPS), and how does the realised solar outcome sit relative to the *ensemble's* band? The expected finding — the empirical band contains reality while the IAM ensemble places it in its upper tail — is precisely the calibration failure of Q-A.

### 5.3 The policy-conditional view: Wright's law

Moore forecasts cost unconditionally from time; **Wright's law forecasts cost conditional on a deployment path**, which makes it the relevant tool for policy counterfactuals (Lafond). Each IAM pathway *is* a deployment path. Writing $X_t = \Delta\ln z_t$ (cumulative production) and $Y_t = \Delta\ln c_t$ (unit cost), the differenced model is $Y_t = \omega X_t + \eta_t$, and the cost forecast is conditional on future experience, $\hat y_{t+\tau} = y_t + \hat\omega\sum_{s\le\tau} X_{t+s}$. Applied to each scenario's solar deployment, this yields an implied cost trajectory; following Way, Ives, Mealy & Farmer (2022), faster deployment drives larger experience-curve cost declines, so pathways that assume an *expensive* transition can be inconsistent with their own deployment. **Caveat (Lafond):** Wright's law is hard to establish as superior to Moore's law (causality, multicollinearity, co-evolution of cost and production); it is presented as the policy-relevant lens, not as a proven point predictor.

## 6. Data Sources

| Variable | Source | Resolution |
|----------|--------|-----------|
| CO$_2$ emissions (fossil + industrial) | Global Carbon Budget 2025 (Friedlingstein et al.) | Annual, 2010–2025 |
| CO$_2$ emissions (cross-check) | IEA Global Energy Review 2025/2026 | Annual |
| Primary energy by fuel (coal, gas, oil) | Energy Institute Statistical Review 2025 | Annual, 2010–2024 |
| Solar PV and wind capacity | IRENA Renewable Capacity Statistics 2025/2026 | Annual, by country |
| Nuclear capacity | IAEA PRIS | Annual |
| SCI scenario ensemble | Scenario Compass Initiative v1.0, IIASA | 5-year steps, 2010–2100 |

Observed data are compiled in `observed_data_cleaned.xlsx`. A genuine long-horizon, out-of-sample test (e.g. AR5-vintage scenarios from ~2014 forecasting 2025) requires the external **IIASA AR5 Scenario Database**, as the SCI ensemble contains no pre-2017 (pre-AR6) pathways.

## References

- Farmer, J.D. & Lafond, F. (2016). How predictable is technological progress? *Research Policy*, 45(3), 647–665.
- Lafond, F., Bailey, A.G., Bakker, J.D., Rebois, D., Zadourian, R., McSharry, P. & Farmer, J.D. (2018). How well do experience curves predict technological progress? A method for making distributional forecasts. *Technological Forecasting and Social Change*, 128, 104–117.
- Lafond, F., Greenwald, D. & Farmer, J.D. (2022). Can stimulating demand drive costs down? World War II as a natural experiment. *Journal of Economic History*, 82(3).
- Way, R., Ives, M.C., Mealy, P. & Farmer, J.D. (2022). Empirically grounded technology forecasts and the energy transition. *Joule*, 6(9), 2057–2082.
- Wagenvoort, B., Dyer, J., Lafond, F. & Farmer, J.D. (in progress). Universality and predictability of technology diffusion.
- Friedlingstein, P. et al. (2026). Global Carbon Budget 2025. *Earth System Science Data*, 18.
- IEA (2026). *Global Energy Review 2026*. Paris: International Energy Agency.
- Energy Institute (2025). *Statistical Review of World Energy 2025*. London.
- Scenario Compass Initiative: https://scenariocompass.org
