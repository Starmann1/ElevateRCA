# PHASE 5 — ROOT CAUSE ANALYSIS, RELIABILITY ENGINEERING & CAUSAL REASONING

### *KONE Elevate — Autonomous Fault Isolation & Root Cause Analysis: Master Research Book*

## How to Read This Chapter

Labels: **[PROJECT SOURCE]**, **[ESTABLISHED ENGINEERING KNOWLEDGE]** (the label for nearly everything below — reliability engineering and probability theory are mature, standard disciplines, not KONE- or even elevator-specific), **[EXTERNAL RESEARCH]**, **[ENGINEERING INFERENCE]**, **[ASSUMPTION]**, **[NOT PUBLICLY ESTABLISHED]**. This chapter did not require live web research — its subject is decades-old, well-documented engineering and statistical methodology — but it does require unusual care in a different way: **every numerical probability, severity score, or occurrence rating in this chapter is illustrative, invented for teaching purposes, and explicitly labeled as such.** None of it is, or claims to be, real KONE data. Where this chapter builds a fault tree or FMEA row, it is reusing and formalizing the engineering reasoning already established in Chapters 2–6 of this book — not inventing new proprietary claims about how elevators fail.

**The central question of this chapter:** *given an elevator fault and multiple pieces of imperfect evidence, how can we systematically determine the most plausible underlying cause instead of simply treating the alarm as the diagnosis?*

**The central principle, stated once and defended throughout:** **observation ≠ root cause.**

---

## From Phase 4 to Phase 5

Phase 4 established that the elevator industry already has connectivity, monitoring, predictive maintenance, analytics, remote diagnostics, technician support, machine learning, generative AI, and — at least one competitor, as of April 2026 — agentic AI. Simply saying *"we use AI"* is worth nothing competitively. The question this project actually has to answer is sharper: **what reasoning process should the AI perform?**

```
Existing evidence
     ↓
Diagnostic hypotheses
     ↓
Causal relationships
     ↓
Evidence evaluation
     ↓
Root-cause ranking
     ↓
Verification
```

This chapter is where that reasoning process finally gets a rigorous, engineering-grounded answer.

---

# Part I — Foundations

## 7.1 What Is Root Cause Analysis?

*[ESTABLISHED ENGINEERING KNOWLEDGE]* These terms get used loosely in everyday conversation about "why something broke." Precision matters here as much as it did for Chapter 4's fault/alarm/event terminology.

| Concept | Meaning | Elevator Example |
|---|---|---|
| **Symptom** | An observable effect | Motor overcurrent alarm |
| **Immediate cause** | The nearest, most directly-preceding trigger of the symptom | Motor drawing more current than the control loop expected |
| **Failure mode** | *How* something fails — the manner of failure | "Excessive torque demand" |
| **Failure mechanism** | The underlying physical/chemical process producing the failure mode | Increased mechanical resistance from an obstruction |
| **Contributing cause** | A factor that made the failure more likely or more severe, without being the sole trigger | Deferred brake maintenance increasing drag over time |
| **Latent cause** | A pre-existing condition, often dormant for a long time, that set the failure up | A design/parameter mismatch introduced at commissioning, undetected for months |
| **Root cause** | The earliest point in the causal chain where intervention would have prevented the failure | The mechanical obstruction itself (or, if recurring, whatever allows obstructions to keep occurring) |
| **Consequence** | What happens as a downstream result of the failure | Drive trip, elevator out of service |

