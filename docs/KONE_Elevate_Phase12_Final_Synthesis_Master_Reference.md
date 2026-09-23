# PHASE 12 — FINAL RESEARCH SYNTHESIS, HACKATHON READINESS, MASTER ARCHITECTURE, CLAIMS, JUDGE PREPARATION & TEAM RESEARCH DIVISION

### *KONE Elevate — Autonomous Fault Isolation & Root Cause Analysis: Master Research Book*

## How to Read This Chapter

This is the final chapter. It does not restart research — it synthesizes Phases 1–11 (the Project Understanding Report plus Chapters 1–13) into one authoritative master reference. Every claim below is classified: **FACT** (directly established, cited to its source chapter), **INFERENCE** (engineering reasoning from established facts), **PROPOSAL** (this project's own design), **ASSUMPTION** (something this project's plan depends on but hasn't verified), **UNKNOWN** (genuinely not established — never treated as "absent," per this book's standing principle). No new claim is introduced here merely because it sounds technically reasonable.

**A reader who reads only this chapter should come away understanding**: what the project is, why it exists, how elevators work, how faults manifest, how KONE's ecosystem relates to it, how competitors approach digital maintenance, how RCA works, how the AI system works, how data flows, how the reasoning works, how safety is preserved, how cybersecurity is addressed, how the system is validated, what the MVP is, what is and isn't novel, what can and can't be claimed, and how to defend the project before KONE engineers and hackathon judges.

---

# Part I — What KONE Elevate Is

## 14.1 Final Project Definition

