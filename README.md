# PRISMA Summer School 2026 — Group Work (Probabilistic Methods)

## Question

What conclusions can we draw on reaching net zero CO₂ emissions globally by 2070?

## Team

- Lucas Alvarez (Universitat Politècnica de València)
- Matteo Catania (Politecnico di Milano)
- Rémi Paccou (CIRED / Schneider Electric)

Supervisor: François Lafond

## Start here

**→ [`output of work.md`](output%20of%20work.md)** — the main written output: the full argument with the
forecasting vocabulary made explicit (framework, the question, the hindcast diagnosis, what can still be
forecast). It embeds every figure and is the document to read first.

Then, for depth:

- [`methodology.md`](methodology.md) — the method itself (notation, metrics, Parts A/B/C, data sources).
- [`findings/`](findings/) — the detailed results behind each claim, one file per part, with the numbers
  and the honest caveats.

## Repository structure

```
├── output of work.md            ← THE OUTPUT — read this first
├── methodology.md               ← the method (notation, metrics, Parts A/B/C)
├── README.md
│
├── findings/                    ← detailed results, one file per part
│   ├── partA1_findings.md       ← hindcast bias (undershoot, NZ low, ambition≠model, vintage)
│   ├── partA2_findings.md       ← error structure & forecast quality (addition, skill, calibration)
│   ├── partB_findings.md        ← variable selection (coal/CO₂/solar discriminate)
│   └── partC_findings.md        ← filtering, the irreducible floor, Wright cost view
│
├── report/main.tex              ← 2-page LaTeX report
├── data/                        ← observed data (6 variables) + cost series + SCI documentation
│
├── scripts/                     ← all analysis & figure code (run from this folder)
│   ├── partA1_hindcast.py       ← Part A.1: hindcast evaluation (6 vars, weighting, vintage)
│   ├── partA2_diagnostics.py    ← Part A.2: addition test, cross-correlation, autocorrelation
│   ├── partB1_boxplots.py       ← Part B.1: variable selection (box plots)
│   ├── partB2_lasso.py          ← Part B.2: variable selection (LASSO, confirms B.1)
│   ├── analyse_pv_wind_wright_costs_vetted_log.py  ← Part C: Wright's-law cost projection (PV/wind)
│   └── co2_overview.py, co2_benchmark.py, …         ← generators for the figures in the output
│
├── figures/                     ← every figure (pipeline + the ones the output embeds)
│
└── archive/                     ← superseded explorations + narrative_plain.md (early 8-step draft)
```

All scripts write their figures to `figures/` and are meant to be run from inside `scripts/`.

## Naming convention

| Prefix | Content |
|--------|---------|
| `partA1_` | Hindcast error computation (ME, MAE, RMSE) |
| `partA2_` | Error diagnostics (autocorrelation, cross-variable, skill, calibration) |
| `partB1_` | Variable selection — box plots |
| `partB2_` | Variable selection — LASSO |
| `partC_`  | Scenario filtering, the irreducible floor, Wright's-law cost view |

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
