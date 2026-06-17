# PRISMA Summer School 2026 — Group Work (Probabilistic Methods)

## Question

What conclusions can we draw on reaching net zero CO₂ emissions globally by 2070?

## Team

- Lucas Alvarez (Universitat Politècnica de València)
- Matteo Catania (Politecnico di Milano)
- Rémi Paccou (CIRED / Schneider Electric)

Supervisor: François Lafond

## Repository structure

```
├── README.md
├── methodology.md               ← full method description (Parts A/B/C)
├── partA1_findings.md           ← Part A.1 results and observations
├── partA2_findings.md           ← Part A.2 results (addition, correlation, autocorrelation)
│
├── report/
│   └── main.tex                 ← 2-page LaTeX report
│
├── data/
│   ├── observed.xlsx            ← observed data (6 variables × 4 time steps)
│   ├── observed_full.xlsx       ← observed data (annual, multiple sources)
│   └── sci_readme.pdf           ← SCI documentation
│
├── scripts/
│   ├── partA1_hindcast.py       ← Part A.1: hindcast evaluation (6 vars, weighting, vintage)
│   ├── partA2_diagnostics.py    ← Part A.2: addition test, cross-correlation, autocorrelation
│
└── figures/
    ├── partA1_fig1_by_year.png      ← 6×3 grid: all variables × ME/MAE/RMSE by year
    ├── partA1_fig2_mae_nz.png       ← 6 histograms: MAE NZ vs non-NZ
    ├── partA1_fig3_dashboard.png    ← dashboard: NZ + economy/energy + vintage
    └── partA2_fig1_diagnostics.png  ← correlation heatmap + ME bars + autocorrelation
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
