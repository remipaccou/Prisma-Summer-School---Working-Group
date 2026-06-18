# 2025 — rebound, ambition, and the naive benchmark

Three linked analyses answering "where does the 2025 error come from, and is the ensemble any good?"

## 1. The "2025 surplus" is not a rebound — it is the trend resuming

| 2025 | value |
|---|---|
| pre-COVID trend, extrapolated | 39,400 |
| reality | 38,100 (−1,300 *below* trend) |
| models (family-weighted mean) | 35,518 (−3,882 below trend) |

Realised 2025 sits *below* its pre-COVID trajectory → there is no exceptional rebound to explain.
The +2,582 ensemble gap comes ~75% from the models assuming a **decline**, not from a shock.

## 2. 2025 accuracy = the assumed ambition, not the model — `co2_2025_ambition.py`

ME at 2025 by AR6 climate category: a near-monotonic gradient.

| C1 (1.5°) | C2 | C3 | C4 | C5 | C6 (<3°) | C7 (<4°) | C8 (>4°) |
|---|---|---|---|---|---|---|---|
| +8,353 | +4,229 | +4,377 | +2,355 | +1,530 | +720 | −2,005 | −6,481 |

Reality falls between **C6 and C7** = a "<3–4°C, low-action" world. The scenarios that
"predict 2025 well" are those that assumed little decarbonisation.

⚠️ Partly tautological (a C1 *must* decarbonise early → low 2025 CO₂). The non-tautological
result is **where reality falls** (C6–C7).

## 3. Naive benchmark — does the ensemble beat a simple rule? — `co2_benchmark.py`

Forecast 2025 using **2010–2015** (pre-COVID) information. skill = |error ensemble| / |error rule|.
skill > 1 → the rule wins. "% beaten" = share of scenarios worse than the rule.

| Variable | error ensemble | error rule | skill | % scenarios beaten |
|---|---|---|---|---|
| CO₂ | 7% | 3% (linear) | **2.0** | 81% |
| Coal | 14% | 3% (linear) | **4.7** | 91% |
| Nuclear | 16% | 2% (random walk) | **9.9** | 95% |
| GDP | 11% | 4% (linear) | **3.0** | 77% |
| Solar PV | 51% | 75% (linear) | 0.7 | 6% |
| Wind | 17% | 30% (linear) | 0.6 | 34% |

**On 4 of 6 variables, a trivial rule beats the entire ensemble** (up to 95% of scenarios
beaten). On PV/wind the ensemble wins but remains massively wrong (51% on PV) → this is where
a dedicated method is needed (**Wright's law / Farmer–Lafond**, cf. Part C2).

**Caveats:** a single target year (2025) → "% beaten" is the robust statistic, not single-point skill.
The rule is trained on 2 points (2010, 2015). For PV the log-trend explodes (7,311): neither naive
nor ensemble captures the exponential — hence the diffusion-curve treatment in §5.2.

## Next lead (colleague / François): AR5 vs AR6

This dataset contains **no AR5 scenarios** (earliest publication = 2017, AR6 lineage). A genuine
long-horizon out-of-sample test (2014-vintage scenarios forecasting 2025) needs the external
**IIASA AR5 Scenario Database**. This is the only true forecasting test, and the most interesting.
