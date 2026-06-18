# Working files

Dossier de travail / explorations — **séparé du pipeline principal** (`scripts/`, `report/`)
pour ne pas perturber le reste et faciliter le partage.

## Contenu

| Fichier | Description |
|---|---|
| `co2_overview.py` | Génère les deux figures ci-dessous (CO₂, ensemble SCI-2025). |
| `co2_overview.png` | **Vue globale** : toutes les trajectoires CO₂ (2010–2100) + 4 points observés (GCB 2025), horizon complet + zoom sur la fenêtre de hindcast. |
| `co2_views.png` | **Découpages** : all / Net-Zero 2070 / pondéré par modèle (1 modèle = moyenne de ses scénarios) / energy / CGE / hybrid. Chaque panneau annote ME/MAE/RMSE (pondérés par famille, 2010–2025). |

## Choix de classification (energy / CGE / hybrid)

- **energy** (équilibre partiel, PIB exogène) : IMAGE, POLES, COFFEE, GCAM, TIAM, PROMETHEUS
- **CGE** (équilibre général complet) : AIM, GEM-E3, IMACLIM, EPPA, CGEM
- **hybrid** (énergie + croissance macro) : REMIND, WITCH, MESSAGE, MERGE

Les hybrides forment leur propre groupe au lieu d'être rangés arbitrairement d'un côté.

## Lancer

```bash
python "co2_overview.py"   # lit le .xlsx SCI-2025 dans ~/PhD/.../Scenario_Compass_Initiative_Data
```

> Le chemin des données est en dur dans le script (`SCI_DATA`). À adapter selon la machine.
