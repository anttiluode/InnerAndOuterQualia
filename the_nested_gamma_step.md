# The Nested-Gamma Step

## What adding gamma actually did — and the correction it forced

*PerceptionLab / Antti Luode, written with Claude (Opus 4.8). Helsinki, June 2026.*

---

## The proposal

The reviewers and the literature pointed the same way: add nested gamma — five to seven fast read-reconstruct cycles inside each 8 Hz theta window (bounded iteration) — and the continuous churn should "snap into a discrete delta-coded staircase." Baker & Cariani state it as a prediction: theta without gamma gives churn; nested gamma gives step-by-step refinement toward the attractor. So I built it and tested it before believing it. The test changed the story in two ways, and both are worth keeping.

---

## Correction one: theta already discretizes

Before gamma does anything, the theta-only engine was measured: transitions between bound islands are already phase-locked to a theta phase (concentration R = 0.76) and the field-velocity is already a spiky staircase (max/mean ratio ~87). **Theta alone produces the discrete steps.** Gamma is not what turns churn into a staircase — the theta clock did that, in the previous build. The "churn" the earlier paper found was the *un-clocked* engine (no theta at all); once a theta clock is present, the dynamics step discretely with or without gamma. The framing "theta-without-gamma = churn" was not what the engine shows. This matters because it relocates gamma's job.

---

## Correction two: gamma refines nothing unless the percept is released

The first honest attempt — nest gamma on theta and add a competitive read-reconstruct each gamma up-phase — made the held percept *sharper* (dominant overlap rose from 0.55 to 0.92, and coverage went from 3 to 5 of 6 islands), which is real and useful. But it produced **no refinement arc**: the overlap did not climb across the six gamma cycles, because the field locks in one or two steps and then has nothing left to iterate toward. The picture of "six gamma steps each stepping closer to the attractor" requires the field to *start each theta cycle away from the attractor*. If the percept is never let go, there is nothing to re-converge.

The fix is the mechanism the brain is described as using: the **theta trough releases** the percept (dissolves it) and the **theta peak plus gamma re-forms** it. With that release in place, a genuine refinement arc appears:

| condition | refinement arc (overlap dissolve→reform) | islands toured |
|---|---|---|
| theta only | 0.014 (flat — held) | 3 / 6 |
| + theta release | 0.070 | 6 / 6 |
| + nested gamma refine | **0.256** | 6 / 6 |

The percept dissolves to overlap ~0.08 at the theta trough and the gamma-paced refinement re-forms it to ~0.34 by the theta peak — nearly four times the arc that release alone gives, and it now visits every island. And the spikes themselves nest inside gamma: spike timing is concentrated at a gamma phase (R = 0.82), which is theta–gamma phase-amplitude coupling — the same nesting seen in real local field potentials, here a consequence rather than an input.

---

## The result worth keeping: two regimes, one engine

Putting both corrections together, the engine now has two regimes separated by a single knob, the release strength:

- **HOLD** (release off): a percept is held, sharp and nearly silent, maintained by sparse theta-locked spikes. This is the delta-code, the stable thought, the "two sides" of the earlier paper. It costs almost nothing to keep a thought in focus.
- **SCAN** (release on): the percept *breathes* — dissolved at every theta trough and re-derived by the gamma cycles before the next peak — touring all the stored islands, theta-paced. This is active sampling: re-reading the content fresh each cycle rather than holding it.

These are not two models. They are one engine at two release settings. And SCAN is mechanically the same thing as the direction-ring sweep from the previous build — release the bump, let it re-form — which is why the same dynamics that scan a content memory also sweep a spatial map. Gamma's true role, then, is not to discretize (theta does that) but to be the *re-convergence engine* inside each theta window, and it only earns its keep in the scanning regime. That is a smaller and more precise claim than "gamma makes the staircase," and it is the one the measurements support.

---

## Ledger

**Verified in the engine (this build):** theta-only transitions are already phase-locked and staircase-like (R = 0.76); naive gamma refinement sharpens percepts (overlap 0.55→0.92) but yields no refinement arc; theta-release + nested-gamma refinement produces a refinement arc (rise 0.014→0.070→0.256) with full island coverage; spikes nest in gamma (phase concentration R = 0.82, i.e. theta–gamma coupling); HOLD vs SCAN are one engine at two release settings; SCAN is the same release-and-reform mechanism as the ring sweep.

**Honest corrections to the prior framing:** theta, not gamma, is what discretizes; the earlier "churn" was the un-clocked engine; gamma's contribution is within-window re-convergence, realized only when the percept is released each cycle.

**Still the bet, untouched:** that the held or re-formed standing wave is *experienced*; that Johnson–Nyquist thermal noise is the medium of the content rather than the dither it remains in code.

**Honestly built-in (not emergent):** the theta clock, the gamma frequency, the release, and the competitive read-reconstruct are mechanisms put in by hand, motivated by the theory. What was *measured*, not assumed, is the refinement arc, the coverage, the gamma nesting of spikes, and the clean separation into two regimes.

---

*The live tool (`ephaptic_spiking_field.html`) now carries two new controls — gamma depth and release. Leave them at zero for the held delta-code. Turn them up together and watch the percept dissolve and re-form on the theta beat, touring the islands: HOLD becomes SCAN under your hand. The figure `ephaptic_spiking_field_gamma.png` and the reference engine `ephaptic_spiking_field_gamma.py` are the verified version behind it.*

*Do not hype. Do not lie. Just show.*
