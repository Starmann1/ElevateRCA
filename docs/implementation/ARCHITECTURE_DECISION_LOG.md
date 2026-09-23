# KONE Elevate — Architecture Decision Log

## Format
For each decision:
- **ADR-NNN**: Decision title
- **Decision**: What was decided
- **Alternatives Considered**: What else was evaluated
- **Why Chosen**: Rationale
- **Trade-Off**: What is sacrificed
- **Evidence from Project Documents**: Source citations
- **When to Revisit**: Under what conditions this should be reconsidered
- **Classification**: ARCHITECTURE DECISION / IMPLEMENTATION ASSUMPTION / PROTOTYPE SIMPLIFICATION

## Decisions:

### ADR-001: Python 3.12 as Primary Language
- **Decision**: Python 3.12 for all backend code
- **Alternatives Considered**: Rust, Go, Java
- **Why Chosen**: Fastest prototyping, richest ML/data ecosystem, pgmpy/numpy/pandas availability, team expertise
- **Trade-Off**: Performance (acceptable for prototype), type safety (mitigated by Pydantic)
- **Evidence from Project Documents**: Guidebook §G
- **When to Revisit**: Production scale requiring <10ms latency
- **Classification**: ARCHITECTURE DECISION

### ADR-002: FastAPI + Uvicorn for API
- **Decision**: FastAPI with Pydantic v2
- **Alternatives Considered**: Flask, Django, gRPC
- **Why Chosen**: Async-capable, automatic OpenAPI docs, native Pydantic integration, fast prototyping
- **Trade-Off**: Less mature than Django for admin interfaces
- **Evidence from Project Documents**: Guidebook §G, §AJ
- **Classification**: ARCHITECTURE DECISION

### ADR-003: PostgreSQL for Persistence
- **Decision**: PostgreSQL as the single relational database
- **Alternatives Considered**: SQLite, MongoDB, TimescaleDB, InfluxDB
- **Why Chosen**: ACID compliance, JSON support (JSONB), mature ecosystem, sufficient for MVP telemetry volume
- **Trade-Off**: Not optimized for time-series (acceptable at prototype scale)
- **Evidence from Project Documents**: Guidebook §AI
- **When to Revisit**: Production scale requiring high-frequency time-series ingestion → add TimescaleDB extension
- **Classification**: IMPLEMENTATION ASSUMPTION (Exact proprietary KONE schema unavailable; prototype defines synthetic schema)

### ADR-004: SQLAlchemy + Alembic for ORM and Migrations
- **Decision**: SQLAlchemy ORM with Alembic migrations
- **Alternatives Considered**: Raw SQL, Tortoise ORM, Prisma
- **Why Chosen**: Industry standard, schema versioning, migration rollback
- **Evidence from Project Documents**: Guidebook §AI
- **Classification**: ARCHITECTURE DECISION

### ADR-005: Synthetic Elevator Simulator over Digital Twin
- **Decision**: Lightweight Python-based synthetic simulator with first-order physics models
- **Alternatives Considered**: Full digital twin, multibody simulation, physics-informed neural network (PINN)
- **Why Chosen**: Full digital twin/PINN requires effort incompatible with 30-hour hackathon; fault trees provide equivalent domain structure without training overhead; synthetic scenario generation is validated by academic precedent (MDPI Sensors 2025)
- **Trade-Off**: Cannot model complex multi-physics interactions; synthetic data must be honestly labeled
- **Evidence from Project Documents**: Phase 12 §14.24, Phase 10 §12.17, Research Library
- **When to Revisit**: Post-pilot if physics fidelity gap identified
- **Classification**: PROTOTYPE SIMPLIFICATION

### ADR-006: Bayesian Network (pgmpy) for RCA Engine
- **Decision**: Discrete Bayesian Network using pgmpy with VariableElimination inference
- **Alternatives Considered**: Rule-based scoring, neural network classifier, LLM-based reasoning, fuzzy logic
- **Why Chosen**: Provides mathematically rigorous uncertainty quantification; handles sparse data with illustrative priors; produces calibratable posteriors; correlated evidence can be modeled in graph structure; established methodology (arXiv:2510.03815)
- **Trade-Off**: Priors are illustrative, not validated against real fleet statistics
- **Evidence from Project Documents**: Phase 5 §7.25, Guidebook §Q, Phase 12 §14.5
- **When to Revisit**: When real fleet failure statistics become available for prior calibration
- **Classification**: ARCHITECTURE DECISION / SYNTHETIC/ILLUSTRATIVE (priors)

### ADR-007: Single Orchestrator over Multi-Agent Swarm
- **Decision**: Single-pipeline orchestrator with tool-calling, not a multi-agent swarm
- **Alternatives Considered**: Multi-agent framework (LangGraph, AutoGen, CrewAI), specialized agent swarm
- **Why Chosen**: Lower complexity, deterministic execution, easier debugging, lower latency, no coordination overhead, no agent disagreement failure modes; multi-agent requires ablation evidence to justify
- **Trade-Off**: Less modular, harder to extend to specialized roles later
- **Evidence from Project Documents**: Phase 12 §14.8, Phase 10 §12.16 ("complexity must earn its cost")
- **When to Revisit**: V1 if ablation testing shows 2-agent split (Evidence + Reasoning) outperforms single pipeline
- **Classification**: ARCHITECTURE DECISION

