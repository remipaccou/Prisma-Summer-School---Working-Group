# Reaching net-zero CO₂ by 2070: what the scenario ensemble can and cannot tell us

*Output of work. Three parts — the question, the diagnosis (hindcast), and what can still be forecast.
Factual and explicit throughout (notation, metrics, and forecasting concepts spelled out), not a story.*

## Framework & notation

Each scenario is treated as a **forecast object** and evaluated as a forecast: unbiased? calibrated?
better than a trivial rule?

- **y** — observed value of a variable (CO₂, coal, solar, wind, nuclear, GDP) in a given year.
- **ŷ** — a scenario's projection of the same thing.
- **ε = y − ŷ** — forecast error. Positive ε ⇒ the scenario projected too little.
- **F** — the predictive distribution: the cloud of scenario values for a variable in a year.

Four concepts the project rests on:

1. **Conditional vs unconditional forecast.** A scenario gives ŷ = f(P): the outcome *given* an
   assumed policy/technology path P. An unconditional forecast is the outcome marginally — a
   probability. One cannot obtain the second by counting the first.
2. **Origin × horizon.** A forecast made at origin t₀ looks out over horizon τ. For a random walk
   with estimated drift, error variance grows as **σ²·(τ + τ²/m)** — long horizons are far less
   constrained than short ones.
3. **Calibration vs sharpness.** Calibrated ⇒ the PIT (the percentile at which y falls in F) is
   uniform: reality near the median about half the time. Sharpness = interval width. A narrow
   interval reality keeps falling outside is overconfident.
4. **Skill vs a naive benchmark.** skill = |ε(model)| / |ε(naive rule)|; skill > 1 ⇒ the naive rule
   wins, i.e. the forecast adds nothing.

---

## Part 1 — The question

**Research question.** The SCI 2025 ensemble holds 1,564 pathways; 497 reach net-zero CO₂ by 2070, so
a naive P(NZ2070) = 497/1564 ≈ 32%. *Does the 2010–2025 record make that 32% meaningful?* This is a
cascade of nested questions (the A/B/C structure):

1. Is the ensemble a trustworthy forecast — unbiased, skilful, calibrated?
2. If we keep only credible scenarios, which variables define "credible", and how does the net-zero
   *share* move?
3. What can a 15-year record structurally not settle about a 45-year question?

**Method (Part 1):** a framing argument (conditional vs unconditional forecast) plus a
sensitivity check on the two arbitrary degrees of freedom hidden in the count.

**Why the 32% is not a probability — three points.**

*(1) What the number actually is.* We compute P̂(NZ2070) = (1/J)·Σⱼ 1[scenario j reaches net-zero] —
the **frequency of net-zero pathways in this sample**. For a sample frequency to estimate a real
probability the sample must be (i) representative of what is being estimated and (ii) made of roughly
independent draws. The SCI ensemble is neither: it is a **convenience sample** — 63 models, the top
three contributing 28% of all runs, with heavily correlated scenarios (same models, reused
assumptions). The frequency therefore measures the *research agenda of the modelling teams*, not the
likelihood of the world.

