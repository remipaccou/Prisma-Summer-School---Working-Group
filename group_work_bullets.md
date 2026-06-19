# Group Work — Bullet Points Summary

## Part A1 — Hindcast evaluation

**Le hindcast : ce qu'on fait**
- On compare 1,564 scénarios (65 modèles, 41 projets, 17 familles) aux données observées 2010-2025 sur 6 variables
- ε = observé − projeté. Positif = le scénario a projeté trop peu
- Trois métriques : ME (biais directionnel), MAE (erreur typique), RMSE (pénalise les gros écarts)
- Pondération par famille (1/n_f) pour corriger le déséquilibre de l'ensemble (REMIND + MESSAGE = 44% des scénarios) *(correction de biais d'échantillonnage)*

**L'ensemble sous-estime 2025**
- CO₂ : ε = +2,582 Mt (les modèles projetaient 35,518, la réalité est 38,100)
- Charbon : record 2025 à 164 EJ, médiane ensemble à 140 EJ, 68% des scénarios sont hors de ±10%
- L'erreur 2020 (−1,572) c'est le COVID — choc exogène, excusable
- L'erreur 2025 (+2,582) c'est structurel : les émissions sont revenues sur la tendance pré-COVID, c'est l'ensemble qui avait parié sur un déclin qui n'est pas venu

