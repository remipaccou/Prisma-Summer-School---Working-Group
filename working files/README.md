# Working files — the narrative

The **readable story** of the project, plus the figures it uses. Separate from the formal
`scripts/` + `figures/` pipeline at the repo root.

## Read this

| File | For |
|---|---|
| **`narrative.md`** | The story in 8 plain steps, illustrated. **Start here** (team-facing). |
| **`narrative_updated.md`** | The same 8 steps in Lafond's vocabulary + formalism, with an honest map of how far his method is applied (supervisor-facing). |

## Figures used by the narrative

| Figure | Step | Shows |
|---|---|---|
| `co2_overview` | 2 | all CO₂ trajectories + observed points (context) |
| `co2_finding1_simple` | 2 | 2020 COVID vs 2025 structural optimism |
| `nz_bias` | 3 | net-zero scenarios are biased low |
| `co2_benchmark` | 4 | a trivial rule beats the ensemble (4/6 variables) |
| `calibration_pit` | 5 | reality falls in the tails → not calibrated |
| `partB1_boxplots` | 6 | coal/CO₂/solar carry the signal |
| `partC_sensitivity` | 7 | the net-zero share is not robust (20→48%) |
| `co2_kaya` | 6 | CO₂ error = decoupling optimism (why CO₂-alone filtering is a trap) |

Each `.py` regenerates its `.png`.

## `archive/`

Secondary / superseded explorations and working notes (energy-vs-economy archetypes, vintage,
2025 ambition gradient, horizon×vintage, the early findings notes, the planning doc). Kept for
reference, not part of the story.

## Running

```bash
python calibration_pit.py && python co2_benchmark.py && python partC_sensitivity.py
```

> Hard-coded data path (`SCI_DATA`) → SCI-2025 `.xlsx` in `~/PhD/.../Scenario_Compass_Initiative_Data`.
