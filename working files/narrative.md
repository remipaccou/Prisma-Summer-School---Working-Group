# Narrative

*Built step by step. One step = one result, stated simply.*

## Research question

The SCI 2025 ensemble holds 1,564 model pathways; 497 reach net-zero CO₂ by 2070 — read
naively, a ~32% "chance" of net-zero by 2070.

**Is that 32% meaningful — and what happens to it once we confront the scenarios with what
actually happened over 2010–2025?**

## Step 1 — The naive 32% is not a probability

**Conceptual.** An IAM scenario is a *conditional* forecast — "*if* policy follows this path,
*then* emissions follow that one." It is not a draw from a distribution of possible futures.
Counting how many "if–then" pathways end in net-zero measures the menu modelling teams chose to
run, not the chance the world gets there.

**Empirical.** The number is not even stable. "Net-zero by 2070" hides an arbitrary deadline:

| Net-zero reached by | Pathways | Share |
|---|---|---|
| 2060 | 256 | 16% |
| 2070 | 497 | 31% |
| 2080 | 688 | 43% |
| any time (≤2100) | 909 | 57% |

Slide the deadline by a decade and the "probability" doubles. A number that depends that much on
its own definition is not a probability.

**So we pivot.** We do not revise a probability. We ask two honest questions:

1. Is the ensemble a usable, well-calibrated forecast?
2. How does conditioning on historical accuracy move the net-zero *share*?

---

## Step 2 — The hindcast: the ensemble undershoots 2025 (structural, not COVID)

We compare the ensemble's CO₂ projection to observed reality at the 4 points 2010→2025.
Error = observed − projected (**positive = the models aimed too low**).

The full ensemble — all CO₂ trajectories (2010–2100) with the 4 observed points (context):

![All SCI scenarios + observed CO₂](co2_overview.png)

| Year | Observed | Projected (mean) | Error |
|---|---|---|---|
| 2010 | 33,400 | 32,995 | +405 |
| 2015 | 35,400 | 35,385 | +15 |
| 2020 | 34,800 | 36,372 | **−1,572** |
| 2025 | 38,100 | 35,518 | **+2,582** |

Through 2015 the ensemble is near-perfect. Then two errors appear — and they are **two different
stories**:

- **2020 (−1,572, models too high) = COVID.** Lockdowns crashed emissions. Remove the dip
  (interpolate 2015→2025) and the error flips sign (≈ +378): without COVID the models were nearly
  spot-on. So ~75% of the 2020 gap is COVID, not model failure.
- **2025 (+2,582, models too low) = structural.** No COVID to remove here: by 2025 emissions had
  recovered, and 38,100 sits right on the pre-COVID trend (~39,400 extrapolated). The ensemble did
  not miss a shock — it assumed a peak-and-decline that never came. **Structural optimism.**

The models' median peaks ~2020 then falls; reality dips (COVID) then rises — they diverge in
opposite directions after 2020.

![Finding 1 — models vs reality, and the 2020/2025 decomposition](co2_finding1_simple.png)

**This +2,582 is the load-bearing number:** it survives every detrending, and it says the
ensemble is biased low.

---

## Step 3 — The net-zero scenarios are the ones most biased low

Split the ensemble into **NZ2070** (the 497 that reach net-zero by 2070) and **non-NZ**.
Their mean CO₂ error over 2010–2025 (family-weighted):

| Group | Mean error (ME) | MAE |
|---|---|---|
| **NZ2070** | **+650** (under-project) | 2,147 (~6%) |
| **non-NZ** | **+216** (far less) | 1,649 (~5%) |

NZ scenarios systematically project less CO₂ than reality — they assumed faster decarbonization
than happened. The gap holds under every weighting (+434 family, +837 scenario, +1,281 project).

![Step 3 — NZ scenarios are biased low, not more imprecise](nz_bias.png)

Three things to keep honest:

- **It is a bias, not imprecision.** The error *magnitude* (MAE) is similar (~6% vs ~5%). What
  separates the groups is the *direction* (NZ always too low), not the size.
- **It is partly tautological.** To reach net-zero by 2070 a pathway must bend emissions down
  early; reality did not; so an NZ pathway under-projects 2025 *by construction*. And a pathway
  that decarbonizes late (after ~2030) is indistinguishable from non-NZ over 2010–2025 — the
  hindcast only catches early movers.
- **It is robust** to how we weight (scenario / family / project).

**Defensible claim** (not "net-zero models are wrong"):

> Pathways premised on an early turn — which has not begun — are now the least consistent with
> observation.

---

*Next: Step 4 — does the ensemble forecast at all? (a trivial rule beats it on 4 of 6 variables).*
