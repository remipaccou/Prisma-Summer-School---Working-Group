# Narrative — detailed version

*Same eight steps as `narrative.md`, but with the forecasting concepts and notation made explicit
and explained. Not the short version — each claim is spelled out enough to follow the reasoning.*

## Framework & notation

We treat each scenario as a **forecast object** and evaluate it exactly the way one evaluates any
forecast: is it unbiased, is it calibrated, does it beat a trivial rule?

**Notation.**
- **y** — the *observed* value of a variable (CO₂, coal, solar, wind, nuclear, GDP) in a given year.
- **ŷ** — a scenario's *projection* of the same thing.
- **ε = y − ŷ** — the *forecast error*. With this sign convention, **positive ε = the scenario
  projected too little** (reality came in above it).
- **F** — the *predictive distribution*: the whole cloud of scenario values for a variable in a year.

**Four concepts the project rests on.**

1. **Conditional vs unconditional forecast.** A scenario is a *conditional* forecast: it says what
   emissions do *given* an assumed policy/technology path ("if this policy, then these emissions").
   An *unconditional* forecast is what will actually happen, full stop. These are different objects,
   and you **cannot turn a pile of conditional "if–then" statements into an unconditional
   probability** just by counting them.
2. **Forecast origin and horizon.** Every forecast is made at an *origin* (the year it was made) and
   looks out over a *horizon* τ (years ahead). Errors grow with horizon: for a random walk with an
   estimated trend, the error variance scales like **τ + τ²/m** (the τ² term is the compounding
   uncertainty in the estimated trend). Short-horizon accuracy says little about the long horizon.
3. **Calibration vs sharpness.** A forecast is *calibrated* if the observed value falls uniformly
   across its predictive distribution — i.e. reality lands near the middle of the cloud about as
   often as near the edges (the "PIT" is uniform). *Sharpness* is how *narrow* the cloud is. The two
   trade off: a narrow cloud that reality keeps falling outside of is **overconfident**, not good.
4. **Skill vs a naive benchmark.** A forecast only earns trust if it beats a trivial rule — a random
   walk ("nothing changes") or a straight-line trend. We measure it with the **skill ratio =
   |model error| / |naive error|**: above 1 means the trivial rule was closer, i.e. the forecast
   added no value.

---

## Research question

The SCI 2025 ensemble holds 1,564 model pathways; 497 of them reach net-zero CO₂ by 2070 — read
naively, a ~32% "chance" of net-zero.

**Top question:** *does the observed record of 2010–2025 tell us anything about reaching net-zero by
2070 — and is that naive 32% a meaningful number?*

This is not one flat question but a **cascade of nested ones** (which is exactly the A/B/C structure):

1. **Is the ensemble even a trustworthy forecast?** (Part A) — three sub-checks: is it *unbiased*
   (Steps 2–3), does it have *skill* against a naive rule (Step 4), is it *calibrated* (Step 5)?
2. **If we keep only the credible scenarios** — which variables define "credible", and how does the
   net-zero *share* move? (Parts B–C, Steps 6–7)
3. **What can a 15-year record structurally *not* settle** about a 45-year question? (Step 8)

The eight steps below open these drawers in order.

---

## Step 1 — The naive 32% is not a probability  ·  *conditional forecasts*

**Why counting does not give a probability.** Each pathway is a conditional forecast. So the 497
net-zero pathways are simply the 497 *assumed policy paths* that happen to end at zero — they
describe the **menu the modelling teams chose to run**, not the likelihood the real world follows.
Dividing 497 by 1,564 averages over that menu as if each path were an equally likely future. It is
not.

**And the number is not even stable.** "Net-zero by 2070" hides an arbitrary choice — the deadline
year. Move it, and far more (or far fewer) pathways qualify, because a later deadline lets slower
decarbonizers count too:

| Net-zero reached by | Pathways | Share |
|---|---|---|
| 2060 | 256 | 16% |
| 2070 | 497 | 31% |
| 2080 | 688 | 43% |
| any time (≤2100) | 909 | 57% |

The "probability" runs from **16% to 57%** just by sliding its own definition a decade. A quantity
that elastic cannot be a probability.

**So we change the question.** Instead of *revising a probability*, we test the ensemble *as a
forecast*: (i) is it calibrated and does it have skill? (ii) when we keep only the scenarios that
tracked reality, how does the net-zero *share* move?

---

## Step 2 — The hindcast: the ensemble undershoots 2025  ·  *the error series ε*

We line up the ensemble's CO₂ projection against reality at the four observed points. The full
ensemble (the fan of all pathways, with the four observed points) sets the scene:

