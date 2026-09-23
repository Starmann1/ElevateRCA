# KONE Elevate — Master Implementation Plan

## 1. Executive Technical Summary

KONE Elevate is an **evidence-driven diagnostic intelligence layer** for modern gearless traction elevators (KONE MonoSpace/MiniSpace with EcoDisc PMSM motors). It performs **structured, multi-hypothesis Root Cause Analysis (RCA)** that:
- Correlates cascading alarm floods into single fault episodes
- Evaluates 6-9 competing physical hypotheses per fault using Bayesian inference
- Explicitly eliminates alternative causes using negative evidence
- Provides calibrated confidence with principled abstention when evidence is insufficient
- Generates auditable ExplainabilityTrace artifacts linking every claim to sensor data and engineering documentation
- Operates strictly as a read-only advisory system outside the elevator safety-control loop

**What it IS NOT**: autonomous elevator control, predictive maintenance, digital twin, generic chatbot, or fleet analytics dashboard.

**Tech Stack**: Python 3.12, FastAPI, PostgreSQL, pgmpy (Bayesian networks), ChromaDB (RAG), Anthropic Claude (LLM), React/Streamlit (UI), Docker Compose.

**CURRENT STATE**: Repository contains only the master prompt and 16 source documents. Zero application code exists.

**TARGET STATE**: A fully demonstrable prototype running 5 scenarios end-to-end within a 30-hour hackathon.

---

## 2. Project Understanding

### The Problem
Modern elevators generate cascading alarm floods where a single root cause triggers 3-5 consequential alarms across subsystems. Current diagnostic approaches treat each alarm independently, leading to:
- Misdiagnosis (treating symptoms as root causes)
- Unnecessary part replacements
- Extended Mean Time to Repair (MTTR)
- Repeat service visits / callbacks

### The Innovation
ElevateRCA bridges the gap between alarm detection (Level 2-3 maturity) and structured diagnostic intelligence (Level 5-6):
- **Level 3-4** (industry standard): IoT connectivity, predictive maintenance, threshold alerting
- **Level 5-6** (ElevateRCA target): Multi-hypothesis RCA with evidence evaluation, alternative elimination, confidence calibration, and principled abstention

### 5 Defensible Differentiators
1. Causal alarm cascade correlation
2. Explicit multi-hypothesis reasoning space
3. Visible alternative-cause elimination with negative evidence
4. Auditable ExplainabilityTrace provenance
5. Calibrated confidence with principled abstention

### What We Cannot Claim (Claim Discipline)
- Cannot claim "KONE has no RCA" — only "not publicly established"
- Cannot claim specific cost savings or downtime reductions (unvalidated hypotheses)
- Cannot claim safety certification
- Cannot claim production readiness

---

## 3. Source-of-Truth Hierarchy

| Tier | Document | Role | Resolution Rule |
|------|----------|------|-----------------|
| 1 | Phase 12: Final Synthesis | Highest authority, final project definition | Overrides all lower tiers |
| 2 | Technical Architecture Guidebook | Implementation baseline | Prefer concrete details if consistent with Tier 1 |
| 3 | Phase 10: Scope/Prioritization/MVP | MVP scope decisions | Scope boundaries are authoritative |
| 4 | Phases 1-11 | Engineering/domain context | Supporting detail only |
| 5 | Idea Proposal + Project Understanding Report | Original intent | Context only; superseded by later phases |
| 6 | Research Source Library | Provenance/references | Reference only |

Note: The Idea Proposal PDF (Tier 5) is UNREADABLE by text tools (binary PDF). Recorded as unavailable source.

---

## 4. Source Availability and Evidence Classification

### Source Availability (16 documents)
| # | Document | Size | Status |
|---|----------|------|--------|
| 1 | KONE_Elevate_Phase12_Final_Synthesis_Master_Reference.md | 78 KB | INSPECTED |
| 2 | KONE_Elevate_Technical_Architecture_Guidebook.md | 91 KB | INSPECTED |
| 3 | KONE_Elevate_Phase10_Scope_Prioritization_MVP.md | 76 KB | INSPECTED |
| 4 | KONE_Elevate_Phase1_Elevator_Engineering.md | 73 KB | INSPECTED |
| 5 | KONE_Elevate_Phase2_Fault_Codes_and_Alarms.md | 75 KB | INSPECTED |
| 6 | KONE_Elevate_Phase3_KONE_Ecosystem.md | 81 KB | INSPECTED |
| 7 | KONE_Elevate_Phase4_Competitive_Landscape.md | 76 KB | INSPECTED |
| 8 | KONE_Elevate_Phase5_RCA_Reliability_Engineering.md | 96 KB | INSPECTED |
| 9 | KONE_Elevate_Phase6_Signal_Processing_Anomaly_Detection.md | 93 KB | INSPECTED |
| 10 | KONE_Elevate_Phase7_AI_GenAI_RAG_MultiAgent.md | 107 KB | INSPECTED |
| 11 | KONE_Elevate_Phase8_Safety_Cybersecurity_Deployment.md | 107 KB | INSPECTED |
| 12 | KONE_Elevate_Phase9_Validation_Evaluation_Demonstration.md | 98 KB | INSPECTED |
| 13 | KONE_Elevate_Phase10_Scope_Prioritization_MVP.md | 76 KB | INSPECTED |
| 14 | KONE_Elevate_Phase11_Competitive_Differentiation_Strategic_Value.md | 70 KB | INSPECTED |
| 15 | KONE_Elevate_Project_Understanding_Report.md | 37 KB | INSPECTED |
| 16 | KONE_Elevate_Research_Source_Library.md | 91 KB | INSPECTED |
| 17 | KONE Elevate Idea Proposal- Arul G (final).pdf | 2.5 MB | **UNREADABLE** (binary PDF) |

