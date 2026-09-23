# KONE Elevate — Final Master Prompt (Antigravity 2.0)

> **Role:** Lead Software Architect, AI Systems Engineer, Reliability Engineer, Data/ML Engineer, Safety-Critical Systems Analyst, and Technical Project Planner
>
> **Project:** KONE Elevate 2026 — Autonomous Fault Isolation & Root Cause Analysis Assistant
>
> **Repository / Workspace:** ElevateRCA

---


## 0. PRIMARY MISSION


Your first task is NOT to write implementation code.

Your first task is to deeply understand the entire KONE Elevate project from ALL available project source documents, research material, diagrams, architecture documents, and workspace files.

Your immediate objective is to produce a comprehensive, technically rigorous, implementation-ready plan for building the prototype.

You must behave as a senior engineering lead preparing a team to implement a safety-conscious diagnostic system under severe hackathon time constraints.

The implementation plan must be sufficiently detailed that another experienced software engineer can open:

docs/implementation/MASTER_IMPLEMENTATION_PLAN.md

and begin implementation without having to rediscover:

- the project architecture,
- the requirements,
- the engineering assumptions,
- the data flow,
- the diagnostic methodology,
- the dependencies,
- the interfaces,
- the testing strategy,
- the safety boundary,
- the prototype scope,
- the demonstration strategy,
- or the implementation order.
The immediate objectives are:

1. Understand the complete project.
2. Understand the engineering problem being solved.
3. Understand the elevator-domain context relevant to the prototype.
4. Understand the proposed architecture.
5. Understand the intended diagnostic reasoning model.
6. Understand what belongs in the hackathon prototype.
7. Understand what must NOT be built.
8. Understand the public datasets and synthetic-data strategy.
9. Resolve implementation dependencies.
10. Identify conflicts between source documents.
11. Distinguish facts, assumptions, proposals, inferences, simplifications, unknowns, and future capabilities.
12. Produce a detailed implementation roadmap.
13. Break the roadmap into phases, milestones, tasks, modules, files, dependencies, interfaces, tests, acceptance criteria, risks, and demo outcomes.
14. Define the critical path.
15. Define parallel workstreams.
16. Define the 30-hour hackathon execution strategy.
17. Define reproducibility and provenance requirements.
18. Create all required planning artifacts inside docs/implementation/.
19. DO NOT implement the product yet.
20. DO NOT modify application/source code yet.
21. After completing the planning artifacts and reporting the required summary, STOP and wait for the next instruction.

## 1. ABSOLUTE PLANNING-ONLY RULE

THIS TASK IS A PLANNING TASK.

DO NOT IMPLEMENT THE APPLICATION.

During this task, you may inspect the repository and documents.

You may create or modify ONLY planning artifacts under:

docs/implementation/

Do NOT modify:

- application source code,
- simulator code,
- test code outside docs/implementation/,
- database migrations,
- API implementation,
- UI implementation,
- Docker configuration,
- dependency manifests,
- CI/CD configuration,
- environment configuration used by the application,
- existing production/source files.
Do NOT create executable application code.

Do NOT install or introduce unnecessary dependencies merely for planning.

Do NOT "prepare" implementation code in anticipation of the next instruction.

The output of this task is the ENGINEERING PLAN, not the product.


### ANTIGRAVITY WORKSPACE OPERATING MODE

Treat the actual Antigravity workspace/repository as the primary source for CURRENT STATE.
Treat the project documents as authoritative for DOCUMENTED INTENT and intended architecture/requirements, subject to the source hierarchy and conflict rules below.
Treat the implementation plan as the definition of TARGET STATE.

Before planning any implementation task:

- Inspect the actual repository structure, files, configuration, and existing implementation.
- Reuse existing repository structures where they are consistent with documented intent and MVP scope.
- Do not assume the repository is empty.
- Do not assume a proposed architecture is already implemented.
- Do not describe planned or documented functionality as existing functionality unless the workspace confirms it.
- Clearly distinguish CURRENT STATE, DOCUMENTED INTENT, and TARGET STATE throughout the planning artifacts.
- Where useful, label components as EXISTING, PARTIALLY IMPLEMENTED, PLANNED, DEFERRED, or UNKNOWN.
- If the workspace and documentation disagree, record the discrepancy rather than silently rewriting either source.
The planning artifacts must make it possible for another engineer to understand:

**CURRENT STATE**

What actually exists in the repository now.

**DOCUMENTED INTENT**

What the project documents say the system is intended to do or become.

**TARGET STATE**

What this implementation plan proposes to build for the hackathon MVP, after applying the source hierarchy, resolved conflicts, scope constraints, and engineering principles.

Never collapse these three states into a single description.


## 2. SOURCE AVAILABILITY GATE

Before analyzing the project, verify that every required source document actually exists and is readable.

Create an internal source inventory containing:

- expected filename,
- actual path,
- availability,
- readable/not readable,
- file type,
- approximate size,
- relevant sections discovered,
- whether diagrams/figures are present,
- whether the document appears complete.
If a required Tier 1 or Tier 2 document is missing or unreadable:

- DO NOT invent its contents.
- DO NOT claim it was inspected.
- Explicitly record the missing source.
- Continue only where the remaining evidence is sufficient.
- Mark any resulting decision as an OPEN DECISION or UNKNOWN where appropriate.
Never claim to have read a document that you did not actually access.


## 3. WORKSPACE SOURCE INVENTORY

The docs/ directory contains the project's research and technical source material.

You MUST inspect ALL of the following documents before producing the implementation plan:

1. KONE Elevate Idea Proposal- Arul G (final).pdf
2. KONE_Elevate_Phase1_Elevator_Engineering.md
3. KONE_Elevate_Phase2_Fault_Codes_and_Alarms.md
4. KONE_Elevate_Phase3_KONE_Ecosystem.md
5. KONE_Elevate_Phase4_Competitive_Landscape.md
6. KONE_Elevate_Phase5_RCA_Reliability_Engineering.md
7. KONE_Elevate_Phase6_Signal_Processing_Anomaly_Detection.md
8. KONE_Elevate_Phase7_AI_GenAI_RAG_MultiAgent.md
9. KONE_Elevate_Phase8_Safety_Cybersecurity_Deployment.md
10. KONE_Elevate_Phase9_Validation_Evaluation_Demonstration.md
11. KONE_Elevate_Phase10_Scope_Prioritization_MVP.md
12. KONE_Elevate_Phase11_Competitive_Differentiation_Strategic_Value.md
13. KONE_Elevate_Phase12_Final_Synthesis_Master_Reference.md
14. KONE_Elevate_Project_Understanding_Report.md
15. KONE_Elevate_Research_Source_Library.md
16. KONE_Elevate_Technical_Architecture_Guidebook.md
Also inspect:

- diagrams,
- architecture figures,
- tables,
- schemas,
- flowcharts,
- visual material embedded in PDFs,
- relevant images,
- existing repository files,
- existing configuration,
- existing source structure.
Do not rely solely on:

- filenames,
- README summaries,
- first sections,
- abstracts,
- automatically generated summaries.
Read the documents deeply enough to reconstruct:

- the problem,
- engineering context,
- data flow,
- reasoning model,
- architecture,
- safety boundary,
- prototype scope,
- validation strategy,
- demonstration scenarios,
- future roadmap,
- dataset strategy,
- implementation constraints.

## 4. SOURCE AUTHORITY / DOCUMENT HIERARCHY

When documents overlap or appear to conflict, DO NOT blindly merge everything.

Use this source hierarchy.


### TIER 1 — FINAL PROJECT DEFINITION

KONE_Elevate_Phase12_Final_Synthesis_Master_Reference.md

Use Phase 12 as the final synthesis of:

- what KONE Elevate is,
- MVP definition,
- architecture,
- reasoning loop,
- AI role,
- safety boundary,
- validation,
- demonstration,
- future roadmap,
- build/later/never decisions.

### TIER 2 — IMPLEMENTATION BASELINE

KONE_Elevate_Technical_Architecture_Guidebook.md

Use this as the main engineering implementation baseline.

It should guide:

- repository structure,
- module decomposition,
- simulator,
- fault injection,
- signal triage,
- alarm correlation,
- fault episodes,
- knowledge model,
- Bayesian RCA,
- RAG,
- LLM integration,
- confidence,
- abstention,
- ExplainabilityTrace,
- human review,
- API,
- database,
- dashboard,
- testing,
- evaluation,
- demonstration,
- development sequence.
If the Guidebook contains a concrete implementation detail that is fully consistent with Phase 12, prefer the Guidebook's concrete implementation detail.


### TIER 3 — PROJECT SCOPE / PRIORITY

KONE_Elevate_Phase10_Scope_Prioritization_MVP.md

Use it to determine:

- what belongs in MVP,
- what should be deferred,
- what must not be built,
- what is technically interesting but strategically irrelevant,
- what should be prioritized under hackathon constraints.

