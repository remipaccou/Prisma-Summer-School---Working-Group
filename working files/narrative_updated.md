# Narrative

*A working note, in the voice of students who keep re-checking their own answer. Three acts:
the question we thought we had → taking the ensemble apart → the one thing we can still forecast.*

---

## Act 1 — The question we thought we had

We started where everyone starts. The SCI 2025 ensemble has 1,564 model pathways; 497 of them reach
net-zero CO₂ by 2070. So 497/1,564 ≈ **32%**, and the natural reflex is to treat that as the chance
of net-zero and to try to make it sharper.

The more we looked, the less that number behaved like a probability — for two reasons.

**Conceptually**, each pathway is a *conditional* forecast: "*if* policy, technology and demand
follow this path, *then* emissions follow that one." It is not a draw from a distribution of possible
futures. Counting how many conditional "if–then" paths happen to end at zero tells us about the
**menu of scenarios the modelling teams chose to run**, not about the likelihood of the world. You
cannot manufacture an unconditional probability by counting conditional forecasts.

**Empirically**, the number isn't even stable. "Net-zero by 2070" hides an arbitrary deadline — slide
it and the share moves a lot:

| Net-zero reached by | Pathways | Share |
|---|---|---|
| 2060 | 256 | 16% |
| 2070 | 497 | 31% |
| 2080 | 688 | 43% |
| any time (≤2100) | 909 | 57% |

A figure that runs from **16% to 57%** by sliding its own definition a decade is not a probability.

So we changed the question. Instead of *revising a probability*, we decided to test the ensemble the
way you test any forecast: **is it biased? does it beat a trivial rule? is it calibrated?** — and
then, if we keep only the scenarios that actually tracked reality, **what happens to the net-zero
share?**

---

## Act 2 — Taking the ensemble apart

If the 32% isn't a probability, the honest move is to backtest the ensemble against what already
happened (2010–2025). We expected it to do reasonably well. It kept failing — in instructive ways.

**It undershoots 2025, and that miss is structural.** Lining up the ensemble's CO₂ projection against
reality (error ε = observed − projected, positive = projected too little):

| Year | observed | ensemble mean | ε |
|---|---|---|---|
| 2010 | 33,400 | 32,995 | +405 |
| 2015 | 35,400 | 35,385 | +15 |
| 2020 | 34,800 | 36,372 | **−1,572** |
| 2025 | 38,100 | 35,518 | **+2,582** |

Two late errors, two different causes. **2020** looks like over-projection, but that is COVID: replace
the dipped 34,800 with a COVID-free interpolation (~36,750) and the error flips to ≈ +378 and nearly
vanishes — the models were right about the underlying level, they just couldn't foresee a pandemic.
**2025** is the real one: emissions had recovered and landed almost exactly on the pre-COVID trend
(~39,400 extrapolated), so reality did nothing surprising — the *ensemble* did, by assuming a
peak-and-decline that never came. The +2,582 is structural optimism, and it survives every way of
removing COVID.

![Models vs reality, COVID (2020) vs structural (2025)](co2_finding1_simple.png)

**The net-zero scenarios are the most biased low.** Splitting by outcome, the net-zero group's mean
CO₂ error is **+650** vs **+216** for the rest (family-weighted). One honesty note: the non-NZ *level*
depends on weighting — it is near zero under scenario weighting, +216 under family weighting — so we
read the **gap**, which is robust (+434 to +837 across weightings). It is a *bias*, not imprecision
(the typical error sizes, ~6% vs ~5%, are close). And it is partly true by construction: reaching
net-zero by 2070 forces an early downturn, so such a pathway *must* under-project a reality that did
not turn. The defensible claim is narrow: *pathways premised on an early turn that has not begun are
now the least consistent with the record.*

![Net-zero scenarios are biased low (not more imprecise)](nz_bias.png)

**A trivial rule beats the ensemble — but this is a corollary, not a separate proof.** Forecasting
2025 from only 2010–2015 with a dumb rule (random walk / straight-line trend) beats the ensemble on
CO₂, coal, nuclear and GDP. We are careful here: the rule wins on CO₂/coal/GDP *for the same reason*
as Act 2's structural optimism — reality stayed on trend while the ensemble bet on a turn — so this
is the same fact seen again, not an independent leg. And nuclear's spectacular "skill 9.9" is hollow:
nuclear is flat (375→377 GW), so "nothing changes" is near-perfect by construction. The honest
takeaway: **on the variables that stayed on trend, the ensemble shows no skill against a ruler.**

![A trivial rule beats the ensemble on the on-trend variables](co2_benchmark.png)