### Evidence Classification Types
- **DOCUMENTED FACT**: Explicitly stated in source documents
- **ENGINEERING INFERENCE**: Derived from engineering principles using documented facts
- **PROJECT PROPOSAL**: Decisions made for this prototype
- **PROTOTYPE SIMPLIFICATION**: Simplified from documented intent for time constraints
- **PUBLIC RESEARCH FACT**: From referenced academic papers or standards
- **SYNTHETIC/ILLUSTRATIVE**: Example values for methodology demonstration
- **FUTURE CAPABILITY**: Deferred to post-MVP
- **UNKNOWN**: Information not available from any source
- **OPEN DECISION**: Requires human judgment call

---

## 5. Final MVP Definition

### MUST HAVE (Non-negotiable even in 3-day build)
- Telemetry ingestion with schema validation
- Signal processing (EWMA/CUSUM anomaly detection)
- Alarm correlation (primary vs consequential classification)
- Fault trees (6 subsystems) and FMEA knowledge base
- Bayesian posterior probability ranking across competing hypotheses
- Evidence trace with supporting AND contradicting evidence
- Confidence scoring with principled abstention
- Source-grounded explanations (no unverified claims)
- Deterministic boundary (LLM cannot compute math or safety decisions)
- Human review workflow (technician accept/edit/reject)
- Safety isolation (zero control path to elevator)

### SHOULD HAVE
- Curated RAG over synthetic troubleshooting corpus
- LLM synthesis (3 touchpoints: extraction, arbitration, rendering)
- Demo scenarios 2-5 (beyond the core overcurrent scenario)
- Dashboard UI (React or Streamlit)

### NEVER BUILD (Prototype)
- Autonomous elevator control
- Generic chatbot / open-ended Q&A
- Predictive maintenance / Remaining Useful Life
- Digital twin / multibody simulation
- Graph Neural Networks or PINN
- Fleet dashboards / mobile app
- Multi-agent framework (LangGraph, AutoGen, CrewAI)
- Kafka / event streaming infrastructure

### 9-Step Minimum Demo Sequence (None Optional)
1. Ingest telemetry
2. Detect anomaly
3. Correlate alarm cascade
4. Retrieve engineering knowledge
5. Generate hypotheses from fault tree
6. Evaluate evidence for/against
7. Eliminate alternatives
8. Score confidence or abstain
9. Present to human reviewer

---

## 6. System Boundary

```
┌─────────────────────────────────────────────┐
│          ELEVATOR SAFETY SYSTEM             │
│  Hardware Safety Chain · Safety Gear        │
│  Overspeed Governor · Door Interlocks       │
│  Mechanical Brakes · PESSRAL Controller     │
└──────────────────┬──────────────────────────┘
                   │ ONE-WAY READ-ONLY
                   │ OBSERVATIONAL DATA
                   ▼
┌─────────────────────────────────────────────┐
│       DIAGNOSTIC INTELLIGENCE LAYER         │
│  (ElevateRCA - THIS SYSTEM)                 │
│  Triage → Correlate → Retrieve → Reason     │
│  → Explain → Abstain-or-Recommend           │
└──────────────────┬──────────────────────────┘
                   │ ADVISORY ONLY
                   ▼
┌─────────────────────────────────────────────┐
│          HUMAN TECHNICIAN                   │
│  Physical Inspection · Verification         │
│  Manual Authorization of Actions            │
└─────────────────────────────────────────────┘
```

Absolute prohibitions: No motor control, no door actuation, no brake manipulation, no safety chain bypass, no autonomous fault resets, no passenger rescue automation, no unilateral work order dispatch.

---

## 7. Core Architecture

Single-pipeline orchestrator with tool-calling (NOT multi-agent swarm).

```
Simulator → Ingestion → Signal Triage (EWMA/CUSUM) → Alarm Correlation
→ Knowledge Retrieval (Fault Trees + FMEA + RAG) → Bayesian RCA (pgmpy)
→ LLM Arbitration → Confidence/Abstention → Synthesis → ExplainabilityTrace
→ Human Review → ValidatedOutcome
```

Core Pipeline Class (from Guidebook §T):
```python
class Pipeline:
    def run(self, episode: FaultEpisode) -> ExplainabilityTrace:
        frame = orchestrator.extract(episode)       # LLM call #1
        evidence = retrieval.gather(frame)           # deterministic + RAG
        hypotheses = rca.diagnose(evidence)           # BN + LLM call #2
        recommendation = synthesis.render(hypotheses) # lookup + LLM call #3
        trace = explainability.assemble(frame, evidence, hypotheses, recommendation)
        return trace
```

32-component architecture. 3 LLM touchpoints. 5 subsystem simulators. 6 fault trees. 10 fault injection types. 5 demo scenarios.

---

## 8. End-to-End Data Flow

Describe the complete data flow from raw sensor reading to technician action:

1. **Raw Telemetry** (TelemetrySample): timestamp, elevator_id, signal_name, value, unit, quality, operating_state
2. **Signal Triage**: EWMA baseline tracking + CUSUM changepoint → AnomalyScore (z_score, sustained_deviation, anomaly_score)
3. **Alarm Generation**: Threshold violation → AlarmEvent (alarm_type, severity, subsystem)
4. **Alarm Correlation**: ISA-18.2 rationalization within 15s window + causal link graph → FaultEpisode (primary + consequential alarms)
5. **Orchestration**: LLM call #1 extracts structured InvestigationFrame from episode
6. **Evidence Retrieval**: SQL queries (telemetry history, maintenance records) + Chroma RAG (troubleshooting docs) → EvidenceBundle
7. **Bayesian RCA**: pgmpy VariableElimination inference over fault tree → ranked HypothesisEvaluation list
8. **LLM Arbitration**: LLM call #2 checks BN top hypothesis against non-network evidence → ArbitrationResult
9. **Confidence Decision**: decide() → HIGH/MEDIUM/LOW tier or ABSTAIN
10. **Synthesis**: corrective_actions.yaml lookup + LLM call #3 → TechnicianView + ManagerView
11. **ExplainabilityTrace Assembly**: Pure function combining all intermediate outputs
12. **Human Review**: POST /diagnosis/{id}/review → ValidatedOutcome written to DB

---

## 9. Reasoning Flow

The 10-step RCA reasoning loop (from Phase 5):
1. OBSERVE: Detect anomalous signals and alarm events
2. CONTEXTUALIZE: Identify operating state, load, environmental conditions
3. GENERATE HYPOTHESES: Traverse fault tree to enumerate candidate causes
4. COLLECT EVIDENCE: Retrieve telemetry features, maintenance history, technical documentation
5. TEST HYPOTHESES: For each hypothesis, check expected vs observed evidence
6. ELIMINATE INCONSISTENT CAUSES: Apply 4-step elimination discipline
7. UPDATE PROBABILITIES: Bayesian posterior update via pgmpy
8. RANK ROOT CAUSES: Order by posterior probability
9. VERIFY: LLM arbitration checks for contradictions
10. CONCLUDE OR ABSTAIN: High confidence → recommend; Low confidence → explicit abstention

Alternative Cause Elimination Discipline (for every hypothesis):
1. What evidence would we expect if this hypothesis were true?
2. Is that evidence present?
3. What evidence would contradict this hypothesis?
4. Is contradictory evidence present?

Negative evidence handling (4 distinct states):
- True negative: Sensor measured normally (informative)
- Missing data: Sensor reading unrecorded (zero diagnostic value)
- Unreliable sensor: Sensor in degraded state
- Unobserved: No sensor exists for this condition

---

## 10. Dataset Strategy

See companion document: DATASET_USAGE_MATRIX.md

Critical fact: There is only ONE real public elevator dataset (Huawei Door Dataset). All other datasets are analogous stand-ins from rotating machinery (CWRU, IMS bearings) or power electronics (NASA IGBT). The primary mechanism for controlled end-to-end RCA validation is the synthetic simulator.

Datasets:
| Dataset | Real Elevator? | Accessible? | Used For | Causal RCA Ground Truth? |
|---------|---------------|-------------|----------|-------------------------|
| Huawei Door | YES | YES | Door degradation validation | NO |
| CWRU Bearing | NO | YES | Vibration algorithm validation | NO |
| NASA IGBT | NO | YES | Drive failure physics | NO |
| NASA IMS | NO | YES | Progressive degradation reference | NO |
| C-MAPSS | NO | YES | Methodology reference only | NO |
| Synthetic Scenarios | N/A | Generated | Primary E2E RCA validation | YES |

All synthetic data must be honestly labeled as synthetic.
All Bayesian priors must be documented as illustrative engineering estimates, not validated fleet statistics.

---

## 11. Evidence Provenance Strategy

Evidence Provenance Classes:
- **CLASS A — Synthetic Ground Truth**: Generated by controlled simulator with known injected faults
- **CLASS B — Public Real-World Dataset**: External real-world data (Huawei Door, CWRU, NASA)
- **CLASS C — Project-Authored Engineering Knowledge**: Fault trees, FMEA, causal links (derived from public engineering knowledge)
- **CLASS D — Public Engineering Documentation**: Research papers, safety standards, OEM technical guides
- **CLASS E — KONE-Specific Source**: Publicly documented KONE information
- **CLASS F — Unknown / Unavailable**: Proprietary KONE data not accessible

Probability Provenance: Every probability value in the system must have documented provenance:
- Prior probabilities: CLASS C (engineering-reasoned estimates, not empirical fleet data)
- Conditional probability tables (CPTs): CLASS C (illustrative, calibratable when real data available)
- Confidence thresholds (0.75, 0.45): CLASS C (engineering decision boundaries)

---

## 12. Phase-by-Phase Implementation Plan

### Phase 0: Repository Scaffold & Environment
- **Goal**: Initialize project structure, set up linters, formatters, and Docker environment.
- **Inputs**: Requirements from Technical Architecture Guidebook.
- **Outputs**: Empty project structure, pyproject.toml, requirements.txt, Docker compose file.
- **Dependencies**: None.
- **Files**: `pyproject.toml`, `requirements.txt`, `docker-compose.yml`, `.gitignore`, `Makefile`.
- **Interfaces**: N/A
- **Algorithms**: N/A
- **Tasks**: Create directories, set up virtual environment, configure git, write Makefile commands.
- **Tests**: `make check` should pass on empty structure.
- **Acceptance Criteria**: Developer can run `make setup` and `make test` successfully.
- **Risks**: Version conflicts in dependencies (Python 3.12, pydantic, pgmpy).
- **Safety**: No safety implications.
- **Security**: Ignore `.env` files.
- **Demo Value**: Foundation for all other tasks.
- **Definition of Done**: [ ] Scaffold complete and CI/CD tools configured.