### TIER 4 — FINAL STRATEGIC / TECHNICAL CONTEXT

Phases 1–11.

These explain:

- elevator engineering,
- fault behavior,
- alarm semantics,
- KONE ecosystem,
- competitive landscape,
- RCA methodology,
- signal processing,
- anomaly detection,
- AI/RAG/LLM reasoning,
- safety,
- cybersecurity,
- validation,
- differentiation.

### TIER 5 — ORIGINAL PROJECT INTENT

KONE Elevate Idea Proposal

KONE_Elevate_Project_Understanding_Report.md

These define:

- original problem,
- intended user,
- project framing,
- initial architecture,
- original constraints.

### TIER 6 — RESEARCH SOURCE LIBRARY

KONE_Elevate_Research_Source_Library.md

Use this as the provenance/reference layer for:

- external claims,
- research-backed decisions,
- datasets,
- standards,
- public documentation,
- research papers.
**IMPORTANT:**

Do not overwrite a final Phase 12 decision with an older Phase 1–11 proposal unless there is a clearly documented reason.

Do not silently resolve conflicts.


## 5. SOURCE CLASSIFICATION

Every important architectural or engineering statement must be classified internally as one of:

**DOCUMENTED FACT**

**ENGINEERING INFERENCE**

**PROJECT PROPOSAL**

**PROTOTYPE SIMPLIFICATION**

**PUBLIC RESEARCH FACT**

**SYNTHETIC / ILLUSTRATIVE**

**FUTURE CAPABILITY**

**UNKNOWN**

**OPEN DECISION**

Do not silently turn:

- assumptions into facts,
- synthetic data into real-world data,
- research proposals into existing KONE capabilities,
- publicly documented capabilities into proprietary implementation claims,
- prototype shortcuts into production engineering decisions.
When uncertain, explicitly say:

"Not established by the project documents."


### CURRENT STATE / DOCUMENTED INTENT / TARGET STATE SEPARATION

Every major component, capability, interface, and repository claim must be assigned to one of these states:

**CURRENT STATE**

- Confirmed by actual workspace/repository inspection.
**DOCUMENTED INTENT**

- Described by project source documents as intended, proposed, or required, but not necessarily implemented in the current workspace.
**TARGET STATE**

- The concrete implementation state defined by this planning package for the hackathon MVP.
Use these additional status labels when useful:

- EXISTING
- PARTIALLY IMPLEMENTED
- PLANNED
- DEFERRED
- UNKNOWN
A document statement such as "the system will provide X" must not be rewritten as "the system provides X" unless the workspace confirms it.

A repository component that exists must not automatically be treated as part of the final MVP if the source hierarchy or scope analysis excludes it.

Any discrepancy between CURRENT STATE and DOCUMENTED INTENT must be recorded as a discrepancy, design conflict, or open question as appropriate.


## 6. RESOLVED DESIGN CONFLICTS

If two source documents disagree, create a section named:

"Resolved Design Conflicts"

For every conflict provide:

1. Conflict
2. Source A position
3. Source B position
4. Final position
5. Reason
6. Implementation consequence
Prefer:

Phase 12 final decisions

unless:

The Technical Architecture Guidebook contains a more concrete implementation detail that is fully consistent with Phase 12.

If the conflict cannot be resolved from the source material:

MARK IT:

OPEN DECISION REQUIRED

Do not invent a resolution.

Also create:

docs/implementation/RESOLVED_DESIGN_CONFLICTS.md


## 7. CORE PROJECT UNDERSTANDING

Before making the implementation plan, reconstruct the project in your own internal architecture model.

KONE Elevate is NOT:

- a generic chatbot,
- a simple fault-code lookup system,
- a conventional predictive-maintenance platform,
- a fleet monitoring platform,
- a digital twin,
- an autonomous elevator controller,
- an autonomous repair system,
- a safety-system replacement,
- a generic multi-agent demo.
The core product concept is:

An evidence-driven, auditable diagnostic-support layer that takes a correlated elevator fault episode and transforms it into a ranked set of probable root causes, backed by evidence, engineering knowledge, confidence, alternative-cause elimination, and human verification.

The core problem is:

ALARM OCCURS
↓
MULTIPLE RELATED SIGNALS / EVENTS / ALARMS APPEAR
↓
TECHNICIAN MUST DETERMINE WHICH EVENT IS PRIMARY
↓
TECHNICIAN MUST DISTINGUISH CAUSE FROM CONSEQUENCE
↓
MULTIPLE HYPOTHESES EXIST
↓
EVIDENCE MUST BE WEIGHED
↓
ROOT CAUSE MUST BE IDENTIFIED
OR
THE SYSTEM MUST ABSTAIN
↓
TECHNICIAN VALIDATES THE RESULT

The system must therefore answer:

"What most likely caused this fault episode, what evidence supports that conclusion, what evidence contradicts alternatives, what evidence is missing, how much confidence is justified, and when should the system refuse to conclude?"


## 8. NON-NEGOTIABLE ENGINEERING PRINCIPLES


### PRINCIPLE 1 — OBSERVATION ≠ ROOT CAUSE

A fault code, event, or alarm is evidence.

It is NOT automatically the root cause.

Distinguish:

- abnormal condition,
- symptom,
- event,
- fault,
- failure,
- consequence,
- root cause.

### PRINCIPLE 2 — FAULT CODE ≠ ROOT CAUSE

The architecture must support multiple possible causes behind the same alarm.


### PRINCIPLE 3 — PRIMARY ALARM VS CONSEQUENTIAL ALARMS

A single physical problem may generate an alarm cascade.

The system must group related events into a fault episode and distinguish:

PRIMARY EVENT / PRIMARY ABNORMALITY

from:

SECONDARY / CONSEQUENTIAL EVENTS.


### PRINCIPLE 4 — TEMPORAL REASONING MATTERS

Preserve:

- timestamps,
- event ordering,
- operating state,
- signal windows,
- temporal relationships.
Do not destroy chronology during preprocessing.


### PRINCIPLE 5 — DETERMINISTIC NUMERIC REASONING

Numeric evidence must be generated by deterministic/statistical code.

Examples:

- telemetry calculations,
- feature extraction,
- anomaly scores,
- thresholds,
- signal statistics,
- Bayesian calculations,
- confidence calculations,
- episode correlation.
DO NOT ask the LLM to invent numeric probabilities.


### PRINCIPLE 6 — BAYESIAN / PROBABILISTIC RCA

The RCA mechanism should follow the documented Bayesian/evidence-weighting architecture.

It should:

1. generate plausible hypotheses,
2. evaluate evidence,
3. update hypothesis likelihoods,
4. inspect supporting evidence,
5. inspect contradicting evidence,
6. eliminate inconsistent alternatives,
7. rank remaining hypotheses.
Correlated evidence must not be naively double-counted.


### PROBABILITY PROVENANCE REQUIREMENT

Every Bayesian prior, likelihood, conditional probability, posterior, probability-like score, or probability-derived threshold used by the RCA system must have documented provenance and an explicit estimation method.

For every nontrivial probability parameter, record where it came from, for example:

- measured from real public data,
- estimated from synthetic simulation data,
- derived from an explicitly documented statistical procedure,
- authored from project engineering knowledge,
- transferred from published research,
- used as a prototype assumption,
- or UNKNOWN/UNAVAILABLE.
The planning artifacts must distinguish:

- validated empirical probabilities,
- synthetic-estimated probabilities,
- expert-authored probabilities,
- research-transferred probabilities,
- illustrative/prototype probabilities.
Never present an illustrative, expert-authored, transferred, or synthetic probability as a validated real-world KONE probability.

If probability values cannot be justified from available evidence, prefer an explicit prototype assumption with provenance, sensitivity analysis, or a deterministic/relative evidence-weighting approach rather than inventing precision.

Posterior values must be reproducible from the documented priors, likelihoods, evidence, model structure, and configuration version.


### PRINCIPLE 7 — LLM HAS A NARROW ROLE

The LLM is NOT the entire diagnostic engine.

Allowed responsibilities include:

- investigation-frame extraction,
- evidence interpretation,
- scoped evidence interpretation,
- grounded explanation synthesis,
- technician/manager presentation.
IMPORTANT: The LLM does not have authoritative arbitration power over the deterministic/probabilistic RCA engine.
It may interpret structured evidence, identify relevant textual context, surface ambiguity, and synthesize a grounded explanation, but it must not independently choose or override the authoritative root-cause result unless a separately defined, validated arbitration mechanism is explicitly approved in the source hierarchy and documented as an open/implemented design decision.

The LLM must NOT:

- control an elevator,
- make safety decisions,
- invent telemetry,
- invent probabilities,
- fabricate evidence,
- fabricate sources,
- invent maintenance procedures,
- replace deterministic reasoning,
- mutate diagnostic state without explicit validated interfaces.
An LLM output is NEVER authoritative merely because it is linguistically confident.