**Les scénarios NZ divergent davantage du réalisé**
- NZ : ME_j = +607 (projettent systématiquement moins d'émissions que le réalisé)
- Non-NZ : ME_j = −23 (quasi centrés sur la réalité)
- Le gap est significatif *(KS test, p < 10⁻¹⁶)*
- Nuance importante : cela ne signifie pas que les modèles NZ sont "mauvais" — cela signifie que les hypothèses de politique et de transformation embarquées dans les trajectoires NZ ne se sont pas matérialisées sur 2010-2025. C'est un constat sur le monde, pas sur la mécanique des modèles

**Economy models vs energy models**
- Economy (REMIND, WITCH, AIM, GEM-E3, IMACLIM, EPPA, CGEM, MERGE — 8 familles, 701 scénarios) : biais positif persistant +613, structurellement plus optimistes sur la décarbonation *(comparaison de moyennes conditionnelles, pondération par famille)*
- Energy (MESSAGE, IMAGE, POLES, COFFEE, GCAM, TIAM, PROMETHEUS — 7 familles, 883 scénarios) : centrés (−41) mais ratent le COVID plus fort (−2,164 vs −1,264)
- En 2025 les deux se trompent pareil (~+2,600) — le rebond post-COVID est un angle mort partagé

**Le vintage ne sauve pas les modèles récents — il les accable**
- Les scénarios ne partent pas tous du même point d'information : un scénario SSP (2015) projette 2025 à 10 ans ; un scénario ENGAGE (2022) projette 2025 à 3 ans
- Les late (2021+) sont mieux calés en 2010 (MAE 685 vs 1,141) — normal, ils connaissaient la réponse
- Mais ils se trompent PLUS en 2025 (ME +3,280 vs +466) — avec plus d'info et un horizon plus court
- Explication : les projets récents (post-Paris, Green Deal, Glasgow) ont intégré des hypothèses de politique climatique plus ambitieuses qui ne se sont pas matérialisées dans les émissions
- L'ensemble SCI reflète l'agenda de recherche autant que la physique du système

**Le gap NZ vs non-NZ est robuste**
- Persiste quelle que soit la pondération (scenario, model, family)
- Persiste dans chaque vintage (early, mid, late)
- Persiste dans chaque type de modèle (economy, energy)

---

## Part A2 — Diagnostics d'erreur

**Finding 5 — Addition énergétique**
- Les modèles sous-estiment le fossile ET le renouvelable simultanément en 2025
- Charbon : +26 EJ (record non anticipé, médiane ensemble = 140 vs 164 observé)
- Solar PV : +1,004 GW (réalité = 2× la médiane projetée : 2,392 vs 1,169 GW)
- Éolien : +153 GW (sous-estimé aussi)
- Nucléaire : −70 GW (surestimé — les modèles attendaient plus de nucléaire que le réel post-Fukushima)
- GDP : −13,400 B$ (surestimé — les modèles attendaient plus de croissance)
- Le monde ajoute du renouvelable sans retirer le fossile → addition, pas substitution

**Finding 6 — Les modèles pensent en substitution**
- Corr(ε_charbon, ε_solaire) = −0.28 *(Pearson, n ≈ 1,065)* : dans l'ensemble, plus de solaire → moins de charbon
- La corrélation est plus forte chez les NZ (−0.30) que chez les non-NZ (−0.17) — les NZ ont une logique de substitution plus agressive
- Mais le ME est positif pour les deux → la réalité est dans un coin du nuage (haut-droite : beaucoup de fossile ET beaucoup de solaire) où les modèles ne vont pas
- Le constat d'addition vient des ME (les niveaux), le diagnostic de substitution vient de la corrélation (la structure interne des modèles)

**Finding 7 — GDP seul biais structurel**
- Pour CO₂, charbon, solaire, éolien : ρ(2010, 2025) ≈ 0 *(autocorrélation de Pearson)* → l'erreur initiale ne prédit pas l'erreur finale. L'erreur s'accumule en route (hypothèses de trajectoire), pas au départ (calibration)
- Pour GDP : ρ = +0.70 → biais fixé dès le départ et persistant (le GDP est une hypothèse exogène dans la plupart des modèles)
- Conséquence : filtrer sur la précision en 2010 ne sert à rien pour l'énergie (ρ ≈ 0, pas de lien), mais pourrait servir pour le GDP (ρ = 0.70, le biais persiste)

---

## §2.5 — Skill vs naive rule

**Pourquoi on fait ça**
- Tester si l'ensemble apporte de la valeur par rapport à une extrapolation triviale (droite 2010-2015 prolongée) *(forecast skill ratio)*
- Si la droite fait mieux, l'ensemble ne peut pas être considéré comme un forecast utile

**Résultat**
- La règle triviale bat l'ensemble sur 4/6 variables : CO₂ (skill 2.0), charbon (4.7), nucléaire (9.9), GDP (3.0)
- L'ensemble bat la règle sur 2/6 : solaire (0.7), éolien (0.6)
- Ce n'est PAS un fait nouveau : la règle gagne là où la réalité est restée sur tendance et l'ensemble a parié sur une inflexion — même cause que le biais NZ
- L'ensemble gagne sur solaire/éolien car la croissance est non-linéaire (exponentielle) — la droite ne capte pas ça, les modèles oui
- Le cas nucléaire (skill = 9.9) est creux : le nucléaire est passé de 375 à 377 GW en 15 ans, "rien ne change" gagne par construction

**Ce que ça ferme**
- L'argument "l'ensemble est biaisé mais reste un meilleur outil qu'une extrapolation simple" → faux sur 4/6 variables

---

## §2.6 — Calibration (PIT)

**Pourquoi on fait ça**
- Tester si l'ensemble est une distribution calibrée *(PIT — probability integral transform)* — si le réalisé tombe au milieu du nuage, on peut lire P(NZ2070) dedans
- Si le réalisé tombe dans les extrêmes, l'ensemble n'est pas une distribution probabiliste fiable

**Résultat : percentile du réalisé 2025 dans l'ensemble**
- GDP : 1er percentile → l'ensemble surestime massivement le PIB
- Nucléaire : 20ème → surestimé
- CO₂ : 75ème → sous-estimé
- Éolien : 75ème → sous-estimé
- Charbon : 79ème → sous-estimé
- Solaire : 90ème → fortement sous-estimé
- Le réalisé n'est JAMAIS près du 50ème → le nuage est systématiquement décalé

**Limites**
- Un seul point par variable (2025) — diagnostic, pas test PIT formel (il faudrait beaucoup de points à différentes dates)
- 75-79ème c'est le haut du milieu, pas une queue — seuls GDP (1er) et solaire (90ème) sont des cas extrêmes

**Ce que ça ferme**
- L'argument "le 32% est approximatif mais dans le bon ordre de grandeur" → non, l'ensemble n'est pas calibré, on ne peut pas lire de probabilité dedans

---

## Part B — Sélection de variables

**Ce qu'on cherche**
- Sur quelles variables les trajectoires NZ et non-NZ divergent-elles du réalisé ? Lesquelles portent de l'information sur le type de trajectoire ?
- Méthode 1 : box plots + score de séparation sep = (médiane NZ − médiane non-NZ) / IQR *(taille d'effet normalisée, apparenté au Cohen's d)*
- Méthode 2 : LASSO — régression logistique L1 qui calcule P(NZ | erreurs) et élimine automatiquement les variables non-informatives *(modèle de classification probabiliste)*

**Finding 10 — Trois variables discriminent, les trois autres non**
- Coal : sep = +0.46 → les trajectoires NZ supposent un déclin du charbon qui n'a pas eu lieu
- CO₂ : sep = +0.39 → les trajectoires NZ supposent une baisse des émissions qui n'a pas eu lieu
- Solar PV : sep = −0.32 → les trajectoires NZ supposent un boom solaire qui A eu lieu (et même plus)
- Wind : sep = −0.08 → pas de séparation
- Nuclear : sep = +0.08 → pas de séparation
- GDP : sep = −0.05 → pas de séparation

**Finding 11 — Le LASSO confirme exactement les mêmes trois, mêmes signes**
- Coal : coefficient +0.34 (erreur charbon élevée → plus probablement NZ)
- CO₂ : coefficient +0.22 (erreur CO₂ élevée → plus probablement NZ)
- Solar : coefficient −0.18 (erreur solaire faible → plus probablement NZ)
- Wind, Nuclear, GDP : coefficients = 0 (éliminés par la pénalité L1)
- Robuste sur plusieurs niveaux de régularisation (C = 0.05 à 0.3)
- Pas circulaire : la cible (statut NZ) est distincte des prédicteurs (erreurs de hindcast)

**Le twist — les trois variables se contredisent**
- Sur charbon et CO₂ : les hypothèses NZ de déclin du fossile n'ont pas tenu
- Sur solaire : les hypothèses NZ de boom technologique ont tenu (et la réalité les dépasse)
- C'est le finding d'addition vu depuis la crédibilité : les NZ ont raison sur la techno propre, tort sur la sortie du fossile

**Conclusion Part B**
- Ce qui sépare les trajectoires NZ des non-NZ face à la réalité, c'est spécifiquement la vitesse de substitution charbon → solaire. Pas le PIB, pas le nucléaire, pas l'éolien
- Le déploiement solaire va plus vite que prévu (les NZ avaient raison). Le retrait du charbon ne se fait pas (les NZ avaient tort). Le goulot d'étranglement n'est pas le déploiement du propre, c'est le retrait du sale
- On ne peut pas dire "les trajectoires NZ sont crédibles" ni "elles ne le sont pas" — elles sont les deux, selon la variable
- Conséquence pour Part C : filtrer sur une seule variable donne des résultats opposés selon le choix. Il faut filtrer sur les trois ensemble et accepter que le résultat ne soit pas un chiffre unique
- CO₂ seul est un piège (identité de Kaya : les erreurs GDP et intensité carbone se compensent → un scénario peut avoir le bon CO₂ pour de mauvaises raisons)

---

## Fichiers Part A + B

| Fichier | Contenu |
|---|---|
| `scripts/partA1_hindcast.py` | 6 variables, pondération, economy/energy, vintage |
| `scripts/partA2_diagnostics.py` | Addition, corrélation croisée, autocorrélation |
| `scripts/co2_finding1_simple.py` | CO₂ obs vs projections |
| `scripts/nz_bias.py` | NZ vs non-NZ bias |
| `scripts/co2_benchmark.py` | Skill vs trivial rule |
| `scripts/calibration_pit.py` | Calibration PIT |
| `scripts/co2_kaya.py` | Décomposition Kaya |
| `scripts/partB1_boxplots.py` | Box plots + sep |
| `scripts/partB2_lasso.py` | LASSO variable selection |
| `figures/partA1_fig1_by_year.png` | 6 vars × ME/MAE/RMSE par année |
| `figures/partA1_fig2_mae_nz.png` | 6 histogrammes NZ vs non-NZ |
| `figures/partA1_fig3_dashboard.png` | Dashboard NZ + economy + vintage |
| `figures/partA2_fig1_diagnostics.png` | Corrélation + ME 2025 + autocorrélation |
| `figures/co2_finding1_simple.png` | COVID vs structurel |
| `figures/nz_bias.png` | NZ bias |
| `figures/co2_benchmark.png` | Skill vs trivial rule |
| `figures/calibration_pit.png` | PIT percentiles |
| `figures/partB1_boxplots.png` | 6 box plots séparation NZ/non-NZ |
| `figures/partB2_lasso.png` | Coefficients LASSO |
