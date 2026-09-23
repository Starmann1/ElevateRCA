# KONE Elevate — File-Level Implementation Map

## Purpose
This document maps every file that must be created during implementation to its phase, module, purpose, key contents, dependencies, and estimated effort.

## Classification
- **CURRENT STATE**: File exists now (noting there are ZERO application files currently)
- **TARGET STATE**: File to be created during implementation

## Repository Structure

```
kone-elevate-rca/
├── README.md                          [Phase 16]
├── pyproject.toml                     [Phase 0]
├── requirements.txt                   [Phase 0]
├── docker-compose.yml                 [Phase 0]
├── Dockerfile                         [Phase 0]
├── .env.example                       [Phase 0]
├── .gitignore                         [Phase 0]
├── alembic.ini                        [Phase 1]
├── alembic/
│   ├── env.py                         [Phase 1]
│   └── versions/
│       └── 001_initial_schema.py      [Phase 1]
├── simulator/
│   ├── __init__.py                    [Phase 2]
│   ├── base.py                        [Phase 2] SubsystemSimulator Protocol
│   ├── drive_motor.py                 [Phase 2] DriveMotorSim
│   ├── door.py                        [Phase 2] DoorSim
│   ├── brake_traction.py              [Phase 2] BrakeTractionSim
│   ├── controller_safety.py           [Phase 2] ControllerSafetySim
│   ├── sensor_env.py                  [Phase 2] SensorEnvSim
│   ├── elevator.py                    [Phase 2] ElevatorSimulator compositor
│   ├── alarm_generator.py             [Phase 2] Threshold-based alarm generation
│   ├── faults.py                      [Phase 2] 10 fault injection functions
│   └── scenario.py                    [Phase 2] Scenario runner
├── pipeline/
│   ├── __init__.py                    [Phase 3]
│   ├── triage.py                      [Phase 3] EWMA/CUSUM anomaly detection
│   ├── correlation.py                 [Phase 4] ISA-18.2 alarm clustering
│   ├── orchestrator.py                [Phase 9] LLM call #1: structured extraction
│   ├── retrieval.py                   [Phase 8] Deterministic DB + RAG vector search
│   ├── rca.py                         [Phase 6] pgmpy Bayesian network + LLM arbitration
│   ├── synthesis.py                   [Phase 9] Lookup + LLM dual rendering
│   ├── explainability.py              [Phase 10] ExplainabilityTrace assembler
│   └── pipeline.py                    [Phase 10] Pipeline.run() orchestration
├── knowledge/
│   ├── failure_modes.yaml             [Phase 5] 6 subsystem fault trees + priors
│   ├── causal_links.yaml              [Phase 5] Alarm cascade graph
│   └── corrective_actions.yaml        [Phase 5] Approved action lookup
├── rag_corpus/
│   ├── fault_code_glossary.md         [Phase 8] Synthetic fault code reference
│   ├── drive_motor_troubleshooting.md [Phase 8] Synthetic troubleshooting guide
│   ├── door_troubleshooting.md        [Phase 8] Synthetic troubleshooting guide
│   ├── brake_troubleshooting.md       [Phase 8] Synthetic troubleshooting guide
│   └── encoder_troubleshooting.md     [Phase 8] Synthetic troubleshooting guide
├── api/
│   ├── __init__.py                    [Phase 11]
│   ├── main.py                        [Phase 11] FastAPI app, CORS, lifespan
│   ├── routes/
│   │   ├── telemetry.py               [Phase 11] POST /telemetry, POST /events
│   │   ├── episodes.py                [Phase 11] GET /fault-episodes, GET /fault-episodes/{id}
│   │   ├── diagnosis.py               [Phase 11] GET /diagnosis/{id}, POST /diagnosis/{id}/review
│   │   ├── explainability.py          [Phase 11] GET /explainability/{id}
│   │   ├── feedback.py                [Phase 11] POST /feedback, POST /validated-outcome
│   │   └── demo.py                    [Phase 11] POST /fault-injection (demo only)
│   ├── schemas.py                     [Phase 11] Pydantic request/response models
│   └── deps.py                        [Phase 11] Dependency injection (DB session, etc.)
├── db/
│   ├── __init__.py                    [Phase 1]
│   ├── models.py                      [Phase 1] SQLAlchemy ORM models
│   ├── session.py                     [Phase 1] Database session management
│   └── crud.py                        [Phase 11] CRUD operations
├── dashboard/
│   ├── package.json                   [Phase 12] React project config
│   ├── src/
│   │   ├── App.tsx                    [Phase 12] Main app component
│   │   ├── components/
│   │   │   ├── FleetView.tsx          [Phase 12] Elevator status grid
│   │   │   ├── TelemetryChart.tsx     [Phase 12] Live time-series with EWMA lines
│   │   │   ├── InvestigationPanel.tsx [Phase 12] ExplainabilityTrace display
│   │   │   └── ReviewBar.tsx          [Phase 12] Accept/Edit/Reject actions
│   │   └── api/
│   │       └── client.ts              [Phase 12] API client
│   └── OR: streamlit_app.py           [Phase 12] Streamlit fallback
├── tests/
│   ├── conftest.py                    [Phase 14] pytest fixtures
│   ├── test_simulator.py              [Phase 14] Simulator unit tests
│   ├── test_triage.py                 [Phase 14] EWMA/CUSUM unit tests
│   ├── test_correlation.py            [Phase 14] Alarm clustering tests
│   ├── test_rca.py                    [Phase 14] Bayesian network tests
│   ├── test_confidence.py             [Phase 14] Confidence/abstention tests
│   ├── test_pipeline.py               [Phase 14] End-to-end pipeline tests
│   ├── test_api.py                    [Phase 14] API endpoint tests
│   ├── test_scenarios.py              [Phase 14] 5 demo scenario tests
│   └── test_rag.py                    [Phase 14] RAG retrieval tests
├── scenarios/
│   ├── scenario_1_overcurrent.py      [Phase 13] Motor overcurrent scenario
│   ├── scenario_2_door_drift.py       [Phase 13] Door degradation scenario
│   ├── scenario_3_encoder.py          [Phase 13] Encoder anomaly scenario
│   ├── scenario_4_cascade.py          [Phase 13] Alarm cascade scenario
│   └── scenario_5_abstention.py       [Phase 13] Abstention scenario
└── docs/
    ├── [existing 16 source documents]
    └── implementation/
        └── [12 planning artifacts]
```