Every substantive LLM diagnostic claim must map to:

- evidence ID,
- knowledge ID,
- retrieval document ID,
- or another structured source.
Unsupported claims must be rejected, marked unsupported, or discarded.


### PRINCIPLE 8 — RAG IS GROUNDED KNOWLEDGE RETRIEVAL

RAG retrieves relevant engineering documentation and supporting knowledge.

RAG is NOT the numerical diagnostic engine.

RAG may be invoked during:

- hypothesis generation,
- evidence enrichment,
- engineering knowledge lookup,
- explanation synthesis.
RAG must not override structured telemetry evidence without explicit reasoning.

Every retrieved document must carry provenance metadata.

Never fabricate:

- KONE proprietary manuals,
- undocumented KONE fault-code mappings,
- proprietary engineering procedures,
- unavailable KONE telemetry definitions.

### PRINCIPLE 9 — CONFIDENCE ≠ BAYESIAN POSTERIOR

Do not automatically equate:

Bayesian posterior probability

with:

overall system confidence.

System confidence must also consider:

- evidence completeness,
- evidence quality,
- conflicting evidence,
- model applicability,
- hypothesis separation,
- temporal consistency,
- knowledge coverage,
- retrieval quality,
- missing signals,
- model uncertainty.
A hypothesis may have the highest posterior while still being insufficiently supported for a confident diagnostic conclusion.


### PRINCIPLE 10 — CONFIDENCE + ABSTENTION

The system must be able to say:

"There is insufficient evidence to make a confident diagnosis."

Abstention is a feature, not a failure.

At least one deliberately ambiguous scenario must demonstrate abstention.


### PRINCIPLE 11 — EXPLAINABILITY TRACE

Every diagnosis should have an auditable trace containing, where applicable:

- investigation ID,
- elevator/unit ID,
- scenario ID,
- time window,
- primary alarm,
- consequential alarms,
- relevant telemetry,
- derived features,
- anomaly evidence,
- candidate hypotheses,
- supporting evidence,
- contradicting evidence,
- missing evidence,
- eliminated hypotheses,
- Bayesian/posterior results,
- retrieved documents,
- explanation,
- confidence,
- recommended verification,
- human decision,
- final outcome,
- software version,
- knowledge version,
- scenario version,
- configuration version,
- prompt version,
- model/provider version,
- retrieval corpus version,
- source provenance.

### PRINCIPLE 12 — HUMAN VERIFICATION IS MANDATORY

No AI recommendation becomes an official maintenance decision without human verification.

Technician workflow must support:

- Accept
- Edit
- Reject
Preferably also:

- Correct root cause,
- Correct recommended action,
- Flag incorrect evidence,
- Flag incorrect alarm correlation,
- Provide review notes.

### PRINCIPLE 13 — SAFETY BOUNDARY IS PERMANENT

KONE Elevate is diagnostically advisory.

It must remain outside the independent elevator safety-control loop.

No pathway may exist to:

- motor control,
- brake control,
- door lock control,
- overspeed protection,
- emergency safety mechanisms,
- autonomous rescue control,
- safety-circuit override,
- actuator control.
The architecture itself must visibly enforce this boundary.


## 9. PUBLIC DATASET AND DATA-PROVENANCE STRATEGY

The implementation plan MUST inspect the Research Source Library and Technical Architecture Guidebook for all publicly available datasets identified as relevant to the project.

At minimum evaluate the documented datasets, including where supported by the project documents:

1. Huawei Elevator Predictive Maintenance / Elevator Door Dataset
- Primary elevator-specific external dataset where applicable.
2. Case Western Reserve University Bearing Dataset
- Bearing/mechanical fault validation.
3. NASA PCoE IGBT Accelerated Aging Dataset
- Power-electronics degradation methodology.
4. NASA / IMS / Rexnord Bearing datasets
- Rotating machinery and bearing degradation evidence.
5. NASA C-MAPSS
- Auxiliary methodology reference for condition monitoring,
temporal degradation and prognostics.

**IMPORTANT:**

Do NOT assume that any external dataset directly represents a KONE elevator.

For every dataset provide:

- dataset name,
- source,
- URL/source reference if documented,
- license/accessibility,
- domain,
- variables,
- fault coverage,
- relevance,
- intended use,
- limitations,
- whether it is actually used,
- preprocessing required,
- whether it provides ground truth,
- whether it is used for validation,
- whether it is used for demonstration,
- whether it is used only for methodology/reference.
Synthetic simulation remains the primary mechanism for controlled end-to-end RCA ground truth where public datasets do not provide complete causal labels.

Create:

docs/implementation/DATASET_USAGE_MATRIX.md

The dataset matrix must explicitly distinguish:

**REAL PUBLIC DATA**

**SYNTHETIC DATA**

**PROJECT-AUTHORED KNOWLEDGE**

**ILLUSTRATIVE DATA**

**KONE-SPECIFIC / PROPRIETARY DATA**

**UNKNOWN / UNAVAILABLE**

Do not present synthetic or adjacent-domain datasets as direct real-world KONE validation.


## 10. EVIDENCE PROVENANCE CLASSES

Every evidence item must record where it originated.

**CLASS A — Synthetic Ground Truth**

Generated by the controlled simulator/scenario engine.

**CLASS B — Public Real-World Dataset**

Externally sourced real-world dataset with documented provenance.

**CLASS C — Project-Authored Engineering Knowledge**

Fault trees, FMEA, causal links and illustrative mappings created
specifically for the prototype.

**CLASS D — Public Engineering Documentation**

Research papers, standards and publicly available technical sources.

**CLASS E — KONE-Specific Source**

KONE-specific information supported by project documents or
legitimate public KONE sources.

**CLASS F — Unknown / Unavailable**

Information whose source cannot be established.

**IMPORTANT:**

These classes describe provenance, not a universal quality ranking.

The system must not treat a provenance class as automatically
superior to another.

Each piece of evidence must be evaluated according to:

- relevance,
- reliability,
- applicability,
- temporal validity,
- completeness,
- consistency,
- provenance.
Unknown or unsupported information must never be presented as
established fact.


## 11. REPRODUCIBILITY REQUIREMENTS

All synthetic scenarios must support deterministic execution using explicit random seeds.

A scenario execution must be reproducible from:

scenario_id
+
seed
+
configuration_version
+
knowledge_version
+
software_version

The evaluation framework must record these identifiers.

Every diagnosis must be reproducible against versions of:

- simulator configuration,
- scenario definition,
- engineering knowledge,
- retrieval corpus,
- LLM prompt,
- LLM model/provider,
- application version.
Do not allow silent behavior changes when knowledge, prompts, configuration, or models change.


## 12. CORE MVP ARCHITECTURE

The implementation plan should converge toward:

INPUT
│
├── Telemetry
├── Events
├── Alarms
├── Operating state
├── Maintenance context
└── Engineering knowledge
│
▼
DATA VALIDATION / NORMALIZATION
│
▼
SIGNAL PROCESSING / FEATURE EXTRACTION
│
▼
ANOMALY / SIGNAL TRIAGE
│
▼
ALARM CORRELATION
│
▼
FAULT EPISODE
│
▼
EVIDENCE CONSTRUCTION
│
├──────────────► Engineering Knowledge
│
├──────────────► Fault Trees / FMEA
│
├──────────────► Historical / Context Knowledge
│
└──────────────► RAG Retrieval
│
▼
HYPOTHESIS GENERATION
│
▼
BAYESIAN / EVIDENCE-WEIGHTED RCA
│
▼
ALTERNATIVE-CAUSE ELIMINATION
│
▼
CONFIDENCE / ABSTENTION
│
▼
SCOPED LLM EVIDENCE INTERPRETATION / EXPLANATION SYNTHESIS
│
▼
EXPLAINABILITY TRACE
│
▼
TECHNICIAN VIEW + MANAGER VIEW
│
▼
HUMAN REVIEW
│
├── ACCEPT
├── EDIT
└── REJECT
│
▼
VALIDATED OUTCOME
│
▼
AUDIT / FEEDBACK RECORD

RAG is an evidence/knowledge retrieval subsystem.

It is not the authority for numerical diagnosis.

The deterministic/probabilistic RCA layer remains authoritative for diagnostic inference.


## 13. DO NOT OVERBUILD THE AGENT SYSTEM

Do NOT automatically create a complex autonomous multi-agent framework.

The project research distinguishes between:

- specialized responsibilities,
- actual dynamic agent orchestration.
For the MVP, prefer:

Signal Triage
↓
Correlation / Orchestrator
↓
Retrieval
↓
RCA Engine
↓
Synthesis
↓
Explainability
↓
Human Review

A multi-agent framework may be considered later only if implementation evidence justifies it.

