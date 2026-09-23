# PHASE 10 — SCOPE, PRIORITIZATION, WHAT NOT TO BUILD, MVP ARCHITECTURE & TECHNICAL DECISION FRAMEWORK

### *KONE Elevate — Autonomous Fault Isolation & Root Cause Analysis: Master Research Book*

## How to Read This Chapter

This chapter is different in kind from the nine that precede it. Phases 1–9 investigated the problem space; this one makes decisions. It draws on nothing new — every claim below traces back to a specific, already-established conclusion from an earlier chapter — and its labels reflect that: **[PREVIOUS PHASE CONCLUSION]** (the dominant label here), **[PROJECT SOURCE]**, **[STRATEGIC RECOMMENDATION]** (this chapter's own synthesis, clearly marked as a recommendation rather than a fact), **[ENGINEERING INFERENCE]**, **[PROPOSED DESIGN]**, **[NOT ESTABLISHED]**. No inference is converted into a fact anywhere below.

```
RESEARCH → UNDERSTANDING → CONSTRAINTS → PRIORITIES
   → ARCHITECTURAL DECISIONS → MVP → DEMONSTRABLE SYSTEM → FUTURE ROADMAP
```

---

## From Phase 9 to Phase 10

Phase 9 established how the system should be validated — and validation itself exposed real constraints: data scarcity (Ch.9 §11.24), a necessarily limited fault-scenario set, limited hackathon time, limited engineering resources, the safety and cybersecurity requirements of Chapter 10, and the genuine complexity cost every additional AI component carries. **Not everything that is technically possible should be built.** This chapter's single governing principle, stated once and then applied relentlessly:

> **TECHNICAL POSSIBILITY ≠ PROJECT PRIORITY.**

---

# Part I — The Problem and the Product

## 12.1 The Central Product Question

> *"What is the smallest technically credible system that demonstrates a meaningful improvement in elevator fault isolation and root-cause analysis?"*

This chapter derives that answer from the preceding nine phases rather than asserting it up front — Parts II through IX below are, collectively, that derivation.

## 12.2 Problem Definition

```
CURRENT STATE → GAP / OPPORTUNITY → KONE ELEVATE → EXPECTED VALUE
```

**Current state** *[PREVIOUS PHASE CONCLUSION, Ch.3]*: KONE's 24/7 Connected Services and Technician Assistant already provide real-time monitoring, remote diagnostics, and an LLM-based (Bedrock/Claude) technician support tool serving roughly 30,000 monthly queries. **Existing capabilities** *[PREVIOUS PHASE CONCLUSION, Ch.4]*: across the researched competitive landscape (Otis ONE, Schindler Ahead/Cube/TOC, TK Elevator MAX/HELIX), remote monitoring, informed dispatch, and general technician-facing AI assistance are all publicly demonstrated by at least one major OEM. **Remaining diagnostic gap** *[PREVIOUS PHASE CONCLUSION, Ch.4 §6.14]*: no OEM researched in this book publicly demonstrates structured multi-hypothesis RCA, primary/consequential alarm correlation, explicit alternative-cause elimination, an auditable evidence trail, or calibrated, abstention-capable confidence. **Proposed KONE Elevate capability**: exactly that gap — an evidence-driven layer that turns a correlated alarm cluster into a ranked, evidence-cited, confidence-scored set of root-cause hypotheses, verified by a human before any action is taken. **Boundary**: KONE Elevate does not attempt to replace monitoring, dispatch, technician chat, or predictive maintenance — it assumes those functions exist (or could exist) around it and focuses narrowly on the diagnostic-reasoning step between "an alarm cluster occurred" and "a technician understands why."

## 12.3 Problem Statement, Five Ways

- **One-sentence:** *KONE Elevate turns a correlated cluster of elevator alarms into a ranked, evidence-cited set of probable root causes, with calibrated confidence and human verification built in.*
- **Technical:** *Given telemetry, event, alarm, and maintenance-history evidence for an elevator incident, KONE Elevate performs alarm correlation, evidence-weighted hypothesis generation and ranking (grounded in engineering fault trees, FMEA, and retrieved documentation), and produces an auditable, confidence-scored root-cause recommendation for human review.*
- **Technician-focused:** *Instead of starting from a raw fault code and a stack of manuals, you get a short list of the most likely causes, ranked, with the specific evidence for and against each one already pulled together — and it tells you plainly when it isn't sure.*
- **Business:** *A diagnostic-support layer designed to reduce the evidence-gathering and hypothesis-narrowing effort a technician currently performs manually, without claiming to replace their judgment or KONE's existing connected infrastructure.*
- **Judge-facing:** *An evidence-driven, auditable, abstention-capable root-cause-analysis layer — the specific diagnostic-reasoning capability this project's own competitive research found no major elevator OEM publicly demonstrating.*

**No version claims "current systems cannot diagnose faults"** — every version above is scoped to the specific, evidenced gap (Ch.4), not an unsupported blanket claim about competitors' capability.

## 12.4 Value Proposition: Hypothesis vs. Proven

Possible value dimensions — fault isolation, RCA assistance, evidence correlation, reduced diagnostic effort, faster investigation, better technician preparation, explanation, auditability — are, per Chapter 9 §11.43, **value hypotheses (H1–H5) this project's methodology is built to test, not proven value.** This chapter treats them accordingly throughout: every architectural decision below is justified by what it would let this project *test*, never by an assumed business outcome.

## 12.5 The Single Core Capability

**If the team could build only one technically meaningful capability, it should be evidence-weighted root-cause ranking with calibrated confidence — RCA itself, not anomaly detection or alarm correlation alone.** Reasoning: anomaly detection and alarm correlation are necessary *foundations* (Ch.6), but neither is, by itself, the differentiator Chapter 4's competitive research identified — any sufficiently mature connected-elevator platform can plausibly detect an anomaly or correlate a few alarms. **What Chapter 4 found no competitor publicly demonstrating is specifically the next step:** weighing multiple candidate causes against evidence, ranking them, eliminating inconsistent alternatives, and reporting honest, calibrated confidence — that is RCA, and it is the one capability this project cannot afford to compromise on, even if every other capability in this chapter's tables below gets cut.

---

# Part II — Prioritization

## 12.6 Must-Have vs. Nice-to-Have

| Capability | Must Have | Nice to Have | Research Only | Exclude | Reason |
|---|---|---|---|---|---|
| Telemetry/event ingestion | ✓ | | | | No evidence without it |
| Alarm correlation | ✓ | | | | Foundational to the cascade/primary-consequential differentiator (Ch.4 §4.5, Ch.6) |
| Signal processing (Ch.6 core methods) | ✓ | | | | Required to extract usable evidence at all |
| Anomaly detection | ✓ | | | | The trigger for the whole pipeline |
| Fault trees / FMEA | ✓ | | | | Cheap, doesn't require AI training data, structural to differentiated RCA (§12.5) |
| Bayesian/probabilistic ranking | ✓ | | | | Core to the calibrated-confidence differentiator (Ch.4's strongest identified claim) |
| RAG (small, curated corpus) | ✓ | | | | Grounds explanations in retrievable evidence (Ch.9 §9.11) |
| LLM (synthesis/explanation role only) | ✓ | | | | Chapter 9's own task-scoped justification, not a general-purpose chatbot |
| Tool calling | ✓ | | | | The mechanism that keeps the LLM off deterministic calculations (Ch.9 §9.14) |
| Explainability/evidence trace | ✓ | | | | The entire auditability differentiator depends on it |
| Confidence + abstention | ✓ | | | | §12.5's identified single strongest differentiator |
| Minimal technician interface | ✓ | | | | Without it, nothing above is actually usable |
| Multi-agent architecture | | | ✓ | | Deferred pending ablation evidence (Ch.9 §9.24, Ch.11 §11.23) — §12.16 |
| Knowledge graph (full graph DB) | | ✓ | | | Fault trees/FMEA cover MVP needs; a graph DB is a V1+ investment (§12.18) |
| Digital twin | | | ✓ | | Requires modeling effort far beyond hackathon scope (§12.17) |
| GNN | | | ✓ | | Requires graph-structured training data this project lacks at MVP scale (§12.17) |
| PINN | | | ✓ | | Requires physics-model formulation beyond hackathon scope (§12.17) |
| RUL / predictive maintenance | | | | ✓ | A different problem from RCA (§12.23) — explicitly out of this project's scope |
| Fleet-wide analytics dashboard | | | | ✓ | Not this project's differentiator; risks diluting focus (§12.24) |

**This table is deliberately ruthless.** The goal stated once and applied throughout: maximize demonstrated diagnostic value, not feature count.

## 12.7 MoSCoW for KONE Elevate

- **Must have:** alarm correlation, fault trees/FMEA, Bayesian ranking, evidence trace/explainability, confidence/abstention, a minimal technician interface — the exact "Must Have" column of §12.6, restated in MoSCoW form because it's the framework judges are most likely to recognize.
- **Should have:** RAG over a small curated document set, LLM-based synthesis/explanation, a second and third demo scenario beyond the flagship case.
- **Could have:** a lightweight knowledge-graph layer, a minimal (2-role) multi-agent split if time allows and ablation-style reasoning supports it, a richer technician interface.
- **Won't have (this build):** digital twin, GNN, PINN, RUL/predictive maintenance, fleet-wide dashboards, autonomous action of any kind (Part V).

## 12.8 A KONE-Elevate-Specific Value/Effort Framework

Rather than a generic software-scoring rubric, every candidate capability in this book is evaluated against five project-specific dimensions: **diagnostic value** (does it move the needle on §12.5's core capability), **evidence dependency** (how much real or synthetic data does it require to function credibly), **validation cost** (per Chapter 9's own methodology, how hard is it to actually test), **complexity cost** (latency, attack surface, debugging burden — Ch.10 §10.41), and **differentiation contribution** (does it address the specific gap Ch.4 identified, or does it duplicate something a competitor already shows). A capability scoring well on diagnostic value and differentiation but poorly on evidence dependency and validation cost (a GNN, for instance) is exactly the profile this framework is built to catch and defer.

## 12.9 Value vs. Complexity Quadrant

| | **Low Complexity** | **High Complexity** |
|---|---|---|
| **High Value** | **QUICK WINS:** alarm correlation, fault trees/FMEA, confidence/abstention, minimal explainability | **CORE INVESTMENTS:** Bayesian ranking engine, RAG (curated), LLM synthesis |
| **Low Value** *(for this project's specific differentiator)* | **DISTRACTIONS:** a polished dashboard UI, broad document ingestion beyond the demo's needs | **FUTURE RESEARCH:** digital twin, GNN, PINN, full multi-agent swarm, fleet-wide knowledge graph |

The MVP is built almost entirely from the top row; the bottom-right quadrant is exactly Part V's exclusion list.

---

# Part III — The MVP, Precisely Defined

## 12.10 MVP Definition: Inputs, Output, User

**Inputs (minimum evidence required):** the alarm(s) that triggered the incident, an event chronology around it, a small set of relevant telemetry signals (not the full sensor suite — just what Chapter 6's specific worked scenarios actually use), the elevator's operating state at the time, basic component metadata, the relevant fault-tree/FMEA knowledge, and — where available — a small maintenance-history excerpt. **Not** the full connected-elevator data platform Chapter 3 described; a deliberately narrow slice sufficient for the demo scenarios.

**Output**, precisely structured, never a generic paragraph:

```
INCIDENT → PRIMARY ABNORMALITY → AFFECTED SUBSYSTEM
   → TOP ROOT-CAUSE HYPOTHESES → SUPPORTING EVIDENCE
   → CONTRADICTING EVIDENCE → CONFIDENCE → RECOMMENDED VERIFICATION
   → TECHNICIAN REVIEW
```

**Why this beats a generic chatbot response:** every field above is independently checkable against the evidence trace (Ch.9 §9.18) — a technician (or a judge) can verify each claim against its source, which a free-form paragraph answer cannot offer regardless of how well-written it is.

**Primary user:** the field technician mid-investigation — chosen over a remote diagnostic specialist, maintenance planner, or supervisor because it's the role this project's entire evidence base (Ch.2's diagnostic-hypothesis framing, Ch.5's RCA methodology) was built around, and optimizing simultaneously for every user role would dilute the interface and the demo alike. **Secondary users:** a remote diagnostic specialist could use the same output for pre-dispatch triage; a maintenance planner could use the historical RCA record for scheduling — both plausible extensions, neither the MVP's design target.

## 12.11 The User Journey

```
FAULT OCCURS → SYSTEM RECEIVES EVENT → CASE CREATED → EVIDENCE COLLECTED
   → ALARMS CORRELATED → HYPOTHESES GENERATED → RCA → EXPLANATION
   → TECHNICIAN REVIEWS → VERIFICATION → MAINTENANCE → OUTCOME RECORDED
```

Each step maps directly onto a chapter already written: event reception (Ch.6's telemetry/event pipeline), case creation (Ch.7 §7.38's investigation state), evidence collection and correlation (Ch.6), hypothesis generation and RCA (Ch.7), explanation (Ch.9 Part VI), technician review and verification (Ch.9 §9.33, Ch.10 Part I), and outcome recording (Ch.10 §10.27's closed-loop learning) — **this journey is not a new design; it is this book's own architecture, walked end to end.**

## 12.12 MVP Architecture

```
                ELEVATOR DATA
                     ↓
             EVENT / TELEMETRY
                     ↓
              EVIDENCE LAYER
                     ↓
             ALARM CORRELATION
                     ↓
              RCA ENGINE
                ↙       ↘
          ENGINEERING    RAG
          KNOWLEDGE       │
        (fault trees,   (curated
         FMEA, Bayes)    documents)
                ↘       ↙
                 AI
             (synthesis,
              explanation)
                  ↓
           STRUCTURED RCA
                  ↓
            EXPLANATION
                  ↓
          CONFIDENCE / ABSTAIN
                  ↓
          TECHNICIAN REVIEW
```

Every box here is a **Must Have** from §12.6's table — nothing in this diagram is aspirational or deferred; this is, deliberately, the smallest architecture that still contains every element §12.5 identified as non-negotiable.

---

# Part IV — The Technology Decisions

## 12.13 What Should Be Deterministic?

*[PREVIOUS PHASE CONCLUSION, Ch.9 §9.44, Ch.10 Part VI]* Signal calculations, event ordering/timestamps, threshold checks, data validation, fault-tree traversal, FMEA lookup, database queries, source-citation formatting, and every safety-relevant constraint remain deterministic, rule-based code — never delegated to an LLM's free generation, for exactly the reasons Chapters 9 and 10 already established at length.

## 12.14 What Should Use ML? What Should Use an LLM? What Should Not?

**ML** — genuinely valuable, but **not required for the MVP's core demo path**: anomaly detection and classical classification (Ch.6) add real value at scale but the MVP's curated demo scenarios can function with simpler, threshold/rule-based detection sufficient to illustrate the pipeline; sensor fusion and RUL are deferred (§12.6). **LLM** — valuable specifically for document interpretation (unstructured maintenance notes/manuals), hypothesis-space language generation from structured evidence, evidence synthesis into a coherent narrative, technician-facing explanation, and investigation planning (Ch.9 §9.1's own task table) — **not** for deterministic numerical work, safety decisions, equipment control, unverified probability generation, unsupported fault-code invention, or anything resembling authoritative safety instruction (Ch.9 §9.12, Ch.10 Part I).

## 12.15 The RAG Decision

**Does KONE Elevate actually need RAG? Yes — scoped narrowly.** Fine-tuning is rejected for the MVP: it requires a labeled training corpus this project's own research (Ch.9 Part II) confirms is scarce industry-wide, and a fine-tuned model can't easily cite its source the way retrieval can (Ch.9 §9.11's exact reasoning). A fully static (non-retrieval) knowledge base loses the ability to synthesize across multiple documents dynamically. A structured engineering database (fault trees, FMEA) is **already the MVP's other knowledge source** (§12.12's left branch) — RAG's role is specifically the *unstructured* documentation (manuals, bulletins) that doesn't fit that schema, making the two complementary rather than competing, exactly as Chapter 9's hybrid-retrieval design already established. **For the MVP specifically: a small, curated document set** (not a sprawling corpus) — enough to demonstrate real retrieval and citation behavior, without taking on the ingestion/versioning/provenance burden (Ch.10 §10.19, §10.37) a large corpus would require at this project's current stage.

## 12.16 The Multi-Agent Decision

**Does KONE Elevate actually need multiple agents for the MVP? No — not yet, and not without evidence it earns the cost.** A single orchestrator using tool-calling (Ch.9 §9.14) — rather than a true multi-agent swarm — is the MVP's recommended architecture: it avoids the coordination, latency, debugging, and observability costs Chapter 9 §9.24 and Chapter 11 §11.23 both flag, without sacrificing any of §12.6's Must-Have capabilities, every one of which can be expressed as a tool call from a single orchestrating process. **If multi-agent architecture is retained at all**, the minimum defensible split is two roles — an evidence/investigation agent and a separate RCA-reasoning agent — never more, and never justified by "it looks more advanced" (the instruction's own, correct, standard). **This is explicitly a "build later, pending ablation evidence" decision (§12.42)**, not a rejection of multi-agent architecture as a concept — Chapter 9's own research on the approach remains valid; it simply hasn't earned its place in a time-constrained MVP without the comparison data Chapter 11 §11.23 specifies as the actual justification standard.

## 12.17 The Digital Twin, GNN, and PINN Decisions

**Digital twin:** compared against simulation and synthetic telemetry — a full digital twin requires detailed physics modeling and validation effort (Ch.9 §9.9) that is simply incompatible with hackathon timescales. **Decision: Research only.** The MVP instead uses lightweight, scenario-specific synthetic telemetry (Ch.9 §11.25) — enough to drive the demo scenarios, without the much larger engineering investment a genuine twin represents.

**GNN:** real academic precedent exists for elevator applications (Ch.9's GNN-LSTM door-fault paper), but a GNN requires graph-structured *training* data at a volume this project doesn't have at hackathon scale. **Decision: Research only.** The *concept* it would otherwise serve — component/subsystem relationships — is represented instead by the much simpler, already-built fault trees (§12.19), which don't require training data at all.

**PINN:** similarly real academic precedent (Ch.9's PINN + e-RGCN paper), but requires physics-model formulation and its own validation burden well beyond MVP scope. **Decision: Research only.**

**Not recommended merely because each is "technically fashionable"** — every one of these three would score well on Chapter 9's academic-literature review and poorly on §12.8's evidence-dependency and validation-cost dimensions, which is exactly the pattern this chapter's framework exists to catch.

## 12.18 The Knowledge Graph and Bayesian Reasoning Decisions

**Knowledge graph:** compared against a structured relational database and the fault-tree representation Chapter 7 already built. **Decision: fault trees/FMEA (already-built, hierarchical, rule-traversable structures) suffice for the MVP; a full graph database with graph-traversal algorithms is a V1/Future investment**, justified once the relationship complexity genuinely outgrows what a tree structure can represent — not before.

**Bayesian reasoning: core, not future.** Unlike every decision above, this one is decisively kept in the MVP — it is the specific mechanism behind §12.5's identified single strongest differentiator (calibrated confidence), it was already fully derived with worked examples in Chapter 7, and it requires no training data at all, only the engineering-reasoned illustrative priors this book has used consistently (never fabricated production statistics, per every prior chapter's standing discipline).

## 12.19 The Fault Tree/FMEA and Explainability Decisions

**Fault trees/FMEA: MVP-core**, and genuinely one of this project's strongest MVP assets precisely *because* they don't depend on AI training data — Chapter 7 built six complete fault trees and a full FMEA table through engineering reasoning alone, meaning this project has real, substantial diagnostic knowledge available on day one, independent of whatever data-scarcity constraints (Ch.9 §11.24) limit the AI-driven components.

**Explainability: MVP-core, at the minimum level Chapter 9 Part VI established** — evidence, source, hypothesis, alternatives, confidence, and a recommended verification step, no less.

## 12.20 Confidence, Abstention, and the Technician Interface

**Confidence and abstention: unambiguously MVP-core** — the project's single strongest identified differentiator (§12.5, Ch.4 §6.14), designed exactly as Chapter 7 and Chapter 9 already specified:

```
HIGH EVIDENCE → HIGHER CONFIDENCE
LOW / CONFLICTING EVIDENCE → LOWER CONFIDENCE
INSUFFICIENT EVIDENCE → ABSTAIN / ESCALATE
```

**Technician interface: deliberately minimal, not a dashboard.** The MVP interface shows exactly §12.10's output structure — incident summary, affected subsystem, likely causes, evidence, alternatives, confidence, recommended verification, source — and nothing more elaborate; a large, feature-rich dashboard is explicitly identified as a distraction in §12.9's quadrant, not a differentiator.

---

# Part V — What Not to Build

## 12.21 What Not to Build

Explicitly, and for reasons already established across this book, none of the following belong in KONE Elevate's initial system: **autonomous elevator control, safety-system control, autonomous rescue, or autonomous repair execution** (Ch.10 Part I's architectural boundary makes these categorically impossible by design, not merely undesirable); **universal fault diagnosis across every elevator model** (this book's own scope is a modern gearless traction elevator, Ch.1, and claiming universality would contradict Chapter 9's own generalization caveats); **a fleet-wide digital twin** (§12.17); **fully autonomous maintenance** (contradicts the human-in-the-loop principle running through the entire book); **unnecessary multi-agent complexity, GNN, or PINN** (§12.16–§12.17); **an unnecessary mobile application or predictive-maintenance dashboard** (dilutes focus away from §12.5's core capability); and **a broad, generic chatbot** (§12.22).

## 12.22 Why Not a Generic Chatbot

A chatbot can answer questions and summarize documentation. **KONE Elevate needs evidence correlation, structured diagnostic reasoning, fault isolation, root-cause ranking, source grounding, confidence, and abstention** — capabilities a conversational interface alone does not provide, regardless of how good the underlying LLM is. **CHATBOT ≠ DIAGNOSTIC INTELLIGENCE**, and this distinction is not cosmetic: it's the exact reason Chapter 9's architecture routes every substantive judgment through tools, structured reasoning, and an evidence trace rather than free conversational generation.

## 12.23 Why Not Another Predictive-Maintenance Platform

*[PREVIOUS PHASE CONCLUSION, Ch.3–Ch.4]* Prediction asks *"something may fail"*; diagnosis asks *"what is likely causing the observed problem"*; RCA asks *"why did this failure occur."* These are three genuinely different problems, and predictive maintenance is already a crowded, well-established category across every OEM this book researched (Ch.3's KONE 24/7 Connected Services, Ch.4's Otis/Schindler/TK Elevator platforms). **Building another predictive-maintenance platform would compete head-on where competitors are already strong, rather than occupying the specific gap Chapter 4 identified** — a strategically weaker choice than this project's actual, deliberately-chosen focus.

## 12.24 Why Not a Giant Platform

```
Large architecture → more components → more failure modes
   → more cybersecurity surface (Ch.10 §10.10) → more validation burden (Ch.9)
   → less demonstrable depth
```

A sprawling platform spreads a fixed amount of hackathon time across many shallow capabilities rather than one deep, well-validated one — directly contradicting §12.1's own governing question, which asks for the *smallest* credible system, not the largest impressive-sounding one.

## 12.25 Core Differentiation, Previewed

Without prematurely performing the full competitive-strategy analysis Phase 11 will own, the technical area that appears most promising for differentiation, based on everything established so far: **evidence-driven RCA with primary/consequential alarm separation, alternative-cause elimination, diagnostic provenance, and uncertainty-aware (calibrated, abstention-capable) reasoning** — restated from Chapter 4's own conclusion, framed here as "**potential** differentiation," since Phase 11 has not yet formally revisited it against the fullest current competitive picture.

---

# Part VI — The Roadmap

## 12.26 MVP → V1 → V2 → Production

- **MVP** (this chapter's scope): §12.6's Must-Have list, 3–5 demo scenarios, synthetic/curated data, single-orchestrator architecture.
- **V1**: broader RAG corpus with real provenance management, a minimal 2-role multi-agent split *if* ablation evidence (Ch.11 §11.23) supports it, expert-reviewed benchmark validation (Ch.11 Phase C).
- **V2**: richer data (historical, where available), a full knowledge-graph layer if relationship complexity has genuinely outgrown fault trees, shadow-mode validation (Ch.11 Phase D).
- **Production**: everything Chapter 10 Part I/VII specifies — full safety/cybersecurity validation, pilot-stage deployment, formal governance — none of it claimed or attempted at the MVP stage.

## 12.27 Technology, Data, and Validation Evolution

```
RULES → RULES + SIGNAL PROCESSING → RULES + ML → RCA ENGINE
   → RCA + RAG → RCA + LLM → RCA + TOOL USE → MULTI-AGENT
   → DIGITAL TWIN / GRAPH / ADVANCED AI
```

```
SYNTHETIC DATA → EXPERT-LABELED SCENARIOS → HISTORICAL DATA
   → CONTROLLED TEST DATA → SHADOW MODE → PILOT DATA → FLEET-SCALE DATA
```

```
OFFLINE SCENARIO TEST → BENCHMARK → EXPERT REVIEW → ABLATION
   → SHADOW MODE → HUMAN-REVIEWED PILOT → OPERATIONAL VALIDATION
```

**Complexity is introduced only when justified by evidence and value** — each arrow above represents a step this project would need to earn, via the specific validation gate (Ch.11 §11.44) associated with it, not a step assumed automatically forthcoming.

---

# Part VII — Engineering Discipline

## 12.28 Build vs. Buy

**Build:** diagnostic reasoning, the evidence model, RCA logic, the domain-knowledge layer (fault trees/FMEA), orchestration — this project's actual intellectual contribution. **Use existing services for:** the LLM itself, a vector database (for RAG), cloud storage, authentication, and monitoring infrastructure — **building everything from scratch is unnecessary**, and would spend scarce hackathon time reinventing commodity infrastructure instead of the genuinely differentiated reasoning layer.

## 12.29 Technology Selection Criteria

Every technology choice in this chapter was implicitly weighed against: accuracy, explainability, latency, cost, data requirements, security (Ch.10), maintainability, integration effort, validation burden (Ch.11), and vendor dependence — the same framework §12.8 formalized, applied consistently rather than ad hoc.

## 12.30 Architectural Simplicity: Minimal / Intermediate / Advanced

| | Capabilities | Complexity | Validation Burden | Benefit | Risk |
|---|---|---|---|---|---|
| **Minimal** | Rules + fault trees only, no LLM | Low | Low | Fast to build, easy to validate | Limited differentiation, weak explanation quality |
| **Intermediate (this chapter's MVP recommendation)** | Fault trees + Bayesian ranking + RAG + single-orchestrator LLM + confidence/abstention | Moderate | Moderate, achievable within hackathon validation scope (Ch.11) | Demonstrates the full differentiated value proposition | Still requires disciplined scoping to stay achievable |
| **Advanced** | Full multi-agent + knowledge graph + digital twin + GNN/PINN | High | Very high — likely exceeds what's achievable to genuinely validate in hackathon time | Impressive on paper | High risk of shallow, unvalidated, or non-functional depth (§12.24) |

**This chapter recommends Intermediate, explicitly and by name** — not the most technically impressive option available, the most defensible one.

## 12.31 Technical Debt

Rapidly assembling AI components under time pressure risks undocumented dependencies, poor observability, inconsistent data schemas, prompt fragility (small prompt changes silently breaking downstream behavior), vendor lock-in, and code that's difficult to test — real risks worth naming explicitly now, precisely because the Intermediate architecture (§12.30) is still complex enough to accumulate them if built carelessly.

## 12.32 Prototype vs. Production

| Aspect | Hackathon Prototype | Production System |
|---|---|---|
| Data | Synthetic/curated (Ch.9 §11.25) | Real, governed (Ch.10 §10.20) |
| Security | Basic hygiene only | Full IEC 62443/ISO 8102-20 posture (Ch.10 §10.11) |
| Reliability | Best-effort | Formal availability/MTBF targets (Ch.10 §10.24) |
| Scalability | Single-scenario demo | Fleet-scale (Ch.10 §10.16) |
| Validation | Feasibility-level (Ch.11 §11.45) | Full A–F roadmap (Ch.11 §11.46) |
| Monitoring | Manual observation | Full observability stack (Ch.10 §10.23) |
| Model governance | Informal | Full lifecycle (Ch.10 §10.21) |
| Standards | None claimed | PESSRAL/IEC 61508 scoping required for any safety-adjacent claim (Ch.10 §10.4) |
| User testing | Judge/demo feedback | Structured human-vs-AI study (Ch.11 §11.37) |
| Integration | Standalone demo | Real KONE system integration (not attempted here) |

## 12.33 Team Capability Constraint

Realistic hackathon constraints — limited time, limited compute, no proprietary KONE data access, necessarily limited domain expertise relative to a career elevator engineer, and limited testing resources — are exactly why §12.30 recommends Intermediate rather than Advanced. **Architecture should match team capability, not the other way around** — no assumption is made here about any individual team member's specific skills; the constraint is structural to any student hackathon team, not a comment on this one.

---

# Part VIII — Building It

## 12.34 Time-Boxed Build Strategy and Build Order

```
STEP 1   Define scenario(s)
STEP 2   Create data schema
STEP 3   Build evidence layer
STEP 4   Implement alarm correlation
STEP 5   Implement RCA logic (fault trees + Bayesian ranking)
STEP 6   Add retrieval (RAG)
STEP 7   Add LLM synthesis
STEP 8   Add explanation
STEP 9   Add confidence/abstention
STEP 10  Validate (Ch.11's Phase A methodology)
```

**Do not start with the LLM.** The dependency order is `Problem definition → Data model → Evidence → RCA logic → Retrieval → AI orchestration → Interface` — **because every later step depends on the structure the earlier ones establish**: RCA logic needs a data model to reason over; RAG needs to know what it's retrieving *for*; the LLM needs both the evidence and the RCA output already well-defined before it can synthesize anything faithful to them (Ch.9 §9.11's groundedness principle, restated as a build-order consequence rather than just a design principle).

## 12.35 The Minimum Demo

The smallest impressive but technically defensible demonstration still contains, in order: (1) a fault occurs, (2) data is received, (3) evidence is extracted, (4) alarm correlation occurs, (5) candidate causes are generated, (6) RCA ranks them, (7) evidence is shown, (8) confidence is shown, (9) human verification occurs. **Nothing on this nine-step list is optional** — it is, in effect, §12.6's Must-Have column expressed as a sequence rather than a table.

## 12.36 Demo Case Prioritization and What-If Scenarios

Ranking criteria for candidate scenarios: technical clarity, evidence richness, causal-reasoning depth, visualizability, feasibility to actually build in the available time, judge comprehensibility, and differentiation. **This selects exactly Chapter 11 §11.40's five cases** (motor overcurrent, door degradation, encoder/position anomaly, alarm cascade, insufficient evidence) — this chapter does not re-derive a different set; it confirms the one Chapter 11 already built meets these criteria.

**Demo what-if robustness variations**, for the MVP specifically: a missing signal, an additional consequential alarm layered onto a known case, conflicting evidence, a different operating condition, and a sensor anomaly — each should visibly change the system's output (lower confidence, a different ranking, or abstention), demonstrating live that the reasoning is genuinely evidence-sensitive rather than a fixed, scripted response per scenario.

## 12.37 Acceptance Criteria and MVP Failure Conditions

**Acceptance criteria, as measurable categories, never invented numerical targets:** correct evidence retrieval, correct subsystem ranking, correct RCA ranking, evidence traceability, no unsupported claims, appropriate abstention behavior, acceptable latency (subjectively, for a live demo — not a formally derived target), and a successful human-review step.

**MVP failure conditions** — the system should be considered unsuccessful if it: cannot distinguish a primary alarm from a secondary/consequential one; routinely invents evidence (Ch.11 §11.31's hallucination testing); produces unsupported causes; cannot explain its own conclusions; fails ungracefully (rather than degrading per Ch.10 §10.6) when data is incomplete; cannot abstain under genuinely insufficient evidence; or has an architecture that cannot actually be validated by Chapter 9's own methodology at all.

## 12.38 Decision Gates

```
GATE 1   Problem Validated
GATE 2   Data Available
GATE 3   Evidence Pipeline Works
GATE 4   RCA Works
GATE 5   AI Adds Value (vs. the Ch.11 §11.22 baselines)
GATE 6   Explainability Works
GATE 7   Validation Passes (Ch.11's Phase A)
GATE 8   Demo Ready
```

Each gate requires the evidence the corresponding Part of this book already specifies — Gate 5, notably, requires the ablation comparison Chapter 11 §11.23 defines, not an assumption that adding AI automatically helped.

---

# Part IX — The Master Tables

## 12.39 Feature Prioritization Table

| Feature | User Value | Technical Difficulty | Data Requirement | Validation Difficulty | Risk | Differentiation Potential | Priority |
|---|---|---|---|---|---|---|---|
| Alarm correlation | High | Moderate | Low | Moderate | Low | Moderate | **Must Have** |
| Anomaly detection | High | Moderate | Moderate | Moderate | Low | Low (commodity capability) | **Must Have** |
| Fault isolation | High | Moderate | Low–moderate | Moderate | Low | Moderate | **Must Have** |
| Fault trees | High | Low | None (engineering-reasoned) | Low | Low | Moderate | **Must Have** |
| FMEA | High | Low | None | Low | Low | Moderate | **Must Have** |
| Bayesian reasoning | High | Moderate | Low (illustrative priors) | Moderate–high | Low | **High** | **Must Have** |
| RAG (curated) | High | Moderate | Low (small corpus) | Moderate | Moderate | **High** | **Must Have** |
| LLM (synthesis role) | High | Moderate | Low | Moderate | Moderate | Moderate | **Must Have** |
| Multi-agent | Uncertain (per Ch.11's ablation caution) | High | Moderate | High | Moderate–high | Uncertain | **Build Later** |
| Explainability | High | Moderate | Low | Moderate | Low | **High** | **Must Have** |
| Confidence | High | Moderate | Low | Moderate–high | Low | **High** | **Must Have** |
| Abstention | High | Low–moderate | Low | Moderate | Low | **High** | **Must Have** |
| Knowledge graph (full) | Moderate | High | High | High | Moderate | Low–moderate | **Build Later** |
| GNN | Uncertain at MVP scale | Very high | Very high | Very high | High | Moderate (real academic precedent) | **Research Only** |
| PINN | Uncertain at MVP scale | Very high | Very high | Very high | High | Moderate (real academic precedent) | **Research Only** |
| Digital twin | Uncertain at MVP scale | Very high | Very high | Very high | High | Moderate | **Research Only** |
| RUL/predictive maintenance | Low (wrong problem, §12.23) | Moderate–high | High | High | Low | Low (crowded category) | **Exclude** |
| Technician interface (minimal) | High | Low | None | Low | Low | Low (necessary, not differentiating) | **Must Have** |

## 12.40 Final MVP Stack

| Layer | Purpose | Why Included | Why Alternatives Rejected |
|---|---|---|---|
| **Data Layer** | Ingest telemetry/events for the demo scenarios | Nothing works without it | A full production data architecture (Ch.10 §10.15) is out of MVP scope |
| **Evidence Layer** | Structure raw data into the evidence-package format (Ch.6) | Direct foundation for correlation/RCA | Skipping straight to LLM-on-raw-data would forfeit groundedness (§12.34's build-order logic) |
| **Diagnostic Layer** | Alarm correlation + anomaly flagging | Chapter 4/6's differentiator foundation | — |
| **Knowledge Layer** | Fault trees, FMEA, Bayesian priors, curated RAG corpus | §12.19/§12.15's decisions | Full knowledge graph deferred (§12.18) |
| **AI Layer** | Single-orchestrator LLM with tool calling | §12.14/§12.16's decisions | Multi-agent deferred pending ablation evidence |
| **Explanation Layer** | Evidence trace, source citation, confidence/abstention | §12.20's decision | — |
| **Human Layer** | Minimal technician interface, explicit review/override | §12.10's decision | A full dashboard rejected as a distraction (§12.9) |

## 12.41 Final MVP Architecture Diagram

```
                    INCIDENT
                       ↓
              TELEMETRY + EVENTS
                       ↓
                DATA VALIDATION
                       ↓
               EVIDENCE EXTRACTION
                       ↓
              ALARM CORRELATION
                       ↓
              DIAGNOSTIC CONTEXT
                       ↓
          ┌────────────┴────────────┐
          ↓                         ↓
   ENGINEERING KNOWLEDGE          RAG
    FTA / FMEA / BAYES          (curated)
          └────────────┬────────────┘
                       ↓
                RCA ENGINE
                       ↓
              AI ORCHESTRATION
              (single orchestrator,
                 tool-calling)
                       ↓
          HYPOTHESIS EVALUATION
                       ↓
              EVIDENCE TRACE
                       ↓
           CONFIDENCE / ABSTAIN
                       ↓
              TECHNICIAN REVIEW
                       ↓
             VERIFIED OUTCOME
                       ↓
             MAINTENANCE RECORD

   ┌─────────────────────────────────────┐
   │   SAFETY CONTROL SYSTEM              │
   │   (fully independent — Ch.10 Part I; │
   │    no connection into the pipeline   │
   │    above, in either direction)       │
   └─────────────────────────────────────┘
```

## 12.42 The Build / Later / Research / Never Matrix

**The single most important table in this chapter.**

| Capability | BUILD NOW | BUILD LATER | RESEARCH ONLY | NEVER / OUT OF SCOPE | Reason |
|---|---|---|---|---|---|
| Telemetry/event ingestion | ✓ | | | | Foundational |
| Alarm correlation | ✓ | | | | §12.6, §12.19's differentiator |
| Signal processing (Ch.6 core) | ✓ | | | | Foundational |
| Anomaly detection | ✓ | | | | Trigger for the pipeline |
| Fault trees / FMEA | ✓ | | | | Data-independent, differentiator (§12.19) |
| Bayesian ranking | ✓ | | | | §12.5's core differentiator |
| RAG (curated corpus) | ✓ | | | | §12.15 |
| LLM (synthesis/explanation) | ✓ | | | | §12.14 |
| Tool calling | ✓ | | | | Keeps the LLM off deterministic work |
| Explainability / evidence trace | ✓ | | | | §12.19, core differentiator |
| Confidence | ✓ | | | | §12.5's identified strongest differentiator |
| Abstention | ✓ | | | | Same |
| Minimal technician interface | ✓ | | | | Without it, nothing else is usable |
| Multi-agent (beyond single orchestrator) | | ✓ | | | Pending ablation evidence (§12.16) |
| Full knowledge graph | | ✓ | | | Fault trees suffice for MVP (§12.18) |
| Broader RAG corpus with full provenance | | ✓ | | | Governance overhead not justified at MVP scale (§12.15) |
| Shadow-mode/pilot infrastructure | | ✓ | | | Requires real deployment context (Ch.10 §10.36) |
| Digital twin | | | ✓ | | Modeling effort exceeds hackathon scope (§12.17) |
| GNN | | | ✓ | | Training-data requirement exceeds hackathon scope (§12.17) |
| PINN | | | ✓ | | Physics-formulation effort exceeds hackathon scope (§12.17) |
| Cross-model/cross-fleet generalization | | | ✓ | | Genuinely open research question (Ch.9 §11.28) |
| Autonomous elevator/safety control | | | | ✓ | Categorically excluded by architecture (Ch.10 Part I) |
| Autonomous rescue/repair execution | | | | ✓ | Same |
| Universal fault diagnosis (all models) | | | | ✓ | Outside this book's own stated scope (Ch.1) |
| Fleet-wide digital twin | | | | ✓ | §12.17, at a scale never intended for this project |
| Fully autonomous maintenance | | | | ✓ | Contradicts the human-in-the-loop principle throughout |
| Generic chatbot (as the primary interface) | | | | ✓ | §12.22 |
| Predictive-maintenance dashboard | | | | ✓ | §12.23 — wrong problem, crowded category |
| RUL estimation | | | | ✓ | §12.23 |

## 12.43 Technical Decision Log

**Decision: RAG.** *Options considered:* fine-tuning, static KB, structured DB only, RAG. *Selected:* RAG, curated corpus, complementary to structured knowledge. *Why:* grounding + citation without a training corpus this project lacks (§12.15). *Evidence:* Ch.9 Part V. *Trade-off:* retrieval-quality risk (Ch.9 §9.19) accepted in exchange for auditability. *Risk:* poor retrieval degrading trust. *Revisit if:* corpus grows large enough to need full provenance infrastructure (→ Build Later).

**Decision: LLM role.** *Options:* general chatbot, full autonomous reasoner, scoped synthesis/explanation tool. *Selected:* scoped tool, never the source of computation or truth. *Why:* Ch.9 §9.11–§9.12's task-fit analysis. *Evidence:* Ch.9 Part III. *Trade-off:* less "impressive-sounding" than an autonomous agent narrative; more defensible. *Risk:* under-using LLM capability judges expect to see more of. *Revisit if:* never, on the core principle — the scope can grow, the principle shouldn't.

**Decision: Multi-agent.** *Options:* single orchestrator, 2-role split, full swarm. *Selected:* single orchestrator for MVP. *Why:* §12.16. *Evidence:* Ch.9 §9.24, Ch.11 §11.23. *Trade-off:* less architecturally elaborate to present. *Risk:* judges expecting a multi-agent showcase. *Revisit if:* ablation evidence (once buildable) shows a 2-role split earns its cost.

**Decision: Fault tree/FMEA as primary knowledge structure.** *Options:* full knowledge graph, relational DB, fault trees. *Selected:* fault trees/FMEA (already built, Ch.7). *Why:* zero additional data requirement, structural to the differentiator. *Evidence:* Ch.7 §7.7–§7.8. *Trade-off:* less flexible than a graph for genuinely complex, many-way relationships. *Risk:* becomes limiting at V1+ scale. *Revisit if:* relationship complexity genuinely outgrows tree structure.

**Decision: Bayesian reasoning.** *Options:* rule-based scoring only, ML-learned scoring, Bayesian. *Selected:* Bayesian, with illustrative priors. *Why:* §12.18, the mechanism behind the confidence differentiator. *Evidence:* Ch.7's full derivation. *Trade-off:* illustrative priors are not production-calibrated (Ch.7's own stated caveat, carried forward). *Risk:* judges challenging prior sourcing. *Revisit if:* real outcome data becomes available to calibrate against (Ch.11 §11.18).

**Decision: GNN.** *Options:* build, research-only. *Selected:* research-only. *Why:* §12.17. *Evidence:* Ch.9 Part II's real academic precedent, weighed against its own data requirement. *Trade-off:* forfeits a technically fashionable capability. *Risk:* none material to the MVP. *Revisit if:* real graph-structured fleet data becomes available.

**Decision: PINN.** Same structure as GNN, same conclusion, same §12.17 reasoning.

**Decision: Digital twin.** Same structure, same §12.17 reasoning; synthetic telemetry substitutes at MVP scale.

**Decision: Cloud/edge.** *Options:* cloud-only, edge-only, hybrid. *Selected:* not architecturally committed at MVP scale — a hackathon prototype runs wherever is convenient; Chapter 10 §10.16's hybrid reasoning governs the eventual production target, not this build. *Evidence:* Ch.10 §10.16. *Trade-off:* none material yet. *Risk:* none material yet. *Revisit if:* moving toward §12.26's V1+.

**Decision: Knowledge graph (full).** *Options:* build now, build later. *Selected:* build later. *Why:* §12.18. *Evidence:* Ch.10 §10.17. *Trade-off:* less flexible relationship modeling at MVP scale. *Risk:* none material to the MVP's demo scenarios. *Revisit if:* V1's expanded scope needs it.

**Decision: Confidence/abstention.** *Options:* omit (simpler demo), include. *Selected:* include, non-negotiably. *Why:* §12.5/§12.20 — this project's single strongest identified differentiator. *Evidence:* Ch.4 §6.14, Ch.9 §9.29–§9.31. *Trade-off:* added engineering complexity, accepted. *Risk:* calibration quality challenged by judges (a fair challenge — Ch.11 §11.18 names this an open limitation). *Revisit if:* never dropped; only refined.

## 12.44 Assumption Register

| Assumption | Why Needed | Risk if Wrong | How to Validate |
|---|---|---|---|
| Representative synthetic telemetry can be constructed | The MVP's entire evidence layer depends on it | Demo scenarios feel unrealistic to a domain-expert judge | Physics-grounding discipline (Ch.9 §11.25), expert review where feasible |
| The five demo fault scenarios can be built convincingly in available time | The whole demonstration strategy depends on it | Incomplete or rushed demo | §12.34's build order, §12.47's time-boxed plans |
| Existing engineering relationships (Ch.1, Ch.7) are sufficiently well-understood to support fault-tree construction | Fault trees are a Must-Have, data-independent asset | Trees miss real-world nuance | Expert/SME review where accessible |
| A small curated document set is sufficient to demonstrate RAG credibly | §12.15's scoping decision | Retrieval demo feels thin | Careful, deliberate document selection matched to the five scenarios |
| A single orchestrator can express every Must-Have capability without a true multi-agent split | §12.16's core architectural decision | Orchestrator becomes an unmanageable monolith | Clean tool-calling boundaries (Ch.9 §9.14) kept disciplined during implementation |

## 12.45 Dependency Map and Critical Path

```
DATA → EVIDENCE → RCA → RAG → LLM → EXPLANATION → HUMAN
```

If **DATA** breaks, nothing downstream has anything to reason over. If **EVIDENCE** (extraction/structuring) breaks, RCA has raw noise instead of structured input. If **RCA** breaks, RAG/LLM have nothing to explain. If **RAG** breaks, explanations lose citation grounding but the RCA ranking itself can still function (§12.15's complementary-knowledge-sources design means this is a partial, not total, failure). If **LLM** breaks, the system can still output the structured RCA result without natural-language synthesis — a degraded but non-catastrophic failure. If **EXPLANATION** breaks, the technician sees raw structured output instead of a synthesized narrative — usable, if less polished. If **HUMAN** review is skipped, Part I of Chapter 10 is violated entirely — this step is never optional.

**Critical path:** `Fault Scenario → Data → Evidence → RCA → Explanation → Validation` — the minimum chain that must work for this project to demonstrate *any* real value; everything else in §12.42's table is an enhancement to this chain, not a replacement for any link in it.

## 12.46 Non-Critical Features

Features removable under time pressure without destroying the central value proposition, in rough order of removability: a polished technician-interface visual design (function over form); the second and third demo scenarios beyond the flagship case (§12.47's compressed plans); RAG corpus breadth beyond the minimum needed for one convincing citation; any multi-agent exploration; any knowledge-graph work. **Never removable, under any time constraint:** the items in §12.48 below.

---

# Part X — Under Time Pressure

## 12.47 If We Have Only 4 Weeks / 2 Weeks / 3 Days

**Four weeks:** the full MVP as defined throughout this chapter — 3–5 scenarios, the complete Must-Have pipeline (§12.6), curated RAG, single-orchestrator LLM synthesis, full confidence/abstention behavior, validated per Chapter 9's Phase A methodology. Week 1: problem/data/evidence foundation. Week 2: RCA and fault-tree/Bayesian logic across the scenario set. Week 3: RAG, LLM synthesis, explanation. Week 4: confidence/abstention refinement, validation, demo polish.

**Two weeks:** compressed ruthlessly to one or two scenarios (the motor-overcurrent flagship case, plus the abstention case given its outsized demonstration value, §12.36), the core evidence→RCA→explanation pipeline, a minimal RAG corpus (perhaps three to five documents, just enough for one real citation), and confidence/abstention kept but simplified.

**Three days:** the absolute minimum, still preserving `EVIDENCE → RCA → EXPLANATION` intact. One scenario — the flagship motor-overcurrent case — with evidence largely pre-structured (less general-purpose extraction code, more scenario-specific preparation), a working RCA ranking (even if the "engine" is more narrowly scripted than fully general-purpose), a synthesized explanation, and — because Chapter 11 identifies it as the single most important capability to demonstrate live — **a second, minimal abstention-only case is prioritized over expanding the first case's polish**, even at three days' notice.

**No specific team size or programming language is assumed** in any of these three plans — the sequencing and priority order hold regardless of team composition.

## 12.48 What to Cut First, What Must Never Be Cut

**Cut, in this order, if time runs short:** (1) any multi-agent exploration; (2) knowledge-graph work; (3) RAG corpus breadth beyond the minimum; (4) demo scenarios beyond two (keep the flagship case and the abstention case); (5) technician-interface visual polish.

**Must never be cut, under any circumstance:** the evidence trace, RCA logic itself, source grounding, confidence/abstention, the human-review step, and the safety boundary (Ch.10 Part I) — removing any one of these doesn't shrink the demo, it removes the thing the demo exists to prove.

---

# Part XI — Anti-Patterns and the Narrative

## 12.49 Architecture and Strategic Anti-Patterns

**Architecture anti-patterns**, each a genuine risk this chapter's own decisions were built to avoid: an LLM-first architecture (deciding on the LLM before the reasoning it should support); AI without evidence grounding; a dashboard-first design; agent proliferation without ablation justification; RAG without provenance; confidence without calibration; a prediction presented as a diagnosis (§12.23's exact confusion); correlation presented as causation (Ch.6/Ch.7's repeated caution); safety-control coupling (Ch.10 Part I's cardinal sin); production claims drawn from prototype-stage data (Ch.9 §11.45); a giant architecture with no real validation plan (§12.24); a generic chatbot disguised as an RCA system (§12.22); synthetic data treated as production truth (Ch.9 §11.25); unsupported OEM comparison claims (Ch.4's evidence discipline); and technology-driven, rather than problem-driven, design generally — the single anti-pattern every other one on this list is, in some sense, an instance of.

**Strategic anti-patterns:** competing with OEMs head-on for connectivity/monitoring infrastructure they already have (§12.2's own boundary exists to prevent this); building another predictive-maintenance platform (§12.23); claiming universal diagnosis (§12.21); claiming autonomous maintenance (§12.21); overusing AI buzzwords without the substance this book's own research actually supports; and presenting every advanced technology surveyed in Chapter 9 as if it were mandatory for this project, rather than selectively and honestly scoped, exactly as Part IV of this chapter has done.

## 12.50 The Technical Storyline

```
PROBLEM → EVIDENCE → RCA GAP → ENGINEERING KNOWLEDGE
   → AI ASSISTANCE → EXPLAINABLE OUTPUT → HUMAN VERIFICATION
   → MEASURABLE VALUE (hypothesis, tested per Ch.11)
```

This is the backbone the final hackathon presentation should follow — and, not coincidentally, it is also the exact structure this entire ten-phase research book has followed, chapter by chapter, from Chapter 1's physical elevator through Chapter 11's validation methodology to this chapter's decisive synthesis.

## 12.51 One-Minute, Three-Minute, and Five-Minute Explanations

**One minute:** *"When an elevator alarm fires, a technician has to work out which of several possible causes actually produced it. KONE Elevate takes the alarm, the surrounding telemetry, and the relevant engineering knowledge, and produces a ranked list of likely causes with the specific evidence for each — not a single guess, and not a black box. If the evidence genuinely doesn't point clearly to one cause, it says so, instead of pretending to be certain. A technician reviews and verifies every conclusion before anything happens."*

**Three minutes (technical):** the one-minute version, extended with: the pipeline runs telemetry and event data through alarm correlation (separating a genuine primary fault from its consequential alarms), then weighs candidate causes using engineering fault trees and Bayesian evidence-updating, retrieves supporting documentation through RAG rather than relying on an LLM's unaided memory, and produces a structured, source-cited output with calibrated confidence — abstaining explicitly when evidence is insufficient. The system sits entirely outside the elevator's independent safety architecture; it observes and recommends, and a human technician verifies every conclusion before any maintenance action is taken.

**Five minutes (architecture walkthrough):** walking §12.41's diagram top to bottom — telemetry/events enter, get validated and structured into evidence, alarms get correlated into incidents (separating primary from consequential — the specific gap Chapter 4's competitive research identified as undemonstrated elsewhere), the RCA engine weighs hypotheses against both engineering knowledge and retrieved documentation, an LLM synthesizes the result into a readable, cited explanation, a confidence/abstention layer decides whether the evidence actually supports a conclusion, and a technician reviews and verifies before anything leaves the system — with the elevator's safety-control system shown, explicitly, as a fully separate box with no connection into any of it.

---

# Part XII — The Judge Attack Test

*Acting as an extremely skeptical senior KONE engineer.*

### Why Build This At All

**1. Why did you build this?** *Strongest:* KONE's own Technician Assistant and every major competitor's platform (Ch.4) demonstrate monitoring, dispatch, and general assistance — none publicly demonstrate structured, evidence-weighted, confidence-calibrated RCA. *Evidence:* Ch.4 §6.14. *Assumption:* the competitive research is current and complete as of when it was conducted. *Weak answer to avoid:* "because AI is powerful."

**2. Why not just use rules?** *Strongest:* rules remain core (fault trees, §12.19) — the question is what rules alone *can't* do: weigh multiple simultaneously plausible causes against continuous evidence and report honest uncertainty. *Evidence:* Ch.7's Bayesian derivation. *Weak answer:* dismissing rules rather than precisely scoping them.

**3. Why not predictive maintenance?** *Strongest:* prediction and diagnosis are different problems (§12.23); this project deliberately occupies the less-crowded, less-demonstrated one. *Evidence:* Ch.3–4. *Weak answer:* implying predictive maintenance is unimportant rather than simply out of this project's chosen scope.

**4. Why not use KONE's existing tools?** *Strongest:* this project doesn't have access to KONE's actual systems or proprietary data (Ch.9 §11.24) — it's a research-stage demonstration of a capability gap, not a replacement for or integration with anything KONE currently runs. *Evidence:* — *Weak answer:* implying any real integration has occurred.

### Why Each Technology

**5. Why do you need an LLM?** Ch.9 §9.1's task-scoped answer — language synthesis and explanation, never computation. **6. Why do you need agents?** You don't, for the MVP (§12.16) — single orchestrator, tool-calling. **7. Why do you need RAG?** Groundedness and citation without a training corpus this project lacks (§12.15). **8. Why do you need a digital twin?** You don't — research-only (§12.17). **9. Why do you need a GNN?** You don't — research-only, real precedent exists but the data requirement doesn't fit this scope (§12.17). **10. Why do you need Bayesian reasoning?** Because it's the specific mechanism behind the project's strongest identified differentiator (§12.5, §12.18). **11. Why do you need explainability?** Because a correct-but-unauditable answer doesn't deliver this project's actual value proposition (Ch.9 §9.28, Ch.11 §11.17).

### Why KONE, Why This Way

**12. Why should KONE build this?** *Strongest:* if the identified gap (Ch.4) is real, this is a specific, evidenced, narrowly-scoped capability worth evaluating — stated as a hypothesis for KONE to test, not a guaranteed win. *Weak answer:* overpromising business value not yet validated (Ch.9 §11.43).

**13. What happens if you're wrong about the gap?** Then this project has still produced a rigorous, well-documented RCA methodology and a working demonstration of evidence-driven diagnostic reasoning — independently useful groundwork, even if the specific competitive gap turns out to be narrower than Chapter 4's public research suggested.

**14. What can you actually demonstrate?** Feasibility of the reasoning pipeline on 3–5 representative, synthetic scenarios (Ch.11 §11.45) — precisely, and no more.

**15. What can you not demonstrate?** Production accuracy, fleet-scale performance, real KONE data compatibility, or safety certification — the full list in Chapter 11 §11.45 and this chapter's §12.21, held firmly.

### Rapid-Fire (16–50)

**16.** Why not fine-tune instead of RAG? — Data scarcity (§12.15). **17.** Why is your confidence trustworthy? — It isn't yet, fully — calibration against real outcomes is an open item (Ch.11 §11.18), honestly flagged. **18.** What if your fault trees are wrong? — Then RCA quality degrades proportionally; they're engineering-reasoned, not KONE-verified (Ch.7's standing label). **19.** What if two technicians disagree with your ranking? — Expected and handled — disagreement is surfaced, not hidden (Ch.9 §9.33). **20.** How is this different from a search engine over manuals? — Structured, evidence-weighted ranking with confidence, not document lookup (§12.22). **21.** What's your biggest technical risk? — Confidence calibration without labeled production data (Ch.9 §11.60 Q60, carried forward). **22.** What's your biggest business risk? — That the identified gap closes before this reaches a stage where it matters (a real, named risk, not previously stated this plainly). **23.** Why five scenarios and not fifty? — Time-boxing and demonstration clarity (§12.36); fifty would be a benchmark, not a demo (Ch.11 §11.34). **24.** Isn't multi-agent the industry trend? — Trend-following isn't the standard this project applies (§12.16); ablation evidence is. **25.** Why not just make the LLM bigger/smarter? — Doesn't fix a groundedness or calibration problem; those are architectural, not model-scale, issues (Ch.9 §9.11). **26.** What if KONE already has something like this internally? — Not publicly established either way (Ch.4's own evidence discipline); this project's claims are scoped to what's publicly demonstrated. **27.** How long would production deployment actually take? — Not estimated here — genuinely unknown without real KONE engagement (Ch.10 §10.35's maturity ladder, no timeline attached). **28.** What's your data source for the demo? — Synthetic, physics-grounded, explicitly labeled (§12.35, Ch.9 §11.25). **29.** Could a competitor build this in a weekend too? — The individual techniques are not secret; the specific combination and the evidence-discipline this book applies throughout is the actual contribution, not any single novel algorithm. **30.** Why should a judge trust your confidence numbers in the demo? — They shouldn't treat them as production-calibrated; the demo shows the *mechanism*, not a validated number (Ch.11 §11.18's honest limitation). **31.** What happens if the demo breaks live? — It should fail gracefully and visibly, itself demonstrating the design philosophy (Ch.9 §11.42). **32.** Why not build the interface first, since that's what judges see? — Because it's the least differentiating layer (§12.9's quadrant) — building it first would optimize for the wrong thing. **33.** Isn't fault-tree construction just as subjective as an LLM guessing? — No — it's traceable, auditable engineering reasoning with stated assumptions, distinct from opaque model generation (Ch.7's evidence discipline). **34.** What's stopping this from just being a fancy flowchart? — The Bayesian evidence-weighting and LLM-assisted synthesis genuinely add value a static flowchart can't provide — but a flowchart-plus-good-engineering-knowledge is, honestly, most of the value even before AI is added (§12.19). **35.** Why does abstention matter more than accuracy? — It doesn't "matter more" — it's what makes reported accuracy trustworthy at all (Ch.11 §11.19). **36.** How do you know your MVP scope is actually minimal? — Every item in it traces to a Must-Have in §12.6's table, each independently justified; nothing is included by default. **37.** What's the weakest part of your architecture? — Data scarcity's downstream effect on genuine calibration (repeated honestly, deliberately, across this chapter). **38.** Why trust fault trees you built yourselves over KONE's actual failure data? — You shouldn't, unconditionally — they're a starting point explicitly labeled as engineering-reasoned, not a claim of KONE-verified accuracy (Ch.7). **39.** What would make you abandon this approach entirely? — Evidence, from a real pilot (Ch.9 §11.46), that the identified competitive gap doesn't translate into measurable diagnostic value once tested against real data. **40.** Isn't "evidence-driven RCA" just RCA? — The "evidence-driven" qualifier specifically means auditable, source-cited, confidence-calibrated — properties Chapter 4's research found unclaimed publicly elsewhere, not a redundant label. **41.** What's the single hardest engineering problem you haven't solved? — Calibration without production outcome data (consistent, deliberately, with Q17/Q21/Q37). **42.** Why not partner with KONE instead of building independently? — A fair strategic question, explicitly deferred to Phase 11's competitive-strategy chapter rather than answered prematurely here. **43.** How do you avoid this becoming shelfware? — By keeping the MVP narrow and genuinely demonstrable (§12.1) rather than broad and impressive-sounding but unvalidated (§12.24). **44.** What's your plan if RAG retrieval is poor during the demo? — Graceful degradation to the fault-tree/Bayesian path alone, which functions independently (§12.45's dependency map). **45.** Isn't this just what every AI hackathon project claims? — The specific, falsifiable claim here — the exact competitive gap named in Ch.4 — is checkable against public sources, unlike a generic "we use AI" pitch. **46.** What did you deliberately choose not to build, and why? — §12.21 and §12.42's full exclusion list, each with a stated reason, ready to recite. **47.** How would you know if this project failed? — Chapter 9 §11.45's MVP failure conditions, verbatim. **48.** What's the single most impressive thing about this system? — Not any one technology — the discipline of the evidence trail end to end (§12.50's storyline). **49.** What's the single most important thing you'd want a judge to remember? — That it can say "I don't know" — and does, live, in the demo (§12.36). **50.** If you had to defend one sentence about this whole project, what would it be? — §12.55's final MVP statement, below.

---

# Part XIII — Final Scope and Statements

## 12.53 Final Decision Scorecard

*Qualitative, not numerical — numbers here would be arbitrary given this project's current evidence base.*

| Dimension | Rating | Basis |
|---|---|---|
| Technical value | High (for the specific, evidenced gap) | Ch.4 §6.14 |
| Feasibility (MVP scope) | High | §12.6–§12.20's disciplined scoping |
| Data availability | Low–moderate, honestly | Ch.9 §11.24, addressed via synthetic/curated data |
| Validation feasibility (MVP scope) | Moderate | Ch.11's Phase A methodology, achievable at this scale |
| Safety | High confidence in the architectural boundary | Ch.10 Part I |
| Cybersecurity | Appropriately scoped for a prototype, not production-hardened | Ch.10 Part II |
| Complexity | Deliberately Intermediate, not Advanced | §12.30 |
| Scalability | Not yet demonstrated | Genuinely deferred to V1+/production (§12.26) |
| Explainability | High | Ch.9 Part VI, §12.19 |
| Differentiation | Potential, evidenced but not yet field-validated | Ch.4, §12.25 |
| Hackathon demonstrability | High | §12.35–§12.36 |

## 12.54 Final Project Scope

**KONE Elevate WILL:** correlate related alarms into a single incident; generate and rank multiple root-cause hypotheses against real, structured evidence; ground its explanations in retrieved documentation and engineering knowledge; report calibrated, honestly-abstaining confidence; and require human verification before any conclusion is acted on.

**KONE Elevate MAY:** eventually incorporate a minimal multi-agent split, a richer knowledge-graph layer, or broader document retrieval — each contingent on the specific evidence §12.42/§12.43 specify, never assumed.

**KONE Elevate WILL NOT:** control an elevator, touch its safety architecture in any way, perform autonomous rescue or repair, claim universal or fleet-wide diagnostic accuracy, or claim any form of safety certification.

**KONE Elevate COULD BECOME:** a validated, pilot-stage diagnostic-support tool integrated into a real KONE service workflow — a genuinely possible future, honestly distant from this project's current, hackathon-stage evidence.

The scope remains centered on **AUTONOMOUS FAULT ISOLATION + ROOT CAUSE ANALYSIS**, deliberately, and does not expand into adjacent elevator technology this book has consciously scoped out at every turn.

## 12.55 THE KONE ELEVATE MVP

- **Problem:** technicians lack a structured, evidence-weighted, auditable way to narrow multiple plausible fault causes to a ranked, confidence-scored short list.
- **User:** the field technician mid-investigation.
- **Inputs:** the triggering alarm(s), an event chronology, a focused telemetry slice, operating state, component metadata, fault-tree/FMEA knowledge, and available maintenance-history excerpts.
- **Processing:** data validation → evidence extraction → alarm correlation → hypothesis generation and Bayesian ranking against fault-tree/FMEA knowledge and RAG-retrieved documentation.
- **Knowledge:** engineering-reasoned fault trees and FMEA (Ch.7), a small curated document corpus (RAG).
- **AI:** a single LLM orchestrator, tool-calling only, no direct computation or safety-relevant authority.
- **Output:** primary abnormality, affected subsystem, ranked root-cause hypotheses with supporting and contradicting evidence, calibrated confidence, and a recommended verification step.
- **Human role:** mandatory review and verification before any maintenance action; full authority to override.
- **Safety boundary:** fully independent of the elevator's safety-control system, architecturally, with no path in either direction (Ch.10 Part I).
- **Validation:** Chapter 11's Phase A (synthetic/offline) methodology, against the tiered ground truth and layered metrics that chapter defines.
- **Demonstration:** the five scenarios of §12.36, including the deliberate abstention case, walked through §12.51's five-minute architecture narrative.

**This is specific enough for a technical team to begin implementation from directly** — every field above resolves to a specific chapter's already-completed design, not a placeholder awaiting further research.

## 12.56 "Build This" and "Do Not Build This"

> **"If we had to build only one version of KONE Elevate, it would be: a single-orchestrator, tool-calling AI layer that correlates alarms, ranks root-cause hypotheses using engineering fault trees, FMEA, and Bayesian evidence-weighting, grounds its explanations in a small curated RAG corpus, reports calibrated and honestly abstaining confidence, and requires a human technician's verification before anything else happens — demonstrated across five carefully chosen scenarios, one of which exists specifically to show the system admitting it doesn't know."**

> **"To preserve technical credibility, safety, and validation feasibility, KONE Elevate should deliberately avoid: any control path into the elevator or its safety systems; a sprawling multi-agent architecture built before ablation evidence justifies it; a digital twin, GNN, or PINN before the data and modeling effort each genuinely requires is available; a generic chatbot standing in for structured diagnostic reasoning; another predictive-maintenance platform competing where OEMs are already strong; and any claim — of accuracy, of generalization, of safety, or of business value — this project's own evidence does not yet support."**

---

# What We Now Know to Build

The actual problem: a specific, evidenced gap in publicly-demonstrated elevator diagnostic capability — structured, auditable, confidence-calibrated RCA — not a general claim that elevator diagnostics are broken. The primary user: the field technician, mid-investigation. The core capability: evidence-weighted root-cause ranking with calibrated, abstention-capable confidence — everything else in this project supports that one capability rather than competing with it for attention. The required data: synthetic and curated, honestly labeled as such, sufficient for feasibility demonstration and nothing beyond it. The required engineering knowledge: fault trees and FMEA, built through reasoning rather than requiring training data — a genuine asset available from day one. The required RCA logic: Bayesian evidence-weighting over that engineering knowledge. The required AI: a scoped, tool-calling LLM orchestrator — synthesis and explanation, never computation or authority. The required RAG: a small, curated corpus, complementary to structured knowledge, not a replacement for it. The required explainability: a full evidence trace, source-cited, checkable claim by claim. The required confidence/abstention behavior: present, honest, and explicitly demonstrated failing gracefully — the single capability this chapter refuses to compromise on under any time constraint. The required human role: mandatory review, full override authority, at every step. The safety boundary: architecturally absolute, inherited whole from Chapter 10. The validation boundary: feasibility-level, honestly bounded, per Chapter 11. The MVP: precisely defined in §12.55. The future roadmap: staged, evidence-gated, never assumed. The explicit exclusions: named, repeatedly, throughout this chapter, and held to.

> **"The strength of KONE Elevate is not the number of AI technologies it contains. Its strength is the quality of the diagnostic reasoning it demonstrates."**

Technically: every decision in this chapter — deferring multi-agent architecture, excluding GNNs and digital twins, keeping the interface minimal, refusing to inflate the demo scenario count — was made in service of exactly this sentence. A system with ten AI components and shallow, unvalidated reasoning behind each one is a weaker demonstration than a system with three well-chosen components and a reasoning process that can withstand the Judge Attack Test in Part XII, claim by claim. This chapter chose the second kind, deliberately, at every decision point above.

---

# Bridge to Phase 11 — Competitive Differentiation, Strategic Positioning, Innovation & KONE Value

The next phase must move from **"what should we build?"** to **"why should KONE care, and how can we defensibly differentiate this from what already exists?"**

Phase 11 must deeply synthesize KONE's existing capabilities against Otis ONE, Schindler Ahead, TK Elevator MAX, and the broader emerging-agentic-AI landscape (Ch.4, revisited and extended); predictive maintenance, remote monitoring, and technician assistance as established categories this project deliberately does not compete in (§12.23); diagnostic intelligence and RCA specifically as the contested-but-undemonstrated ground this project claims (§12.25); competitive gaps and this project's actual defensibility; strategic value to KONE, to customers, to technicians, and to the service organization; a genuine innovation narrative; intellectual-property considerations; scalability and real adoption barriers; organizational fit; the build/buy/partner question explicitly deferred in this chapter's Q42; what KONE already publicly does, versus what remains genuinely not established; and, finally, what KONE Elevate can credibly claim once every one of those questions has been honestly answered.

Phase 11 content is not generated here — this document ends at the close of Phase 10.