*(2) It moves with the deadline (degree of freedom #1).* "Net-zero by 2070" hides a chosen cutoff:

| Reach net-zero by | 2060 | 2070 | 2080 | ≤2100 (ever) |
|---|---|---|---|---|
| Share | 16% | 31% | 43% | 57% |

*(3) It moves with the composition (degree of freedom #2).* The frequency also depends on how many
runs each team submitted. Re-weighting so each modelling **family**, or each **project**, counts once:

| Weighting | by scenario count | one vote / family | one vote / project |
|---|---|---|---|
| NZ2070 share | 31% | 24% | 39% |

Two choices that have nothing to do with the climate — the deadline and the weighting — each move the
number by roughly half (16–57%, 24–39%). A quantity that elastic is not a probability. Conceptually
this is inevitable: each pathway is a *conditional* forecast ŷ = f(P) (emissions *given* an assumed
policy path P), not a draw from the distribution of futures, and counting conditional "if–then"
statements cannot produce an unconditional probability. So we stop trying to revise a number and
instead test the ensemble *as a forecast* (Part 2), reporting a sensitivity, not a probability.

---

## Part 2 — Diagnosis: is the ensemble a usable forecast?

*Research question: is the ensemble unbiased, skilful, and calibrated — and which variables carry
credibility signal? **Method: a hindcast (backtest).** Each scenario's projection is scored against
the observed 2010–2025 record (error ε = y − ŷ), then summarised by bias/accuracy metrics (§2.1–2.2),
skill against a naive rule (§2.3), PIT calibration (§2.4), box-plot/LASSO variable selection (§2.5),
and credibility filtering (§2.6).*

**2.1 — Error series; the 2025 undershoot is structural.** The full ensemble (all 1,591 pathways
2010–2100, with the four observed points) and a zoom on the hindcast window:

![Full SCI ensemble and the observed CO₂ points](figures/co2_overview.png)

ε = y − ŷ on CO₂ (family-weighted mean):

| Year | y | ŷ | ε |
|---|---|---|---|
| 2010 | 33,400 | 32,995 | +405 |
| 2015 | 35,400 | 35,385 | +15 |
| 2020 | 34,800 | 36,372 | **−1,572** |
| 2025 | 38,100 | 35,518 | **+2,582** |

The 2020 error is COVID: replacing the dipped 34,800 by a COVID-free interpolation (≈36,750) flips ε
to ≈ +378, so ~75% of the 2020 gap is the shock. The 2025 error is structural: 38,100 lies on the
pre-COVID trend (~39,400 extrapolated), so reality did not deviate — the ensemble did, by assuming a
peak-and-decline. The +2,582 survives every detrending.

![COVID (2020) vs structural (2025)](figures/co2_finding1_simple.png)

**2.2 — Bias by outcome.** Mean error ME = mean over years of ε, family-weighted: NZ2070 **+650** vs
non-NZ **+216**. (The non-NZ *level* is weighting-dependent — near 0 under scenario weighting — so we
read the **gap**, robust at +434/+837/+1,281 under family/scenario/project weighting.) The typical
magnitudes (MAE ≈ 6% vs 5%) are close: this is a **bias** (systematic direction), not imprecision.
It is also partly definitional — reaching net-zero by 2070 forces an early downturn, so such pathways
must under-project a reality that did not turn.

![NZ scenarios biased low, not more imprecise](figures/nz_bias.png)

**2.3 — Skill vs a naive rule (a corollary, not an independent test).** Forecasting 2025 from 2010–
2015 with a random walk or linear trend:

| Variable | skill = \|ε_ens\|/\|ε_rule\| | % scenarios beaten |
|---|---|---|
| CO₂ | 2.0 | 81% |
| Coal | 4.7 | 91% |
| Nuclear | 9.9 | 95% |
| GDP | 3.0 | 77% |
| Solar PV | 0.7 | 6% |
| Wind | 0.6 | 34% |

The rule wins on 4/6. But this is **the same fact as §2.1–2.2**, not an independent leg: the rule
wins on CO₂/coal/GDP precisely because reality stayed on trend while the ensemble bet on a turn. And
nuclear's skill 9.9 is **hollow** — nuclear is flat (375→377 GW), so "nothing changes" wins by
construction. Honest statement: on the on-trend variables the ensemble shows no skill against a ruler.

![A trivial rule beats the ensemble on the on-trend variables](figures/co2_benchmark.png)

**2.4 — Calibration (a diagnostic, not a formal test).** Percentile of observed 2025 in F:

| GDP | Nuclear | CO₂ | Wind | Coal | Solar PV |
|---|---|---|---|---|---|
| 1st | 20th | 75th | 75th | 79th | 90th |

Reality is **systematically on the low-emissions side**. We do not overstate it: 75th–79th is the
upper-middle, **not a tail** — only GDP (1st) and solar (90th) are true tails. And with **one point
per variable** this is a suggestive diagnostic of low bias, not a formal PIT test (which needs many
origins × targets). "Overconfident" is firm only for solar and GDP. What is solid is the *direction*:
reality off-centre low ⇒ F is not a clean distribution to read P(NZ2070) from.

![Reality on the low-emissions side of the cloud](figures/calibration_pit.png)

**2.5 — Variable selection (Part B).** Separation score sep = (median_NZ − median_non-NZ)/IQR per
variable: **Coal +0.46, CO₂ +0.39, Solar −0.32** discriminate; Wind, Nuclear, GDP ≈ 0 do not. The
three informative variables **disagree in sign**: NZ worse on coal/CO₂, better on solar (the addition
signature). An L1-LASSO predicting NZ from the errors selects the same three with the same signs.
Consequence: filter on coal+CO₂+solar jointly — CO₂ alone is a trap (its GDP/intensity errors cancel).

![Coal, CO₂, solar carry the signal — and disagree](figures/partB1_boxplots.png)

**2.6 — Filtering (Part C): ~20%, not "anything".** Keeping the 25% most accurate and recomputing the
net-zero share: **CO₂ → 20%, multivariate → 22%, solar-only → 48%** (naive 34%). So the corrected
share is **~20% under any reasonable filter**; it rises to 48% only under solar-only filtering, a poor
criterion since solar is the variable everyone misses. The robust result is the *directional*
dependence on the conditioning variable — the empirical proof of Part 1 (no single unconditional
probability exists). We label this object the **sensitivity of the net-zero share**, not a revised
probability.

![Net-zero share ~20% under sensible filters](figures/partC_sensitivity.png)

---

## Part 3 — What can still be forecast

*Research question: if the ensemble is unreliable, what can we forecast honestly — and where is the
real constraint on net-zero? **Method:** forecast-horizon limits (§3.1), an independent
experience-curve forecast (Wright's law) for technology cost (§3.2), reconciled through the
addition/substitution structure (§3.3).*

**3.1 — The structural limit.** A 15-year backtest cannot settle a 45-year question (error variance
∝ τ + τ²/m). A pathway flat until ~2030 then crashing to net-zero is indistinguishable from non-NZ
over 2010–2025, so filtering cannot go below the late-mover share (~20% as a practical floor;
unidentifiable by construction). And every scenario is post-2017, so this is a hindcast, not a true
out-of-sample test — the AR5 vintage (~2014 forecasting 2025) would provide one but is absent here.

**3.2 — The one quantity with skill: cost (Wright's law).** Solar PV cost fell ~2,440 → ~250 USD/kW
(2010→2024); a log-log experience-curve fit (learning rate ≈ 0.39, i.e. cost falls ~39% per doubling
of capacity) projects ~38 USD/kW by 2070 for net-zero pathways and ~43 for non-net-zero ones. The two
projections are nearly identical — clean tech becomes cheap whether or not the world reaches net-zero.

![PV cost (Wright): collapse, and NZ ≈ non-NZ](figures/pv_wright_cost_projection_to_2070_log.png)

The shaded band is a **±2 s.e. (≈95%) learning-rate uncertainty**, propagated from the standard error
of the fitted exponent through the projection. Even at its edges the net-zero and non-net-zero bands
overlap, so the "NZ ≈ non-NZ" reading is robust to learning-rate uncertainty. *Two caveats we hold
ourselves to:* the band reflects only the learning-rate fit (estimated on few overlapping points), not
trajectory or model uncertainty; and Wright's law is hard to prove strictly superior to a time-trend,
so this is the policy-relevant lens, not a proven point forecast.

**3.3 — Reconciliation: the lock is substitution, not cost.** Part 2 (ensemble too optimistic) and
§3.2 (clean tech cheaper than assumed) only seem to conflict. The world does two things at once:
deploys renewables faster than any model (costs fall faster — §3.2) *and* keeps the fossils
(emissions rise — Part 2). So the constraint on net-zero is **not the cost of clean technology** —
that is outperforming the scenarios — it is **substitution**: clean is added without removing dirty.
The net-zero scenarios miss reality not because their technology optimism is wrong but because they
assume a fossil phase-out that is not happening.

**Conclusion.** None of this forecloses net-zero by 2070; it **relocates the constraint**. The naive
32% is not a probability; the ensemble's probabilistic reading does not survive the record; the
sensitivity floor is ~20% under sensible filtering but cannot be sharpened further. The door to 2070
is opened by cheap clean technology and held shut by fossil inertia — the decisive variable is
substitution (policy and system inertia), not cost.

### How far the forecasting method is applied (honest map)

| Method | Status |
|---|---|
| Scenarios = conditional forecasts | ✅ central reframe (Part 1) |
| Calibration / PIT | ✅ §2.4 (one point per variable — diagnostic, not formal test) |
| Skill vs a naive rule | ✅ §2.3 |
| Wright's law (cost ~ cumulative deployment) | ✅ PV/wind cost projections built (`analyse_pv_wind_wright_costs…`) with a ±2 s.e. learning-rate band |
| Random walk + variance σ²(τ+τ²/m); Bertalanffy–Richards diffusion | ⬜ framed, not fitted (no deployment forecast built yet) |
| Pooled Student-t, surrogate datasets, MA(1), CRPS/conformal | ⬜ not done — need long, many-point series; here 15 years / 4 points / all-AR6 |
