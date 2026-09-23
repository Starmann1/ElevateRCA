# KONE Elevate — 30-Hour Hackathon Build Plan

> **Classification:** [PROJECT PROPOSAL]
> **State:** [TARGET STATE] (Defines the plan to build the prototype)

## Philosophy
- Every hour block has MUST / SHOULD / OPTIONAL / CUT-FIRST items
- MUST items are non-negotiable for a demonstrable system
- CUT-FIRST items are the first to go under time pressure
- Freeze points prevent destabilizing changes near demo time

## Team Assumptions
- Assume a small team (1-3 developers) working intensively [SYNTHETIC/ILLUSTRATIVE]
- All members have Python proficiency [DOCUMENTED FACT]
- LLM API key pre-provisioned [PROJECT PROPOSAL]
- Development environment pre-configured [PROJECT PROPOSAL]

## Block 1: Foundation (Hours 0-6)

### MUST HAVE (Hours 0-4)
- [ ] Git repository initialized with .gitignore (Python, .env)
- [ ] Python 3.12 virtual environment created
- [ ] pyproject.toml / requirements.txt with: fastapi, uvicorn, pydantic, sqlalchemy, alembic, pgmpy, numpy, pandas, anthropic, chromadb, pytest
- [ ] Docker Compose: FastAPI + PostgreSQL containers
- [ ] .env.example with ANTHROPIC_API_KEY, DATABASE_URL, LOG_LEVEL
- [ ] PostgreSQL schema: ALL tables from Guidebook §AI migrated via Alembic [PROTOTYPE SIMPLIFICATION]
- [ ] Repository directory structure created:
  ```
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
  └── docs/
  ```
- [ ] SubsystemSimulator protocol defined
- [ ] DriveMotorSim and DoorSim implemented with step() and inject_fault() [PROTOTYPE SIMPLIFICATION]
- [ ] ElevatorSimulator compositor ticking subsystems
- [ ] AlarmGenerator with threshold-based alarm triggers
- [ ] 3 fault types working: igbt_overcurrent, mechanical_jam, door_photoeye_drift [PROTOTYPE SIMPLIFICATION]

### SHOULD HAVE (Hours 4-6)
- [ ] BrakeTractionSim, ControllerSafetySim, SensorEnvSim subsystem simulators
- [ ] Remaining fault types: door_roller_wear, encoder_drift, brake_timing_violation, safety_chain_trip
- [ ] FaultGroundTruth tracking on injection
- [ ] Scenario runner class
- [ ] SignalBaseline dataclass and update_and_score() function
- [ ] Operating-state-aware baselines

### OPTIONAL
- [ ] intermittent_fault, sensor_noise_burst, simultaneous_cascade fault types
- [ ] Comprehensive unit tests for simulator

### CUT-FIRST
- [ ] Advanced physics models (multi-body dynamics)
- [ ] High-fidelity noise models

---

## Block 2: Core Engine (Hours 6-12)

### MUST HAVE (Hours 6-10)
- [ ] EWMA/CUSUM triage pipeline producing anomaly scores [PROJECT PROPOSAL]
- [ ] Alarm correlation engine: cluster_alarms() with CAUSAL_LINKS
- [ ] FaultEpisode creation with primary/consequential classification
- [ ] FaultEpisode state machine (OPEN → TRIAGED → ... → CLOSED)
- [ ] knowledge/failure_modes.yaml for drive_motor and door subsystems [SYNTHETIC/ILLUSTRATIVE]
- [ ] knowledge/causal_links.yaml defining cascade relationships [SYNTHETIC/ILLUSTRATIVE]
- [ ] knowledge/corrective_actions.yaml with action definitions [SYNTHETIC/ILLUSTRATIVE]

### SHOULD HAVE (Hours 10-12)
- [ ] failure_modes.yaml expanded: brake_traction, encoder, safety_chain subsystems
- [ ] FMEA scoring (Severity × Occurrence × Detectability = RPN) in knowledge base
- [ ] Basic unit tests for triage and correlation
- [ ] Integration test: simulator → triage → correlation → episode

