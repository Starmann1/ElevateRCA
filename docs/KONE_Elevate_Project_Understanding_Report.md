# KONE Elevate — Project Understanding Report

**Phase:** 1 only — internal understanding of the source material. No chapter content, no booklet, no Chapter 1 is included below. Per your instructions, I'm stopping here and waiting for your next instruction.

**Sources analyzed:** *KONE Idea Proposal — Autonomous Fault Isolation & Root Cause Analysis Assistant* (team RiskForge/NexGen, Rajalakshmi Engineering College) and *KONE Elevate — Master Research Roadmap* (48 numbered research topics, priority-tagged, plus a dependency chain and a "12 non-negotiable topics" list). Both text and diagrams were read — several conclusions below (e.g., the "no control link" icon on the safety circuit, the color-coded architecture legend) come specifically from the diagrams, not just the prose.

**A note on scope and terminology:** Per your instruction, I have not named, labeled, quoted, or compared against the predecessor architecture the roadmap's reuse-mapping topic references — everywhere that's relevant below, I describe it only in generic engineering terms (what's newly built vs. adapted vs. retained), never by name. One practical thought, offered once: since the roadmap frames your current multi-agent design as an adaptation of that earlier system, it may be worth a quick internal check that this lineage is fine under KONE Elevate's rules on prior/existing work, so it isn't a surprise question from a judge later. Entirely your call — I won't raise it again unless you want to.

**Tag legend** (applied at the level of major conclusions, not every clause):

| Tag | Meaning |
|---|---|
| `[SOURCE-DERIVED]` | Drawn directly from the two documents |
| `[EXPLICITLY STATED IN ROADMAP]` | The roadmap says this outright, often as direct guidance to the team |
| `[SUPPORTED BY PROVIDED TECHNICAL MATERIAL]` | Backed by specific diagrams, tables, or schemas in the material |
| `[RESEARCH GAP]` | The source material itself flags this as unresearched, or it's evidently missing |
| `[ASSUMPTION]` | An assumption the project material makes, stated or implicit |
| `[REQUIRES EXTERNAL VERIFICATION]` | A third-party claim (KONE/Otis/Schindler/TK) the roadmap cites but I have not independently re-checked in this pass |

Where the documents don't contain enough to support a claim, I've written **NOT ESTABLISHED IN THE PROVIDED PROJECT MATERIALS** instead of filling the gap.

---

## A. Project Objective

- **[SOURCE-DERIVED]** Team RiskForge (now renamed NexGen), led by Arul Amudhan G at Rajalakshmi Engineering College, is proposing an **Autonomous Fault Isolation & Root Cause Analysis (RCA) Assistant** for KONE Elevate 2026.
- **[SOURCE-DERIVED]** The objective is an advisory, evidence-based diagnostic layer that sits alongside existing elevator telemetry/alarm/maintenance systems: it correlates related alarms into a single "fault episode," isolates the affected subsystem, ranks competing root-cause hypotheses with confidence and supporting evidence, recommends corrective actions, and renders two outputs (detailed for technicians, simplified for building managers) — all while staying structurally outside the elevator's safety-control loop.
- **[EXPLICITLY STATED IN ROADMAP]** The roadmap frames one specific question as the project's central research question, governing "your final architecture, demo, differentiation slide, technical claims, and judge Q&A": *"What can our evidence-driven, auditable RCA layer do that existing elevator monitoring, predictive-maintenance and technician-assistance systems do not publicly demonstrate?"*
- **[SOURCE-DERIVED]** Current status: architecture/design stage only. Prototype development and evaluation against "controlled, physics-grounded synthetic scenarios" are explicitly stated as the *next* steps, not yet done.
- **[SOURCE-DERIVED]** KONE Elevate appears to be a staged competition: the current document is an "Idea Proposal," and the roadmap separately refers to a "final round" in 2026 (for which, notably, AWS + generative AI research is called "mandatory") and a "Hackathon Demonstration" milestone. This staging matters for section M below.

## B. Problem Statement

- **[SOURCE-DERIVED]** Elevator faults frequently trigger cascades of interrelated alarms rather than a single clean signal. The proposal's worked example: debris blocks a door → "door obstruction" → "door-close timeout" → safety-circuit trip → "drive start failure" (motor safety-locked) — four apparently separate faults from one underlying cause.
- **[SOURCE-DERIVED]** The proposal explicitly labels this example *"an illustrative engineering scenario; not based on a specific KONE service case"* — the specific fault chain is pedagogical, not verified KONE data (see section N).
- **[SOURCE-DERIVED]** Today, isolating the true cause requires **manual** correlation of telemetry, fault logs, and maintenance history — slow when multiple subsystems are involved, and prone to delayed/incorrect diagnosis, longer downtime, repeat visits, and unnecessary part replacement.
- **[SOURCE-DERIVED]** The problem is framed as a specific reasoning gap, not a monitoring gap: *"move from fault detection to reliable, evidence-based fault isolation and root-cause identification."*

## C. Current Proposed Solution

- **[SOURCE-DERIVED]** The Assistant will: correlate alarms/events in a shared time window; pull evidence from sensors/telemetry, fault logs, maintenance history, and manuals/fault-code docs; generate and compare multiple root-cause hypotheses via an elevator-specific fault tree **and** Bayesian reasoning (rather than single fault codes); rank causes with confidence and show why alternatives were ruled out; recommend corrective actions; and produce dual-audience output (technician-detailed / manager-simplified) from one auditable reasoning trail.
- **[SOURCE-DERIVED]** Six stated differentiators, each framed as a shift: alarm detection → causal fault isolation; single signal → multi-evidence diagnosis; fixed rules → competing hypotheses; diagnosis → evidence & confidence; RCA → actionable technician support; AI assistance → explainable & safety-bounded.
- **[EXPLICITLY STATED IN ROADMAP]** At least one implicit differentiation angle in the proposal — novelty via a multi-agent architecture — is explicitly **not safe** per the roadmap, which notes TK Elevator's 2026 agentic-AI direction already uses multiple specialized agents. The proposal's differentiation claims need to be checked against section L before being used publicly. **[RESEARCH GAP]**

## D. End-to-End System Workflow

- **[SUPPORTED BY PROVIDED TECHNICAL MATERIAL]** Core diagnostic flow (proposal): Fault/Anomaly Detected → Related Alarms Correlated → Fault Episode Formed → Relevant Evidence Retrieved → Fault Subsystem Isolated → Root Cause Determined (+ confidence & evidence) → Recommended Action + Report → Human Review.
- **[SUPPORTED BY PROVIDED TECHNICAL MATERIAL]** A more granular 8-step sequence diagram splits this into two phases: **Real-time Detection & Isolation** (telemetry/technician-report streaming → anomaly correlation → fault-episode formation → structured context handoff → evidence retrieval — "typically seconds") and **Reasoning & Synthesis** (subsystem isolation + root cause → recommended action + report → human review — "typically seconds to minutes"). The proposal explicitly notes these timings are illustrative and may vary by deployment. **[ASSUMPTION]**
- **[EXPLICITLY STATED IN ROADMAP]** A broader KONE incident lifecycle is described separately (§11): fault occurs → elevator detects fault → alarm generated → remote monitoring → alert → diagnosis → service ticket → technician dispatch → parts/tools prep → site inspection → repair → testing → return to service → maintenance record. The proposal's workflow clearly maps to the "diagnosis" step of this larger lifecycle, but *where exactly it plugs in* — who receives the alert, who decides severity/dispatch, how a completed repair feeds back into the system — is **not established in the provided project materials**; the roadmap poses these as open questions, not yet answered by the proposal. **[RESEARCH GAP]**

## E. Core Technical Architecture

- **[SUPPORTED BY PROVIDED TECHNICAL MATERIAL]** Pipeline stages: multiple data sources → data ingestion/normalization → alarm correlation & triage → orchestration → evidence retrieval → fault isolation & root-cause analysis → corrective-action synthesis → separate Technician / Building Manager views. An Explainability Engine runs across the whole pipeline, capturing evidence, confidence scores, and reasoning trace.
- **[SOURCE-DERIVED]** Explicit design principle: *"combines deterministic event processing and retrieval with AI-assisted reasoning, rather than relying on a single general-purpose LLM for diagnosis."* The architecture diagram labels the Retrieval Agent specifically as "deterministic, rule-based (not LLM)."
- **[SUPPORTED BY PROVIDED TECHNICAL MATERIAL]** The architecture diagram shows a **hard, explicit block** (dashed line + circle-slash icon) between the AI pipeline and the elevator safety circuit, which is separately labeled "hardware fail-safe, always autonomous." This is a drawn, not just stated, boundary.
- **[EXPLICITLY STATED IN ROADMAP]** The roadmap frames the current agent architecture as an adaptation of an earlier, more general system (see the terminology note above — I'm not naming it). What matters for internal understanding is the *reuse classification* it gives: one agent role is entirely new to this domain, several are described as modified or heavily modified for elevators specifically, and a couple of components (the explainability-trace object, the human-reviewer role) are described as carried over largely as-is. That classification is useful for scoping how much of the engineering work is genuinely new vs. adapted, without needing to name what it was adapted from.

## F. Elevator Engineering Foundation

- **[EXPLICITLY STATED IN ROADMAP]** Roadmap topics 1–4 (all P0) are positioned as prerequisite to everything else: elevator types (traction — geared/gearless, MRL, hydraulic, vacuum/pneumatic — vs. passenger/freight/high-rise/hospital/service use cases); full mechanical architecture (motor → drive/VFD → traction sheave → ropes/belts → car + counterweight, plus guide rails/shoes, brake, machine, cabin, buffers, governor, safety gear, overspeed protection, landing system); electrical/control architecture (controller: PLC, main control board, I/O, safety controller, drive interface, comms, event/fault logging, state machines; VFD/VVVF: AC→DC→AC, DC bus, inverter, PWM, IGBT, gate drivers, sensors, regenerative braking; PMSM: rotor/stator, field-oriented control, encoder feedback, current signatures); door system (operator, motor, belt, rollers, lock, interlock, photo-eye, light curtain, safety edge, encoder, cycle time); brake/rope/traction system and its safety layer (governor, safety gear, UCMP/UCM, ACOP, buffers).
- **[EXPLICITLY STATED IN ROADMAP]** A sensor dictionary (§5) spans electrical, mechanical, position, door, environmental, and operational signals.
- **[REQUIRES EXTERNAL VERIFICATION]** The roadmap cites KONE's own public claim that its connected services analyze **200+ parameters**, including door behavior, shaft position/movement, usage, stopping accuracy, mileage, and drive time.
- **[EXPLICITLY STATED IN ROADMAP]** A key distinction the RCA engine must encode: an apparent *"motor problem"* vs. *"motor appears abnormal because the brake/traction system is creating excessive load"* — i.e., where a symptom shows up is not necessarily where the cause is.
- **[RESEARCH GAP]** Which specific elevator architecture(s) the RCA system targets (geared vs. gearless traction, MRL, hydraulic, etc.) is posed by the roadmap as an open question (§1.1: *"Which architecture your RCA system targets"*) — **not established in the provided project materials**.

## G. Diagnostic / RCA Logic

- **[SOURCE-DERIVED]** Alarm correlation groups temporally-close alarms into one fault episode instead of treating each independently (worked example: Door Obstruction → Door-Close Timeout → Safety Trip → Drive-Start Failure).
- **[SOURCE-DERIVED]** The RCA Agent's job: retrieve relevant records/logs/docs → identify the affected subsystem → generate root-cause hypotheses → compare them via fault-tree + Bayesian reasoning → rank by confidence and evidence → explain why alternatives are less likely. Stated objective: move from *"multiple alarms occurred"* to *"these events are connected, this subsystem is affected, and this is the most likely underlying cause."*
- **[EXPLICITLY STATED IN ROADMAP]** *"Fault code ≠ root cause"* is called out as **the exact reasoning problem the project addresses** — illustrated with "Motor Overcurrent" resolving to five distinct possible causes (mechanical jam, motor winding fault, cable fault, IGBT failure, wrong VFD parameters).
- **[EXPLICITLY STATED IN ROADMAP]** Reasoning should be in terms of P(Cause | Evidence) — explicitly *not* brittle `IF alarm = X THEN cause = Y` rules — because Bayesian-style combination handles partial, noisy, and correlated evidence.
- **[EXPLICITLY STATED IN ROADMAP]** Six canonical fault trees are directed to be built (§19): Motor Overcurrent, Door Failure, Leveling Error, Brake Fault, Encoder Fault, Safety Chain Trip — each as fault → causes → evidence, described as *"the foundation of your RCA engine."* A companion FMEA (§20: failure mode/cause/effect/detection method/severity/occurrence/detectability/action) is meant to become the *"static knowledge base."*
- **[RESEARCH GAP]** Neither document contains the actual populated fault trees, FMEA table, or Bayesian conditional-probability tables — only the case names, the field template, and one worked FMEA line (IGBT → short circuit → drive trip → elevator unavailable → current/temperature evidence). **NOT ESTABLISHED IN THE PROVIDED PROJECT MATERIALS.**
- **[EXPLICITLY STATED IN ROADMAP]** Five worked fault scenarios exist for validation/demo purposes (§42) — see section K.

## H. AI / Agent Architecture

- **[SUPPORTED BY PROVIDED TECHNICAL MATERIAL]** The proposal's agent table names: Alarm Correlation & Triage, Orchestrator Agent, Retrieval Agent, RCA Agent, Synthesis Agent, Explainability Engine, Human Review/Sign-off.
- **[EXPLICITLY STATED IN ROADMAP]** Roadmap §29 assigns one guiding question per agent: Signal Triage ("Is something abnormal?"), Orchestrator ("What investigation are we conducting?"), Retrieval ("What evidence do we have?"), **Fault Isolation Agent** ("Where is the problem?"), **RCA Agent** ("Why did it happen?"), Synthesis ("What should be done?"), Explainability Engine ("Why do we believe this?"), Human Reviewer ("Should the maintenance action proceed?").
- **Cross-document note:** the roadmap treats "Fault Isolation" and "RCA" as two distinct agents/questions (where vs. why), while the proposal's own architecture diagram merges them into a single RCA Agent box. This is a real terminology/structure gap between the two documents worth resolving explicitly before the booklet is written, not just a naming quirk — "where is the fault" and "why did it happen" may warrant separate evaluation criteria even if implemented in one component. **[RESEARCH GAP]**
- Related minor naming variance: the proposal calls the front-end triage component "Alarm Correlation & Triage"; the roadmap calls the same conceptual role the "Signal Triage Agent." Likely the same role, worth aligning on one name.
- **[EXPLICITLY STATED IN ROADMAP]** Explicit LLM-scoping discipline required at every stage: *"always ask: What should the LLM do? and What should the LLM NOT do?"* — e.g., the LLM must never freely invent a maintenance action (§38), and retrieval is meant to be deterministic/rule-based rather than LLM-driven (per the architecture diagram).
- **[EXPLICITLY STATED IN ROADMAP]** RAG requirements (§28): ingestion, chunking, embeddings, vector DB, metadata filtering, hybrid (BM25 + semantic) search, reranking, citation/source grounding. The system should retrieve maintenance manual + fault-code documentation + past maintenance + telemetry + event logs *before* producing a recommendation.
- **[EXPLICITLY STATED IN ROADMAP]** Flagged P0 competencies for the agent/LLM layer: ReAct, tool calling, agentic AI, structured outputs, function calling, planning, reflection, verification, self-consistency, multi-agent orchestration, agent memory, context management.

## I. Data and Evidence Flow

- **[SOURCE-DERIVED]** Five input streams, consistent across both documents: elevator system/motor/drive/controller data; sensor readings (current, vibration, door-cycle timing, encoder/position, load); alarm & event logs (fault codes, trip events); historical maintenance data (repairs, part replacements); technician free-text reports.
- **[SOURCE-DERIVED]** Pipeline: Data Ingestion & Normalization → Multi-Agent Core (analysis, isolation, RCA, action synthesis) → Actionable Outputs (fault location, confidence-ranked root cause, corrective actions, analysis report/insights) — rendered separately for technician and building-manager audiences from **one** underlying evidence trace.
- **[SUPPORTED BY PROVIDED TECHNICAL MATERIAL]** Proposed concrete schemas (§36): sensor schema (timestamp, elevator_id, sensor_id, value, unit, quality); alarm schema (timestamp, elevator_id, alarm_code, severity, subsystem, state); investigation schema (asset, time_window, symptoms, evidence, hypotheses, confidence, root_cause, action). The resulting "ExplainabilityTrace" object (observation, evidence, hypothesis, evidence for/against, alternatives, confidence, decision, action, source, timestamp) is called a *"major engineering artifact."*
- **[EXPLICITLY STATED IN ROADMAP]** Reference IoT/edge/cloud chain: Elevator → Sensors → Controller → Edge Gateway → Network → Cloud → Data Platform → AI, with candidate technologies flagged for research only (MQTT, OPC-UA, Kafka, time-series DBs, AWS IoT Core, Azure IoT, AWS Lambda/Step Functions, Databricks, Snowflake) — **no commitment to a specific stack is made in either document.** **[ASSUMPTION / RESEARCH GAP]**

## J. Safety and Cybersecurity Boundaries

- **[SOURCE-DERIVED]** Repeated, load-bearing constraint: the AI is advisory-only, with **no autonomous control path** to motor, brake, door locks, safety circuit, or any other safety-critical hardware; final decisions and physical interventions stay with qualified humans. The architecture diagram draws this as a blocked link, not just a stated rule.
- **[EXPLICITLY STATED IN ROADMAP]** Explicit conceptual boundary: **Observe → Diagnose → Explain → Recommend → Human confirms**, never **Observe → AI controls elevator**. §44 ("What NOT to Build") explicitly forbids: autonomous elevator controller, automatic safety override, autonomous passenger rescue, automatic brake release, automatic safety-chain reset, fully autonomous repair authorization.
- **[SOURCE-DERIVED]** Confidence-gated human-in-the-loop behavior: high confidence → recommend; low confidence → abstain → route to technician. Root-cause confidence and corrective-action confidence are meant to be scored **separately**, since accurate diagnosis doesn't guarantee correct remediation.
- **[RESEARCH GAP]** Relevant safety standards are named as research targets — EN 81-20/50, ASME A17.1/CSA B44, ASME A17.2, ASME A17.4, IEC 61508, IEC 62061, PESSRAL, ISO 8100/ISO 8102-20 — but neither document contains actual analysis against these standards yet. **NOT ESTABLISHED IN THE PROVIDED PROJECT MATERIALS.**
- **[REQUIRES EXTERNAL VERIFICATION]** The roadmap notes KONE has publicly discussed IEC 62443 certification for DX-class elevators and ISO 27001 for digital services including 24/7 Connected Services — meaning any real integration would need to clear an existing certification bar, not a theoretical one. Cybersecurity topics (secure boot, TLS, zero trust, prompt injection, RAG poisoning, etc.) are flagged for research; **the project's own security architecture is not yet defined in either document.** **[RESEARCH GAP]**

## K. Validation Strategy

- **[SOURCE-DERIVED]** The prototype will be evaluated against *"controlled, physics-grounded synthetic fault scenarios,"* assessed on: alarm-correlation correctness, fault-isolation accuracy, RCA accuracy (known cause ranked among top hypotheses), evidence/explainability traceability, confidence calibration, corrective-action relevance, and technician usefulness.
- **[EXPLICITLY STATED IN ROADMAP]** Explicit constraint: real KONE fault-labeled data isn't publicly available, and OEM fault-code tables (KONE/Otis/Schindler) aren't publicly documented. Validation must instead draw on synthetic fault injection, physics-based simulation, analogous public datasets (CWRU bearing data, NASA datasets), elevator-IoT literature, digital-twin simulation, or expert-labeled scenarios — and the roadmap explicitly warns against ever presenting synthetic/demo results as production validation.
- **[EXPLICITLY STATED IN ROADMAP]** Five canonical fault scenarios are recommended as the concrete basis for test data, fault-tree/RCA graphs, demos, the evaluation set, and judge explanations:

  | Scenario | Evidence conjunction | Root cause |
  |---|---|---|
  | 1 — IGBT / Motor Overcurrent | current spike + IGBT temp spike + no mechanical obstruction + drive self-test failure | IGBT fault |
  | 2 — Mechanical Jam | current↑ + vibration↑ + motor temp↑ + drive internally healthy | Mechanical obstruction |
  | 3 — Door Photo-eye Drift | door cycle time↑ + repeated reopen + photo-eye instability | Photo-eye degradation |
  | 4 — Encoder Fault | position mismatch + speed feedback inconsistency + leveling deviation | Encoder/position feedback fault |
  | 5 — Brake Problem | brake timing abnormal + motor torque normal + position drift | Brake system issue |

- **[EXPLICITLY STATED IN ROADMAP]** A broader metrics taxonomy beyond raw accuracy is specified (§40): detection (precision/recall/F1/false-alarm rate/latency), fault isolation (component accuracy, top-1/top-3), RCA (root-cause accuracy, top-k, evidence correctness, causal consistency), recommendation (action validity/safety/precision), system (MTTR, diagnostic latency, repeat visits, callback rate, downtime), explainability (evidence coverage, citation correctness, trace completeness).

## L. Competitive Landscape

- **[REQUIRES EXTERNAL VERIFICATION]** Per the roadmap, KONE 24/7 Connected Services already runs monitor → analyze → alert → report with AI-based analytics to flag maintenance needs before disruption, across 200+ parameters, and can help technicians investigate intermittent faults by "rewinding" historical equipment state. KONE already has a GenAI Technician Assistant — the roadmap states directly: *"your team cannot pitch 'AI assistant for KONE technicians' as the novelty."*
- **[REQUIRES EXTERNAL VERIFICATION]** Otis ONE: connects elevators to the cloud, provides real-time equipment status, predictive insights, and mechanic dispatch; mechanics reportedly get equipment info remotely rather than needing physical access to the controller fault log first.
- **[REQUIRES EXTERNAL VERIFICATION]** Schindler Ahead: a connected, cloud-based system with continuous monitoring, analytics, and a Technical Operations Center (roadmap cites a third-party source, "Elevator Solutions USA," for this — not a Schindler primary source). The roadmap explicitly warns not to conflate Schindler Ahead (digital monitoring/maintenance) with **Schindler PORT** (a separate traffic/access/destination-control ecosystem).
- **[REQUIRES EXTERNAL VERIFICATION]** TK Elevator MAX: the roadmap says the older MAX already provided ranked probable causes, and TK announced a newer 2026 agentic-AI service layer with multiple specialized agents, digital twins, and spare-parts recommendations. Direct consequence stated in the roadmap: *"'We are the first multi-agent AI elevator maintenance system' is no longer a safe claim."*
- **[RESEARCH GAP]** A detailed capability matrix (KONE / Otis / Schindler / TK / Our system, across ~19 capability rows including fault isolation, root-cause ranking, Bayesian reasoning, RAG, explainability trace, confidence + abstention, human approval) is specified as a deliverable but not populated in either document. **NOT ESTABLISHED IN THE PROVIDED PROJECT MATERIALS** — only the row/column skeleton exists.
- **[EXPLICITLY STATED IN ROADMAP]** Proposed differentiation strategy (§45): reject *"we use AI"* as a claim; argue instead from evidence-linked RCA, a structured ExplainabilityTrace object, exhaustive subsystem investigation, explicit alternative-cause elimination, confidence + abstention behavior, separately-scored diagnosis/action confidence, and dual-audience rendering — positioning against existing **monitoring** with **causal investigation**.
- All competitor claims above are attributed by the roadmap to public sources but have not been independently re-checked in this pass — flag for verification before use in the booklet or in judge Q&A, since vendor capabilities change.

## M. Known Research Gaps

- Real, labeled elevator-fault data is scarce and proprietary; OEM fault-code tables (KONE/Otis/Schindler) are not publicly documented. **[EXPLICITLY STATED IN ROADMAP]**
- The competitor comparison matrix, the six fault trees, the FMEA table (beyond one worked example), and the Bayesian conditional-probability tables are all specified in structure but **not populated** — **NOT ESTABLISHED IN THE PROVIDED PROJECT MATERIALS.**
- Safety standards (EN 81, ASME A17, IEC 61508/62061, PESSRAL, ISO 8100/8102-20) and cybersecurity architecture (IEC 62443, ISO 27001, secure boot, prompt-injection/RAG-poisoning defenses) are named as research targets, not yet researched in the provided material.
- The project's integration point into KONE's broader incident lifecycle (who dispatches, who selects parts, how a closed repair updates the system) is posed as an open question in the roadmap (§11) and unanswered in the proposal.
- The academic-literature matrix (§47: paper / subsystem / data / method / accuracy / limitation) is specified but not populated.
- **A cross-document tension worth flagging directly:** the roadmap states AWS + generative AI research is *"mandatory for the final round in 2026"* (§10), but the Idea Proposal — which is presumably the earlier-stage document — does not mention a cloud provider, AWS, or Bedrock anywhere. This gap between "what's required for the next round" and "what the current proposal actually specifies" seems like a natural next-step item.
- The terminology-exclusion item noted at the top of this report (architecture reuse mapping) is treated here as internal context only, not reproduced by name, per your instruction.

## N. Known Assumptions

- **[ASSUMPTION]** KONE-specific fault taxonomy, fault-code mappings, and diagnostic rules in the proposal are explicitly labeled illustrative, pending KONE SME input — they are not claimed to be accurate today.
- **[ASSUMPTION]** The system assumes access to elevator telemetry, alarm/event logs, maintenance history, and technician observations; actual availability and quality are explicitly stated as unassessed.
- **[ASSUMPTION]** Initial validation will use synthetic, physics-grounded scenarios rather than field data — stated as a deliberate choice, not an oversight.
- **[SOURCE-DERIVED]** The door-jam cascade example used throughout the proposal is explicitly labeled as illustrative, not based on a specific KONE service case.
- **[SOURCE-DERIVED]** No elevator architecture (traction/hydraulic/MRL, etc.) has actually been committed to yet — the roadmap poses this as something to decide, not something already assumed. This is a gap, not yet an assumption made.

## O. Known Limitations

- **[SOURCE-DERIVED]** No production or field validation exists yet; only synthetic scenario testing is currently planned.
- **[SOURCE-DERIVED]** The system is designed to reduce confidence and abstain rather than force a conclusion when evidence is incomplete or conflicting — by design, it will sometimes not produce a definitive answer.
- **[SOURCE-DERIVED]** No autonomous-action capability by design — the system cannot act on its own conclusions; human confirmation is always required. This is a deliberate scope boundary, not something to be "fixed" later.
- **[EXPLICITLY STATED IN ROADMAP]** Any differentiation claim implying the project is "first" or uniquely novel in multi-agent AI for elevator maintenance is explicitly flagged as unsafe given TK Elevator's stated 2026 direction.

## P. Important Unresolved Questions

- Which specific elevator architecture(s) is the system targeting? (§1.1)
- Who receives the alert, decides severity, dispatches, selects parts, handles a callback, and how does the system "learn" from a completed repair? (§11)
- Which CMMS/EAM system(s) does maintenance history and work-order data actually need to come from? (§13)
- What does a KONE technician concretely see today, before arriving at an elevator — i.e., what is the real baseline this project needs to beat? (§9)
- Can historical repair data legitimately shift the Bayesian prior probability of a future fault? (§37, described in the roadmap as "an excellent Bayesian/RCA question")
- How should "where is the fault" (isolation) and "why did it happen" (root cause) be cleanly separated in the agent pipeline, given the mismatch between the two documents noted in section H?
- At each pipeline stage, precisely what is the LLM allowed to do, and what is it explicitly barred from doing? (§27, §38)
- What is the team's specific, defensible answer to *"why would KONE build this if KONE already has 24/7 Connected Services?"* — the roadmap treats this as the question the whole project must ultimately answer. (§45, dependency chain)

## Q. Complete Research Dependency Chain

**[EXPLICITLY STATED IN ROADMAP]** The roadmap gives this sequence explicitly, with the instruction that it should be followed in order:

```
ELEVATOR
  → How does it work?
  → What can physically fail?
  → What sensors detect it?
  → What alarms are generated?
  → Which alarms are consequences?
  → How do technicians diagnose?
  → How is RCA formalized?
  → How can AI automate the RCA?
  → How do competitors do this?
  → What does KONE already have?
  → What is genuinely missing?
  → What can we safely demonstrate?
  → How do we validate it?
  → How do we prove the value?
```

Restated by the roadmap as a progression: **elevator engineering → failure physics → sensor evidence → diagnostic reasoning → AI → safety → implementation** — with an explicit caution against starting from *"which LLM should we use?"* This chain is the backbone I used to order the chapter structure in section R.

## R. Proposed Chapter Structure for the Master Research Book

This is a **proposed organizational synthesis**, not a verbatim roadmap deliverable — I've mapped the roadmap's 48 research topics (respecting their P0/P1/P2/P3 priorities and the dependency chain above) into a book structure, framed per your instruction entirely around **"KONE Elevate — Autonomous Fault Isolation & Root Cause Analysis"** and the RCA Agent architecture. No chapter content has been written; this is the outline only, for your review before anything gets drafted. Roadmap topic numbers are in brackets for traceability.

**Working title:** *KONE Elevate — Autonomous Fault Isolation & Root Cause Analysis: Master Research Book*

**Part I — Elevator Engineering Foundations** *(P0)*
1. How Elevators Work: Types & Architectures [§1.1]
2. Elevator Mechanical Systems: Motor, Drive Train, Car & Counterweight [§1.2]
3. Elevator Electrical & Control Architecture: Controller, VFD/VVVF, PMSM [§2]
4. The Elevator Door System and Its Failure Modes [§3]
5. Brake, Rope & Traction System: Mechanics and Failure Modes [§4]

**Part II — Sensing, Faults & Alarms** *(P0)*
6. Elevator Sensors & Telemetry: A Complete Signal Dictionary [§5]
7. Fault Codes & Alarm Architecture: Why "Fault Code ≠ Root Cause" [§6]
8. Alarm Correlation & Alarm-Flood Management [§22]
9. Time-Series Signal Processing for Elevator Diagnostics [§23]
10. Anomaly Detection: Methods and a Defensible Baseline [§24]

**Part III — The KONE Ecosystem** *(P0)*
11. KONE Elevator Architecture & Product Families [§7]
12. KONE's Digital Ecosystem: 24/7 Connected Services [§8]
13. KONE Technician Tools & Software; What a Technician Sees Today [§9]
14. KONE + AWS + Generative AI [§10]
15. The KONE Maintenance Workflow, End to End [§11]
16. Maintenance Methodologies & Where This Project Sits [§12]
17. CMMS/EAM & the Maintenance-Software Landscape [§13]

**Part IV — Competitive Landscape** *(P0)*
18. Otis ONE [§14]
19. Schindler Ahead (and Why Schindler PORT Is a Different Thing) [§15]
20. TK Elevator MAX and Its 2026 Agentic-AI Direction [§16]
21. Competitor Comparison Matrix [§17]

**Part V — Root-Cause Analysis Methodology** *(P0)*
22. RCA Fundamentals: From 5 Whys to Bayesian Networks [§18]
23. Fault Tree Construction for Six Canonical Elevator Faults [§19]
24. FMEA for Elevator Components [§20]
25. Bayesian Root-Cause Reasoning [§21]

**Part VI — AI, Agents & Explainability** *(mostly P0)*
26. Elevator-Specific AI: The Academic Landscape [§25]
27. Digital Twins: What They Are, and Why We're Not Building One (Yet) [§26, P1]
28. LLMs for Industrial RCA: What the Model Should and Shouldn't Do [§27]
29. Retrieval-Augmented Generation for Maintenance Evidence [§28]
30. Multi-Agent Architecture: One Question per Agent [§29]
31. Explainable AI & the ExplainabilityTrace [§30]
32. Confidence & Uncertainty: Separating Diagnosis from Action [§31]
33. Human-in-the-Loop: Escalation and Abstention [§32]

**Part VII — Safety, Security & Data** *(P0)*
34. Safety Engineering & Standards (EN 81, ASME A17, IEC 61508…) [§33]
35. Elevator Cybersecurity [§34]
36. IoT, Edge & Cloud Architecture [§35]
37. Data Architecture: Schemas for Sensors, Alarms & Investigations [§36]
38. Historical Maintenance Data as a Bayesian Prior [§37]

**Part VIII — From Diagnosis to Action**
39. Corrective Action Synthesis: Why the LLM Doesn't Invent Repairs [§38]
40. Technician & Building-Manager Workflows: One Trace, Two Audiences [§39]

**Part IX — Validation, Boundaries & Differentiation** *(P0)*
41. Metrics & Evaluation Beyond "Did It Guess Right?" [§40]
42. Validation Strategy Under Data Scarcity [§41]
43. The Fault Scenario Library: Five Canonical Cases [§42]
44. Architecture Design Rationale & Scope Boundaries — what's newly built vs. adapted, and an explicit list of what this system will never do (autonomous control, safety override, etc.) [generalized from §43's reuse-mapping content + §44]
45. Competitive Differentiation: The Central Research Question [§45]

**Part X — Advanced Topics & Literature** *(P1/P2, background)*
46. Advanced/Future Techniques (GNNs, PINNs, few-shot learning, etc.) [§46]
47. Academic Literature Review [§47]

**Appendix — Team Research Division** [§48] *(organizational reference, not book content)*

**Quick cross-reference — the roadmap's "12 non-negotiable" topics against this structure:**

| # | Non-negotiable topic | Maps to chapter(s) |
|---|---|---|
| 1 | How a modern traction elevator works | 1–2 |
| 2 | KONE architecture & DX/connected ecosystem | 11–12 |
| 3 | KONE 24/7 Connected Services & Technician Assistant | 12–13 |
| 4 | Otis ONE | 18 |
| 5 | Schindler Ahead | 19 |
| 6 | TK Elevator MAX + 2026 agentic-AI direction | 20 |
| 7 | Elevator subsystem failure modes & sensor signatures | 4–6 |
| 8 | Fault Tree + FMEA + Bayesian RCA | 23–25 |
| 9 | Alarm correlation / primary-vs-consequential faults | 8 |
| 10 | Time-series anomaly detection + signal processing | 9–10 |
| 11 | Elevator safety standards + cybersecurity | 34–35 |
| 12 | Explainable, evidence-grounded multi-agent RCA | 30–31 (and 26–33 broadly) |

---

*This concludes the Project Understanding Report. No chapter content has been drafted — waiting on your next instruction.*
