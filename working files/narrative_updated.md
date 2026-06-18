# Narrative 

## Framework & notation

We treat each scenario as a **forecast object** and evaluate it the way one evaluates any forecast.

**Notation.**
- $y_{v,t}$ — observed value of variable $v$ at time $t$ (CO₂, coal, solar, wind, nuclear, GDP).
- $\hat{y}_{j,v,t}$ — scenario $j$'s projection.
- $\varepsilon_{j,v,t} = y_{v,t} - \hat{y}_{j,v,t}$ — forecast error (**positive = the scenario aimed too low**).
- $F_{v,t}$ — the ensemble's empirical predictive distribution (the cloud of scenarios) for $v$ at $t$.

**Four Lafond concepts the whole project rests on.**

1. **Conditional vs unconditional forecast.** A scenario is a *conditional* forecast,
   $\hat{y}_j = f_j(P_j)$ — emissions *given* an assumed policy/technology path $P_j$. An
   *unconditional* forecast is $\mathbb{E}[y_t \mid \text{information}]$ — what will actually happen.
   **You cannot obtain the second by counting the first.**
2. **Forecast origin × horizon.** Each forecast has an origin $t_0$ (when it was made)
   and a horizon $\tau = t - t_0$. For a random walk with an estimated drift, error variance grows
   as $\sigma^2(\tau) \propto \tau + \tau^2/m$ — uncertainty compounds with horizon.
3. **Calibration & sharpness.** A forecast is *calibrated* if observations fall uniformly
   across its predictive distribution: the PIT $F_{v,t}(y_{v,t}) \sim \mathrm{Uniform}(0,1)$.
   *Sharpness* is how narrow the intervals are. A narrow interval that misses too often is
   **overconfident**.
4. **Skill vs a naive benchmark.** A forecast earns trust only by beating a trivial rule
   (random walk / linear trend). Skill ratio $= |\varepsilon_{\text{model}}| / |\varepsilon_{\text{naive}}|$;
   **$>1$ means the naive rule wins.**

---

## Research question

The SCI 2025 ensemble holds 1,564 pathways; 497 reach net-zero CO₂ by 2070 — read naively, a ~32%
"chance". **Is that 32% meaningful — and what happens to it once we confront the scenarios with the
observed record 2010–2025?**

## Step 1 — The naive 32% is not a probability  ·  

**Conceptual.** Counting how many conditional forecasts $\hat{y}_j = f_j(P_j)$ end in net-zero
measures the *menu of assumed policy paths* $\{P_j\}$ the modelling teams chose to run — not
$\mathbb{P}(\text{net-zero})$. The 497/1564 mixes "if–then" statements as if they were "then".

**Empirical.** The count is not even stable — "net-zero by 2070" hides an arbitrary deadline:

| Net-zero reached by | Pathways | Share |
|---|---|---|
| 2060 | 256 | 16% |
| 2070 | 497 | 31% |
| 2080 | 688 | 43% |
| any time (≤2100) | 909 | 57% |

A number that doubles when you slide its own definition by a decade is not a probability.

**Pivot.** We stop revising a probability and instead test the ensemble *as a forecast*:
(i) is it calibrated and skilful? (ii) how does conditioning on accuracy move the net-zero *share*?

---

## Step 2 — The hindcast: the ensemble undershoots 2025  ·  *[Lafond: error series $\varepsilon_{j,t}$]*

Error $\varepsilon = y - \hat{y}$ on CO₂ at the 4 points 2010→2025. Full ensemble (context):

![All SCI scenarios + observed CO₂](co2_overview.png)

| Year | $y$ (obs) | $\hat{y}$ (mean) | $\varepsilon$ |
|---|---|---|---|
| 2010 | 33,400 | 32,995 | +405 |
| 2015 | 35,400 | 35,385 | +15 |
| 2020 | 34,800 | 36,372 | **−1,572** |
| 2025 | 38,100 | 35,518 | **+2,582** |

Two late errors, two stories:
- **2020 = COVID.** Remove the dip and $\varepsilon$ flips to ≈ +378 — ~75% of the gap is the shock,
  not the model.
- **2025 = structural.** No shock to remove; 38,100 sits on the pre-COVID trend (~39,400). The
  ensemble assumed a peak-and-decline that never came. **Structural optimism** ($\varepsilon = +2{,}582$,
  the load-bearing number).