### Phase 1: Database Schema & Migrations
- **Goal**: Establish the relational model in PostgreSQL using SQLAlchemy.
- **Inputs**: Data contracts from architecture guidebook.
- **Outputs**: SQLAlchemy models and Alembic migrations.
- **Dependencies**: Phase 0.
- **Files**: `elevate/db/models.py`, `elevate/db/session.py`, `alembic/`.
- **Interfaces**: DB interactions for CRUD operations on telemetry, alarms, episodes.
- **Algorithms**: N/A
- **Tasks**: Write Pydantic schemas, convert to SQLAlchemy models, generate migrations.
- **Tests**: DB insert/query roundtrip tests using pytest-postgresql.
- **Acceptance Criteria**: Can create records for TelemetrySample and FaultEpisode.
- **Risks**: Schema mismatch with data contracts.
- **Safety**: N/A
- **Security**: Secure connection strings.
- **Demo Value**: Persistent storage for demo states.
- **Definition of Done**: [ ] Migrations run cleanly on fresh DB.

### Phase 2: Elevator Simulator & Fault Injection
- **Goal**: Build a deterministic synthetic data generator for KONE elevator physics and faults.
- **Inputs**: Phase 1_Elevator_Engineering knowledge.
- **Outputs**: A Python generator yielding TelemetrySample and AlarmEvent.
- **Dependencies**: Phase 0, Phase 1.
- **Files**: `elevate/simulator/engine.py`, `elevate/simulator/faults.py`.
- **Interfaces**: `generate_scenario(scenario_id) -> Iterator[TelemetrySample]`.
- **Algorithms**: Kinematic profiles (jerk, acceleration), thermal decay curves, vibration synthesis.
- **Tasks**: Implement normal operation profile, implement 5 fault injection profiles.
- **Tests**: Assert signal bounds during normal and fault states.
- **Acceptance Criteria**: Simulator outputs timestamped data reflecting valid physics.
- **Risks**: Math complexity causing simulator drift.
- **Safety**: N/A
- **Security**: N/A
- **Demo Value**: Provides the exact data needed to run the 5 demo scenarios.
- **Definition of Done**: [ ] Can generate all 5 fault scenarios as CSV or DB inserts.

### Phase 3: Signal Triage (EWMA/CUSUM)
- **Goal**: Detect anomalies in incoming continuous telemetry streams.
- **Inputs**: Telemetry samples from simulator.
- **Outputs**: AnomalyScore structures identifying deviations.
- **Dependencies**: Phase 2.
- **Files**: `elevate/triage/anomaly.py`.
- **Interfaces**: `detect(signal_series) -> List[AnomalyScore]`.
- **Algorithms**: EWMA (Exponentially Weighted Moving Average) for baseline, CUSUM for changepoint detection.
- **Tasks**: Implement EWMA tracking, implement CUSUM bounds check, write thresholds.
- **Tests**: Verify detection of step changes and gradual drifts in synthetic data.
- **Acceptance Criteria**: Reliably flags the fault injection start time within 2 seconds.
- **Risks**: False positive alerts tuning.
- **Safety**: N/A
- **Security**: N/A
- **Demo Value**: Demonstrates early detection before cascading failures.
- **Definition of Done**: [ ] Anomaly events correctly trigger on synthetic anomalies.

### Phase 4: Alarm Correlation Engine
- **Goal**: Group related alarms into single FaultEpisodes.
- **Inputs**: Streams of AlarmEvents and AnomalyScores.
- **Outputs**: Consolidated FaultEpisode.
- **Dependencies**: Phase 3.
- **Files**: `elevate/correlation/engine.py`.
- **Interfaces**: `correlate(alarms, time_window=15) -> FaultEpisode`.
- **Algorithms**: Time-window grouping (ISA-18.2 logic), topology-based causal linking.
- **Tasks**: Implement sliding window grouper, identify primary vs consequential alarm.
- **Tests**: Given a flood of 5 alarms, successfully identify the primary trigger.
- **Acceptance Criteria**: Outputs a single FaultEpisode per injected fault.
- **Risks**: Edge cases where alarms span multiple windows.
- **Safety**: N/A
- **Security**: N/A
- **Demo Value**: Solves the "alarm flood" problem visually.
- **Definition of Done**: [ ] Groups 3+ alarms into 1 episode reliably.

### Phase 5: Engineering Knowledge Base
- **Goal**: Codify the fault trees and FMEA tables into structured data.
- **Inputs**: Technical architecture and Phase 5 RCA documents.
- **Outputs**: JSON/YAML fault trees, Python classes for inference.
- **Dependencies**: Phase 0.
- **Files**: `elevate/knowledge/fault_trees.yaml`, `elevate/knowledge/loader.py`.
- **Interfaces**: `get_fault_tree(subsystem) -> Dict`.
- **Algorithms**: Graph traversal (DFS/BFS) for tree extraction.
- **Tasks**: Write YAML for 6 subsystems, build loader, define causal priors.
- **Tests**: Validate schema of all loaded YAML files.
- **Acceptance Criteria**: Can parse all 6 fault trees without errors.
- **Risks**: Missing priors or disjoint logic.
- **Safety**: Accurate representation of engineering knowledge.
- **Security**: N/A
- **Demo Value**: Provides the domain expertise underlying the RCA.
- **Definition of Done**: [ ] Knowledge base is completely codified and loadable.

