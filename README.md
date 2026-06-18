# PRISMA Summer School 2026 — Group Work (Probabilistic Methods)

## Question

What conclusions can we draw on reaching net zero CO₂ emissions globally by 2070?

## Team

- Lucas Alvarez (Universitat Politècnica de València)
- Matteo Catania (Politecnico di Milano)
- Rémi Paccou (CIRED / Schneider Electric)

Supervisor: François Lafond

## Repository structure

**→ Main written output: [`working files/narrative_updated.md`](working%20files/narrative_updated.md)** — the full story with the forecasting vocabulary made explicit. (Plain 8-step version: [`working files/narrative.md`](working%20files/narrative.md).) *The output will be promoted to the repo root once final.*

```
├── README.md
├── methodology.md               ← full method description (Parts A/B/C)
├── findings/                    ← detailed results, one file per part (A1/A2/B/C)
│   ├── partA1_findings.md       ← hindcast bias (undershoot, NZ low, ambition≠model, vintage)
│   ├── partA2_findings.md       ← error structure & forecast quality (addition, skill, calibration)
│   ├── partB_findings.md        ← variable selection (coal/CO₂/solar discriminate)
│   └── partC_findings.md        ← filtering + the irreducible floor + Wright cost view
│
├── report/main.tex              ← 2-page LaTeX report
├── data/                        ← observed data (6 variables) + SCI documentation
│
├── scripts/                     ← analysis pipeline (the "official" run)
│   ├── partA1_hindcast.py       ← Part A.1: hindcast evaluation (6 vars, weighting, vintage)
│   ├── partA2_diagnostics.py    ← Part A.2: addition test, cross-correlation, autocorrelation
│   ├── partB1_boxplots.py       ← Part B.1: variable selection (box plots)
│   ├── partB2_lasso.py          ← Part B.2: variable selection (LASSO, confirms B.1)
│   └── analyse_pv_wind_wright_costs_vetted_log.py  ← Part C.2: Wright's-law cost projection (PV/wind)
│
├── figures/                     ← figures for the pipeline (partA1/A2/B1/B2 + Wright PV/wind)
│
└── working files/               ← the narratives + their figures + lab
    ├── narrative.md             ← the story in 8 steps (team-facing)
    ├── narrative_updated.md     ← the OUTPUT (detailed, with forecasting vocabulary)
    ├── *.png                    ← the figures the narratives embed
    ├── scripts/                 ← the Python that regenerates those figures
    └── archive/                 ← secondary / superseded explorations
```

## Naming convention

| Prefix | Content |
|--------|---------|
| `partA1_` | Hindcast error computation (ME, MAE, RMSE) |
| `partA2_` | Error diagnostics (autocorrelation, cross-variable) |
| `partB1_` | Variable selection — box plots |
| `partB2_` | Variable selection — LASSO |
| `partC1_` | Scenario filtering and revised P(NZ2070) |
| `partC2_` | PV forecast (logistic + Wright's law) |

## Observed variables

| Variable | Source | Confidence |
|----------|--------|-----------|
| CO₂ emissions (Mt CO₂/yr) | Global Carbon Budget 2025 | high |
| Coal primary energy (EJ/yr) | Energy Institute Statistical Review 2025 | medium |
| Solar PV capacity (GW) | IRENA 2026 | high |
| Wind capacity (GW) | IRENA 2026 | high |
| Nuclear capacity (GW) | IAEA PRIS | high |
| GDP PPP (B US$2010/yr) | IMF WEO / World Bank | medium |

## Configuration

Each user must set their local path to the SCI data files:

```python
SCI_DATA = Path.home() / 'PhD' / '4. Modeling' / 'Prisma School' / 'Scenario_Compass_Initiative_Data'
```

SCI xlsx files are NOT in the repo (too large). Download from [SWITCHdrive](https://drive.switch.ch/index.php/s/8CAZ2vDfUVwGhYX?path=%2FGroup%20Work%2F_Scenario_Compass_Initiative_Data).