- **Project name:** KONE Elevate — Autonomous Fault Isolation & Root Cause Analysis.
- **Category:** an evidence-driven, auditable diagnostic-support layer for elevator maintenance — not a monitoring platform, not a predictive-maintenance platform, not a general-purpose chatbot (Ch.12 §12.22–§12.23).
- **Core problem:** the gap between an elevator alarm firing and a technician holding a verified, evidence-weighed understanding of its cause (Ch.13 §13.9).
- **Primary user:** the field technician mid-investigation (Ch.12 §12.10).
- **Secondary users:** remote diagnostic specialists, maintenance planners (Ch.12 §12.10).
- **Operational context:** a connected, modern gearless traction elevator (Ch.1's stated scope), generating telemetry, events, and alarms already collected by existing connected-elevator infrastructure (Ch.3).
- **Technical objective:** correlate alarms, weigh evidence against engineering knowledge and retrieved documentation, and rank root-cause hypotheses with calibrated, abstention-capable confidence (Ch.7, Ch.9).
- **Business objective:** test whether this reduces diagnostic friction and effort — a hypothesis, not a claim (Ch.9 §11.43, Ch.13 §13.21).
- **Safety objective:** remain architecturally, permanently outside the elevator's independent safety-control loop (Ch.10 Part I).
- **Core capability:** evidence-weighted root-cause ranking with calibrated confidence (Ch.12 §12.5).
- **System boundary:** observes, analyzes, recommends; a human verifies before any maintenance action (Ch.10 §10.38).
- **Out-of-scope boundary:** elevator/safety control, autonomous rescue or repair, universal cross-model diagnosis, fleet-wide digital twin, predictive maintenance as a category, and any safety-certification claim (Ch.12 §12.21).

**Nine explanation depths, kept mutually consistent:**

1. **One sentence:** *KONE Elevate turns a correlated cluster of elevator alarms into a ranked, evidence-cited set of probable root causes, with calibrated confidence and human verification built in.*
2. **30 seconds:** adds — *it grounds every conclusion in real telemetry, engineering fault trees, and retrieved documentation, and says plainly when the evidence isn't enough to be sure.*
3. **1 minute:** Ch.12 §12.51's one-minute explanation, verbatim.
4. **3 minutes:** Ch.12 §12.51's three-minute explanation, verbatim.
5. **5 minutes, technical:** Ch.12 §12.51's five-minute architecture walkthrough, verbatim.
6. **Executive:** *A research-stage proposal investigating a specific, evidence-documented gap in publicly available elevator-diagnostic capability — worth evaluating against KONE's own internal tools, which may already address some or all of it.*
7. **Engineer-to-engineer:** *A Bayesian evidence-weighting layer over structured fault trees/FMEA and RAG-retrieved documentation, orchestrated by a scoped, tool-calling LLM, with confidence calibration and selective abstention, sitting entirely outside the elevator's independent safety-control loop.*
8. **Technician-oriented:** Ch.12 §12.55's problem/user framing, restated conversationally: *"Instead of starting cold on a fault code, you get a ranked short list of likely causes with the evidence already pulled together — and it tells you straight when it isn't sure."*
9. **Judge-oriented:** Ch.13 §13.29's defensible positioning statement, verbatim.

## 14.2 Final Problem Statement

**Why the problem is not merely "elevators generate too many alarms":** fault detection is not diagnosis (an anomaly flag says *something* changed, not *why*); diagnosis is not RCA (a probable-cause guess is not the same as a ranked, evidence-weighed, alternative-eliminated conclusion, Ch.13 §13.11); a fault code may not identify the physical root cause (Ch.2's alarm taxonomy shows one code can map to many mechanisms, Ch.7 §7.7's fault trees formalize this); multiple alarms can represent one underlying fault (Ch.4/Ch.6's cascade and primary/consequential-alarm findings); intermittent faults are genuinely hard (Ch.9 §11.11's own admission this is the hardest scenario category); temporal relationships matter (Ch.6 §8.4's chronology discipline); sensor evidence must be interpreted in context, since the sensor itself can fail (Ch.7 §7.34, Ch.9 §11.7's sensor-failure scenarios); historical maintenance information matters because a repeat repair reveals a prior misdiagnosis (Ch.5 §5.16); technicians need evidence, not merely another alert (Ch.13 §13.19's diagnostic-friction framing); and confidence/uncertainty matter because a system that always answers, regardless of evidence strength, is less trustworthy than one that can say it doesn't know (Ch.9 §9.31).

**Five forms of the final problem statement:**

- **Technical:** *Given telemetry, event, alarm, and maintenance-history evidence for an elevator incident, produce an auditable, confidence-scored root-cause recommendation for human review, distinguishing primary from consequential alarms and eliminating evidence-inconsistent alternative hypotheses.*
- **Operational:** *Reduce the manual evidence-gathering and hypothesis-narrowing burden currently borne entirely by the technician during an investigation.*
- **Technician:** *Give me the ranked likely causes and the evidence for each, before I start guessing.*
- **Business:** *Test whether structured, auditable diagnostic reasoning measurably reduces diagnostic effort without claiming to replace technician judgment.*
- **Hackathon:** *Demonstrate, on representative scenarios, that evidence-driven RCA is feasible, auditable, and honest about its own uncertainty — a capability no OEM researched in this book publicly demonstrates today (Ch.13 §13.9).*

---

# Part II — How It Works, End to End

## 14.3 The Complete End-to-End System Story

```
 1. Physical degradation      → a component begins to wear/drift (Ch.1)
 2. Sensor change             → a monitored signal shifts (Ch.6)
 3. Telemetry generation      → continuous readings reflect the change
 4. Event generation          → a discrete state change is logged
 5. Alarm generation          → a threshold is crossed (Ch.4)
 6. Alarm cascade             → the primary alarm triggers secondary ones (Ch.4 §4.6)
 7. Signal processing         → filtering, feature extraction (Ch.6)
 8. Anomaly detection         → the abnormality is flagged
 9. Evidence aggregation      → telemetry+events+alarms+history become one package (Ch.6 §8.30)
10. Hypothesis generation     → candidate causes proposed (Ch.7 §7.15)
11. Fault-tree/FMEA/Bayesian/
    causal reasoning          → hypotheses weighed against structured knowledge (Ch.7)
12. Alternative-cause testing → negative evidence downgrades inconsistent hypotheses (Ch.13 §13.16)
13. Historical evidence
    retrieval                 → maintenance-history context pulled in (Ch.5 §5.16)
14. Engineering knowledge
    retrieval (RAG)           → documentation retrieved and cited (Ch.9 §9.17)
15. Tool calls                → deterministic calculations performed outside the LLM (Ch.9 §9.14)
16. Agent coordination        → (single orchestrator for the MVP, Ch.12 §12.16)
17. Confidence calculation    → calibrated, evidence-strength-dependent (Ch.9 §9.29)
18. Explanation generation    → a faithful narrative grounded in the evidence trace (Ch.9 Part VI)
19. Technician review         → the mandatory human checkpoint (Ch.10 Part I)
20. Recommended investigation
    /action                   → a specific next verification step
21. Repair                    → performed by the technician, never the system
22. Verification              → confirms (or contradicts) the RCA conclusion
23. Learning/knowledge
    feedback                  → the verified outcome informs future cases (Ch.10 §10.27)
```

**Computationally**, steps 7–18 are this project's actual contribution; **operationally**, steps 1–6 and 19–23 are the existing maintenance world this project inserts itself into narrowly, never replaces (Ch.13 §13.20's value-chain framing).

## 14.4 Three Full Worked Examples

| Field | A — Motor/Drive Fault | B — Door Fault | C — Encoder/Position Fault |
|---|---|---|---|
| **Observed symptoms** | Elevated motor current during travel | Repeated door reopening, no visible obstruction | Leveling deviation, rough stops |
| **Telemetry** | Phase current trending up; drive temperature nominal | Door cycle time increasing; photo-eye event pattern erratic | Encoder position vs. commanded position diverging |
| **Alarms** | Overcurrent (primary); drive trip (consequential) | Door obstruction/timeout (recurring) | Leveling deviation, encoder fault |
| **Temporal sequence** | Current rises over several trips before trip event (Ch.2 §2.5) | Cycle-time drift over many cycles, not a single event (Ch.4 §4.9) | Gradual divergence, not a step change (Ch.7 §7.34) |
| **Candidate causes** | Brake drag; mechanical obstruction; motor winding fault; drive/IGBT fault (Ch.7 §7.7.1) | Genuine obstruction; photo-eye degradation; mechanical resistance (Ch.4 §4.9) | Encoder signal degradation; genuine traction/rope issue; leveling-sensor fault (Ch.7 §7.34) |
| **Supporting evidence** | Current-brake-timing correlation across trips | Multi-cycle instability, no consistent physical location | Divergence unconfirmed by an independent leveling sensor |
| **Contradicting/negative evidence** | Clean drive self-test rules out drive-side fault (§13.16) | Consistent-location pattern would argue for genuine obstruction instead — absent here | If the independent sensor *also* drifts, this argues for real motion, not encoder fault (Ch.7 §7.34) |
| **Primary fault** | Brake drag (mechanical) | Photo-eye degradation | Encoder signal degradation |
| **Consequential alarms** | Drive trip | — | Leveling deviation alarm |
| **Eliminated alternatives** | Motor winding fault (no phase imbalance at light load) | Genuine obstruction (no consistent location) | Genuine traction issue (independent sensor doesn't corroborate) |
| **Final RCA** | Mechanical (brake) ranked above electrical | Sensor degradation ranked above mechanical/obstruction | Encoder fault ranked above traction issue |
| **Confidence** | Moderate–high (multiple correlated signals) | Moderate (pattern-based, no single decisive signal) | Moderate (contingent on independent-sensor cross-check quality) |
| **Abstention condition** | Would abstain if brake-timing data were missing | Would abstain if fewer than several cycles were available to establish the pattern | Would abstain if no independent leveling signal existed to cross-check |
| **Technician verification** | Physical brake inspection | Photo-eye cleaning/alignment check | Encoder connector/alignment inspection |
| **Recommended next diagnostic step** | Check brake release timing directly | Observe several more door cycles for pattern confirmation | Cross-check against an independent position reference |
| **Expected corrective action** | Brake adjustment/replacement | Photo-eye cleaning, realignment, or replacement | Encoder cleaning, reseating, or replacement |
| **Post-repair verification** | Current returns to baseline across subsequent trips | Cycle time and reopening rate return to baseline | Position tracking matches independent reference again |

---

# Part III — The Master Architecture

## 14.5 Master Architecture

*32 components, condensed. "AI required?" and "LLM appropriate?" columns directly resolve Ch.12 Part IV's technology decisions.*

| # | Component | Responsibility | Deterministic/Probabilistic | AI Required? | LLM Appropriate? | Safety Note | MVP or Future |
|---|---|---|---|---|---|---|---|
| 1 | Elevator/physical system | Ground truth source | — | No | No | Outside this system entirely (Ch.10 Part I) | N/A |
| 2 | Sensors | Raw signal generation | Deterministic (hardware) | No | No | — | N/A |
| 3 | Edge/controller interface | Signal access point | Deterministic | No | No | — | MVP |
| 4 | Telemetry ingestion | Continuous data intake | Deterministic | No | No | — | MVP |
| 5 | Event/alarm ingestion | Discrete data intake | Deterministic | No | No | — | MVP |
| 6 | Time synchronization | Chronology integrity | Deterministic | No | No | Prevents false causal ordering (Ch.6 §8.4) | MVP |
| 7 | Data quality layer | Validity checks | Deterministic | No | No | — | MVP |
| 8 | Signal processing | Filtering, denoising | Deterministic | No | No | — | MVP |
| 9 | Feature extraction | Structured features from raw signal | Deterministic/statistical | Optional (ML) | No | — | MVP |
| 10 | Anomaly detection | Flags abnormal behavior | Probabilistic (statistical/ML) | Yes (lightweight) | No | — | MVP |
| 11 | Alarm correlation | Groups related alarms | Rule-based + probabilistic | Optional | No | — | MVP — core differentiator |
| 12 | Evidence construction | Assembles the evidence package | Deterministic | No | No | — | MVP |
| 13 | Engineering knowledge base | Fault trees, FMEA | Deterministic (authored) | No | No | — | MVP — core differentiator |
| 14 | Fault ontology/taxonomy | Naming/classification structure | Deterministic | No | No | — | MVP |
| 15 | Fault tree/FMEA knowledge | Structured causal knowledge | Deterministic | No | No | — | MVP |
| 16 | Historical maintenance knowledge | Prior case context | Deterministic retrieval | No | No | — | MVP (small scale) |
| 17 | RAG layer | Retrieves documentation | Deterministic retrieval + semantic ranking | Yes (embeddings) | No (retrieval itself) | — | MVP — curated corpus (Ch.12 §12.15) |
| 18 | Diagnostic reasoning engine | RCA logic | Probabilistic (Bayesian) | Yes | No | — | MVP — core differentiator |
| 19 | Bayesian/probabilistic reasoning | Evidence-weighted ranking | Probabilistic | Yes | No | — | MVP — core differentiator |
| 20 | AI reasoning layer (LLM) | Synthesis, explanation | — | Yes | **Yes, scoped** | Never computation/authority (Ch.10 Part VI) | MVP |
| 21 | Tool layer | Deterministic calculations callable by the LLM | Deterministic | No | No (called by LLM) | — | MVP |
| 22 | Multi-agent orchestration | Task decomposition across agents | — | Optional | Optional | — | **Build Later** (Ch.12 §12.16) |
| 23 | Alternative-cause elimination | Downgrades inconsistent hypotheses | Deterministic/probabilistic | Yes | No | — | MVP — core differentiator |
| 24 | Confidence estimation | Calibrated score | Probabilistic | Yes | No | — | MVP — core differentiator |
| 25 | Abstention mechanism | Withholds a conclusion when evidence is weak | Deterministic rule over confidence | No | No | — | MVP — core differentiator |
| 26 | Explainability/evidence trace | Full auditability | Deterministic | No | No | — | MVP — core differentiator |
| 27 | Technician interface | Presents the output | — | No | No | — | MVP, minimal (Ch.12 §12.20) |
| 28 | Human approval | Verification/override | — | No | No | **Mandatory, permanent (Ch.10 Part I)** | MVP |
| 29 | Corrective-action support | Suggests next steps only | Deterministic | No | No | Never issues instructions to act on the elevator itself | MVP |
| 30 | Verification | Confirms outcome | — | No | No | Human-performed | MVP |
| 31 | Audit logging | Full trace persistence | Deterministic | No | No | — | MVP |
| 32 | Feedback/knowledge update | Closes the loop | Deterministic + periodic | No | No | — | Future (Ch.10 §10.27) |

## 14.6 Master Data Flow and the Investigation Object Schema

```
Investigation ID → elevator identity → timestamp window → triggering event
   → raw telemetry → normalized signals → alarms → correlated events
   → extracted features → anomalies → candidate faults → evidence items
   → hypotheses → reasoning steps → retrieved documents → tool results
   → eliminated hypotheses → selected root cause → confidence → explanation
   → recommended action → human decision → repair outcome → verification result
```

**Conceptual schema fields** (Ch.10 §10.18's common data model, restated as a single investigation record): `investigation_id`, `elevator_id`, `time_window`, `evidence[]` (each item: `source`, `timestamp`, `value`, `provenance`), `hypotheses[]` (each: `cause`, `supporting_evidence[]`, `contradicting_evidence[]`, `status: active|eliminated`), `confidence_score`, `abstained: bool`, `explanation_text`, `retrieved_documents[]` (with `version`, `citation`), `recommended_action`, `human_decision`, `repair_outcome`, `verification_result`. **Every field traces back to Ch.9 §9.18's lineage chain and Ch.10 §10.37's reproducibility requirement** — this schema is not new; it is those two chapters' principles made concrete as a record structure.

## 14.7 Master Reasoning Loop

```
OBSERVE → NORMALIZE → CORRELATE → DETECT → GENERATE HYPOTHESES
   → TEST HYPOTHESES → ELIMINATE ALTERNATIVES → RANK CAUSES
   → CHECK CONFIDENCE → EXPLAIN → ABSTAIN OR ESCALATE
   → HUMAN VERIFY → ACT → VERIFY OUTCOME
```

| Step | Requires | Method | Output | Failure Mode | Feeds |
|---|---|---|---|---|---|
| Observe | Raw sensor/event stream | Ingestion (Ch.6) | Raw evidence | Missing/corrupted data | Normalize |
| Normalize | Raw evidence | Validation, unit/time alignment | Clean evidence | Silent bad-data acceptance | Correlate |
| Correlate | Clean evidence | Alarm-cascade logic (Ch.4 §4.6) | Grouped incident | Unrelated alarms merged | Detect |
| Detect | Grouped incident | Anomaly detection (Ch.6) | Flagged abnormality | False pos/neg | Generate Hypotheses |
| Generate Hypotheses | Flagged abnormality + fault trees | Ch.7 §7.15's method | Candidate causes | Incomplete hypothesis space | Test Hypotheses |
| Test Hypotheses | Candidates + evidence | Bayesian weighting (Ch.7) | Evidence-scored hypotheses | Correlated-evidence double-counting (Ch.7 §7.16) | Eliminate Alternatives |
| Eliminate Alternatives | Scored hypotheses | Negative-evidence check (§13.16) | Reduced hypothesis set | Failing to check for contradicting evidence | Rank Causes |
| Rank Causes | Reduced set | Ranking | Ordered list | Ignoring correlated evidence (repeat of the above) | Check Confidence |
| Check Confidence | Ranked list | Calibration (Ch.9 §9.29) | Confidence score | Miscalibration | Explain |
| Explain | Ranking + confidence + trace | LLM synthesis, grounded (Ch.9) | Technician-facing narrative | Unfaithful explanation | Abstain or Escalate |
| Abstain or Escalate | Confidence | Threshold rule | Proceed or withhold | Failing to abstain when warranted | Human Verify |
| Human Verify | Full output | Technician review (Ch.10 Part I) | Approved/overridden conclusion | Automation bias (Ch.9 §11.38) | Act |
| Act | Approved conclusion | Human-performed repair | Physical change | — | Verify Outcome |
| Verify Outcome | Repair result | Confirmation | Verified/contradicted RCA | Repeat fault | Feedback loop |

**The Detection → Classification → Fault Isolation → Diagnosis → RCA → Recommendation distinction, one final time, in one table:**

| Step | Question Answered |
|---|---|
| Detection | *Is something abnormal happening?* |
| Classification | *What type of fault is this?* |
| Fault Isolation | *Which subsystem is involved?* |
| Diagnosis | *What is probably wrong?* |
| RCA | *Why did it happen?* |
| Recommendation | *What should be checked?* |

## 14.8 Final AI/GenAI/Agent Role Resolution

| Function | Technology | Why |
|---|---|---|
| Signal filtering, thresholds, event ordering | Deterministic code | No judgment required (Ch.9 §9.44) |
| Anomaly flagging | Statistical/lightweight ML | Pattern detection at scale (Ch.6) |
| Hypothesis ranking | Bayesian/probabilistic reasoning | Calibrated evidence-weighting (Ch.7) |
| Document interpretation, synthesis, explanation | LLM, tool-calling only | Language task, not computation (Ch.12 §12.14) |
| Documentation retrieval | RAG | Grounding without fine-tuning (Ch.12 §12.15) |
| Task orchestration | Single orchestrator (MVP) | Ablation evidence not yet available to justify multi-agent (Ch.12 §12.16) |
| Safety-relevant decisions, elevator/action control | **Human only** | Categorically excluded (Ch.10 Part I) |

**"Using an LLM" is not itself the innovation, and neither is "multi-agent architecture"** (Ch.13 §13.24) — the actual intelligence lies in structured evidence, engineering knowledge, temporal reasoning, causal reasoning, alternative-cause elimination, evidence provenance, uncertainty representation, and mandatory verification. **Minimum defensible AI architecture:** fault trees + Bayesian ranking + a single scoped LLM orchestrator with RAG and tool-calling (Ch.12 §12.41). **More advanced future architecture:** a justified multi-agent split, a full knowledge graph, richer causal models — each contingent on the specific evidence Ch.12 §12.43 already specifies before being adopted.

## 14.9 Final Explainability and Trust Model

**No hidden chain-of-thought is proposed.** The technician-facing `ExplainabilityTrace` shows: suspected fault, confidence, supporting evidence, contradicting evidence, temporal relationship, relevant alarms, eliminated alternatives, retrieved engineering references (with citation), a recommended next diagnostic step, and an explicit human-verification requirement — Ch.9 Part VI's design, restated as the final, canonical output contract. Provenance, source attribution, confidence, uncertainty, abstention, contradiction handling, human approval, and the audit trail are the eight properties that make this structure trustworthy, not any property of the underlying language model's fluency.

---

# Part IV — Safety and Cybersecurity (Final Boundaries)

## 14.10 Final Safety Boundary

**KONE Elevate is diagnostic/decision-support intelligence and must not directly replace certified elevator safety functions or safety-control logic** — the single sentence Chapter 10 built an entire Part around, restated here as this book's final word on the subject.

| AI MAY | AI MUST NOT |
|---|---|
| Observe telemetry, alarms, events | Control elevator movement, doors, or brakes |
| Analyze and correlate evidence | Override or bypass the safety chain |
| Generate and rank hypotheses | Make any safety-relevant decision |
| Recommend inspection/verification steps | Issue instructions treated as authoritative without human review |
| Report confidence and abstain | Claim certainty it hasn't earned |
| Explain its reasoning with citations | Hide or misrepresent its evidence trail |

Independent protection layers, PESSRAL's boundary on programmable electronics in safety functions (Ch.10 §10.4), fail-safe degradation (Ch.10 §10.6), mandatory human verification, deployment isolation from the safety-control zone (Ch.10 §10.13), and the explicit refusal to claim certification (Ch.10 §10.40) are inherited here in full, unmodified.

## 14.11 Final Cybersecurity Boundary

Identity/access management, least privilege, zero trust, encryption in transit and at rest, network segmentation (isolating the diagnostic zone from the safety-control zone), secure boot/firmware integrity, secure OTA updates, audit logging, and observability (Ch.10 Part II) govern the conventional attack surface. **The AI-specific surface** — RAG poisoning, prompt injection, tool misuse, data/knowledge-base poisoning, model manipulation — is addressed by treating all retrieved content as untrusted data (never instructions), scoping every tool to least privilege, and never granting any agent a capability resembling control (Ch.10 §10.22). **The unique risk an AI diagnostic layer adds, beyond conventional industrial cybersecurity:** a compromised knowledge base or a successful prompt injection can corrupt *reasoning* even when every conventional OT/IT control holds — which is exactly why RAG security and tool-permission scoping are treated as first-class cybersecurity concerns in this book, not an afterthought bolted onto a standard industrial-security checklist.

---

# Part V — Competitive Position and Differentiation

## 14.12 Final Competitive Position

| Capability Layer | KONE | Otis | Schindler | TK Elevator | KONE Elevate |
|---|---|---|---|---|---|
| 1. Connectivity | Confirmed | Confirmed | Confirmed | Confirmed | Assumed input |
| 2. Monitoring | Confirmed | Confirmed | Confirmed | Confirmed | Assumed input |
| 3. Alerting | Confirmed | Confirmed | Confirmed | Confirmed | Assumed input |
| 4. Prediction | Partially Evidenced | Partially Evidenced | Claimed | Claimed | Not proposed |
| 5. Anomaly Detection | Claimed | Claimed | Claimed | Claimed | Proposed |
| 6. Fault Classification | Claimed | Claimed | Claimed | Claimed | Proposed |
| 7. Fault Isolation | Claimed | Claimed | Claimed | Claimed | Proposed |
| 8. Diagnosis | Claimed | Claimed | Claimed (TOC) | Claimed (DOC) | Proposed |
| 9. Root Cause Analysis | **Not Publicly Established** | **Not Publicly Established** | **Not Publicly Established** | **Not Publicly Established** | **Proposed** |
| 10. Evidence-Grounded Investigation | Partially Evidenced | Not Publicly Established | Not Publicly Established | Partially Evidenced | **Proposed — core** |
| 11. Alternative-Cause Elimination | Not Publicly Established | Not Publicly Established | Not Publicly Established | Not Publicly Established | **Proposed — core** |
| 12. Explainable Diagnosis | Not Publicly Established | Not Publicly Established | Not Publicly Established | Not Publicly Established | **Proposed — core** |
| 13. Confidence-Aware Diagnosis | Not Publicly Established | Not Publicly Established | Not Publicly Established | Not Publicly Established | **Proposed — core** |
| 14. Human-Verified Autonomous Investigation | Implied | Implied | Implied (TOC) | Implied | **Explicit, architecturally mandatory** |

**Publicly established:** rows 1–8, broadly, across the whole industry. **Not publicly established anywhere researched:** rows 9–13 — this project's actual claimed territory. **What cannot be claimed:** that any competitor, KONE included, lacks these capabilities internally — only that they are not publicly demonstrated (Ch.13 §13.3).

*Also carried forward from Chapter 13: KONE and TK Elevator announced an agreement to combine (April 29, 2026), pending regulatory approval, not expected to close before Q2 2027 — treated throughout this book as a pending, unclosed transaction, not a current fact about either company's capabilities (Ch.13 §13.4).*

## 14.13 Final Differentiation

| Candidate | Category |
|---|---|
| Evidence-linked RCA | **A — Genuinely differentiating** (per §14.12's row 9–10) |
| Primary-vs-consequential alarm reasoning | **A — Genuinely differentiating** |
| Alternative-cause elimination | **A — Genuinely differentiating** |
| Auditable evidence trace | **A — Genuinely differentiating** |
| Uncertainty-aware (confidence/abstention) reasoning | **A — Genuinely differentiating** |
| Engineering knowledge + telemetry fusion | **B — Useful but common** (plausibly already done internally, industry-wide, undocumented) |
| Technician-centered diagnostic workflow | **B — Useful but common**, overlapping with KONE's own Technician Assistant (Ch.13 §13.27) |
| Temporal reasoning | **C — Implementation detail**, necessary but not itself a headline claim |
| LLM usage | **D — Weak differentiator** (Ch.13 §13.24) |
| RAG usage | **D — Weak differentiator** |
| Multi-agent architecture | **E — Not a differentiator**, deferred for the MVP entirely (Ch.12 §12.16) |

**"If another company builds an LLM + RAG + multi-agent system tomorrow, what remains defensible?"** Domain knowledge (fault trees/FMEA, built without training data), the diagnostic workflow itself, the evidence data model, causal knowledge, the fault ontology, engineering rules, accumulated historical maintenance knowledge, the validation framework, technician integration, the feedback loop, and — over time, the hardest of all to replicate — verified outcome data (Ch.13 §13.23–§13.25).

## 14.14 Final KONE Value Proposition

```
Better evidence → better fault isolation → less diagnostic uncertainty
   → fewer unnecessary investigations → faster technician decisions
   → more consistent troubleshooting → better knowledge capture
   → improved maintenance outcomes
```

| Stakeholder | Value (mechanism-explained, not vague) |
|---|---|
| Technicians | Less manual evidence-hunting because the evidence package (Ch.6 §8.30) is pre-assembled; ranked hypotheses because Bayesian weighting (Ch.7) replaces unaided guessing |
| Customers/building owners | Potentially reduced downtime *if* faster, more accurate diagnosis reduces repeat visits — hypothesis, not proven (Ch.9 H1) |
| Maintenance operations | Better triage input from a structured RCA output rather than a raw alarm |
| Service managers | Structured case records support parts planning and technician allocation |
| Engineering teams | A structured, growing corpus of verified RCA cases (Ch.13 §13.23's data moat) |
| KONE digital ecosystem | A complementary layer to existing Connected Services/Technician Assistant, not a replacement (Ch.13 §13.27) |
| Reliability engineering | Fault-tree/FMEA structure doubles as a documentation and analysis asset independent of the AI layer |
| Future AI-enabled maintenance | A reasoning methodology that survives whichever specific AI stack the industry converges on next (Ch.13 §13.42) |

**Proven value:** none yet. **Expected value:** the mechanism chain above, engineering-reasoned. **Hypothesized value:** Ch.9's H1–H5. **Value requiring pilot validation:** all of it, honestly, per Ch.9's validation roadmap (§11.46) and Ch.10's maturity ladder (§10.35).

---

# Part VI — The MVP and Roadmap

## 14.15 Final MVP Definition

Ch.12 §12.55's MVP, restated as the canonical final spec: inputs (triggering alarm, event chronology, focused telemetry slice, operating state, component metadata, fault-tree/FMEA knowledge, available maintenance-history excerpt), processing (validation → evidence extraction → alarm correlation → Bayesian-ranked hypothesis generation against fault trees/FMEA and RAG-retrieved documentation), knowledge (engineering-reasoned fault trees/FMEA, a small curated document corpus), AI (single-orchestrator, tool-calling LLM, no computation/authority), output (primary abnormality, subsystem, ranked hypotheses with supporting/contradicting evidence, calibrated confidence, recommended verification), interface (minimal, non-dashboard), validation (Ch.9's Phase A, offline/synthetic), demo boundary (five scenarios, Ch.12 §12.36, including the deliberate abstention case).

**Must Build:** everything in Ch.12 §12.6's Must-Have column. **Should Build:** a broader curated corpus, a second/third demo scenario. **Could Build:** a minimal 2-role agent split, a lightweight knowledge-graph layer — contingent on ablation evidence. **Do Not Build:** digital twin, GNN, PINN, multi-agent beyond a single orchestrator, RUL/predictive maintenance, fleet-wide dashboard, anything resembling elevator/safety control (Ch.12 §12.21–§12.42).

## 14.16 MVP → Pilot → V1 → V2 → Production Roadmap

| Stage | Capabilities | Data | AI Maturity | Validation Maturity | Cybersecurity Maturity | Safety Assurance | Human Involvement |
|---|---|---|---|---|---|---|---|
| **MVP/Hackathon** | §14.15's spec | Synthetic/curated | Single orchestrator | Ch.9 Phase A (offline) | Basic hygiene | Architectural boundary only | Full review of every conclusion |
| **Pilot** | + expert-reviewed benchmark | Historical (where available) | Same, refined | Ch.9 Phase C | Ch.10 §10.11 basic posture | Same boundary, more scrutiny | Full review |
| **V1** | + broader RAG, possibly 2-role agents | Historical + expert-labeled | Possibly multi-agent, if justified | Ch.9 Phase D (shadow mode) | Improved | Same | Full review |
| **V2** | + knowledge graph if warranted | Richer/historical at scale | Refined | Ch.9 Phase E (human-reviewed pilot) | Approaching production posture | Same | Full review, reduced friction |
| **Production** | Full Ch.10 architecture | Fleet-scale, governed | Mature, monitored | Ch.9 Phase F | Full IEC 62443/ISO 8102-20 posture | Formal safety-case discipline (Ch.10 §10.30) | Full review, permanently (never removed) |

**What must be proven before progressing:** each stage's specific validation gate (Ch.9 §11.44, Ch.12 §12.38) — never assumed, always evidenced.

---

# Part VII — Validation and Scenarios

## 14.17 Final Validation Framework

*[Consolidating Ch.9 in full]* Ground truth is hard because the actual root cause is rarely rigorously confirmed in ordinary maintenance records (Ch.9 §11.3) — this book uses tiered ground truth (true/expert-labeled/inferred) and never treats them as equally reliable.

| Layer | Metric(s) |
|---|---|
| Anomaly detection | Precision, Recall, F1, Sensitivity, Specificity, FPR, FNR |
| Fault classification | Accuracy, macro-F1, weighted-F1, confusion matrix |
| Fault isolation | Top-1/Top-k accuracy |
| RCA | Root-cause Top-k, causal-chain correctness, alternative-elimination accuracy |
| Retrieval | Precision@k, Recall@k, MRR, NDCG |
| Explanation | Groundedness, citation correctness, completeness |
| Confidence | Brier score, Expected Calibration Error, reliability diagram |
| Abstention | Coverage, selective accuracy, risk-coverage curve |
| Human usefulness | Time-to-diagnosis (jointly with correctness), technician agreement, override rate |

**Hackathon-relevant metrics:** feasibility on representative scenarios, groundedness, abstention behavior, evidence traceability — qualitative and demonstrable within the available time. **Production-relevant metrics:** the full calibration and generalization suite above, requiring real outcome data this project doesn't have (Ch.9 §11.24, §11.28).

## 14.18 Final Fault Scenario Library

*Consolidated from Ch.9 §11.6–§11.8, in one table.*

| Scenario | Primary Fault | Discriminating Evidence | Validation Difficulty |
|---|---|---|---|
| Motor overcurrent (mechanical) | Brake drag/obstruction | Current-brake-timing correlation | Moderate |
| Motor overcurrent (electrical) | Winding fault | Phase imbalance at light load | Moderate |
| Drive fault | IGBT/inverter | Failed self-test | Moderate |
| Overheating | Thermal degradation (motor/drive) | Gradual trend independent of duty cycle | High |
| Brake-related | Drag/timing anomaly | Brake-release-timing sensor deviation | Moderate |
| Traction-related | Rope/sheave wear | Independent-sensor agreement pattern | High |
| Door obstruction | Physical blockage | Consistent location | Low |
| Door motor issue | Mechanical resistance | Elevated current + longer cycle time | Low–moderate |
| Door sensor issue | Photo-eye degradation | Multi-cycle instability, no location | High |
| Encoder issue | Signal degradation | Independent leveling-sensor disagreement | High |
| Positioning issue | Leveling deviation | Position-vs-commanded divergence | Moderate |
| Communication fault | Bus/gateway issue | Widespread, non-physical-pattern data gaps | High |
| Sensor fault | Stuck/drift/noise | Zero variance / statistical noise-floor | Moderate |
| Intermittent fault | Marginal connector, etc. | Historical/event-log pattern only | Very high |
| Alarm cascade | One root, many alarms | Primary/consequential separation | Moderate |
| Multi-fault | Two independent causes | Distinct, non-overlapping evidence clusters | High |

## 14.19 Final Demonstration Design

**Five scenarios (Ch.9 §11.40, Ch.12 §12.36):** (1) motor overcurrent — flagship differential diagnosis; (2) door degradation — pattern-based ambiguity resolution; (3) encoder/position — independent-sensor cross-check; (4) alarm cascade — primary/consequential separation; (5) insufficient/conflicting evidence — **the abstention case, the single most important demonstration in this entire project.**

**5-minute demo script:** intro/problem (30s) → Case 1 live walkthrough, evidence→RCA→explanation (2 min) → Case 4, cascade reasoning (1 min) → Case 5, abstention (1 min) → close (30s). **10-minute demo script:** the same five cases, each given roughly 1.5–2 minutes, with the architecture diagram (§14.39) shown once at the start and referenced, not re-explained, at each case.

---

# Part VIII — Claim Discipline

## 14.20 Final Claim & Evidence Registry

| Claim | Status | Safe Wording | Unsafe Wording | Judge May Challenge |
|---|---|---|---|---|
| A specific RCA gap exists publicly | **GREEN** | "not publicly established across every OEM researched" | "no one else does this" | Research completeness (Ch.13 §13.39 Q64) |
| RCA improves diagnostic time | **YELLOW** | "a hypothesis this project is designed to test" | "reduces diagnostic time" | Ch.9 §11.43's H1 |
| Explainability is demonstrated | **GREEN** | "the prototype exposes a full evidence trace" | "fully explainable AI" | Faithfulness (Ch.9 §11.17) |
| Confidence is calibrated | **YELLOW** | "designed for calibration; not yet validated against real outcomes" | "our confidence is accurate" | Ch.9 §11.18's open limitation |
| Works across elevator models | **RED** | "scoped to a modern gearless traction elevator" | "works across models" | Ch.1's stated scope |
| Autonomous diagnosis | **RED** | (no safe version exists) | "autonomous diagnosis" | Ch.10 Part I |
| Production-ready | **RED** | "a hackathon-stage research prototype" | "production-ready" | Ch.9 §11.45 |
| Safety-certified | **RED** | "explicitly not claimed" | "safety-certified" | Ch.10 §10.40 |
| Competitors lack this | **RED** | "not publicly demonstrated" | "no competitor has this" | Ch.13 §13.3 |
| KONE lacks this | **RED** | "not publicly established in KONE's materials" | "KONE doesn't have RCA" | Ch.13 §13.3 |

## 14.21 What We Know / Infer / Propose / Cannot Claim

| WHAT WE KNOW | WHAT WE INFER | WHAT WE PROPOSE | WHAT WE CANNOT CLAIM |
|---|---|---|---|
| KONE has a GenAI Technician Assistant (Bedrock/Claude), scaling toward 40,000 technicians (Ch.13 §13.5) | Competitors likely perform some internal RCA, undocumented (Ch.13 §13.3) | Evidence-driven, ranked, confidence-calibrated RCA with abstention (Ch.7, Ch.9) | Competitors or KONE lack this capability |
| TK Elevator has publicly announced Azure-based agentic AI (Ch.13 §13.8) | The specific mechanism behind TKE's "operational playbooks" likely differs from structured multi-hypothesis RCA, but this isn't confirmed | A single-orchestrator, tool-calling architecture for the MVP (Ch.12 §12.16) | That multi-agent architecture is unnecessary in general — only that it's unproven for this MVP |
| KONE and TKE announced an agreement to combine, not yet closed (Ch.13 §13.4) | The combination, if closed, would give KONE two AI platforms to potentially integrate | This project's methodology is relevant regardless of the M&A outcome (Ch.13 §13.40) | That the deal will close, or on what terms |
| Data on real elevator faults is scarce industry-wide (Ch.9 §11.24) | Synthetic/curated data is a necessary, imperfect substitute at this stage | Physics-grounded synthetic scenarios (Ch.9 §11.25) | That synthetic validation equals production validation |
| PESSRAL/IEC 61508 govern safety-related programmable electronics (Ch.10 §10.4) | This project's AI layer sits outside that governed scope by design | An architecturally independent diagnostic layer | Any safety certification or SIL rating |

## 14.22 Final Assumption & Risk Register

| Risk | Likelihood | Impact | Mitigation | Residual Risk | Validation Method |
|---|---|---|---|---|---|
| Limited real elevator data | High | High | Synthetic/curated data, honestly labeled | Moderate | Ch.9's tiered ground truth |
| Synthetic data unrealistic | Moderate | Moderate | Physics-grounding (Ch.9 §11.25) | Moderate | Expert review where feasible |
| Model hallucination | Moderate (without mitigation) | High | Tool-calling, RAG, structured outputs (Ch.9 §9.35) | Low, with mitigations | Faithfulness testing (Ch.9 §11.16) |
| False confidence | Moderate | High | Calibration testing, abstention (Ch.9 §9.29–§9.31) | Moderate, honestly open | ECE/Brier score |
| Prompt injection / RAG poisoning | Low (with controls) | Moderate | Source validation, data-as-data discipline (Ch.10 §10.22) | Low | Adversarial testing (Ch.9 §11.30) |
| Safety-boundary confusion | Very low | High if it occurred | Architectural exclusion (Ch.10 Part I) | Very low | Design review |
| Overclaiming competitor capabilities | Moderate (without discipline) | High (credibility) | §14.20's claim registry | Low, if discipline held | Judge Q&A (§14.26) |
| Prototype-to-production gap | Certain, by design | N/A — expected | Explicit staging (§14.16) | N/A | Honest scoping |
| Technician trust/automation bias | Real, human-factors risk | Moderate–high | Evidence visibility, honest confidence (Ch.9 §11.38) | **Moderate — the least architecturally-solvable risk in this book** | Human-subject study (Ch.9 §11.37) |

## 14.23 Final Technical Decision Log

*Consolidated from Ch.12 §12.43, restated as the final, canonical version.*

| Decision | Reason | Alternative Considered | Why Rejected |
|---|---|---|---|
| RCA, not only prediction | §14.12's identified gap | Predictive-maintenance platform | Crowded category, wrong problem (Ch.13 §13.12) |
| Evidence-first | Auditability is the core differentiator | Opaque model output | Fails this project's own value proposition |
| Telemetry + engineering knowledge fusion | Neither alone suffices | Telemetry-only or knowledge-only | Weaker evidence base |
| RAG | Grounding without a training corpus | Fine-tuning | Data scarcity (Ch.9 §11.24) |
| Scoped LLM | Synthesis/explanation only | General-purpose chatbot | §14.24 |
| Single orchestrator (not multi-agent) | Complexity must earn its cost | Multi-agent swarm | No ablation evidence yet (Ch.12 §12.16) |
| Deterministic rules for computation | Reliability, auditability | LLM-computed values | Ch.9 §9.44 |
| Bayesian reasoning | Calibrated confidence, no training data needed | Rule-based scoring only | Weaker uncertainty representation |
| Anomaly detection | Necessary trigger | Skip straight to RCA | Nothing to reason about without it |
| Confidence + abstention | This project's strongest identified differentiator | Always-answer design | §14.12's gap |
| Human in the loop | Non-negotiable | Any autonomous-action design | Ch.10 Part I |
| No elevator/safety control | Categorical exclusion | — | Ch.10 Part I |
| Not a generic chatbot | §14.24 | — | — |
| Not another predictive-maintenance platform | Ch.13 §13.12 | — | — |
| No reliance entirely on the LLM | Ch.9 §9.44's determinism split | — | — |
| No autonomous-maintenance claim | Ch.10 §10.40 | — | — |

## 14.24 Final "What Not to Build" List

Generic chatbot (structured reasoning, not conversation, is the point, §14.13); direct safety control; autonomous physical intervention; unsupported real-time elevator control claims; unnecessary digital-twin complexity (Ch.12 §12.17); unnecessary multi-agent complexity (Ch.12 §12.16); over-engineered ML beyond what the MVP's scenarios need; fake precision (invented percentages, thresholds, or sample sizes anywhere in this book); unsupported proprietary-KONE-integration claims; unsupported production-readiness claims; and treating synthetic data as if it were real field data — each excluded for a reason this book has stated, repeatedly, at every phase it came up.

---

# Part IX — The Pitch

## 14.25 Final Technical Storyline for Judges

Elevator systems are complex, with many interacting subsystems (Ch.1). Failures create multiple observations across telemetry, events, and alarms (Ch.2, Ch.6). Existing connected systems already generate enormous evidence (Ch.3). Detection and prediction are valuable but don't automatically solve diagnostic reasoning (§14.12's gap). Technicians still have to determine what actually caused the event. KONE Elevate converts fragmented evidence into an auditable investigation: it correlates alarms and telemetry, generates and tests competing hypotheses, eliminates alternatives using evidence, retrieves engineering knowledge, produces an evidence-linked RCA, communicates uncertainty honestly, and can abstain. A technician verifies the result. The verified outcome feeds future knowledge. **Nothing in this storyline claims more than the preceding thirteen chapters actually support.**

## 14.26 100+ Judge Questions — Master Defense Bank

*Curated from the 300+ questions already built across Chapters 9–13; organized by the roadmap's own 41 categories, each answer kept to one line and cross-referenced to its full treatment.*

**A. Problem definition:** *Why does this problem matter?* → §14.2. *Isn't this just "too many alarms"?* → §14.2's opening rebuttal.
**B. Elevator engineering:** *Why does a fault code not equal a root cause?* → §14.2, Ch.2. *What's your scope?* → A modern gearless traction elevator (Ch.1).
**C. KONE ecosystem:** *What does KONE's connected fleet already provide?* → §14.5's row 1–8 equivalent, Ch.3.
**D. 24/7 Connected Services:** *Doesn't this already do diagnostics?* → §14.12's row-by-row answer, Ch.13 §13.5.
**E. Technician Assistant/GenAI:** *What's new versus KONE's own tool?* → Ch.13 §13.27, §13.40's dedicated defense.
**F. Competitors, general:** *Aren't competitors ahead?* → §14.12's matrix; TKE's agentic AI is the strongest case, addressed directly (Ch.13 §13.40).
**G. Otis ONE:** *Doesn't Otis do this?* → No public GenAI technician tool found (Ch.13 §13.6) — Ch.13 §13.40's Otis script.
**H. Schindler Ahead:** *Doesn't Schindler's TOC do this?* → Mechanism not publicly described (Ch.13 §13.7) — Ch.13 §13.40's Schindler script.
**I. TK Elevator MAX:** *Doesn't TKE's agentic AI already provide probable causes?* → Ch.13 §13.40's TKE script, in full.
**J. Agentic AI:** *Isn't agentic AI the same thing?* → No — Ch.13 §13.40's "agentic AI generally" script.
**K. RCA:** *How do you know it's really RCA and not classification?* → §14.7's six-step distinction table.
**L. Fault trees:** *Are your fault trees KONE-verified?* → No, engineering-reasoned (Ch.7 §7.7) — stated honestly, always.
**M. FMEA:** *Where do your severity/occurrence scores come from?* → Illustrative, stated as such (Ch.7 §7.8).
**N. Bayesian reasoning:** *Where do your priors come from?* → Illustrative, engineering-reasoned, never fabricated production statistics (Ch.7, Ch.12 §12.43).
**O. Alarm correlation:** *How do you separate primary from consequential?* → §14.4's worked examples, Ch.4 §4.5–§4.6.
**P. Signal processing:** *What's your feature set?* → Ch.6's core methods, scenario-scoped for the MVP (Ch.12 §12.14).
**Q. Anomaly detection:** *What's your false-positive rate?* → Not yet measured at production scale — honestly (Ch.9 §11.12).
**R. Data scarcity:** *Where's your real data?* → None — synthetic/curated, always labeled as such (Ch.9 §11.24–§11.25).
**S. Synthetic data:** *Is it realistic?* → Physics-grounded, not claimed production-representative (Ch.9 §11.25).
**T. AI/ML:** *Why ML at all?* → Anomaly detection specifically (§14.8's table).
**U. LLMs:** *Why an LLM?* → Synthesis/explanation only, never computation (§14.8).
**V. RAG:** *Why RAG?* → Grounding without a training corpus (Ch.12 §12.15).
**W. Multi-agent:** *Why not multi-agent?* → Not yet justified by ablation evidence (Ch.12 §12.16).
**X. Explainability:** *Is your explanation faithful?* → Tested via claim-by-claim groundedness auditing (Ch.9 §11.16–§11.17, §11.32).
**Y. Confidence:** *Is your confidence trustworthy?* → Not yet fully calibrated against real outcomes — an open, named limitation (Ch.9 §11.18).
**Z. Abstention:** *Can it really say "I don't know"?* → Yes — demonstrated live as Case 5 (§14.19).
**AA. Safety:** *Can it control the elevator?* → Never — architecturally excluded (§14.10).
**AB. Cybersecurity:** *What's your attack surface?* → §14.11's full answer.
**AC. Validation:** *How do you prove any of this?* → §14.17's full metric suite, honestly bounded to feasibility-level for the prototype.
**AD. MVP:** *What can you actually demonstrate?* → §14.15, §14.19's five scenarios.
**AE. Scalability:** *Does this work at fleet scale?* → Not demonstrated; genuinely open (Ch.12 §12.33).
**AF. Deployment:** *How would this reach production?* → §14.16's staged roadmap.
**AG. Business value:** *What's the ROI?* → Not calculated — no fabricated baseline (Ch.9 §11.43, §14.14).
**AH. Innovation:** *What's genuinely new?* → §14.13's Category-A list.
**AI. IP/defensibility:** *What's your moat?* → Data and workflow integration, not the technology (Ch.13 §13.23–§13.25).
**AJ. "KONE already does this":** → §14.26's dedicated defense pattern (below) and Ch.13 §13.40.
**AK. "Why not existing KONE tools?":** → Complements, doesn't replace (Ch.13 §13.27); this project has no access to KONE's actual tools to extend directly.
**AL. "Why not a simpler rules engine?":** → Rules remain core (fault trees); the gap is in evidence-weighing multiple simultaneously plausible causes (Ch.12 §12.52 Q2).
**AM. "Why do you need AI?":** → Task-scoped answer, §14.8 — not all of it is "AI" in the LLM sense; much is deterministic or classical statistics.
**AN. "Why do you need agents?":** → You don't, for the MVP (§14.8, Ch.12 §12.16).
**AO. "Why should KONE care?":** → §14's closing paragraph (§14.38), in full.

**Especially prepared, per the source instruction's explicit list — each answered fully above and cross-referenced:** "KONE already has predictive maintenance" → §14.12 row 4 + Ch.13 §13.12. "KONE already has Technician Assistant" → E, above. "Otis/Schindler/TK already have connected platforms" → G/H/I, above. "Isn't this just ChatGPT over maintenance manuals?" → V + Ch.12 §12.22's chatbot-vs-diagnostic-intelligence distinction. "Why can't a rules engine do this?" → AL, above. "Why do you need multiple agents?" → AN, above. "Where is your real elevator data?" → R, above. "How can you claim RCA without ground truth?" → Ch.9 §11.3's tiered framework — we don't claim certainty, we claim a tested methodology. "Can your AI make the elevator unsafe?" → AA, above — no. "What happens when the AI is wrong?" → Human verification catches it (§14.10); the failure mode is wasted time, never a safety event. "How do you know the AI is confident?" → Y, above — honestly, not fully yet. "What happens when there is an unseen fault?" → Abstention, or a low-ranked, clearly-uncertain hypothesis set (Ch.9 §11.28's rare-fault discussion). "What is actually autonomous?" → Nothing, by design (§14.10). "What is actually novel?" → §14.13's Category A.

## 14.27 Final Judge Attack Test

*A simulated skeptical KONE-engineer panel.*

**On novelty:** *"Every piece of this exists elsewhere — what's actually new?"* → The specific combination (fault-tree-grounded, Bayesian-ranked, alternative-cause-eliminating, confidence-calibrated, abstention-capable RCA) is not publicly demonstrated as a combination anywhere this book's research found (§14.12). **Vulnerability:** this claim rests on research completeness this book cannot guarantee (Ch.13 §13.39 Q64) — **improvement:** direct verification with KONE SMEs before any external claim.

**On feasibility:** *"Can this actually be built in hackathon time?"* → Yes, at the MVP scope defined in §14.15, with the compressed 3-day/2-week/4-week plans already specified (Ch.12 §12.47). **Vulnerability:** none major, if the scope discipline (§14.24) holds.

**On elevator engineering:** *"Do you actually understand elevators, or just AI?"* → §14.4's worked examples and the full fault-tree/FMEA structure (Ch.7) are the evidence. **Vulnerability:** none of it is KONE-verified — **improvement:** SME review, explicitly invited rather than assumed unnecessary.

**On data:** *"You have no real data — how seriously should we take any of this?"* → Honestly, this is the project's single biggest limitation, named without hedging (Ch.9 §11.60 Q70). **Vulnerability:** genuinely real — **improvement:** the strongest possible fix is exactly what this project cannot self-provide: real KONE data access.

**On safety:** *"What if a technician trusts a wrong AI conclusion?"* → Automation bias, named as the least architecturally-solvable risk in this entire book (§14.22) — mitigated by design, never claimed eliminated. **Vulnerability:** real, human-factors, not fully solved by any architecture. **Improvement:** UI/process design, training — both genuinely outside a hackathon prototype's ability to validate.

**On AI:** *"Isn't the LLM just going to hallucinate?"* → Mitigated by tool-calling, RAG, structured outputs, and abstention as the last line of defense (Ch.9 §9.35) — not eliminated. **Vulnerability:** none of these mitigations have been stress-tested at scale yet.

**On deployment:** *"This is nowhere near production."* → Correctly identified — this project has never claimed otherwise (§14.16, §14.20).

**On validation:** *"How do you know your metrics mean anything?"* → They're measured against tiered, honestly-labeled ground truth (§14.17) — the ceiling on any claim is exactly as high as the ground-truth tier supporting it, never higher.

**On competitors:** *"What if TK Elevator's system already does exactly this?"* → Not disprovable from outside (Ch.13 §13.39 Q63) — the honest response is that this project's value would then lie in its independent methodology and validation discipline, not in having found an unclaimed gap.

**On business value:** *"Why should KONE spend money on this?"* → It shouldn't, yet — this is a hypothesis worth cheap evaluation, not a funded commitment (§14.14, honestly).

**Remaining vulnerabilities, named directly:** research completeness (competitive claims could be incomplete), zero real-world validation, confidence calibration not yet tested against real outcomes, and automation bias not fully solvable by architecture alone. **None of these are hidden anywhere in this book** — each has been named, repeatedly, at the point it first became relevant.

## 14.28 Final Pitches

**30 seconds:** *"Elevator alarms tell you something's wrong. They don't tell you why. KONE Elevate correlates the alarms, weighs the evidence, ranks the likely causes, and says plainly when it isn't sure — with a technician verifying every conclusion."*

**1 minute:** Ch.12 §12.51's one-minute version, verbatim.

**3 minutes:** the 1-minute version, plus: the technical mechanism (alarm correlation, Bayesian ranking against fault trees, RAG-grounded explanation), the specific competitive gap (§14.12), and the honest validation boundary (feasibility-demonstrated, not production-proven).

**5 minutes:** the 3-minute version, plus a live transition directly into the demo (§14.19), walking the architecture diagram (§14.39) once before Case 1 begins.

## 14.29 Final One-Page Executive Brief

**Project:** KONE Elevate — Autonomous Fault Isolation & RCA. **Problem:** the gap between an alarm and a verified understanding of its cause (§14.2). **Users:** field technicians, primarily. **Solution:** evidence-driven, Bayesian-ranked RCA with calibrated abstention. **Architecture:** fault trees/FMEA + RAG + a scoped LLM orchestrator, entirely outside the elevator's safety-control loop (§14.5, §14.10). **Differentiation:** primary/consequential alarm separation, alternative-cause elimination, auditable evidence, calibrated confidence — not publicly demonstrated elsewhere in the industry (§14.12). **Value:** a hypothesis (faster, more consistent diagnosis) worth testing, not a proven outcome (§14.14). **MVP:** five demonstrable scenarios, including a deliberate abstention case (§14.19). **Validation:** offline/synthetic feasibility, honestly bounded (§14.17). **Safety boundary:** architecturally permanent, never claimed certified (§14.10). **Competitive position:** the specific RCA-depth gap is real across every OEM researched, KONE included (§14.12) — and KONE and TK Elevator have a pending, unclosed combination worth being aware of (§14.21). **Future roadmap:** staged, evidence-gated, from hackathon prototype to a genuinely validated pilot (§14.16).

---

# Part X — Reference Materials

## 14.30 Final Glossary

**Fault** — an underlying abnormal condition. **Failure** — the loss of a required function. **Symptom** — an observable sign of a fault. **Event** — a discrete logged occurrence. **Alarm** — an event crossing a defined threshold. **Warning** — a lower-severity alarm. **Trip** — a protective shutdown. **Fault code** — a system-assigned label, not necessarily the root cause (§14.2). **Telemetry** — continuous sensor data. **Anomaly** — a statistically or physically abnormal pattern. **Detection** — noticing an anomaly. **Classification** — assigning a fault type. **Fault isolation** — identifying the affected subsystem. **Diagnosis** — identifying the probable cause. **RCA** — establishing *why* a fault occurred, with evidence. **Causal reasoning** — inferring cause-effect relationships. **FTA** — Fault Tree Analysis. **FMEA** — Failure Mode and Effects Analysis. **FMECA** — FMEA with criticality analysis added. **Bayesian inference** — probability updating given evidence. **Alarm correlation** — grouping related alarms. **Temporal correlation** — relating events by time, correctly ordered. **Signal processing** — extracting usable information from raw sensor data. **Feature engineering** — constructing informative variables from raw data. **RAG** — Retrieval-Augmented Generation. **LLM** — Large Language Model. **Tool calling** — an LLM invoking external deterministic functions. **Agent** — a reasoning unit with a defined role. **Multi-agent** — multiple coordinating agents. **Digital twin** — a high-fidelity virtual replica of a physical system. **Knowledge graph** — a structured, relationship-based knowledge representation. **Explainability** — the ability to show why a conclusion was reached. **Confidence** — a stated degree of certainty. **Calibration** — whether stated confidence matches actual accuracy. **Uncertainty** — the degree to which a conclusion is not fully supported. **Abstention** — declining to conclude when evidence is insufficient. **HITL** — Human-in-the-Loop. **PESSRAL** — Programmable Electronic Systems in Safety-Related Applications for Lifts. **Edge computing** — processing near the physical asset. **Cloud computing** — centralized, remote processing. **CMMS** — Computerized Maintenance Management System. **EAM** — Enterprise Asset Management. **Predictive maintenance** — forecasting future failure risk (distinct from RCA, §14.2). **Condition monitoring** — ongoing tracking of equipment health.

## 14.31 Master Knowledge Map

| Chapter(s) | Established | Depended On By | Enabled Decision |
|---|---|---|---|
| 1–3 (Phase 1) | Elevator physics, subsystems, failure modes, sensor dictionary | Every later chapter | The whole book's physical grounding |
| 4 (Phase 2) | Fault codes, alarm cascades, diagnostic hypothesis space | Ch.6 (correlation), Ch.7 (fault trees) | The primary/consequential distinction |
| 5 (Phase 3) | KONE ecosystem, Technician Assistant | Ch.13 (competitive analysis) | "Complement, not replace" positioning |
| 6 (Phase 4) | Otis/Schindler/TKE landscape | Ch.13 | The identified competitive gap |
| 7 (Phase 5) | RCA methodology, fault trees, FMEA, Bayesian reasoning | Ch.9, Ch.12 | The core reasoning engine's design |
| 8 (Phase 6) | Signal processing, anomaly detection, alarm correlation algorithms | Ch.7, Ch.9 | The evidence-construction pipeline |
| 9 (Phase 7) | AI/GenAI/RAG/multi-agent, explainability | Ch.10, Ch.12 | The AI-layer scoping decisions |
| 10 (Phase 8) | Safety, cybersecurity, data architecture, deployment | Ch.12, Ch.13, Ch.14 | The permanent safety boundary |
| 11 (Phase 9) | Validation methodology, fault scenarios, demonstration strategy | Ch.12, Ch.14 | The MVP's validation plan |
| 12 (Phase 10) | Scope, MVP, build/later/never decisions | Ch.13, Ch.14 | The final MVP itself |
| 13 (Phase 11) | Competitive differentiation, strategic positioning, the pending KONE-TKE combination | Ch.14 | This chapter's final positioning |
| 14 (Phase 12, this chapter) | Full synthesis | — | The team's authoritative reference |

**The dependency chain, end to end:** physical elevator engineering (1–3) makes fault taxonomy possible (4); fault taxonomy plus the KONE/competitive landscape (5–6) motivates a specific RCA methodology (7); that methodology needs real signal evidence (8); that evidence needs an AI layer to reason over it at scale (9); that AI layer needs a safety/security boundary (10) and a way to prove it works (11); all of it needs disciplined scoping (12) and a defensible strategic case (13); and all thirteen chapters converge here (14).

## 14.32 Mapping the Research Program's Topics

*The original planning roadmap's exact 48-item enumeration is not preserved verbatim in this book's working memory at this stage of the project; the table below maps the research program's actual, substantive coverage — which addresses the roadmap's intent — organized by chapter, rather than claiming a precise item-by-item reproduction of the original numbered list.*

| Topic Area | Chapter(s) | MVP-Critical? |
|---|---|---|
| Elevator types, mechanics, electrical/drive systems | 1–3 | Yes (foundational) |
| Subsystem failure modes, sensor dictionary | 1–3 | Yes |
| Fault codes, alarm taxonomy, cascades | 4 | Yes |
| KONE connected services, Technician Assistant | 5 | Supporting (positioning) |
| Otis/Schindler/TK Elevator landscape | 6, 13 | Supporting (positioning) |
| RCA methodology (5 Whys, Fishbone, FTA, FMEA, Bow-Tie) | 7 | Yes |
| Bayesian/causal reasoning | 7 | Yes |
| Signal processing, feature extraction | 8 | Yes |
| Anomaly detection methods | 8 | Yes |
| Alarm correlation algorithms | 8 | Yes |
| AI taxonomy, elevator-specific academic literature | 9 | Supporting |
| LLM task-fit, RAG, tool-calling | 9 | Yes |
| Multi-agent architecture | 9 | Research/Future |
| Explainability, confidence, abstention | 9 | Yes |
| Safety standards (EN 81, ASME A17, IEC 61508, PESSRAL) | 10 | Supporting (governs the boundary) |
| Cybersecurity standards (IEC 62443, ISO 8102-20) | 10 | Supporting |
| Data architecture, edge/cloud | 10 | Supporting |
| Validation methodology, metrics | 11 | Yes |
| Fault scenario library | 11 | Yes |
| Demonstration design | 11, 12 | Yes |
| MVP scoping, build/later/never decisions | 12 | Yes |
| Competitive differentiation, moat analysis | 13 | Supporting |
| Digital twin, GNN, PINN | 9, 12 | Research-only, explicitly deferred |

## 14.33 Final Team Research Division

| Workstream | Responsibilities | Chapters Owned | Deliverables | Validation Role | Judge-Question Role |
|---|---|---|---|---|---|
| **A — Elevator Engineering & Failure Modes** | Physical accuracy, fault-tree/FMEA construction | 1–3, 7 (engineering half) | Fault trees, FMEA tables, worked examples (§14.4) | Domain plausibility checks | B, L, M |
| **B — KONE Ecosystem & Competitive Intelligence** | KONE/competitor research, positioning | 5, 6, 13 | Capability maps, defense scripts | Claim-registry review (§14.20) | C–J, AJ |
| **C — RCA / Reliability / Causal Reasoning** | Bayesian engine, reasoning loop | 7 (reasoning half), part of 9 | The RCA engine's core logic | RCA-metric validation (§14.17) | K, N, O |
| **D — Data / Signal Processing / Anomaly Detection** | Evidence pipeline, telemetry handling | 8 | Signal-processing/anomaly-detection code | Signal-level validation | P, Q, R, S |
| **E — AI / RAG / Agent Architecture** | LLM orchestration, RAG, explainability | 9, parts of 12 | The AI orchestrator, ExplainabilityTrace | AI-layer validation (Ch.9) | T–Z |
| **F — Safety / Cybersecurity / Validation / Presentation** | Boundary enforcement, demo, judge prep | 10, 11, 12, 14 | Demo script, pitch materials, this chapter's defense bank | Full validation-framework ownership | AA–AO |

**Dependencies:** A feeds C (fault trees are C's input); D feeds C (evidence is C's input); C feeds E (RCA output is what E explains); B informs F's positioning work throughout; F cross-checks every workstream's claims against §14.20's registry before anything reaches a judge. **Required cross-checks:** no workstream finalizes a claim about KONE or a competitor without F's sign-off; no workstream finalizes a safety-adjacent statement without checking it against §14.10.

## 14.34 Final Research Verification Plan

| Claim | Priority | Source Type Needed | Safe Wording Until Verified |
|---|---|---|---|
| KONE Technician Assistant scale (1,500→6,000→40,000 users) | High | Official KONE/AWS materials (already sourced, Ch.13) | As currently stated, with the source cited |
| TK Elevator pilot statistics (~20,000 fewer visits, 40%+ fewer callbacks) | High | TKE/Microsoft press materials (already sourced, Ch.13) | Attributed explicitly as company-reported, not independently audited |
| KONE-TKE combination closing status | High | KONE/TKE ongoing disclosures | "Announced, not yet closed, as of this research" — re-verify before presenting if time has passed |
| Otis ONE's absence of a public GenAI tool | Medium | Continued monitoring | "Not found in this research" — re-verify shortly before presenting |
| Schindler Ahead's AI specifics | Medium | Continued monitoring | Same caveat |
| Academic paper claims (GNN/PINN precedent) | Medium | Already cited (Ch.9) | As cited, with the paper named |
| Any business-value figure | Low (none currently claimed) | Real KONE data | Do not state until available |

## 14.35 Final "If Asked..." Response Bank

*Each answer below is the condensed, presentation-ready form of a fully-worked answer elsewhere in this book.*

"KONE already has this." → §14.35's Otis/Schindler/TKE-parallel script, Ch.13 §13.40, adapted: acknowledge, name what's publicly established, name the narrower gap, state what's unproven. "KONE already has AI." → Yes — the differentiation is a reasoning structure, not AI usage itself (§14.13). "KONE already has Technician Assistant." → The closest existing capability; addressed directly, not avoided (Ch.13 §13.27). "KONE already has predictive maintenance." → A different problem (§14.2). "Your competitors already do this." → Not established publicly (§14.12). "Where is the innovation?" → §14.13's Category A. "Where is your data?" → None real; synthetic, honestly labeled (§14.22). "Is your data synthetic?" → Yes. "Can you prove RCA?" → Feasibility-level, not production-level (§14.17). "Why use an LLM?" → Synthesis/explanation only (§14.8). "Why use agents?" → We don't, for the MVP (§14.8). "Why not just use rules?" → Rules remain core; the gap is multi-hypothesis evidence-weighing (Ch.12 §12.52 Q2). "What happens if the AI is wrong?" → Human verification catches it before action (§14.10). "Can the AI control the elevator?" → Never (§14.10). "Is this production ready?" → No (§14.16). "What is autonomous?" → Nothing (§14.10). "What exactly can you demonstrate?" → §14.19's five scenarios. "What remains future work?" → §14.16's roadmap beyond MVP. "What makes this defensible?" → Data/workflow, not technology (§14.13). "Why should KONE invest in this?" → It's a cheap hypothesis to test against a real, evidenced gap (§14.38).

## 14.36 Final Do-Not-Say List

Never say, without direct evidence: *"KONE cannot do X"* or *"[Competitor] cannot do X"* (§14.20's RED row); *"our data is real"* (it isn't); *"this is production-ready"* (it isn't); *"we are safety-certified"* (never claimed); *"our AI is always accurate"* (contradicted by abstention's own existence); *"this will save KONE $X"* or any other fabricated business-impact figure; *"this is the first system to do X"* (unverifiable); *"our AI is fully autonomous"* (contradicted by Ch.10 Part I); *"we've deployed this in the field"* (never done). **Safer replacement, for each:** state the evidence tier (§14.20), state the hypothesis framing (§14.14), state the boundary (§14.10), and stop there.

## 14.37 Final Project Scorecard

| Dimension | Current Maturity | Weakness | Required Improvement | Evidence Needed |
|---|---|---|---|---|
| Problem importance | High (evidenced gap, §14.12) | Research completeness | KONE SME confirmation | Direct KONE engagement |
| Elevator-domain understanding | High (Ch.1–4, §14.4) | Not KONE-verified | Expert review | SME sign-off |
| Technical feasibility | High (Ch.12's MVP) | None major | — | Working prototype |
| RCA depth | High (Ch.7) | Illustrative priors only | Real outcome data | Pilot-stage data |
| AI necessity | Well-justified (§14.8) | — | — | — |
| Evidence grounding | High (Ch.6, Ch.9) | — | — | — |
| Explainability | High (Ch.9 Part VI) | Faithfulness untested at scale | Larger-scale testing | Ch.9's methodology, applied |
| Uncertainty handling | High (design), Low (calibration validation) | No real-outcome calibration yet | Real data | Pilot |
| Safety | High confidence (architectural) | — | — | — |
| Cybersecurity | Appropriately scoped for a prototype | Not production-hardened | Full posture at V1+ | Ch.10's roadmap |
| Validation | Moderate (feasibility-level) | No production validation | Full A–F roadmap | Ch.9 §11.46 |
| Competitive differentiation | Moderate–High (evidenced, not proven unique) | Research completeness | Continued monitoring | §14.34 |
| KONE value | Hypothesis-stage | Unmeasured | Pilot | Real deployment |
| Scalability | Unknown | Cross-model generalization untested | V1+ testing | Real fleet data |
| Prototype feasibility | High | — | — | — |
| Innovation | Moderate–High (combination, not invention) | — | — | — |
| Defensibility | Moderate (data/workflow, not tech) | Data moat not yet built | Time and real deployment | Pilot-stage accumulation |

---

# Part XI — The Final Word

## 14.38 Final Decision: What KONE Elevate Actually Is

**What is KONE Elevate?** An evidence-driven, auditable diagnostic-support layer for elevator fault isolation and root-cause analysis. **What problem does it solve?** The gap between an alarm firing and a technician holding a verified, evidence-weighed understanding of its cause. **What does it technically do?** Correlates alarms, weighs evidence against structured engineering knowledge and retrieved documentation, ranks root-cause hypotheses with calibrated confidence, and abstains when evidence is insufficient. **What does it not do?** Control the elevator, touch its safety architecture, diagnose universally across every elevator model, or act without human verification. **What is genuinely different?** Primary/consequential alarm separation, multi-hypothesis RCA with alternative-cause elimination, calibrated abstention-capable confidence, and a full auditable evidence trace — a combination not publicly demonstrated by any OEM this book researched, KONE included. **What can be demonstrated?** Feasibility, on five representative synthetic scenarios, including a live abstention case. **What cannot yet be proven?** Production accuracy, measured business value, fleet-scale generalization, and calibration against real outcomes. **Why does KONE care?** Because the specific reasoning step this project targets remains publicly unaddressed across an industry that has otherwise moved fast on connectivity, prediction, and even agentic AI — worth cheap evaluation precisely because it's cheap to test and specifically scoped, not because it's guaranteed to matter. **What would make it defensible?** Real KONE data, expert validation, and disciplined claim-keeping exactly as this book has practiced throughout. **What should the team build next?** Exactly §14.15's MVP, in the order §14.34 and Ch.12 §12.34 specify, defended with exactly the discipline this chapter's registries provide.

> **The canonical definition:** *KONE Elevate is an evidence-driven diagnostic intelligence layer that correlates elevator alarms, telemetry, engineering knowledge, and maintenance evidence into ranked, auditable root-cause hypotheses with calibrated confidence — complementing, not replacing, existing connected-elevator and technician-assistance capabilities, and requiring human verification before any action.*

## 14.39 Final Master Architecture Summary

```
PHYSICAL ELEVATOR
     ↓                          the ground truth; entirely outside this system (Ch.10 Part I)
SENSORS / CONTROLLER DATA
     ↓                          raw signal access
TELEMETRY + EVENTS + ALARMS
     ↓                          the three data types this book distinguishes throughout (Ch.6)
DATA QUALITY + TIME ALIGNMENT
     ↓                          prevents corrupted evidence and false causal ordering (Ch.6 §8.4-5)
SIGNAL PROCESSING + FEATURE EXTRACTION
     ↓                          converts raw signal into usable structure (Ch.6)
ANOMALY / EVENT DETECTION
     ↓                          the trigger for the whole investigation (Ch.6)
ALARM CORRELATION
     ↓                          separates primary from consequential — a core differentiator (Ch.4, §14.12)
EVIDENCE PACKAGE
     ↓                          the structured input to reasoning (Ch.6 §8.30)
FAULT HYPOTHESES
     ↓                          candidate causes, generated against engineering knowledge (Ch.7)
ENGINEERING KNOWLEDGE + FTA/FMEA + HISTORICAL DATA
     ↓                          the knowledge this project's core reasoning is grounded in (Ch.7, Ch.5)
CAUSAL / PROBABILISTIC REASONING
     ↓                          Bayesian evidence-weighting — the actual RCA engine (Ch.7)
ALTERNATIVE-CAUSE ELIMINATION
     ↓                          negative evidence downgrades inconsistent hypotheses (§14's own repeated theme)
RAG / AI / TOOLS / AGENTS WHERE JUSTIFIED
     ↓                          scoped synthesis and explanation, never computation or authority (Ch.9, Ch.12)
RANKED ROOT-CAUSE HYPOTHESES
     ↓                          the structured output, never a single unexplained guess
CONFIDENCE + UNCERTAINTY
     ↓                          calibrated, evidence-strength-dependent (Ch.9 §9.29)
EXPLAINABLE EVIDENCE TRACE
     ↓                          full provenance, checkable claim by claim (Ch.9 Part VI)
ABSTAIN / ESCALATE WHEN NECESSARY
     ↓                          the system's honesty mechanism, demonstrated live in every worked example
TECHNICIAN VERIFICATION
     ↓                          the mandatory, permanent human checkpoint (Ch.10 Part I)
CORRECTIVE ACTION SUPPORT
     ↓                          a recommendation, never an instruction the system itself executes
POST-REPAIR VERIFICATION
     ↓                          confirms or contradicts the RCA conclusion
KNOWLEDGE FEEDBACK LOOP
                                closes the cycle, informing future investigations (Ch.10 §10.27)
```

**Every arrow above is a boundary this book has examined from at least three separate angles — engineering, AI-architectural, and safety/strategic — across its fourteen chapters.** None is asserted here for the first time; every one is a conclusion this research program earned.

---

This is the final chapter of the KONE Elevate Master Research Book. Fourteen chapters, built across twelve research phases, converge here: a physically-grounded, evidence-disciplined, safety-bounded, competitively-honest case for a specific, narrow, testable diagnostic-reasoning capability — proposed as a hypothesis worth KONE's evaluation, not asserted as a certainty it hasn't earned. The team's task from here is not further research. It is building exactly what this chapter specifies, defending it with exactly the discipline this chapter's registries provide, and being honest — as this entire book has tried to be, at every phase — about precisely where the evidence ends and the proposal begins.
