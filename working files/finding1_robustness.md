# Finding 1 — robustness & defense notes

Numbers behind `co2_finding1.png`. Variable: CO₂ Energy & Industrial Processes,
family-weighted (1/n_f). All in Mt CO₂.

## The core claim, separated by year

Models were well calibrated through 2020 **once COVID is removed**, but assumed an
emissions **peak ~2020 + decline** that did not happen. The ensemble mean peaks at 36.4 Gt
(2020) and falls to 35.5 Gt (2025); reality dipped (COVID) then rose to 38.1 Gt.

| Year | obs | proj (fam-wtd) | ME | Reading |
|---|---|---|---|---|
| 2010 | 33,400 | 32,995 | +405 | calibrated |
| 2015 | 35,400 | 35,385 | +15 | calibrated |
| 2020 | 34,800 | 36,372 | **−1,572** | **COVID** (see below) |
| 2025 | 38,100 | 35,518 | **+2,582** | **structural optimism** |

## 1. The 2020 over-projection is COVID — robust to the counterfactual

Two COVID-free counterfactuals for 2020 (neither is "the" truth; reported as a range):

| 2020 counterfactual | value | ME |
|---|---|---|
| raw observed | 34,800 | −1,572 |
| interpolate 2015→2025 | 36,750 | **+378** |
| extrapolate 2010–2015 trend | 37,400 | **+1,028** |

Both flip the sign → the 2020 "overshoot" is the COVID dip, not model bias.
(The interpolation uses 2025 and is mildly circular — hence we show the forward-trend
variant too; the conclusion holds either way.)

## 2. The 2025 under-projection is NOT COVID

38,100 is real observed (no dip to remove). The pre-COVID trend (+400/yr) extrapolates 2025
to 39,400 — reality (38,100) is ~on trend (−1,300). The +2,582 gap is the ensemble assuming
a decline, i.e. structural optimism. **This is the load-bearing number and it survives detrending.**

## 3. Weighting sensitivity (for the NZ gap, Finding 2) — robust

ME_j, NZ2070 vs non-NZ:

| weighting | NZ | non-NZ | gap |
|---|---|---|---|
| scenario | +807 | −30 | +837 |
| **family (primary)** | +607 | −23 | **+630** |
| project (robustness) | +841 | −441 | +1,281 |

Family is the **conservative** primary estimate; project (which controls for the
convenience-sample structure) gives a larger gap and is reported as robustness — not the headline.

## 4. The "32%" is definition-dependent

P(NZ2070) depends entirely on the net-zero threshold:

| definition | n | share |
|---|---|---|
| net-zero CO₂ ≤2060 | 256 | 16% |
| net-zero CO₂ ≤2070 | 497 | 31% |
| net-zero CO₂ ≤2080 | 688 | 43% |
| net-zero CO₂ ever (≤2100) | 909 | 57% |

→ ammunition for the framing point: an IAM ensemble is not a forecast distribution, and the
headline share is not even stable to its own definition.

## 5. Addition signature — lead with marginals, not the joint fraction

At 2025: **82%** of scenarios under-project coal, **90%** under-project solar.
Joint (both): 72% ≈ 0.82×0.90 = 0.738 → the joint fraction adds nothing beyond the marginals.
The real addition-vs-substitution evidence is the **negative within-ensemble error correlation**
(A2 Finding 6, Coal↔Solar), not the 72%.

## Count reconciliation

1,591 CO₂ scenarios (all "World", no duplicates); 1,563 have a 2025 value → the doc's
"1,564 scenarios" = those comparable at 2025. No data issue.