**Why finding the first visible symptom is not the same as finding the root cause:** consider motor overcurrent. The immediate interpretation — "the motor is overloaded" — is true but incomplete; it restates the symptom in slightly different words rather than explaining it. The actual candidate root causes sit one or more steps further back: mechanical obstruction, brake drag, a traction problem, a motor winding problem, a cable issue, a drive/IGBT issue, or a configuration issue (Chapter 2 §2.5's original list, now formalized as fault-tree branches in §7.7).

> **KEY CONCEPT:** "What happened?" (motor overcurrent) is a different question from "why did it happen?" (one of at least seven distinct physical stories). RCA exists entirely to answer the second question using evidence, not to restate the first one with more technical vocabulary.

## 7.2 RCA vs. Fault Detection vs. Fault Isolation vs. Prediction vs. Corrective Recommendation

This chapter is building on a distinction Phases 3 and 4 already introduced (Ch.5 §5.14, Ch.6 §6.9) — restated here with two additional rows, because this chapter needs the full picture precisely:

| Capability | Core Question | Input | Output |
|---|---|---|---|
| **Fault detection** | "Is something abnormal?" | Real-time sensor thresholds | An alert |
| **Fault classification** | "What *type* of abnormality is this?" | The alert plus its category (Ch.4 §4.7) | A fault category label |
| **Fault isolation** | "Which subsystem/component is likely involved?" | The fault category, correlated signals | A narrowed investigation scope |
| **Root cause analysis** | "Why did the failure occur?" | Multi-source evidence weighed against a hypothesis space | A ranked, evidence-backed explanation with confidence |
| **Failure prediction** | "Could this occur in the future?" | Trend/degradation data | A forecast |
| **Corrective recommendation** | "What should be done about it?" | The RCA output, mapped to known remedies | A specific recommended action |

These six capabilities must not be conflated — Phase 4's entire competitive-landscape finding rested on exactly this distinction (every OEM researched clears detection, prediction, and recommendation; none publicly demonstrates structured RCA specifically). This chapter is about the one row every competitor left open.

## 7.3 An Overview of RCA and Reliability Methods

*[ESTABLISHED ENGINEERING KNOWLEDGE]* Twelve methods recur across reliability engineering and RCA practice, each developed to answer a slightly different question:

1. **5 Whys** — iterative causal drilling
2. **Fishbone / Ishikawa** — categorical brainstorming
3. **Fault Tree Analysis (FTA)** — top-down, "what could cause this failure"
4. **FMEA** — bottom-up, "what can this component do wrong"
5. **FMECA** — FMEA plus criticality ranking
6. **Event Tree Analysis (ETA)** — forward-looking, "what happens after this initiating event"
7. **Bow-Tie Analysis** — combines FTA and ETA around one central event
8. **Cause-and-effect diagrams** — a general category Fishbone belongs to
9. **Bayesian Networks** — probabilistic, evidence-weighted reasoning
10. **Causal graphs** — explicit cause→effect structure, the backbone Bayesian reasoning runs on
11. **Markov models** — state-transition modeling over time
12. **Dynamic Bayesian Networks** — Bayesian reasoning extended across time
13. **Reliability Block Diagrams (RBD)** — system-level reliability from component reliability

Each is introduced individually below (§7.4–§7.19), then compared side-by-side in one consolidated table once all thirteen have actually been taught (§7.20) — building that comparison before the methods are explained would ask the reader to evaluate tools they haven't seen yet.

The project's own research roadmap gives this chapter its organizing principle directly: move away from generic, categorical methods (5 Whys, Fishbone) toward **elevator-subsystem fault trees combined with probabilistic reasoning.** Everything from §7.6 onward builds toward that specific combination.

---

# Part II — Classical Qualitative Methods

## 7.4 5 Whys

*[ESTABLISHED ENGINEERING KNOWLEDGE]* The method: ask "why" repeatedly, using each answer as the starting point for the next question, until a root cause is reached (conventionally around five iterations, though the number is a rule of thumb, not a fixed rule).

**Applied to an elevator example:**

```
Elevator stopped
   ↓ Why?
Drive tripped
   ↓ Why?
Motor current exceeded threshold
   ↓ Why?
Motor required excessive torque
   ↓ Why?
Mechanical resistance increased
   ↓ Why?
A mechanical obstruction developed
```

**Limitations, and why they matter for this project specifically:**

- **Linear reasoning** — 5 Whys follows one chain at a time. It has no natural way to represent "the answer could branch into two, three, or seven distinct possibilities at this step," which is exactly the situation at every step of the chain above (Chapters 2 and 4 already showed "motor required excessive torque" has at least nine candidate explanations, not one).
- **Depends heavily on investigator knowledge** — each "why" answer requires someone to already know the right next-level explanation; the method provides no mechanism for generating or weighing competing answers.
- **Naturally oversimplifies multiple simultaneous causes** — a single chain cannot represent two independent problems occurring together (§7.28).
- **Does not naturally represent uncertainty** — every step is stated as fact, with no confidence attached.
- **Can lead to premature conclusions** — the chain stops at the first explanation that "feels" complete, not necessarily the best-supported one.

> **COMMON MISCONCEPTION:** 5 Whys is often treated as *the* RCA method, full stop. It's genuinely useful for a human walking through a single, already-mostly-understood incident narratively — but as the sole reasoning framework for autonomous, multi-signal, evidence-weighted diagnosis, it's insufficient by design, not by poor execution. It has no branching, no probability, and no evidence-weighing built in at all.

## 7.5 Fishbone / Ishikawa

*[ESTABLISHED ENGINEERING KNOWLEDGE]* A cause-and-effect diagram organizing candidate causes into standard categories — classically **people, process, machine, material, environment, measurement** — branching off a central "spine" pointing at the effect being investigated. Adapted to elevator diagnosis, the categories might become: technician/procedural factors, control/software behavior, mechanical components, material degradation (wear, corrosion), environmental conditions (temperature, humidity, usage pattern), and sensor/measurement issues.

**Strengths:** genuinely useful for brainstorming — a team walking through a Fishbone diagram is unlikely to entirely miss a whole category of cause. Good for structuring a human investigation meeting.

**Limitations:** categorical rather than probabilistic (it lists candidates; it doesn't rank them), weak temporal representation (no sense of sequence or timing), weak sensor-evidence integration (a Fishbone diagram doesn't naturally connect a branch to the specific telemetry that would confirm or deny it), doesn't naturally rank competing causes, and doesn't establish causality formally — it's a checklist of "things worth considering," not a model of how they actually produce the observed effect.

**Why the roadmap recommends moving past generic Ishikawa categories:** "machine," "material," "environment" are useful for a *general* manufacturing-defect investigation, but they don't map naturally onto elevator subsystems the way this project needs. A branch labeled "machine" that has to cover the motor, the drive, the brake, the doors, and the traction system simultaneously is less useful than six separate, elevator-subsystem-specific fault trees (§7.7) — which is exactly the alternative structure this chapter builds instead.

---

# Part III — Fault Tree Analysis, In Depth

## 7.6 Fault Tree Analysis Fundamentals

*[ESTABLISHED ENGINEERING KNOWLEDGE]* A fault tree represents a single **top event** (the failure being investigated) and works backward, branching into the conditions that could produce it, down to **basic events** — the lowest-level causes the tree doesn't decompose any further.

- **Top event** — the failure under investigation (e.g., "Motor Overcurrent").
- **Intermediate event** — a failure category one level below the top event, itself caused by something further down (e.g., "Mechanical Excessive Load").
- **Basic event** — a root-level cause the tree doesn't break down further (e.g., "Mechanical obstruction in the hoistway").
- **OR gate** — the event above occurs if **any one** of the events below it occurs. Most of the branching in this chapter's elevator fault trees uses OR logic, because in practice almost any one of several distinct physical problems is independently sufficient to produce a given elevator symptom.
- **AND gate** — the event above occurs only if **all** of the events below it occur together. Less common in the trees below, but conceptually important — e.g., a specific *false* safety trip might require both a marginal sensor condition **and** a specific environmental trigger occurring simultaneously, rather than either alone being sufficient.
- **Minimal cut sets** — the smallest combinations of basic events that, together, are sufficient to cause the top event. For a tree that's entirely OR-gated, every basic event is its own minimal cut set (any single one is independently sufficient).
- **Qualitative FTA** — building the tree's logical structure without assigning probabilities; useful for understanding *what* could cause a failure.
- **Quantitative FTA** — assigning a probability to each basic event and propagating those probabilities up through the gates to estimate the probability of the top event. (OR gates combine probabilities additively-ish, for rare/independent events roughly `P(A or B) ≈ P(A) + P(B)`; AND gates combine them multiplicatively, `P(A and B) = P(A) × P(B)` for independent events.)

```
TOP EVENT
   │
   ├── Intermediate Event A (OR)
   │      ├── Basic Event 1
   │      └── Basic Event 2
   ├── Intermediate Event B (OR)
   │      ├── Basic Event 3
   │      └── Basic Event 4
   └── Intermediate Event C (OR)
          └── Basic Event 5
```

## 7.7 Six Elevator-Specific Fault Trees

Each tree below reuses the engineering reasoning already established in Chapters 2–6 of this book, now formalized into proper fault-tree structure. **[ENGINEERING INFERENCE, grounded in Chapters 1–3's mechanical/electrical foundations]** — none of these trees claim to be KONE's actual internal fault taxonomy (Ch.4 §4.23's Research Gap still applies in full).

### 7.7.1 Motor Overcurrent

```
MOTOR OVERCURRENT
   │
   ├── Mechanical Excessive Load (OR)
   │      ├── Mechanical obstruction
   │      ├── Brake drag
   │      ├── Traction/rope problem (increased friction demand)
   │      ├── Counterweight imbalance / genuine excessive load
   │      └── Guide-shoe/rail binding
   │
   ├── Motor Electrical Fault (OR)
   │      ├── Winding insulation breakdown
   │      ├── Progressive winding degradation (temperature-related)
   │      └── Other motor internal fault
   │
   ├── Drive/Inverter Fault (OR)
   │      ├── IGBT failure
   │      ├── Current-sensing fault
   │      ├── Gate-driver fault
   │      └── Other inverter abnormality
   │
   ├── Cable/Connection Fault (OR)
   │      └── Loose or partially-shorted motor cabling
   │
   └── Configuration/Parameter Issue (OR)
          └── Drive parameters mismatched to the installed motor
```

**Evidence-linked extension** — this is the upgrade the roadmap explicitly calls for: a fault tree alone tells you *what could* be wrong; attaching evidence to each branch tells you *what would confirm or deny it*.

| Branch | Expected Evidence |
|---|---|
| Mechanical obstruction | Current↑ correlated with motion attempts; vibration↑; clean drive self-test |
| Brake drag | Current↑ correlated with brake-release timing; possible position drift |
| IGBT / drive fault | Current abnormality *and* drive-temperature abnormality *and* a failed drive self-test |
| Winding fault | Phase-current imbalance independent of load or motion state; elevated motor temperature |
| Cable fault | Intermittent/erratic current, often vibration-correlated |
| Configuration issue | Persistent, systematic elevated current from a known configuration-change point forward; clean hardware self-test |

> **DIAGNOSTIC INSIGHT:** Notice that a fault tree by itself is symmetric — every branch looks equally plausible until evidence is attached. The moment evidence is attached, the tree stops being a static diagram and becomes the skeleton of a genuine diagnostic reasoning process. This is the transition §7.14 onward formalizes mathematically.

### 7.7.2 Door Failure

```
DOOR FAILURE
   │
   ├── Obstruction-Related (OR)
   │      ├── Genuine physical obstruction
   │      └── Photo-eye degradation (false obstruction detection)
   │
   ├── Drivetrain-Related (OR)
   │      ├── Roller wear
   │      ├── Door belt wear/slip
   │      └── Track misalignment or debris
   │
   ├── Door Motor Fault (OR)
   │      └── Winding/mechanical wear in the door operator motor
   │
   ├── Feedback-Related (OR)
   │      └── Door encoder fault
   │
   ├── Lock/Interlock Fault (OR)
   │      └── Contact wear or misalignment
   │
   └── Controller/Electrical Issue (OR)
          └── Door-control logic or wiring fault
```

Evidence per branch (condensed, reusing Chapter 4 §4.9's differential table): photo-eye instability across many cycles vs. a single repeatable obstruction event; elevated door-motor current with longer cycle time (rollers/track); panel-position mismatch (belt); position-vs-commanded deviation (encoder); lock-state instability (interlock); communication-error indicators with no positional pattern (controller/electrical).

> **Why This Matters to KONE Elevate RCA:** One "door fault" alarm, six structurally distinct subsystems, each with a nearly identical top-level symptom (repeated reopening, elevated cycle time). This tree is the formal version of Chapter 4 §4.9's central finding.

### 7.7.3 Leveling Error

```
LEVELING ERROR
   │
   ├── Position-Feedback Related (OR)
   │      ├── Encoder drift/fault
   │      └── Independent leveling-sensor fault
   │
   ├── Motion-Related (OR)
   │      ├── Rope stretch/slip (genuine position discrepancy)
   │      └── Traction/sheave wear
   │
   ├── Brake-Related (OR)
   │      └── Brake timing deviation affecting final-stop precision
   │
   └── Controller-Related (OR)
          └── Calibration/interpretation error in the control loop
```

**The key diagnostic question this tree exists to answer** (Chapter 3 §3.7's fifth worked example, now formalized): does an independent leveling sensor **agree** with the encoder (suggesting the deviation is real motion — rope/sheave branches) or **disagree** with it (suggesting the encoder itself is the fault)?

### 7.7.4 Brake Fault

```
BRAKE FAULT
   │
   ├── Coil-Related (OR)
   │      └── Brake coil degradation/failure
   │
   ├── Mechanical Wear (OR)
   │      └── Lining/pad wear
   │
   ├── Adjustment/Timing (OR)
   │      ├── Brake release timing deviation
   │      └── Brake engage timing deviation
   │
   ├── Monitoring/Sensor Issue (OR)
   │      └── Brake-timing or torque-sensor fault (the monitoring system itself, not the brake)
   │
   └── Control Issue (OR)
          └── Brake-control logic/wiring fault
```

**A brake problem may appear as another subsystem's abnormality** — the theme established in Chapter 3 §3.2 and reinforced throughout this book. A brake fault can produce motor-current abnormalities (drag → elevated current), position abnormalities (drag or premature/late engagement → drift), motion abnormalities (juddering during release/engage transitions), and stopping abnormalities (imprecise final leveling). None of these four symptom categories, on their own, obviously points back to the brake — which is exactly why this fault tree, and its evidence links, need to exist explicitly rather than being left to intuition.

### 7.7.5 Encoder / Position Feedback Fault

```
ENCODER / POSITION FEEDBACK FAULT
   │
   ├── Hardware-Related (OR)
   │      ├── Encoder component wear/degradation
   │      └── Contamination
   │
   ├── Signal/Wiring-Related (OR)
   │      └── Connector or cable fault (intermittent, often vibration-correlated)
   │
   ├── Alignment-Related (OR)
   │      └── Physical misalignment (reproducible pattern tied to rotor position)
   │
   └── Interpretation-Related (OR)
          └── Controller-side calibration/interpretation error (the raw signal is fine; the derived value isn't)
```

This is the formal version of Chapter 4 §4.10's alternative-cause table — the same four branches, now expressed as fault-tree structure with the distinguishing evidence attached to each.

### 7.7.6 Safety-Chain Trip

```
SAFETY-CHAIN TRIP
   │
   ├── Genuine Safety-Relevant Condition (OR)
   │      └── A real condition the safety chain is specifically designed to catch
   │
   └── Sensing/Contact Degradation (OR)
          └── A component within the safety chain itself producing a false trip
```

This tree is deliberately shallow, and deliberately stops here. Consistent with Chapter 4 §4.7-G and this book's safety boundary throughout, this book does not decompose safety-chain internals further, does not describe what specific conditions the chain monitors in implementation detail, and absolutely does not describe how any part of a safety chain could be bypassed, defeated, or worked around — none of that has diagnostic value, and all of it has real potential for harm. What matters diagnostically is only the two-branch distinction above: **is this event evidence of a real hazard, or evidence of a degrading safety-chain component?** — and, per Chapter 4 §4.7-G, resolving that distinction is explicitly **always** human/qualified-technician territory, never something this project's AI layer acts on unilaterally. Full safety-standards treatment (EN 81, IEC 61508, and related material) comes later in this research book.

---

# Part IV — FMEA and Related Methods

## 7.8 Failure Mode and Effects Analysis (FMEA)

*[ESTABLISHED ENGINEERING KNOWLEDGE]* Where a fault tree works top-down (start with a failure, find its causes), FMEA works bottom-up: start with a **component**, enumerate everything it could plausibly do wrong, and trace each failure mode forward to its effects.

Core FMEA fields: **component**, **function** (what it's supposed to do), **failure mode** (how it fails), **cause** (why that failure mode occurs), **effect** (what happens as a result — distinguished as **local effect**, the immediate consequence, versus **system effect**, the consequence at the whole-elevator level), **detection method** (how the failure would be noticed), and — in quantitative FMEA — **severity**, **occurrence**, and **detectability** ratings, combined into a **Risk Priority Number (RPN)**.

**A stated scoring methodology, used consistently below, and explicitly not a claim about KONE's own methodology:** a simple 1–5 scale for each of the three ratings. Severity: 1 = negligible, 5 = safety-relevant or total loss of service. Occurrence: 1 = rare, 5 = frequent. Detectability: 1 = easily caught before failure, 5 = very difficult to detect in advance — **note the inversion**: a *high* detectability score means *poor* detectability (hard to catch), which is the standard (if often confusing) FMEA convention. RPN = Severity × Occurrence × Detectability, ranging 1–125; higher RPN means higher priority for design or maintenance attention.

| Component | Function | Failure Mode | Cause | Effect | Detection | Sev. | Occ. | Det. | RPN | Recommended Action |
|---|---|---|---|---|---|---|---|---|---|---|
| Motor | Produce torque | Winding insulation breakdown | Age, thermal stress | Overcurrent, uneven running | Phase-current imbalance | 4 | 2 | 3 | 24 | Periodic insulation-resistance testing |
| IGBT / drive | Switch DC bus to synthesize motor AC supply | Short/open failure | Thermal stress, component aging | Drive trip, elevator out of service | Drive self-test | 4 | 2 | 2 | 16 | Drive temperature trending |
| Brake | Hold car stationary; provide holding torque | Incomplete release / drag | Wear, misadjustment, coil degradation | Overcurrent, accelerated wear, leveling deviation | Brake-timing correlation with current | 5 | 3 | 3 | 45 | Brake timing/torque monitoring; scheduled inspection |
| Encoder | Report position/speed | Signal drift/dropout | Contamination, connector wear | Rough control, leveling inaccuracy | Independent leveling-sensor cross-check | 3 | 2 | 3 | 18 | Periodic signal-quality check |
| Door motor | Drive door panel motion | Weak/inconsistent movement | Winding/mechanical wear | Slow/incomplete cycles | Elevated door-motor current | 2 | 3 | 2 | 12 | Current-trend monitoring |
| Door roller | Guide door panel along track | Wear | Cyclic mechanical stress | Slow/noisy door movement | Cycle-time trend | 2 | 4 | 2 | 16 | Scheduled roller inspection/lubrication |
| Door belt | Transmit door-motor motion to panel(s) | Wear/stretch/slip | Cyclic stress, age | Inconsistent panel sync | Panel-position mismatch | 2 | 3 | 3 | 18 | Belt-tension inspection |
| Photo-eye | Detect door-path obstruction | Alignment/lens drift | Age, contamination, vibration | False obstruction detection, repeated reopening | Multi-cycle instability pattern | 3 | 3 | 3 | 27 | Periodic alignment check |
| Door lock/interlock | Confirm safe locked state before motion | Contact wear/misalignment | Cyclic mechanical stress | Repeated reopening, safety-circuit-open | Lock-state signal instability | 5 | 2 | 2 | 20 | Contact inspection; safety-relevant priority regardless of RPN |
| Traction sheave | Transfer rotational motion to ropes via friction | Groove wear | Cyclic loading, age | Rope slip under load, position deviation | Load-dependent speed/position mismatch | 3 | 2 | 3 | 18 | Groove-wear inspection |
| Rope/belt | Transmit sheave motion to car/counterweight | Wear, fatigue, uneven elongation | Age, cyclic loading | Uneven load sharing, vibration, position drift | Vibration-signature change | 5 | 2 | 3 | 30 | Scheduled rope inspection (safety-relevant, code-governed) |
| Leveling/position system | Confirm precise floor alignment | Sensor drift/contamination | Age, contamination | Imprecise floor stop | Consistent small position offset | 3 | 2 | 2 | 12 | Periodic sensor check |

**Note the pattern in the RPN column:** brake drag (45) and rope wear (30) rank highest — not necessarily because they're the most *frequent* failures in this illustrative table, but because their **severity** rating is high (both are safety-relevant) and their **detectability** is moderate (neither is trivially obvious before it manifests as a symptom). This is FMEA doing exactly what it's designed to do: surfacing components where the combination of consequence and detection difficulty deserves attention, not just components that fail often.

> **RESEARCH GAP:** These severity/occurrence/detectability scores are the authors' own illustrative engineering judgment, using the stated 1–5 methodology above, for teaching purposes. Real occurrence and detectability rates depend on actual field failure data KONE has not published (Ch.4 §4.23). Never present this specific table as KONE production FMEA data.

## 7.9 FMEA vs. FTA

| Characteristic | FMEA | FTA |
|---|---|---|
| Direction | Bottom-up (component → failure mode → effect) | Top-down (failure → possible causes) |
| Starting point | A component | A specific top-level failure |
| Coverage | Broad — every failure mode of every component | Narrow — only the causes of one specific top event |
| Best for | Building a comprehensive static knowledge base | Investigating one specific observed failure |
| Natural output | A prioritized list (via RPN) of what deserves attention | A structured hypothesis space for one investigation |

**Why they complement each other, and why this project needs both:** FMEA answers "what can fail, and how worried should we be, in general" — building the static knowledge base (§7.22) ahead of time. FTA answers "given that *this specific* top event just occurred, what are the live candidate explanations" — the structure an actual investigation runs on. Chapter 3 §3.6's Master Failure → Evidence Matrix was, in effect, an FMEA-flavored artifact; §7.7's six trees are the FTA-flavored counterpart, built from the same underlying component knowledge.

## 7.10 FMECA

*[ESTABLISHED ENGINEERING KNOWLEDGE]* FMECA (Failure Mode, Effects, and **Criticality** Analysis) extends FMEA by combining severity and probability/frequency into an explicit **criticality** ranking, used to prioritize which failure modes deserve design attention or more intensive maintenance focus, beyond FMEA's basic RPN. For this project's purposes, FMECA is functionally an emphasis shift within the same table structure §7.8 already built — using severity × occurrence specifically (leaving detectability as a separate consideration) to rank criticality for maintenance-planning purposes, distinct from RPN's use in prioritizing where better detection methods are needed. **No arbitrary criticality values are assigned here beyond the illustrative FMEA scores already stated and labeled in §7.8** — a real criticality ranking would require real KONE failure-frequency data this book does not have.

## 7.11 Event Tree Analysis (ETA)

*[ESTABLISHED ENGINEERING KNOWLEDGE]* Where a fault tree asks **"what causes this failure?"**, an event tree asks **"what could happen *after* this initiating event, depending on whether protective functions succeed or fail?"** — it works forward in time from a starting point, not backward from an outcome.

**Conceptual elevator example**, starting from the initiating event "motor overcurrent detected":

```
Motor overcurrent detected
   │
   ├── Drive protective trip succeeds → Motion stops safely →
   │       Leveling/safety events follow per Ch.4 §4.6's cascade pattern
   │
   └── Drive protective trip fails to engage (hypothetical, illustrative) →
           More severe downstream consequence (illustrative branch only —
           this book does not claim any specific KONE protective-response
           failure rate or scenario)
```

ETA is more naturally suited to **safety and consequence analysis** ("if this goes wrong, how bad could it get, and did the safety systems work as intended") than to root-cause diagnosis of an *already-occurred* fault, which is why it plays a supporting role in this chapter rather than a central one — it's the right tool for reliability/safety engineering asking "what if," not for RCA asking "why did."

## 7.12 Bow-Tie Analysis

*[ESTABLISHED ENGINEERING KNOWLEDGE]* Bow-Tie Analysis puts a single top event at the center and combines a fault tree on the left (threats → top event, i.e., causes) with an event tree on the right (top event → consequences), visually resembling a bow tie. It adds explicit **preventive barriers** (controls that stop a threat from causing the top event) on the left side and **mitigating barriers** (controls that limit the consequences once the top event has occurred) on the right side.

**Conceptual elevator example:** Threat (mechanical obstruction) → [preventive barrier: none really available for a foreign object, which is why this branch flows through] → Top event (motor overcurrent) → [mitigating barrier: drive overcurrent protection] → Consequence (controlled trip and stop, rather than sustained damage).

Bow-Tie is genuinely useful for visualizing the *whole* risk picture — causes, barriers, and consequences together — but this book deliberately does **not** adopt it as the project's main RCA framework, consistent with the roadmap's own recommendation: Bow-Tie is barrier/risk-management-oriented, not evidence-weighing-oriented, and doesn't naturally represent the probabilistic, multi-hypothesis reasoning §7.14 onward builds.

---

# Part V — Causal and Probabilistic Reasoning

## 7.13 Causal Graphs

*[ESTABLISHED ENGINEERING KNOWLEDGE]* A causal graph represents cause-and-effect relationships as nodes (events/states) connected by directed edges (influence relationships) — a more general, flexible structure than a fault tree's strict hierarchy, capable of representing a cause that contributes to multiple effects, or an effect with contributions from multiple independent causes, in one unified diagram.

```
Mechanical obstruction → Mechanical resistance → Motor torque demand
        → Motor current → Drive overcurrent → Elevator trip
```

**Why this representation matters — correlation vs. causation, precisely:** two variables are **correlated** if they tend to occur together (A and B are observed together more often than chance alone would predict). Two variables are in a **causal** relationship if A actually influences B through some real mechanism — the arrow in the diagram above represents a specific physical mechanism at each step (increased resistance genuinely requires more torque; more torque genuinely requires more current), not just a statistical pattern noticed in past data.

**Why temporal correlation alone is insufficient to establish causation** — this is Chapter 4 §4.12's principle, now given its formal justification: two events occurring close together in time are *consistent with* a causal relationship, but the same pattern would also be produced by (a) genuine causation, (b) both events sharing an unobserved common cause, or (c) pure coincidence. A causal graph, built from real engineering knowledge of the physical mechanisms involved (exactly what Chapters 1–3 of this book established), is what lets a system distinguish "these are connected because I know the mechanism" from "these merely happened close together."

## 7.14 Bayesian Reasoning

This is the deepest, most mathematically important section in the chapter — the formal machinery behind every "P(Cause | Evidence)" reference in this entire book, explained from first principles.

**The starting problem.** Given an observation (motor overcurrent) and a set of candidate hypotheses (H1 through H7, §7.15), how should new pieces of evidence change how much we believe in each one?

**Bayes' theorem, in words before symbols:** the probability that a hypothesis is true, *given* what we've observed, depends on three things — how likely that hypothesis was *before* we saw the evidence, how likely the evidence would be *if* that hypothesis were true, and how likely the evidence would be overall (across every hypothesis, not just this one).

**In symbols:**

**P(H | E) = [ P(E | H) × P(H) ] / P(E)**

Reading each term individually:

- **P(H)** — the **prior probability**: how likely this hypothesis is *before* considering the new evidence (based on general base rates — how often this kind of failure typically occurs).
- **P(E | H)** — the **likelihood**: if this hypothesis were true, how probable is it that we'd observe exactly this evidence?
- **P(E)** — the probability of observing this evidence *at all*, across every hypothesis under consideration — a normalizing factor that ensures the resulting probabilities across all hypotheses sum to 1.
- **P(H | E)** — the **posterior probability**: the updated belief in this hypothesis, *after* folding in the evidence. This is the number the system actually wants.

**For comparing multiple hypotheses**, the normalizing term P(E) is the same for every hypothesis being compared, so it's often more useful to work with the proportional form:

**P(H | E) ∝ P(E | H) × P(H)**

— "posterior is proportional to likelihood times prior" — then normalize across all hypotheses at the end so they sum to 1.

**For multiple, independent pieces of evidence** (E1, E2, E3, ...), the likelihoods combine multiplicatively:

**P(H | E1, E2, E3, ...) ∝ P(H) × P(E1 | H) × P(E2 | H) × P(E3 | H) × ...**

**This is the version worth being careful with.** That multiplication is only mathematically valid if the evidence pieces are **conditionally independent given the hypothesis** — a condition that, as §7.16 explains in detail, elevator evidence frequently violates.

> **KEY CONCEPT:** The entire point of this machinery is captured in one line, already stated in Chapter 2: reason in terms of **P(Cause | Evidence)**, never `IF alarm = X THEN cause = Y`. A rule-based lookup treats every case as certain; Bayesian reasoning treats every case as a *degree of belief*, updated incrementally as evidence arrives — which matches how real diagnosis actually works, one clue at a time, rarely with total certainty.

## 7.15 Worked Bayesian Example: Motor Overcurrent

**Illustrative example only — not production KONE probabilities**, restated as a permanent label on every number in this section.

**Hypotheses** (from §7.7.1's fault tree, condensed to seven top-level branches):

- H1 — Mechanical obstruction
- H2 — Brake drag
- H3 — Motor winding fault
- H4 — Cable fault
- H5 — IGBT/drive fault
- H6 — Excessive load
- H7 — Parameter/configuration issue

**Illustrative priors** (before any evidence beyond "motor overcurrent occurred"), reflecting a rough, illustrative sense that mechanical and load-related causes are somewhat more common in practice than hardware winding/IGBT failures, and that configuration issues, while less frequent, aren't rare:

| Hypothesis | Illustrative Prior |
|---|---|
| H1 Mechanical obstruction | 0.25 |
| H2 Brake drag | 0.15 |
| H3 Motor winding fault | 0.10 |
| H4 Cable fault | 0.08 |
| H5 IGBT/drive fault | 0.12 |
| H6 Excessive load | 0.20 |
| H7 Parameter/config issue | 0.10 |

**Now fold in evidence, one piece at a time:**

**Evidence A — Current↑.** This is, deliberately, the *least* informative piece of evidence available, and that's worth stating explicitly as a teaching point: every one of the seven hypotheses was selected specifically *because* it plausibly produces elevated current. P(Evidence A | Hi) is roughly high for all seven — so the posterior after Evidence A alone looks almost identical to the prior. **The alarm that triggered the investigation barely updates the investigation at all.**

**Evidence B — Vibration↑.** Now genuinely informative: strongly expected under H1 (an obstruction) and H6 (load-related imbalance), moderately expected under H2 (brake-drag judder), and weakly expected under H3/H4/H5/H7 (electrical-only causes don't typically produce a strong vibration signature). Illustrative effect: mass shifts toward H1 and H6, somewhat toward H2, away from H3/H4/H5/H7.

**Evidence C — Drive temperature normal.** Evidence *against* H5 specifically (an IGBT/drive fault would typically run hot). Illustrative effect: H5's posterior drops further.

**Evidence D — Drive self-test normal.** Reinforces the case against H5, and to a lesser extent H4 (a severe cable fault might also trigger self-test flags). Illustrative effect: H5 drops further still; H4 drops slightly.

**Evidence E — Brake timing abnormal.** Strong, specific evidence *for* H2 — this is the one piece of evidence that directly, uniquely implicates a single hypothesis rather than shifting weight among several.

**Illustrative posterior ranking after all five pieces of evidence** (again: illustrative, not calculated from real data, and presented as relative ordering rather than false-precision decimals):

1. **H2 Brake drag** — promoted to the leading hypothesis, on the strength of Evidence E specifically, with partial support from Evidence B.
2. **H1 Mechanical obstruction** — still strongly plausible, supported by Evidence B, not contradicted by anything.
3. **H6 Excessive load** — still plausible (Evidence B partially supports it), but not specifically confirmed by anything.
4. **H3, H4, H7** — reduced but not eliminated; no direct evidence for or against most of them in this set.
5. **H5 IGBT/drive fault** — pushed to the bottom, contradicted twice (Evidence C and D).

> **WORKED EXAMPLE takeaway:** Watch how the ranking changed *shape*, not just position — H5 moved because it was directly **contradicted**, twice, by independent evidence; H2 moved because it was directly **confirmed** by one highly specific piece of evidence; H1 and H6 moved only slightly, supported by evidence that doesn't distinguish well between them. This differential pattern — some hypotheses eliminated by contradiction, one promoted by specific confirmation, others left genuinely tied — is a more honest and more useful output than a single point estimate would be.

## 7.16 Correlated Evidence and the Double-Counting Problem

The multiplicative evidence-combination formula in §7.14 assumed the evidence pieces were **conditionally independent given the hypothesis.** This assumption frequently fails in elevator diagnosis, and naively multiplying non-independent likelihoods leads to **overconfidence** — a false sense of certainty the evidence doesn't actually support.

**Concrete example:** motor current↑ and motor torque↑ are not two independent observations — under the physics established in Chapter 1 §1.5 (T ≈ k · I_q), they are, almost by definition, restatements of the same underlying fact. Treating them as two separate, independent confirmations of a hypothesis and multiplying their likelihoods together **double-counts** the same evidence, inflating confidence beyond what's actually justified. The same problem arises between a drive trip and the overcurrent event that caused it (Ch.4 §4.5) — they aren't independent evidence of a shared upstream cause; one is a direct, near-deterministic consequence of the other.

**What a responsible system must do instead:** recognize which pieces of evidence are genuinely independent measurements of different physical quantities, and which are correlated/redundant measurements of essentially the same underlying fact — collapsing or down-weighting the redundant ones before combining likelihoods, rather than multiplying every available signal as if each were an independent confirmation.

> **EVIDENCE WARNING:** This is one of the most consequential, easy-to-get-wrong details in the entire probabilistic-reasoning toolkit. A system that doesn't account for evidence correlation will report confidence scores that look impressively precise and are, in fact, systematically inflated — which is arguably worse than reporting honest uncertainty, since it actively misleads a technician into trusting a conclusion more than the underlying evidence warrants.

> **Why This Matters to KONE Elevate RCA:** This is a direct, technical justification for why confidence calibration (flagged throughout this book, including in KONE's own stated design priorities, Ch.5 §5.10) is a genuinely hard problem, not a bolt-on feature — getting it right requires an explicit model of which evidence sources are independent, which requires the causal-graph structure from §7.13, not just a list of signals.

## 7.17 Dynamic Bayesian Networks

*[ESTABLISHED ENGINEERING KNOWLEDGE]* Everything in §7.14–§7.16 reasoned about a single snapshot in time. Elevator diagnosis is inherently **temporal** — the same static Bayesian picture, evaluated at successive moments, can look very different, and the *pattern of change itself* carries diagnostic information (Ch.4 §4.12's chronology argument, now extended into a formal model).

```
t0   Normal
t1   Vibration increases
t2   Motor current increases
t3   Overcurrent event (alarm raised)
t4   Drive trip
t5   Position deviation
```

A **Dynamic Bayesian Network** represents this as a sequence of linked Bayesian networks, one per time step, where each step's beliefs are informed both by new evidence at that step *and* by the belief state carried forward from the previous step — rather than treating each moment as an isolated, memoryless snapshot. Conceptually, this lets the system distinguish, for example, a **gradual** rise in current over many trips (consistent with wear-based degradation — pointing toward brake or rope wear) from a **sudden** jump within a single trip (more consistent with a discrete event, like an obstruction appearing) — the same final current reading, but a materially different diagnostic story depending on the trajectory that led there.

This chapter deliberately keeps the mathematics conceptual rather than deriving the full transition/observation-model formalism — the goal here is that the team understands *why* time matters formally, not that every member can derive a DBN's transition equations from scratch.

## 7.18 Markov Models

*[ESTABLISHED ENGINEERING KNOWLEDGE]* A simpler, related idea: model a component's health as moving through a small number of discrete **states** — for example, **Healthy → Degraded → Faulted** — with a **transition probability** governing how likely the component is to move from one state to the next within a given time window. **State estimation** is then the task of inferring which state a component is most likely in, given the evidence observed so far.

```
Healthy ──(transition prob.)──> Degraded ──(transition prob.)──> Faulted
```

**The key limitation, stated honestly:** the defining "Markov assumption" — that the probability of the *next* state depends only on the *current* state, not on the full history that led there — is often too simplistic for real elevator components, whose degradation frequently depends on accumulated usage history (total cycles, load patterns, maintenance history — Ch.5 §5.16), not just their instantaneously-observed present condition. **When Markov models remain useful anyway:** as one simplified input signal among several within a larger reasoning system (e.g., a rough wear-progression indicator feeding into the broader evidence-weighing process), rather than as the sole or primary diagnostic mechanism.

## 7.19 Reliability Block Diagrams (RBD)

*[ESTABLISHED ENGINEERING KNOWLEDGE]* An RBD represents how component reliability combines into overall system reliability, using **series** connections (the system fails if *any* block in the series fails — directly analogous to fault-tree OR logic) and **parallel/redundant** connections (the system only fails if *all* parallel blocks fail — analogous to AND logic, representing genuine redundancy).

**Why RBD is more naturally suited to system-reliability analysis than to direct root-cause diagnosis, and why this distinction matters:** RBD answers "how reliable is this system, given what we know about each component's individual reliability" — a forward-looking, aggregate, design-and-planning question. It does not naturally answer "given that a failure has already occurred, which specific component is responsible" — the backward-looking, single-incident question this entire chapter is about. RBD is the right tool for Chapter 5's asset-planning context (KONE 24/7 Planner, §5.8) or for a future reliability-centered-maintenance analysis, not for this project's core RCA reasoning loop.

---

# Part VI — Synthesis

## 7.20 The Comparative RCA Framework

Now that all thirteen methods have been taught individually, they can be meaningfully compared:

| Method | Main Question | Represents Causality? | Handles Probability? | Handles Time? | Handles Multiple Causes? | Elevator RCA Suitability |
|---|---|---|---|---|---|---|
| 5 Whys | Why, iteratively | Weakly (implicit) | No | No | No (single chain) | Low — human investigation only |
| Fishbone/Ishikawa | What categories of cause exist | No | No | No | Yes (lists, doesn't rank) | Low — brainstorming only |
| Fault Tree Analysis | What causes this top event | Yes (structurally) | Yes (quantitative FTA) | No | Yes | **High** — foundational |
| FMEA | What can this component do wrong | Yes (per row) | Via RPN, weakly | No | Yes (across rows) | **High** — foundational knowledge base |
| FMECA | Same as FMEA, prioritized | Yes | Yes (criticality) | No | Yes | Moderate — planning-oriented |
| Event Tree Analysis | What happens after this event | Yes (forward) | Yes | Partially | Yes (branches) | Moderate — consequence/safety-oriented |
| Bow-Tie | Causes + consequences + barriers | Yes | Weakly | No | Yes | Moderate — risk-communication-oriented |
| Causal graphs | How are events physically related | **Yes, explicitly** | Can be combined with probability | Can be extended | Yes | **High** — the structural backbone |
| Bayesian Networks | Given evidence, which cause is likely | Via structure | **Yes, centrally** | No (static) | Yes, ranked | **High** — the reasoning engine |
| Dynamic Bayesian Networks | Same, evolving over time | Via structure | Yes | **Yes, centrally** | Yes, ranked | **High** — for temporal evidence |
| Markov models | What state is this component in | Weakly | Yes | Yes (simplified) | No (single component) | Moderate — one input signal |
| Reliability Block Diagrams | How reliable is the system | No (aggregate only) | Yes | No | N/A | Low for RCA; useful for planning |

**Foundational** (directly load-bearing for this project's architecture): Fault Tree Analysis, FMEA, causal graphs, Bayesian Networks.
**Supporting** (feed into or extend the foundational methods): FMECA, Dynamic Bayesian Networks, Markov models.
**Advanced/contextual** (useful background, not core to this project's specific RCA design): 5 Whys, Fishbone, Event Tree Analysis, Bow-Tie, Reliability Block Diagrams.

## 7.21 Why One Method Is Not Enough

No single method from §7.20's table covers the full reasoning process this project needs. A realistic diagnostic workflow combines several, each doing the part it's actually good at:

- **FMEA** answers *"what can fail?"* — the static knowledge base, built once, reused across every investigation.
- **Fault Tree** answers *"how can this specific top-level fault occur?"* — the structured hypothesis space for one investigation.
- **Causal graph** answers *"how are these events physically related?"* — the justification for why temporal proximity should (or shouldn't) count as evidence.
- **Time-series evidence** answers *"when did the behavior change, and how?"* — the raw material Chapter 6 of this book (Phase 6) will focus on extracting reliably.
- **Bayesian reasoning** answers *"given all available evidence, which cause is most plausible, and how confident should we be?"* — the final integration step.

**This combination — not any single method in isolation — is the conceptual architecture of this project's RCA reasoning layer.**

## 7.22 Static Knowledge vs. Dynamic Evidence

A distinction load-bearing for everything that follows in this book:

**Static engineering knowledge** — things true regardless of what's happening on any specific elevator right now: component relationships (Chapters 1–3), known failure modes (§7.8's FMEA), fault-tree structure (§7.7), engineering constraints (physics established in Ch.1 §1.5). This doesn't change investigation to investigation.

**Dynamic operational evidence** — things specific to this particular fault episode, right now: sensor values, alarms, event chronology, current operating conditions, maintenance history (Ch.5 §5.16). This is different every time.

**STATIC KNOWLEDGE + DYNAMIC EVIDENCE = CONTEXTUAL DIAGNOSIS.** Neither alone is sufficient — static knowledge without live evidence is just a textbook; live evidence without static knowledge is just a stream of numbers with no way to interpret what they mean. This is one of the most important conceptual foundations for the AI architecture chapters later in this book, because it maps directly onto a design decision already flagged as far back as the Understanding Report: the system should combine **deterministic, rule-based retrieval** (the static knowledge) with **AI-assisted reasoning** (working over dynamic evidence) — never a single general-purpose model expected to hold and apply both from memory alone.

---

# Part VII — The Reasoning Process Itself

## 7.23 Hypothesis Generation

Given an observation (e.g., motor overcurrent), the system should generate the **full** candidate hypothesis set from the relevant fault tree — H1 through H7, §7.7.1 — not stop at the first plausible one. **The system should not immediately select a hypothesis. It should investigate.** This single sentence is arguably the most important behavioral instruction in the whole chapter, and it's worth being explicit about why: premature selection is exactly the diagnostic failure mode Chapter 4 §4.18 named first ("treating the alarm as the root cause") and last ("concluding without sufficient evidence") — hypothesis generation exists specifically to keep the investigation open long enough for evidence to actually do its job.

## 7.24 Hypothesis Testing

```
Hypothesis
   ↓
Expected evidence (what would we see if this were true?)
   ↓
Observed evidence (what did we actually see?)
   ↓
Support or Contradiction
   ↓
Updated hypothesis confidence
```

| Hypothesis | Expected Evidence | Observed Evidence | Supports? | Contradicts? |
|---|---|---|---|---|
| H2 Brake drag | Current↑ correlated with brake-release timing | Brake timing abnormal (Evidence E) | Yes | — |
| H5 IGBT/drive fault | Drive temp↑, failed self-test | Drive temp normal, self-test normal | — | Yes (twice) |
| H1 Mechanical obstruction | Vibration↑, clean self-test | Vibration↑ present, self-test clean | Yes | — |

**Good RCA is not simply finding supporting evidence for a favored hypothesis.** It requires actively searching for evidence that would *contradict* each hypothesis, too — the H5 row above is the more diagnostically valuable one precisely because it demonstrates the contradiction search working, not just the confirmation search.

## 7.25 Alternative-Cause Elimination

Using the same motor-overcurrent example, the discipline this section formalizes as a repeatable procedure, run for *every* live hypothesis, not just the leading one:

1. **What evidence would we expect if this specific hypothesis were true?**
2. **Is that evidence present?**
3. **What evidence would contradict this specific hypothesis?**
4. **Is contradictory evidence present?**

Repeated for H1 through H7 in §7.15's worked example, this procedure is what actually produced the ranking shown there — H5 wasn't just "less supported," it was **actively contradicted** on two separate, independent counts (Evidence C and D), which is a meaningfully stronger and more defensible basis for demotion than simply noting an absence of supporting evidence.

**Why this is stronger than "find evidence supporting the first plausible explanation":** the latter approach can produce a confident-sounding conclusion that happens to be wrong, simply because nobody checked whether the evidence was *equally* consistent with a different, unexamined hypothesis. Systematic elimination closes that gap by construction — every live hypothesis gets the same scrutiny, not just the one that occurred to the investigator first.

## 7.26 Negative Evidence

**"No vibration increase." "No abnormal brake timing." "No drive-temperature anomaly." "No evidence of mechanical obstruction."** Each of these is informative — but **absence of evidence is not always evidence of absence**, and a responsible system has to distinguish four genuinely different situations that can all look identical in a log:

- **True negative** — the sensor genuinely observed normal conditions; this is real, informative negative evidence.
- **Missing data** — the relevant sensor reading simply wasn't captured for this time window (a gap in the record, not a confirmed "normal").
- **Unreliable sensor** — a reading exists, but the sensor itself is of questionable trustworthiness at this moment (perhaps flagged elsewhere as degraded).
- **Unobserved condition** — no sensor exists that would have captured this particular signal at all, so its absence from the log carries zero information either way.

Conflating any of the last three with the first — treating "we have no data on this" the same as "we checked, and it was normal" — silently manufactures evidence that doesn't exist. This distinction connects directly forward to uncertainty handling (§7.30 and later chapters of this book).

## 7.27 Conflicting Evidence

**Example:** motor current↑, but vibration normal. Several honest interpretations exist simultaneously: a purely electrical issue (which wouldn't necessarily produce vibration); a mechanical issue not observable by *that particular* vibration sensor's placement or sensitivity; a sensor problem with the vibration reading itself; a timing mismatch (the two readings weren't actually simultaneous); a transient condition that resolved between the two measurements; or simply insufficient data to resolve the conflict at all.

**The system should not force a conclusion when evidence genuinely conflicts.** *"Insufficient evidence"* is introduced here as a first-class, legitimate diagnostic outcome — not a failure state to be engineered away, but a correct and honest answer when the data doesn't yet support anything stronger, directly consistent with the abstention design already established in this project (Understanding Report §J, Ch.4 §4.16).

## 7.28 Multiple Simultaneous Faults

**"One incident equals one root cause" is a convenient simplifying assumption, and it is sometimes wrong.** Two genuinely independent problems can occur close together in time purely by chance: a mechanical issue coinciding with an unrelated, independently-developing encoder degradation; a door problem coinciding with an unrelated communication fault. Multiple simultaneous faults complicate every stage covered so far in this book: alarm correlation (Ch.4 §4.5) has to avoid incorrectly merging two unrelated episodes into one (a false-positive risk explicitly raised in Ch.6's judge-question set, §6.19 Q18); fault trees have to be evaluated in parallel rather than assuming a single top event explains everything; Bayesian reasoning has to represent and track more than one live, unresolved investigation at once rather than forcing every symptom into one hypothesis space; and technician workflow has to accommodate genuinely investigating two things rather than being told a single, oversimplified story.

**The system must be capable of retaining multiple, separately-tracked hypothbuild spaces when the evidence genuinely doesn't support merging them** — this is a direct design requirement, not an edge case to handle later.

## 7.29 Root Cause vs. Contributing Causes vs. Symptoms

Returning to §7.1's terminology with a concrete worked chain, because collapsing these into one label is a common and consequential error:

- **Root cause:** brake drag.
- **Contributing cause:** deferred brake maintenance (increased the likelihood/severity of the drag, without itself being the drag).
- **Observed symptom:** motor current increase.
- **Secondary/consequential effect:** drive overcurrent alarm.

**Why these four should not be collapsed into one label:** the repair action differs depending on which one is being addressed. Fixing the *symptom* (clearing the overcurrent alarm) fixes nothing. Fixing the *root cause* (servicing the brake) fixes the immediate problem. Addressing the *contributing cause* (revising the maintenance interval) is what actually prevents recurrence — and is a categorically different kind of intervention than either of the other two, operating at the maintenance-policy level rather than the single-repair level.

## 7.30 RCA Confidence

**Illustrative example only:** Mechanical obstruction — 0.72; Brake drag — 0.18; Motor winding fault — 0.06; IGBT fault — 0.04. (These numbers are for illustration of the *shape* of a confidence output, not calculated from §7.15's example or any real data.)

**Why confidence must be evidence-based, not fabricated:** a confidence score is only meaningful if it actually reflects how well the available evidence discriminates between hypotheses — inventing a plausible-looking number to satisfy an output format requirement (§7.16's "double-counting" failure mode, taken to its logical extreme) is worse than reporting no number at all, because it actively misrepresents the strength of the underlying case. **Why low confidence should be allowed to remain low:** artificially inflating a weak case to look more decisive defeats the entire purpose of calibrated confidence — the honest output, when evidence is genuinely ambiguous, is a flat or multi-modal distribution across several hypotheses, not a manufactured leader. **Why multiple hypotheses may need to be retained simultaneously:** per §7.28, sometimes the evidence honestly doesn't resolve to one answer, and the system's output should say so rather than picking a winner arbitrarily. This chapter deliberately does not go deep into formal calibration methodology (reliability diagrams, Brier scores, conformal prediction) — that belongs to a dedicated uncertainty-engineering phase later in this book.

## 7.31 The RCA Reasoning Loop

The single most important conceptual artifact in this chapter, synthesizing everything above into one repeatable process:

```
OBSERVE
   ↓
CONTEXTUALIZE          (what subsystem, what fault category — Ch.4 §4.7)
   ↓
GENERATE HYPOTHESES    (§7.23, from the relevant fault tree)
   ↓
COLLECT EVIDENCE       (§7.24, multi-source — Ch.4 §4.11)
   ↓
TEST HYPOTHESES        (§7.24, expected vs. observed)
   ↓
ELIMINATE INCONSISTENT CAUSES   (§7.25, actively, not just passively)
   ↓
UPDATE PROBABILITIES   (§7.14–§7.16, Bayesian, correlation-aware)
   ↓
RANK ROOT CAUSES       (with confidence — §7.30)
   ↓
VERIFY                 (human/technician confirmation, Understanding Report §J)
   ↓
CONCLUDE  or  ABSTAIN  (§7.27, both are legitimate outcomes)
```

Every method taught in this chapter maps onto exactly one or two stages of this loop — Fault Trees and FMEA feed **Generate Hypotheses**; multi-source evidence retrieval feeds **Collect Evidence**; Bayesian reasoning powers **Test Hypotheses** through **Rank Root Causes**; the human-in-the-loop design (Understanding Report §J) governs **Verify**; and §7.27's honest-uncertainty principle governs the final branch. Nothing in this book's later AI-architecture chapters should introduce a stage that doesn't map back to this loop.

---

# Part VIII — Worked End-to-End Examples

## 7.32 Master Example: Motor Overcurrent, Start to Finish

```
ALARM:  Motor overcurrent, 10:31:01
   ↓
EVENT CHRONOLOGY:  Overcurrent → drive trip (10:31:02) →
                    leveling fault (10:31:03) → safety trip (10:31:04)
                    [the exact cascade from Ch.4 §4.5]
   ↓
SENSOR EVIDENCE:  Current↑ (A), vibration↑ (B), drive temp normal (C),
                   drive self-test normal (D), brake timing abnormal (E)
   ↓
CANDIDATE HYPOTHESES:  H1–H7, from §7.7.1's fault tree
   ↓
FAULT TREE:  Routes the investigation into Mechanical Excessive Load,
              Motor Electrical Fault, Drive Fault, Cable Fault, and
              Configuration Issue branches simultaneously
   ↓
FMEA KNOWLEDGE:  Brake drag's illustrative RPN (45, §7.8) already flags
                   it as a high-priority component independent of this
                   specific incident — a useful prior-shaping input
   ↓
CAUSAL RELATIONSHIP:  Brake drag → resistance → torque demand →
                        current, a known, physically-justified chain
                        (§7.13), not a coincidental correlation
   ↓
BAYESIAN UPDATING:  §7.15's full walkthrough — H5 eliminated by
                      contradiction; H2 promoted by specific confirmation
   ↓
ALTERNATIVE-CAUSE ELIMINATION:  §7.25's procedure, applied to all seven
                                   hypotheses, not just the leader
   ↓
ROOT-CAUSE RANKING:  H2 (Brake drag) leading; H1 and H6 retained as
                       live alternatives; H3/H4/H7 reduced; H5 minimal
   ↓
DIAGNOSTIC CONCLUSION:  "Most likely: brake drag. Moderate confidence.
                          Mechanical obstruction and excessive load
                          remain plausible alternatives, not ruled out."
   ↓
VERIFICATION REQUIREMENT:  A technician physically checks brake
                             release/timing before any repair proceeds
```

**The final conclusion is not guaranteed.** It's the best-supported hypothesis given the evidence actually available in this scenario — a different, equally plausible sequence of evidence (say, if Evidence B had been absent and a load-sensor reading had instead confirmed near-rated load) would have produced a different, equally legitimate ranking. That's the entire point of evidence-weighted reasoning over fixed lookup tables.

## 7.33 Second Example: Door Failure, Start to Finish

```
ALARM:  Door obstruction / door-close timeout, recurring across
         several cycles over two days
   ↓
HYPOTHESES (§7.7.2):  Genuine obstruction, photo-eye degradation,
                        roller wear, belt problem, door motor,
                        encoder, lock/interlock, controller/electrical
   ↓
EVIDENCE:  Photo-eye state unstable across multiple cycles; no
            consistent physical location for the "obstruction";
            door-motor current normal; cycle time only mildly
            elevated; lock-state signal stable
   ↓
SUPPORTING / CONTRADICTING:
   Genuine obstruction — contradicted (no consistent location,
       recurs without a removable cause)
   Photo-eye degradation — supported (instability pattern matches
       exactly; Ch.4 §4.9's canonical ambiguity, resolved here by
       the multi-event pattern rather than any single event)
   Roller/belt/motor — contradicted (current and cycle-time evidence
       don't show the expected signatures)
   Lock/interlock — contradicted (signal stable)
   ↓
RANKED CONCLUSION:  Photo-eye degradation, high confidence — this is
                      the one case in this book's worked examples
                      where the evidence resolves unusually cleanly,
                      specifically because the multi-event pattern
                      (not any single event) is what's diagnostic
   ↓
VERIFICATION:  Physical photo-eye alignment/cleaning check
```

## 7.34 Third Example: Leveling / Position Deviation, Start to Finish

```
ALARM:  Leveling deviation, gradual trend over several weeks
        (not a sudden event)
   ↓
HYPOTHESES (§7.7.3):  Encoder drift, independent leveling-sensor
                        fault, rope stretch/slip, sheave wear,
                        brake timing deviation, controller
                        calibration error
   ↓
EVIDENCE:  Independent leveling sensor AND main encoder both show
            the SAME gradual deviation, growing over time; no
            correlation with brake-release events; vibration trend
            mild but present; maintenance history shows no recent
            rope inspection
   ↓
SUPPORTING / CONTRADICTING:
   Encoder-only fault — contradicted (an independent sensor shows
       the SAME deviation; a pure encoder fault should not agree
       with an independent reference — this is the exact
       distinguishing check from Ch.3 §3.7 and §7.7.3)
   Brake timing — contradicted (no correlation with brake events)
   Rope stretch — supported (gradual trend, mild vibration increase,
       consistent with slow mechanical wear; maintenance-history
       gap raises rather than lowers this hypothesis's prior,
       per Ch.5 §5.16's reasoning)
   ↓
RANKED CONCLUSION:  Rope stretch/wear, moderate-to-high confidence,
                      informed as much by WHICH sensors agree with
                      each other as by any single reading
   ↓
VERIFICATION:  Physical rope inspection, informed by maintenance
                interval history
```

**Why subsystem boundaries matter, demonstrated by this example specifically:** the same observed alarm (leveling deviation) could plausibly originate in the position-feedback subsystem, the motion/traction subsystem, or the brake subsystem — three entirely different repair actions. The evidence that actually resolves it here isn't any single sensor reading; it's the **agreement between two independent sensors**, which rules out the feedback-only explanation by construction.

---

# Part IX — Boundaries and Honesty

## 7.35 Human Technician vs. Formal RCA

| | Human Technician | Formal RCA System |
|---|---|---|
| Reasoning basis | Experience + mental model + observation + historical knowledge + physical inspection | Structured knowledge (FMEA, fault trees) + telemetry + event chronology + probabilistic reasoning + explicit evidence |
| Strength | Intuition for unusual/novel cases; physical inspection | Consistency, speed, systematic coverage of the full hypothesis space |
| Weakness | Inconsistent under time pressure or fatigue; limited working memory for many simultaneous evidence sources | No physical senses; only as good as its knowledge base and available telemetry |

**The goal is not to pretend AI replaces engineering expertise.** It's to formalize and augment diagnostic reasoning — giving a technician a systematically-generated, evidence-weighed starting hypothesis and its full supporting/contradicting rationale, rather than either (a) an unexplained black-box guess or (b) nothing at all beyond the raw fault code. The human technician's physical-inspection and novel-case judgment remain irreplaceable — and remain, per this project's safety boundary, the final verification step in every worked example above.

## 7.36 What an RCA System Should Not Do

It should **not**: equate an alarm with the root cause (§7.1); choose the first plausible cause without testing alternatives (§7.25); ignore alternative hypotheses (§7.25); double-count correlated evidence (§7.16); treat correlation as causation (§7.13); fabricate missing sensor values (§7.26); fabricate maintenance history; invent proprietary fault mappings (Ch.4 §4.23); force a conclusion when evidence is insufficient (§7.27); override safety mechanisms (§7.7.6, Understanding Report §J); or confuse prediction with diagnosis (§7.2).

## 7.37 Toward an RCA Knowledge Base

The structured representation this chapter's material naturally converges on, for a single piece of engineering knowledge:

```
Component → Function → Failure Mode → Cause → Effect
   → Sensor Signature → Alarm → Alternative Causes
   → Diagnostic Evidence → Verification Method
```

**FMEA + Fault Trees + Causal Graphs**, taken together, are exactly what would populate this structure — FMEA supplies the component/function/failure-mode/effect backbone; fault trees supply the cause hierarchy and OR/AND relationships for any given top event; causal graphs supply the explicit mechanism justifying each link. This chapter does not design the final software architecture that would store or query this structure — that belongs to the data-architecture material later in this book.

## 7.38 The RCA Data Model

The conceptual data an investigation needs to carry, as a structured object rather than an unstructured block of text handed to a model: **asset**, **time window**, **symptoms**, **events**, **alarms**, **sensor evidence**, **operating context**, **candidate hypotheses**, **supporting evidence**, **contradicting evidence**, **historical evidence**, **root-cause ranking**, **confidence**, **verification status**.

**Why structured investigation state is preferable to an unstructured text block:** every field above corresponds to a specific stage of §7.31's reasoning loop; a structured object lets each stage read and write exactly the fields relevant to it, keeps supporting and contradicting evidence traceably separate (rather than blended into prose an LLM might paraphrase imprecisely), and is what actually makes an audit trail auditable — a reviewer can inspect the *fields*, not just parse free text and hope nothing was lost in translation. No specific implementation technology is specified here — that's a later chapter's concern.

## 7.39 Limitations of Formal RCA

Intellectual honesty, stated directly: formal RCA, as taught in this chapter, still depends on **incomplete knowledge** (the fault trees and FMEA here are engineering-reasoned, not exhaustively validated); can be blind to **unknown failure modes** not yet represented in any tree; is degraded by **sensor faults** that corrupt the evidence it depends on; suffers from **missing data**; is vulnerable to **correlated evidence** if not carefully modeled (§7.16); struggles with **multiple simultaneous faults** (§7.28); assumes **stable operating conditions** that real installations may not always provide; depends on data this project does not currently have (**insufficient labels**, Ch.4 §4.23's **proprietary information** gap); rests on **model assumptions** (conditional independence, Markov simplification, §7.16 and §7.18) that don't always hold; produces **imperfect probabilities**, illustrative at best without real calibration data; and can face genuine **causal ambiguity** that no amount of careful reasoning fully resolves with the evidence actually available.

**An RCA system must be designed to acknowledge all of this — not engineered to hide it behind a confident-sounding output.**

## 7.40 Research Gaps

| Known Gap | Assumption Being Made Instead | Genuinely Unknown |
|---|---|---|
| No public OEM fault-code mappings | This book's fault trees are engineering-reasoned, not KONE's actual taxonomy (Ch.4 §4.23) | Whether KONE's internal taxonomy resembles this book's structure at all |
| No labeled elevator fault dataset | Synthetic, physics-grounded scenarios substitute for validation (Understanding Report §K) | True real-world base rates for any of §7.15's illustrative priors |
| Limited public causal models for elevators | This chapter's causal graphs are derived from Chapters 1–3's general engineering, not elevator-specific published research | Whether elevator-specific causal structure differs meaningfully from the general mechanical/electrical reasoning used here |
| Real-world probability calibration | Not attempted in this chapter — explicitly deferred | Whether any of §7.15's illustrative posteriors would survive contact with real field data |
| Distinguishing sensor faults from equipment faults | Addressed conceptually (§7.26) | No specific method proposed or validated yet |
| Multiple simultaneous faults | Addressed as a design requirement (§7.28) | No specific detection/separation mechanism proposed yet |
| Transferring generic reliability knowledge to specific elevator architectures | This book targets a modern gearless traction elevator throughout (Ch.1's stated scope decision) | How much of this chapter's reasoning would need to change for a hydraulic or MRL-variant installation |

---

# Judge Questions

**1. What exactly is root cause?** *Short:* The earliest point in the causal chain where intervention would have prevented the failure (§7.1). *Detailed:* Distinguished from immediate cause, contributing cause, and symptom in the same section's table. *Evidence:* Standard reliability-engineering terminology. *Assumptions:* None specific to KONE. *Tested:* Whether the team can define their own core term precisely on demand. *Avoid:* Conflating root cause with "whatever the fault code says."

**2. How is RCA different from fault detection?** *Short:* Detection asks "is something abnormal"; RCA asks "why" (§7.2). *Detailed:* Different input, different output — §7.2's table. *Evidence:* Conceptual, reinforced across Ch.4–6. *Assumptions:* None. *Tested:* Basic conceptual grounding, likely re-asked in several forms. *Avoid:* Treating them as synonyms.

**3. How is RCA different from fault isolation?** *Short:* Isolation narrows to a subsystem; RCA explains the specific mechanism within it (§7.2). *Detailed:* Isolation is a necessary but not sufficient precursor to RCA. *Evidence:* §7.2's table. *Assumptions:* None. *Tested:* Whether the team keeps a three-way (not just two-way) distinction straight. *Avoid:* Using "isolation" and "RCA" interchangeably.

**4. Why is a fault code not a root cause?** *Short:* A fault code names a detected symptom, not its cause (Ch.4 §4.1). *Detailed:* §7.7.1's nine-branch fault tree for a single fault code is the concrete proof. *Evidence:* This book's own repeated worked example. *Assumptions:* None. *Tested:* Whether the team's central thesis is genuinely internalized. *Avoid:* A vague restatement without the concrete tree.

**5. Why isn't 5 Whys sufficient?** *Short:* It's linear and can't represent branching hypotheses or uncertainty (§7.4). *Detailed:* Five explicit limitations listed in §7.4. *Evidence:* Standard critique of the method in reliability literature. *Assumptions:* None. *Tested:* Whether the team can critique a familiar method specifically, not just dismiss it. *Avoid:* "It's too simple" without naming which specific limitation matters here.

**6. Why not simply use an FMEA?** *Short:* FMEA is a static knowledge base, not a live investigation tool (§7.9). *Detailed:* FMEA answers "what can fail"; it doesn't weigh live evidence for one specific incident. *Evidence:* §7.9's comparison table. *Assumptions:* None. *Tested:* Whether FMEA's actual role (feeding hypothesis generation) vs. limitation is understood precisely. *Avoid:* Dismissing FMEA entirely — it's foundational, just not sufficient alone.

**7. Why do you need a fault tree?** *Short:* It structures the hypothesis space a specific investigation reasons over (§7.6–§7.7). *Detailed:* Six concrete elevator trees built in this chapter, each reused in the worked examples (§7.32–§7.34). *Evidence:* Direct demonstration. *Assumptions:* Trees are engineering-reasoned, not KONE's actual taxonomy. *Tested:* Whether a tree can be sketched from memory for at least one fault type. *Avoid:* Presenting the trees as confirmed KONE data.

**8. What does Bayesian reasoning add?** *Short:* A principled way to update belief across competing hypotheses as evidence arrives (§7.14). *Detailed:* P(H|E) ∝ P(E|H)×P(H), demonstrated in §7.15. *Evidence:* Standard probability theory. *Assumptions:* Conditional independence, flagged as often false (§7.16). *Tested:* Whether the math can be explained in plain language, not just cited. *Avoid:* Citing "Bayesian" as a buzzword without being able to walk through §7.15's example.

**9. Why not use deterministic rules?** *Short:* Rules assume certainty; real evidence is graded and sometimes conflicting (§7.14's KEY CONCEPT). *Detailed:* `IF alarm=X THEN cause=Y` cannot represent the nine-cause ambiguity §7.7.1's tree demonstrates. *Evidence:* This book's own repeated worked examples. *Assumptions:* None. *Tested:* Whether the team can defend probabilistic reasoning against a "just write more rules" pushback. *Avoid:* Implying rules have no place at all — deterministic retrieval still matters (§7.22).

**10. What happens when evidence conflicts?** *Short:* The system doesn't force a conclusion; "insufficient evidence" is a valid outcome (§7.27). *Detailed:* Worked with the current↑/vibration-normal example. *Evidence:* Direct extension of the project's own abstention design. *Assumptions:* None. *Tested:* Whether abstention is defended as a strength. *Avoid:* Implying the system always resolves conflicts somehow.

**11. What happens when evidence is missing?** *Short:* Missing data is distinguished from a true negative (§7.26). *Detailed:* Four distinct categories — true negative, missing data, unreliable sensor, unobserved condition. *Evidence:* Direct engineering reasoning. *Assumptions:* None. *Tested:* Whether "no data" and "confirmed normal" are kept separate. *Avoid:* Treating silence as evidence.

**12. How do you handle sensor failure?** *Short:* By cross-checking against independent/complementary signals wherever possible (Ch.4 §4.18 item 9, §7.34's worked example). *Detailed:* §7.34 shows exactly this check (encoder vs. independent leveling sensor). *Evidence:* Direct worked demonstration. *Assumptions:* An independent check exists for the signal in question — not always true. *Tested:* Whether the team has a concrete example ready, not just a principle. *Avoid:* Assuming every signal has a convenient independent check available.

**13. How do you prevent double-counting correlated evidence?** *Short:* By modeling which evidence pieces are genuinely independent before combining likelihoods (§7.16). *Detailed:* Current↑ and torque↑ example — same underlying fact, not two confirmations. *Evidence:* Direct physics (Ch.1 §1.5). *Assumptions:* Requires an explicit causal-graph model to identify redundancy. *Tested:* Whether the team understands this as a real, hard problem, not a footnote. *Avoid:* Claiming this is already fully solved — it's flagged as genuinely hard (§7.39).

**14. How do you distinguish correlation from causation?** *Short:* Via a known physical mechanism (a causal graph), not time proximity alone (§7.13). *Detailed:* Three explanations for temporal proximity — genuine causation, shared unobserved cause, coincidence. *Evidence:* Standard causal-inference reasoning. *Assumptions:* None. *Tested:* Whether the three-way distinction is named, not just "correlation isn't causation" as a slogan. *Avoid:* The slogan without the mechanism.

**15. Can one fault produce multiple alarms?** *Short:* Yes — the entire premise of Ch.4's cascade material, reused in §7.32's worked example. *Detailed:* Motor overcurrent → drive trip → leveling fault → safety trip. *Evidence:* This book's own repeated example. *Assumptions:* None. *Tested:* Whether the cascade can be walked fluently, again. *Avoid:* A generic answer without the specific chain.

**16. Can multiple faults occur simultaneously?** *Short:* Yes, and the system must be able to retain more than one live hypothesis space when evidence doesn't support merging (§7.28). *Detailed:* Two independent examples given — mechanical + encoder, door + communication. *Evidence:* Direct engineering reasoning. *Assumptions:* None. *Tested:* Whether this is treated as a real design requirement, not an edge case. *Avoid:* Assuming every episode has exactly one cause.

**17. How do you identify the initiating fault?** *Short:* Chronology plus physical plausibility, not chronology alone (Ch.4 §4.12, §7.13). *Detailed:* A causal graph justifies which temporally-first event is credibly upstream. *Evidence:* Repeated across Ch.4 and this chapter. *Assumptions:* None. *Tested:* Consistency with earlier chapters' answer to the same question. *Avoid:* "Whichever came first," unqualified.

**18. How do you use negative evidence?** *Short:* Carefully, distinguishing true negatives from missing/unreliable data (§7.26). *Detailed:* Direct restatement of §7.26's four-category framework. *Evidence:* Direct engineering reasoning. *Assumptions:* None. *Tested:* Whether this nuance is retained under a direct question. *Avoid:* Treating all absence as equally informative.

**19. How do you eliminate alternative causes?** *Short:* By testing each hypothesis against expected evidence, not just the leading one (§7.25). *Detailed:* The four-step procedure, applied to all seven hypotheses in §7.15. *Evidence:* Direct worked demonstration. *Assumptions:* None. *Tested:* Whether elimination is systematic in the team's account, not anecdotal. *Avoid:* "We rule things out" without the procedure.

**20. What happens if two causes have similar probability?** *Short:* Both are retained and reported, not artificially separated (§7.28, §7.30). *Detailed:* A flat or multi-modal confidence output is the honest result, not a forced single winner. *Evidence:* Direct extension of the abstention principle. *Assumptions:* None. *Tested:* Whether the team is comfortable with a genuinely tied output. *Avoid:* Implying the system always picks a clear winner.

**21. Can the system say "I don't know"?** *Short:* Yes — explicitly, as a designed, legitimate outcome (§7.27, §7.30). *Detailed:* This is a repeated design principle across the whole book, not invented for this chapter. *Evidence:* Understanding Report §J; Ch.4 §4.16. *Assumptions:* None. *Tested:* Whether this is defended confidently. *Avoid:* Apologizing for abstention.

**22. How do you obtain Bayesian priors?** *Short:* In production, from real historical failure-rate data KONE has not published; here, illustratively (§7.15). *Detailed:* This is an explicit, named research gap (§7.40). *Evidence:* Honest limitation, not a solved problem. *Assumptions:* Real priors would come from field data this project doesn't currently have. *Tested:* Whether the team admits this gap unprompted. *Avoid:* Implying §7.15's numbers are real or derivable without real data.

**23. Where do your probabilities come from?** *Short:* Illustrative engineering judgment for teaching purposes in this book; production probabilities would require real field data (§7.15, §7.40). *Detailed:* Same answer as Q22, restated. *Evidence:* — *Assumptions:* — *Tested:* Consistency between Q22 and Q23's answers — a likely follow-up pairing. *Avoid:* Giving a different answer than Q22.

**24. Are your probabilities real or illustrative?** *Short:* Illustrative, explicitly and repeatedly labeled as such throughout this chapter. *Detailed:* Every numerical example in §7.8, §7.15, and §7.30 carries this label. *Evidence:* — *Assumptions:* — *Tested:* Whether the team volunteers this without being pressed. *Avoid:* Any hesitation before answering "illustrative."

**25. How do you validate a root-cause conclusion?** *Short:* Human/technician verification before any repair action (§7.31's final stages; Understanding Report §J). *Detailed:* Physical inspection, per every worked example in §7.32–§7.34. *Evidence:* Direct architectural design principle. *Assumptions:* A technician remains available and empowered to perform this check. *Tested:* Whether "verification" is named as a required stage, not an optional nicety. *Avoid:* Implying the system's conclusion is self-validating.

**26. How do FMEA and FTA complement each other?** *Short:* FMEA builds the static knowledge base; FTA structures a live investigation (§7.9). *Detailed:* Bottom-up vs. top-down, general vs. specific. *Evidence:* §7.9's table. *Assumptions:* None. *Tested:* Whether both methods' distinct roles are named, not just "we use both." *Avoid:* Presenting them as redundant with each other.

**27. Why use causal graphs?** *Short:* They justify why a temporal correlation should count as causal evidence (§7.13). *Detailed:* The explicit mechanism (physics from Ch.1) is what separates correlation from causation. *Evidence:* §7.13. *Assumptions:* None. *Tested:* Whether the team can name the specific role, not just "graphs are useful." *Avoid:* A generic answer without the correlation/causation distinction.

**28. Why would a dynamic Bayesian model be useful?** *Short:* Because the *trajectory* of change over time is itself diagnostic, not just the current snapshot (§7.17). *Detailed:* Gradual vs. sudden current rise example. *Evidence:* §7.17. *Assumptions:* Math kept conceptual, not fully derived in this book. *Tested:* Whether the gradual-vs-sudden distinction is understood as the concrete payoff. *Avoid:* A definition without the concrete example.

**29. Why not just use an LLM?** *Short:* Because an LLM alone has no built-in mechanism for calibrated, evidence-weighed, correlation-aware probabilistic reasoning (§7.14–§7.16). *Detailed:* This chapter's entire mathematical apparatus is exactly what a bare LLM call doesn't provide by default. *Evidence:* Direct architectural principle (Understanding Report §E). *Assumptions:* None. *Tested:* Whether the team can defend their hybrid architecture technically, not just assert it's better. *Avoid:* Vague "LLMs hallucinate" without the specific missing mechanism.

**30. What should the LLM actually reason over?** *Short:* Structured evidence and hypothesis state (§7.38's data model) — not raw fault codes alone. *Detailed:* The LLM's role is generating human-readable explanation and handling ambiguous free text, not performing the probability arithmetic itself. *Evidence:* Consistent with Ch.4 §4.15's "LLM should/shouldn't do" framing. *Assumptions:* None. *Tested:* Whether a clean division of labor is articulated. *Avoid:* "The LLM does everything."

**31. How do you prevent hallucinated root causes?** *Short:* By grounding every conclusion in the structured evidence model (§7.38), never letting the model assert a cause without a corresponding evidence trail. *Detailed:* Directly parallels KONE's own stated verification priority for their Technician Assistant (Ch.5 §5.10). *Evidence:* Architectural design principle plus a genuine industry parallel. *Assumptions:* Implementation actually enforces this — a design intent, not yet a tested result. *Tested:* Whether the team connects this to KONE's own stated concern, showing genuine cross-chapter synthesis. *Avoid:* "We'll test it carefully" without a structural mechanism.

**32. How do you handle proprietary OEM fault mappings?** *Short:* By building engineering-reasoned trees explicitly labeled as such, never invented as if confirmed (Ch.4 §4.23, this chapter throughout). *Detailed:* Every fault tree and FMEA row in this chapter carries this caveat. *Evidence:* Explicit, repeated labeling. *Assumptions:* — *Tested:* Whether this limitation is owned confidently. *Avoid:* Implying the trees are more authoritative than they are.

**33. How do you diagnose without real KONE fault data?** *Short:* Physics-grounded synthetic scenarios (Understanding Report §K), reasoned from Chapters 1–3's general engineering, validated against internal consistency rather than field accuracy. *Detailed:* This is explicitly what the whole book's methodology has been building toward — Chapters 1–7 constitute the reasoning, not the data. *Evidence:* Consistent project design (Understanding Report §K). *Assumptions:* Synthetic validation demonstrates reasoning-process correctness, not production accuracy — a distinction worth stating unprompted. *Tested:* Whether the team volunteers this caveat. *Avoid:* Presenting synthetic-scenario success as field validation.

**34. How does a technician verify the AI's conclusion?** *Short:* Via the same physical-inspection step every worked example in this chapter ends with (§7.32–§7.34). *Detailed:* The ExplainabilityTrace (referenced throughout this book) gives the technician the evidence to check, not just a bare conclusion to accept or reject blindly. *Evidence:* Direct architectural principle. *Assumptions:* — *Tested:* Whether verification is described as evidence-informed, not a rubber stamp. *Avoid:* Implying verification is a formality.

**35. What happens when the AI has insufficient evidence?** *Short:* It abstains and defers to the technician, explicitly (§7.27, §7.30, Understanding Report §J). *Detailed:* This is the single most repeated design principle in the entire research book — worth being able to state without hesitation, from any chapter, at any point. *Evidence:* Consistent across every phase of this book. *Assumptions:* — *Tested:* The single most important closing question — essentially "is this principle actually load-bearing, or just something you said once." *Avoid:* Any answer that isn't immediate and confident.

---

# Master RCA Framework

```
ENGINEERING KNOWLEDGE  (Chapters 1–3)
        +
FAILURE MODES           (§7.8's FMEA)
        +
FAULT TREES              (§7.7)
        +
CAUSAL RELATIONSHIPS       (§7.13)
        +
REAL-TIME EVIDENCE          (Ch.4 §4.11)
        +
HISTORICAL EVIDENCE          (Ch.5 §5.16)
        +
EVENT CHRONOLOGY               (Ch.4 §4.12)
        +
PROBABILISTIC REASONING         (§7.14–§7.17)
        +
ALTERNATIVE-CAUSE ELIMINATION    (§7.25)
        =
EVIDENCE-BASED ROOT-CAUSE INVESTIGATION
```

```
Observation → Hypotheses → Evidence → Causal interpretation
   → Probability update → Root-cause ranking → Verification
   → Conclusion / Abstention
```

# What We Now Understand

Root cause analysis is the discipline of distinguishing what happened from why it happened (§7.1) — and every classical method surveyed in this chapter (5 Whys, Fishbone, FTA, FMEA, FMECA, ETA, Bow-Tie) answers a genuinely different question, none of them sufficient alone for autonomous, evidence-weighed elevator diagnosis. Fault trees give the hypothesis structure; FMEA gives the static knowledge base; causal graphs justify treating a relationship as more than coincidence; Bayesian reasoning — done carefully, accounting for correlated evidence — is what actually updates belief as evidence arrives; Dynamic Bayesian Networks and Markov models extend that reasoning across time. Alternative-cause elimination, negative-evidence discipline, honest handling of conflicting evidence, and the willingness to retain multiple live hypotheses or abstain entirely are what separate genuine evidence-based reasoning from confident guessing. Verification by a qualified human remains the final, non-negotiable step in every example this chapter worked through.

# The Central Principle

> **ROOT-CAUSE ANALYSIS IS NOT THE PROCESS OF FINDING THE FIRST PLAUSIBLE EXPLANATION; IT IS THE PROCESS OF SYSTEMATICALLY EVALUATING COMPETING CAUSAL HYPOTHESES AGAINST AVAILABLE EVIDENCE.**

Every method, table, fault tree, and worked example in this chapter exists to make that one sentence operational rather than aspirational — turning it from a value the project claims to hold into a specific, repeatable reasoning loop (§7.31) that can be inspected, audited, and defended, one hypothesis and one piece of evidence at a time.

---

# Bridge to Phase 6 — Alarm Correlation, Time-Series Analysis & Anomaly Detection

```
RCA hypotheses
     ↓
Required evidence
     ↓
Telemetry
     ↓
Event streams
     ↓
Signal processing
     ↓
Alarm correlation
     ↓
Anomaly detection
     ↓
Usable diagnostic evidence
```

This chapter's entire reasoning framework has one large, unaddressed dependency: it assumes clean, reliable, already-identified pieces of evidence ("current↑," "vibration↑," "drive self-test normal") arrive ready to reason over. They don't, in reality — they have to be extracted from continuous, noisy, high-frequency elevator signals first. Phase 6 must therefore study how reliable evidence is actually produced from raw telemetry: alarm correlation and alarm-flood management, temporal and causal correlation, primary-vs-consequential alarm identification at the signal-processing level, sampling and filtering, RMS, FFT and spectral analysis, wavelets, cross-correlation and lag analysis, motor current signature analysis, vibration analysis, door-cycle analysis, encoder/position analysis, and both statistical and machine-learning approaches to anomaly detection.

Phase 6 content is not generated here — this document ends at the close of Phase 5.