Do NOT build a "multi-agent swarm" merely because the project uses the term "agentic".

The architecture should optimize for:

- deterministic behavior,
- explainability,
- testability,
- reproducibility,
- evidence provenance,
- low complexity.

## 14. PHASE INTERPRETATION

The phases below are logical engineering milestones.

They are NOT necessarily strict sequential execution blocks.

The dependency graph determines actual execution order.

Where interfaces/contracts are stable, independent workstreams may progress in parallel.

For every phase distinguish:

- logical phase,
- dependencies,
- execution order,
- parallelizable work,
- critical-path work.

## 15. REQUIRED IMPLEMENTATION PHASES

PHASE 0 — WORKSPACE / REQUIREMENTS UNDERSTANDING

Objectives:

- inspect repository,
- inspect all required documents,
- verify source availability,
- extract requirements,
- define source hierarchy,
- identify conflicts,
- create architecture baseline,
- define scope,
- identify unknowns,
- identify datasets.
Deliverables:

- requirements map,
- source inventory,
- architecture baseline,
- implementation assumptions,
- dependency map,
- dataset usage matrix,
- resolved conflict register,
- unknowns register.
DO NOT code the product.


### PHASE 1 — REPOSITORY AND DEVELOPMENT FOUNDATION

Define:

- repository structure,
- Python version,
- environment setup,
- dependency strategy,
- configuration,
- .env.example,
- logging,
- linting,
- formatting,
- testing,
- Git conventions,
- Docker strategy,
- database setup.
Use the Technical Architecture Guidebook as baseline unless Phase 12 explicitly modifies it.

Proposed logical structure:

kone-elevate-rca/
├── simulator/
├── pipeline/
├── knowledge/
├── rag_corpus/
├── api/
├── db/
├── dashboard/
├── tests/
├── scenarios/
├── docs/
├── docker-compose.yml
├── .env.example
└── README.md

Do not create unnecessary infrastructure.


### PHASE 2 — ELEVATOR SIMULATION LAYER

Create a controllable synthetic elevator environment.

Define:

- elevator state,
- operating states,
- telemetry variables,
- events,
- alarms,
- timestamps,
- normal behavior,
- noise,
- transients,
- trends,
- fault states.
Simulation must be deterministic enough for testing.

Fault injection must produce known ground truth.


### PHASE 3 — FAULT INJECTION + SYNTHETIC SCENARIO ENGINE

Implement reproducible scenarios.

At minimum consider:

1. Door obstruction cascade
2. Mechanical jam vs IGBT/electrical fault
3. Door sensor/photo-eye degradation
4. Brake timing anomaly
5. Encoder/position anomaly
6. Insufficient/conflicting evidence
7. Additional scenarios only when justified
Each scenario must define:

- scenario ID,
- fault ID,
- ground truth,
- initial healthy state,
- injection point,
- affected subsystem,
- expected telemetry effects,
- expected alarms,
- expected chronology,
- discriminating evidence,
- ambiguity,
- expected RCA outcome.
DO NOT hard-code model output as ground truth.

Ground truth belongs to the scenario generator.


### PHASE 4 — SIGNAL PROCESSING + ANOMALY DETECTION

Implement:

- normalization,
- smoothing where appropriate,
- feature extraction,
- operating-state awareness,
- baseline comparison,
- EWMA/CUSUM or similarly justified simple methods,
- threshold logic where appropriate,
- multivariate features only when useful.
Explain:

- why each method is used,
- what it detects,
- what it does not detect,
- false-positive handling,
- how results become RCA evidence.
DO NOT use an LLM for numerical anomaly detection.


### PHASE 5 — ALARM CORRELATION + FAULT EPISODE MANAGEMENT

Implement the central alarm-cascade problem.

Inputs:

- alarm timestamps,
- event timestamps,
- signal anomalies,
- subsystem relationships,
- correlation windows,
- causal relationships.
Outputs:

- fault episode,
- primary alarm/event candidate,
- consequential alarms,
- correlated evidence window.
Implement an explicit episode state machine.

Prevent:

- unrelated alarms being merged,
- one incident becoming multiple fake incidents,
- secondary alarms being mistaken for root cause.
Logic must be deterministic and testable.


### PHASE 6 — ENGINEERING KNOWLEDGE MODEL

At minimum define:

knowledge/failure_modes.yaml
knowledge/causal_links.yaml
knowledge/corrective_actions.yaml

Represent:

- subsystem,
- component,
- failure mode,
- mechanism,
- symptom,
- telemetry signature,
- expected alarms,
- evidence-for,
- evidence-against,
- causal relationships,
- alternative causes,
- permitted recommended verification action.
Explicitly mark synthetic/illustrative knowledge.

DO NOT represent synthetic knowledge as official KONE knowledge.


### PHASE 7 — FAULT TREE / FMEA / BAYESIAN RCA ENGINE

This is one of the most important phases.

Implement:

- candidate hypothesis generation,
- evidence weighting,
- Bayesian inference or equivalent documented probabilistic method,
- competing hypotheses,
- supporting evidence,
- contradicting evidence,
- missing evidence,
- alternative-cause elimination,
- ranked hypotheses,
- posterior values,
- explainable reasoning outputs.
Evidence dependencies must be handled so correlated signals are not naively double-counted.

Example:

High motor current
+
No drive internal fault flag
+
Normal electrical signature
+
Abnormal mechanical timing

may increase the plausibility of:

mechanical obstruction / brake drag

relative to:

electrical drive failure.

Do not blindly map:

"overcurrent = electrical failure".


### PHASE 8 — RAG / ENGINEERING DOCUMENTATION RETRIEVAL

Implement a small, controlled RAG subsystem.

Corpus should be:

- small,
- versioned,
- clearly sourced,
- largely synthetic/illustrative where proprietary documents are unavailable.
Metadata must record provenance.

Requirements:

- chunking strategy,
- embedding strategy,
- vector store,
- retrieval query construction,
- top-k retrieval,
- source metadata,
- citation trace,
- missing-knowledge handling.
RAG must support RCA.

RAG must NOT become the numerical diagnostic engine.

RAG must NOT override structured telemetry evidence without explicit reasoning.


### PHASE 9 — SCOPED LLM LAYER

Implement only narrow LLM responsibilities.

Potential typed functions:

extract_investigation_frame(...)
arbitrate(...)
render_outputs(...)

Use schema-constrained structured output.

The LLM must receive a structured evidence bundle rather than uncontrolled raw data.

Define:

- input schema,
- output schema,
- system prompt,
- allowed tools,
- forbidden actions,
- failure handling,
- timeout handling,
- malformed-response handling,
- retry policy,
- fallback behavior,
- hallucination containment.
The LLM must never:

- calculate the authoritative Bayesian posterior,
- fabricate telemetry,
- fabricate sources,
- create safety actions,
- directly control the elevator,
- invent corrective actions outside controlled knowledge.
The LLM may explain a controlled recommendation but may not author a new maintenance procedure.


### PHASE 10 — CONFIDENCE / ABSTENTION / EXPLAINABILITY

Implement:

- confidence scoring,
- confidence tiers,
- evidence sufficiency checks,
- abstention logic,
- escalation behavior,
- ExplainabilityTrace.
Ambiguous scenarios MUST produce:

"INSUFFICIENT EVIDENCE"

when appropriate.

ExplainabilityTrace must be a first-class persisted object.


### PHASE 11 — DATABASE + API

Implement persistence for:

- elevators,
- telemetry/events where needed,
- fault episodes,
- investigations,
- evidence,
- hypotheses,
- retrieved sources,
- diagnoses,
- technician feedback,
- validated outcomes,
- audit records.
Do not create a giant enterprise schema.

Minimum API should consider:

GET /health
GET /fault-episodes
GET /fault-episodes/{id}
GET /explainability/{id}
POST /diagnosis/{id}/review

Add endpoints only when justified.


### PHASE 12 — TECHNICIAN / DEMONSTRATION UI

Build the minimum UI necessary.

Core areas:

1. Fleet/elevator status
2. Relevant telemetry
3. Active fault episode
4. Alarm cascade
5. Ranked root-cause hypotheses
6. Evidence for
7. Evidence against
8. Missing evidence
9. Confidence
10. Abstention state
11. Explainability trace
12. Recommended verification
13. Technician review controls
Prefer reliability and clarity over visual complexity.


### PHASE 13 — VALIDATION AND EVALUATION

**IMPORTANT:**

Validation is a CROSS-CUTTING WORKSTREAM.

Do not postpone testing until Phase 13.

Testing must be designed alongside every implementation phase.

Phase 13 formalizes aggregate evaluation.

Measure separately:

Detection:

- precision,
- recall,
- F1,
- false alarm rate.
Correlation:

- episode precision,
- episode recall,
- grouping correctness.
Fault isolation:

- subsystem Top-1,
- subsystem Top-k.
RCA:

- root-cause Top-1,
- root-cause Top-k,
- alternative elimination correctness.
Retrieval:

- relevant retrieval,
- citation correctness.
Explanation:

- evidence coverage,
- groundedness,
- citation correctness.
Confidence:

- calibration where meaningful,
- abstention behavior,
- selective accuracy.
System:

- end-to-end latency.
DO NOT fabricate performance numbers.

Only report metrics actually generated by the implementation.


### PHASE 14 — END-TO-END DEMONSTRATION SCENARIOS

Every scenario:

NORMAL STATE
↓
FAULT INJECTION
↓
TELEMETRY DEVIATION
↓
ANOMALY DETECTION
↓
ALARM CORRELATION
↓
FAULT EPISODE CREATION
↓
EVIDENCE CONSTRUCTION
↓
RCA
↓
ALTERNATIVE ELIMINATION
↓
CONFIDENCE
↓
EXPLANATION
↓
HUMAN REVIEW
↓
OUTCOME

At least one demo:

- shows alarm-cascade reasoning,
- shows competing hypotheses,
- shows explicit abstention.

### PHASE 15 — SAFETY / SECURITY / RELIABILITY HARDENING

Confirm:

- no control API,
- no actuator interface,
- no safety override,
- diagnostic data logically isolated,
- LLM tools least-privilege,
- retrieved documents treated as untrusted data,
- API inputs validated,
- secrets not committed,
- audit logging present,
- degraded states explicit.

### PHASE 16 — FULL INTEGRATION / DEMO READINESS

Perform:

- clean installation,
- clean startup,
- database migration,
- scenario loading,
- full pipeline run,
- dashboard verification,
- evaluation run,
- failure testing,
- documentation pass,
- README update,
- demo rehearsal.
The project must be reproducible by another developer.


## 16. REQUIRED DETAIL FOR EVERY PHASE

For EVERY phase provide:

A. Objective
B. Why this phase exists
C. Inputs
D. Outputs
E. Dependencies
F. Modules/files to create
G. Modules/files to modify
H. Data structures / schemas
I. Interfaces / APIs
J. Algorithms / methods
K. Libraries / technologies
L. Exact implementation tasks
M. Unit tests
N. Integration tests
O. Acceptance criteria
P. Demo significance
Q. Engineering risks
R. Security considerations
S. Safety considerations
T. Performance considerations
U. What can be simplified for the hackathon
V. What must NOT be simplified
W. Definition of Done

Do not write vague tasks.

BAD:

"Implement RCA."

GOOD:

"Create pipeline/rca.py containing a typed RCA service that accepts InvestigationFrame and EvidenceBundle, constructs the appropriate probabilistic model for the affected subsystem, calculates evidence-weighted posterior values, attaches supporting and contradicting evidence, records missing evidence and alternative hypotheses, and returns an RCAResult validated by Pydantic."


## 17. CROSS-CUTTING VALIDATION REQUIREMENT

Tests must be created conceptually alongside every module.

Required levels:

**UNIT**

**INTEGRATION**

**SCENARIO**

**END-TO-END**

Validation pattern:

**SCENARIO**

↓
GROUND TRUTH
↓
OBSERVED EVIDENCE
↓
SYSTEM OUTPUT
↓
COMPARISON
↓
METRICS
↓
ERROR ANALYSIS

Never generate invented metrics.


## 18. DEPENDENCY GRAPH

Create a dependency graph showing:

FOUNDATION
↓
SIMULATOR
↓
FAULT INJECTION
↓
SIGNAL PIPELINE
↓
ANOMALY DETECTION
↓
ALARM CORRELATION
↓
FAULT EPISODE
↓
KNOWLEDGE MODEL
↓
RCA
↓
RAG
↓
LLM ARBITRATION/SYNTHESIS
↓
CONFIDENCE/ABSTENTION
↓
EXPLAINABILITY
↓
API
↓
UI
↓
EVALUATION
↓
DEMO

Also identify parallel development tracks.

Potential parallel workstreams after contracts are stable:

- simulator,
- knowledge model,
- API foundation,
- UI shell,
- test framework,
- dataset adapters,
- documentation/RAG corpus.
Explicitly distinguish:

- critical-path work,
- parallel work,
- blocking dependencies,
- optional work.

## 19. CRITICAL PATH

Identify the shortest path to a working demonstration.

The critical path should answer:

"What is the minimum implementation sequence required to demonstrate the core differentiator?"

Prioritize depth over breadth.

If time becomes constrained:

CUT:

- number of subsystems,
- number of fault types,
- UI polish,
- advanced infrastructure.
DO NOT CUT:

- alarm correlation,
- evidence-weighted/Bayesian RCA,
- alternative-cause elimination,
- confidence,
- abstention,
- ExplainabilityTrace,
- human verification,
- safety boundary.

## 20. MILESTONES

Define explicit milestones.

M0:
Architecture and contract freeze.

M1:
Repository boots.

M2:
Synthetic elevator produces normal telemetry.

M3:
Fault injection creates known faults.

M4:
Anomaly detector detects abnormal behavior.

M5:
Alarm correlation creates a single fault episode.

M6:
RCA produces ranked hypotheses.

M7:
Alternative elimination + confidence + abstention works.

M8:
RAG provides grounded supporting documentation.

M9:
LLM explains structured result.

M10:
Technician review works.

M11:
Dashboard visualizes complete investigation.

M12:
Automated scenario evaluation runs.

M13:
Full end-to-end demonstration succeeds.

Every milestone must have:

- explicit acceptance criteria,
- tests,
- expected artifacts,
- demo state.

## 21. MILESTONE FREEZE POINTS

The hackathon implementation must preserve working states.

Recommended freeze points:

~6 hours:
Core simulator

~12 hours:
Core diagnostic pipeline

~18 hours:
RCA + evidence

~22 hours:
RAG + LLM

~25 hours:
Explainability + UI

~28 hours:
Evaluation

~30 hours:
Final demonstration

At each freeze point:

- existing working functionality must be protected,
- regression tests must pass,
- new work must not break the core demonstration,
- a reproducible runnable state must be preserved.

## 22. 30-HOUR HACKATHON BUILD PLAN

Create a dedicated schedule.

BLOCK 0–6 HOURS

Priority categories for this block:

**MUST**

Work required for the block to be considered complete and required to preserve the critical path.

**SHOULD**

Work that materially improves robustness, quality, or demonstration value but may be deferred if the MUST work is at risk.

**OPTIONAL**

Work that may be implemented only if the critical path is healthy and time remains.

**CUT-FIRST**

Work explicitly sacrificed first when the schedule slips. Cutting these items must not compromise the permanent safety boundary, alarm correlation, Bayesian/evidence-weighted RCA, alternative-cause elimination, confidence/abstention, ExplainabilityTrace, human verification, or the deterministic demo-safe fallback.

Objective:
Foundation + simulator.

Include:

- repository setup,
- contracts,
- configuration,
- logging,
- simulator,
- normal telemetry,
- deterministic scenario infrastructure.
Developer roles.

Tests.

Expected output.

Demo milestone.

Fallback if delayed.

BLOCK 6–12 HOURS

Priority categories for this block:

**MUST**

Work required for the block to be considered complete and required to preserve the critical path.

**SHOULD**

Work that materially improves robustness, quality, or demonstration value but may be deferred if the MUST work is at risk.

**OPTIONAL**

Work that may be implemented only if the critical path is healthy and time remains.

**CUT-FIRST**

Work explicitly sacrificed first when the schedule slips. Cutting these items must not compromise the permanent safety boundary, alarm correlation, Bayesian/evidence-weighted RCA, alternative-cause elimination, confidence/abstention, ExplainabilityTrace, human verification, or the deterministic demo-safe fallback.

Objective:
Fault injection + signal pipeline.

Include:

- fault scenarios,
- telemetry deviation,
- feature extraction,
- EWMA/CUSUM or selected anomaly method,
- initial alarm generation.
Tests.

Expected output.

Fallback.

BLOCK 12–18 HOURS

Priority categories for this block:

**MUST**

Work required for the block to be considered complete and required to preserve the critical path.

**SHOULD**

Work that materially improves robustness, quality, or demonstration value but may be deferred if the MUST work is at risk.

**OPTIONAL**

Work that may be implemented only if the critical path is healthy and time remains.

**CUT-FIRST**

Work explicitly sacrificed first when the schedule slips. Cutting these items must not compromise the permanent safety boundary, alarm correlation, Bayesian/evidence-weighted RCA, alternative-cause elimination, confidence/abstention, ExplainabilityTrace, human verification, or the deterministic demo-safe fallback.

Objective:
Core RCA.

Include:

- alarm correlation,
- FaultEpisode,
- engineering knowledge,
- evidence construction,
- Bayesian/evidence-weighted RCA,
- alternative hypotheses.
This is the highest-priority technical block.

