# KONE Elevate — Resolved Design Conflicts

## Source Hierarchy Reference
- **TIER 1**: Phase 12 Final Synthesis (highest authority)
- **TIER 2**: Technical Architecture Guidebook (implementation baseline)
- **TIER 3**: Phase 10 Scope/Prioritization/MVP
- **TIER 4**: Phases 1-11 (domain context)
- **TIER 5**: Idea Proposal, Project Understanding Report
- **TIER 6**: Research Source Library

## Conflict Resolution Format
For each conflict:
1. **Conflict ID**: (C-001, C-002, etc.)
2. **Conflict Description**: What disagrees
3. **Source A Position**: (Document, section, statement)
4. **Source B Position**: (Document, section, statement)
5. **Final Position**: The resolved decision
6. **Reason**: Why this resolution
7. **Implementation Consequence**: What this means for the build
8. **Classification**: RESOLVED / OPEN DECISION REQUIRED

## Identified Conflicts:

### C-001: Pipeline Sequencing — Retrieval Before vs After RCA
- **Conflict Description**: Pipeline sequence logic conflict.
- **Source A Position**: Guidebook §C/§T: Pipeline sequence is Orchestrator → Retrieval → RCA (retrieval runs BEFORE RCA)
- **Source B Position**: Guidebook §R RAG: RAG query uses "RCA Agent's current leading hypothesis + subsystem" (implies retrieval runs AFTER/DURING RCA)
- **Final Position**: Two-pass retrieval. Initial broad retrieval by symptoms/alarms before RCA, then targeted retrieval by leading hypothesis after BN inference for enrichment.
- **Reason**: Balances early broad context with precise later enrichment based on findings.
- **Implementation Consequence**: Pipeline implementation will need a two-pass structure for retrieval.
- **Classification**: RESOLVED

### C-002: Multi-Agent vs Single Orchestrator Architecture
- **Conflict Description**: Number of agents in architecture.
- **Source A Position**: Phase 7 §9.20: Defines 8 specialized agent roles with multi-agent architecture
- **Source B Position**: Phase 12 §14.8, Phase 10 §12.16: Single orchestrator with tool-calling mandated for MVP
- **Final Position**: Single orchestrator for MVP per Phase 12 authority. Agent responsibilities become functions/modules invoked by single pipeline.
- **Reason**: Simplifies implementation for MVP per Phase 12 guidance.
- **Implementation Consequence**: Pipeline will be a monolithic orchestrator calling module functions rather than multiple communicative agents.
- **Classification**: RESOLVED

### C-003: LLM Model Selection Discrepancy
- **Conflict Description**: Model specification conflict.
- **Source A Position**: Guidebook §S: References speculative future models (Claude Sonnet 5, GPT-6 Astra)
- **Source B Position**: Guidebook §AN code: Uses `claude-sonnet-4-6`
- **Final Position**: Use configurable `ANTHROPIC_MODEL` environment variable. Default to currently available Claude model.
- **Reason**: Ensures prototype is runnable today while remaining flexible.
- **Implementation Consequence**: Configurable model strings needed rather than hardcoded futures.
- **Classification**: RESOLVED

### C-004: Subsystem Coverage in Build Schedule vs Demo Scenarios
- **Conflict Description**: Number of covered subsystems.
- **Source A Position**: Guidebook §AT: MUST-HAVE hours 0-18 covers only 2 subsystems (drive_motor, door)
- **Source B Position**: Guidebook §AR: All 5 demo scenarios require 4+ subsystems (drive_motor, door, brake, encoder, safety)
- **Final Position**: Knowledge YAML must include all 5 subsystems early (parallel to pipeline work). Demo scenarios 3-5 can use simpler pipeline implementations.
- **Reason**: Required to satisfy demo scenarios comprehensively.
- **Implementation Consequence**: Need to flesh out knowledge base earlier across more subsystems.
- **Classification**: RESOLVED

