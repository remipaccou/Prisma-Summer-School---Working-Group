# Hindcast Evaluation of IAM Scenario Ensembles: Method

## 1. Context and Research Question

The Scenario Compass Initiative (SCI 2025) assembles 1,564 integrated assessment model pathways from 65 models. Of these, 497 reach global net zero CO$_2$ emissions by 2070.

A naive reading of the ensemble would suggest $P(\text{NZ2070}) = 497/1564 \approx 32\%$. But this treats all scenarios as equally credible. Some of these models were built years ago; some have been calibrated on outdated assumptions; some have already been contradicted by observed data over 2010–2025. The question is: **does correcting for historical accuracy change the probability of reaching net zero by 2070?**

To answer this, we need a method to evaluate scenario credibility against observed data, identify which variables carry the most information about credibility, and revise the probability accordingly.

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

## 3. Part A — Hindcast Error Analysis

### 3.1 Rationale

The SCI scenarios project the evolution of CO$_2$ emissions, energy supply, and technology deployment from 2010 to 2100. For the period 2010–2025, observed data is available from the Global Carbon Budget, IEA, and the Energy Institute Statistical Review. By comparing each scenario's projection to the observed trajectory, we measure how well it anticipated what actually happened. Scenarios that failed to track reality over the recent past have weaker grounds for credibility regarding their future projections.

### 3.2 Error computation

For each scenario $j$, variable $v$, and year $t \in T$:

$$\varepsilon_{j,v,t} = y_{v,t} - \hat{y}_{j,v,t}$$

A positive $\varepsilon$ means the scenario underestimated the observed value (projected less CO$_2$ or less coal than actually occurred). A negative $\varepsilon$ means it overestimated.

We compute three summary metrics, each capturing a different aspect of forecast quality:

**Mean Error (ME)** — systematic bias. The sign indicates whether the ensemble collectively over- or underestimates:

$$\text{ME}_{v,t} = \frac{1}{J} \sum_{j=1}^{J} \varepsilon_{j,v,t} \qquad \text{(averaged over scenarios, one value per year)}$$

$$\text{ME}_{j,v} = \frac{1}{|T|} \sum_{t \in T} \varepsilon_{j,v,t} \qquad \text{(averaged over time, one value per scenario)}$$

$$\overline{\text{ME}}_v = \frac{1}{J \cdot |T|} \sum_{j} \sum_{t} \varepsilon_{j,v,t} \qquad \text{(averaged over both)}$$

**Mean Absolute Error (MAE)** — typical error magnitude, regardless of sign:

$$\text{MAE}_{j,v} = \frac{1}{|T|} \sum_{t \in T} |\varepsilon_{j,v,t}|$$

**Root Mean Square Error (RMSE)** — penalises large deviations more heavily than MAE:

$$\text{RMSE}_{j,v} = \sqrt{\frac{1}{|T|} \sum_{t \in T} \varepsilon_{j,v,t}^2}$$

### 3.3 Why these three metrics

ME alone can be misleading: a scenario that overestimates by 5,000 in 2020 and underestimates by 5,000 in 2025 has ME $\approx$ 0 but is clearly inaccurate. MAE captures total error magnitude. RMSE further penalises scenarios with occasional large misses, distinguishing a scenario that is consistently off by 1,000 from one that is perfect three times and off by 4,000 once (same MAE, very different RMSE).

### 3.4 Error diagnostics

Beyond aggregate metrics, we examine the structure of errors.

**Autocorrelation** — Do scenarios that err at one time point also err at others?

$$\rho_v(t_0, t_1) = \text{Corr}\left(\varepsilon_{j,v,t_0},\; \varepsilon_{j,v,t_1}\right) \quad \text{across } j$$

High autocorrelation indicates a structural model bias (the model is calibrated wrong from the start), as opposed to a random error (the model got the trend right but missed a specific event like COVID). This matters because structural biases are likely to persist into the future, while random errors may not.

**Cross-variable correlation** — Do scenarios that overestimate coal also underestimate renewables?

$$\rho(v_1, v_2) = \text{Corr}\left(\varepsilon_{j,v_1,t},\; \varepsilon_{j,v_2,t}\right) \quad \text{across } j$$

If errors are correlated across variables, it reveals a coherent worldview embedded in the model: some models are systematically "fossil-heavy" while others are systematically "green". This means filtering on a single variable may suffice, or conversely, that filtering on one variable without checking others could be misleading if compensating biases exist.

**Error vs. NZ2070 status** — Do NZ scenarios have systematically larger errors?

$$|\varepsilon_{j,v,t}| = \alpha + \beta \cdot \mathbb{1}[j \in \mathcal{N}] + u_j$$

If $\beta > 0$, NZ scenarios are less accurate historically. This is the central test: it directly links historical credibility to the outcome we care about.

## 4. Part B — Variable Selection

### 4.1 Rationale

The SCI dataset contains over 2,000 variables per scenario. Not all are equally relevant for assessing credibility. We need to identify which variables carry the most information about whether a scenario tracks reality. This serves two purposes: (i) it tells us what to monitor in the real world to assess whether we are on a NZ-compatible path, and (ii) it determines which variables to use for filtering in Part C.

### 4.2 Box-plot comparison (non-parametric approach)

We split scenarios into two groups based on historical accuracy: "accurate" (MAE below a threshold $\tau$) and "inaccurate" (MAE above $\tau$). For each variable in the SCI at year 2025 or 2030, we compare the distribution across the two groups using side-by-side box plots.

Variables where the two distributions are clearly separated are informative: knowing their value tells you whether the scenario is historically credible. Variables where the distributions overlap are uninformative.

