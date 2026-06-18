# Part C — la « part net-zéro corrigée » n'est pas robuste

## Le reframe (Lafond, slide 3 : « scenarios = conditional forecasts »)

Un scénario IAM est une prévision **conditionnelle** (« si la politique suit ce chemin, alors… »).
On ne peut pas fabriquer une probabilité **inconditionnelle** en comptant des prévisions
conditionnelles. Donc le naïf `497/1564 ≈ 32%` n'est pas une probabilité, et « réviser
P(NZ2070) » est mal posé. On rebaptise : **sensibilité de la PART net-zéro au filtrage de crédibilité.**

## Le résultat : la part NZ n'est même pas directionnellement robuste

En gardant les scénarios les plus précis sur 2010-2025, la part net-zéro va dans des sens
**opposés** selon la variable de crédibilité (naïf = 34%, n=1205 avec CO₂+charbon+solaire) :

| Filtre (garder 25% plus précis) | Part NZ |
|---|---|
| **CO₂** | **19%** ⬇️ |
| équilibré (CO₂+charbon+solaire, rangs) | 22% ⬇️ |
| **Solaire** | **48%** ⬆️ |

→ La « part NZ corrigée » peut valoir **n'importe quoi entre 20% et 48%** selon un choix de
variable *défendable*. **Cette non-robustesse EST le résultat** (= slide 3 prouvé empiriquement).

## Le mécanisme (précision NZ vs non-NZ, MAE normalisée)

| Variable | NZ | non-NZ | |
|---|---|---|---|
| CO₂ | 0,063 | 0,048 | NZ **moins** précis |
| Charbon | 0,117 | 0,089 | NZ **moins** précis |
| Solaire | 0,340 | 0,401 | NZ **PLUS** précis |

La réalité a donné **raison aux NZ sur le solaire** (ils ont prévu le boom) et **tort sur le
CO₂/charbon** (pas de décarbonation). C'est la **signature « addition »** au niveau de la crédibilité :
filtrer sur ce que les NZ ont raté (CO₂/charbon) les élimine ; filtrer sur ce qu'ils ont réussi
(solaire) les garde. → `co2_kaya.png` montre la version « pourquoi le CO₂ seul est piégé »
(erreurs PIB/intensité qui se compensent).

## Conséquence pour le rapport

- Garder la figure `partC_sensitivity.png`, **étiquetée « sensibilité de la part », pas « probabilité ».**
- Le filtre **CO₂ seul est trompeur** (Kaya) → c'est la Part B en une phrase : filtrer multivarié.
- Prochaine étape (cours Lafond) : (1) calibration de l'ensemble (PIT/coverage), (2) benchmark
  honnête (CO₂ marche aléatoire ; solaire courbe de diffusion **Bertalanffy-Richards**, pas Moore),
  (3) vue conditionnelle (Wright sur le déploiement de chaque scénario).