### Phase 6: Bayesian RCA Engine
- **Goal**: Calculate posterior probabilities of hypotheses using `pgmpy`.
- **Inputs**: FaultEpisode, retrieved evidence, fault trees.
- **Outputs**: Ranked list of HypothesisEvaluation.
- **Dependencies**: Phase 4, Phase 5.
- **Files**: `elevate/rca/bayesian.py`.
- **Interfaces**: `diagnose(episode, knowledge) -> List[HypothesisEvaluation]`.
- **Algorithms**: VariableElimination inference on Bayesian Networks.
- **Tasks**: Build BN dynamically from fault tree, inject evidence states, run inference.
- **Tests**: Given hardcoded evidence, verify exact expected probabilities.
- **Acceptance Criteria**: Ranks the true root cause in Top-1 or Top-3 for the 5 scenarios.
- **Risks**: Inference performance on large networks (mitigated by sub-system bounding).
- **Safety**: Does not make control decisions.
- **Security**: N/A
- **Demo Value**: The core diagnostic intelligence logic.
- **Definition of Done**: [ ] `pgmpy` calculates correct posteriors for all scenarios.

### Phase 7: Confidence & Abstention Logic
- **Goal**: Calibrate trust in the RCA output and abstain when uncertain.
- **Inputs**: List of HypothesisEvaluation.
- **Outputs**: ConfidenceDecision (HIGH/MEDIUM/LOW or ABSTAIN).
- **Dependencies**: Phase 6.
- **Files**: `elevate/rca/confidence.py`.
- **Interfaces**: `evaluate_confidence(evaluations) -> ConfidenceDecision`.
- **Algorithms**: Threshold logic, probability margin analysis, conflict detection.
- **Tasks**: Implement decision boundaries (e.g., top > 0.75 and margin > 0.20 for HIGH).
- **Tests**: Test explicit abstention on conflicted evidence.
- **Acceptance Criteria**: Abstains correctly on Demo Scenario 5 (Conflicting Evidence).
- **Risks**: Tuned too strictly (always abstains) or loosely.
- **Safety**: Abstention ensures safety by deferring to humans.
- **Security**: N/A
- **Demo Value**: Highlights the "principled abstention" differentiator.
- **Definition of Done**: [ ] Confidence logic successfully handles all edge cases.

### Phase 8: RAG Integration
- **Goal**: Retrieve relevant troubleshooting text to support the hypothesis.
- **Inputs**: InvestigationFrame keywords.
- **Outputs**: EvidenceBundle containing relevant text snippets.
- **Dependencies**: Phase 5.
- **Files**: `elevate/rag/chroma_client.py`, `elevate/rag/ingest.py`.
- **Interfaces**: `retrieve(query) -> List[Document]`.
- **Algorithms**: Dense vector search via ChromaDB, BM25 fallback (optional).
- **Tasks**: Set up ChromaDB, embed synthetic manuals, build retrieval query.
- **Tests**: Validate relevance of retrieved chunks for "Brake dragging".
- **Acceptance Criteria**: Retrieves correct paragraph in top 3 results.
- **Risks**: Poor embedding quality.
- **Safety**: Retrieved text is advisory only.
- **Security**: N/A
- **Demo Value**: Grounds the final explanation in "real" manuals.
- **Definition of Done**: [ ] RAG pipeline successfully returns context.

### Phase 9: LLM Integration (3 Touchpoints)
- **Goal**: Integrate Anthropic Claude for extraction, arbitration, and synthesis.
- **Inputs**: Context data at 3 points in pipeline.
- **Outputs**: Structured Pydantic outputs from LLM.
- **Dependencies**: Phase 4, Phase 6, Phase 8.
- **Files**: `elevate/llm/client.py`, `elevate/llm/prompts.py`.
- **Interfaces**: `call_llm(prompt, schema) -> BaseModel`.
- **Algorithms**: Structured output parsing, chain-of-thought prompting.
- **Tasks**: Write 3 specific prompts, wire up Anthropic client, parse JSON responses.
- **Tests**: Mock LLM responses to ensure pipeline robustness.
- **Acceptance Criteria**: LLM consistently returns schema-valid data.
- **Risks**: Hallucinations or malformed JSON (mitigated by strict schema).
- **Safety**: LLM explicitly instructed not to invent steps or command actions.
- **Security**: API key management.
- **Demo Value**: Makes the output human-readable and contextual.
- **Definition of Done**: [ ] All 3 touchpoints work with real Anthropic calls.

### Phase 10: ExplainabilityTrace Assembly
- **Goal**: Package all intermediate states into the final audit artifact.
- **Inputs**: Outputs from Phases 4, 6, 7, 8, 9.
- **Outputs**: Complete ExplainabilityTrace object.
- **Dependencies**: Phase 9.
- **Files**: `elevate/pipeline/trace.py`.
- **Interfaces**: `assemble_trace(...) -> ExplainabilityTrace`.
- **Algorithms**: Object composition.
- **Tasks**: Map all components to the 9-dimension schema.
- **Tests**: Schema validation of the final trace object.
- **Acceptance Criteria**: Produces a valid, complete ExplainabilityTrace.
- **Risks**: Missing data from earlier pipeline steps.
- **Safety**: Provides full transparency of the reasoning process.
- **Security**: Trace should not include raw API keys or PII.
- **Demo Value**: The primary output payload shown to the user.
- **Definition of Done**: [ ] Trace assembles cleanly for all 5 scenarios.

### Phase 11: API Layer
- **Goal**: Expose the pipeline via REST API.
- **Inputs**: The assembled core pipeline.
- **Outputs**: FastAPI application.
- **Dependencies**: Phase 1, Phase 10.
- **Files**: `elevate/api/main.py`, `elevate/api/routers/`.
- **Interfaces**: HTTP GET/POST endpoints matching Section 20.
- **Algorithms**: HTTP routing, serialization.
- **Tasks**: Implement all defined endpoints, add Swagger docs, handle errors.
- **Tests**: API integration tests using TestClient.
- **Acceptance Criteria**: Can run a full scenario end-to-end via POST/GET requests.
- **Risks**: Asynchronous state management.
- **Safety**: N/A
- **Security**: CORS, basic input validation.
- **Demo Value**: Connects the backend intelligence to the frontend UI.
- **Definition of Done**: [ ] FastAPI runs and passes all endpoint tests.