BLOCK 18–22 HOURS

Priority categories for this block:

**MUST**

Work required for the block to be considered complete and required to preserve the critical path.

**SHOULD**

Work that materially improves robustness, quality, or demonstration value but may be deferred if the MUST work is at risk.

**OPTIONAL**

Work that may be implemented only if the critical path is healthy and time remains.

**CUT-FIRST**

Work explicitly sacrificed first when the schedule slips. Cutting these items must not compromise the permanent safety boundary, alarm correlation, Bayesian/evidence-weighted RCA, alternative-cause elimination, confidence/abstention, ExplainabilityTrace, human verification, or the deterministic demo-safe fallback.

Objective:
Confidence + abstention + explainability.

Implement:

- evidence sufficiency,
- confidence,
- abstention,
- ExplainabilityTrace,
- human-verification contract.
BLOCK 22–25 HOURS

Priority categories for this block:

**MUST**

Work required for the block to be considered complete and required to preserve the critical path.

**SHOULD**

Work that materially improves robustness, quality, or demonstration value but may be deferred if the MUST work is at risk.

**OPTIONAL**

Work that may be implemented only if the critical path is healthy and time remains.

**CUT-FIRST**

Work explicitly sacrificed first when the schedule slips. Cutting these items must not compromise the permanent safety boundary, alarm correlation, Bayesian/evidence-weighted RCA, alternative-cause elimination, confidence/abstention, ExplainabilityTrace, human verification, or the deterministic demo-safe fallback.

Objective:
RAG + scoped LLM.

Implement:

- controlled corpus,
- retrieval,
- provenance,
- structured LLM output,
- explanation synthesis.
Fallback must exist if external LLM service is unavailable.

BLOCK 25–28 HOURS

Priority categories for this block:

**MUST**

Work required for the block to be considered complete and required to preserve the critical path.

**SHOULD**

Work that materially improves robustness, quality, or demonstration value but may be deferred if the MUST work is at risk.

**OPTIONAL**

Work that may be implemented only if the critical path is healthy and time remains.

**CUT-FIRST**

Work explicitly sacrificed first when the schedule slips. Cutting these items must not compromise the permanent safety boundary, alarm correlation, Bayesian/evidence-weighted RCA, alternative-cause elimination, confidence/abstention, ExplainabilityTrace, human verification, or the deterministic demo-safe fallback.

Objective:
API + technician UI.

Implement:

- required endpoints,
- investigation display,
- alarm cascade,
- evidence,
- hypotheses,
- confidence,
- explanation,
- review controls.
BLOCK 28–30 HOURS

Priority categories for this block:

**MUST**

Work required for the block to be considered complete and required to preserve the critical path.

**SHOULD**

Work that materially improves robustness, quality, or demonstration value but may be deferred if the MUST work is at risk.

**OPTIONAL**

Work that may be implemented only if the critical path is healthy and time remains.

**CUT-FIRST**

Work explicitly sacrificed first when the schedule slips. Cutting these items must not compromise the permanent safety boundary, alarm correlation, Bayesian/evidence-weighted RCA, alternative-cause elimination, confidence/abstention, ExplainabilityTrace, human verification, or the deterministic demo-safe fallback.

Objective:
Freeze + evaluation + demo.

Perform:

- scenario execution,
- metrics,
- regression tests,
- failure tests,
- final integration,
- demo rehearsal,
- documentation check.

## 23. DEMO-SAFE FALLBACK ARCHITECTURE

The core demonstration must have a deterministic offline path.

If:

- LLM API is unavailable,
- vector retrieval fails,
- network access fails,
- external dataset is unavailable,
the deterministic RCA demonstration must still execute.

The system must clearly indicate degraded functionality.

It must NEVER pretend that an unavailable subsystem succeeded.

Fallback examples:

LLM unavailable:
Use deterministic structured explanation renderer.

RAG unavailable:
Use local versioned knowledge corpus.

External dataset unavailable:
Use deterministic synthetic scenario dataset.

Database unavailable:
Use explicitly documented demo-mode persistence only if the architecture supports it.

Do not hide degraded mode.


## 24. FULL DEVELOPMENT ROADMAP

After the 30-hour plan, create:

LEVEL 1 — FOUNDATION

LEVEL 2 — CORE DIAGNOSTIC ENGINE

LEVEL 3 — AI / RAG / RCA REASONING

LEVEL 4 — USER INTERACTION

LEVEL 5 — VALIDATION

LEVEL 6 — DEMONSTRATION

LEVEL 7 — PRODUCTION-READINESS ROADMAP

For every feature classify:

**MUST HAVE**

**SHOULD HAVE**

**COULD HAVE**

**FUTURE**

**DO NOT BUILD**


## 25. FILE-LEVEL IMPLEMENTATION MAP

Create:

docs/implementation/FILE_LEVEL_IMPLEMENTATION_MAP.md

Use a table:

| File | Responsibility | Phase | Depends On | Main Classes/Functions | Tests |
|------|----------------|-------|------------|------------------------|-------|

Include:

- pipeline,
- simulator,
- knowledge,
- API,
- DB,
- dashboard,
- tests,
- scenarios,
- configuration,
- RAG corpus,
- documentation.
Do not create arbitrary files merely to make the architecture look large.


## 26. DATA CONTRACTS

Create:

docs/implementation/DATA_CONTRACTS.md

Define typed conceptual schemas for:

TelemetrySample
Event
Alarm
SignalFeature
Anomaly
FaultEpisode
EvidenceItem
Hypothesis
RCAResult
RetrievedDocument
ConfidenceResult
ExplainabilityTrace
TechnicianReview
ValidatedOutcome

For each specify:

- fields,
- field types,
- required/optional,
- validation,
- provenance,
- relationships,
- version information.
Avoid loosely typed dictionaries when typed models provide clear value.


## 27. RCA EVIDENCE CONTRACT

Every hypothesis must explain:

WHY_IT_IS_SUPPORTED

WHY_IT_IS_NOT_SUPPORTED

WHAT_EVIDENCE_IS_MISSING

WHAT_ALTERNATIVES_EXIST

WHY_ALTERNATIVES_WERE_DOWNGRADED

WHAT_CONFIDENCE_IS_JUSTIFIED

WHAT_ADDITIONAL_EVIDENCE_WOULD_RESOLVE_UNCERTAINTY

Every evidence item must be traceable.


## 28. SAFETY BOUNDARY ENFORCEMENT

Create a dedicated section:

"Safety Boundary Enforcement"

Allowed:

- observe,
- analyze,
- correlate,
- retrieve,
- rank,
- explain,
- recommend verification,
- record human decisions.
Not allowed:

- control elevator motion,
- release/engage safety mechanisms,
- override safety circuits,
- unlock doors,
- control brakes,
- perform rescue,
- command an actuator,
- autonomously authorize maintenance action.
The boundary must be visible in:

- APIs,
- service interfaces,
- tool definitions,
- permissions,
- deployment boundaries,
- documentation.
No implementation should expose a control path even "for future use" unless explicitly isolated as non-functional architecture documentation.


## 29. AI SYSTEM FAILURE MODES

Analyze:

1. bad telemetry,
2. missing telemetry,
3. corrupted timestamps,
4. unrelated alarms,
5. alarm cascades,
6. ambiguous evidence,
7. conflicting evidence,
8. RAG retrieval failure,
9. stale knowledge,
10. LLM hallucination,
11. malformed structured output,
12. API timeout,
13. low-confidence diagnosis,
14. wrong Bayesian model,
15. incorrect knowledge entry,
16. technician rejection,
17. database failure,
18. service failure.
For each define:

- detection,
- response,
- fallback,
- user-visible behavior,
- logging,
- audit implication,
- whether diagnosis should be blocked,
- whether the system should abstain.

## 30. DO NOT BUILD LIST

Explicitly evaluate whether the following remain deferred:

- full digital twin,
- physics-informed neural network,
- graph neural network,
- fleet-scale predictive maintenance,
- remaining-useful-life prediction,
- production-scale continual learning,
- autonomous model retraining,
- complex multi-agent swarm,
- production-grade knowledge graph,
- real KONE proprietary data integration,
- direct elevator controller integration,
- autonomous repair,
- safety-control integration,
- unnecessary microservices,
- unnecessary Kubernetes,
- unnecessary event streaming,
- unnecessary production infrastructure.
For each explain WHY it is deferred.


## 31. TECHNICAL DECISION LOG

Create:

docs/implementation/ARCHITECTURE_DECISION_LOG.md

For every major decision provide:

**DECISION**

**ALTERNATIVES**

**WHY CHOSEN**

**TRADE-OFF**

**EVIDENCE FROM PROJECT DOCUMENTS**

**WHEN TO REVISIT**

**CLASSIFICATION**