![All SCI scenarios + observed CO₂](co2_overview.png)

The errors ε = y − ŷ (family-weighted ensemble mean):

| Year | y (observed) | ŷ (ensemble mean) | ε |
|---|---|---|---|
| 2010 | 33,400 | 32,995 | +405 |
| 2015 | 35,400 | 35,385 | +15 |
| 2020 | 34,800 | 36,372 | **−1,572** |
| 2025 | 38,100 | 35,518 | **+2,582** |

Through 2015 the ensemble is essentially perfect. Then two errors appear — and the key insight is
that **they come from completely different causes**:

- **2020 (−1,572, the models look too high) = COVID, not model failure.** The observed 34,800 is
  *artificially low*: lockdowns crashed emissions for one year. To judge the models fairly we should
  compare them to a *COVID-free* 2020 — estimate it by interpolating between 2015 and 2025
  (≈ 36,750). Against that counterfactual the error is no longer −1,572 but **≈ +378** — it changes
  sign and nearly vanishes. In other words the models were almost exactly right about the underlying
  2020 level; they simply could not foresee a pandemic. Roughly **three-quarters of the 2020 gap is
  the shock**, and it washes out by 2025.
- **2025 (+2,582, the models too low) = structural, and this one is real.** Here there is no dip to
  remove: by 2025 emissions had fully recovered. And 38,100 is almost exactly where a plain trend
  drawn through 2010–2015 would have landed (~39,400). So reality did *not* do anything surprising —
  it kept rising on trend. It is the **ensemble** that bent away: its median assumed emissions would
  peak around 2020 and then fall. That assumed turn never came. This is **structural optimism**, and
  the +2,582 is the load-bearing number of the whole study — it survives every way of removing COVID.

![Models vs reality, and the 2020 (COVID) / 2025 (structural) split](co2_finding1_simple.png)

---

## Step 3 — The net-zero scenarios are the most biased low  ·  *systematic bias in ε*

Now split the ensemble by outcome: **NZ2070** (the 497 reaching net-zero by 2070) vs **non-NZ**.
Comparing their **mean error (ME)** — a scenario's average error over the four years, family-weighted:

| Group | Mean error (ME) | Typical error (MAE) |
|---|---|---|
| **NZ2070** | **+650** (projected too little CO₂) | 2,147 (~6%) |
| **non-NZ** | **+216** (far less biased) | 1,649 (~5%) |

The net-zero pathways sit systematically *below* reality — as expected, since they assumed a faster
decarbonization than has occurred.

![Net-zero scenarios are biased low, not more imprecise](nz_bias.png)

Three points keep this honest:

- **It is a bias, not imprecision.** A *bias* is a systematic error always in the same direction
  (the average error is not zero); *imprecision* is large but scattered error that averages to ~zero.
  Look at the *typical* error size (MAE): the two groups are close, ~6% vs ~5% — they are not far
  apart in *how wrong* they are, they differ in *which direction* (NZ always too low). In forecasting
  terms the net-zero cloud is **mis-centred, not less sharp**. (This is also why we read ME, which
  measures direction, separately from MAE, which measures size.)
- **It is partly true by construction.** Reaching net-zero by 2070 *forces* a pathway to start
  bending emissions down early. Reality did not bend down, so an early-bending pathway *must*
  under-project 2025 — the bias is half a definition. Worse, a pathway that decarbonizes *late*
  (flat until ~2030, then a crash) looks identical to a non-NZ pathway over 2010–2025. The 15-year
  hindcast can only see the *early* movers.
- **It is robust.** The NZ–non-NZ gap holds whichever weighting we use (gap of +434 / +837 / +1,281
  under family / scenario / project weighting).