## Detailed File Implementations

### Root Project & Configuration (Phase 0)

| Path | Purpose | Key Contents | Dependencies | Estimated Lines | Priority |
|---|---|---|---|---|---|
| `pyproject.toml` | Python project metadata and dependencies | Poetry/PIP config, pytest config | None | 50 | MUST |
| `requirements.txt` | Alternative Python dependencies | pip install list | None | 20 | MUST |
| `docker-compose.yml` | Multi-container orchestration | App, DB (Postgres), Redis | None | 40 | MUST |
| `Dockerfile` | Image build instructions | Python 3.11 base, copy, run | None | 20 | MUST |
| `.env.example` | Template for environment variables | DB_URL, LLM_API_KEY, LOG_LEVEL | None | 15 | MUST |
| `.gitignore` | Ignore rules for git | `venv/`, `__pycache__/`, `.env` | None | 30 | MUST |

### Database & Models (Phase 1)

| Path | Purpose | Key Contents | Dependencies | Estimated Lines | Priority |
|---|---|---|---|---|---|
| `db/models.py` | SQLAlchemy ORM definitions | Elevator, Telemetry, FaultEpisode, Diagnosis, Feedback | None | 200 | MUST |
| `db/session.py` | Session lifecycle management | `engine`, `SessionLocal`, `get_db` | `sqlalchemy` | 30 | MUST |
| `alembic.ini` & `alembic/env.py` | Migration configuration | Alembic setup | `db/models.py` | 100 | MUST |
| `alembic/versions/001_initial_schema.py` | Initial table creation | `upgrade()`, `downgrade()` | None | 150 | MUST |

### Simulator (Phase 2)

| Path | Purpose | Key Contents | Dependencies | Estimated Lines | Priority |
|---|---|---|---|---|---|
| `simulator/base.py` | Shared interfaces | `SubsystemSimulator` Protocol, `SimState` dataclass | None | 50 | MUST |
| `simulator/drive_motor.py` | Drive subsystem simulation | `DriveMotorSim` | `simulator/base.py` | 100 | MUST |
| `simulator/door.py` | Door subsystem simulation | `DoorSim` | `simulator/base.py` | 100 | MUST |
| `simulator/brake_traction.py` | Brake/traction simulation | `BrakeTractionSim` | `simulator/base.py` | 80 | MUST |
| `simulator/controller_safety.py` | Controller simulation | `ControllerSafetySim` | `simulator/base.py` | 80 | MUST |
| `simulator/sensor_env.py` | Environmental variables | `SensorEnvSim` | `simulator/base.py` | 60 | MUST |
| `simulator/elevator.py` | Compositor mapping subsystems | `ElevatorSimulator`, `step()` loop | Subsystems | 150 | MUST |
| `simulator/alarm_generator.py` | Generate alarm events | Threshold checks on telemetry | None | 100 | MUST |
| `simulator/faults.py` | Specific fault injections | `inject_overcurrent()`, `inject_door_drift()` | Subsystems | 120 | MUST |
| `simulator/scenario.py` | Test scenario runner | `ScenarioRunner` | Simulator | 80 | MUST |

### Pipeline (Phases 3-10)