This is a simplified, visual version of forecast encompassing: instead of regressing errors on projections, we directly compare distributions. It requires no modeling assumptions and produces immediately interpretable figures.

### 4.3 LASSO regression (regularised variable selection)

To formalise the box-plot approach, we regress absolute error on all available scenario variables simultaneously, with L1 regularisation:

$$\min_\beta \sum_{j=1}^{J} \left( |\varepsilon_{j,v,t}| - \beta_0 - \sum_{k=1}^{K} \beta_k \hat{y}_{j,v_k,t} \right)^2 + \lambda \sum_{k=1}^{K} |\beta_k|$$

The $\lambda$ penalty shrinks most coefficients to exactly zero. The variables that survive with $\beta_k \neq 0$ are the ones that best predict forecast error. This is useful because:

- It handles collinearity: when coal and CO$_2$ are highly correlated, LASSO picks the more informative one rather than splitting the signal.
- It is automatic: no need to pre-select candidate variables.
- The output is a short list of variables ranked by importance.

### 4.4 Dimensionality reduction (PCA/SVD)

An alternative to selecting individual variables is to compress the variable space. Using singular value decomposition:

$$Y = U \Sigma V'$$

where $Y$ is the $J \times K$ matrix of scenario projections (scenarios as rows, variables as columns), $U$ captures scenario patterns, $\Sigma$ captures variance, and $V'$ captures variable loadings. The first few principal components often explain most of the variance. We then test which components correlate with historical accuracy.

This is useful when the question is not "which specific variable matters" but "what underlying dimension of variation matters" — for instance, a component that loads on coal, gas, and CO$_2$ simultaneously might represent a "fossil intensity" dimension.

## 5. Part C — Filtering, Forecasting, and Revised Probability

### 5.1 Scenario filtering

Based on Parts A and B, we define a credibility criterion. We retain scenarios whose MAE on selected variables falls below a threshold $\tau$:

$$\mathcal{C}_\tau = \left\{ j : \text{MAE}_{j,v} \leq \tau \quad \forall\, v \in \mathcal{V}_{\text{selected}} \right\}$$

where $\mathcal{V}_{\text{selected}}$ is the set of variables identified in Part B.

The revised probability of NZ2070 is:

$$P(\text{NZ2070} \mid \text{credible}) = \frac{|\mathcal{N} \cap \mathcal{C}_\tau|}{|\mathcal{C}_\tau|}$$

We vary $\tau$ and plot $P(\text{NZ2070} \mid \mathcal{C}_\tau)$ as a function of $\tau$ to assess robustness. If the revised probability is stable across a range of thresholds, the result is robust; if it is highly sensitive to $\tau$, the result depends on the filtering choice.

### 5.2 Application to Solar PV: logistic growth and Wright's law

As a focal case, we apply a simple forecasting model to solar PV deployment, connecting the hindcast evaluation to a forward-looking probabilistic forecast.

**Logistic growth model** for PV deployment:

$$y(t) = \frac{L}{1 + \exp\left(-k(t - t_0)\right)}$$

where $L$ is the saturation level (maximum installed capacity), $k$ is the growth rate, and $t_0$ is the inflection point. In the early phase ($t \ll t_0$), this reduces to exponential growth: $y(t) \approx \exp(kt)$. In log space: $\ln y \approx kt + \text{const}$, so $k$ can be estimated by linear regression on observed log-capacity over 2010–2025.

**Wright's law** for PV cost:

$$\Delta \ln c = \omega \cdot \Delta \ln z + \varepsilon$$

where $c$ is unit cost, $z$ is cumulative production, and $\omega$ is the learning rate. For solar PV, the empirical estimate is $\omega \approx -0.32$ (roughly 20% cost reduction per doubling of cumulative production). Given a logistic trajectory for deployment, cumulative production $z(t)$ is determined, and Wright's law gives a probabilistic forecast for future cost: $\hat{c}_{t+\tau} = z_{t+\tau}^{\omega}$.

**Connection to ensemble evaluation:** we compare each SCI scenario's PV trajectory against the fitted logistic + Wright model. Scenarios whose PV projections are consistent with the empirically calibrated model inherit credibility from the observed learning curve. We test whether these scenarios are the same ones that score well on the hindcast evaluation (Part A), providing an independent validation.

## 6. Data Sources

| Variable | Source | Resolution |
|----------|--------|-----------|
| CO$_2$ emissions (fossil + industrial) | Global Carbon Budget 2025 (Friedlingstein et al.) | Annual, 2010–2025 |
| CO$_2$ emissions (cross-check) | IEA Global Energy Review 2025/2026 | Annual |
| Primary energy by fuel (coal, gas, oil) | Energy Institute Statistical Review 2025 | Annual, 2010–2024 |
| Solar PV and wind capacity | IRENA Renewable Capacity Statistics 2025 | Annual, by country |
| Nuclear capacity | IAEA PRIS | Annual |
| SCI scenario ensemble | Scenario Compass Initiative v1.0, IIASA | 5-year steps, 2010–2100 |

All observed data is compiled in `observed_data_cleaned.xlsx`.

## References

- Friedlingstein, P. et al. (2026). Global Carbon Budget 2025. *Earth System Science Data*, 18.
- IEA (2026). *Global Energy Review 2026*. Paris: International Energy Agency.
- Energy Institute (2025). *Statistical Review of World Energy 2025*. London.
- Farmer, J.D. & Lafond, F. (2016). How predictable is technological progress? *Research Policy*, 45(3), 647–665.
- Scenario Compass Initiative: https://scenariocompass.org