> So the defensible claim is narrow — and that is why it holds: *pathways premised on an early turn
> that has not begun are now the least consistent with what we observe.* (Not "net-zero models are
> wrong.")

---

## Step 4 — Skill: a trivial rule beats the ensemble  ·  *skill vs a random walk*

A forecast only deserves trust if it beats a dumb rule. The test: stand in **2015**, use *only* the
2010 and 2015 data, and predict 2025 — once with a trivial rule (hold the last value, or extend the
straight-line trend), once with the ensemble (its median). Then compare who landed closer.
**Skill ratio = |ensemble error| / |rule error|; above 1 means the rule won.** "% beaten" is the
share of *individual* scenarios the rule out-predicted.

| Variable | ensemble error | rule error | skill | % of scenarios beaten by the rule |
|---|---|---|---|---|
| **CO₂** | 7% | 3% | **2.0** | **81%** |
| **Coal** | 14% | 3% | **4.7** | **91%** |
| **Nuclear** | 16% | 2% | **9.9** | **95%** |
| **GDP** | 11% | 4% | **3.0** | **77%** |
| Solar PV | 51% | 75% | 0.7 | 6% |
| Wind | 17% | 30% | 0.6 | 34% |

![A trivial rule beats the ensemble on 4 of 6 variables](co2_benchmark.png)

On **four of six variables a two-point rule beats the entire IAM ensemble** — for nuclear, simply
assuming "nothing changes" beats 95% of the scenarios. The ensemble only wins on solar and wind, and
even there it is still ~50% wrong on PV: not "good on renewables", but "*everyone* misses PV, and the
straight line misses it even more" — which is precisely where a purpose-built method (a diffusion /
experience curve, below) is needed. *Caveat:* with a single target year, the robust statistic is
"% beaten", not the skill on one point. **The lesson:** an ensemble a ruler outperforms on most
variables has not shown forecasting skill, and any net-zero share read from it inherits that weakness.

---

## Step 5 — Calibration: reality sits in the tails  ·  *the PIT test*

Step 4 judged the *point* forecast (the median). But an ensemble is a *range* — maybe it is honest as
a distribution, giving a wide-enough cloud that reality lands somewhere reasonable inside it? We test
this with the **PIT**: for each variable, at what percentile of the scenario cloud does the observed
2025 value fall? If the ensemble were a calibrated forecast, reality would land near the middle (the
50th percentile) about half the time — scattered uniformly. If it keeps landing in the **tails**, the
cloud is both off-centre and too narrow.

| Variable | percentile of observed 2025 | reading |
|---|---|---|
| **GDP** | **1st** | ensemble far too high |
| Nuclear | 20th | too high |
| CO₂ | 75th | too low |
| Wind | 75th | too low |
| Coal | 79th | too low |
| **Solar PV** | **90th** | far too low |

![Reality falls in the tails of the cloud, not its centre](calibration_pit.png)

For all six variables reality lands in a tail, never the centre — for GDP it sits below *99%* of
scenarios. And calibration **gets worse with horizon**: CO₂ was near the middle in 2015 (52nd
percentile) but had drifted to the 75th by 2025. So the ensemble is **biased *and* overconfident** —
not a calibrated predictive distribution. This is the probabilistic restatement of Step 1: if reality
routinely sits at the 90th or 1st percentile of the cloud, that cloud is not a probability
distribution of futures, and no "P(net-zero)" can be read off it. Note that ordinary error metrics
(MAE) would miss this — only the *calibration* view reveals it.

---

## Step 6 — Part B: which observables carry the signal  ·  *informative variables*

To filter scenarios by credibility (Step 7) we first need to know *which variables actually tell
apart* a good pathway from a bad one. For each variable we compare the hindcast error of NZ vs non-NZ
scenarios with box plots. If the two groups separate cleanly, that variable is informative; if their
error distributions overlap, it is useless for filtering. We score the separation as **sep =
(median of NZ − median of non-NZ) / IQR** — how far apart the two medians are, in units of the spread.

| Variable | sep | carries signal? | direction |
|---|---|---|---|
| **Coal** | +0.46 | ✅ | NZ worse |
| **CO₂** | +0.39 | ✅ | NZ worse |
| **Solar** | −0.32 | ✅ | NZ better |
| Wind / Nuclear / GDP | ≈ 0 | ❌ | — |

![Coal, CO₂, solar separate the groups; wind/nuclear/GDP do not](partB1_boxplots.png)

Only three variables carry signal — **coal, CO₂, solar**. The other three separate nothing.
**And the signs disagree**: net-zero scenarios are *worse* on CO₂ and coal (they assumed a fall that
did not happen) but *better* on solar (they correctly expected the boom). That contradiction is the
"addition" signature seen at the level of credibility. An L1-penalized logistic regression (LASSO)
that tries to predict net-zero membership from the errors **independently picks the same three
variables, with the same signs** (`partB2_lasso`); PCA adds nothing. The practical conclusion: we
must **filter on coal + CO₂ + solar together** — filtering on CO₂ alone is a trap, because its GDP
and carbon-intensity errors partly cancel (the Kaya decomposition).

---

## Step 7 — Part C: filtering gives no number  ·  *the conditional-forecast trap*

