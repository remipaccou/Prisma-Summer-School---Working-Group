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
├── methodology_draft.md         ← full method description (Parts A/B/C)
│
├── report/
│   └── main.tex                 ← 2-page LaTeX report
│
├── data/
│   ├── observed.xlsx            ← observed data (CO₂ + Coal, 4 time steps)
│   ├── observed_full.xlsx       ← observed data (annual, multiple sources)
│   └── sci_readme.pdf           ← SCI documentation
│
├── scripts/
│   ├── partA1_co2_errors.py     ← Part A.1: error computation (ME, MAE, RMSE)
│   ├── partA1_co2_errors.ipynb  ← Part A.1: interactive notebook
│   └── partA1_co2_weighted.ipynb
│
└── figures/
    ├── partA1_fig_co2_3x3.png   ← 3×3 grid (ME/MAE/RMSE × 3 views)
    └── ...
```

## Naming convention

### Prefixes by section

| Prefix | Method §  | Content |
|--------|-----------|---------|
| `partA1_` | §3.1–3.3 | Error computation (ME, MAE, RMSE) |
| `partA2_` | §3.4     | Error diagnostics (autocorrelation, cross-variable) |
| `partB1_` | §4.2     | Variable selection — box plots |
| `partB2_` | §4.3     | Variable selection — LASSO |
| `partC1_` | §5.1     | Scenario filtering and revised P(NZ2070) |
| `partC2_` | §5.2     | PV forecast (logistic + Wright's law) |

### File types

| Location | Naming | Example |
|----------|--------|---------|
| `scripts/` | `partXY_description.py` or `.ipynb` | `partA1_co2_errors.py` |
| `figures/` | `partXY_fig_description.png` | `partA1_fig_co2_3x3.png` |
| `data/` | descriptive name | `observed.xlsx` |

## Configuration

Each user must set their local path to the SCI data files:

```python
SCI_DATA = Path.home() / 'PhD' / '4. Modeling' / 'Prisma School' / 'Scenario_Compass_Initiative_Data'
```

SCI xlsx files are NOT in the repo (too large). Download from [SWITCHdrive](https://drive.switch.ch/index.php/s/8CAZ2vDfUVwGhYX?path=%2FGroup%20Work%2F_Scenario_Compass_Initiative_Data).
