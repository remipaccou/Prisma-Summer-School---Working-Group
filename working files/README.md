# Working files

Working / exploration folder — **separate from the main pipeline** (`scripts/`, `report/`)
so as not to disturb the rest and to make sharing easier. Everything concerns the variable
**CO₂ (Energy & Industrial Processes)**, SCI-2025 ensemble.

## 1. Global view & breakdowns — `co2_overview.py`

| Figure | Description |
|---|---|
| `co2_overview.png` | All CO₂ trajectories (2010–2100) + 4 observed points (GCB 2025): full horizon + zoom on the hindcast window. |
| `co2_views.png` | Breakdowns: all / Net-Zero 2070 / weighted by model (1 model = average of its scenarios) / energy / CGE / hybrid. Each panel annotates family-weighted ME/MAE/RMSE (2010–2025). |

## 2. Archetype test — `co2_archetypes.py`

Restricted to a few "pure" models to reduce intra-group dispersion:
- **ENERGY** (bottom-up, exogenous GDP): POLES, TIAM, COFFEE
- **ECONOMY** (CGE + hybrids): GEM-E3, IMACLIM, WITCH

| Figure | Description |
|---|---|
| `co2_archetypes.png` | One panel per model (intra-model dispersion visible) + metrics. |
| `co2_archetypes_summary.png` | ME by year (energy vs economy) + group ME/MAE/RMSE bars. |

**Result**: the energy trend **over-projects** (ME ≈ −715), the economy trend **under-projects** (≈ +655),
but high dispersion → suggestive, not conclusive.

## 3. Vintage analysis — `co2_vintage.py`

Cross-references the **publication year** (`Scientific Manuscript`, a proxy for the vintage / base year)
with the hindcast error.

| Figure | Description |
|---|---|
| `co2_vintage.png` | MAE by year according to vintage (left) + vintage composition of the 6 archetypes (right). |

**Key points**
- A recent scenario "predicting" 2020 predicts nothing: 2020 is **historical** for it.
- Real but partial effect (the models are not harmonized on the GCB observations).
- ⚠️ **Confounding**: the energy/economy split is correlated with vintage (IMACLIM = 100% ≥2024).
  → to conclude, one must **compare at equal vintage** or score each scenario only
  **after its base year** (true out-of-sample).

## 4. Finding 1 — defense layer — `co2_finding1.py`

Separates the **COVID-contaminated 2020** from the **structural 2025** (the true signal).

| Figure / file | Description |
|---|---|
| `co2_finding1.png` | Left: models peak ~2020 and decline vs reality which plunges (COVID) then recovers onto trend. Right: ME decomposition — 2020 = COVID (robust to 2 counterfactuals: +378 / +1,028), 2025 = +2,582 structural. |
| `finding1_robustness.md` | All the robustness numbers: COVID detrend, weighting sensitivity (family/project), NZ threshold sensitivity (16→57%), addition signature (marginals vs joint), 1591/1564 reconciliation. |

**Takeaway**: 2020 = COVID noise (to detrend), 2025 = optimism signal (to keep).
This is the load-bearing number, and it survives detrending.

## 5. 2025 — rebound, ambition, naive benchmark

| File | Description |
|---|---|
| `co2_finding1_simple.py/.png` | Pedagogical version of Finding 1 (models vs reality + COVID/structural bars). |
| `co2_2025_ambition.py/.png` | 2025 ME by AR6 climate category: C1→C8 gradient; reality falls to C6-C7 ("<3-4°C" world). |
| `co2_benchmark.py/.png` | Naive benchmark test (Lafond/Farmer): for 4 of 6 variables, a trivial rule beats the ensemble (up to 95% of scenarios beaten). |
| `benchmark_findings.md` | Note: rebound≠trend, ambition gradient, benchmark, AR5 lead. |

## 6. Part C — net-zero share sensitivity (the project's result)

| File | Description |
|---|---|
| `partC_sensitivity.py/.png` | The "corrected NZ share" is not robust: 20%→48% depending on the filtering variable (CO₂ ⬇️ vs solar ⬆️). Lafond slide 3: no unconditional probability from conditional forecasts. |
| `co2_kaya.py/.png` | Kaya decomposition: the CO₂ error = decoupling optimism (GDP +14%, intensity −18%), not growth → why filtering on CO₂ alone is a trap. |
| `partC_findings.md` | The reframe, the result (non-robustness), the mechanism, the next steps (calibration, Bertalanffy-Richards, Wright). |

## Energy / CGE / hybrid classification

- **energy**: IMAGE, POLES, COFFEE, GCAM, TIAM, PROMETHEUS
- **CGE**: AIM, GEM-E3, IMACLIM, EPPA, CGEM
- **hybrid**: REMIND, WITCH, MESSAGE, MERGE

## Running

```bash
python "co2_overview.py" && python "co2_archetypes.py" && python "co2_vintage.py"
```

> Hard-coded data path (`SCI_DATA`) → reads the SCI-2025 `.xlsx` in
> `~/PhD/.../Scenario_Compass_Initiative_Data`. Adapt to the machine.