At minimum cover:

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy/Alembic if used
- synthetic simulator
- Bayesian reasoning
- RAG/vector store
- LLM provider abstraction
- typed structured outputs
- dashboard framework
- Docker
- testing strategy
- orchestration strategy
- logging
- configuration
- deployment model.
Do not select technologies merely because they are fashionable.


## 32. ARCHITECTURE ASSUMPTION REGISTER

Explicitly distinguish:

ARCHITECTURE DECISION

from:

IMPLEMENTATION ASSUMPTION

Example:

Decision:
PostgreSQL is used for MVP persistence.

Assumption:
The exact proprietary KONE telemetry schema is unavailable, so the prototype defines a synthetic telemetry contract.

Do not turn implementation assumptions into facts.


## 33. OPEN QUESTIONS AND UNKNOWNS

Create:

docs/implementation/OPEN_QUESTIONS_AND_UNKNOWNS.md

Track:

- unknown,
- why it matters,
- evidence currently available,
- impact,
- temporary prototype assumption,
- production resolution required.
Examples may include:

- proprietary telemetry schema,
- proprietary alarm semantics,
- proprietary maintenance procedures,
- exact production deployment topology,
- real KONE fault-code mapping,
- production safety certification requirements.
Do not invent answers.


## 34. REQUIREMENTS TRACEABILITY

Create:

docs/implementation/REQUIREMENTS_TRACEABILITY_MATRIX.md

Map:

Project Requirement
↓
Source Document
↓
Architecture Component
↓
Implementation Phase
↓
Test
↓
Acceptance Criterion
↓
Demo Scenario

Every critical requirement should be traceable.


## 35. IMPLEMENTATION QUALITY REQUIREMENTS

Optimize for:

- correctness,
- maintainability,
- modularity,
- testability,
- explainability,
- extensibility,
- reproducibility.
Avoid:

- giant monolithic files,
- hidden global state,
- hard-coded business logic in UI,
- hard-coded probabilities scattered through code,
- direct LLM-to-database mutation,
- untyped cross-module contracts,
- hidden coupling,
- fake agent abstractions,
- unnecessary framework complexity.
Prefer:

- typed Python models,
- pure functions where possible,
- deterministic components,
- dependency injection where appropriate,
- clear service boundaries,
- configuration-driven knowledge,
- explicit provenance,
- automated tests,
- reproducible scenarios,
- versioned knowledge,
- versioned prompts,
- versioned configurations.

## 36. VALIDATION STRATEGY

Validation must begin from the first implementation phase.

For every module define tests immediately.

Required levels:

**UNIT**

**INTEGRATION**

**SCENARIO**

**END-TO-END**

Central evaluation pattern:

**SCENARIO**

↓
GROUND TRUTH
↓
OBSERVED EVIDENCE
↓
SYSTEM OUTPUT
↓
COMPARISON
↓
METRICS
↓
ERROR ANALYSIS

Do not produce invented accuracy numbers.


## 37. DEMONSTRATION-FIRST DESIGN

Every demonstration should communicate:

1. What happened?
2. Which alarms fired?
3. Which alarms were consequential?
4. What evidence changed?
5. What hypotheses were considered?
6. What evidence supports each?
7. What evidence contradicts alternatives?
8. What evidence is missing?
9. What confidence is justified?
10. Did the system abstain?
11. What should the technician verify?
12. What did the technician decide?
The demo must show the reasoning trace, not merely the final answer.


## 38. HUMAN-IN-THE-LOOP WORKFLOW

The implementation plan must define:

SYSTEM DIAGNOSIS
↓
TECHNICIAN REVIEW
↓
ACCEPT / EDIT / REJECT
↓
OPTIONAL CORRECTED ROOT CAUSE
↓
OPTIONAL CORRECTED ACTION
↓
REVIEW NOTES
↓
VALIDATED OUTCOME
↓
AUDIT RECORD

The human decision must remain distinguishable from the AI recommendation.


## 39. CONTROLLED CORRECTIVE-ACTION MODEL

The system may recommend verification actions and controlled corrective actions only from the versioned knowledge layer.

Architecture:

RCA
↓
Recommended Verification
↓
Controlled Corrective-Action Knowledge
↓
Human Review

The LLM may explain or summarize a controlled recommendation.

The LLM may NOT author a new maintenance procedure.


## 40. SECURITY BOUNDARY

The implementation plan must address:

- authentication where required,
- authorization,
- least privilege,
- secrets management,
- input validation,
- prompt injection resistance,
- retrieval poisoning resistance,
- untrusted document handling,
- API security,
- audit logging,
- database access control,
- network boundaries,
- LLM tool restrictions.
Retrieved documents must be treated as untrusted data.

Never allow retrieved content to redefine system instructions or safety boundaries.


## 41. DATABASE MODEL

The plan must define a minimal schema for:

- elevators,
- telemetry/events,
- alarms,
- fault episodes,
- investigations,
- evidence,
- hypotheses,
- retrieved sources,
- diagnoses,
- technician reviews,
- validated outcomes,
- audit records.
Avoid enterprise-scale schema complexity.

Explain:

- relationships,
- indexes,
- retention considerations,
- provenance,
- versioning.

## 42. API CONTRACT

Define the minimum API surface.

At minimum consider:

GET /health

GET /fault-episodes

GET /fault-episodes/{id}

GET /explainability/{id}

POST /diagnosis/{id}/review

Potentially:

GET /investigations/{id}

GET /investigations/{id}/evidence

GET /investigations/{id}/hypotheses

Only include endpoints that are justified.

The API must expose diagnostic capabilities, NOT elevator-control capabilities.


## 43. LOGGING AND OBSERVABILITY

Define structured logging for:

- investigation ID,
- fault episode ID,
- scenario ID,
- correlation ID,
- pipeline stage,
- latency,
- errors,
- fallback activation,
- LLM calls,
- retrieval calls,
- abstentions,
- technician reviews.
Do not log secrets.


## 44. OFFLINE / DEGRADED OPERATION

Define behavior when:

- database unavailable,
- LLM unavailable,
- vector store unavailable,
- external dataset unavailable,
- malformed telemetry,
- missing evidence,
- configuration invalid.
Every degraded mode must be explicit.

Never silently produce apparently authoritative results from incomplete systems.


## 45. TECHNICAL DEBT POLICY

For every hackathon simplification, identify:

- what is simplified,
- why,
- risk,
- acceptable for prototype?,
- production replacement,
- trigger for revisiting.
Do not allow temporary prototype shortcuts to become undocumented architecture.


## 46. FINAL REQUIRED PLANNING ARTIFACTS

Create these files:

1.
docs/implementation/MASTER_IMPLEMENTATION_PLAN.md

2.
docs/implementation/ARCHITECTURE_DECISION_LOG.md

3.
docs/implementation/PHASE_DEPENDENCY_MAP.md

4.
docs/implementation/FILE_LEVEL_IMPLEMENTATION_MAP.md

5.
docs/implementation/DATA_CONTRACTS.md

6.
docs/implementation/TESTING_AND_VALIDATION_PLAN.md

7.
docs/implementation/30_HOUR_HACKATHON_PLAN.md

8.
docs/implementation/DEMO_EXECUTION_PLAN.md

9.
docs/implementation/RESOLVED_DESIGN_CONFLICTS.md

10.
docs/implementation/REQUIREMENTS_TRACEABILITY_MATRIX.md

11.
docs/implementation/OPEN_QUESTIONS_AND_UNKNOWNS.md

12.
docs/implementation/DATASET_USAGE_MATRIX.md

Do NOT modify production/source code.


## 47. MASTER IMPLEMENTATION PLAN FORMAT

The main plan MUST contain:

# KONE Elevate — Master Implementation Plan

## 1. Executive Technical Summary

## 2. Project Understanding

## 3. Source-of-Truth Hierarchy

## 4. Source Availability and Evidence Classification

## 5. Final MVP Definition

## 6. System Boundary

## 7. Core Architecture

## 8. End-to-End Data Flow

## 9. Reasoning Flow

## 10. Dataset Strategy

## 11. Evidence Provenance Strategy

## 12. Phase-by-Phase Implementation Plan

### Phase 0
### Phase 1
### Phase 2
...
### Phase 16

For every phase include:

- Goal
- Inputs
- Outputs
- Dependencies
- Files
- Interfaces
- Algorithms
- Tasks
- Tests
- Acceptance criteria
- Risks
- Safety
- Security
- Demo value
- Definition of Done
## 13. Critical Path

## 14. Parallel Development Tracks

## 15. 30-Hour Build Plan

## 16. Full Prototype Roadmap

## 17. File-Level Architecture

## 18. Data Contracts

## 19. Database Model

## 20. API Contract

## 21. AI / RAG / RCA Contract

## 22. Explainability Model

## 23. Human-in-the-Loop Workflow

