# Working files

Working / exploration folder — **separate from the main pipeline** (`scripts/`, `report/`).
SCI-2025 IAM ensemble vs observed 2010–2025 data.

See **`plan.md`** for the one-page roadmap (reframed question + 3 Lafond deliverables).

## The essential story (4–5 figures)

| File | Variables | What it shows |
|---|---|---|
| `calibration_pit.py/.png` | **6 vars** | **L1** — the ensemble is not a calibrated forecast: reality 2025 sits in the tails (GDP 1st, nuclear 20th, CO₂ 75th, coal 79th, solar 90th percentile), not the centre. |
| `co2_benchmark.py/.png` | **6 vars** | A trivial rule (random walk / linear trend) beats the whole ensemble on 4 of 6 variables (up to 95% of scenarios beaten); only solar/wind favour the ensemble, and there it is still ~50% off. |
| `partC_sensitivity.py/.png` | CO₂+coal+solar | **The result** — the "corrected net-zero share" is not even directionally robust: 20%→48% depending on the credibility variable (CO₂ ⬇️ vs solar ⬆️). Lafond slide 3: no unconditional probability from conditional forecasts. |
| `co2_finding1_simple.py/.png` | CO₂ | 2020 = COVID noise (detrends away), 2025 = structural optimism (+2,582, the load-bearing number). |
| `co2_kaya.py/.png` | CO₂+GDP | The CO₂ error = decoupling optimism (GDP +14%, intensity −18%), not growth → why filtering on CO₂ alone is a trap. |

## Notes

- `plan.md` / `narrative.md` — project roadmap (question reframed, 3 deliverables, what to cut).
- `benchmark_findings.md` — rebound≠trend, ambition gradient, naive benchmark, AR5 lead.
- `partC_findings.md` — the Part C reframe, result, mechanism, next steps.

## `archive/`

Secondary / superseded CO₂ explorations (kept for reference, not part of the core story):
overview & breakdowns, energy-vs-economy archetypes, vintage analysis, the 2025 ambition gradient,
the complex Finding-1 figure, Finding-1 robustness note.

## Classification (energy / CGE / hybrid)

- **energy**: IMAGE, POLES, COFFEE, GCAM, TIAM, PROMETHEUS
- **CGE**: AIM, GEM-E3, IMACLIM, EPPA, CGEM
- **hybrid**: REMIND, WITCH, MESSAGE, MERGE

## Running

```bash
python calibration_pit.py && python co2_benchmark.py && python partC_sensitivity.py
```

> Hard-coded data path (`SCI_DATA`) → reads the SCI-2025 `.xlsx` in
> `~/PhD/.../Scenario_Compass_Initiative_Data`. Adapt per machine.
