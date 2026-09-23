# PHASE 8 — SAFETY ENGINEERING, CYBERSECURITY, DATA ARCHITECTURE & INDUSTRIAL DEPLOYMENT

### *KONE Elevate — Autonomous Fault Isolation & Root Cause Analysis: Master Research Book*

## How to Read This Chapter

Labels: **[PROJECT SOURCE]**, **[OFFICIAL STANDARD / REGULATORY SOURCE]** (verified via live research where the standard is specialized enough to risk error from memory — noted per instance), **[OEM SOURCE]**, **[ACADEMIC EVIDENCE]**, **[OFFICIAL TECHNOLOGY DOCUMENTATION]**, **[INDUSTRY EVIDENCE]**, **[ENGINEERING INFERENCE]**, **[PROPOSED DESIGN]** (this project's own architectural choice, never a claim about an existing KONE system), **[NOT ESTABLISHED]**. This chapter does not reproduce copyrighted standard text — every standard below is summarized for its architectural implications only, and its actual authoritative text should be consulted directly before any real engineering decision relies on it.

**The central question of this chapter:** *how can an AI-assisted elevator fault-isolation and root-cause-analysis system be designed, integrated, secured, validated, and deployed around a safety-critical industrial system without becoming a safety or cybersecurity liability?*

**The central principle, governing everything below:**

> **THE AI DIAGNOSTIC SYSTEM MUST BE DESIGNED AROUND THE SAFETY ARCHITECTURE OF THE ELEVATOR, NOT THE OTHER WAY AROUND.**

---

## From Phase 7 to Phase 8

Phase 7 demonstrated how AI can potentially reason over engineering evidence. But an elevator is not an ordinary software application — it is safety-critical, physically constrained, connected, distributed, cyber-physical, maintained in the field, subject to real regulatory requirements, and dependent on safety mechanisms that must remain independent of any diagnostic layer. **A highly intelligent AI system can still be unacceptable** if it compromises safety, introduces a meaningful attack surface, provides an unsafe recommendation, becomes a single point of failure, receives corrupted data without noticing, loses connectivity ungracefully, produces unexplained decisions, or cannot be audited.

```
AI CAPABILITY → SAFETY CONSTRAINT → CYBERSECURITY CONSTRAINT
        → ARCHITECTURAL BOUNDARY → VALIDATED INDUSTRIAL SYSTEM
```

---

# Part I — The Safety Architecture

## 10.1 Safety-Critical vs. Mission-Critical vs. Non-Critical

*[ENGINEERING INFERENCE, standard systems-engineering terminology]* A **safety-critical** function's failure can cause physical harm. A **mission-critical** function's failure prevents the system from accomplishing its core purpose, without necessarily causing physical harm. A **business-critical** function's failure causes financial or reputational damage without threatening either safety or the core mission. A **diagnostic-support** function assists a human decision-maker without itself being required for safety, mission, or business continuity.

| Function | Safety Critical? | Consequence of Failure | Appropriate AI Role |
|---|---|---|---|
| Elevator motion control | Yes | Physical harm possible | **None** |
| Door safety (lock/interlock) | Yes | Physical harm possible | **None** |
| Brake control | Yes | Physical harm possible | **None** |
| Overspeed protection | Yes | Physical harm possible | **None** |
| Emergency systems | Yes | Physical harm possible | **None** |
| Telemetry analysis | No | Missed/delayed insight | Full — this is the project's core domain |
| Anomaly detection | No | False positive/negative diagnosis | Full, with abstention |
| Alarm correlation | No | Miscorrelated incident | Full, with human review |
| RCA | No | Wrong diagnosis, wasted effort | Full, with confidence + human verification |
| Technician recommendation | No | Wasted time, wrong first step | Recommend only, human decides |
| Maintenance prioritization | No | Suboptimal scheduling | Recommend only |
| Passenger communication | Partially (emergency comms specifically can be safety-adjacent) | Delayed/incorrect information during an incident | Support, not replace, existing approved channels |

**Where KONE Elevate's RCA function should be positioned, precisely:** entirely within the bottom, non-safety-critical portion of this table — a diagnostic-support function whose worst-case failure is a wrong or delayed diagnosis, never physical harm, because it has no path to any of the top rows. **This book provides no instructions for defeating or bypassing any safety mechanism**, and this table's structure is itself the reason none are needed: the AI's entire addressable scope sits below the line where such instructions would even be relevant.

## 10.2 The Fundamental Safety Principle: AI Is Not the Safety Controller

The architecture conceptually separates two systems entirely:

**The safety control system** performs certified safety functions — hardware-level, independent, and (per §10.4) governed by specific, rigorous standards.

**The diagnostic AI system** observes available information, identifies probable causes, and supports maintenance decisions — nothing more.

**Why this separation matters, stated plainly:** a safety controller must behave correctly under a formally analyzed, bounded set of failure conditions, verified against rigorous engineering standards, because its failure mode is physical harm. A diagnostic AI's failure mode — a wrong or unhelpful suggestion — is a fundamentally different, much lower-consequence category of risk, and conflating the two categories, even with good intentions, is the single most dangerous architectural mistake this project could make.

## 10.3 Elevator Safety Architecture, Revisited

Returning to Chapter 1's foundation with the safety lens now explicit: the safety chain, door interlocks, overspeed protection (governor + safety gear), brakes, emergency operation, Unintended Car Movement Protection (UCMP), terminal stopping/protection, emergency communications, inspection operation, controller supervision, and independent protective functions generally (Ch.1 §1.4, Ch.3 §3.2/§3.4, Ch.4 §4.7-G) together form a layer that is, by design, **independent of the elevator's normal control logic** — precisely so that a fault in normal operation (including, now, a fault in any diagnostic AI layered on top of it) cannot compromise safety.

```
                ELEVATOR CONTROL
                      │
        ┌─────────────┴─────────────┐
        ↓                           ↓
 NORMAL CONTROL              SAFETY FUNCTIONS
        │                           │
        ↓                           ↓
 MOTION / DOORS              INDEPENDENT
 DRIVE / LOGIC               PROTECTION
        │                           │
        └─────────────┬─────────────┘
                      ↓
              PHYSICAL ELEVATOR
```

```
            DIAGNOSTIC AI
                  ↓
              OBSERVES
                  ↓
              ANALYZES
                  ↓
             RECOMMENDS

   (no path into either branch above)
```

## 10.4 The Safety Standards Landscape

*[OFFICIAL STANDARD / REGULATORY SOURCE — summarized for architectural relevance only; none of this reproduces copyrighted standard text, and none of it should substitute for consulting the actual standards]*

| Standard | Scope | Architectural Implication for an AI Diagnostic Layer |
|---|---|---|
| **EN 81-20** | Safety rules for the construction and installation of new passenger and goods lifts (European harmonized standard) | Defines the physical/design safety baseline (door protection, safety gear, buffers, and similar) the elevator itself must meet — the AI layer operates entirely outside this scope, observing its outputs, never modifying its requirements |
| **EN 81-50** | Design rules, calculations, examinations, and tests of lift components (companion to EN 81-20, component-level) | Component-level verification/testing methodology — relevant context for understanding what "verified" means for a physical safety component, a bar the AI layer is not attempting to meet or replace |
| **ISO 8100 series** | International lift/escalator/moving-walk safety standards, broadly harmonized with the EN 81 approach at the international level | The umbrella international framework several other standards in this chapter (notably ISO 8102-20, §10.11) explicitly reference and build on |
| **ASME A17.1 / CSA B44** | North American Safety Code for Elevators and Escalators (harmonized US/Canadian code) | The North American analog to EN 81/ISO 8100 — the relevant baseline if this project were ever deployed in a North American context |
| **ASME A17.2** | Guide for Inspection of Elevators, Escalators, and Moving Walks | **Directly relevant to a critical distinction (§10.5): an AI diagnostic recommendation is not equivalent to a formal inspection or test result governed by this guide** — inspection/testing has its own defined, certified methodology the AI layer does not perform or substitute for |
| **ASME A17.4** | Guidance concerning emergency personnel and evacuation procedures for elevator incidents | **This project provides no rescue or evacuation procedure of any kind** — passenger emergency handling must remain governed entirely by approved procedures and trained emergency personnel, never AI improvisation, regardless of how confident the AI's situational assessment might seem |
| **IEC 61508** | Functional safety of electrical/electronic/programmable electronic (E/E/PE) safety-related systems — the foundational, cross-industry functional-safety standard | Defines **Safety Integrity Levels (SIL 1–4)** and the full safety lifecycle (hazard/risk analysis → safety requirements → design → verification → validation → operation). **This book does not claim any SIL classification for KONE Elevate** — that would require an actual, formal safety analysis this project has not performed, and claiming one without it would be a serious credibility failure |
| **IEC 62061** | Functional safety of safety-related control systems, specifically for machinery (a machinery-sector application of IEC 61508's principles) | Reinforces, in a machinery-specific context, that safety-related control systems require a defined lifecycle and formal risk reduction — not simply a claim of "high accuracy" (§10.5 makes this distinction the chapter's own point) |

**PESSRAL** — Programmable Electronic Systems in Safety-Related Applications for Lifts — deserves separate, deeper treatment, because it's the standard most directly relevant to *why* an AI layer must stay outside the safety loop, and because it has a specific, verifiable history worth getting right. PESSRAL entered lift standards via a 2005 amendment to the earlier EN 81-1/81-2 series, and its principles were later formalized internationally as **ISO 22201** ("Lifts (elevators), escalators and moving walks — Programmable electronic systems in safety-related applications"), which explicitly builds on IEC 61508 (referencing its constituent parts on general requirements, E/E/PE system requirements, software requirements, and application guidelines) and uses SILs to specify target failure measures for lift safety functions. **The core idea PESSRAL formalizes:** programmable electronics *can* participate in elevator safety functions — replacing older hardwired/relay-based safety circuits — but only under a rigorous engineering discipline specifically designed for this purpose, including self-diagnostics, defined verification, and a defined safety lifecycle. Industry commentary on PESSRAL (an Elevatori Magazine analysis) explicitly warns that "cherry picking and skipping the basics" when applying it can produce unsafe systems, and a 2026 *Elevator World* piece frames the same territory — programmable safety electronics amid growing IoT, predictive maintenance, and digital-twin adoption — as creating "significant cybersecurity and organizational challenges," explicitly noting that "certification and standards lag behind rapid innovation, creating compliance gaps."

> **KEY CONCEPT:** PESSRAL is proof that programmable electronics *can*, in principle, safely participate in elevator safety functions — but only through a specific, rigorous, independently-verified engineering discipline built for exactly that purpose. **A research-stage diagnostic AI prototype should never casually imply it meets, or is even attempting to meet, this bar.** This project's AI layer is deliberately, architecturally kept *outside* the safety-related-systems boundary PESSRAL governs, precisely because meeting that bar is a separate, much larger, formally-verified engineering undertaking this project does not claim to have performed.

## 10.5 Safety Integrity vs. AI Accuracy

The single most important conceptual distinction in this Part, stated directly: **a model can have 99% classification accuracy and still be entirely inappropriate for a safety function.** Conversely, **a diagnostic AI can be extremely useful without itself being part of the safety-control loop at all.** These are not in tension — they are the same principle stated twice.

| Concept | Meaning |
|---|---|
| Accuracy | Fraction of predictions that are correct overall |
| Precision | Of the cases flagged positive, how many genuinely were |
| Recall | Of the genuine positive cases, how many were flagged |
| Availability | Fraction of time a system is operational and responsive |
| Reliability | Probability a system performs correctly over a given period |
| Functional safety | Freedom from unacceptable risk of physical harm due to system malfunction — a formally defined, certified property, not a statistical one |
| Fail-safe behavior | The system defaults to a known-safe state on failure, rather than an undefined or unsafe one |
| Fault tolerance | The system continues correct operation despite a component failure |
| Diagnostic coverage | The fraction of possible failures a system can actually detect |
| Validation | Confirming a system meets its intended purpose under realistic conditions, following a defined, repeatable methodology |

**Why 99% accuracy is not functional safety:** functional safety is a certified, formally-verified property established through a defined lifecycle (hazard analysis, safety requirements, verified design, independent assessment) against a bounded, analyzed set of failure modes — an accuracy percentage measured on a test set says nothing about *worst-case* behavior, *independence* from other failure sources, or *certified* verification, all of which functional safety specifically requires. This project's diagnostic AI is useful precisely because it does not need to clear that bar — its entire value proposition rests on staying in a role where a wrong output costs time and trust, never safety.

## 10.6 Fail-Safe Architecture and Single Points of Failure

**Fail-safe behavior**, applied to every plausible AI-layer failure — the model unavailable, the cloud unavailable, telemetry missing, sensor data corrupted, retrieval failing, the network down, the database unavailable — resolves to one governing rule: **the elevator continues to rely entirely on its established, independent safety/control architecture, regardless of what happens to the diagnostic AI layer.** The diagnostic AI degrades gracefully; the elevator does not degrade at all as a result of the AI's state.

```
NORMAL
   ↓
DEGRADED           (partial evidence available, lower confidence, more abstention)
   ↓
AI UNAVAILABLE     (falls back to existing, pre-AI maintenance processes)
   ↓
SAFE DIAGNOSTIC FALLBACK
```

**"Safe fallback" does not mean giving the AI authority to control the elevator when something goes wrong with the AI itself** — it means the *opposite*: the AI having no such authority in the first place is precisely what makes its own failure safe.

**Why making the AI service a single point of failure would be architecturally dangerous, even though it's not safety-critical:** cloud failure, edge failure, database failure, network outage, model failure, or identity-service failure should each degrade *diagnostic capability*, not create a cascading dependency anywhere else in the maintenance workflow — the existing, pre-AI maintenance process (Ch.5 §5.12) must remain fully functional with the AI layer entirely absent, which is both a safety-adjacent design requirement and, independently, good general systems-engineering practice.

## 10.7 AI Safety Boundaries

| Function | AI May Observe | AI May Analyze | AI May Recommend | Human Required | AI Must Not Control |
|---|---|---|---|---|---|
| Elevator movement | ✓ | ✓ | | | ✓ |
| Door state | ✓ | ✓ | | | ✓ |
| Brake state | ✓ | ✓ | | | ✓ |
| Safety chain | ✓ (state only) | | | ✓ (always) | ✓ |
| Anomaly detection | ✓ | ✓ | ✓ | | |
| Fault isolation | ✓ | ✓ | ✓ | | |
| RCA | ✓ | ✓ | ✓ | ✓ (verification) | |
| Inspection recommendation | | ✓ | ✓ | ✓ (before acting) | |
| Maintenance prioritization | | ✓ | ✓ | ✓ (final decision) | |
| Repair recommendation | | ✓ | ✓ | ✓ (before acting) | |
| Safety override | | | | | ✓ — **never, under any circumstance** |

## 10.8 Human-in-the-Loop Safety

Continuing Chapter 9 §9.33 with the safety framing made explicit:

```
AI → Recommendation → Evidence → Confidence → Human review → Approved maintenance process
```

Discussed dimensions, all already established but now anchored specifically to safety consequence rather than general quality: **technician review** (the default path for every conclusion), **escalation** (for genuinely ambiguous or high-stakes cases), **override** (a human's judgment always takes precedence over the AI's), **disagreement** (surfaced explicitly, never silently resolved in the AI's favor), **low-confidence cases** (routed to review by design, Ch.9 §9.31), and **high-risk recommendations** (receiving the same or greater scrutiny regardless of how confident the AI's output happens to be).

---

# Part II — Cybersecurity

## 10.9 The Cyber-Physical System

An elevator connected to cloud/IoT infrastructure is, structurally, a **cyber-physical system** — a physical, safety-relevant process (Part I) coupled to a digital, networked information system (this Part).

```
PHYSICAL ELEVATOR → CONTROLLER → EDGE/GATEWAY → NETWORK → CLOUD → DATA PLATFORM → AI → TECHNICIAN
```

**Every boundary in this chain introduces its own trust, authentication, authorization, data-integrity, confidentiality, availability, and monitoring requirements** — a cyber-physical system's overall security is only as strong as its weakest individual boundary, which is precisely why the remainder of this Part treats each boundary as its own concern rather than assuming one blanket "secure" label covers the whole chain.

## 10.10 Threat Modeling

*[ENGINEERING INFERENCE, standard security-engineering methodology]*

```
Assets → Threats → Attack surfaces → Threat actors → Vulnerabilities → Consequences → Controls
```

**Conceptual assets:** the elevator controller, edge gateway, sensors, firmware, diagnostic data, credentials, APIs, cloud infrastructure, databases, the RAG knowledge base, AI models, technician applications, and maintenance records — **asset inventory is foundational** precisely because a threat or control can't be meaningfully reasoned about until it's clear what's actually being protected.

**Threat actor categories** (discussed at the category level only — this book provides no offensive instruction of any kind): opportunistic attackers (low-sophistication, broad-target), criminal actors (financially motivated, more sophisticated), insiders (with legitimate but potentially misused access), compromised vendors, compromised devices (already-breached equipment used as an entry point), and supply-chain attackers (compromising a trusted component before it ever reaches the deployed system).

**Attack surfaces, at the category level:** sensors, controller interfaces, gateways, the network itself, APIs, cloud infrastructure, mobile/technician applications, identity systems, software-update mechanisms, the RAG knowledge base, and AI model interfaces — a notably longer list than a traditional, non-AI industrial system would have, since the AI/RAG layer (Ch.9 §9.36) introduces genuinely new surface area beyond conventional OT/IT security concerns.

## 10.11 The Cybersecurity Standards Landscape

**IEC 62443** *[OFFICIAL STANDARD / REGULATORY SOURCE]* — the leading industrial automation and control systems cybersecurity framework. Core concepts: **zones** (groups of assets sharing a common security requirement), **conduits** (the defined, controlled communication paths between zones), **security levels** (graduated protection targets, typically SL 1 through SL 4, reflecting increasing threat sophistication), **defense in depth** (§10.34), and a full security **lifecycle** spanning specification, design, implementation, and maintenance. Applied conceptually to this project's ecosystem: the elevator controller and safety chain form one zone (the most restricted); the diagnostic AI, RAG knowledge base, and technician applications form a separate zone; the conduit between them should be narrow, monitored, and — per Part I — strictly one-directional in terms of any actionable authority (observational data flows toward the AI layer; nothing flows back that could influence safety-critical behavior). **This project does not claim IEC 62443 certification** — that requires a formal assessment this research book has not performed.

**ISO/IEC 27001** — information security *management*, distinguished from the technical controls IEC 62443 specifies: governance, policies, risk management, access control, incident management, and continuous improvement, organized as a management-system discipline rather than a technical specification. **How it complements IEC 62443:** 27001 governs the organizational processes and accountability around security; IEC 62443 (and ISO 8102-20, below) governs the technical implementation specific to industrial/lift systems — a mature security posture needs both, not either alone.

**ISO 8102-20:2022** — "Electrical requirements for lifts, escalators and moving walks — Part 20: Cybersecurity," published by ISO/TC 178 in August 2022, is **the first cybersecurity standard written specifically for lifts, escalators, and moving walks.** *[OEM SOURCE — KONE's own published account]* KONE played a direct, documented role in its development: three senior KONE team members served on the working group, and KONE's own Leading Expert, Ari Kattainen, convened it — a genuinely concrete confirmation that cybersecurity is not a theoretical concern for this project's real-world context, consistent with what Chapter 3's research already established. The standard covers the full lifecycle (product development, manufacturing, installation, operation/maintenance, decommissioning) for "Equipment Under Control" (EUC) capable of connecting to external systems, defines **three security levels** with safety functions requiring the strictest (Security Level 3) and alarm functions requiring the lightest (Security Level 1), and is explicitly built on **IEC 62443** rather than reinventing its own technical framework — mapping roles and lifecycle practices directly to IEC 62443-4-1's product-supplier and system-integrator model. It does not mandate third-party certification but explicitly recommends independent security-vulnerability analysis and periodic penetration testing. **Relevant caveat:** it does not apply retroactively to equipment installed before its publication, and a revision is already in development at the time of this research — standards in this space are actively evolving, not fixed.

**The NIST Cybersecurity Framework** *[OFFICIAL STANDARD / REGULATORY SOURCE]* organizes security activity into five functions: **Identify** (understand assets and risk — §10.10's threat model), **Protect** (implement safeguards — §10.12's technical controls), **Detect** (monitor for anomalous activity — §10.23's observability), **Respond** (act on detected incidents), and **Recover** (restore normal operation — §10.24's resilience/disaster-recovery discussion). Mapped to KONE Elevate: this entire Phase 8 chapter is, structurally, an Identify-and-Protect-level exercise; Detect, Respond, and Recover remain largely deferred to actual operational deployment, appropriately, since this project has not yet reached that stage.

**Zero trust** — "never trust, always verify" — replaces the older assumption that anything inside a network perimeter is implicitly trustworthy with continuous verification of device identity, user identity, and service identity, combined with least-privilege access at every step. **Why this matters specifically for a connected elevator ecosystem:** a compromised technician device, a compromised gateway, or a compromised API credential should never automatically grant broad access simply because it originated from inside the "trusted" network — every request, including ones the AI layer itself makes to a tool (Ch.9 §9.14), should be independently verified and scoped.

## 10.12 Technical Security Controls

| Control | Purpose | Elevator-Ecosystem Application |
|---|---|---|
| Identity and access management | Authenticate and authorize every actor | Distinct identities for technicians, service accounts, and the AI system itself, each with least-privilege scope |
| Encryption in transit | Protect data moving between systems | TLS (or equivalent) for telemetry, alarm data, and any AI-tool communication |
| Encryption at rest | Protect stored data | Applied to telemetry stores, maintenance records, and the RAG knowledge base alike |
| Secure boot / signed firmware | Ensure a device only runs verified, unmodified software | Directly relevant to the edge gateway and controller-adjacent hardware |
| OTA update security | Ensure updates are authentic and haven't been tampered with | Authentication, integrity verification, rollback capability, staged/tested deployment before full rollout |
| Network segmentation | Prevent lateral movement between zones | The safety-chain zone remains isolated from the diagnostic/IT zone (§10.13) |

**This book provides no insecure implementation shortcuts and no credential material of any kind** — every control above is discussed at the architectural-principle level, appropriate for a research book establishing requirements, not an implementation guide.

## 10.13 Network Segmentation

**Why the diagnostic/IT environment should not automatically have unrestricted access to elevator control systems:** this is IEC 62443's zones-and-conduits principle (§10.11) applied concretely — a defined **conduit**, not open network access, should connect the diagnostic AI's data-ingestion layer to the elevator's telemetry sources, with firewalls, gateways, and (where appropriate) a DMZ-style intermediate zone enforcing that the connection remains observational, monitored, and narrowly scoped, never a path by which a compromise of the diagnostic layer could reach the safety-control zone.

---

# Part III — Data Integrity and Architecture

## 10.14 Data Integrity, Quality, and Time Synchronization

**RCA depends entirely on trustworthy evidence** — restating Chapter 6 §8.43's data-quality chain with the security lens now added: threats to timestamps, sensor values, event logs, maintenance records, and documents include not just accidental corruption (Ch.6 §8.5) but deliberate **tampering**, alongside duplication, clock errors, and missing records more generally. **BAD DATA → BAD RCA** holds regardless of whether the badness is accidental or adversarial — which is exactly why data-integrity controls (checksums, signed telemetry where feasible, tamper-evident logging) matter here as much as the purely quality-focused mitigations Chapter 6 already established.

| Data Problem | Diagnostic Consequence | Mitigation |
|---|---|---|
| Missing data | Silence mistaken for "normal" (Ch.7 §7.26) | Explicit missing-data flagging, never silent imputation |
| Stale data | Outdated evidence treated as current | Timestamp/version checks before use |
| Corrupted data | Wrong evidence trusted | Validation against expected ranges/patterns (Ch.6 §8.5) |
| Sensor drift | Gradual, easy-to-miss evidence degradation | Periodic cross-checking against independent signals (Ch.7 §7.34) |
| Duplicate events | Inflated apparent evidence, false confidence | Deduplication logic |
| Timestamp mismatch | False or missed causal relationships (§10.14 below) | Synchronized clocks, explicit alignment checks (Ch.6 §8.4) |
| Unit mismatch | Silently wrong calculations | Explicit unit validation at ingestion |
| Impossible values | Corrupted or spoofed data treated as real | Range/plausibility checks |
| Inconsistent identifiers | Evidence misattributed to the wrong asset | A canonical identifier scheme (§10.18) |

**Why timestamps matter, restated with the multi-system reality of a real deployment in view:** event chronology, sensor alignment, and the primary/consequential alarm reasoning that runs throughout this book (Ch.4 §4.5, Ch.6 §8.22) all depend on genuinely correct temporal ordering across what is, in a real deployment, a distributed system with multiple independent clocks — **clock drift between subsystems, uncorrected, can silently produce an incorrect causal story**, exactly the risk Chapter 6 §8.4 flagged at the signal-processing level and now reappearing as a full data-architecture requirement.

## 10.15 The Data Architecture

```
PHYSICAL SENSORS
     ↓
CONTROLLER / EDGE
     ↓
INGESTION
     ↓
STREAM PROCESSING
     ↓
TIME-SERIES STORAGE
     ↓
EVENT STORE
     ↓
MAINTENANCE DATA
     ↓
DOCUMENT STORE
     ↓
KNOWLEDGE LAYER
     ↓
AI / RCA
     ↓
TECHNICIAN APPLICATION
```

Each layer's role, briefly: **ingestion** validates and normalizes incoming data at the boundary (§10.14's checks applied here, first); **stream processing** applies Chapter 6's real-time signal-processing methods; **time-series storage** and the **event store** hold continuous telemetry and discrete events respectively, reflecting Chapter 6 §8.2's fundamental data-type distinction; **maintenance data** and the **document store** hold historical repair records and retrievable documentation respectively (Ch.5 §5.16, Ch.9 §9.17); the **knowledge layer** holds the structured engineering knowledge from Chapter 7 (fault trees, FMEA, knowledge graphs); **AI/RCA** is this book's Chapters 7–9 combined reasoning layer; and the **technician application** is the human-facing endpoint where Part I's human-in-the-loop requirement is actually exercised.

## 10.16 Edge vs. Cloud

**Edge computing** — processing near the elevator rather than in the cloud — matters for latency (some evidence needs near-real-time availability), bandwidth (not every raw signal needs to leave the site), resilience to connectivity loss (Chapter 6's signal processing can continue locally even if the network drops), and privacy (some data may be appropriately kept local). **Cloud computing** matters for large-scale storage, historical analytics, fleet-wide learning, model management, document retrieval at scale, dashboards, and centralized orchestration — capabilities that inherently benefit from aggregation across many elevators, not just one.

| Function | Edge | Cloud | Why |
|---|---|---|---|
| Safety control | N/A (safety architecture is independent, per Part I) | N/A | Outside this system's scope entirely |
| Signal preprocessing | **Preferred** | Possible | Low latency, resilient to connectivity loss |
| Anomaly detection (statistical baseline) | **Preferred** | Possible | Fast, lightweight, works even offline |
| Anomaly detection (deep learning) | Possible | **Preferred** | Heavier compute, benefits from centralized model management |
| Historical analytics | Not suited | **Preferred** | Needs fleet-scale, long-horizon data |
| RAG (retrieval) | Possible for a local cache | **Preferred** | Needs a large, centrally-maintained knowledge base |
| LLM reasoning | Possible with a smaller model | **Preferred** for the full capability | Compute-intensive, benefits from centralized model updates |
| Model training | Not suited | **Preferred** | Needs aggregated data and significant compute |
| Fleet analytics | Not suited | **Preferred** | Inherently cross-elevator |

**No claim is made that every function must be edge-based or every function must be cloud-based** — this table's own pattern (a genuine mix, not a one-sided answer) is the point.

## 10.17 Event-Driven Architecture and Data Storage

**Event-driven architecture**, conceptually: `Fault event → event bus → correlation → analytics → RCA case`, with **event producers** (sensors, controllers, the anomaly-detection layer) publishing events, **event consumers** (the correlation engine, the RCA orchestrator, logging) subscribing to relevant events, and **event routing** enabling asynchronous processing — components don't block waiting on each other, which matters directly for the resilience goals of §10.6 and §10.24.

Storage options, compared conceptually: **time-series databases** (optimized for high-volume, timestamped sensor data — Ch.6's telemetry); **relational databases** (structured records with well-defined relationships — maintenance records, asset registries); **document stores** (flexible, semi-structured content — technician notes, raw ingested documents before chunking); **object storage** (large binary content — raw sensor logs, model artifacts); **vector databases** (embedding-based similarity search — Ch.9 §9.17's RAG retrieval layer); and **graph databases** (relationship-heavy data — Ch.9 §9.10's knowledge graph). **No single storage technology suits every layer of §10.15's architecture** — each is chosen for the specific access pattern its layer actually needs.

## 10.18 The Common Data Model

A conceptual entity model, tying together every data concept this book has introduced:

```
Asset — Elevator — Component — Sensor — Signal — Event — Alarm
   — Incident — Fault — Failure Mode — Hypothesis — Evidence
   — Maintenance Record — Technician — Document — Model — RCA Case
```

Relationships, briefly: an **Elevator** is a specific **Asset**, composed of **Components**, each monitored by one or more **Sensors** producing **Signals**; abnormal signal behavior produces **Events**, some of which become **Alarms**; a cluster of related alarms forms an **Incident**; investigating an incident generates **Hypotheses** about the underlying **Fault** and its **Failure Mode**, each weighed against **Evidence**; the whole investigation is an **RCA Case**, informed by **Maintenance Records**, retrieved **Documents**, and reviewed by a **Technician**, with every AI-generated judgment traceable to the specific **Model** (and version, §10.37) that produced it. **This is, in effect, Chapter 7 §7.38's investigation-state data model, formalized as a persistent, relational schema rather than a single in-flight investigation's working memory.**

## 10.19 Data Lineage

**"Where did this diagnostic conclusion come from?"** — a question this project's entire explainability design (Ch.9 Part VI) exists to answer, now traced as a concrete data chain:

```
RCA conclusion → Hypothesis → Evidence → Telemetry → Sensor → Timestamp → Asset
```

```
Documentation claim → Document version → Retrieved chunk → Specific claim used
```

**Why lineage is essential for auditability:** every "trace" concept established throughout this book (Ch.4 §4.21, Ch.7 §7.38, Ch.9 §9.18/§9.23/§9.28) is only genuinely auditable if the underlying data architecture actually preserves this chain end-to-end — an explainability design that stops at "the evidence was X" without being able to trace X back to a specific sensor reading at a specific timestamp is explainability in name only.

## 10.20 Data Governance and Privacy

**Governance dimensions:** ownership (which team/system is accountable for a given data category), retention (how long data is kept, and why), versioning (§10.37), access (who/what can read or write it), quality (Ch.6 §8.43's chain), lineage (§10.19), deletion, privacy, and regulatory requirements — none of which this book claims to have fully specified for a real KONE deployment; they are named as the governance dimensions a real implementation would need to address.

**Maintenance data privacy**, discussed at the principle level: technician information, customer/building information, maintenance records, and operational data all warrant standard data-protection principles — **minimization** (collect only what's needed for the stated diagnostic purpose), **access control** (restrict to those with a genuine need), **anonymization where appropriate** (particularly for any data used in broader model training or research contexts), and defined **retention** limits. **This book does not invent KONE-specific privacy policies** — these are general data-protection principles, offered as a checklist a real deployment would need to satisfy against KONE's actual policies and applicable regulation, not a substitute for either.

---

# Part IV — AI and Model Governance

## 10.21 Model Governance and Drift

```
TRAIN → VALIDATE → APPROVE → DEPLOY → MONITOR → RETRAIN → RETIRE
```

Versioning and rollback capability at every stage (§10.37) are what make this lifecycle auditable rather than ad hoc — a model update should be a tracked, reversible event, not a silent replacement.

**Model drift** — the data distribution a deployed model encounters diverging over time from what it was trained/validated on — can arise from new elevator models entering the fleet, changed sensors, new controller software, environmental changes, a growing/changing building portfolio, or evolving maintenance practices. **Monitoring for drift** (§10.23) is what makes Chapter 9 §9.32's out-of-distribution detection an operational reality rather than a theoretical design goal — a model that silently drifts out of its valid operating range, undetected, is functionally indistinguishable from a model that was never validated for its current conditions at all.

## 10.22 AI Security, RAG Security, and Agent Permissions

Building directly on Chapter 9 §9.35–§9.37, now at the deployment-architecture level: **model theft**, **adversarial inputs** (deliberately crafted evidence designed to mislead the model), **data poisoning** (corrupting training or fine-tuning data), model drift (§10.21), **prompt injection** and **RAG poisoning** (Ch.9 §9.36), **unauthorized tool use**, and **excessive agent permissions** are all real, named categories of AI-specific risk that a conventional (non-AI) industrial cybersecurity posture doesn't natively cover.

**RAG security, restated as an architectural requirement rather than a caution:** retrieved content is **untrusted data**, always — malicious documents, stale documents, conflicting revisions, poisoned embeddings, and incorrect metadata are all real failure categories (Ch.9 §9.19), addressed through source validation, document provenance (§10.19), version control (§10.37), access control, content validation, and trusted-source ranking within the retrieval pipeline itself.

**LLM tool security, via least privilege:** a diagnostic agent should be able to query telemetry, query alarm history, and retrieve documentation — and should **not** automatically receive any broader capability, including anything resembling operational control, merely because it's technically feasible to grant.

| Tool | Permission | Risk | Control |
|---|---|---|---|
| Telemetry query | Read-only | Low | Scoped to relevant asset/time window |
| Alarm/event query | Read-only | Low | Same |
| Maintenance-history query | Read-only | Low–moderate (contains records about people, §10.20) | Access control, minimization |
| Documentation/RAG retrieval | Read-only | Moderate (Ch.9 §9.19/§9.36) | Source validation, provenance |
| Fault-tree/FMEA lookup | Read-only | Low | — |
| Signal-analysis tool | Compute-only, read input/return result | Low | Deterministic, auditable computation |
| Knowledge-graph query | Read-only | Low | — |
| **Anything resembling control** | — | **Unacceptable** | **Never granted, under any circumstance** |

**Agent permissions**, formalized: **agent identity** (each agent/process has its own identifiable credential, not a shared one), **agent authorization** (scoped per §10.22's tool table), **tool scopes** (the specific, limited set of actions a given tool permits), **rate limits** (bounding how much any single agent can do in a given window, limiting the blast radius of a misbehaving or compromised agent), **audit logs** (§10.23), and **human approval** (Part I, throughout) — together making **"the LLM has access to everything"** an explicitly, architecturally unacceptable design, not merely an unwise default.

## 10.23 Audit Logging and Observability

**An audit trail**, recorded for every meaningful action: user, system, agent, tool, timestamp, input, retrieved evidence, output, decision, approval, and override — supporting accountability in the most literal sense: **any conclusion the system ever produced should be reconstructible from the log**, independent of whether the system itself is still running the same way it was at the time.

**Observability**, across infrastructure, data, models, agents, retrieval, latency, and errors, with representative metrics: availability, latency, retrieval failure rate, model confidence distribution, abstention rate (a metric this project should actively want to see nonzero, per Ch.9 §9.31 — a system that never abstains is more likely under-calibrated than perfectly confident), tool error rate, and data-quality indicators (Ch.6 §8.43).

## 10.24 Reliability Engineering and Resilience

*[ENGINEERING INFERENCE, standard reliability-engineering vocabulary]* **Availability** is the fraction of time a system is operational; **reliability** is the probability of correct operation over a defined period; **maintainability** is how readily a system can be restored after failure; **fault tolerance** is continued correct operation despite a component failure. **MTBF** (Mean Time Between Failures) and **MTTR** (Mean Time To Repair) are the standard quantitative measures underlying availability calculations — **this book does not invent specific target values for any of these** for KONE Elevate, since real targets require real operational data this project does not have.

**Resilience**, applied to network outage, cloud outage, AI-service outage, database outage, and telemetry outage alike: each should trigger §10.6's graceful-degradation behavior, never a hard failure that propagates beyond the diagnostic layer itself.

**Disaster recovery**, at the conceptual level: backups, redundancy, defined failover behavior, and data-recovery procedures, organized around two standard targets — **RTO** (Recovery Time Objective — how quickly service must be restored) and **RPO** (Recovery Point Objective — how much data loss, measured in time, is acceptable) — **no specific target values are invented here**; both remain business/engineering decisions a real deployment would need to set deliberately, informed by the actual consequence of an outage (which, per Part I, is delayed diagnosis, never a safety consequence).

---

# Part V — Deployment

## 10.25 Deployment Architecture

```
                ELEVATOR
                    │
              Controller
                    │
              Edge Gateway
                    │
          ┌─────────┴─────────┐
          │                   │
    Local Analytics       Secure Network
                              │
                           Cloud
                              │
       ┌──────────────────────┼──────────────────────┐
       ↓                      ↓                      ↓
 Telemetry Store         Knowledge/RAG          AI Services
       │                      │                      │
       └──────────────────────┼──────────────────────┘
                              ↓
                       RCA Orchestrator
                              ↓
                     Technician Interface
                              ↓
                        Human Review
                              ↓
                    Maintenance System
```

**Every connection in this diagram is a §10.9 boundary** — the Edge Gateway↔Secure Network connection is the primary observational conduit from the elevator side; the Cloud's three parallel stores feed the RCA Orchestrator (Ch.9's multi-agent architecture, concretely deployed); the Orchestrator's output reaches a human exclusively through the Technician Interface, never bypassing it; and the Maintenance System at the bottom is the pre-existing process (Ch.5 §5.12) this entire pipeline feeds into, not replaces.

## 10.26 APIs and Interoperability

Potential interfaces: telemetry, alarm/event, maintenance history, documentation, RCA, and the technician application itself — each requiring authentication, authorization, versioning, rate limiting, input validation, and monitoring, consistent with §10.12 and §10.22's controls applied at the API layer specifically.

**Interoperability**, given the real diversity of elevator models, controllers, sensors, and software systems any real fleet contains (Ch.5 §5.15's CMMS/EAM discussion, Ch.6 §8.31's per-installation state-machine caveat): common schemas (§10.18), adapters (translating a specific controller's native format into the common model), canonical identifiers (so "this asset" means the same thing across every system that references it), and consistent metadata are what make a diagnostic layer built for "an elevator" actually usable across a real, heterogeneous fleet rather than one specific installation.

## 10.27 The Digital Thread and Closed-Loop Learning

**Digital thread:** `Physical asset → data → event → diagnosis → maintenance → outcome` — a continuous, traceable connection across an asset's entire operational lifecycle, giving §10.19's lineage concept its full temporal scope, not just within one investigation but across an asset's history.

**Closed-loop learning**, reprising Chapter 5 §5.17 with the full data architecture now in view: `Detection → RCA → Maintenance → Technician verification → Actual cause → Repair → Outcome → Historical record → Future diagnosis`. **Verified maintenance outcomes are valuable training/evaluation evidence** precisely because they're the one category of data in this whole architecture with an independently-confirmed ground truth (a technician's physical confirmation) — everything else in the pipeline is evidence *toward* a conclusion; a verified outcome is evidence *of* whether a past conclusion was actually right.

---

# Part VI — Where Safety Meets Cybersecurity Meets Risk

## 10.28 The Safety and Cybersecurity Intersection

The risk chain this entire chapter has been building toward, stated explicitly:

```
Cybersecurity failure → Data integrity failure → Diagnostic failure
        → Potential (indirect) safety consequence
```

**Read carefully — this is an indirect chain, not a claim that the AI layer itself sits in the safety loop.** A compromised sensor feed or a poisoned knowledge base can produce a wrong diagnosis (§10.14, §10.22); a wrong diagnosis can lead to a wrong maintenance action; a sufficiently wrong maintenance action, left uncorrected by human verification, *could* eventually have safety relevance — but only by passing through every one of Part I's independent safeguards (human review, the safety chain's own independence, ASME A17.2's formal inspection/testing process) first. **This is precisely why Part I's architectural separation matters as much as Part II's technical security controls do** — cybersecurity protects data integrity; the safety-architecture separation (§10.2) is the independent backstop that keeps even a successful attack on the diagnostic layer from ever reaching the physical system directly.

## 10.29 Threat + Failure Mode Combinations

| Technical Failure / Cyber Threat | Diagnostic Consequence | Safety Implication | Mitigation |
|---|---|---|---|
| Sensor failure (accidental) | Missing/corrupted evidence | None directly — the diagnostic layer has no control path | Ch.6 §8.5 quality checks; independent cross-checks (Ch.7 §7.34) |
| Sensor spoofing (deliberate) | Confidently wrong evidence | None directly, per the same architectural boundary | Data integrity controls (§10.14), anomaly detection on the telemetry pipeline itself |
| Network loss | Missing evidence, degraded confidence | None — safety systems are independent of this connection entirely | Graceful degradation (§10.6) |
| Corrupted telemetry | Wrong evidence, potential wrong diagnosis | None directly | Validation at ingestion (§10.15) |
| Stale model | Degraded or miscalibrated confidence | None directly | Drift monitoring (§10.21), versioning (§10.37) |
| Malicious document (RAG) | Misleading retrieved "evidence" or a manipulated model response (Ch.9 §9.36) | None directly, contained by the safety boundary | Source validation, treating retrieved content strictly as data (§10.22) |
| Compromised gateway | Potential broader data-integrity compromise | None directly, if network segmentation (§10.13) holds | Zone/conduit isolation, monitoring |

**Every "safety implication" cell in this table reads "none directly"** — that is the entire point of Part I's architectural boundary, demonstrated concretely rather than merely asserted. A real deployment's job is to keep that boundary intact under every one of these conditions, not to make the diagnostic layer itself failure-proof (an unachievable goal for any software system).

## 10.30 Safety Case and Assurance Case Thinking

**A safety case**, at a high level: `CLAIM → ARGUMENT → EVIDENCE` — a structured demonstration that a specific safety claim is justified by a specific line of reasoning, backed by specific evidence. **This project does not have, and does not claim to have, a formal safety case** — building one would require the full IEC 61508/PESSRAL lifecycle (§10.4), performed by qualified safety engineers, which is genuinely outside this research book's scope. What this section borrows is the **mindset**: stating claims precisely, backing them with an explicit argument, and grounding the argument in real evidence — improving this project's own engineering rigor even without a formal certification process attached.

**An assurance case for the AI layer specifically**, applying the same structure to a claim this project *can* meaningfully make: **Claim** — the AI diagnostic output is trustworthy enough for its defined, non-safety-critical use. **Argument** — the system uses verified evidence (Ch.6), operates within bounded functions (Part I), includes validation and contradiction-checking (Ch.7 §7.25, Ch.9 §9.39), and requires human oversight before any action (throughout). **Evidence** — tests, logs, benchmark results (deferred to a later phase), and source provenance (§10.19). **Confidence alone is not assurance** — a system can report high confidence and still be wrong (Ch.9 §9.29); assurance requires the independent argument-and-evidence structure above, not a self-reported number.

## 10.31 Risk Register

| Risk | Cause | Consequence | Severity | Likelihood | Detection | Mitigation | Residual Risk |
|---|---|---|---|---|---|---|---|
| Hallucination | LLM generates unsupported claims | Wrong diagnosis presented confidently | High | Moderate (without mitigation) | Structured-output/citation checks (Ch.9 §9.35) | Tool-based access, RAG, structured outputs, human review | Low, with mitigations applied |
| False diagnosis | Any upstream evidence or reasoning error | Wasted technician time, possible missed true cause | Moderate | Moderate | Evidence verification, contradiction checks | Alternative-cause elimination (Ch.7 §7.25), confidence/abstention | Low–moderate |
| Missing telemetry | Sensor/network/ingestion failure | Reduced evidence, lower confidence | Low–moderate | Moderate | Data-quality checks (Ch.6 §8.5) | Explicit missing-data handling, never silent imputation | Low |
| Sensor failure | Hardware degradation | Corrupted evidence | Moderate | Low–moderate | Independent cross-checking | Ch.7 §7.34's independent-signal pattern | Low |
| Cyber compromise (any point) | §10.10's threat actors | Data-integrity or availability loss | Potentially high, contained by architecture | Low (with controls) | §10.23 observability | §10.11–§10.13's controls | Low, given the safety boundary's independence |
| RAG poisoning | Corrupted knowledge base | Persistent, hard-to-detect diagnostic bias | Moderate–high | Low (with controls) | Source vetting, provenance auditing | §10.22 | Low–moderate |
| Cloud outage | Infrastructure failure | Diagnostic capability unavailable | Low (non-safety) | Low–moderate | Availability monitoring | Graceful degradation (§10.6) | Low |
| Model drift | Changing real-world conditions | Silently declining accuracy | Moderate | Moderate over time | Drift monitoring (§10.21) | Scheduled retraining/revalidation | Low–moderate |
| Incorrect maintenance history | Data-entry error, unrelated system issue | Wrong prior probability (Ch.5 §5.16) | Low–moderate | Moderate | Data-quality review | Cross-checking against other evidence | Low–moderate |
| Agent failure/disagreement | Ch.9 §9.24's multi-agent failure modes | Ambiguous or contradictory output | Low–moderate | Moderate | Explicit disagreement surfacing | Independent evidence-verification stage | Low |
| Human overtrust | Technician defers to AI without genuine review | A wrong conclusion proceeds unchecked | Potentially high | Genuine, human-factors risk — not eliminated by architecture alone | Difficult to detect directly | Training, UI design encouraging genuine review, not rubber-stamping | **Moderate — the least architecturally-solvable risk in this table** |
| Unauthorized action | A permissions/scope failure | Action taken beyond intended AI authority | Would be high if it occurred | Very low, given Part I's hard boundaries | Audit logging (§10.23) | Least-privilege tool scoping (§10.22), no control-capability ever granted | Very low |

**Severity/likelihood ratings above are qualitative engineering judgment, not derived from a formal quantitative risk assessment** — consistent with this book's consistent practice, no arbitrary numerical scores are assigned without a stated basis (Ch.7 §7.8's FMEA scoring discipline, applied here to risk more generally).

## 10.32 Hazard Analysis and FMEA for the AI Platform

**Hazard vs. failure mode vs. risk vs. threat, distinguished:** a **hazard** is a potential source of harm; a **failure mode** is how a system fails to perform its function; **risk** is the combination of a hazard's severity and likelihood; a **threat** is a potential cause of a security-relevant failure specifically (a subset of the broader failure-mode concept, viewed through an adversarial lens). Applied to this project: the diagnostic system has essentially no direct hazards (Part I's boundary), real failure modes (§10.31), calculable risk for each, and real cybersecurity threats (§10.10) as one *source* of some of those failure modes.

**FMEA thinking, applied to the AI platform's own pipeline** (Chapter 7 §7.8's methodology, retargeted from elevator components to this project's own software pipeline):

| Pipeline Stage | Failure Mode | Cause | Effect | Detection | Mitigation |
|---|---|---|---|---|---|
| Telemetry ingestion | Corrupted/missing data accepted silently | Upstream sensor/network fault, no validation | Bad evidence propagates | Ingestion-time validation | Explicit quality checks (§10.14) |
| Anomaly detection | False positive/negative | Threshold miscalibration, context blindness (Ch.6 §8.24) | Wrong or missed investigation trigger | Ongoing performance monitoring | State-aware baselines (Ch.6 §8.31) |
| Alarm correlation | Unrelated events incorrectly merged | Time-proximity-only correlation | Wrong incident framing | Physical-plausibility check (Ch.6 §8.20) | Causal-graph-grounded correlation |
| Retrieval | Wrong/stale document surfaced | Retrieval-quality issue (Ch.9 §9.19) | Misleading grounding | Source-grounding audit | Hybrid retrieval + reranking |
| RCA | Overconfident or wrong ranking | Correlated-evidence double-counting (Ch.7 §7.16) | Wrong recommended focus | Contradiction search (Ch.7 §7.25) | Correlation-aware Bayesian updating |
| Confidence | Miscalibrated score | Insufficient calibration data | Technician over/under-trusts the output | Calibration monitoring (deferred to a later phase) | Conservative default, explicit abstention |
| Technician output | Ambiguous or overwhelming presentation | Poor synthesis (Ch.9 §9.39) | Reduced trust, wasted review time | User feedback | Dual-audience, structured explanation design (Ch.4 §4.21) |
| Audit logging | Incomplete trace | Implementation gap | Reduced auditability | Completeness checks (§10.23) | Log-schema validation |

## 10.33 Bow-Tie Analysis

Applying Chapter 7 §7.12's method to a specific, major risk — **an incorrect AI diagnostic recommendation:**

```
THREATS                    PREVENTIVE BARRIERS
  Bad sensor data      →   Data-quality checks (Ch.6 §8.5)
  Correlated evidence  →   Correlation-aware Bayesian updating (Ch.7 §7.16)
  RAG poisoning        →   Source validation (§10.22)
  Model drift          →   Drift monitoring (§10.21)
        ↓
   TOP EVENT: Incorrect AI diagnostic recommendation generated
        ↓
MITIGATING BARRIERS                    CONSEQUENCES
  Confidence/abstention (Ch.9 §9.31)   Wasted technician time (if unmitigated)
  Human review (Part I, throughout)    Delayed correct diagnosis
  Physical verification requirement    (No safety consequence — Part I's
  (Ch.7 §7.31, every worked example)    architectural boundary holds regardless)
```

**Why multiple independent barriers matter:** no single barrier above is claimed to be perfect — the whole point of a bow-tie structure, and of defense in depth generally (§10.34), is that the *combination* of several imperfect, independent barriers is what makes the overall consequence acceptable, not any one barrier alone.

## 10.34 Defense in Depth and Privilege Boundaries

```
Physical → Device → Network → Identity → Application → Data → AI → Human
```

**Why no single security control should be relied upon:** each layer above addresses a different category of failure, and a compromise at one layer should still be contained by the layers around it — a philosophy that runs through this entire chapter, from IEC 62443's zones/conduits (§10.11) to §10.33's bow-tie barriers to Part I's safety-architecture separation itself, which is, in effect, the deepest and most important layer of defense in this whole system.

**A layered permission model**, formalizing §10.22's tool-permission table into a general principle:

```
Read-only telemetry
     ↓
Read-only diagnostics
     ↓
RCA generation
     ↓
Maintenance recommendation
     ↓
Human approval
     ↓
Restricted operational controls (not granted to this system at all)
```

**This project's RCA system should remain within its defined diagnostic scope** — every permission boundary in this book, restated one final time, exists to keep that statement true by construction, not by policy alone.

---

# Part VII — From Prototype to Production

## 10.35 Production Readiness: A Maturity Ladder

```
LEVEL 0   Concept
LEVEL 1   Offline research prototype           ← this project's current stage
LEVEL 2   Historical-data evaluation
LEVEL 3   Shadow mode
LEVEL 4   Human-reviewed operational pilot
LEVEL 5   Production diagnostic support
```

**What evidence is required to progress between levels, briefly:** Level 1→2 requires access to real (or credibly representative) historical data to evaluate against, beyond the synthetic scenarios this project currently uses. Level 2→3 requires demonstrated accuracy on that historical evaluation sufficient to justify running alongside real operations without influencing them. Level 3→4 requires shadow-mode performance data (§10.36) strong enough to justify human-reviewed operational use. Level 4→5 requires sustained pilot performance, validated safety-boundary integrity, and organizational readiness (training, support processes) beyond the technology itself. **This book does not claim the hackathon prototype is production-ready, and states this explicitly rather than leaving it ambiguous: this project sits at Level 1.**

## 10.36 Validation Environments and Synthetic Data Safety

**How the system can be tested without direct access to proprietary production systems:** historical records (where available), synthetic telemetry, simulated faults, digital-twin environments (Ch.9 §9.9), public research datasets (Ch.9 Part II's academic literature, where applicable), controlled test benches, and expert-generated scenarios — each with real limitations (public datasets rarely match this specific problem exactly; expert-generated scenarios reflect expert assumptions, not necessarily field reality; simulated faults reflect the fidelity of the simulation, not guaranteed real-world behavior).

**Synthetic data is useful but dangerous, and both halves of that sentence matter equally:** unrealistic correlations (a simulation may make two signals move together too cleanly compared to noisy reality), overly clean data (missing the real-world messiness Chapter 6's entire signal-quality discussion addresses), incorrect fault signatures (if the underlying physics model is subtly wrong), and general distribution mismatch versus real production conditions are all real risks. **Synthetic data is useful for testing that the reasoning process behaves as designed. It is never, by itself, evidence that the system is representative of production performance** — the single most repeated caution in this entire research book, restated here at the validation-architecture level specifically.

**Data isolation**, briefly: development, testing, staging, and production environments should remain genuinely separate — real production data, if it ever becomes available to this project, should not simply be copied into every environment indiscriminately, both for privacy/governance reasons (§10.20) and because a test environment contaminated with production data stops being a reliable test of how the system behaves on genuinely unseen input.

## 10.37 Version Control and Reproducibility

Versioning applies to models, prompts, agent definitions, RAG documents, schemas, rules, fault trees, FMEA tables, and APIs alike — **a diagnosis must be reproducible with the specific version of the system that generated it**, which is both good engineering practice generally and a direct requirement of §10.19's audit-lineage principle.

**Reproducibility, as a concrete test:** can this project reconstruct, six months from now, exactly why the system reached a specific diagnosis? The required artifacts: the input data, timestamps, model version, knowledge-base version, the specific retrieved sources, tool outputs, configuration, and the final result — every one of them a field already present in §10.18's data model and §10.23's audit log, now understood as jointly serving this reproducibility requirement, not as separate, unrelated concerns.

## 10.38 The System Boundary

```
┌─────────────────────────────────────┐
│        ELEVATOR SAFETY SYSTEM        │
│                                       │
│  Independent safety functions        │
└──────────────────┬────────────────────┘
                    │
                    │ Observational data only
                    ↓
┌─────────────────────────────────────┐
│       DIAGNOSTIC INTELLIGENCE        │
│                                       │
│  Signals · Alarms · RCA · AI         │
│  RAG · Explainability                │
└──────────────────┬────────────────────┘
                    ↓
             HUMAN REVIEW
                    ↓
       APPROVED MAINTENANCE PROCESS
```

**This diagram is, in a real sense, the single most important artifact in this entire chapter — and in this entire research book.** Every standard summarized in Parts I–II, every risk analyzed in Part VI, and every maturity requirement in this Part exists to keep this specific boundary — one arrow, flowing one direction, carrying observational data only — true in practice, not just on paper.

## 10.39 What the System Must Never Assume

- AI output is always correct.
- Missing data means normal operation.
- Correlation means causation.
- Fault code equals root cause.
- High confidence equals certainty.
- Cloud availability is guaranteed.
- Sensor readings are always trustworthy.
- Retrieved documents are automatically correct.
- More agents guarantee better diagnosis.
- Production architecture can be inferred from marketing material.
- A prototype is automatically safety-certified.

**Every item on this list is a specific error this research book has explicitly guarded against somewhere in its preceding nine chapters** — this list is, in effect, an index of this whole book's hard-won cautions, compiled once, in one place, for exactly the moment a team member needs a fast pre-demo sanity check.

## 10.40 What KONE Elevate Should — and Should Not — Claim

**A defensible positioning**, tested against this entire book's research rather than accepted as marketing copy:

> *"An evidence-driven diagnostic intelligence layer that assists technicians by correlating elevator telemetry, alarms, engineering knowledge, and maintenance evidence to isolate probable root causes and provide auditable recommendations."*

**Why this is safer and more defensible than claiming "fully autonomous elevator control":** every word in it is a claim this book's research actually supports — "assists" (Part I's human-in-the-loop boundary), "correlating... evidence" (Ch.4, Ch.6), "auditable" (§10.19, Ch.9 Part VI) — none of it implies authority this project doesn't have or hasn't earned. **No claim is made here of actual KONE production integration** — that remains a real, separate, future undertaking, contingent on KONE SME review and real data access neither this book nor this project currently has.

**What KONE Elevate should not claim, stated as a firm list:** safety certification, autonomous safety decisions, autonomous rescue, autonomous elevator control, guaranteed root-cause accuracy, universal diagnosis across every elevator model, access to proprietary KONE data unless actually granted, production deployment, or real-time KONE integration unless actually demonstrated. **Every item on this second list, if claimed prematurely, would directly contradict evidence already established elsewhere in this book** — this list is not a new caution so much as the logical consequence of everything Parts I through VI already established.

## 10.41 Architecture Trade-offs and the Minimum Viable Architecture

| Architecture | Advantages | Disadvantages | Best Use |
|---|---|---|---|
| Cloud-only | Simplest to build and manage; centralized updates | No resilience to connectivity loss; higher latency for time-sensitive checks | Early-stage prototypes, fleet-wide analytics |
| Edge-only | Low latency, resilient offline | Limited compute for heavier models; harder to manage updates across many sites | Latency-critical signal preprocessing |
| Hybrid | Combines both strengths (§10.16's table) | More components, more integration complexity | A real production deployment at any meaningful scale |

**"More intelligence" is not the same as "better system."** More components mean more latency, more cost, more maintenance burden, a larger attack surface (§10.10), and more distinct failure modes (Ch.9 §9.24 for agents specifically; §10.31 more broadly) — a genuinely useful architectural discipline, not a reason to avoid sophistication where it's earned.

**A minimum viable architecture**, sized for demonstrating this project's core value without building an enterprise-scale platform for a hackathon:

```
Telemetry/Event Input → Evidence Extraction → Alarm Correlation
   → Engineering Knowledge Retrieval → RCA Engine → LLM Explanation
   → Confidence → Human Review
```

**Why this may be preferable to an enormous platform at this stage:** every layer in Parts I–VI of this chapter is a real, eventually-necessary concern for a production system — but a hackathon-stage demonstration's job is to prove the *reasoning* (Chapters 2, 4, 6, 7, 9) is sound and evidence-grounded, not to have pre-built the full industrial deployment stack this chapter describes. **A believable, well-reasoned MVP that's honest about what it doesn't yet include is a stronger demonstration than an over-built architecture whose extra pieces can't be defended under questioning.**

**Toward future production architecture**, briefly: `MVP → Pilot → Fleet-scale → Production`, with §10.35's maturity ladder governing what becomes necessary at each stage — data governance (§10.20) and full observability (§10.23) become essential at Pilot; fleet-wide model management (§10.21) and full edge/cloud optimization (§10.16) become essential at Fleet-scale; formal safety-case discipline (§10.30) and complete regulatory alignment (Parts I–II) become essential before any claim of Production readiness specifically.

---

# Part VIII — Worked Scenarios

## 10.42 Scenario 1: Motor Overcurrent Under Failure Conditions

The nominal path, reusing Chapter 9 §9.40's worked example: (1) telemetry received, (2) data validated, (3) alarms correlated, (4) anomaly identified, (5) engineering knowledge retrieved, (6) hypotheses generated, (7) evidence evaluated, (8) RCA produced, (9) confidence calculated, (10) evidence explained, (11) recommendation sent to the technician.

**Now introduce failures, one at a time, and trace the architectural response:**

- **Telemetry disappears mid-investigation.** §10.6's degradation applies: confidence drops, the missing signal is flagged explicitly (never silently treated as "normal," §10.39), and if the remaining evidence is insufficient, the system abstains (Ch.9 §9.31) rather than completing the ranking on a partial picture.
- **Cloud becomes unavailable.** Per §10.16's edge/cloud split, any edge-resident signal processing continues; cloud-dependent stages (RAG, full LLM reasoning) pause; the elevator's own safety and control systems are entirely unaffected (§10.6), and the existing, pre-AI maintenance process remains available.
- **A retrieved document conflicts with another.** Handled fully in §10.44 below, as its own dedicated scenario.
- **A sensor appears corrupted.** Cross-checked against an independent signal where one exists (Ch.7 §7.34); if no independent check is available, confidence in evidence drawing on that sensor is explicitly reduced, not silently trusted.
- **AI confidence falls below a usable threshold.** The system abstains and routes to human review with whatever partial evidence trail exists — a legitimate, designed outcome (Ch.9 §9.31), not a system failure.

**Throughout every one of these failures, the elevator's independent safety system remains entirely untouched** — the scenario exists specifically to demonstrate, concretely, that §10.38's boundary diagram holds under realistic operational stress, not just in the nominal case.

## 10.43 Scenario 2: A Cybersecurity / Data-Integrity Incident

Diagnostic data integrity becomes questionable — for example, telemetry readings that fail §10.14's plausibility checks in a pattern more consistent with tampering than ordinary sensor drift.

```
Detection           (§10.14's integrity checks, §10.23's monitoring, flag the
                      anomalous pattern)
        ↓
Quarantine/flagging  (the affected data is marked untrusted, not silently used)
        ↓
Confidence reduction (any conclusion drawing on the flagged data has its
                      confidence explicitly lowered — Ch.9 §9.29)
        ↓
Abstention           (if the flagged data was load-bearing for the leading
                      hypothesis, the system abstains rather than proceed on
                      compromised evidence — Ch.9 §9.31)
        ↓
Human escalation     (routed for review, with the integrity concern itself
                      explicitly surfaced, not hidden inside a generic
                      "low confidence" label)
```

**This book provides no offensive attack instructions anywhere in this scenario or elsewhere** — the walkthrough is entirely the defensive response, which is the only part of this topic with legitimate diagnostic or engineering value.

## 10.44 Scenario 3: A RAG Document Conflict

Two versions of a maintenance document contain different information about the same procedure or fault code.

```
Version detection    (document metadata, §10.15's document store, flags that
                      two retrieved sources have different version/revision
                      identifiers)
        ↓
Provenance check     (§10.19 — which source is more current, and is either
                      one confirmed authoritative for this specific elevator
                      model?)
        ↓
Conflict identified  (surfaced explicitly in the evidence trace, Ch.9 §9.23/
                      §9.28 — not silently resolved by picking one arbitrarily)
        ↓
No blind generation  (the LLM does not attempt to reconcile or average the
                      conflicting content into a plausible-sounding synthesis
                      — Ch.9 §9.35's core hallucination-mitigation principle,
                      applied to exactly this situation)
        ↓
Escalation           (a human resolves which source applies, informed by the
                      explicit conflict rather than an invisible one)
```

---

# Judge Questions

*Organized by the roadmap's own categories.*

### Safety

**1. Is your AI safety-certified?** *Short:* No, and this is explicitly not claimed anywhere in this project (§10.40). *Detailed:* Certification requires a formal IEC 61508/PESSRAL lifecycle this research book has not performed. *Evidence:* — *Assumptions:* — *Tested:* Honesty under direct questioning. *Avoid:* Any hedge implying partial certification.

**2. Is your AI part of the elevator safety loop?** *Short:* No — architecturally excluded by design (§10.2, §10.38). *Detailed:* The system boundary diagram shows one-directional, observational-only data flow. *Evidence:* — *Assumptions:* — *Tested:* Firmness. *Avoid:* Any hedge.

**3. What happens if your AI fails?** *Short:* It degrades gracefully; the elevator's safety and control systems are entirely unaffected (§10.6, §10.42). *Detailed:* — *Evidence:* — *Assumptions:* — *Tested:* Whether "fails" is answered concretely, not deflected. *Avoid:* Vagueness.

**4. What happens if the cloud goes down?** *Short:* Diagnostic capability degrades or pauses; elevator operation is unaffected (§10.16, §10.42). *Detailed:* — *Evidence:* — *Assumptions:* — *Tested:* Same pattern as Q3, specific to cloud. *Avoid:* Implying any elevator-side impact.

**5. Can your AI control the elevator?** *Short:* No, never (§10.7, §10.34). *Detailed:* No tool, permission, or architectural path exists for this. *Evidence:* — *Assumptions:* — *Tested:* Maximal firmness — this is the single most important "no" in the whole book. *Avoid:* Any hedge whatsoever.

**6. Can it override the safety chain?** *Short:* Never (§10.7). *Detailed:* — *Evidence:* — *Assumptions:* — *Tested:* Same firmness. *Avoid:* Same.

**7. Why is your architecture safe?** *Short:* Because the diagnostic layer has no control path into safety-critical functions — independence by architecture, not by policy (§10.2, §10.38). *Detailed:* — *Evidence:* — *Assumptions:* — *Tested:* Whether "safe" is defended structurally, not just asserted. *Avoid:* A vague "we're careful."

**8. What standard are you following?** *Short:* None claimed as fully followed or certified against; several (EN 81, ISO 8100, IEC 61508, PESSRAL, ISO 8102-20) inform this chapter's architectural reasoning (§10.4, §10.11). *Detailed:* — *Evidence:* [OFFICIAL STANDARD / REGULATORY SOURCE] *Assumptions:* — *Tested:* Whether "informed by" and "certified against" are kept distinct. *Avoid:* Claiming compliance.

**9. What is SIL?** *Short:* Safety Integrity Level — IEC 61508's graduated (1–4) measure of a safety function's required risk reduction (§10.4). *Detailed:* — *Evidence:* [OFFICIAL STANDARD / REGULATORY SOURCE] *Assumptions:* No SIL claimed for this project. *Tested:* Definitional accuracy. *Avoid:* Inventing a SIL rating for this project.

**10. What is PESSRAL?** *Short:* Programmable Electronic Systems in Safety-Related Applications for Lifts — the standard governing when programmable electronics may participate in lift safety functions (§10.4). *Detailed:* Formalized as ISO 22201, building on IEC 61508. *Evidence:* [OFFICIAL STANDARD / REGULATORY SOURCE] *Assumptions:* — *Tested:* Whether the team understands why this project deliberately stays outside its scope. *Avoid:* Implying this project meets PESSRAL's bar.

**11. Why isn't accuracy enough for safety?** *Short:* Accuracy is a statistical measure; functional safety is a certified, worst-case-analyzed property (§10.5). *Detailed:* — *Evidence:* — *Assumptions:* — *Tested:* Whether this distinction is genuinely internalized, not just repeated. *Avoid:* Conflating the two.

**12. How do you validate safety boundaries?** *Short:* By architectural review (§10.38's diagram) and the explicit absence of any control-capable tool or permission (§10.22, §10.34) — not by testing the AI's accuracy. *Detailed:* — *Evidence:* — *Assumptions:* — *Tested:* Whether "validate the boundary" and "validate the model" are kept separate. *Avoid:* Answering with an accuracy metric.

### Cybersecurity

**13. What is your attack surface?** *Short:* Sensors, gateways, network, APIs, cloud, technician apps, identity systems, updates, the RAG knowledge base, and AI model interfaces (§10.10). *Detailed:* — *Evidence:* — *Assumptions:* — *Tested:* Whether the AI-specific surface (RAG, model interfaces) is included, not just conventional OT/IT. *Avoid:* An incomplete list.

**14. Why is IEC 62443 relevant?** *Short:* It's the leading industrial-automation cybersecurity framework, and ISO 8102-20 (the lift-specific cybersecurity standard) is explicitly built on it (§10.11). *Detailed:* — *Evidence:* [OFFICIAL STANDARD / REGULATORY SOURCE] *Assumptions:* — *Tested:* Whether the ISO 8102-20 connection is known. *Avoid:* Treating IEC 62443 as generic, unconnected background.

**15. How do you secure the edge gateway?** *Short:* Secure boot, signed firmware, network segmentation (§10.12–§10.13). *Detailed:* — *Evidence:* — *Assumptions:* — *Tested:* Specificity. *Avoid:* A generic "we secure it."

**16. How do you authenticate devices?** *Short:* Device identity as part of a zero-trust model — continuous verification, not implicit trust (§10.11). *Detailed:* — *Evidence:* — *Assumptions:* — *Tested:* Whether zero trust is named specifically. *Avoid:* Vague reassurance.

**17. How do you secure APIs?** *Short:* Authentication, authorization, versioning, rate limiting, validation, monitoring (§10.26). *Detailed:* — *Evidence:* — *Assumptions:* — *Tested:* Whether a specific control list is ready. *Avoid:* "APIs are secured."

**18. What if telemetry is manipulated?** *Short:* Detected via integrity/plausibility checks, quarantined, confidence reduced, escalated (§10.43). *Detailed:* — *Evidence:* — *Assumptions:* — *Tested:* Whether the full detection-to-escalation chain is known. *Avoid:* "We'd catch it" without the mechanism.

**19. What if a RAG document is malicious?** *Short:* Treated as untrusted data; never followed as an instruction (§10.22, Ch.9 §9.36). *Detailed:* — *Evidence:* — *Assumptions:* — *Tested:* Whether the data-vs-instruction principle is stated precisely. *Avoid:* Vague reassurance.

**20. What if an agent calls an unauthorized tool?** *Short:* Prevented by least-privilege tool scoping — the tool/permission itself shouldn't exist for that agent (§10.22). *Detailed:* — *Evidence:* — *Assumptions:* — *Tested:* Whether prevention (design) is distinguished from detection (logging). *Avoid:* Only naming logging as the answer.

**21. How do you implement least privilege?** *Short:* Per-tool, per-agent permission scoping (§10.22's table); nothing resembling control granted to any agent. *Detailed:* — *Evidence:* — *Assumptions:* — *Tested:* Concreteness. *Avoid:* An abstract definition only.

**22. How do you detect compromise?** *Short:* Observability (§10.23) — anomalous access patterns, integrity-check failures, audit-log review. *Detailed:* — *Evidence:* — *Assumptions:* Detection is not guaranteed — a real, named limitation. *Tested:* Honesty about detection limits. *Avoid:* Overclaiming guaranteed detection.

**23. How do you secure OTA updates?** *Short:* Authentication, integrity verification, rollback capability, staged deployment (§10.12). *Detailed:* — *Evidence:* — *Assumptions:* — *Tested:* Specificity. *Avoid:* "Updates are secure."

**24. What happens during network failure?** *Short:* Graceful degradation per §10.6; elevator operation unaffected. *Detailed:* — *Evidence:* — *Assumptions:* — *Tested:* Consistency with the safety-question answers above. *Avoid:* A different answer than Q3/Q4's pattern.

### Data

**25. How do you handle missing data?** *Short:* Explicitly flagged, never treated as "normal" (§10.14, §10.39, Ch.7 §7.26). *Detailed:* — *Evidence:* — *Assumptions:* — *Tested:* Cross-chapter consistency. *Avoid:* Silent imputation.

**26. How do you synchronize timestamps?** *Short:* Clock synchronization and explicit alignment checks across distributed subsystems (§10.14, Ch.6 §8.4). *Detailed:* — *Evidence:* — *Assumptions:* — *Tested:* Whether the false-causal-ordering risk is named. *Avoid:* Assuming timestamps are automatically comparable.

**27. How do you guarantee data integrity?** *Short:* You don't "guarantee" it — you detect and mitigate integrity threats through validation, checks, and monitoring (§10.14, §10.22). *Detailed:* — *Evidence:* — *Assumptions:* — *Tested:* Whether "guarantee" is honestly softened to "detect and mitigate." *Avoid:* Overclaiming a guarantee.

**28. How do you maintain lineage?** *Short:* Every claim traceable to source, version, and timestamp (§10.19). *Detailed:* — *Evidence:* — *Assumptions:* — *Tested:* Whether the specific chain (claim→evidence→source→timestamp/version) is named. *Avoid:* A vague "we keep records."

**29. Where is historical data stored?** *Short:* Conceptually, in a time-series store (telemetry) and event store (alarms/events), per §10.15's layered architecture — no specific production technology is claimed. *Detailed:* — *Evidence:* — *Assumptions:* — *Tested:* Whether "conceptual, not a specific vendor commitment" is stated. *Avoid:* Naming a specific unverified production system.

**30. How do you handle multiple elevator models?** *Short:* Canonical identifiers, adapters, and common schemas (§10.18, §10.26); explicitly named as an open interoperability challenge, not fully solved (§9.7, §9.32). *Detailed:* — *Evidence:* — *Assumptions:* This book's own scope is a modern gearless traction elevator (Ch.1). *Tested:* Whether the scope limitation is volunteered. *Avoid:* Claiming universal model support.

**31. How do you version maintenance records?** *Short:* Per §10.37's versioning discipline, applied to maintenance records alongside models, prompts, and documents. *Detailed:* — *Evidence:* — *Assumptions:* — *Tested:* Whether versioning is understood as spanning data, not just models. *Avoid:* Limiting the answer to model versioning only.

**32. How do you protect customer data?** *Short:* Minimization, access control, anonymization where appropriate, defined retention (§10.20). *Detailed:* — *Evidence:* — *Assumptions:* No KONE-specific policy invented. *Tested:* Whether general principles are given, not fabricated specifics. *Avoid:* Inventing a KONE policy.

### Deployment

**33. Why edge?** *Short:* Latency, bandwidth, resilience to connectivity loss (§10.16). *Detailed:* — *Evidence:* — *Assumptions:* — *Tested:* Specific reasons, not "edge is good." *Avoid:* Vagueness.

**34. Why cloud?** *Short:* Large-scale storage, fleet-wide analytics, centralized model management (§10.16). *Detailed:* — *Evidence:* — *Assumptions:* — *Tested:* Same. *Avoid:* Same.

**35. Why hybrid?** *Short:* Different functions genuinely need different properties — no single deployment model suits every layer (§10.16's table, §10.41). *Detailed:* — *Evidence:* — *Assumptions:* — *Tested:* Whether hybrid is justified by task-fit, not assumed by default. *Avoid:* "Hybrid is always best" without the table.

**36. What happens if the cloud is unavailable?** *Short:* Same as Q4 — graceful degradation, elevator unaffected. *Detailed:* — *Evidence:* — *Assumptions:* — *Tested:* Consistency across the question set. *Avoid:* A new, different answer.

**37. What happens if the AI service is unavailable?** *Short:* Same as Q3 — falls back to the existing, pre-AI maintenance process (§10.6). *Detailed:* — *Evidence:* — *Assumptions:* — *Tested:* Same consistency check. *Avoid:* Same.

**38. What is your MVP architecture?** *Short:* Telemetry/event input → evidence extraction → alarm correlation → knowledge retrieval → RCA engine → LLM explanation → confidence → human review (§10.41). *Detailed:* — *Evidence:* — *Assumptions:* — *Tested:* Whether a concrete, memorized pipeline is ready. *Avoid:* Describing the full Part I–VI architecture as if it were the MVP.

**39. How would you scale?** *Short:* Per §10.35's maturity ladder — additional governance, observability, and edge/cloud optimization become necessary at each stage, not built upfront. *Detailed:* — *Evidence:* — *Assumptions:* — *Tested:* Whether scaling is framed as staged, not instantaneous. *Avoid:* Claiming current readiness to scale.

**40. How would you monitor production?** *Short:* Full observability — availability, latency, retrieval failures, confidence distribution, abstention rate, tool errors, data quality (§10.23). *Detailed:* — *Evidence:* — *Assumptions:* — *Tested:* Specificity of metrics. *Avoid:* "We'd monitor it" without naming metrics.

### AI

**41. What if the model hallucinates?** *Short:* Mitigated by tool-based access, RAG, structured outputs, citations, and — as the last line of defense — abstention and human review (Ch.9 §9.35). *Detailed:* — *Evidence:* — *Assumptions:* — *Tested:* Whether multiple layered mitigations are named. *Avoid:* One silver-bullet answer.

**42. What if the RAG retrieval is wrong?** *Short:* Hybrid retrieval + reranking reduce the risk; source-grounding makes wrong retrieval detectable (§10.22, Ch.9 §9.17–§9.19). *Detailed:* — *Evidence:* — *Assumptions:* — *Tested:* Whether this is framed as risk-reduced, not risk-eliminated. *Avoid:* Overclaiming.

**43. What if the model drifts?** *Short:* Drift monitoring flags it; scheduled retraining/revalidation addresses it (§10.21). *Detailed:* — *Evidence:* — *Assumptions:* — *Tested:* Whether drift is treated as an ongoing operational concern, not a one-time solved problem. *Avoid:* Implying drift is a solved, past issue.

**44. What if the elevator model changes?** *Short:* Named as an OOD/domain-shift concern requiring detection and, likely, revalidation (§9.32, §10.30's scope note). *Detailed:* — *Evidence:* — *Assumptions:* — *Tested:* Whether this is acknowledged as a real, open challenge. *Avoid:* Claiming automatic generalization.

**45. How does the system abstain?** *Short:* Explicitly, when evidence or confidence is insufficient, per Ch.9 §9.31's designed behavior. *Detailed:* — *Evidence:* — *Assumptions:* — *Tested:* Confidence and immediacy of the answer — this should be reflexive by this point in the book. *Avoid:* Hesitation.

**46. How is confidence calibrated?** *Short:* Via a dedicated probabilistic model (Ch.7), not LLM self-report; full calibration methodology is deferred to a later phase (Ch.9 §9.29). *Detailed:* — *Evidence:* — *Assumptions:* — *Tested:* Whether "the LLM says how confident it is" is avoided. *Avoid:* That exact wrong answer.

**47. How do you prevent human overtrust?** *Short:* Named as the least architecturally-solvable risk in this book (§10.31) — addressed through UI design and process discipline, not purely technical controls. *Detailed:* — *Evidence:* — *Assumptions:* — *Tested:* Whether this is honestly flagged as a real, human-factors limitation, not claimed as solved. *Avoid:* Overclaiming that overtrust is prevented by architecture alone.

**48. How do you audit the diagnosis?** *Short:* Full evidence trace with source/version/timestamp lineage (§10.19, §10.23). *Detailed:* — *Evidence:* — *Assumptions:* — *Tested:* Concreteness. *Avoid:* "Everything is logged" without the specific chain.

### Architecture

**49. Why do you need an LLM?** *Short:* For language understanding, planning, and explanation — never for computation or control (Ch.9 §9.11–§9.12). *Detailed:* — *Evidence:* — *Assumptions:* — *Tested:* Precise task-scoping. *Avoid:* "LLMs are powerful."

**50. Why not use rules?** *Short:* Rules remain core to the deterministic layer (fault-tree traversal, calculations); they don't scale to free-text interpretation or the full evidence-weighing task (Ch.9 §9.1, §10.44's own use of "no blind generation" alongside deterministic conflict detection). *Detailed:* — *Evidence:* — *Assumptions:* — *Tested:* Whether rules are dismissed (wrong) or precisely scoped (right). *Avoid:* Dismissing rules entirely.

**51. Why not use a conventional ML model?** *Short:* Used extensively — for anomaly detection and fault classification (Ch.6, Ch.9 Part II) — alongside, not instead of, the LLM/RAG/agent layer, each doing a different job. *Detailed:* — *Evidence:* — *Assumptions:* — *Tested:* Whether "conventional ML" is understood as already integral, not a rejected alternative. *Avoid:* Implying the architecture is LLM-only.

**52. Why use multiple agents?** *Short:* Specialization and debuggability for genuinely distinct reasoning stages, weighed against real coordination cost (Ch.9 §9.21). *Detailed:* — *Evidence:* — *Assumptions:* — *Tested:* Whether the honest trade-off, not just the benefit, is cited. *Avoid:* "More agents = better" (directly contradicted in Ch.9 §9.24).

**53. Why not use one model?** *Short:* Single-agent remains a legitimate, lower-cost option; multi-agent is chosen where specialization earns its overhead (Ch.9 §9.21). *Detailed:* — *Evidence:* — *Assumptions:* — *Tested:* Whether single-agent is fairly represented, not dismissed. *Avoid:* Treating single-agent as automatically inferior.

**54. Which components are deterministic?** *Short:* Signal calculations, fault-tree/knowledge-graph traversal, timestamps, thresholds, source citation, safety constraints (Ch.9 §9.44). *Detailed:* — *Evidence:* — *Assumptions:* — *Tested:* Whether a concrete list, not a vague gesture, is given. *Avoid:* Vagueness.

**55. Which are probabilistic?** *Short:* Hypothesis ranking, anomaly scores, diagnosis confidence, competing-cause comparison (Ch.9 §9.44). *Detailed:* — *Evidence:* — *Assumptions:* — *Tested:* Same. *Avoid:* Same.

**56. Which decisions remain human?** *Short:* Safety-sensitive decisions, ambiguous diagnoses, physical inspection, final repair authorization, novel faults, low-confidence cases (Ch.9 §9.44, Part I throughout). *Detailed:* — *Evidence:* — *Assumptions:* — *Tested:* Same. *Avoid:* Same.

### Strategic

**57. What makes this deployable?** *Short:* A staged maturity path (§10.35) from the current Level 1 research prototype toward production, with each stage's required evidence named explicitly. *Detailed:* — *Evidence:* — *Assumptions:* — *Tested:* Whether deployability is framed honestly as a path, not a current state. *Avoid:* Claiming current deployability.

**58. What makes this different from predictive maintenance?** *Short:* Predictive maintenance forecasts future risk; this explains an already-occurred fault's cause (Ch.5 §5.14, restated consistently throughout). *Detailed:* — *Evidence:* — *Assumptions:* — *Tested:* Consistency with every earlier chapter's answer to this exact question. *Avoid:* Any drift.

**59. What makes this different from a technician chatbot?** *Short:* Structured, tool-grounded, multi-stage reasoning over verified evidence with an auditable trace — not free-form conversation (Ch.9 §9.47 Q47). *Detailed:* — *Evidence:* — *Assumptions:* — *Tested:* Same consistency check. *Avoid:* Same.

**60. What is the biggest technical risk?** *Short:* Calibrating honest confidence and correct abstention without labeled production data (Ch.7 §7.39, Ch.9 §9.29/§9.50 Q50). *Detailed:* — *Evidence:* — *Assumptions:* — *Tested:* Whether a real, unsolved problem is named. *Avoid:* Naming something trivial.

**61. What is the biggest safety risk?** *Short:* Not a technical risk at all, architecturally — human overtrust in a low-confidence or wrong output (§10.31's own flagged "least architecturally-solvable risk"). *Detailed:* — *Evidence:* — *Assumptions:* — *Tested:* Whether the team distinguishes "safety risk from the AI directly" (near-zero, by design) from "safety-adjacent risk from human process" (real, honestly flagged). *Avoid:* Claiming zero safety risk of any kind.

**62. What is the biggest cybersecurity risk?** *Short:* RAG/knowledge-base poisoning and prompt injection — the AI-specific attack surface a conventional industrial system doesn't have (§10.22, Ch.9 §9.36). *Detailed:* — *Evidence:* — *Assumptions:* — *Tested:* Whether an AI-specific risk, not just a generic IT risk, is named. *Avoid:* A generic cybersecurity answer that ignores the AI-specific surface.

**63. What would you remove if you had only two months?** *Short:* The full production-grade infrastructure (Parts I–VII); keep the MVP reasoning pipeline (§10.41) that actually demonstrates the core contribution. *Detailed:* — *Evidence:* — *Assumptions:* — *Tested:* Whether the team can prioritize honestly under a real constraint. *Avoid:* Claiming nothing would need to be cut.

**64. What would you never automate?** *Short:* Anything in §10.7's "AI Must Not Control" column and §10.34's excluded operational-controls tier — safety override, brake release, safety-chain bypass, autonomous rescue. *Detailed:* — *Evidence:* — *Assumptions:* — *Tested:* Whether this list is immediate and firm. *Avoid:* Any hesitation.

**65. What evidence would you need before production deployment?** *Short:* Real (or credibly representative) data at each maturity stage (§10.35), sustained shadow-mode and pilot performance (§10.36), and full safety/cybersecurity boundary validation (Parts I–II) — not marketing-quality demo results alone. *Detailed:* — *Evidence:* — *Assumptions:* — *Tested:* Whether the team understands the real distance between a hackathon demo and production readiness. *Avoid:* Implying the hackathon prototype is close to this bar.

---

# Master Risk Matrix

| Category | Risk | Failure Mode | Detection | Mitigation | Human Role |
|---|---|---|---|---|---|
| Safety | AI influences a safety-critical decision | (Architecturally prevented, not merely mitigated) | N/A — no path exists | §10.2, §10.7, §10.38's hard boundary | Always the sole authority over safety-relevant action |
| Cybersecurity | Compromise of the diagnostic pipeline | Data tampering, prompt injection, RAG poisoning | §10.23 observability | §10.11–§10.13, §10.22 | Reviews flagged/quarantined evidence |
| Data | Corrupted or missing evidence | Sensor/network/ingestion fault | §10.14's checks | Explicit flagging, never silent imputation | Confirms via independent means when flagged |
| AI | Hallucination or overconfidence | Free generation beyond grounded evidence | Structured-output/citation audit | RAG, tools, structured outputs, abstention | Verifies before any action |
| Infrastructure | Cloud/edge/network outage | Component failure | Availability monitoring | Graceful degradation (§10.6) | Uses existing pre-AI process if needed |
| Operations | Model drift, stale knowledge | Real-world distribution shift | §10.21 drift monitoring | Scheduled retraining/revalidation | Approves updates |
| Human Factors | Overtrust or under-review | Rubber-stamping AI output | Difficult — the least detectable risk in this table | Training, UI design, process discipline | The actual, irreducible mitigation |

# Master Architecture

```
                     PHYSICAL ELEVATOR
                            │
                     SAFETY / CONTROL
                            │
                 ───────────┼───────────
                            │
                    OBSERVATIONAL DATA
                            ↓
                    EDGE / GATEWAY
                            ↓
                SECURE DATA INGESTION
                            ↓
             ┌──────────────┼──────────────┐
             ↓              ↓              ↓
       TELEMETRY         EVENTS        MAINTENANCE
             │              │              │
             └──────────────┼──────────────┘
                            ↓
                  SIGNAL / EVENT ANALYTICS
                            ↓
                    STRUCTURED EVIDENCE
                            ↓
             ENGINEERING KNOWLEDGE LAYER
                  ┌─────────┼─────────┐
                  ↓         ↓         ↓
                FMEA      FTA      KNOWLEDGE
                                      GRAPH
                  └─────────┼─────────┘
                            ↓
                     RCA ENGINE
                            ↓
                  AI ORCHESTRATION
                    ↙      ↓      ↘
                 TOOLS    RAG    MODELS
                    ↘      ↓      ↙
                   EVIDENCE VERIFICATION
                            ↓
                      RCA OUTPUT
                            ↓
                   EXPLAINABILITY
                            ↓
                 CONFIDENCE / ABSTAIN
                            ↓
                     HUMAN REVIEW
                            ↓
                  MAINTENANCE PROCESS
                            ↓
                    VERIFIED OUTCOME
                            ↓
                     HISTORICAL DATA
```

Surrounding the entire architecture: **CYBERSECURITY + IDENTITY + ACCESS CONTROL + AUDITING + MONITORING + DATA GOVERNANCE** (Parts II–IV, applied end-to-end, not as a bolt-on). Separately, and never touched by anything in the diagram above: the **SAFETY CONTROL SYSTEM**, independently protected, exactly as Part I established.

# Master Principles

1. Safety functions remain independent — always, architecturally, not by policy alone.
2. AI observes before it recommends; it never acts.
3. Evidence precedes conclusions, never the reverse.
4. Missing evidence must reduce confidence, never be silently treated as normal.
5. Correlation is not causation — verified at every layer, from alarms to SHAP scores.
6. High confidence is not certainty.
7. The LLM is not the source of truth.
8. Retrieved data must be provenance-aware.
9. Tools perform deterministic calculations; the LLM reasons over their results.
10. Least privilege applies to every agent and every tool, without exception.
11. Cybersecurity is part of system architecture, not an add-on.
12. Data integrity is part of diagnostic reliability, not a separate concern.
13. Every conclusion should be auditable, end to end.
14. The system must be able to abstain, and should be trusted more, not less, for doing so.
15. Human expertise remains part of the safety boundary, permanently.
16. More AI complexity does not automatically produce a better diagnosis.
17. Production readiness requires evidence at every maturity stage, not demonstration quality alone.
18. Prototype capability must never be confused with certification.

---

# What We Now Understand

Elevator safety architecture is independent by design, and this project's diagnostic AI is deliberately, architecturally kept outside it — not merely instructed to stay outside, but structurally unable to reach it. Functional safety (IEC 61508, PESSRAL) is a certified property distinct from statistical accuracy, however high. Cyber-physical security (IEC 62443, ISO 8102-20 — a standard KONE itself helped write) protects the data this project's reasoning depends on, addressing an attack surface that now includes the AI/RAG layer specifically, not just conventional OT/IT concerns. Data integrity is inseparable from diagnostic reliability — bad data produces bad RCA regardless of how sophisticated the reasoning layer above it becomes. Edge and cloud architecture each serve genuinely different needs, and a real deployment uses both deliberately, not by default. Model governance, audit logging, and reproducibility are what make this system's conclusions defensible six months later, not just at the moment they're generated. Production readiness is a staged, evidence-gated maturity path, and this project sits honestly at its earliest stage. Resilience means the elevator is unaffected by any failure of the diagnostic layer, always. And auditability — the ability to trace any conclusion, fully, to its source — is not a feature this system has; it's the structural property everything else in this chapter exists to make true.

# The Core Principle

> **KONE ELEVATE SHOULD BE AN INTELLIGENCE LAYER AROUND THE ELEVATOR, NOT A REPLACEMENT FOR THE ELEVATOR'S SAFETY SYSTEM.**

Technically: every architectural choice in this chapter — the hard boundary of §10.38, the least-privilege permissions of §10.22 and §10.34, the graceful degradation of §10.6, the independent standards landscape of Part I — exists to make this one sentence true by construction, not by intention. A system whose safety depends on its designers remembering to be careful is not a safe system; a system whose architecture makes the unsafe path structurally unreachable is. This chapter's entire purpose has been building the second kind.

---

# Bridge to Phase 9 — Validation, Evaluation, Fault Scenarios, Demonstration & Evidence of Value

The question this research book has been building toward for eight phases changes shape one final time: from **"can the system be safely and securely architected?"** — answered, at the level this research book can answer it, across this chapter — to **"how do we prove that it actually works?"**

Phase 9 must investigate evaluation metrics, validation strategy, the fault scenario library (already begun across Chapters 2, 4, and 7), benchmark design, the synthetic-vs-real-data distinction this book has insisted on at every turn, ground truth, RCA accuracy, fault-isolation accuracy, top-k accuracy, evidence precision, retrieval accuracy, explanation quality, calibration, abstention behavior, false positives and negatives, detection latency, technician time saved, diagnostic-effort reduction, baseline comparison, human-vs-AI comparison, shadow mode (§10.36 introduced the concept; Phase 9 must design it concretely), ablation studies, robustness and failure injection, demonstration design, hackathon-prototype validation specifically, reproducibility (§10.37, now applied to evaluation itself), limitations, and — the question every judge-question section in this entire book has been implicitly building toward — what evidence is actually sufficient before a claim can be made to a judge.

Phase 9 content is not generated here — this document ends at the close of Phase 8.

---

## Sources Consulted

- ISO, "ISO 8102-20:2022 — Electrical requirements for lifts, escalators and moving walks — Part 20: Cybersecurity," iso.org
- KONE Corporation, "Elevators and escalators just got safer — thanks to a new cybersecurity standard," kone.com/en/news-and-insights/stories
- Liftinstituut, "International Standards Organization publishes new cybersecurity standard," liftinstituut.com/newsroom
- iTeh Standards / genorma.com, ISO 8102-20:2022 scope and technical-topic summaries
- Elevatori Magazine, industry analysis of PESSRAL implementation risks
- Elevator World (2026), industry commentary on programmable safety electronics, IoT, and compliance gaps in the current lift-standards landscape
- General background on EN 81-20/50, ISO 8100 series, ASME A17.1/CSA B44/A17.2/A17.4, IEC 61508, IEC 62061, IEC 62443, ISO/IEC 27001, and the NIST Cybersecurity Framework drawn from established, stable, widely-documented industry and standards-body knowledge — none of it reproduces copyrighted standard text, and any real engineering decision should consult the authoritative current version of each standard directly rather than this summary