The original plan was: keep the credible scenarios, recompute the net-zero share, report a corrected
figure. **There is no single corrected figure.** When we keep the most accurate scenarios over
2010–2025 and recompute the net-zero share, it moves in **opposite directions** depending on which
variable we judged accuracy on (the naive share is ≈ 34%):

| Keep the 25% most accurate on… | resulting net-zero share |
|---|---|
| **CO₂** | **~20%** ⬇️ |
| coal + CO₂ + solar (multivariate) | ~22% ⬇️ |
| **Solar** | **~48%** ⬆️ |

![The corrected net-zero share is not robust — it ranges 20–48%](partC_sensitivity.png)

So the "corrected" share is **anything between 20% and 48%**, on either side of the naive 34%. The
reason is exactly Step 6: net-zero pathways were *right* about the solar boom but *wrong* about
emissions, so filtering on what they got wrong (CO₂/coal) throws them out, while filtering on what
they got right (solar) keeps them. **This non-robustness is the empirical proof of Step 1**: you
cannot extract an unconditional probability from conditional forecasts, because the answer depends on
the conditioning variable you happen to choose. So we rename the object: not "the revised
probability", but **the *sensitivity* of the net-zero share**. The tension we started with has become
the result.

---

## Step 8 — The honest limit  ·  *origin × horizon*

Before concluding, the boundary of what this can show. We tested skill over a 15-year horizon; the
question is about a 45-year one — and error variance grows like **τ + τ²/m**, so a 45-year claim is
far less constrained than a 15-year one. Three things the recent record structurally *cannot* settle:

1. **Late decarbonizers are invisible.** A pathway that stays flat until ~2030 and only then crashes
   to net-zero looks identical to a non-NZ pathway over 2010–2025. The hindcast cannot separate them,
   so credibility filtering cannot push the net-zero share below the share of these late movers
   (~20%). That floor is genuine uncertainty the data cannot resolve, not a number we can sharpen.
2. **There is no true out-of-sample test here.** Every scenario in this ensemble is post-2017
   (AR6-era), so it was built already knowing part of the 2010–2025 history — this is a *hindcast*,
   not a real forecast. A genuine long-horizon test would need *older* scenarios: the AR5 vintage of
   ~2014, forecasting 2025 with no knowledge of it. This ensemble does not contain them (the IIASA
   AR5 database would).
3. **15 years is not 45 years.** Being accurate over a short horizon does not guarantee accuracy over
   a long one. The hindcast bounds what we can *claim*, not what will *happen*.

---

## How far this applies the forecasting method (honest map)

A frank accounting of which forecast-evaluation tools we actually used, versus framed or skipped:

| Method | Status | Where / why |
|---|---|---|
| Scenarios = conditional forecasts | ✅ applied | the central reframe — Steps 1 and 7 |
| Calibration & sharpness (PIT) | ✅ applied | Step 5 |
| Skill against a naive rule | ✅ applied | Step 4 |
| Random walk + error variance (τ + τ²/m) | 🟡 partial | framed in Step 8; used in the solar forecast |
| Forecast origin × horizon | 🟡 partial | vintage × horizon in cross-section, not a full rolling backtest |
| Wright's law (cost conditional on deployment) | ⬜ framed, not run | per-scenario cost vs experience curve |
| Bertalanffy–Richards diffusion curve | ⬜ diagnosed, not fitted | the honest solar forecast (`partC2`, the remaining piece) |
| Student-t pooling, surrogate datasets, formal error-growth test, MA(1), Bayesian posterior, CRPS / conformal intervals | ⬜ not done | these need long series with many observations; we have 15 years, 4 points per variable, all AR6 |

**Verdict.** The forecasting *framework* is the backbone of the whole project — treat scenarios as
conditional forecasts, test calibration, demand skill over a naive rule, build honest intervals. The
full *toolkit* is deliberately not applied: the data are too short and too compressed (everything is
post-2017) to support the heavy pooled machinery — which is exactly *why* we point to AR5 as the only
genuine long-horizon test. The one place the method is meant to run end-to-end is the solar forecast,
and doing that properly (a Bertalanffy–Richards diffusion curve, not a naive exponential) is the
remaining constructive piece.

## Where the argument stands

The 2025 world looks like the low-action pathways, not the net-zero ones; the pathways that promise
net-zero assumed a turn that has not started; the ensemble is biased low, overconfident on the
technologies that have moved fastest, and beaten by trivial rules on the variables it should find
easy. **None of this forecloses net-zero by 2070.** What it removes is the ground for treating
**32% as the *chance* of getting there**: the door to 2070 is not closed by the data — it is the
*probabilistic reading of the ensemble* that does not survive contact with the record.
