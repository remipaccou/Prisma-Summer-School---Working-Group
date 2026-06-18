# Part C — Findings (filtering, the limit, and the cost view)

## Overview

Part C was meant to deliver the corrected number: keep the credible scenarios, recompute the net-zero share. It does not produce a single number — and that is the result. It then turns constructive: the one thing that *can* be forecast honestly is technology cost, conditional on deployment (Wright's law), and it relocates the barrier to net zero.

## Finding 12 — Filtering gives no stable number (C.1)

Keeping the 25% of scenarios most accurate over 2010–2025 and recomputing the net-zero share, the result moves in **opposite directions** depending on the credibility variable (naive share ≈ 34%):

| Keep the 25% most accurate on… | net-zero share |
|---|---|
| CO₂ | ~20% ↓ |
| coal + CO₂ + solar (multivariate) | ~22% ↓ |
| Solar | ~48% ↑ |

Read honestly: **under any reasonable filter (CO₂ or the multivariate criterion) the share is ~20%** — a third below the naive 34%. It rises to ~48% only under a *solar-only* filter, which is the questionable choice precisely because solar is the variable where every scenario fails (Finding 9); "most accurate on solar" means "least catastrophically wrong among a uniformly wrong field". So the honest statement is not "anything between 20% and 48%" but: **the answer depends on the conditioning variable, and only a poorly-motivated filter lifts it.**

The mechanism is Finding 10: net-zero pathways were right on solar and wrong on CO₂/coal, so filtering on what they missed removes them while filtering on what they got right keeps them. This **non-robustness is the empirical proof of the conditional-forecast point**: one cannot extract an unconditional probability from conditional forecasts, because the answer depends on the conditioning variable chosen. We therefore relabel the object — not "the revised probability" but **the sensitivity of the net-zero share** to credibility filtering.

→ Figure: `figures/partC_sensitivity.png`

## Finding 13 — The irreducible floor (the honest limit)

Even a careful filter meets a wall. A pathway that decarbonises *late* (flat to ~2030, then crashes to net zero by 2070) is indistinguishable from a non-net-zero pathway over 2010–2025. The 15-year hindcast cannot separate them, so credibility filtering cannot push the net-zero share below the share of these late movers (~20%). That residual is genuine uncertainty the record is structurally unable to resolve, not a number we can sharpen. A true long-horizon test would need older (AR5, ~2014) scenarios forecasting 2025 with no knowledge of it — absent from this ensemble.

## Finding 14 — The barrier is substitution, not technology cost (C.2, Wright's law)

Moore's law forecasts cost unconditionally from time; **Wright's law forecasts cost conditional on a deployment path**, which makes it the right tool here — each scenario *is* a deployment path. Fitting a one-factor learning curve (cost ∝ cumulative-capacity^−b) on historical PV/wind costs and projecting along each group's capacity trajectory:

- PV cost collapses from ~2,440 $/kW (2010) to ~250 (2024) and Wright projects ~30–50 $/kW by 2070.
- The net-zero and non-net-zero cost paths are **nearly identical** — deploying more makes PV only marginally cheaper, because both worlds already drive cost to the floor.

This reconciles the constructive result with the critical Part A. The world deploys renewables *faster* than the models assumed (Finding 5) and their cost is falling *faster* than the models assumed (Wright) — so clean technology is doing better, not worse, than the ensemble supposes. Yet emissions keep rising (Finding 1) because fossils are not retiring. **The barrier to net zero is therefore not the cost of clean technology — empirically that is improving ahead of the models — it is substitution: the failure to phase out fossils even as renewables boom and cheapen.** The near-identical cost paths reinforce this: cost does not distinguish the net-zero world from the other; substitution does.

*Caveats.* Wright's law is hard to establish as superior to Moore's law (cost and production co-evolve; multicollinearity) — it is the policy-relevant lens, not a proven point predictor. And the cost projection is currently reported as lines; to stay consistent with the calibration critique of the ensemble (Finding 9), it should carry an **uncertainty band** on the learning rate, not a single curve.

→ Figures: `figures/pv_wright_cost_projection_to_2070.png`, `figures/wind_wright_cost_projection_to_2070.png`

## Key takeaway

There is no single corrected net-zero probability — the share is ~20% under any reasonable filter, bounded below by late movers the record cannot expose, and the very non-robustness proves the 32% was never a probability. And the constructive view relocates the question: net zero by 2070 is not foreclosed by data, nor blocked by clean-technology cost (which is improving ahead of the models). What the record shows is that the world adds renewables without subtracting fossils. The door to 2070 is opened by technology and held shut by fossil inertia.

## Files

| File | Description |
|---|---|
| `scripts/partC_sensitivity.py` | Net-zero share vs filtering criterion (C.1) |
| `scripts/analyse_pv_wind_wright_costs_vetted_log.py` | Wright's-law cost projection, PV & wind (C.2) |
| `figures/partC_sensitivity.png` | The share is not robust |
| `figures/pv_wright_cost_projection_to_2070.png` | PV cost to 2070 by group |
| `figures/wind_wright_cost_projection_to_2070.png` | Wind cost to 2070 by group |