![Finding 1 — models vs reality, 2020/2025 decomposition](co2_finding1_simple.png)

---

## Step 3 — The net-zero scenarios are the most biased low  ·  *[Lafond: systematic bias in $\varepsilon$]*

Split by net-zero status. Mean error $\mathrm{ME}_j = \frac{1}{|T|}\sum_t \varepsilon_{j,t}$
(family-weighted):

| Group | ME | MAE |
|---|---|---|
| **NZ2070** | **+650** | 2,147 (~6%) |
| **non-NZ** | **+216** | 1,649 (~5%) |

![Step 3 — NZ scenarios biased low, not more imprecise](nz_bias.png)

- **Bias, not imprecision** — the *magnitudes* (MAE) are close; the *sign* differs. In Lafond's
  terms the NZ sub-ensemble is *miscentred*, not *less sharp*.
- **Partly tautological** — reaching net-zero by 2070 *forces* an early downturn; a late
  decarbonizer is indistinguishable from non-NZ over 2010–2025 (a **horizon** limit, slide 11).
- **Robust** to weighting (gap +434 / +837 / +1,281 under family / scenario / project).

> Defensible claim: *pathways premised on an early turn — which has not begun — are now the least
> consistent with observation.*

---

## Step 4 — Skill: a trivial rule beats the ensemble  ·  *[Lafond: skill vs random walk, slide 2]*

From origin 2015 ($\tau$ = 10 yr), predict 2025 with a naive rule (random walk / linear trend) vs
the ensemble. Skill ratio $= |\varepsilon_{\text{ens}}|/|\varepsilon_{\text{naive}}|$; $>1$ = rule wins.

| Variable | $|\varepsilon_{\text{ens}}|$ | $|\varepsilon_{\text{naive}}|$ | skill | % scenarios beaten |
|---|---|---|---|---|
| **CO₂** | 7% | 3% | **2.0** | **81%** |
| **Coal** | 14% | 3% | **4.7** | **91%** |
| **Nuclear** | 16% | 2% | **9.9** | **95%** |
| **GDP** | 11% | 4% | **3.0** | **77%** |
| Solar PV | 51% | 75% | 0.7 | 6% |
| Wind | 17% | 30% | 0.6 | 34% |

![Step 4 — a trivial rule beats the ensemble on 4 of 6 variables](co2_benchmark.png)

On **4 of 6 variables a 2-point rule beats the ensemble**. It wins only on solar/wind — and is
still ~50% off on PV, *exactly* where a dedicated diffusion/experience-curve method is needed.
*Caveat*: one target year → "% beaten" is the robust statistic, not the skill on a single point.
**No skill against the naive benchmark ⇒ the implied net-zero share inherits that weakness.**

---

## Step 5 — Calibration: reality sits in the tails  ·  *[Lafond: PIT / calibration, slide 5]*

PIT test: where does $y_{v,2025}$ fall in the ensemble distribution $F_{v,2025}$? Calibrated ⇒
percentiles $\sim \mathrm{Uniform}$, i.e. reality near the median ~half the time.

| Variable | PIT (percentile of $y_{2025}$) | Reading |
|---|---|---|
| **GDP** | **1st** | far too high |
| Nuclear | 20th | too high |
| CO₂ | 75th | too low |
| Wind | 75th | too low |
| Coal | 79th | too low |
| **Solar PV** | **90th** | far too low |

![Step 5 — reality falls in the tails, not the centre](calibration_pit.png)

Reality lands in the **tails for all six** (GDP below 99% of scenarios), and calibration **degrades
with horizon** (CO₂: 52nd in 2015 → 75th in 2025). The ensemble is **biased *and* overconfident** —
not a calibrated predictive distribution. This is the probabilistic proof of Step 1: no
$\mathbb{P}(\text{net-zero})$ can be read from $F$. *Calibration, not MAE, is what reveals it.*

---

## Step 6 — Part B: which observables carry the signal  ·  *[Lafond: informative variables]*

Box plots of $\varepsilon$ per variable, NZ vs non-NZ. Separation
$\mathrm{sep} = (\text{med}_{NZ} - \text{med}_{\neg NZ})/\mathrm{IQR}$:

| Variable | sep | Carries signal? | Direction |
|---|---|---|---|
| **Coal** | +0.46 | ✅ | NZ worse |
| **CO₂** | +0.39 | ✅ | NZ worse |
| **Solar** | −0.32 | ✅ | NZ better |
| Wind / Nuclear / GDP | ≈0 | ❌ | — |

