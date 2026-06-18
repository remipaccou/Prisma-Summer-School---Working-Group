# Consolidation plan — Hindcast of IAM ensembles

*The single document so we never get lost again. The whole project on one page.*

---

## The question (reframed)

**Before:** "by correcting for historical accuracy, what is the revised probability of net-zero 2070?"

**After (Lafond, slide 3 — *scenarios = conditional forecasts*):** an IAM scenario is a *"if policy follows this path, then…"*. **One cannot extract an unconditional probability from a bag of conditional forecasts.** So we do not *revise a probability* — we **test whether the ensemble is a calibrated forecast**, and we **build our own honest forecast** of the observables.

## The story in one sentence

> **The SCI ensemble is not a calibrated forecast — it is too confident and biased low. We show it through calibration; we build an honest benchmark of the observables; and the conditional view (Wright) reconciles the gap.**

---

## The 3 deliverables (the backbone of the report)

| # | Deliverable | What it shows | Status | Files |
|---|---|---|---|---|
| **L1** | **Ensemble calibration (PIT/coverage)** | The ensemble is NOT calibrated: reality falls in the tails (CO₂ 75th, solar 90th, **GDP 1st percentile**). Replaces ME/MAE/RMSE with Lafond's true metric. | ✅ **done** | `calibration_pit.py/.png` |
| **L2** | **Honest benchmark** | CO₂ = random walk with drift (already beats the ensemble); solar = **Bertalanffy-Richards diffusion curve** (not Moore — corrects the +149%), validated in PIT/coverage. Our intervals cover reality where the IAM misses it. | ⬜ **to be coded (the signature piece)** | `co2_benchmark.*` (deterministic skeleton) |
| **L3** | **Conditional view (Wright)** | Each scenario IS a deployment path → Wright gives the implied cost. Way et al. 2022: the "expensive transition" assumption is inconsistent with their own deployment. Links the *addition* mode to cost. | ⬜ **one slide** | — |

---

## Part A — the foundation (done, no more polishing)

Error diagnostics that *prepare* the 3 deliverables. Everything is in `working files/`:

- **Finding 1** — 2020 = COVID noise, 2025 = structural signal (+2,582 survives detrending). → `co2_finding1*`, `finding1_robustness.md`
- **Ambition gradient** — the 2025 error = the assumed ambition (C1→C8); reality at C6-C7 (~3-4°C world). → `co2_2025_ambition.*`
- **Kaya** — the CO₂ error = **decoupling** optimism (GDP +14%, intensity −18%), not growth. → `co2_kaya.*`
- **Naive benchmark** — a rule beats the ensemble on 4/6 variables (up to 95% of scenarios). → `co2_benchmark.*`
- **Addition not substitution** — reality = more coal AND more solar (72% of scenarios). This is the mechanism.
- **Vintage** — real but partial effect; the energy/economy split is confounded with it. → `co2_vintage.*`

## Part C — secondary object (NOT the core)

**Sensitivity of the net-zero SHARE to filtering** (not "the revised probability"). The NZ share ranges from **20% to 48%** depending on the credibility variable (CO₂ ⬇️, solar ⬆️) → **non-robustness = slide 3 proven.** → `partC_sensitivity.*`, `partC_findings.md`

**Part B folds into C:** we filter **multivariate (CO₂+coal+solar)** because CO₂ alone is a trap (Kaya). No need for LASSO/PCA.

---

## What we cut

- ❌ **PCA/SVD** — changes nothing, appendix at best.
- ❌ **Energy vs economy (Finding 3)** — does not bite at 2025, confounded with vintage.
- ⚠️ **LASSO** — light only, and **circularity trap** (regressing the CO₂ error on the CO₂ projection). If we do it: predict the *late* error with *early* variables.
- ✅ **Box plots** — keep, cheap and visual.

## Feasibility caveats (to state, not hide)

- **15 years / 4 points** → we take **the spirit of Lafond** (calibration, honest intervals, B-R on annual solar), not the pooled machinery (surrogate datasets, rolling origins).
- **Wright (slide 23)**: hard to prove it beats Moore → present it as the *policy-relevant view*, not "the truth".
- **Unknown solar asymptote L** → the B-R forecast will be sensitive to it. To be declared.
- **Inflated naive p-values** (KS p<10⁻¹⁶) due to serial dependence (slide 11) → one sentence is enough.

---

## Next step

1. **L1** — plot the PIT/calibration figure (the numbers exist). *Cheap.*
2. **L2** — code the **Bertalanffy-Richards** solar + PIT backtest. *The differentiating piece.*
3. **L3** — one Wright/Way et al. slide.
4. Write the 3 framing paragraphs in `methodology.md` (§3.1, §5, §5.2).