### Phase 12: Dashboard/UI
- **Goal**: Build the user interface for the technician and manager views.
- **Inputs**: ExplainabilityTrace JSON from API.
- **Outputs**: Streamlit or React frontend application.
- **Dependencies**: Phase 11.
- **Files**: `frontend/app.py` (if Streamlit).
- **Interfaces**: REST client to FastAPI.
- **Algorithms**: UI rendering, state management.
- **Tasks**: Build trace view, confidence gauge, evidence list, review buttons.
- **Tests**: Manual UI testing.
- **Acceptance Criteria**: Cleanly displays all 9 dimensions of the trace.
- **Risks**: Cluttered UI hiding critical information.
- **Safety**: Highlights confidence levels prominently to avoid automation bias.
- **Security**: N/A
- **Demo Value**: The visual wow-factor of the hackathon.
- **Definition of Done**: [ ] Dashboard displays the 5 demo scenarios perfectly.

### Phase 13: Demo Scenario Execution
- **Goal**: Pre-configure and script the 5 demo scenarios.
- **Inputs**: Simulator, API, UI.
- **Outputs**: Demo scripts/buttons to trigger each scenario instantly.
- **Dependencies**: Phase 11.
- **Files**: `scripts/run_demo.py`, configuration YAMLs.
- **Interfaces**: N/A
- **Algorithms**: N/A
- **Tasks**: Write scripts to inject faults, await processing, and open UI to results.
- **Tests**: Run each script start to finish.
- **Acceptance Criteria**: 1-click execution for each of the 5 scenarios.
- **Risks**: Timing issues between simulator generation and API processing.
- **Safety**: N/A
- **Security**: N/A
- **Demo Value**: Ensures flawless live demonstration.
- **Definition of Done**: [ ] All 5 scenarios work reliably with 1 click.

### Phase 14: Testing & Validation
- **Goal**: Ensure robustness across the 9-layer validation hierarchy.
- **Inputs**: Entire codebase.
- **Outputs**: Test reports and coverage metrics.
- **Dependencies**: Phase 13.
- **Files**: `tests/` directory.
- **Interfaces**: pytest.
- **Algorithms**: N/A
- **Tasks**: Write unit tests for core math, API tests, LLM mock tests.
- **Tests**: Full test suite run.
- **Acceptance Criteria**: >80% coverage on core logic (`elevate/rca`, `elevate/correlation`).
- **Risks**: Flaky tests due to timing or probabilistic LLM responses.
- **Safety**: Validates the deterministic boundaries.
- **Security**: N/A
- **Demo Value**: Proves the system works outside the "happy path".
- **Definition of Done**: [ ] `pytest` passes with required coverage.

### Phase 15: Demo Preparation
- **Goal**: Rehearse and freeze the codebase.
- **Inputs**: Completed application.
- **Outputs**: Demo script, finalized dataset, frozen repo.
- **Dependencies**: Phase 14.
- **Files**: `DEMO_SCRIPT.md`.
- **Interfaces**: N/A
- **Algorithms**: N/A
- **Tasks**: Dry-run demo timing, write talking points, freeze code changes.
- **Tests**: Timed runthroughs.
- **Acceptance Criteria**: Demo can be delivered smoothly in under 10 minutes.
- **Risks**: Live bugs (mitigation: code freeze).
- **Safety**: N/A
- **Security**: N/A
- **Demo Value**: Maximum impact delivery.
- **Definition of Done**: [ ] 3 flawless rehearsals completed.

### Phase 16: Documentation & Handoff
- **Goal**: Finalize all markdown documentation for the judges/evaluators.
- **Inputs**: Project context.
- **Outputs**: Final README and companion docs.
- **Dependencies**: Phase 15.
- **Files**: `README.md`, `docs/`.
- **Interfaces**: N/A
- **Algorithms**: N/A
- **Tasks**: Update instructions, verify architecture diagrams, clean up repo.
- **Tests**: N/A
- **Acceptance Criteria**: An external engineer can run the system using only the README.
- **Risks**: Outdated instructions.
- **Safety**: Clear disclaimers about non-production status.
- **Security**: No secrets committed to the repo.
- **Demo Value**: Leaves a lasting, professional artifact.
- **Definition of Done**: [ ] Repo is clean, documented, and ready for submission.

---

## 13. Critical Path
Phase 0 → Phase 3 → Phase 4 → Phase 6 → Phase 9 → Phase 10 → Phase 11 → Phase 12 → Phase 15 → Phase 16
Estimated: ~25 hours on the critical path

See PHASE_DEPENDENCY_MAP.md for full dependency graph.

---

## 14. Parallel Development Tracks
- **Track A (Core Pipeline)**: Phase 0 → 3 → 4 → 6 → 7 → 10
- **Track B (Simulator)**: Phase 0 → 2 → 13
- **Track C (Data Layer)**: Phase 0 → 1 → 11
- **Track D (Knowledge)**: Phase 0 → 5 → feeds 6
- **Track E (RAG/LLM)**: Phase 0 → 8 → 9 → feeds 10
- **Track F (Frontend)**: Phase 11 → 12

---

## 15. 30-Hour Build Plan
See companion document: 30_HOUR_HACKATHON_PLAN.md

