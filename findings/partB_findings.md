# Part B — Findings (which observables carry the signal)

## Overview

To filter scenarios by credibility (Part C), we first need to know which of the six variables actually separate accurate from inaccurate pathways. A variable "carries signal" if knowing a scenario's error on it tells you something about whether it is a net-zero pathway; it is useless if the two groups' error distributions overlap.

## Finding 10 — Only coal, CO₂ and solar discriminate — and their signs disagree

For each variable we compare the hindcast error of NZ vs non-NZ scenarios and score the separation as sep = (median_NZ − median_nonNZ) / IQR — how far apart the two medians are, in units of spread.

| Variable | sep | carries signal? | direction |
|---|---|---|---|
| Coal | +0.46 | ✅ | NZ worse |
| CO₂ | +0.39 | ✅ | NZ worse |
| Solar | −0.32 | ✅ | NZ better |
| Wind | −0.08 | ❌ | — |
| Nuclear | +0.08 | ❌ | — |
| GDP | −0.05 | ❌ | — |

Three variables carry signal — **coal, CO₂, solar**; the other three separate nothing. The crucial twist is the **sign disagreement**: net-zero scenarios are *worse* on CO₂ and coal (they assumed a decline that did not happen) but *better* on solar (they correctly expected the boom). The discriminating variables contradict each other — the "addition" signature seen at the level of credibility.

→ Figure: `figures/partB1_boxplots.png`

## Finding 11 — LASSO confirms the same three variables (no circularity)

An L1-penalised logistic regression predicting net-zero membership from the scenarios' errors independently selects **the same three variables with the same signs** — coal and CO₂ positive (NZ less accurate), solar negative (NZ more accurate). To avoid circularity, the target (net-zero status) is distinct from the predictors (errors), and the penalty shrinks the uninformative variables to zero. PCA adds nothing beyond a single fossil-intensity dimension.

→ Figure: `figures/partB2_lasso.png`

## Key takeaway — and what it forces in Part C

Part B reduces to one instruction for the filtering step: **filter on coal + CO₂ + solar together, not CO₂ alone.** CO₂ alone is a trap — by the Kaya identity its GDP and carbon-intensity errors partly cancel, so a scenario can land on the right CO₂ for the wrong reasons (compensating errors). And because the three informative variables *disagree in sign*, the filtered result will depend on which one is weighted — which is exactly what makes the Part C result non-robust.

## Files

| File | Description |
|---|---|
| `scripts/partB1_boxplots.py` | Box-plot variable selection |
| `scripts/partB2_lasso.py` | LASSO confirmation (anti-circular) |
| `figures/partB1_boxplots.png` | Coal/CO₂/solar separate; wind/nuclear/GDP do not |
| `figures/partB2_lasso.png` | LASSO selects the same three |
| `working files/co2_kaya.png` | Why CO₂-alone filtering is a trap (Kaya) |