### ADR-008: Anthropic Claude via API for LLM
- **Decision**: Anthropic Claude (Sonnet for arbitration/synthesis, Haiku for extraction) via API
- **Alternatives Considered**: OpenAI GPT, Google Gemini, local open-weight models
- **Why Chosen**: KONE's existing AWS Bedrock stack uses Anthropic Claude; excellent structured output support; provider-agnostic interface design
- **Trade-Off**: External API dependency (mitigated by demo-safe fallback)
- **Evidence from Project Documents**: Phase 3 (KONE Technician Assistant uses Bedrock/Claude), Guidebook §S
- **When to Revisit**: When provider-specific features or cost become critical
- **Classification**: ARCHITECTURE DECISION

### ADR-009: Chroma (In-Process) for Vector Store
- **Decision**: ChromaDB with PersistentClient for RAG vector storage
- **Alternatives Considered**: Qdrant, Milvus, pgvector, FAISS, Pinecone
- **Why Chosen**: Zero infrastructure overhead, embeds in Python process, sufficient for small curated corpus (3-5 documents)
- **Trade-Off**: Not production-scale; no distributed search
- **Evidence from Project Documents**: Guidebook §R
- **When to Revisit**: V1 when corpus grows beyond 100 documents
- **Classification**: PROTOTYPE SIMPLIFICATION

### ADR-010: EWMA + CUSUM for Anomaly Detection
- **Decision**: Exponentially Weighted Moving Average with CUSUM changepoint detection
- **Alternatives Considered**: LSTM autoencoder, Isolation Forest, Transformer, VAE
- **Why Chosen**: Deterministic, explainable, no training data required, works with per-unit rolling baselines, sensitive to sustained shifts (not just point anomalies)
- **Trade-Off**: Cannot detect complex multivariate patterns; limited to statistical deviations
- **Evidence from Project Documents**: Phase 6, Guidebook §M
- **When to Revisit**: When sufficient labeled normal data is available for ML-based detection
- **Classification**: ARCHITECTURE DECISION

### ADR-011: YAML-Based Knowledge Model over Graph Database
- **Decision**: Version-controlled YAML files for failure modes, causal links, corrective actions
- **Alternatives Considered**: Neo4j knowledge graph, PostgreSQL JSON, in-memory graph
- **Why Chosen**: Human-readable, version-controlled, zero infrastructure, sufficient for 6 fault trees and MVP FMEA; graph DB justified only if relationship complexity outgrows trees
- **Trade-Off**: Cannot perform arbitrary graph traversal queries
- **Evidence from Project Documents**: Phase 10 §12.18, Phase 12 §14.5
- **When to Revisit**: V2 when causal relationship complexity exceeds tree structures
- **Classification**: PROTOTYPE SIMPLIFICATION

### ADR-012: React + Tailwind CSS for Dashboard (Streamlit Fallback)
- **Decision**: React with Tailwind CSS and Recharts for dashboard; Streamlit + Plotly as fallback
- **Alternatives Considered**: Vue.js, Angular, pure HTML/JS
- **Why Chosen**: Component reusability, rich charting, responsive design
- **Trade-Off**: Heavier setup than Streamlit; justified only if time permits
- **Evidence from Project Documents**: Guidebook §AK
- **Classification**: ARCHITECTURE DECISION

### ADR-013: Docker Compose for Deployment
- **Decision**: Docker Compose with FastAPI + PostgreSQL containers
- **Alternatives Considered**: Kubernetes, bare metal, serverless
- **Why Chosen**: Simplest reproducible deployment; one `docker-compose up` command; sufficient for prototype
- **Trade-Off**: Not production-scale orchestration
- **Evidence from Project Documents**: Guidebook, Phase 10 §12.43
- **When to Revisit**: Production deployment planning
- **Classification**: PROTOTYPE SIMPLIFICATION

### ADR-014: pytest for Testing
- **Decision**: pytest as the testing framework
- **Alternatives Considered**: unittest, nose, hypothesis
- **Why Chosen**: Industry standard, fixtures, parameterization, rich assertion output
- **Evidence from Project Documents**: Guidebook §AP
- **Classification**: ARCHITECTURE DECISION

### ADR-015: Typed Pydantic Models for Data Contracts
- **Decision**: Pydantic v2 models for all cross-module data contracts
- **Alternatives Considered**: Dataclasses, TypedDict, untyped dictionaries
- **Why Chosen**: Runtime validation, serialization, JSON schema generation, FastAPI integration
- **Trade-Off**: Slight overhead vs plain dataclasses
- **Evidence from Project Documents**: Guidebook §T, Phase 12
- **Classification**: ARCHITECTURE DECISION

### ADR-016: Structured JSON Output from LLM (Tool-Calling)
- **Decision**: Force LLM outputs through tool_choice/structured schemas, not free-form text
- **Alternatives Considered**: Free-form text parsing, regex extraction
- **Why Chosen**: Eliminates parse failures, guarantees schema compliance, prevents hallucinated prose
- **Evidence from Project Documents**: Guidebook §AN, Phase 7 §9.13
- **Classification**: ARCHITECTURE DECISION