Summary:
- Block 1 (0-6h): Foundation — scaffold, DB, simulator, first faults
- Block 2 (6-12h): Core Engine — triage, correlation, knowledge base
- Block 3 (12-18h): Reasoning — Bayesian RCA, confidence, abstention
- Block 4 (18-22h): Intelligence — RAG, LLM integration, ExplainabilityTrace
- Block 5 (22-26h): Interface — API, dashboard
- Block 6 (26-28h): Validation — all scenarios, tests
- Block 7 (28-30h): Demo prep — rehearsal, freeze

---

## 16. Full Prototype Roadmap
See PHASE_DEPENDENCY_MAP.md for milestones M0-M13.

---

## 17. File-Level Architecture
See companion document: FILE_LEVEL_IMPLEMENTATION_MAP.md

Total estimated files: ~55-60 files across simulator, pipeline, knowledge, rag_corpus, api, db, dashboard, tests, scenarios, and config.

---

## 18. Data Contracts
See companion document: DATA_CONTRACTS.md

Key contracts: TelemetrySample, AlarmEvent, SignalBaseline, AnomalyScore, FaultEpisode, InvestigationFrame, EvidenceBundle, HypothesisEvaluation, ArbitrationResult, ConfidenceDecision, ExplainabilityTrace, TechnicianView, ManagerView, TechnicianFeedback, ValidatedOutcome, FaultGroundTruth.

---

## 19. Database Model
PostgreSQL with SQLAlchemy ORM. Key tables:
- elevator, telemetry, alarm_event, fault_episode, episode_alarm_link
- fault_hypothesis, evidence, diagnosis
- knowledge_document, maintenance_record
- technician_feedback, validated_outcome
- model_version, knowledge_version, drift_event, calibration_report, evaluation_run

Full schema in DATA_CONTRACTS.md and Guidebook §AI.

---

## 20. API Contract
FastAPI endpoints:
- POST /telemetry — ingest readings
- POST /events — ingest alarms
- POST /fault-injection — demo fault trigger
- GET /fault-episodes — list episodes
- GET /fault-episodes/{id} — episode detail
- GET /diagnosis/{id} — diagnosis result
- GET /explainability/{id} — full trace
- POST /diagnosis/{id}/review — human review
- POST /feedback — technician feedback
- POST /validated-outcome — store ground truth

---

## 21. AI / RAG / RCA Contract

### LLM Role Boundaries
The LLM MAY: synthesize explanations, interpret documentation, formulate investigation plans, generate hypotheses from predefined domain space, evaluate evidence, generate structured output.

The LLM MUST NEVER: compute signal processing, calculate Bayesian probabilities, make safety decisions, invent missing evidence, generate novel repair steps, issue elevator commands.

### 3 LLM Touchpoints
1. Orchestrator extraction (FaultEpisode → InvestigationFrame)
2. RCA arbitration (BN posterior + evidence → ArbitrationResult)
3. Synthesis rendering (hypotheses + evidence → TechnicianView + ManagerView)

### RAG Architecture
Ingestion → Section-based chunking → Dual index (dense embeddings + BM25) → Hybrid retrieval with metadata filtering → Cross-encoder reranking → Context assembly.
Vector store: ChromaDB (in-process).
Corpus: Synthetic troubleshooting documents in rag_corpus/.

### Hallucination Containment (8 Layers)
1. Tool-grounded telemetry access
2. RAG document grounding
3. Structured output contracts (Pydantic)
4. Deterministic math offloading
5. Mandatory source provenance
6. Active contradiction checking
7. Principled abstention
8. Human physical verification

---

## 22. Explainability Model
ExplainabilityTrace: 9-dimension audit artifact
1. Observation
2. Evidence (validated sensor features)
3. Hypothesis (specific failure mode)
4. Supporting Evidence (with citations)
5. Contradicting Evidence (with citations)
6. Alternative Hypotheses (eliminated with reasoning)
7. Confidence (calibrated posterior)
8. Verification Requirements (physical inspections)
9. Source Lineage (sensor IDs, timestamps, manual revisions)

Full schema in DATA_CONTRACTS.md.

---

## 23. Human-in-the-Loop Workflow
Workflow: OBSERVE → DIAGNOSE → EXPLAIN → RECOMMEND → HUMAN CONFIRMS
- Human review is PERMANENT, not transitional
- Review actions: accept, accept-with-edit, reject-with-reason, flag-evidence-wrong, flag-correlation-wrong
- API: POST /diagnosis/{episode_id}/review
- Enforces episode.state == UNDER_REVIEW (409 otherwise)
- Sole write path to validated_outcome table

---

## 24. Safety Boundary
- System classified as NON-SAFETY-CRITICAL Diagnostic-Support
- Zero physical actuation path (tool does not exist in schema)
- One-way read-only telemetry observation
- IEC 62443 zone separation: Safety Zone (SL3) → Edge Gateway (DMZ) → Diagnostic Cloud (SL1)
- Standards: EN 81-20/50, ASME A17.1, IEC 61508 (project claims NO SIL rating)
- Worst-case failure: delayed/inaccurate diagnosis (never physical hazard)
- Complete AI failure has ZERO effect on elevator operation

---

## 25. Security Boundary
- Least-privilege agent tool scoping (read-only query tools only)
- controller_actuation tool: BLOCKED (interface does not exist)
- Prompt injection defense: untrusted-data delimiters, structured output enforcement
- Retrieval poisoning defense: source vetting, chunk hashing
- Secrets: .env file, never hardcoded
- API: Pydantic validation, rate limiting
- No inbound connections from cloud to elevator controller

---

## 26. Failure and Degraded-Mode Strategy
- **LLM unavailable**: Fall back to deterministic BN + rule-based synthesis
- **RAG unavailable**: Fall back to fault-tree-only diagnosis
- **Database unavailable**: Use in-memory episode state
- **Telemetry corruption**: Explicit quality flag, confidence penalty
- **Missing data**: Never assume normal; flag as missing with zero diagnostic value
- **KnowledgeGapError**: Convert to abstention trace
- **Conflicting evidence**: Abstain with explicit conflict description