### OPTIONAL
- [ ] Operating-state transition detection from telemetry
- [ ] Cross-correlation lag analysis

### CUT-FIRST
- [ ] FFT/spectral analysis
- [ ] Envelope analysis
- [ ] Advanced statistical features beyond EWMA/CUSUM

---

## Block 3: Reasoning Engine (Hours 12-18)

### MUST HAVE (Hours 12-16)
- [ ] pgmpy DiscreteBayesianNetwork for drive_motor subsystem [PROTOTYPE SIMPLIFICATION]
- [ ] pgmpy network for door subsystem [PROTOTYPE SIMPLIFICATION]
- [ ] VariableElimination inference computing posteriors
- [ ] Evidence evaluation: supporting + contradicting evidence for each hypothesis
- [ ] decide() function: HIGH (≥ 0.75) / MEDIUM (≥ 0.45) / LOW (< 0.45) tiers [ENGINEERING INFERENCE]
- [ ] Abstention logic: LOW confidence returns explicit abstention reason
- [ ] Dual confidence: root_cause_confidence + action_confidence

### SHOULD HAVE (Hours 16-18)
- [ ] pgmpy networks for brake, encoder, safety_chain subsystems
- [ ] Pipeline.run(episode) → ExplainabilityTrace integration
- [ ] Scenario 1 (Motor Overcurrent) passing end-to-end
- [ ] Scenario 5 (Abstention) passing end-to-end

### OPTIONAL
- [ ] LLM arbitration layer (arXiv:2510.03815 pattern) [PUBLIC RESEARCH FACT]
- [ ] Dynamic Bayesian Network for temporal evidence [FUTURE CAPABILITY]

### CUT-FIRST
- [ ] CPT recalibration from feedback
- [ ] Conformal prediction wrapper

---

## Block 4: Intelligence Layer (Hours 18-22)

### MUST HAVE (Hours 18-20)
- [ ] RAG corpus: synthetic troubleshooting manual chunks in rag_corpus/ [SYNTHETIC/ILLUSTRATIVE]
- [ ] Chroma PersistentClient with sentence embeddings
- [ ] retrieve_evidence(hypothesis, subsystem) function
- [ ] LLM Call #1: Orchestrator extraction (FaultEpisode → InvestigationFrame)
- [ ] LLM Call #2: RCA Arbitration (BN posterior + evidence → ArbitrationResult)
- [ ] LLM Call #3: Synthesis rendering (dual TechnicianView + ManagerView)
- [ ] Structured tool_choice/JSON output enforcement

### SHOULD HAVE (Hours 20-22)
- [ ] Full ExplainabilityTrace assembly function
- [ ] Demo-safe fallback: deterministic-only path when LLM unavailable [PROJECT PROPOSAL]
- [ ] Complete pipeline integration test: simulator → full trace
- [ ] Scenarios 2, 3, 4 passing end-to-end

### OPTIONAL
- [ ] Prompt injection defense (untrusted data delimiters)
- [ ] LLM response caching for repeated scenarios

### CUT-FIRST
- [ ] Cross-encoder reranking
- [ ] Hybrid BM25+vector search (use vector-only if time-constrained) [PROTOTYPE SIMPLIFICATION]

---

## Block 5: Interface Layer (Hours 22-26)

### MUST HAVE (Hours 22-24)
- [ ] FastAPI app with core endpoints:
  - POST /telemetry
  - POST /events
  - POST /fault-injection (demo)
  - GET /fault-episodes
  - GET /diagnosis/{episode_id}
  - GET /explainability/{episode_id}
  - POST /diagnosis/{episode_id}/review
- [ ] Pydantic v2 request/response models
- [ ] Database CRUD operations via SQLAlchemy

### SHOULD HAVE (Hours 24-26)
- [ ] Dashboard (React + Tailwind OR Streamlit fallback) [OPEN DECISION]:
  - Fleet status grid
  - Live telemetry chart with EWMA threshold lines
  - ExplainabilityTrace visualization
  - Review action bar (accept/edit/reject)
