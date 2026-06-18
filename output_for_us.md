# Output of our thinking — the plain version (for us, not the jury)

This is the project said straight, no jargon, with the numbers we actually use. The formal,
jury-facing version is `working files/narrative_updated.md`; this one is so the three of us hold the
same thread and can present it out loud.

---

## The question

Can the world realistically reach net-zero CO₂ by 2070 — and is the "32% chance" people quote real?

## The one-line answer

**The 32% is not a real probability. The simulations forecast badly (they expected emissions to fall,
they rose). Meanwhile clean tech is getting cheap faster than the models assumed. So the thing
blocking net-zero is not the cost of clean technology — it's that we add clean energy without
removing the dirty. The door to 2070 is opened by technology and held shut by fossil inertia.**

Everything below builds that sentence.

---

## Part 1 — The "32%" is fake

People take the 1,564 simulations, see that 497 reach net-zero by 2070, divide, and call it "32%
chance." It isn't a chance. Three reasons:

1. **It's just a count of what researchers chose to run.** The 3 biggest labs alone produce 28% of
   all simulations. So the number describes their research menu, not the real world.
2. **It moves on its own if you change the deadline.** Net-zero "by 2060" = 16%. "By 2080" = 43%.
   "Ever" = 57%. Slide the date ten years and it doubles. A real probability doesn't do that.
3. **It moves again if you change how you count the simulations.** Give each modelling team one vote
   instead of counting every run: it goes 24% → 31% → 39% depending on the choice.

Two knobs that have nothing to do with the climate (the deadline, the counting) each move the number
by half. → It's not a probability. So we stop trying to "correct the 32%" and instead ask a better
question: *are these simulations even good forecasts?*

## Part 2 — The simulations forecast badly

We checked them against what actually happened, 2010 → 2025:

- **They expected too little CO₂ in 2025.** They assumed emissions would peak around 2020 and start
  falling. Emissions kept rising. (And no — this is not COVID. COVID only explains 2020; by 2025
  emissions were back on their old upward trend.)
- **The net-zero simulations are the most off.** Partly because reaching net-zero by 2070 *forces*
  them to assume an early fall that didn't happen — so they're "too low" almost by definition. So we
  say: *they assumed an early turn that hasn't started*, NOT "net-zero models are bad."
- **A dumb rule beats them.** "Just draw a straight line from 2010-2015" predicts 2025 better than the
  whole ensemble on 4 of 6 variables.
- **Reality always lands on the high-emissions side** of the cloud of simulations.

→ As a forecasting tool, the ensemble is not trustworthy — it points too optimistic.

## Part 3 — What we CAN say (the real conclusion)

- **One thing we forecast well: cost.** Solar went from ~2,440 to ~250 $/kW (2010→2024) and keeps
  falling to ~30-40 by 2070. Clean tech gets cheap no matter what.
- **The world is doing two things at once:** deploying renewables *faster and cheaper* than the models
  thought, AND keeping the coal. Solar capacity in 2025 is **double** what the median model expected —
  yet coal hit a record.
- **So the lock on net-zero is not cost — it's substitution.** We add clean without subtracting dirty.
  The net-zero simulations fail not because they're too optimistic about technology (if anything
  they're too pessimistic) but because they assume a fossil phase-out that isn't happening.

---

## What we honestly CANNOT say (the limits)

- **We can't rule out a late net-zero.** A path that stays flat then crashes after 2030 looks exactly
  like a "no-action" path today. A 15-year check can't tell them apart. So the corrected share can't
  go below ~20% — that floor is real uncertainty, not a number we can sharpen.
- **This is a hindcast, not a real forecast.** All these simulations are from after 2017, so they
  already "knew" part of 2010-2025. The only true test would use older (2014, AR5) simulations — we
  don't have them in this dataset.
- **15 years ≠ 45 years.** Being right to 2025 doesn't guarantee being right to 2070.

## Say this / don't say that (for the defense)

| ✅ Say | ❌ Don't say |
|---|---|
| "The 32% is not a probability — it's a count, and it's unstable." | "We computed the real probability of net-zero." |
| "The simulations assumed an early turn that hasn't begun." | "Net-zero models are wrong / bad." |
| "The corrected share is ~20% under any sensible filter." | "It's anywhere between 20% and 48%." (only the solar-only filter gives 48%, and that filter is a poor choice) |
| "Reality is biased low in the cloud; clearly so for solar and GDP." | "Reality is in the tails for all six variables." (75th–79th is upper-middle, not a tail) |
| "A trivial rule beats it — which restates the optimism, it's a corollary." | "This is independent proof the models have no skill." (it's the same fact; and nuclear's 9.9 is hollow because nuclear is flat) |
| "The barrier is substitution, not technology cost." | "Net-zero by 2070 is impossible." (we don't show that) |

## Numbers to have ready

- 1,564 simulations, 497 net-zero by 2070 → naive 32%.
- Deadline sensitivity: 16% (2060) / 31% (2070) / 43% (2080) / 57% (ever).
- Counting sensitivity: 24% / 31% / 39%.
- CO₂ 2025: observed 38,100 Mt; ensemble ~35,500 → undershoot +2,582 (this survives removing COVID).
- Solar 2025: observed 2,392 GW vs median 1,169 → reality is 2× the models.
- Corrected net-zero share: ~20% under CO₂ or multivariate filtering; ~20% floor from late movers.
- Solar cost: ~2,440 → ~250 $/kW (2010→2024) → ~30-40 by 2070.

## Where Lafond's method fits (one line)

We used his framework as the backbone — treat each simulation as an *if-then* forecast, test whether
the ensemble is calibrated, demand it beat a dumb rule, and build an honest cost forecast (Wright's
law). We did **not** run his heavy statistical machinery, because our data is too short (15 years, a
few points). Saying that openly is a strength, not a weakness.