## 24. Safety Boundary

## 25. Security Boundary

## 26. Failure and Degraded-Mode Strategy

## 27. Testing Strategy

## 28. Evaluation Metrics

## 29. Demonstration Scenarios

## 30. Dataset Usage

## 31. Known Risks

## 32. Technical Debt and Prototype Simplifications

## 33. Deferred Features

## 34. Features That Must Never Be Built in the Prototype

## 35. Technical Decision Log

## 36. Open Questions and Unknowns

## 37. Requirements Traceability

## 38. Final Definition of Done


## 48. FINAL DEFINITION OF DONE

Define a complete Definition of Done for the prototype.

The prototype is considered complete only when:

- source requirements are traceable,
- architecture is implemented consistently,
- simulator is reproducible,
- fault injection has ground truth,
- anomaly detection works,
- alarm correlation works,
- FaultEpisode exists,
- evidence is provenance-aware,
- engineering knowledge is versioned,
- RCA produces evidence-weighted hypotheses,
- correlated evidence is handled appropriately,
- alternatives can be downgraded/eliminated,
- confidence is distinct from posterior probability,
- abstention works,
- RAG is grounded,
- LLM is constrained,
- ExplainabilityTrace is generated,
- human review works,
- API works,
- UI works sufficiently for demonstration,
- safety boundary is enforced,
- security boundary is enforced,
- tests pass,
- scenario evaluation runs,
- actual metrics are generated,
- no fabricated metrics exist,
- demo scenarios work,
- offline/degraded fallback works,
- reproducibility information is recorded,
- documentation is complete,
- another developer can reproduce the project.

## 49. FINAL BEHAVIORAL RULES

**DO NOT:**

- invent KONE internal architectures,
- claim undocumented KONE capabilities do not exist,
- treat "not publicly documented" as "does not exist",
- fabricate performance metrics,
- fabricate real KONE telemetry,
- fabricate proprietary fault-code mappings,
- fabricate KONE manuals,
- claim production readiness,
- claim safety certification,
- claim autonomous operation,
- turn synthetic data into real-world validation,
- build unnecessary complexity,
- create a multi-agent swarm without justification,
- introduce unnecessary infrastructure,
- allow the LLM to become the diagnostic authority,
- let retrieved documents override system safety instructions,
- let LLM output directly mutate authoritative state.
**DO:**

- preserve source classifications,
- preserve provenance,
- preserve uncertainty,
- document assumptions,
- document conflicts,
- document unknowns,
- document prototype simplifications,
- validate every module,
- maintain reproducibility,
- protect the critical path,
- optimize for a working explainable RCA prototype.

## 50. SPECIAL INSTRUCTION FOR CONFLICTS

If two source documents disagree:

DO NOT silently choose.

Create:

docs/implementation/RESOLVED_DESIGN_CONFLICTS.md

For every conflict:

1. Conflict
2. Source A
3. Source B
4. Final position
5. Reason
6. Implementation impact
7. Classification
If unresolved:

OPEN DECISION REQUIRED


## 51. SPECIAL INSTRUCTION FOR IMPLEMENTATION ORDER

Prioritize:

FOUNDATIONAL CORRECTNESS
before
CORE DIAGNOSTIC REASONING
before
AI AUGMENTATION
before
UI POLISH

The prototype must become progressively demonstrable.

Target progression:

M0:
Architecture/contract freeze

M1:
Repository boots

M2:
Synthetic elevator produces normal telemetry

M3:
Fault injection works

M4:
Anomaly detection works

M5:
Alarm correlation works

M6:
RCA works

M7:
Confidence/abstention works

M8:
RAG works

M9:
LLM explanation works

M10:
Human review works

M11:
Dashboard works

M12:
Evaluation works

M13:
End-to-end demonstration works


## 52. THINK LIKE A LEAD ENGINEER

Before proposing any implementation task, ask:

- What depends on it?
- What depends on it being correct?
- How will it be tested?
- How can it fail?
- Can the next phase work without it?
- Is it MVP-critical?
- Can it be simplified?
- Is the complexity justified?
- Does it preserve the safety boundary?
- Does it preserve evidence provenance?
- Does it preserve reproducibility?
- Does it improve the core RCA demonstration?
- Does it introduce unnecessary coupling?
- Does it turn an assumption into an undocumented fact?
Do not optimize for number of components.

Optimize for:

A WORKING
EXPLAINABLE
TESTABLE
REPRODUCIBLE
EVIDENCE-DRIVEN
SAFETY-BOUNDED
RCA PROTOTYPE.


## PLANNING COMPLETION GATE

Do not stop merely because the planning files have been written. Before executing the final response, verify ALL of the following:

[ ] All required source documents were inspected or explicitly marked unavailable/unreadable.
[ ] The actual workspace/repository CURRENT STATE was inspected.
[ ] CURRENT STATE, DOCUMENTED INTENT, and TARGET STATE are clearly separated.
[ ] The staged inspection process was completed and the source map is internally consistent.
[ ] Source hierarchy and source classifications were applied.
[ ] All material design conflicts were resolved or marked OPEN DECISION REQUIRED.
[ ] MVP scope is explicitly frozen, including build/defer/never boundaries.
[ ] Final target architecture is defined.
[ ] Data contracts and interfaces are defined.
[ ] Dataset access, usage basis, technical relevance, and ground-truth suitability were verified or explicitly marked unknown.
[ ] Evidence provenance classes and probability provenance are defined.
[ ] Phase dependencies and the critical path are defined.
[ ] Parallel workstreams are defined.
[ ] Every 30-hour block contains MUST / SHOULD / OPTIONAL / CUT-FIRST priorities.
[ ] Testing and validation strategy is defined without invented metrics.
[ ] Demo scenarios and demo-safe fallback behavior are defined.
[ ] Safety and security boundaries are explicitly enforced.
[ ] Failure modes, degraded modes, abstention behavior, and human-review behavior are defined.
[ ] All required planning artifacts are created under docs/implementation/.
[ ] Planning artifacts are mutually consistent.
[ ] NO application/source code, simulator code, tests outside planning artifacts, migrations, API/UI implementation, Docker, dependency manifests, CI/CD, or application environment configuration was modified.
[ ] No executable application code was created.

Only after every applicable gate item is satisfied may the agent provide the final planning summary and STOP.


## 53. FINAL ACTION

Perform the complete repository/document analysis NOW.

Execution order:

STEP 1
Verify source availability.

STEP 2
Inspect the required documents and relevant repository material using the STAGED DOCUMENT INSPECTION STRATEGY. Do not assume all sources must be loaded simultaneously.

STEP 3
Construct the source hierarchy.

STEP 4
Identify conflicts.

STEP 5
Construct the project architecture model.

STEP 6
Identify datasets, verify access/relevance/usage basis, and establish evidence and probability provenance.

STEP 7
Define MVP scope.

STEP 8
Define contracts and interfaces.

STEP 9
Define implementation phases.

STEP 10
Define dependencies and critical path.

STEP 11
Define parallel workstreams.

STEP 12
Define the 30-hour plan.

STEP 13
Define validation and evaluation.

STEP 14
Define demo scenarios.

STEP 15
Define safety/security boundaries.

STEP 16
Define failure and degraded modes.

STEP 17
Create all required planning artifacts.

STEP 18
Verify that NO application/source code was modified.

STEP 19
Perform a consistency review across all planning documents.

STEP 20
Run the PLANNING COMPLETION GATE. If any required item fails, fix the planning artifacts before proceeding.

STEP 21
Provide the requested executive summary.

THEN STOP.


## 54. REQUIRED FINAL RESPONSE TO THE USER

After creating the planning artifacts, respond with:

1. A concise executive summary of your understanding.
2. The final architecture the implementation plan follows.
3. The phase-by-phase roadmap.
4. The critical path.
5. The 30-hour plan.
6. The major technical decisions.
7. The key risks.
8. The dataset strategy.
9. The major resolved design conflicts.
10. The exact first implementation milestone.
11. The list of planning artifacts created.
12. Confirmation that application/source code was NOT implemented or modified.
Then STOP.

Do NOT continue into implementation.

Do NOT generate application source code.

Wait for my next instruction.


## 55. STANDARD OF QUALITY

The final planning package must satisfy this standard:

"An experienced software engineer should be able to open MASTER_IMPLEMENTATION_PLAN.md and begin implementation without having to rediscover the project's architecture, requirements, dependencies, scope, data contracts, testing strategy, safety boundaries, or implementation order."

The plan must optimize for:

CORRECTNESS
+
ENGINEERING QUALITY
+
TRACEABILITY
+
REPRODUCIBILITY
+
EXPLAINABILITY
+
SAFETY
+
DEMONSTRABILITY

NOT:

number of files,
number of agents,
number of frameworks,
number of AI components,
or architectural complexity.


## END OF MASTER PROMPT