- [ ] Dashboard connected to API via fetch/axios
- [ ] POST /feedback endpoint

### OPTIONAL
- [ ] Real-time WebSocket telemetry updates
- [ ] Model health panel (mocked) [SYNTHETIC/ILLUSTRATIVE]

### CUT-FIRST
- [ ] Advanced CSS/animations
- [ ] Multiple elevator fleet views

---

## Block 6: Validation & Polish (Hours 26-28)

### MUST HAVE (Hours 26-27)
- [ ] All 5 demo scenarios passing end-to-end
- [ ] Automated test suite: `pytest tests/ -v`
- [ ] Key metrics computed on scenario runs:
  - Top-1 root cause accuracy
  - Alarm correlation accuracy
  - Abstention correctness
- [ ] Bug fixes for any failing scenarios

### SHOULD HAVE (Hours 27-28)
- [ ] Edge case tests (noise burst, out-of-range values)
- [ ] ExplainabilityTrace completeness assertions
- [ ] API error handling (graceful 4xx/5xx responses)
- [ ] README.md with setup and run instructions

### OPTIONAL
- [ ] Self-correction demonstration walkthrough
- [ ] Calibration report generation

### CUT-FIRST
- [ ] Performance benchmarks
- [ ] Load testing

---

## Block 7: Demo Prep (Hours 28-30)

### MUST HAVE (Hours 28-29)
- [ ] Demo script finalized and printed
- [ ] Full rehearsal run of 8-10 minute demo
- [ ] Fallback data pre-generated for offline demo [SYNTHETIC/ILLUSTRATIVE]
- [ ] Docker Compose clean restart verified
- [ ] All API keys verified working

### SHOULD HAVE (Hours 29-30)
- [ ] Judge Q&A defense preparation
- [ ] Architecture diagram for slides
- [ ] Claim-by-claim evidence verification

### OPTIONAL
- [ ] Backup laptop configured
- [ ] Screen recording of successful demo run

### CUT-FIRST
- [ ] Nothing — this block is sacred

---

## Freeze Points
| Freeze | Hour | Rule |
|---|---|---|
| **Knowledge Freeze** | Hour 20 | No changes to YAML files |
| **API Contract Freeze** | Hour 25 | No endpoint changes |
| **Code Freeze** | Hour 28 | Bug fixes only |
| **Demo Freeze** | Hour 29 | Rehearsed and locked |

## Time-Pressure Scenario Reductions
| Available Time | Scenarios | Subsystems | LLM Calls | UI |
|---|---|---|---|---|
| 30 hours (full) | 5 scenarios | 5 subsystems | 3 calls | React dashboard |
| 2 weeks | 5 scenarios | 5 subsystems | 3 calls | React dashboard |
| 1 week | 3 scenarios (1, 4, 5) | 3 subsystems | 2 calls | Streamlit |
| 3 days | 2 scenarios (1, 5) | 2 subsystems | 1 call | API-only demo |
| 1 day | 1 scenario (1) + 1 abstention | 1 subsystem | 0 calls (BN only) | curl/Postman |

## Risk Mitigation
| Risk | Probability | Impact | Mitigation |
|---|---|---|---|
| LLM API outage | Medium [PROVENANCE: ENGINEERING INFERENCE] | High | Demo-safe deterministic fallback |
| Bayesian prior miscalibration | High [PROVENANCE: ENGINEERING INFERENCE] | Medium | Priors labeled illustrative; manual tuning |
| LLM hallucination | Medium [PROVENANCE: PUBLIC RESEARCH FACT] | High | Structured output enforcement; citation requirement |
| Database corruption | Low [PROVENANCE: ENGINEERING INFERENCE] | High | Docker volume reset; Alembic re-migration |
| RAG retrieval irrelevance | Medium [PROVENANCE: ENGINEERING INFERENCE] | Medium | Curated small corpus; manual chunk review |
| Time overrun | High [PROVENANCE: ENGINEERING INFERENCE] | High | Cut-first items defined per block |
