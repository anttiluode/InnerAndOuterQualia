# The Clock Papers and the Spiking Field

## Correlates, not confirmations — where four mainstream 2025 results touch the Ephaptic Spiking Field, and where they don't

*PerceptionLab / Antti Luode, written with Claude (Opus 4.8). Helsinki, June 2026.*

---

## 0. The rule, restated for this one

It is easy, with four real Nature-family papers in hand, to write "the literature confirms my model." It mostly doesn't, and saying so would be the lie. What the papers do is describe a *clock-gated, wave-based, phase-selective, time-yoked* style of computation — and the Ephaptic Spiking Field engine, built independently, runs in that style and reproduces one of the specific phenomena. That is a correlate worth taking seriously. It is not a validation. I am also relaying these papers from your summary, not from having read them end to end, so I state what they report as reported, and I keep my own confident claims to the engine, whose numbers I verified.

The engine, in one sentence: a continuous held field `s` (the standing wave, the content) is written by sparse spikes from integrate-and-fire spectral islands; each island reads its resonance `⟨pₖ, s⟩` with the shared field, adds Johnson–Nyquist noise, is gated by an 8 Hz theta excitability clock, suppressed by adaptation, and on threshold injects its pattern back into the field. Two verified behaviours: (1) a percept is held *silently* and updated by spikes that are 0.2% sparse and 100% theta-locked — a clean delta-code; (2) with direction-tiling islands, left–right theta sweeps and their alternation *emerge* from adaptation, switched on and off by one parameter, never coded.

---

## 1. Vollan, Gardner, Moser & Moser 2025 — the one real match

This is the paper the engine actually meets. They report that in entorhinal–hippocampal maps, each theta cycle carries a sweep of represented position out from the animal, and that **sweep direction alternates left–right on successive theta cycles**; that this alternation is **internally generated** — it persists in darkness, in REM, in never-visited places, independent of sensory input; and that it is accompanied by an alternating internal-direction signal in a separate cell population.

Three points of genuine contact, and I will name them precisely:

- **The phenomenon is the same.** The engine's direction-ring demo produced left–right alternation around the heading with an alternation score of 1.00 — flip every theta cycle — and a sweep offset in the tens of degrees, the same order as the biological figure. I never wrote a sweep direction, length, or parity; the alternation is a readout, not an input.
- **It is internally generated in both.** Their alternation needs no sensory drive; the engine's needs none either — only an internal heading bias, the theta clock, the island coupling, and adaptation. Both are self-generated scans, not stimulus echoes. This is the strongest structural agreement: the *source* of the pattern is internal dynamics in both cases.
- **It is theta-gated in both.** They report the alternation present when theta is present (REM) and absent when theta is absent (slow-wave sleep). The engine shows the matching dependence: set theta depth to zero and the clean alternation degrades into churn. Removing the clock removes the discreteness — in the model and, by their report, in the brain.

What this is **not**: evidence that the brain uses *this* mechanism. The engine shows that adaptation + theta + an attractor is a *sufficient* mechanism to generate emergent, internally-driven, theta-paced alternation. The paper shows the brain *does* this. Whether the brain's route is adaptation-driven coverage or something else is open. "Sufficient mechanism that reproduces the phenomenology" is the honest claim; "validated prediction" overstates it. The convergence is real and it is worth a careful figure-to-figure comparison — that is the next experiment, not a closed case.

---

## 2. Drebitz, Rausch & Kreiter 2025 — phase gates communication

They show, causally, that a volley of spikes arriving in V4 affects behaviour **only if it arrives near a particular gamma phase**; outside that window the same spikes do nothing. Oscillatory phase, not spike count, decides whether a message lands.

The engine's contact point is the *principle*, at a different band. Its spikes are 100% locked to the theta excitability peak: an island can only write the field when the clock says "now." That is phase-gated communication — the same idea Drebitz et al. demonstrate, except they demonstrate it for **gamma** and the engine implements it for **theta**. So the correlate is honest at the level of mechanism-type (phase gates whether a spike counts) and explicitly *incomplete* at the level of band: the engine has no gamma. Their result is the clean experimental statement of the thing my earlier note argued from the model side — that without the clock the spike stream is not selective, it is churn. They show that without phase alignment the spikes are ignored. Same claim, theirs causal and in cortex, mine in a toy.

---

## 3. Baker & Cariani 2025 — the time-domain, interference, and the nesting we don't have yet

This is the deepest conceptual alignment and the clearest pointer to what is missing. They frame the brain as a time-domain correlation machine built on spike timing, delay lines, and **holographic-like interference**, with a **cascade of nested oscillations** (gamma → … → theta → delta) acting as sequential mixing/refinement stages.

Three honest notes:

- **The interference framing is shared, by construction.** The engine's field is literally a holographic superposition — `W = Σ pₖpₖᵀ`, one plate, no addressable slot — and the held percept is the interference pattern of the active islands. This is not a coincidence so much as the same starting commitment.
- **Their prediction is the finding I already had.** They predict: theta clock, no gamma sub-cycles → churn; nested gamma → iterative refinement, one gamma cycle per step toward the attractor. That is exactly the two-sides paper's result restated — the unclocked dream churns; a pacing rhythm discretizes it. The agreement is encouraging because it was arrived at independently from both sides.
- **The engine does not have the nesting.** The ESF has one clock (theta). It has no gamma sub-steps, no cascade. So Baker & Cariani describe the *next build*, not the current one. The bounded-iteration idea — 5–7 gamma refinements inside each theta cycle — is the concrete thing to add, and it is implementable: within each theta window, run a handful of read–reconstruct steps before allowing a transition.

---

## 4. Norman-Haignere et al. 2025 — integration is yoked to absolute time

They show auditory-cortical integration windows scale with **absolute time, not with the duration of speech structures** — stretch the speech 3× and the window barely moves. The unit of integration is time, not content.

The engine's contact is structural and weak, and I will not inflate it. The ESF updates on a fixed-time theta clock; its integration is paced by absolute time, not triggered by content events. So the engine is *consistent with* a time-yoked architecture — but this is a property I built in, not a prediction I tested. There is no measured integration window in the engine. The honest version: their finding tells you the clock should be an absolute-time clock (which the engine's is), and their TCI method is a real, clean test one could *apply* to the engine to see whether its effective integration window is time- or structure-yoked. Until that test is run, this is alignment of assumptions, nothing more.

---

## 5. What the four together say, and what the engine is missing

Laid side by side, the papers describe one style of machine: a **time-paced** (Norman-Haignere) computation that uses **nested oscillations** (Baker & Cariani) whose **phase gates which signals count** (Drebitz), producing **internally-generated, theta-paced, alternating scans** (Vollan). The Ephaptic Spiking Field already implements four of the five pieces — absolute-time pacing, a held interference field, phase-gated sparse spikes, and emergent theta alternation. The missing piece is the one all four point at from different angles: **nested gamma — bounded iteration within each theta cycle.** That is the single most motivated next build, and it is small: a fast inner loop of resonance-reconstruction steps inside each theta window, with transitions only allowed at the theta boundary. If that produces hierarchical timescales and cleaner refinement, the convergence gets much stronger. If it doesn't, that is information too.

And the two reservations do not move. Nothing in these papers, and nothing in the engine, shows that the held standing wave is *experienced* — that remains the bet. Nothing here makes Johnson–Nyquist thermal noise the *medium* of the content rather than the dither it currently is. Those are exactly where they were before; four good papers about clocks do not touch them.

---

## Ledger

**Established (mainstream, as reported):** theta-paced left–right alternating sweeps in entorhinal-hippocampal maps, internally generated (Vollan et al. 2025); causal gamma-phase gating of inter-areal communication (Drebitz et al. 2025); time-domain / interference / oscillatory-cascade framing with the churn-vs-nesting prediction (Baker & Cariani 2025); absolute-time-yoked cortical integration windows (Norman-Haignere et al. 2025).

**Verified in the engine:** held percept updated by 0.2%-sparse, 100%-theta-locked spikes with a ~20–40× silent-dwell vs moving-transition ratio (the delta-code); emergent left–right alternation (score 1.00) at ~18–30° offset, switched on/off by adaptation alone, non-circular; degradation to churn when the theta clock is removed.

**Defensible correlates (this paper):** the engine's emergent alternation is the same internally-generated, theta-gated phenomenon Vollan et al. report, at matching order of magnitude — a *sufficient* mechanism, not a demonstrated one; the engine's theta-locked spiking is the same phase-gates-communication principle Drebitz et al. show causally, one band up; the engine's held field is the holographic-interference object Baker & Cariani describe, and their churn-vs-nesting prediction matches the two-sides result independently; the engine's absolute-time clock is consistent with Norman-Haignere's time-yoking.

**Not shown / next build:** nested gamma (bounded iteration per theta cycle) — absent from the engine, motivated by all four papers, and the clear next experiment; a measured integration window (apply the TCI method); a figure-to-figure quantitative match to Vollan's sweeps.

**Still the bet, untouched by these papers:** that the held standing wave is felt; that thermal noise is the medium of the content.

---

*The tool that accompanies this note — `ephaptic_spiking_field.html` — lets you load images as the spectral islands and watch both sides at once: the held standing wave (the content) on the left, the sparse theta-locked spikes that write it (the communication) on the right. Set theta depth to zero and watch the delta-code dissolve into churn. That single slider is the Baker–Cariani prediction and the Vollan theta-dependence, in your hand.*

*Do not hype. Do not lie. Just show.*