### C-005: Knowledge Graph / Neo4j vs Hierarchical Fault Trees
- **Conflict Description**: Knowledge store implementation strategy.
- **Source A Position**: Phase 7 §9.10: Describes knowledge graphs in Neo4j with directional relationships
- **Source B Position**: Phase 10 §12.18, Phase 12 §14.5: Hierarchical fault trees and YAML sufficient for MVP; Neo4j deferred to V2
- **Final Position**: YAML-based fault trees for MVP per Tier 1/3 authority. Knowledge graph deferred.
- **Reason**: YAML meets MVP requirements with vastly lower complexity.
- **Implementation Consequence**: Neo4j dropped; YAML schema adopted.
- **Classification**: RESOLVED

### C-006: Asynchronous vs Synchronous Pipeline Execution
- **Conflict Description**: Execution flow type.
- **Source A Position**: Guidebook §G/§AZ: Describes async ingestion queue (asyncio.Queue)
- **Source B Position**: Guidebook §T: Pipeline.run() is synchronous
- **Final Position**: Synchronous pipeline for MVP simplicity. Async ingestion can be a thin wrapper that queues episodes for synchronous processing.
- **Reason**: Simplifies pipeline control flow for MVP.
- **Implementation Consequence**: Pipeline logic stays synchronous, asynchronous parts handled externally or by a thin queue.
- **Classification**: RESOLVED

### C-007: KnowledgeGapError Handling
- **Conflict Description**: Error behavior when lacking knowledge mapping.
- **Source A Position**: Guidebook §AO: render() raises KnowledgeGapError if root cause unmapped
- **Source B Position**: Project requirements: System must gracefully degrade, never crash
- **Final Position**: Catch KnowledgeGapError, convert to abstention trace with reason "Knowledge gap: unmapped corrective action"
- **Reason**: Fulfills the 'never crash' requirement.
- **Implementation Consequence**: Error handler inside the RCA agent/pipeline that handles the exception appropriately.
- **Classification**: RESOLVED

### C-008: Event Streaming (Kafka) in MVP
- **Conflict Description**: Use of event bus.
- **Source A Position**: Phase 8 §10.17: Describes Kafka event bus architecture
- **Source B Position**: Phase 10 §12.28, Phase 12 §14.24: Unnecessary infrastructure deferred
- **Final Position**: No Kafka for MVP. Direct function calls. Kafka deferred to production.
- **Reason**: Removes overhead for MVP.
- **Implementation Consequence**: Synchronous logic and function calls used instead of message queueing.
- **Classification**: RESOLVED

### C-009: TimescaleDB vs Plain PostgreSQL
- **Conflict Description**: Database implementation.
- **Source A Position**: Phase 8 §10.17: Suggests TimescaleDB for time-series
- **Source B Position**: Guidebook §AI, Phase 10: PostgreSQL sufficient for MVP
- **Final Position**: Plain PostgreSQL for MVP. TimescaleDB extension can be added later without schema changes.
- **Reason**: Eliminates dependency complexity.
- **Implementation Consequence**: Postgres used for the backend schema.
- **Classification**: RESOLVED

### C-010: Confidence Calibration Claims
- **Conflict Description**: Validation of confidence intervals.
- **Source A Position**: Phase 12 §14.20: "Confidence engine is mathematically designed for calibration" — marked YELLOW
- **Source B Position**: Reality: No real-world maintenance outcomes to calibrate against
- **Final Position**: Confidence mechanism is implemented but explicitly documented as uncalibrated against real outcomes. Priors are illustrative.
- **Reason**: True calibration requires real world data feedback loops that aren't possible here.
- **Implementation Consequence**: Confidence is synthesized and documented as illustrative.
- **Classification**: RESOLVED

### C-011: KONE-TKE Acquisition Impact on Technology Stack
- **Conflict Description**: Implication of acquisition on tech choices.
- **Source A Position**: Phase 11 §13.4: KONE-TKE combination may merge AWS and Azure stacks
- **Source B Position**: MVP scope: Prototype is technology-agnostic
- **Final Position**: No impact on MVP. Note as strategic context only. Platform-agnostic design is a feature.
- **Reason**: Focus remains on the application prototype rather than infrastructure lock-in.
- **Implementation Consequence**: None.
- **Classification**: RESOLVED (no implementation impact)

## Open Decisions
None at this time.
