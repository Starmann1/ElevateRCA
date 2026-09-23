# PHASE 2 — DIAGNOSTIC FOUNDATION

### *KONE Elevate — Autonomous Fault Isolation & Root Cause Analysis: Master Research Book*

## How to Read This Chapter

Labels used throughout: **[PROJECT SOURCE]** (from the idea proposal or research roadmap), **[ESTABLISHED INDUSTRIAL KNOWLEDGE]** (standard fault/alarm/diagnostic engineering, true across industrial control systems generally — this is the label for most of this chapter), **[EXTERNAL RESEARCH]**, **[ENGINEERING INFERENCE]**, **[ASSUMPTION]**, and **[NOT PUBLICLY ESTABLISHED]**. No proprietary KONE fault-code definitions, controller behavior, or fault-code-to-component mappings are invented anywhere in this chapter — where the real answer is KONE-internal, it is called out explicitly as a Research Gap rather than guessed.

**The central question of this chapter:** *if an elevator reports a fault, what exactly does that fault tell us — and what does it NOT tell us?*

**The governing principle:** **fault code ≠ root cause.**

---

## From Phase 1 to Phase 2

Phase 1 built this causal chain: **Component → Failure → Physical effect → Observable symptom → Sensor evidence.** It stopped at the sensor. Phase 2 extends the chain past the sensor, into the machine's own interpretation of what it's seeing:

**Component → Failure → Physical effect → Sensor evidence → Controller interpretation → Event → Alarm/Fault → Diagnostic investigation.**

Using the example that ran through both of Phase 1's electrical chapters: *[ESTABLISHED INDUSTRIAL KNOWLEDGE]*

```
Mechanical obstruction
        ↓
Increased resistance to motion
        ↓
Increased required motor torque
        ↓
Increased motor current
        ↓
Drive's current sensor reads an abnormal value
        ↓
Drive's internal logic classifies this against a threshold      ← NEW in Phase 2
        ↓
"Overcurrent" event is logged                                    ← NEW in Phase 2
        ↓
Overcurrent alarm is raised; possible drive trip                 ← NEW in Phase 2
        ↓
Possible secondary position/leveling/safety events                ← NEW in Phase 2
```

Everything below the "sensor evidence" line is new territory for this project's reasoning: it's where a physical fact becomes a piece of *machine-generated language* — a code, a severity level, a timestamped log entry — that a human or an AI system then has to interpret. That act of interpretation is where this chapter, and ultimately this whole project, lives.

> **Why This Matters to KONE Elevate RCA:** Everything the RCA Agent will ever see as "input" sits at or below this line — event logs, alarm codes, fault records. It will never directly observe the physical obstruction itself. Understanding exactly how much (and how little) information survives the journey from physical cause to logged alarm is the entire justification for evidence-based reasoning over fault-code lookup.

---

## 4.1 What Exactly Is a Fault?

These terms are used almost interchangeably in casual conversation and are **not** interchangeable in a diagnostic system. *[ESTABLISHED INDUSTRIAL KNOWLEDGE]*

| Term | Meaning | Typical Trigger | Typical System Response | Diagnostic Meaning |
|---|---|---|---|---|
| **Abnormal condition** | A physical/electrical state outside expected range | A physical cause, whether or not anything has noticed yet | None yet — may be entirely undetected | The starting point; not yet "known" by the system |
| **Symptom** | An observable effect indicating an underlying problem | An abnormal condition beginning to manifest | May or may not be logged | Points toward a problem without naming it |
| **Event** | A discrete, timestamped occurrence the system records | Any state change, benign or not | Logged | The broadest, most neutral unit of evidence |
| **Fault** | A *detected* deviation from correct/expected behavior | An abnormal condition crossing a defined detection threshold | Logged, usually with a fault code | The system's own claim that something is wrong |
| **Failure** | Loss of a component's ability to perform its function | A fault that reflects a genuine, often lasting, physical breakdown | Logged; may restrict operation | A stronger claim than "fault" — implies the underlying cause is real and persistent, not necessarily true of every fault |
| **Malfunction** | Operating, but incorrectly | Similar to fault; often used more loosely, including partial/intermittent deviations | Varies | Overlaps with fault/failure |
| **Warning** | A lower-severity alert: trending toward abnormal | A deviation that hasn't yet crossed a critical threshold | Logged; usually no operational restriction | Early evidence, often ignorable in isolation, valuable in aggregate |
| **Alarm** | A signal raised because a defined abnormal condition was detected | A fault crossing an alarm-worthy severity threshold | Logged, surfaced for attention | Requires investigation |
| **Trip** | An automatic protective *action* | A fault judged unsafe or damaging to continue operating through | Motion/operation stopped automatically | Evidence that the system judged the condition serious, not just present |
| **Shutdown** | Cessation of operation (of the elevator or a subsystem) | Could be a trip, or a controlled/commanded stop | Operation ceases | Broader term than "trip" — includes non-protective stops |
| **Safety activation** | Triggering of an independent, hardware-level safety-chain component | A condition the safety chain itself is designed to catch | The specific safety mechanism engages (see §4.7-G) | The most severe category — always requires qualified human verification before service resumes |

A concrete progression, using a slowly-degrading photo-eye as the example: it can begin drifting (**abnormal condition**) with nothing detecting it yet; a technician or a sensitive monitoring system might notice occasional instability (**symptom**); the controller logs each reopening (**event**); once instability crosses a defined frequency threshold, the controller may classify it as a **fault**; if severity or frequency is high enough, an **alarm** surfaces it for attention; the door system does not typically **trip** the whole elevator over this alone, but if it prevents the safety circuit from ever confirming "locked," the drive is inhibited — which is a consequence of the fault, not a separate escalation step.

> **Why This Matters to KONE Elevate RCA:** The RCA Agent's evidence retrieval needs to know which of these categories a given piece of logged data actually belongs to — a warning and a trip carry very different diagnostic weight, even when they reference the same underlying component.

## 4.2 Fault Code vs. Alarm vs. Event

*[ESTABLISHED INDUSTRIAL KNOWLEDGE throughout this section]* Industrial control systems — elevators included — log far more than what a technician would call "a fault." Event logs typically capture ordinary state transitions (door opened, car departed floor 3, normal stop) alongside abnormal ones, because **the boundary between "interesting" and "not interesting" often isn't clear until later**, once a pattern emerges. This is exactly why historical logs matter for diagnosis: a sequence of individually-unremarkable events can, in hindsight, be the earliest evidence of a developing problem.

Faults themselves come in several behavioral flavors, distinguished by how they recur over time:

- **Transient faults** — occur once, briefly, and clear on their own.
- **Persistent faults** — remain present and detectable as long as the underlying cause remains.
- **Intermittent faults** — appear and disappear unpredictably, often tied to a marginal or condition-dependent cause (covered in depth in §4.13).
- **Recurring faults** — the same fault code reappears repeatedly over time, whether or not any single occurrence persists.
- **Latched faults** — remain flagged/active even after the triggering condition clears, until explicitly reset (a deliberate design choice, usually for safety-relevant conditions, so a momentary problem isn't silently forgotten).
- **Self-clearing faults** — automatically clear once the triggering condition resolves, with no reset required.
- **Historical faults** — no longer active, but preserved in the event log for later review.

> **Why This Matters to KONE Elevate RCA:** Whether a fault is latched, self-clearing, or historical changes what "the fault is still present" even means at the moment a technician (or the RCA Agent) begins investigating — which is one more reason a fault's *current state* cannot be read in isolation from its *log history*.

## 4.3 Hard Fault vs. Soft Fault

*[ESTABLISHED INDUSTRIAL KNOWLEDGE]*

| Fault Type | What Happens Physically | What the Controller Observes | What a Technician Might See On-Site | Evidence Remaining After the Event |
|---|---|---|---|---|
| **Hard fault** | An ongoing, genuine physical/electrical problem | Consistent detection every time the condition is checked | Reproducible — the fault is still present and verifiable | Strong — the cause is still there to inspect |
| **Soft / transient fault** | A momentary deviation (e.g., a brief power dip, an unusual but non-faulty event) | Logged once, may or may not meet an alarm threshold | Often nothing at all — condition has already resolved | Weak — limited to whatever was logged at the moment |
| **Intermittent fault** | A marginal condition that only manifests under specific circumstances (temperature, vibration, load) | Recurs unpredictably in the log | Frequently unreproducible on demand | Scattered across many log entries over time — individually weak, collectively strong |
| **Recoverable fault** | A condition the system can safely reset from once cleared | Logged, then cleared (manually or automatically) | Elevator returns to service without physical repair | The reset event itself, plus whatever preceded it |
| **Non-recoverable fault** | A condition requiring physical intervention before safe resumption | Logged, operation remains restricted until addressed | Fault persists through any reset attempt | Strong — repeated failed-reset attempts are themselves informative |

**Why an intermittent fault might vanish before the technician arrives:** many of the conditions that trigger intermittent faults — a specific temperature range, a specific vibration pattern under load, a marginal connector that only opens under thermal expansion — are simply not present at the moment of a scheduled inspection. The elevator may behave completely normally during the visit, which is not evidence the problem is gone; it is evidence the triggering condition wasn't present *right then*. This is precisely why historical telemetry — not just present-moment inspection — is essential evidence for this category of fault.

> **COMMON MISCONCEPTION:** "If the technician can't reproduce it, it isn't a real fault." Intermittent faults are frequently the most serious category precisely because they resist easy reproduction — dismissing them for that reason is a diagnostic failure mode in its own right (see §4.18, item 10).

> **Why This Matters to KONE Elevate RCA:** Distinguishing hard from intermittent faults changes what "sufficient evidence" even looks like — a hard fault can be confirmed by present-moment inspection; an intermittent one can often only be confirmed by pattern-matching across historical events, which is a fundamentally different evidence-gathering task.

## 4.4 Fault Severity and System Response

*[ESTABLISHED INDUSTRIAL KNOWLEDGE — presented as a conceptual industry framework, not a claim about any specific manufacturer's exact implementation]*

```
Normal
   ↓
Deviation          (measurable, but not yet flagged)
   ↓
Warning            (flagged, low urgency)
   ↓
Alarm              (flagged, requires attention)
   ↓
Fault              (confirmed abnormal condition, may restrict operation)
   ↓
Trip / protective shutdown   (automatic protective action taken)
```

Real systems — including, presumably, KONE's, though this book does not claim to know its exact internal labeling **[NOT PUBLICLY ESTABLISHED]** — may compress or relabel these tiers, but the underlying idea is close to universal in industrial control: **severity governs response, and response governs impact.** A low-severity deviation might only ever appear in a log a technician reviews later; a trip-level fault takes the elevator out of service immediately. Severity influences:

- **Elevator availability** — whether the car keeps running at all.
- **Service impact** — degraded performance vs. complete unavailability.
- **Technician priority** — which alarms get dispatched on immediately vs. queued for the next scheduled visit.
- **Diagnostic urgency** — how quickly evidence needs to be gathered before it's lost (relevant especially for transient/intermittent faults).
- **Safety response** — whether independent, hardware-level protection is involved (§4.7-G).
- **Escalation** — whether a recurring lower-severity pattern should itself trigger a higher-priority response, even though no single occurrence crossed the trip threshold.

> **Why This Matters to KONE Elevate RCA:** Severity is itself evidence. A pattern of repeated low-severity warnings that never individually escalate can still be a strong diagnostic signal of a developing problem — arguably a more useful one than a single hard trip, because it carries a *trend*, not just a snapshot.

## 4.5 Primary vs. Secondary (Consequential) Alarms

This is the single most consequential distinction in the entire chapter, because it directly determines what "the problem" even means.

**Primary fault** — the initiating abnormal condition; the thing that, if corrected, would prevent the entire episode from recurring.

**Secondary (consequential) alarm** — a later abnormal condition *caused by* the initiating event, not an independent problem in its own right.

Consider this timeline, built from a realistic elevator event log: *[PROJECT SOURCE — this exact sequence is used in the Master Research Roadmap]*

```
10:31:01   Motor overcurrent
10:31:02   Drive trip
10:31:03   Leveling fault
10:31:04   Safety trip
```

**Are these four independent failures, or four observations generated by one initiating fault?**

Read causally, one plausible reconstruction is:

```
10:31:01  Something (e.g., a mechanical obstruction) forces the motor
          to draw abnormal current.  →  MOTOR OVERCURRENT logged.
                    ↓
10:31:02  The drive's protective logic reacts to the overcurrent
          condition by cutting motor power.  →  DRIVE TRIP logged.
                    ↓
10:31:03  Because motion stopped abruptly, mid-travel, the car is no
          longer at a recognized, leveled floor position.
          →  LEVELING FAULT logged.
                    ↓
10:31:04  Because the car is not in a confirmed safe/leveled state,
          the system does not permit normal operation to resume.
          →  SAFETY TRIP logged.
```

Under this reading, there is **one** thing to actually fix (whatever caused the overcurrent at 10:31:01), and the other three alarms are downstream evidence of that same event — not three additional problems requiring three additional repairs. This is why the primary/secondary distinction changes the diagnostic conclusion so dramatically: treating all four as independent could lead a technician (or an AI system) to investigate — and potentially replace parts on — three subsystems that are, in fact, functioning exactly as designed in response to the real, single problem upstream.

> **DIAGNOSTIC INSIGHT:** A short time window between alarms is *suggestive* of a shared cause, but it is the physical plausibility of the causal chain — does an overcurrent-triggered trip actually explain a leveling fault? — that turns a temporal coincidence into a credible primary/secondary relationship. §4.12 returns to this distinction in more depth.

> **Why This Matters to KONE Elevate RCA:** This is precisely the reasoning the project's "alarm correlation" stage is designed to formalize — grouping a set of temporally-close alarms into a single fault episode, and then identifying which member of that group is the primary event, is the direct engineering translation of the reasoning walked through above.

## 4.6 The Fault Cascade

A **fault cascade** is the general pattern behind the timeline above: a root physical problem propagates through the system, each stage producing effects that the next stage detects and reacts to, generating a chain of alarms from a single origin.

```
Root physical problem
        ↓
Subsystem abnormality
        ↓
Sensor deviation
        ↓
Controller detection
        ↓
Protective action
        ↓
Secondary system effects
        ↓
Additional alarms
```

**Example 1 — Mechanical obstruction**
Obstruction → increased load → motor current rises → drive detects overcurrent → drive trip → motion stops → car not at a recognized floor position → leveling-related event.
*Initiating fault:* the obstruction. *Intermediate effects:* elevated torque demand, elevated current. *Final alarms:* overcurrent, drive trip, leveling event. *Possible misleading interpretation:* treating the leveling event as an independent encoder or leveling-system problem.

**Example 2 — Encoder feedback failure**
Encoder degrades → incorrect speed/position feedback reaches the controller → controller detects a mismatch between commanded and actual behavior → motion-control fault → leveling deviation → protective response if the mismatch is severe enough.
*Initiating fault:* the encoder. *Intermediate effects:* control-loop miscorrection, degraded motion quality. *Final alarms:* motion-control fault, leveling deviation. *Possible misleading interpretation:* treating the leveling deviation as a rope-stretch or brake-timing issue (§3.3) rather than tracing it back to the feedback source.

**Example 3 — Door problem**
Door issue (e.g., photo-eye drift) → repeated reopening → excessive door-cycle duration → door timeout → elevator effectively unavailable, even though the drive, motor, and traction system are entirely healthy.
*Initiating fault:* the door subsystem. *Intermediate effects:* repeated failed close attempts. *Final alarms:* door timeout, potentially safety-circuit-open and drive-start-inhibited downstream. *Possible misleading interpretation:* investigating the drive or safety circuit directly, since that's where the elevator visibly "stopped working," when the actual cause never left the door subsystem.

> **Why This Matters to KONE Elevate RCA:** Three different subsystems, three structurally identical cascade patterns. Recognizing the *pattern* — root cause, propagation, multiple downstream alarms — rather than memorizing subsystem-specific rules is what lets a fault-isolation system generalize to fault types it hasn't seen a labeled example of before.

## 4.7 Elevator Fault Categories

A working taxonomy, drawn from the roadmap's own list. *[PROJECT SOURCE + ESTABLISHED INDUSTRIAL KNOWLEDGE]* Each category is characterized at the level needed to route an alarm to the right investigation, not re-derived in full (the deep-dives in §4.8–§4.10, and Chapter 3, already cover several of these in detail).

**A. Drive-related faults** — overcurrent, overvoltage, undervoltage, DC-bus abnormalities, inverter/IGBT issues, drive temperature, motor-control abnormalities. Diagnostic character: often the *most* ambiguous category, because the drive sits electrically downstream of nearly every mechanical subsystem (Ch. 1 §1.5) — a drive-side alarm is frequently evidence of something happening elsewhere, not a drive defect.

**B. Motor-related faults** — winding problems, overheating, abnormal current, torque abnormalities, mechanical loading. Diagnostic character: overlaps heavily with drive-related faults in symptom presentation; phase-balance and temperature-trend data are the most useful signals for separating "motor" from "drive" specifically.

**C. Brake-related faults** — timing, release problems, drag, wear, insufficient braking behavior. Diagnostic character: a safety-relevant category that frequently masquerades as a motor/current issue (Ch. 3 §3.2) and deserves elevated diagnostic priority regardless of statistical frequency.

**D. Door-related faults** — timeout, photo-eye issues, lock/interlock issues, encoder/position problems, motor/belt/roller problems. Diagnostic character: covered in full in §4.9; the highest-frequency fault category in most installations simply because doors cycle far more often than the main drive completes distinct trips.

**E. Encoder/position faults** — position mismatch, speed-feedback inconsistency, leveling deviation, signal loss, feedback instability. Diagnostic character: covered in full in §4.10; uniquely tricky because a bad encoder degrades the *quality of every other measurement's interpretation*, not just its own reading.

**F. Communication faults** — controller, drive, sensor, or network/bus-related. Diagnostic character: distinguished from a "real" fault in the subsystem the missing data was about — a sensor that stops reporting is not the same as a sensor reporting a bad value, but downstream logic may not always distinguish the two cleanly (see the alarm-cascade table, §4.20, row 5).

**G. Safety-chain faults.** The safety chain is a series of interlocked checks (door locks, governor state, overtravel limits, and similar) that must **all** confirm "safe" before the elevator is permitted to move. *[ESTABLISHED INDUSTRIAL KNOWLEDGE]* An interruption anywhere in that chain inhibits motion — this is a deliberate, fail-safe design, not a bug. This book does **not** describe how to bypass, defeat, or work around any part of a safety chain, and would not do so even if asked, because that information has no legitimate diagnostic purpose and real potential for harm. What matters for this project is understanding *why* safety events require categorically different treatment than every other fault category discussed in this chapter: they are handled by independent, hardware-level mechanisms specifically so that they do not depend on — and are not delayed by — any software reasoning layer, AI or otherwise. Consistent with the project's own stated safety boundary (Understanding Report §J), the RCA Agent's role here is limited to helping a technician understand, after the fact, *why* a safety-chain event occurred, using ordinary telemetry evidence — never to interpret, predict, or influence whether the safety chain itself should act.

**H. Environmental/thermal faults** — excessive temperature, humidity-related issues, abnormal environmental conditions. Diagnostic character: usually *contextual* evidence rather than a fault in their own right — a hot machine room doesn't fail on its own, but it changes what "normal" drive/motor temperature readings should look like, and can make an otherwise-borderline reading cross an alarm threshold.

> **Why This Matters to KONE Elevate RCA:** This taxonomy is what the alarm-correlation stage uses to decide which evidence sources are relevant to a given fault episode — an encoder-category alarm should pull in leveling and position data by default; a door-category alarm should pull in photo-eye and lock-state history; and so on.

## 4.8 Deep-Dive: Motor Overcurrent, Revisited and Expanded

Chapter 2 introduced this reasoning chain with eight candidate causes, told narratively. The roadmap identifies this exact example — mechanical jam, motor winding fault, cable fault, IGBT failure, or wrong VFD parameters, all converging on the same fault code — as the project's central illustration of why **fault code ≠ root cause**, and this chapter formalizes it as a full comparison table, with one additional column: what *other* causes each hypothesis could itself be confused with.

| Candidate Cause | Physical Mechanism | Expected Sensor Evidence | Expected Electrical Behavior | Possible Alarm | Evidence Supporting | Evidence Against | Other Possible Causes It Resembles |
|---|---|---|---|---|---|---|---|
| **Mechanical jam** | Physical obstruction resists motion | Current elevated during motion attempts; vibration signature change | Clean drive self-test | Overcurrent, stalled-motion | Current tied specifically to motion attempts; clean self-test | Elevated current while stationary | Brake drag, rope/traction issue |
| **Brake drag** | Brake fails to fully release | Current elevated correlated with brake-release timing; possible position drift | Clean drive self-test | Overcurrent, possible brake fault | Tight correlation with brake state across trips | Elevated current regardless of brake state | Mechanical jam, rope/traction issue |
| **Excessive load** | Car loaded near/beyond rated capacity | Current elevated proportional to load-sensor reading | Clean | Overcurrent, overload | Correlates directly with load data | Elevated current at normal/low load | (Generally distinct if load data exists) |
| **Rope/traction issue** | Rope or sheave wear reduces available friction | Current elevated under load; possible position/speed mismatch if slip occurs | Clean | Overcurrent, position deviation | Load-dependent severity; matches wear/inspection history | No position deviation, no wear indicators | Sheave wear, counterweight imbalance |
| **Motor winding fault** | Insulation breakdown / partial short | Phase-current imbalance independent of load/motion state; elevated motor temp | Drive-side self-test may isolate the anomaly to the motor | Overcurrent, motor-temperature fault | Imbalance present even under light/no load | Balanced phases, normal temperature | IGBT/drive fault (similar "current-side" symptom) |
| **Motor cable fault** | Loose connection or partial short in motor wiring | Intermittent/erratic current, sometimes vibration-correlated | Intermittent drive fault pattern | Overcurrent, intermittent fault log pattern | Non-repeatable pattern across similar trips | Highly consistent, repeatable pattern | Loose sensor connection (different subsystem, similar "erratic" signature) |
| **IGBT / drive fault** | Device degradation/failure inside the drive | Abnormal current waveform/phase imbalance traceable to drive side; elevated drive temperature | Drive self-test fails or flags an internal fault | Drive fault / IGBT fault | Failed self-test; drive-side temperature anomaly | Clean self-test with a mechanically-explicable pattern | Motor winding fault |
| **Incorrect drive parameters** | Configuration mismatch causes the control loop to over-command current | Persistent, systematic elevated current from a known configuration-change point forward | Clean hardware self-test — nothing is physically broken | Overcurrent (often a "nuisance trip" pattern) | Correlates with a known configuration change; consistent regardless of load/mechanical state | Sudden onset with no configuration change nearby | (Distinguished mainly by configuration-history evidence, not sensor pattern alone) |
| **Guide-shoe / rail binding** | Car or counterweight guide shoes bind against the rail | Current elevated at consistent points in travel tied to position, not load | Clean | Overcurrent, position-correlated pattern | Repeatable at the same physical location every trip | No positional consistency | Mechanical jam (a stationary obstruction), rail-lubrication issues |

**How an experienced technician differentiates these hypotheses in practice:** broadly, by layering evidence rather than trusting any single reading — checking whether elevated current is direction-dependent (suggests counterweight/traction asymmetry), position-dependent (suggests a localized mechanical cause like binding or an obstruction), load-dependent (suggests genuine load or traction-margin issues), brake-state-dependent (suggests brake drag), or none of the above (which shifts weight toward an electrical-side cause — winding, cabling, or the drive itself) — and then confirming with a drive self-test and, where safe and appropriate, direct physical inspection.

> **COMMON MISCONCEPTION:** "Overcurrent means motor failure." The table above makes the actual claim concrete: overcurrent is an *observation that requires contextual investigation* — nine structurally distinct causes, several producing near-identical raw current signatures, separated mainly by secondary correlations (timing, direction, load, position) rather than the current reading alone.

> **Why This Matters to KONE Elevate RCA:** This table is the most direct precedent in the whole book for what a populated fault-tree node, and its Bayesian evidence weighting, will eventually look like in the project's RCA-focused phase.

## 4.9 Deep-Dive: Door Fault

| Candidate Cause | Symptom | Sensor Evidence | Event | Alarm | Alternative Causes |
|---|---|---|---|---|---|
| **Photo-eye degradation** | Repeated reopening, no visible cause | Photo-eye state instability across cycles | Door fails to complete close cycle | Door obstruction / timeout | Genuine obstruction |
| **Genuine obstruction** | Door fails to close at one specific, repeatable point | Photo-eye/safety-edge triggers exactly at the object; clears when removed | Door fails to complete close cycle | Door obstruction | Photo-eye degradation — this is the pairing the project's own proposal example is built around |
| **Roller wear** | Slow, noisy door movement | Elevated door-motor current, longer cycle time | Cycle duration exceeds normal | Door timeout | Track misalignment, motor weakness |
| **Belt issue** | Inconsistent panel synchronization/speed | Current-pattern change, panel-position mismatch | Uneven or incomplete motion | Door fault, timeout | Roller wear, motor weakness |
| **Door-motor weakness** | Weak/inconsistent movement | Elevated or erratic motor current | Slow/incomplete cycles | Door fault, timeout | Obstruction, belt/roller issue |
| **Door-encoder fault** | Reported position disagrees with reality | Position-vs-commanded deviation | Premature stop/reverse commands | Door encoder fault | Belt slippage (similar mismatch, different mechanism) |
| **Lock/interlock instability** | Repeated reopening; fails to confirm locked | Lock-state signal instability | Safety circuit can't confirm locked | Door-lock fault, safety-circuit-open | Photo-eye/obstruction symptoms |
| **Track/mechanical resistance** | Binding at a specific, repeatable point in travel | Elevated current at a consistent travel position | Inconsistent cycle timing | Door timeout | Roller wear |
| **Controller/electrical issue** | Erratic behavior matching no single mechanical pattern | Communication-error indicators, command-vs-response inconsistency | Unpredictable, no positional correlation | Door fault, possible communication fault | Any of the above, if severe enough to look mechanical |

**Why "door fault" is not equivalent to one specific failed component:** the table above spans an optical sensor, a mechanical lock, two different wear-prone drivetrain components, a dedicated motor, an encoder, and the control electronics itself — nine structurally different subsystems, several of which share nearly identical top-level symptoms (repeated reopening, elevated cycle time). A "door fault" alarm narrows the investigation to the door subsystem; it does essentially none of the work of narrowing it further than that.

> **Why This Matters to KONE Elevate RCA:** The photo-eye/genuine-obstruction pair remains the sharpest test case in the whole book for the difference between "the evidence is ambiguous" and "the evidence is genuinely insufficient" — a single event looks identical either way; only a multi-event pattern resolves it, which is a strong argument for weighting historical, not just present-moment, evidence heavily in this specific fault category.

## 4.10 Deep-Dive: Encoder / Leveling Fault

An encoder problem can, by itself, produce: a **position mismatch** (reported position disagrees with an independent reference), **speed-feedback inconsistency** (reported speed doesn't match what the commanded profile would predict), **leveling deviation** (the final stop position is off), general **motion abnormalities** (rougher ride quality, since FOC's torque-control precision — Ch. 2 §2.4 — depends on accurate rotor-angle feedback), and, if the controller's own signal-consistency checks catch it directly, an explicit **encoder fault** code.

| Alternative Cause | Distinguishing Evidence |
|---|---|
| **Rope/sheave slip (a real motion problem)** | An independent leveling sensor *and* the encoder both show the same deviation — agreement between two independent references suggests the discrepancy reflects real motion, not a feedback fault |
| **Encoder misalignment** | The deviation has a consistent, reproducible pattern tied to a specific rotor position, rather than random noise |
| **Wiring/connector issue** | Intermittent, often correlated with vibration or temperature, and may resolve if the connector is disturbed |
| **Controller interpretation/calibration** | The raw encoder signal, if independently checkable, looks clean, but the controller's derived value is wrong |
| **Genuinely intermittent connection** | Not reproducible on demand; recurs unpredictably; historical/event-log reconstruction is the main available tool |

> **Why This Matters to KONE Elevate RCA:** Reinforces, in a third subsystem, the same lesson as §4.8 and §4.9: an alarm identifies where the *symptom* was observed, not necessarily where the *cause* lives. Three separate deep-dives, three structurally identical conclusions — this repetition is deliberate, because it's the pattern that generalizes, not any one subsystem's specific fault list.

## 4.11 Diagnostic Signals

Six categories of information a diagnostic process — human or AI — can draw on:

- **Real-time signals** — current sensor values and live states (Ch. 3 §3.5's dictionary, read at this instant).
- **Historical signals** — past trends and previous behavior of those same signals.
- **Event data** — timestamped log entries: what happened, when.
- **Alarm data** — alarm code, severity, subsystem, and state (active/cleared/latched).
- **Operational context** — trips, starts/stops, travel distance, door cycles, running hours, load — the usage backdrop against which "normal" is defined.
- **Maintenance history** — previous repairs, replaced components, recurring faults, technician notes.

**Why no individual signal is always sufficient:** each category answers a different question — real-time signals answer "what's happening right now," historical signals answer "has this happened before," event/alarm data answer "what did the system itself conclude," operational context answers "is this consistent with normal wear," and maintenance history answers "has this already been addressed once." None of these questions, alone, is the question that actually matters — *what caused this* — but together they substantially narrow it.

> **The key principle:** diagnostic evidence becomes stronger when multiple independent or complementary observations agree.

> **Why This Matters to KONE Elevate RCA:** This is a direct restatement, in general form, of the project's own "multi-source evidence retrieval" design principle — the reason the Retrieval Agent is specified to pull from telemetry, fault logs, maintenance history, and documentation together, rather than from any single source.

## 4.12 Temporal Reasoning

Timestamps carry real diagnostic information — but less than they first appear to.

```
10:31:01   Motor current rises
10:31:02   Drive overcurrent
10:31:03   Drive trip
10:31:04   Position deviation
10:31:05   Safety event
```

**Why event ordering matters:** the sequence tells you the *order in which the system noticed things*, which is a real, useful constraint — a cause cannot be logged after its effect. This is why the primary/secondary reasoning in §4.5 leans on chronology.

**Why temporal sequence does NOT automatically prove causality.** A later event may be:

- A genuine **consequence** of the earlier one (the reading in §4.5).
- An **independent event** that simply happened to occur nearby in time.
- A **coincidental event** with no causal relationship at all.

Distinguishing these requires more than the clock. The diagnostic system must combine:

**Temporal evidence + Physical knowledge + Sensor evidence + Subsystem relationships + Historical context.**

Physical knowledge is what turns "these happened close together" into "this plausibly caused that" — knowing, for instance, that a drive trip is a known, direct protective response to overcurrent (Ch. 2 §2.3) is what makes the 10:31:01→10:31:02 link credible, not merely their one-second separation.

> **DIAGNOSTIC INSIGHT:** Two alarms one second apart with no plausible physical link are weaker evidence of a shared cause than two alarms thirty seconds apart *with* one. Time proximity and causal plausibility are separate axes of evidence, and both matter.

> **Why This Matters to KONE Elevate RCA:** This section is the direct conceptual bridge to the project's later alarm-correlation and causal-reasoning work — grouping alarms by time window is only the *first* filter; confirming a genuine primary/secondary relationship additionally requires the physical-knowledge layer built across Chapters 1–3 of this book.

## 4.13 Intermittent Faults

Intermittent faults are difficult for a specific, structural reason: **the evidence that would confirm them is frequently absent at exactly the moment someone goes looking.** Contributing factors include temperature dependence (a marginal component that only misbehaves above/below a threshold), vibration dependence, load dependence, environmental dependence (humidity, ambient conditions), and loose or marginal electrical connections that only open under specific mechanical or thermal stress — plus, as a distinct category, **communication instability**, where the underlying component may be fine but the link reporting its state is not.

**Historical telemetry is the primary tool for reconstructing what happened before the technician arrived.** A single site visit that finds nothing wrong is not evidence the problem doesn't exist; a review of the log for the days or weeks prior — looking for the pattern of warnings, near-threshold readings, or brief self-clearing faults that a hard-fault-only view would filter out entirely — is often the only way to build a credible case for what's actually going on. *[ESTABLISHED INDUSTRIAL KNOWLEDGE]* This book does not claim any specific detail about how KONE's own systems reconstruct historical state internally **[NOT PUBLICLY ESTABLISHED]** — only that the general principle (historical pattern reconstruction as the primary tool against intermittence) is standard industrial diagnostic practice.

> **Why This Matters to KONE Elevate RCA:** Intermittent faults are the strongest possible argument, within this whole chapter, for why the project's evidence retrieval must default to *pulling history*, not just the live/most-recent state — a design choice with no real cost when the fault is a simple hard fault, and enormous value when it isn't.

## 4.14 Fault Code Diagnostic Value

Not all fault information carries equal weight. A useful mental model is a hierarchy of progressively narrowing specificity:

```
"Elevator fault"
        ↓
"Drive fault"
        ↓
"Overcurrent"
        ↓
"Overcurrent + high temperature"
        ↓
"Overcurrent + high temperature + normal mechanical behavior"
        ↓
"Overcurrent + high temperature + drive self-test abnormal"
```

Each added piece of context narrows the plausible hypothesis space — the bottom line of this chain is consistent with far fewer of the nine candidate causes in §4.8's table than the top line is. But **narrowing is not the same as proving.** Even the most specific line above ("drive self-test abnormal") still leaves at least two live hypotheses (an IGBT/drive fault, or a motor winding fault severe enough to produce a drive-detectable anomaly) — it has sharply reduced the space, not eliminated all but one member of it.

This is the distinction between **symptom specificity** (how precisely the described symptom is characterized) and **diagnostic certainty** (how confident the resulting conclusion is). They move together, but specificity alone does not guarantee certainty — the last mile from "very likely" to "confirmed" often still requires either direct physical verification or a piece of evidence that is exclusively consistent with one remaining hypothesis.

> **Why This Matters to KONE Elevate RCA:** This is a direct preview of why the project's confidence scoring is designed to reflect the actual state of the evidence rather than simply how detailed the alarm description sounds — a highly specific-sounding fault description is not automatically a highly *certain* one.

## 4.15 Fault Code as a Search-Space Reducer

A more useful way to think about what a fault code is actually *for*: not as an answer, but as a **filter**. A fault code does not identify the root cause. It can, however:

- Narrow which subsystem to look at.
- Identify which evidence is worth collecting.
- Identify which historical events are relevant to pull.
- Activate the relevant set of diagnostic hypotheses to consider.
- Prioritize the order evidence should be retrieved in.

"Motor overcurrent," under this framing, should cause a diagnostic system to open an investigation into motor, drive, IGBT, cabling, brake, traction, load, mechanical resistance, and configuration/parameters together — **not** to immediately conclude "motor failure." This reframing is the direct conceptual bridge into the project's RCA architecture: a fault code is the trigger that opens an investigation and scopes its evidence retrieval, not the output of one.

> **Why This Matters to KONE Elevate RCA:** This is close to a literal specification for what the project's alarm-correlation and evidence-retrieval stages need to do the moment a fault episode is formed — treat the fault code as a routing signal, not a conclusion.

## 4.16 The Diagnostic Hypothesis Space

Formalizing §4.8's reasoning as an explicit **hypothesis space**:

```
Observed:  Motor overcurrent

H1 — Mechanical obstruction
H2 — Brake drag
H3 — Motor winding fault
H4 — Cable fault
H5 — IGBT fault
H6 — Excessive load
H7 — Parameter/configuration issue
```

The diagnostic process's job, at this stage, is to gather evidence that:

- **Increases support** for some hypotheses (e.g., a clean drive self-test increases support for H1, H2, H6).
- **Decreases support** for others (a clean self-test decreases support for H5).
- **Eliminates** hypotheses genuinely inconsistent with the evidence (a load sensor showing a light load largely eliminates H6).
- **Retains uncertainty** when the evidence is insufficient to do any of the above confidently — which is a legitimate, and often correct, outcome, not a failure of the process.

This chapter deliberately stops short of introducing the formal mathematics of *how* to combine this evidence — that belongs to the project's dedicated RCA/Bayesian-reasoning phase. What matters here is the conceptual shape: a diagnosis is not "pick the first plausible cause," it is "maintain a set of live hypotheses and let evidence move probability mass between them."

> **Why This Matters to KONE Elevate RCA:** This section exists specifically to prepare the team conceptually for the Bayesian reasoning the roadmap calls for later — everything here (hypotheses, supporting/contradicting evidence, retained uncertainty) has a direct, formal counterpart in that later material; this chapter deliberately introduces the *shape* of the reasoning before the *arithmetic* of it.

## 4.17 The Technician's Diagnostic Process

How a skilled technician conceptually approaches an alarm: *[ESTABLISHED INDUSTRIAL KNOWLEDGE]*

```
Alarm received
        ↓
Understand the symptom
        ↓
Check recent events
        ↓
Check operating conditions
        ↓
Inspect the relevant subsystem
        ↓
Compare sensor evidence
        ↓
Consider possible causes
        ↓
Eliminate inconsistent causes
        ↓
Identify the likely cause
        ↓
Verify the diagnosis
        ↓
Repair
        ↓
Test
        ↓
Close the incident
```

The project's proposed RCA system is, at its core, attempting to assist and augment exactly this reasoning process — structuring and accelerating the "check recent events → check operating conditions → compare sensor evidence → consider possible causes → eliminate inconsistent causes" portion of the workflow specifically, using the same kind of evidence a technician already gathers, organized and cross-referenced automatically. This chapter does not attempt to specify *how* that assistance should be architected — that is deliberately left to the dedicated architecture phase of this book.

> **Why This Matters to KONE Elevate RCA:** Naming the workflow the project is augmenting — rather than inventing a new one — is itself a grounding exercise: every stage of the project's eventual agent pipeline should map back to a step in this list, or it's solving a problem the technician doesn't actually have.

## 4.18 Diagnostic Failure Modes

| Mistake | Why It Happens | Why It's Dangerous | How Evidence-Based Diagnosis Avoids It |
|---|---|---|---|
| Treating the alarm as the root cause | The fault code is the most immediately visible information | Leads to repairing/replacing the wrong (often costlier) component | Separates "what was observed" from "what caused it"; requires supporting evidence before naming a cause |
| Focusing only on the latest alarm | The most recent alarm is the most attention-grabbing | Ignores that recent alarms are often consequential, not initiating | Reconstructs the full episode timeline before concluding |
| Ignoring event chronology | Alarms reviewed as a list, not a timeline | Breaks primary/secondary reasoning (§4.5) | Explicit temporal-sequence reconstruction as a standard step |
| Ignoring historical behavior | Historical data takes extra effort to retrieve | Intermittent/gradual faults become invisible | History treated as a standard, not optional, evidence source |
| Ignoring mechanical causes of electrical symptoms | Electrical evidence is precise and readily available | Leads to unnecessary electrical-component replacement | Mechanical evidence (vibration, brake state, load) checked alongside electrical evidence by default |
| Ignoring secondary alarms | Attention goes to the most severe-looking alarm | Secondary alarms often carry corroborating or contradicting evidence | Every alarm in an episode is treated as evidence, not noise |
| Assuming one alarm = one failed component | Alarm language suggests a specific single cause | The same alarm can result from many distinct single-component failures | Explicit hypothesis-space generation (§4.16) before concluding |
| Ignoring alternative hypotheses | Tempting to stop once a plausible cause is found | The first plausible explanation isn't necessarily correct | Supporting *and* contradicting evidence weighed for every candidate |
| Over-trusting a single sensor | A clear reading feels authoritative | The sensor itself (or its wiring/interpretation) can be the fault | Cross-checked against at least one independent/complementary signal |
| Ignoring intermittent behavior | Intermittent faults are, by definition, often absent when checked | Produces a false "no fault found" and the problem recurs | Historical/event-log reconstruction specifically targets absent-technician evidence |
| Treating correlation as causation | Temporal proximity feels causally connected | Misattributes a coincidental or independent event | Explicit reminder (§4.12) that proximity is evidence, not proof |
| Concluding without sufficient evidence | Pressure to resolve quickly | A confident-but-wrong conclusion is worse than an honest "insufficient evidence" | Deliberately retains and flags uncertainty when evidence doesn't support confidence — the abstention behavior in the project's own proposal |

> **Why This Matters to KONE Elevate RCA:** This list is, essentially, a specification-by-negation for the RCA Agent's design — every row here is a behavior the project's evidence-weighing, confidence-scoring, and abstention design choices exist specifically to prevent.

## 4.19 Master Diagnostic Table

| Observed Fault/Alarm | Possible Root Causes | Relevant Sensors | Historical Evidence | Possible Secondary Effects | Diagnostic Questions |
|---|---|---|---|---|---|
| Motor overcurrent | Jam, brake drag, load, rope/traction, winding, cable, IGBT/drive, parameters | Phase current, motor temp, vibration, load, brake timing | Prior overcurrent events, recent parameter/brake service | Drive trip, motion stall, possible safety-chain involvement | Elevated at rest or only in motion? Correlated with brake timing? |
| Drive trip | Any severe overcurrent/overvoltage, IGBT/drive fault, DC-bus anomaly | Drive fault log, DC-bus voltage, drive temp | Recurring trips, recent firmware/parameter changes | Motion stopped mid-travel, leveling deviation | Preceded by another alarm? Self-test clean? |
| Overvoltage | Regen/chopper mismanagement, supply anomaly, rectifier fault | DC-bus voltage, chopper status, input power quality | Correlation with heavy-load descending trips | Drive trip, nuisance trips under specific conditions | Correlates with regenerative (overhauling) conditions? |
| Undervoltage | Building-supply sag, rectifier fault | DC-bus voltage, input power quality | Other equipment affected simultaneously | Drive trip, degraded torque capability | Isolated to elevator, or building-wide? |
| Overload | Genuine excess load, load-sensor miscalibration | Load sensor, motor current | Load history, calibration history | Overload alarm, motion inhibited | Does current-implied load agree with the sensor? |
| Motor temperature | High duty cycle, winding fault, ambient heat, cooling issue | Motor/drive/machine-room temp, usage data | Recent high usage, HVAC issues | Drive derating or protective trip | Explained by duty cycle and ambient, or in excess of it? |
| Brake abnormality | Wear, misadjustment, coil issue | Brake torque/timing, current at release moments | Brake maintenance/wear trend | Overcurrent, leveling deviation, accelerated wear | Correlates tightly with brake-release timing? |
| Door timeout | Obstruction, photo-eye drift, roller/belt/track wear, motor weakness, lock instability | Photo-eye state, door-motor current, cycle duration | Recurrence pattern | Safety-circuit-open, drive-start-inhibited | Tied to a specific removable cause, or recurs without one? |
| Door-lock fault | Contact wear/misalignment, mechanical damage | Lock-state signal, safety-circuit state | Recurrence, recent door service | Safety-circuit-open, motion inhibited | Signal itself unstable, or reliably "unlocked"? |
| Photo-eye issue | Alignment/lens drift, contamination, wiring | Photo-eye state across cycles, environment | Pattern across cycles, cleaning history | Door timeout, repeated reopening | Correlates with a specific object, or intermittent without one? |
| Encoder fault | Contamination, connector, wear, wiring | Signal quality/dropout, position-vs-commanded, leveling-sensor cross-check | Recent service, recurrence | Leveling deviation, rough motion | Does an independent position reference disagree, or agree? |
| Leveling deviation | Encoder drift, brake timing, rope stretch/slip, leveling-sensor fault | Leveling sensor, encoder, brake timing, rope condition | Trend over time | Passenger complaints, repeated re-leveling | Consistent direction/magnitude, or variable? |
| Communication fault | Bus/wiring, connector, EMI, component failure | Comm-error counters, affected subsystem's local data | Recurrence, environmental correlation | Loss of downstream data, possible false secondary alarms | Isolated to one link, or multiple simultaneously? |
| Safety-chain event | Genuine safety condition, OR a degraded sensing/contact component | Safety-chain state, specific link, governor/safety-gear status | Prior events, recent safety-system service | Elevator fully out of service pending qualified inspection | Genuine precipitating condition, or does only the chain state itself look anomalous? |
| Overspeed-related event | Genuine overspeed, OR governor/speed-sensing fault | Motor/car speed vs. commanded, governor switch state | Prior events, recent governor service | Safety-gear engagement, out of service pending inspection | Does the speed data itself show an excursion, or only the governor path? |

## 4.20 Alarm Cascade Table

| Initiating Fault | Immediate Effect | First Alarm | Secondary Effect | Secondary Alarm | Final System Effect |
|---|---|---|---|---|---|
| Mechanical obstruction | Increased resistance to motion | Overcurrent | Drive protective trip | Drive trip | Motion stopped mid-travel; elevator unavailable until cleared |
| Door photo-eye degradation | Intermittent false-obstruction detection | Door obstruction | Door repeatedly fails to complete its close cycle | Door-close timeout | Safety circuit remains open; drive-start inhibited — elevator effectively out of service with no drive/motor problem at all |
| Encoder signal degradation | Inaccurate position/speed feedback | Encoder fault | Control loop corrects based on wrong information | Leveling deviation | Repeated re-leveling; ride-quality complaints even without a "hard" failure yet |
| Brake drag | Continuous mechanical resistance during travel | Overcurrent (correlated with brake-release timing) | Accelerated wear on both brake and motor if unaddressed | Brake-wear or motor-temperature alarm, over time | An intermittent nuisance becomes two separate, costlier component problems |
| Communication-link degradation | Intermittent loss of a specific signal | Communication fault | Controller falls back to a default/last-known value, or flags downstream logic as uncertain | An unrelated-looking secondary alarm from whichever subsystem depended on that signal | A "one wire" problem can present as a fault in an entirely different subsystem |

**The purpose of this table:** every row demonstrates a case where investigating the *final* alarm alone would point a technician (or an AI system without alarm correlation) toward the wrong subsystem entirely. Correlating alarms into a single episode — recognizing that a row's later columns are downstream of its first — is a necessary step **before** root-cause analysis can meaningfully begin, not an optional refinement of it.

## 4.21 The Fault → Evidence → Hypothesis Map

A reusable conceptual model tying the whole chapter together:

```
OBSERVATION              (a sensor reading, an alarm, an event)
        ↓
EVENT                    (logged, timestamped)
        ↓
SYMPTOM                  (what the observation suggests is happening)
        ↓
POSSIBLE SUBSYSTEM       (narrowed via fault category, §4.7)
        ↓
CANDIDATE CAUSES         (the hypothesis space, §4.16)
        ↓
SUPPORTING EVIDENCE      (evidence that increases confidence in a hypothesis)
        ↓
CONTRADICTING EVIDENCE   (evidence that decreases confidence in a hypothesis)
        ↓
REMAINING HYPOTHESES     (what's left once evidence has been weighed)
        ↓
DIAGNOSTIC CONCLUSION    (a ranked, evidence-backed answer — or an honest
                           statement that more evidence is needed)
```

Each layer does real narrowing work, but — consistent with §4.14 — no layer *guarantees* the next. This model is the direct conceptual scaffold for the project's later stages: alarm correlation operates on the observation/event/symptom layers; fault isolation narrows to a subsystem; root-cause analysis works the candidate-causes-through-remaining-hypotheses layers; and probabilistic (Bayesian) reasoning is the formal mechanism for how supporting and contradicting evidence actually move confidence between hypotheses.

> **Why This Matters to KONE Elevate RCA:** This map is close to a literal table of contents for the rest of the research book — every subsequent phase deepens exactly one or two of these nine layers.

## 4.22 What the Diagnostic System Knows vs. Does Not Know

A distinction worth stating explicitly, because it grounds every later claim this project makes about what the RCA Agent is and is not capable of.

**It may know:**

- A sensor crossed a defined threshold.
- An event occurred, at a specific time.
- An alarm was generated, at a specific severity.
- Several events occurred in a specific sequence.
- Certain signals changed, and by how much.
- Historical behavior of those same signals.
- Operating context (load, usage, recent conditions).
- Maintenance history (repairs, replacements, prior conclusions).

**It may NOT know automatically:**

- The true physical root cause.
- Whether two alarms share one cause, or are independent.
- Whether a sensor itself is the thing that's faulty.
- Whether a temporally-close event is causal, or coincidental.
- Whether the available evidence is actually sufficient to conclude anything.
- Whether a recommended action is safe without human/technician verification.

> **Why This Matters to KONE Elevate RCA:** This is the direct conceptual foundation for responsible AI reasoning in every later chapter — confidence scoring, abstention behavior, and the human-in-the-loop design all exist specifically because the right column above is real and permanent, not a temporary limitation to be engineered away.

## 4.23 KONE-Specific Research Boundaries

Everything in this chapter has been framed in terms of general industrial fault/alarm/diagnostic principles, deliberately, because the specific detail of how KONE's own controllers classify, name, and structure their fault codes is proprietary and not publicly available in full. This book does not invent that mapping.

What *can* reasonably be researched from public sources: general elevator fault categories, industry-wide diagnostic and alarm-management principles, publicly documented descriptions of KONE's connected services and their general capabilities (already surfaced in the project's Master Research Roadmap and the earlier Understanding Report), and publicly available general engineering information about traction elevators.

### Research Gap

**Exact proprietary OEM fault-code → component → root-cause mappings are not fully publicly established.**

This matters for the project in a direct, practical way: the fault trees, FMEA tables, and diagnostic tables built throughout this book (Chapter 3's failure matrix, this chapter's motor-overcurrent and door-fault tables) are built from general engineering reasoning about how traction elevators work and fail, not from KONE's actual internal fault-code taxonomy. They are a credible, defensible *starting point* — precisely the kind of illustrative material the project's own proposal describes itself as offering — not a substitute for KONE SME review, which the proposal's own roadmap correctly identifies as the necessary next step before any of this material could be treated as production-accurate.

## 4.24 Judge-Question Preparation

**1. Why doesn't an overcurrent fault automatically mean motor failure?**
*Concise:* Because at least nine structurally distinct causes can produce the same current signature (§4.8).
*Detailed:* Motor torque is approximately proportional to commanded current (Ch. 1 §1.5); anything that increases required torque — a jam, brake drag, excessive load, rope/traction issues — increases current identically to a genuine electrical fault. Distinguishing them requires secondary evidence: correlation with brake state, load, direction, or position.
*What the judge is testing:* whether the team actually understands the physics behind their own headline example, or is repeating it as a slogan.

**2. How do you distinguish a primary fault from a consequential alarm?**
*Concise:* By combining chronology with physical plausibility, not chronology alone (§4.5, §4.12).
*Detailed:* A later alarm is a plausible consequence only if a known causal mechanism connects it to the earlier one (e.g., a drive trip is a documented protective response to overcurrent). Time proximity alone is suggestive but not sufficient.
*What the judge is testing:* whether the team can articulate their own alarm-correlation logic beyond "things that happen close together."

**3. How can one physical failure generate multiple alarms?**
*Concise:* Through a fault cascade — each stage's effect becomes the next stage's detected symptom (§4.6).
*Detailed:* The door-photo-eye example is the clearest case in this book: one degrading component generates an obstruction alarm, a timeout alarm, a safety-circuit-open condition, and a drive-inhibited state, all from a single root cause.
*What the judge is testing:* whether the team can walk a cascade end-to-end with a concrete example, not just assert that cascades happen.

**4. Why are fault codes insufficient for RCA?**
*Concise:* Because a fault code names a detected symptom, not a cause (§4.1, §4.15).
*Detailed:* A fault code is best understood as a search-space reducer — it narrows which subsystem and which evidence matter, but the actual cause has to be established by weighing multiple, independent pieces of evidence against a hypothesis space.
*What the judge is testing:* whether the team's core thesis is genuinely load-bearing, or decorative.

**5. What happens if the sensor reporting the fault is itself faulty?**
*Concise:* This is exactly why no single sensor is trusted in isolation (§4.18, item 9).
*Detailed:* Cross-checking against an independent or complementary signal (e.g., two independent position references, per §4.10) is the standard defense; when no independent check exists, confidence should be reduced accordingly rather than treating the questionable reading as ground truth.
*What the judge is testing:* whether the team has thought about evidence reliability, not just evidence collection.

**6. How do you handle intermittent faults?**
*Concise:* By weighting historical, pattern-based evidence over present-moment inspection (§4.13).
*Detailed:* Intermittent faults are, by definition, frequently absent when checked directly; reconstructing the pattern from event-log history — including sub-threshold warnings that never individually triggered an alarm — is the primary tool.
*What the judge is testing:* whether the team's design treats history as a first-class input or an afterthought.

**7. Why is event chronology important?**
*Concise:* It constrains which causal stories are physically possible (§4.5, §4.12).
*Detailed:* A cause cannot be logged after its effect; ordering is a real, if incomplete, constraint that the primary/secondary-alarm distinction depends on.
*What the judge is testing:* basic causal reasoning literacy.

**8. Can temporal correlation prove causation?**
*Concise:* No — it is evidence, not proof (§4.12).
*Detailed:* A later event can be a genuine consequence, an independent coincidence, or an unrelated event that merely happened nearby in time; physical plausibility (does a known mechanism connect them?) is what turns proximity into a credible causal claim.
*What the judge is testing:* whether the team will overclaim under pressure — this is one of the easiest traps to fall into when explaining a confident-sounding demo.

**9. What evidence would distinguish brake drag from motor failure?**
*Concise:* Correlation with brake-release timing specifically (§4.8, §4.2).
*Detailed:* Brake drag produces current elevation tightly tied to brake-release/engage events across multiple trips; a genuine motor winding fault produces phase imbalance largely independent of brake state.
*What the judge is testing:* whether the team can apply their general framework to a specific, concrete pair on demand.

**10. How would you distinguish an IGBT problem from a mechanical jam?**
*Concise:* The drive's own internal self-test (§4.8).
*Detailed:* An IGBT/drive-side fault is expected to be traceable via the drive's self-diagnostics and drive-side temperature; a mechanical jam is expected to leave the drive's self-test clean while current correlates with motion attempts specifically.
*What the judge is testing:* the same as Q9, applied to the electrical/mechanical boundary specifically.

**11. Why can't an LLM simply read the fault code and diagnose the problem?**
*Concise:* Because the fault code alone doesn't contain enough information to do so (§4.1, §4.15) — no amount of language-model reasoning recovers information that was never captured in the first place.
*Detailed:* An LLM reasoning over a bare fault code is reasoning over the least-specific line of the §4.14 hierarchy; this project's architecture instead treats the fault code as a trigger for structured, multi-source evidence retrieval before any language-model reasoning happens at all.
*What the judge is testing:* whether the team understands why their architecture is deliberately *not* "send the fault code to an LLM and ask what's wrong" — a distinction worth being able to state crisply.

**12. What happens when there is insufficient evidence?**
*Concise:* The system should reduce confidence and say so, not guess (§4.16, §4.18 item 12).
*Detailed:* Retaining uncertainty is a legitimate diagnostic outcome; the project's stated design explicitly reduces confidence and flags a case for further technician investigation rather than forcing a conclusion when evidence is incomplete or conflicting.
*What the judge is testing:* whether the team will defend abstention as a design strength or apologize for it as a weakness — it should be the former.

**13. Why is historical telemetry important?**
*Concise:* It's often the only evidence available for intermittent or gradually-developing faults (§4.13).
*Detailed:* Present-moment inspection alone systematically misses anything condition-dependent; a log review can recover the pattern even when the triggering condition isn't present during the visit.
*What the judge is testing:* essentially the same ground as Q6, from a slightly different angle — expect judges to probe this more than once.

**14. Why are proprietary OEM fault-code mappings a limitation?**
*Concise:* Because this book's fault trees and tables are built from general engineering reasoning, not KONE's actual internal taxonomy (§4.23).
*Detailed:* The team should be explicit that the illustrative material in this research book is a credible starting point pending KONE SME review, not a claim of production accuracy — overclaiming here is a real credibility risk.
*What the judge is testing:* intellectual honesty about the boundary between what the team knows and what they're inferring.

**15. How does this approach differ from conventional fault-code lookup?**
*Concise:* A lookup maps one code to one answer; this approach maps one code to an investigation (§4.15, §4.21).
*Detailed:* Conventional lookup tables implicitly assume the fault-code-to-cause relationship the whole book has been demonstrating is false; this project instead formalizes fault codes as scoping/routing signals into a multi-evidence, multi-hypothesis reasoning process.
*What the judge is testing:* whether the team can state their core differentiator in one clean sentence when put on the spot.

**16. KONE's connected services already analyze 200+ parameters — isn't multi-signal evidence-gathering something they already do?**
*Concise:* Very possibly, at the monitoring layer — this project's claimed contribution is the reasoning layer on top of that evidence, not the evidence collection itself (Understanding Report, §L).
*Detailed:* The team's own competitive-differentiation research already flags this as the sharpest version of this question; multi-parameter monitoring and evidence-weighted causal reasoning with an explicit, auditable hypothesis trail are not the same claim, and the team should be precise about which one they're actually making.
*What the judge is testing:* whether the team has genuinely internalized their own competitive-landscape research, or will be caught flat-footed by the single most predictable question in the room.

**17. How do you avoid incorrectly merging two unrelated faults that happen to occur at the same time?**
*Concise:* The same physical-plausibility check used throughout this chapter — proximity in time alone isn't sufficient grounds to merge them (§4.12).
*Detailed:* If no credible causal mechanism connects two temporally-close alarms — no subsystem relationship, no known cascade pattern like those in §4.6/§4.20 — they should be treated as separate fault episodes, even though separating truly coincidental events from a subtle shared cause is inherently harder than confirming an already-plausible link.
*What the judge is testing:* whether the team has considered the false-positive side of alarm correlation, not just the true-positive side their examples emphasize.

**18. How would this chapter's framework have handled your own proposal's door-obstruction example?**
*Concise:* Exactly as walked through in §4.6, Example 3 and §4.9 — one initiating cause, correctly correlated rather than treated as four independent problems.
*Detailed:* The team should be able to narrate that specific cascade fluently, since it's their own illustrative scenario: obstruction detected → repeated reopening → door-close timeout → safety-circuit-open → drive-start-inhibited, with the RCA layer's job being to correctly attribute all of that back to the door subsystem rather than triggering an unnecessary drive or safety-system investigation.
*What the judge is testing:* whether the team can apply their own framework to their own headline example fluently, on the spot, without needing to look it up.

---

# Phase 2 — What We Now Understand

1. A **fault** is a detected deviation, not necessarily a physical failure — and neither is the same thing as a **symptom**, an **event**, or an **alarm** (§4.1).
2. An **alarm** is a signal raised when a defined threshold is crossed — a claim the system is making about what it observed, not an independently verified fact about the world.
3. A **fault code** tells us what the controller detected and, at best, roughly where — never, by itself, why.
4. It does **not** tell us the true physical cause, whether it shares an origin with other alarms, or how confident we should be.
5. Alarms can **cascade** because subsystems are interdependent — one physical event can trigger a chain of detections across several layers of the system (§4.6).
6. The **primary/consequential** distinction changes the diagnostic conclusion entirely — confusing the two can lead to fixing the wrong thing, repeatedly (§4.5).
7. **Chronology** narrows which causal stories are physically possible, but does not, by itself, prove any of them (§4.12).
8. **Historical evidence** is often the only way to diagnose intermittent or gradually-developing faults — present-moment inspection systematically misses them (§4.13).
9. **Multiple, independent evidence sources** strengthen a diagnostic conclusion in a way no single source can (§4.11).
10. A responsible diagnostic process maintains a **hypothesis space** and updates it with evidence, rather than committing early to the first plausible explanation (§4.16).

## The Central Diagnostic Principle

> A fault code is an observation or diagnostic indication, not automatically a root-cause diagnosis.

In technical terms: a fault code represents the output of a threshold-based classification performed by the controller (or drive) on a narrow set of locally-available signals, at a specific moment. It reflects the controller's own, necessarily limited, view — it has no access to brake state unless brake state happens to be one of its inputs, no access to maintenance history, no access to what happened on a different subsystem three seconds earlier unless that data is explicitly correlated for it. Root-cause determination requires synthesizing evidence the fault-generating logic itself was never designed to combine — which is precisely the gap this entire project exists to close.

---

# Bridge to Phase 3 — From Elevator Diagnostics to the KONE Ecosystem

Phase 1 answered *how the elevator works*. Phase 2 answered *how its abnormalities become diagnostic information* — the journey from a physical cause to a logged, timestamped, coded alarm, and everything that's lost and gained along the way.

A natural question now follows, and it's the right one to ask next: **if this is how an elevator generates faults and diagnostic evidence, how does KONE currently collect, monitor, interpret, and act on that information in the real world?** This project is not being proposed into a vacuum — the Understanding Report already established that KONE 24/7 Connected Services, Otis ONE, Schindler Ahead, and TK Elevator MAX all already do *some* version of monitoring and predictive maintenance on exactly this kind of data. Before this book can credibly argue what a new RCA layer adds, it has to accurately understand what already exists.

Phase 3 must therefore study: KONE's own elevator architecture and product families, the KONE DX/connected ecosystem, KONE 24/7 Connected Services in depth, KONE's existing technician tools and (critically) its existing GenAI capabilities, the KONE maintenance workflow end-to-end, maintenance methodologies more broadly, and the CMMS/EAM landscape those workflows run on.

```
PHASE 1:  How the elevator works.
     ↓
PHASE 2:  How elevator abnormalities become diagnostic information.
     ↓
PHASE 3:  How KONE's real-world ecosystem currently handles that information.
```

Phase 3 content is not generated here — this document ends at the close of Phase 2.
