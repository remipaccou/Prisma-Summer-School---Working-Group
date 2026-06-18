# Working files — the narrative and its lab

The **readable story** of the project (the two narratives), the figures it uses, the code that
makes them, and an archive of superseded explorations. Separate from the formal `scripts/` +
`figures/` pipeline at the repo root.

## Folder map

```
working files/
├── narrative.md            ← the story in 8 plain steps (team-facing, start here)
├── narrative_updated.md    ← same steps + forecasting vocabulary/formalism (detailed; the OUTPUT)
├── *.png                   ← the 8 figures the narratives embed (kept next to the narratives so
│                             the image links resolve)
├── scripts/                ← the Python that regenerates each figure (one .py per .png)
└── archive/                ← secondary / superseded explorations, kept for reference
```

## The two narratives

| File | For |
|---|---|
| **`narrative.md`** | The story in 8 plain steps, illustrated. Team-facing. |
| **`narrative_updated.md`** | The same steps with the forecasting vocabulary and formalism made explicit, plus an honest map of how far the method is applied. **This is the project's main written output** (to be promoted to the repo root once final). |

## Figures (in this folder) and the code (in `scripts/`)

| Figure `.png` | Generator (`scripts/`) | Step | Shows |
|---|---|---|---|
| `co2_overview` | `co2_overview.py` | 2 | all CO₂ trajectories + observed points (context) |
| `co2_finding1_simple` | `co2_finding1_simple.py` | 2 | 2020 COVID vs 2025 structural optimism |
| `nz_bias` | `nz_bias.py` | 3 | net-zero scenarios are biased low |
| `co2_benchmark` | `co2_benchmark.py` | 4 | a trivial rule beats the ensemble (4/6 variables) |
| `calibration_pit` | `calibration_pit.py` | 5 | where observed 2025 falls in the cloud (PIT) |
| `partB1_boxplots` | (root `scripts/partB1_boxplots.py`) | 6 | coal/CO₂/solar carry the signal |
| `co2_kaya` | `co2_kaya.py` | 6 | why CO₂-alone filtering is a trap (Kaya) |
| `partC_sensitivity` | `partC_sensitivity.py` | 7 | the net-zero share is not robust |

The figures stay in this folder (not in `scripts/`) so the narratives' `![...](file.png)` links keep
resolving. Each generator regenerates its figure.

## `archive/`

Secondary and superseded explorations, kept for reference, not part of the main story:
energy-vs-economy archetypes, vintage, the 2025 ambition gradient, horizon × vintage
(`horizon_findings.md` + figures), the early findings notes (`finding1_robustness.md`,
`benchmark_findings.md`), the Part C working note (`partC_findings.md`), and the planning doc.

## Running

```bash
cd "working files/scripts"
python co2_finding1_simple.py && python calibration_pit.py && python co2_benchmark.py && python partC_sensitivity.py
```

> Each script reads the SCI data via a hard-coded `SCI_DATA` path
> (`~/PhD/.../Scenario_Compass_Initiative_Data`); the SCI `.xlsx` files are not in the repo.
