# ElevateRCA — Current Architecture (As Inspected)

> **Inspection Date:** 2026-09-28
> **Inspector:** Antigravity Automated Architecture Audit
> **Repository:** `d:\HACKATHONS\KONE Elevate\prototype\ElevateRCA`
> **Commit:** `5205099` — `feat: initial commit with ElevateRCA architecture, documentation, and README`
> **Branch:** `main`

---

## 1. Critical Finding: Documentation-Only Repository

> [!CAUTION]
> **The repository contains ZERO application source code.**
>
> The README describes a full architecture with `api/`, `pipeline/`, `simulator/`, `knowledge/`, `tests/`, `dashboard/`, `db/` directories — but **none of these directories or source files exist**. The commit history contains only documentation and the GUIDE knowledge base.

### What Actually Exists (46 files, ~21 MB)

| Category | Count | Description |
|---|---|---|
| **GUIDE/ PDFs** | 13 | Real OEM/safety/maintenance documentation (PDFs) |
| **GUIDE/ datasets** | 2 | Troubleshooting CSV + JSON (15 records each) |
| **docs/ planning** | 16 | Phase 1-12 research documents + guidebook + reports |
| **docs/implementation/** | 12 | Planning artifacts (from prior session) |
| **Root files** | 3 | README.md, .gitignore, master prompt |
| **Application code** | **0** | No `.py`, `.yaml`, `.toml`, `.tsx`, `.js`, `.sql`, `Dockerfile`, `docker-compose.yml` |

### What the README Claims Exists (But Does NOT)

```
CLAIMED                          STATUS
─────────────────────────────────────────────
api/main.py                      ❌ DOES NOT EXIST
api/deps.py                      ❌ DOES NOT EXIST
api/schemas.py                   ❌ DOES NOT EXIST
api/routes/telemetry.py          ❌ DOES NOT EXIST
api/routes/episodes.py           ❌ DOES NOT EXIST
api/routes/diagnosis.py          ❌ DOES NOT EXIST
api/routes/explainability.py     ❌ DOES NOT EXIST
api/routes/demo.py               ❌ DOES NOT EXIST
pipeline/pipeline.py             ❌ DOES NOT EXIST
pipeline/triage.py               ❌ DOES NOT EXIST
pipeline/correlation.py          ❌ DOES NOT EXIST
pipeline/orchestrator.py         ❌ DOES NOT EXIST
pipeline/retrieval.py            ❌ DOES NOT EXIST
pipeline/rca.py                  ❌ DOES NOT EXIST
pipeline/synthesis.py            ❌ DOES NOT EXIST
pipeline/explainability.py       ❌ DOES NOT EXIST
simulator/base.py                ❌ DOES NOT EXIST
simulator/elevator.py            ❌ DOES NOT EXIST
simulator/drive_motor.py         ❌ DOES NOT EXIST
simulator/door.py                ❌ DOES NOT EXIST
simulator/brake_traction.py      ❌ DOES NOT EXIST
simulator/controller_safety.py   ❌ DOES NOT EXIST
simulator/sensor_env.py          ❌ DOES NOT EXIST
simulator/alarm_generator.py     ❌ DOES NOT EXIST
simulator/faults.py              ❌ DOES NOT EXIST
simulator/scenario.py            ❌ DOES NOT EXIST
knowledge/failure_modes.yaml     ❌ DOES NOT EXIST
knowledge/causal_links.yaml      ❌ DOES NOT EXIST
knowledge/corrective_actions.yaml ❌ DOES NOT EXIST
rag_corpus/*.md                  ❌ DOES NOT EXIST
db/models.py                     ❌ DOES NOT EXIST
db/session.py                    ❌ DOES NOT EXIST
db/crud.py                       ❌ DOES NOT EXIST
dashboard/src/App.tsx             ❌ DOES NOT EXIST
dashboard/streamlit_app.py       ❌ DOES NOT EXIST
tests/*.py                       ❌ DOES NOT EXIST
docker-compose.yml               ❌ DOES NOT EXIST
Dockerfile                       ❌ DOES NOT EXIST
pyproject.toml                   ❌ DOES NOT EXIST
requirements.txt                 ❌ DOES NOT EXIST
```

---

## 2. Existing Agents

**None.** No agent code exists. No LangChain, LangGraph, CrewAI, or custom agent implementations are present.

---

## 3. Data Flow

**No data flow exists** because no application code exists. The README describes:

```
Simulator → Ingestion → Triage (EWMA/CUSUM) → Alarm Correlation
→ Orchestrator (LLM #1) → Retrieval (SQL + RAG) → Bayesian RCA
→ LLM Arbitration (#2) → Confidence/Abstention → Synthesis (LLM #3)
→ ExplainabilityTrace → API → UI → Human Review
```

This is aspirational architecture, not implemented.

---

## 4. RAG Pipeline

**No RAG pipeline exists.**

- No ChromaDB integration code
- No embedding generation code
- No document chunking or ingestion code
- No vector index
- No retrieval functions
- The `rag_corpus/` directory described in the README does not exist

The GUIDE folder contains 13 PDFs + 2 structured datasets that should form the RAG knowledge base, but no ingestion pipeline processes them.

---

## 5. RCA Pipeline

**No RCA pipeline exists.**

- No pgmpy Bayesian network code
- No hypothesis generation or elimination code
- No evidence evaluation code
- No confidence scoring
- No abstention logic

---

## 6. UI / Dashboard

**No UI exists.**

- No React/Streamlit/HTML frontend code
- No dashboard components

---

## 7. API

**No API exists.**

- No FastAPI application
- No route handlers
- No Pydantic schemas

---

## 8. Persistence / Database

**No database exists.**

- No SQLAlchemy models
- No SQLite/PostgreSQL database
- No Alembic migrations
- No CRUD operations

---

## 9. Tests

**No tests exist.**

- No pytest files
- No test fixtures
- No conftest.py

---

## 10. GUIDE Folder — The Project's Only Technical Asset

The GUIDE folder is the **only substantive technical content** beyond documentation:

### 10.1 PDF Documents (13 files, ~17.6 MB)

| # | Filename | Size | Type | Subsystem | Configuration |
|---|----------|------|------|-----------|---------------|
| 1 | `brake_of_geared_traction_machine.pdf` | 3.8 MB | BRAKE_SYSTEM_GUIDE | Brake/Traction | Geared machines |
| 2 | `brake_of_gearless_traction_machine.pdf` | 2.4 MB | BRAKE_SYSTEM_GUIDE | Brake/Traction | Gearless machines |
| 3 | `elevator_brake_pad.pdf` | 898 KB | COMPONENT_GUIDE | Brake Pad | General |
| 4 | `elevator_door_operations.pdf` | 1.7 MB | DOOR_SYSTEM_GUIDE | Door | General |
| 5 | `elevator_hoisting_rope.pdf` | 285 KB | HOISTING_SYSTEM_GUIDE | Hoisting/Traction | General |
| 6 | `sets_egov_8_9.pdf` | 796 KB | SAFETY_SYSTEM_MANUAL | SETS-01 | EGOV = 8 or 9 |
| 7 | `sets_egov_a.pdf` | 685 KB | SAFETY_SYSTEM_MANUAL | SETS-01 | EGOV = A |
| 8 | `sets_egov_b.pdf` | 620 KB | SAFETY_SYSTEM_MANUAL | SETS-01 | EGOV = B |
| 9 | `sets_egov_d_e.pdf` | 634 KB | SAFETY_SYSTEM_MANUAL | SETS-01 | EGOV = D or E |
| 10 | `sets_egov_f.pdf` | 574 KB | SAFETY_SYSTEM_MANUAL | SETS-01 | EGOV = F |
| 11 | `sets-11.pdf` | 710 KB | SAFETY_SYSTEM_MANUAL | SETS-11 | SETS-11 |
| 12 | `kone guide maintainance procdure.pdf` | 2.9 MB | MAINTENANCE_MANUAL | General | KONE OEM |
| 13 | `OEM 1.pdf` | 1.5 MB | OEM_REFERENCE | General | OEM |

### 10.2 Structured Datasets (2 files, ~15 KB)

| Filename | Format | Records | Schema Fields |
|----------|--------|---------|---------------|
| `elevator_troubleshooting_dataset.csv` | CSV | 15 | id, component, symptom, alarm, evidence, possible_causes, maintenance_check, recommended_action, priority, root_cause_category |
| `elevator_troubleshooting_dataset.json` | JSON | 15 | Same 10 fields as CSV |

Both files contain the same 15 troubleshooting records (ELV-001 through ELV-015) covering: Traction Machine, Brake, Door System, Door Interlock, Leveling System, Controller/Drive, Motor/Drive, Encoder/Feedback, Governor/Safety, Machine Room, Hoist Ropes, Emergency Communication.

---

## 11. Known Limitations

1. **No executable code** — the entire project is documentation and planning
2. **README describes non-existent architecture** — significant credibility risk if inspected
3. **GUIDE PDFs are not ingested** — the primary technical knowledge base is idle
4. **No RAG pipeline** — the claimed ChromaDB/BM25 hybrid retrieval doesn't exist
5. **No diagnostic case management** — no iterative RCA loop
6. **No technician interaction** — no feedback ingestion or evidence update mechanism
7. **No safety constraint enforcement** — no code-level safety boundary
8. **Planning artifacts reference non-existent code** — `docs/implementation/` documents describe files that don't exist

---

## 12. What Must Be Built From Scratch

Everything. The entire application must be implemented:

1. Python project structure + dependencies
2. GUIDE document ingestion pipeline (PDF parsing + CSV/JSON parsing)
3. RAG vector store (ChromaDB with metadata-aware retrieval)
4. Diagnostic case state management (persistent, iterative)
5. Technician feedback agent (NL → structured evidence)
6. RCA reasoning engine (hypothesis generation, evidence evaluation, elimination)
7. Contradiction detection
8. Confidence/abstention logic
9. Report generation
10. FastAPI backend
11. Streamlit or React frontend
12. Tests
13. End-to-end demo scenario
