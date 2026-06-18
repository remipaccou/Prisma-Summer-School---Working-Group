# Plan de consolidation — Hindcast des ensembles IAM

*Le document unique pour ne plus se perdre. Tout le projet sur une page.*

---

## La question (reframée)

**Avant :** « en corrigeant pour la précision historique, quelle est la probabilité révisée de net-zéro 2070 ? »

**Après (Lafond, slide 3 — *scenarios = conditional forecasts*) :** un scénario IAM est un *« si la politique suit ce chemin, alors… »*. **On ne peut pas extraire une probabilité inconditionnelle d'un sac de prévisions conditionnelles.** Donc on ne *révise pas une proba* — on **teste si l'ensemble est un forecast calibré**, et on **construit notre propre prévision honnête** des observables.

## Le récit en une phrase

> **L'ensemble SCI n'est pas un forecast calibré — il est trop sûr et biaisé bas. On le montre par la calibration ; on construit un benchmark honnête des observables ; et la vue conditionnelle (Wright) réconcilie l'écart.**

---

## Les 3 livrables (la colonne vertébrale du rapport)

| # | Livrable | Ce que ça montre | État | Fichiers |
|---|---|---|---|---|
| **L1** | **Calibration de l'ensemble (PIT/coverage)** | L'ensemble n'est PAS calibré : la réalité tombe dans les queues (CO₂ 75e, solaire 90e, **PIB 1er percentile**). Remplace ME/MAE/RMSE par la vraie métrique de Lafond. | 🟡 **calculé, manque la figure** | (PIT à tracer) |
| **L2** | **Benchmark honnête** | CO₂ = marche aléatoire à dérive (bat déjà l'ensemble) ; solaire = **courbe de diffusion Bertalanffy-Richards** (pas Moore — corrige le +149%), validé en PIT/coverage. Nos intervalles couvrent le réel là où l'IAM le rate. | ⬜ **à coder (le morceau signature)** | `co2_benchmark.*` (squelette déterministe) |
| **L3** | **Vue conditionnelle (Wright)** | Chaque scénario EST un chemin de déploiement → Wright donne le coût implicite. Way et al. 2022 : l'hypothèse « transition chère » est incohérente avec leur propre déploiement. Relie le mode *addition* au coût. | ⬜ **une diapo** | — |

---

## Part A — la fondation (faite, à ne plus polir)

Diagnostics d'erreur qui *préparent* les 3 livrables. Tout est dans `working files/` :

- **Finding 1** — 2020 = bruit COVID, 2025 = signal structurel (+2 582 survit au détrending). → `co2_finding1*`, `finding1_robustness.md`
- **Gradient d'ambition** — l'erreur 2025 = l'ambition supposée (C1→C8) ; réalité à C6-C7 (monde ~3-4°C). → `co2_2025_ambition.*`
- **Kaya** — l'erreur CO₂ = optimisme de **découplage** (PIB +14%, intensité −18%), pas de croissance. → `co2_kaya.*`
- **Benchmark naïf** — une règle bat l'ensemble sur 4/6 variables (jusqu'à 95% des scénarios). → `co2_benchmark.*`
- **Addition not substitution** — réalité = plus de charbon ET de solaire (72% des scénarios). C'est le mécanisme.
- **Vintage** — effet réel mais partiel ; le split energy/economy y est confondu. → `co2_vintage.*`

## Part C — objet secondaire (PAS le cœur)

**Sensibilité de la PART net-zéro au filtrage** (pas « la proba révisée »). La part NZ va de **20% à 48%** selon la variable de crédibilité (CO₂ ⬇️, solaire ⬆️) → **non-robustesse = slide 3 prouvé.** → `partC_sensitivity.*`, `partC_findings.md`

**Part B se fond dans C :** on filtre **multivarié (CO₂+charbon+solaire)** parce que le CO₂ seul est piégé (Kaya). Pas besoin de LASSO/PCA.

---

## Ce qu'on coupe

- ❌ **PCA/SVD** — ne change rien, annexe au mieux.
- ❌ **Energy vs economy (Finding 3)** — ne mord pas à 2025, confondu avec le millésime.
- ⚠️ **LASSO** — léger seulement, et **piège de circularité** (régresser l'erreur CO₂ sur la projection CO₂). Si on le fait : prédire l'erreur *tardive* avec des variables *précoces*.
- ✅ **Box plots** — garder, cheap et visuel.

## Réserves de faisabilité (à dire, pas cacher)

- **15 ans / 4 points** → on prend **l'esprit de Lafond** (calibration, intervalles honnêtes, B-R sur le solaire annuel), pas la machinerie poolée (surrogate datasets, origines roulantes).
- **Wright (slide 23)** : difficile de prouver qu'il bat Moore → le présenter comme la *vue pertinente pour la politique*, pas « la vérité ».
- **Asymptote L du solaire inconnue** → la prévision B-R y sera sensible. À déclarer.
- **p-values naïves gonflées** (KS p<10⁻¹⁶) par la dépendance sérielle (slide 11) → une phrase suffit.

---

## Prochain pas

1. **L1** — tracer la figure PIT/calibration (les chiffres existent). *Cheap.*
2. **L2** — coder le solaire **Bertalanffy-Richards** + backtest PIT. *Le morceau différenciant.*
3. **L3** — une diapo Wright/Way et al.
4. Écrire les 3 paragraphes de cadrage dans `methodology.md` (§3.1, §5, §5.2).