**It is biased low — though "miscalibrated" is a diagnosis, not a proof.** Asking where reality lands
in the scenario cloud (its percentile): GDP 1st, nuclear 20th, CO₂ 75th, wind 75th, coal 79th, solar
90th. Reality is **systematically on the low-emissions side** — strongly so for solar and GDP. But we
will not overstate it: 75th–79th is the upper-middle, *not* a tail, and with only one point per
variable this is a suggestive diagnostic of low bias, not a formal calibration test (which needs many
origins × targets). "Overconfident" is firm only where reality is in a true tail (solar, GDP).

![Reality is on the low-emissions side of the cloud](calibration_pit.png)

**Only three variables tell the groups apart, and they disagree.** Of the six, only coal, CO₂ and
solar separate net-zero from non-net-zero scenarios; wind, nuclear, GDP do not. And the three that do
*contradict each other*: net-zero scenarios are worse on coal and CO₂ (they assumed a fall that did
not happen) but **better on solar** (they correctly expected the boom). That is the "addition"
signature at the level of credibility. Practical consequence: filter on coal + CO₂ + solar together,
not CO₂ alone (whose GDP/intensity errors can cancel).

![Coal, CO₂, solar carry the signal — and disagree](partB1_boxplots.png)

**So filtering gives ~20%, not "anything".** Keeping the most accurate scenarios and recomputing the
net-zero share: it lands at **~20% under any reasonable filter** (CO₂ → 20%, multivariate → 22%). It
only rises to 48% under *solar-only* filtering — a poor criterion, since solar is the variable
*everyone* misses badly. So the honest claim is not "the number could be anything between 20 and 48",
it is: **~20% whenever you filter sensibly, and only a questionable filter pushes it back up.** What
is robust is that the answer *depends on the conditioning variable* — which is the empirical proof of
Act 1: you cannot read a single unconditional probability out of conditional forecasts.

![The corrected net-zero share: ~20% under sensible filters](partC_sensitivity.png)

---

## Act 3 — The one thing we can still forecast

By here we were uneasy: if we have spent the whole project showing the ensemble is an unreliable
forecast, can we say anything *constructive*? Two things — one a limit, one a genuine forecast.

**The limit, stated honestly.** A 15-year backtest cannot settle a 45-year question. A pathway that
stays flat until ~2030 and only then crashes to net-zero is indistinguishable from a non-net-zero
pathway over 2010–2025, so no filter can push the share below the share of these "late movers" (the
~20% acts as a practical floor — we cannot measure it precisely, by definition). And every scenario
here is post-2017, so this is a hindcast, not a true out-of-sample test; the AR5 vintage (~2014
forecasting 2025) would be the real test, and this ensemble does not contain it.

**The forecast we *can* make: cost.** The one quantity with a long, clean track record is the cost of
clean technology, and Wright's law (cost falls with cumulative deployment) forecasts it well. Solar PV
cost fell from ~2,440 $/kW in 2010 to ~250 in 2024, and Wright projects it toward ~30–40 $/kW by 2070.

![PV cost collapses, and the net-zero / non-net-zero curves are nearly identical](../figures/pv_wright_cost_projection_to_2070.png)

The striking detail: the net-zero and non-net-zero projections sit almost on top of each other. Clean
tech becomes very cheap **whether or not the world reaches net-zero.** (Two caveats we hold ourselves
to: this figure draws *lines*, not uncertainty bands — to be consistent with our own critique of the
ensemble's overconfidence, it needs a band on the learning rate; and Wright's law is hard to prove
strictly better than a time-trend, so we present it as the policy-relevant lens, not a proven point
forecast.)

**The reconciliation — and the real conclusion.** At first this seems to contradict Act 2: how can
net-zero be "improbable" *and* clean tech be cheaper than the models assumed? It does not contradict,
once you remember the addition signature. The world is doing **two things at once**: deploying
renewables faster than any model (so costs fall faster than assumed — Act 3) while keeping the fossils
(so emissions keep rising — Act 2). The lock on net-zero is therefore **not the cost of clean
technology** — that is going *better* than the scenarios assume. The lock is **substitution**: we add
clean energy without removing the dirty. The net-zero scenarios miss reality not because their
technology optimism is wrong, but because they assume a fossil phase-out that is not happening.

So, where it leaves us. None of this forecloses net-zero by 2070 — it **relocates the problem**. The
naive 32% is not a probability; the ensemble's probabilistic reading does not survive the record; but
the door to 2070 is *opened* by cheap clean technology and *held shut* by fossil inertia. The
decisive variable is not cost, it is substitution — which is to say, policy and system inertia, not
engineering.