| Path | Purpose | Key Contents | Dependencies | Estimated Lines | Priority |
|---|---|---|---|---|---|
| `pipeline/triage.py` | Statistical anomaly detection | `EWMATracker`, `CUSUMDetector` | `numpy`, `pandas` | 150 | MUST |
| `pipeline/correlation.py` | ISA-18.2 alarm clustering | `AlarmClusterer`, temporal grouping | None | 100 | MUST |
| `pipeline/rca.py` | Bayesian network reasoning | `BayesianRCA`, exact inference | `pgmpy` | 200 | MUST |
| `pipeline/retrieval.py` | RAG vector search | `KnowledgeRetriever`, FAISS index | `langchain` | 120 | MUST |
| `pipeline/orchestrator.py` | LLM context extraction | Structured prompts, context assembly | `langchain` | 150 | MUST |
| `pipeline/synthesis.py` | Dual rendering output | `DiagnosisSynthesizer`, standard lookups | None | 150 | MUST |
| `pipeline/explainability.py` | Trace assembler | `ExplainabilityTrace` formatter | Pipeline | 100 | MUST |
| `pipeline/pipeline.py` | Orchestrate components | `run_analysis()` end-to-end flow | All Pipeline | 150 | MUST |

### Knowledge & RAG Corpus (Phases 5, 8)

| Path | Purpose | Key Contents | Dependencies | Estimated Lines | Priority |
|---|---|---|---|---|---|
| `knowledge/failure_modes.yaml` | System logic and priors | YAML definitions | None | 200 | MUST |
| `knowledge/causal_links.yaml` | Topology/alarm rules | Alarm cascades | None | 100 | MUST |
| `knowledge/corrective_actions.yaml` | Standard Operating Procedures | Action lookup by code | None | 150 | MUST |
| `rag_corpus/*.md` | Mock documentation | Troubleshooting manuals for RAG | None | ~50/ea | MUST |

### API (Phase 11)

| Path | Purpose | Key Contents | Dependencies | Estimated Lines | Priority |
|---|---|---|---|---|---|
| `api/main.py` | FastAPI entrypoint | `FastAPI()`, CORS setup | `api/routes` | 80 | MUST |
| `api/schemas.py` | Validation models | Pydantic classes (TelemetryData, DiagnosisResponse) | None | 150 | MUST |
| `api/deps.py` | FastApi dependencies | `get_db()`, API keys | `db/session.py` | 40 | MUST |
| `api/routes/telemetry.py` | Data ingestion | `POST /telemetry`, `POST /events` | `db/crud.py` | 80 | MUST |
| `api/routes/episodes.py` | Fault list API | `GET /fault-episodes` | `db/crud.py` | 80 | MUST |
| `api/routes/diagnosis.py` | RCA outputs | `GET /diagnosis/{id}`, reviews | `pipeline.py` | 100 | MUST |
| `api/routes/demo.py` | Scenario triggers | `POST /fault-injection` | `simulator` | 60 | OPTIONAL |
| `db/crud.py` | DB query helpers | `create_telemetry()`, `get_episode()` | `db/models.py` | 200 | MUST |

### Dashboard (Phase 12)

| Path | Purpose | Key Contents | Dependencies | Estimated Lines | Priority |
|---|---|---|---|---|---|
| `dashboard/src/App.tsx` | Main web interface | Layout, state | React | 150 | MUST |
| `dashboard/src/components/FleetView.tsx` | Fleet grid | Elevator cards, status colors | React | 120 | MUST |
| `dashboard/src/components/TelemetryChart.tsx` | Telemetry plots | Recharts / Chart.js graphs | React | 150 | MUST |
| `dashboard/src/components/InvestigationPanel.tsx` | Explanations | Trace breakdown UI | React | 200 | MUST |
| `dashboard/src/components/ReviewBar.tsx` | Feedback loop | Accept/reject buttons | React | 80 | MUST |
| `dashboard/streamlit_app.py` | Fast prototype UI | Complete streamlit logic | `streamlit` | 300 | FALLBACK |

### Scenarios (Phase 13)

| Path | Purpose | Key Contents | Dependencies | Estimated Lines | Priority |
|---|---|---|---|---|---|
| `scenarios/scenario_1_overcurrent.py` | High current simulation | Runs simulator, checks outputs | Simulator | 60 | MUST |
| `scenarios/scenario_2_door_drift.py` | Mechanical drift simulation | Runs simulator, checks outputs | Simulator | 60 | MUST |
| `scenarios/scenario_3_encoder.py` | Component error simulation | Runs simulator, checks outputs | Simulator | 60 | MUST |
| `scenarios/scenario_4_cascade.py` | Multi-alarm event simulation | Runs simulator, checks outputs | Simulator | 60 | MUST |
| `scenarios/scenario_5_abstention.py` | Confidence threshold failure | Runs simulator, expects fallback | Simulator | 60 | MUST |

### Tests (Phase 14)

| Path | Purpose | Key Contents | Dependencies | Estimated Lines | Priority |
|---|---|---|---|---|---|
| `tests/conftest.py` | Pytest fixtures | DB, mock data, FastAPI client | None | 100 | MUST |
| `tests/test_simulator.py` | Validate simulator physics | Physics asserts, fault checks | Simulator | 150 | MUST |
| `tests/test_triage.py` | Math tests | EWMA checks | Pipeline | 100 | MUST |
| `tests/test_rca.py` | Bayesian logic tests | Posterior probabilities | Pipeline | 120 | MUST |
| `tests/test_api.py` | Endpoint checks | API client calls | API | 200 | MUST |
| `tests/test_pipeline.py` | Integration tests | Full end-to-end logic | All | 200 | MUST |
