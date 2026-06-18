# 2025 — rebond, ambition, et benchmark naïf

Trois analyses liées qui répondent à « d'où vient l'erreur 2025 et que vaut l'ensemble ».

## 1. Le « surplus 2025 » n'est pas un rebond — c'est la tendance qui reprend

| 2025 | valeur |
|---|---|
| tendance pré-COVID extrapolée | 39 400 |
| réalité | 38 100 (−1 300 *sous* la tendance) |
| modèles (moyenne fam.) | 35 518 (−3 882 sous la tendance) |

La réalité 2025 est *sous* sa trajectoire pré-COVID → pas de rebond exceptionnel à expliquer.
Le +2 582 vient à ~75 % de l'hypothèse de **déclin** des modèles, pas d'un choc.

## 2. La précision 2025 = l'ambition supposée, pas le modèle — `co2_2025_ambition.py`

ME 2025 par catégorie climatique AR6 : gradient quasi monotone.

| C1 (1.5°) | C2 | C3 | C4 | C5 | C6 (<3°) | C7 (<4°) | C8 (>4°) |
|---|---|---|---|---|---|---|---|
| +8 353 | +4 229 | +4 377 | +2 355 | +1 530 | +720 | −2 005 | −6 481 |

La réalité tombe entre **C6 et C7** = un monde « <3-4°C, faible action ». Les scénarios qui
« prévoient bien » 2025 sont ceux qui supposaient peu de décarbonation.

⚠️ En partie tautologique (un C1 *doit* décarboner tôt → CO₂ 2025 bas). Le résultat
non-tautologique = **où tombe la réalité** (C6-C7).

## 3. Benchmark naïf — l'ensemble bat-il une règle ? — `co2_benchmark.py`

Prévision de 2025 avec l'info **2010-2015** (pré-COVID). skill = |err ensemble| / |err règle|.
skill > 1 → la règle gagne. « % battus » = part des scénarios pires que la règle.

| Variable | err ensemble | err règle | skill | % scénarios battus |
|---|---|---|---|---|
| CO₂ | 7 % | 3 % (linéaire) | **2.0** | 81 % |
| Charbon | 14 % | 3 % (linéaire) | **4.7** | 91 % |
| Nucléaire | 16 % | 2 % (random walk) | **9.9** | 95 % |
| PIB | 11 % | 4 % (linéaire) | **3.0** | 77 % |
| Solar PV | 51 % | 75 % (linéaire) | 0.7 | 6 % |
| Éolien | 17 % | 30 % (linéaire) | 0.6 | 34 % |

**4 variables sur 6 : une règle triviale bat l'ensemble entier** (jusqu'à 95 % des scénarios
battus). Sur PV/éolien l'ensemble gagne mais reste massivement faux (51 % sur le PV) → c'est là
qu'il faut une méthode dédiée (**loi de Wright / Farmer-Lafond**, cf. Part C2).

**Caveats** : une seule année cible (2025) → « % battus » est la stat robuste, pas le skill sur 1 point.
Règle entraînée sur 2 points (2010, 2015). Pour le PV, le log-trend explose (7 311) : ni naïf ni
ensemble ne captent l'exponentielle.

## Piste suivante (collègue / François) : AR5 vs AR6

Ce dataset n'a **aucun scénario AR5** (publi la plus ancienne = 2017, lignée AR6). Pour un vrai
test out-of-sample long-horizon (scénarios 2014 prévoyant 2025), il faut la base externe
**IIASA AR5 Scenario Database**. Très intéressant car c'est le seul vrai test de prévision.