---

## 27. Testing Strategy
See companion document: TESTING_AND_VALIDATION_PLAN.md
9-layer validation hierarchy. 5 demo scenarios as test cases. Error taxonomy E1-E14. Acceptance gates 1-10.

---

## 28. Evaluation Metrics
See TESTING_AND_VALIDATION_PLAN.md for full definitions.
Key metrics: Detection (P/R/F1), Fault Isolation (Top-1/Top-3), RCA (Top-k cause accuracy), Retrieval (P@k, MRR), Explanation (citation correctness, hallucination rate), Confidence (ECE, Brier), Abstention (coverage, selective accuracy).

---

## 29. Demonstration Scenarios
See companion document: DEMO_EXECUTION_PLAN.md
5 scenarios: (1) Motor Overcurrent / Brake Drag, (2) Door Degradation / Photo-Eye, (3) Encoder / Position Anomaly, (4) Alarm Cascade / IGBT, (5) Abstention / Conflicting Evidence.

---

## 30. Dataset Usage
See companion document: DATASET_USAGE_MATRIX.md

---

## 31. Known Risks
| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| LLM API outage during demo | Medium | High | Deterministic fallback path |
| Bayesian prior miscalibration | High | Medium | Priors labeled illustrative; manual tuning |
| LLM hallucination | Medium | High | 8-layer containment; structured output |
| Synthetic data unrealism | Medium | Medium | Physics-grounded scenarios; honest labeling |
| RAG retrieval irrelevance | Medium | Medium | Curated small corpus; manual review |
| Fault tree incompleteness | Medium | Low | Start with 6 well-documented trees |
| Time overrun | High | High | MUST/SHOULD/CUT-FIRST priorities per block |
| Human overtrust | Medium | Medium | UI friction requiring verification checkoffs |

---

## 32. Technical Debt and Prototype Simplifications
- First-order physics in simulator (not multibody)
- In-process ChromaDB (not production vector DB)
- Single PostgreSQL (not TimescaleDB)
- No Kafka event streaming
- No Neo4j knowledge graph
- Synchronous pipeline (not fully async)
- No LSTM/deep learning anomaly detection
- No conformal prediction calibration wrapper
- No CPT recalibration from feedback loop
- No mlflow model registry

---

## 33. Deferred Features
- Multi-agent architecture (requires ablation evidence)
- Knowledge graph (Neo4j)
- Closed-loop self-correction with CPT recalibration
- Fleet-wide analytics
- Edge deployment with quantized models
- Digital twin integration
- Kafka event streaming
- TimescaleDB extension
- Model versioning and shadow deployment
- Drift detection

---

## 34. Features That Must Never Be Built in the Prototype
- Autonomous elevator control or safety override
- Generic chatbot / open-ended conversational AI
- Predictive maintenance / RUL estimation
- Digital twin / PINN / GNN
- Fleet management dashboards
- Mobile app
- Multi-agent framework (LangGraph, AutoGen, CrewAI)
- Any write path from AI to elevator controller

---

## 35. Technical Decision Log
See companion document: ARCHITECTURE_DECISION_LOG.md
16 decisions (ADR-001 through ADR-016) covering language, API, database, simulator, RCA engine, LLM, RAG, anomaly detection, knowledge model, UI, deployment, testing, data contracts, and structured output.

---

## 36. Open Questions and Unknowns
See companion document: OPEN_QUESTIONS_AND_UNKNOWNS.md
16 unknowns (U-001 through U-016) covering proprietary KONE data, telemetry schemas, fault codes, failure rates, CMMS platform, sensor sampling rates, and safety certification.

---

## 37. Requirements Traceability
See companion document: REQUIREMENTS_TRACEABILITY_MATRIX.md
29 functional requirements (FR-001 through FR-029) and 10 non-functional requirements (NFR-001 through NFR-010), each traced to source documents and implementation phases.

---

## 38. Final Definition of Done

The prototype is DONE when:
- [ ] All 5 demo scenarios pass end-to-end
- [ ] ExplainabilityTrace generated for each scenario
- [ ] Alarm cascade correctly identifies primary vs consequential
- [ ] Bayesian RCA ranks correct root cause in top-1 or top-3
- [ ] Abstention triggers correctly on conflicting evidence
- [ ] Confidence tiers (HIGH/MEDIUM/LOW) behave correctly at boundaries
- [ ] Human review workflow (accept/edit/reject) functional
- [ ] No control path from AI to elevator exists
- [ ] All LLM claims have source citations
- [ ] Dashboard displays investigation trace
- [ ] Demo rehearsal completed within 10 minutes
- [ ] README with setup instructions exists
- [ ] Docker Compose starts cleanly
- [ ] pytest suite passes

---

## Companion Documents
This plan is supported by 11 companion documents under docs/implementation/:
1. ARCHITECTURE_DECISION_LOG.md
2. PHASE_DEPENDENCY_MAP.md
3. FILE_LEVEL_IMPLEMENTATION_MAP.md
4. DATA_CONTRACTS.md
5. TESTING_AND_VALIDATION_PLAN.md
6. 30_HOUR_HACKATHON_PLAN.md
7. DEMO_EXECUTION_PLAN.md
8. RESOLVED_DESIGN_CONFLICTS.md
9. REQUIREMENTS_TRACEABILITY_MATRIX.md
10. OPEN_QUESTIONS_AND_UNKNOWNS.md
11. DATASET_USAGE_MATRIX.md
