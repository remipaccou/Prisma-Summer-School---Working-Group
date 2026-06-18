# Working files

Dossier de travail / explorations — **séparé du pipeline principal** (`scripts/`, `report/`)
pour ne pas perturber le reste et faciliter le partage. Tout porte sur la variable
**CO₂ (Energy & Industrial Processes)**, ensemble SCI-2025.

## 1. Vue globale & découpages — `co2_overview.py`

| Figure | Description |
|---|---|
| `co2_overview.png` | Toutes les trajectoires CO₂ (2010–2100) + 4 points observés (GCB 2025) : horizon complet + zoom sur la fenêtre de hindcast. |
| `co2_views.png` | Découpages : all / Net-Zero 2070 / pondéré par modèle (1 modèle = moyenne de ses scénarios) / energy / CGE / hybrid. Chaque panneau annote ME/MAE/RMSE pondérés par famille (2010–2025). |

## 2. Test sur archétypes — `co2_archetypes.py`

Restreint à quelques modèles « purs » pour réduire la dispersion intra-groupe :
- **ENERGY** (bottom-up, PIB exogène) : POLES, TIAM, COFFEE
- **ECONOMY** (CGE + hybrides) : GEM-E3, IMACLIM, WITCH

| Figure | Description |
|---|---|
| `co2_archetypes.png` | Un panneau par modèle (dispersion intra-modèle visible) + métriques. |
| `co2_archetypes_summary.png` | ME par année (energy vs economy) + barres ME/MAE/RMSE de groupe. |

**Résultat** : tendance énergie **sur-projette** (ME ≈ −715), économie **sous-projette** (≈ +655),
mais forte dispersion → suggestif, non concluant.

## 3. Analyse millésime — `co2_vintage.py`

Croise l'**année de publication** (`Scientific Manuscript`, proxy du millésime / année de base)
avec l'erreur de hindcast.

| Figure | Description |
|---|---|
| `co2_vintage.png` | MAE par année selon le millésime (gauche) + composition en millésimes des 6 archétypes (droite). |

**Points clés**
- Un scénario récent « prédisant » 2020 ne prédit rien : 2020 est de l'**historique** pour lui.
- Effet réel mais partiel (les modèles ne sont pas harmonisés sur les obs GCB).
- ⚠️ **Confusion** : le split energy/economy est corrélé au millésime (IMACLIM = 100 % ≥2024).
  → pour conclure, il faut **comparer à millésime égal** ou scorer chaque scénario seulement
  **après son année de base** (vrai out-of-sample).

## 4. Finding 1 — couche soutenance — `co2_finding1.py`

Sépare le **2020 contaminé COVID** du **2025 structurel** (le vrai signal).

| Figure / fichier | Description |
|---|---|
| `co2_finding1.png` | Gauche : modèles culminent ~2020 et déclinent vs réalité qui plonge (COVID) puis remonte sur tendance. Droite : décomposition du ME — 2020 = COVID (robuste à 2 contrefactuels : +378 / +1 028), 2025 = +2 582 structurel. |
| `finding1_robustness.md` | Tous les chiffres de robustesse : détrend COVID, sensibilité pondération (famille/projet), sensibilité seuil NZ (16→57%), signature addition (marges vs jointe), réconciliation 1591/1564. |

**À retenir** : 2020 = bruit COVID (à détrender), 2025 = signal d'optimisme (à garder).
C'est le chiffre porteur, et il survit au détrending.

## 5. 2025 — rebond, ambition, benchmark naïf

| Fichier | Description |
|---|---|
| `co2_finding1_simple.py/.png` | Version pédagogique du Finding 1 (modèles vs réalité + barres COVID/structurel). |
| `co2_2025_ambition.py/.png` | ME 2025 par catégorie climatique AR6 : gradient C1→C8 ; la réalité tombe à C6-C7 (monde « <3-4°C »). |
| `co2_benchmark.py/.png` | Test de benchmark naïf (Lafond/Farmer) : pour 4 variables sur 6, une règle triviale bat l'ensemble (jusqu'à 95 % des scénarios battus). |
| `benchmark_findings.md` | Note : rebond≠tendance, gradient d'ambition, benchmark, piste AR5. |

## 6. Part C — sensibilité de la part net-zéro (le résultat du projet)

| Fichier | Description |
|---|---|
| `partC_sensitivity.py/.png` | La « part NZ corrigée » n'est pas robuste : 20%→48% selon la variable de filtrage (CO₂ ⬇️ vs solaire ⬆️). Lafond slide 3 : pas de proba inconditionnelle depuis des prévisions conditionnelles. |
| `co2_kaya.py/.png` | Décompo de Kaya : l'erreur CO₂ = optimisme de découplage (PIB +14%, intensité −18%), pas de croissance → pourquoi filtrer sur le CO₂ seul est piégé. |
| `partC_findings.md` | Le reframe, le résultat (non-robustesse), le mécanisme, les prochaines étapes (calibration, Bertalanffy-Richards, Wright). |

## Classification energy / CGE / hybrid

- **energy** : IMAGE, POLES, COFFEE, GCAM, TIAM, PROMETHEUS
- **CGE** : AIM, GEM-E3, IMACLIM, EPPA, CGEM
- **hybrid** : REMIND, WITCH, MESSAGE, MERGE

## Lancer

```bash
python "co2_overview.py" && python "co2_archetypes.py" && python "co2_vintage.py"
```

> Chemin des données en dur (`SCI_DATA`) → lit le `.xlsx` SCI-2025 dans
> `~/PhD/.../Scenario_Compass_Initiative_Data`. À adapter selon la machine.