![Step 6 — coal, CO₂, solar discriminate](partB1_boxplots.png)

**The signs disagree**: NZ scenarios are *worse* on CO₂/coal but *better* on solar — the "addition"
signature at the credibility level. An L1-LASSO predicting NZ membership from the errors selects the
**same three variables with the same signs** (`partB2_lasso`); PCA adds nothing. → **filter
multivariate (coal+CO₂+solar)**; CO₂ alone is a trap (Kaya: GDP/intensity errors cancel).

---

## Step 7 — Part C: filtering gives no number  ·  *[Lafond: the conditional-forecast trap, slide 3]*

Keep the most accurate scenarios; recompute the net-zero share. It moves in **opposite directions**
by credibility variable (naive ≈ 34%):

| Keep 25% most accurate on… | Net-zero share |
|---|---|
| **CO₂** | **~20%** ⬇️ |
| multivariate | ~22% ⬇️ |
| **Solar** | **~48%** ⬆️ |

![Step 7 — the corrected net-zero share is not robust](partC_sensitivity.png)

The "corrected" share is anything in **20–48%**. NZ scenarios were right on solar, wrong on
CO₂/coal — so the answer depends on the *conditioning variable* you choose. **This non-robustness is
the empirical proof of slide 3**: you cannot extract an unconditional probability from conditional
forecasts. We relabel the object: *the **sensitivity** of the net-zero share*, not a probability.

---

## Step 8 — The honest limit  ·  *[Lafond: origin × horizon, slide 11]*

We tested skill over $\tau$ = 15 yr; the question is $\tau$ = 45 yr, and error variance grows as
$\tau + \tau^2/m$.

1. **Late decarbonizers are invisible** — flat until ~2030 then crashing to net-zero looks like
   non-NZ over 2010–2025, so filtering cannot push the share below the late-mover floor (~20%).
2. **No true out-of-sample test** — every scenario is post-2017 (AR6); a genuine long-horizon test
   needs the AR5 vintage (~2014 forecasting 2025), absent here (IIASA AR5 database would supply it).
3. **15 ≠ 45 years** — short-horizon skill does not transfer; the hindcast bounds the *claim*, not
   the *outcome*.

---

## How far this applies Lafond's method (honest map)

| Lafond method | Status | Where |
|---|---|---|
| Scenarios = conditional forecasts (sl. 3) | ✅ applied | the central reframe — Steps 1, 7 |
| Calibration & sharpness / PIT (sl. 5) | ✅ applied | Step 5 |
| Skill vs a naive rule (sl. 2) | ✅ applied | Step 4 |
| Random walk + error variance $\sigma^2(\tau+\tau^2/m)$ (sl. 6–8) | 🟡 partial | framed in Step 8; used in the solar forecast |
| Forecast origin × horizon (sl. 11) | 🟡 partial | vintage × horizon, in cross-section not a full rolling backtest |
| Wright's law — cost conditional on deployment (sl. 20–25) | ⬜ framed, not run | per-scenario cost vs experience curve |
| Bertalanffy–Richards diffusion curve (sl. 26–29) | ⬜ diagnosed, not fitted | the honest solar forecast (`partC2`, next) |
| Student-t pooling, surrogate datasets, $\Xi(\tau)$ test, MA(1), Bayesian posterior, CRPS/conformal (sl. 9–18, 30) | ⬜ not done | **need long, many-point series; we have 15 yr / 4 points / all-AR6** |

**Verdict.** Lafond's *framework* is the project's backbone — conditional forecasts, calibration,
skill against a naive rule, honest intervals. His full *toolkit* is not applied, and deliberately so:
the data are too short and too compressed (all post-2017) to carry the pooled machinery — which is
*why* we point to AR5 as the only genuine long test. The one place his exact formula is meant to run
is the solar forecast; doing it properly (Bertalanffy–Richards, not Moore) is the remaining piece.

## Where the argument stands

The 2025 world resembles the low-action pathways; the net-zero pathways assumed a turn that has not
started; the ensemble is biased low, overconfident on the fastest-moving technologies, and beaten by
trivial rules on the variables it should find easy. **None of this forecloses net-zero by 2070** — it
removes the ground for treating **32% as the *chance* of getting there.** The door to 2070 is not
closed by data; it is the *probabilistic reading of the ensemble* that does not survive.
