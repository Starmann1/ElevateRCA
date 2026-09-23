# KONE Elevate — Requirements Traceability Matrix

## Purpose
This matrix maps every functional and non-functional requirement to its source document (backward traceability) and to the implementation phase/module that will satisfy it (forward traceability).

## Format
| Req ID | Requirement Description | Source Document(s) | Source Section | Source Tier | MoSCoW Priority | Implementation Phase | Implementation Module | Verification Method |

## Functional Requirements

### Core Pipeline Requirements
- FR-001: Ingest timestamped telemetry with schema validation | Phase 12, Guidebook §AI | Tier 1/2 | MUST | Phase 1, Phase 11 | pipeline/ingestion, api/ | Unit test + Integration test
- FR-002: Normalize timestamps to UTC | Phase 6 | Tier 4 | MUST | Phase 3 | pipeline/triage.py | Unit test
- FR-003: Validate physical range constraints on sensor values | Phase 6, Phase 9 | Tier 4 | MUST | Phase 3 | pipeline/triage.py | Unit test (Gate 1)
- FR-004: Detect anomalies using EWMA/CUSUM per signal per unit | Phase 6, Guidebook §M | Tier 2/4 | MUST | Phase 3 | pipeline/triage.py | Unit test
- FR-005: Condition anomaly baselines on operating state | Phase 6 | Tier 4 | MUST | Phase 3 | pipeline/triage.py | Unit test
- FR-006: Correlate temporally related alarms into fault episodes | Phase 2, Guidebook §N | Tier 2/4 | MUST | Phase 4 | pipeline/correlation.py | Integration test
- FR-007: Classify alarms as primary or consequential | Phase 2, Guidebook §N | Tier 2/4 | MUST | Phase 4 | pipeline/correlation.py | Scenario test (Scenario 4)
- FR-008: Generate candidate hypotheses from fault trees | Phase 5, Guidebook §P | Tier 2/4 | MUST | Phase 6 | pipeline/rca.py | Unit test
- FR-009: Compute Bayesian posterior probabilities using pgmpy | Phase 5, Guidebook §Q | Tier 1/2 | MUST | Phase 6 | pipeline/rca.py | Unit test
- FR-010: Evaluate supporting AND contradicting evidence for each hypothesis | Phase 5, Phase 12 | Tier 1 | MUST | Phase 6 | pipeline/rca.py | Scenario test
- FR-011: Provide dual confidence scoring (diagnostic + action) | Phase 12, Guidebook §U | Tier 1/2 | MUST | Phase 7 | pipeline/rca.py | Unit test
- FR-012: Abstain when evidence insufficient (confidence < 0.45) | Phase 12, Guidebook §U | Tier 1/2 | MUST | Phase 7 | Scenario test (Scenario 5)
- FR-013: Retrieve relevant troubleshooting documents via RAG | Phase 7, Guidebook §R | Tier 2/4 | SHOULD | Phase 8 | pipeline/retrieval.py | Unit test
- FR-014: LLM extraction of structured investigation frame | Guidebook §T | Tier 2 | SHOULD | Phase 9 | pipeline/orchestrator.py | Integration test
- FR-015: LLM arbitration between BN posterior and evidence | Guidebook §AN | Tier 2 | SHOULD | Phase 9 | pipeline/rca.py | Integration test
- FR-016: LLM synthesis of dual-audience reports | Guidebook §AO | Tier 2 | SHOULD | Phase 9 | pipeline/synthesis.py | Integration test
- FR-017: Generate complete ExplainabilityTrace | Phase 12, Guidebook §V | Tier 1/2 | MUST | Phase 10 | pipeline/explainability.py | Integration test
- FR-018: Support human review (accept/edit/reject) via API | Guidebook §W, §AJ | Tier 2 | MUST | Phase 11 | api/ | Integration test
- FR-019: Record technician feedback and validated outcomes | Guidebook §Y | Tier 2 | SHOULD | Phase 11 | api/, db/ | Integration test

### Simulator Requirements
- FR-020: Simulate 5 subsystems with first-order physics | Guidebook §K | Tier 2 | MUST | Phase 2 | simulator/ | Unit test
- FR-021: Support 10 fault injection types | Guidebook §L | Tier 2 | MUST | Phase 2 | simulator/ | Unit test
- FR-022: Track fault ground truth for evaluation | Guidebook §L | Tier 2 | MUST | Phase 2 | simulator/ | Unit test

### Knowledge Requirements
- FR-023: Define 6 subsystem fault trees with failure modes | Phase 5, Guidebook §P | Tier 2/4 | MUST | Phase 5 | knowledge/ | Schema validation
- FR-024: Define FMEA with severity/occurrence/detectability scoring | Phase 5 | Tier 4 | MUST | Phase 5 | knowledge/ | Schema validation
- FR-025: Define pre-approved corrective actions lookup | Guidebook §AO | Tier 2 | MUST | Phase 5 | knowledge/ | Schema validation

### UI/Dashboard Requirements
- FR-026: Display fleet status grid | Guidebook §AK | Tier 2 | SHOULD | Phase 12 | dashboard/ | Manual verification
- FR-027: Display live telemetry chart with anomaly thresholds | Guidebook §AK | Tier 2 | SHOULD | Phase 12 | dashboard/ | Manual verification
- FR-028: Display ExplainabilityTrace investigation panel | Guidebook §AK | Tier 2 | SHOULD | Phase 12 | dashboard/ | Manual verification
- FR-029: Provide review action bar (accept/edit/reject) | Guidebook §AK | Tier 2 | SHOULD | Phase 12 | dashboard/ | Manual verification

## Non-Functional Requirements

### Safety Requirements
- NFR-001: ZERO control path from AI to elevator hardware | Phase 8, Phase 12 | Tier 1/4 | MUST | All phases | Architecture | Gate 9
- NFR-002: Read-only telemetry access only | Phase 8 | Tier 4 | MUST | Phase 11 | api/ | Security review
- NFR-003: Human review required before any action | Phase 12, Phase 8 | Tier 1/4 | MUST | Phase 11 | api/ | Integration test

### Quality Requirements
- NFR-004: All LLM claims must have source citations | Phase 7, Phase 12 | Tier 1/4 | MUST | Phase 9, 10 | pipeline/ | Gate 6
- NFR-005: No invented corrective actions | Guidebook §AO | Tier 2 | MUST | Phase 9 | pipeline/synthesis.py | Integration test
- NFR-006: Structured JSON output from LLM (no free-form) | Phase 7, Guidebook §AN | Tier 2/4 | MUST | Phase 9 | pipeline/ | Integration test

### Performance Requirements (Prototype)
- NFR-007: End-to-end diagnosis within 30 seconds | Guidebook §T | Tier 2 | SHOULD | All phases | pipeline/ | Performance test
- NFR-008: API response within 5 seconds for read endpoints | Engineering inference | N/A | SHOULD | Phase 11 | api/ | Performance test

### Data Integrity
- NFR-009: Synthetic data clearly labeled as synthetic | Phase 12 | Tier 1 | MUST | Phase 2, 8 | simulator/, rag_corpus/ | Code review
- NFR-010: Bayesian priors documented as illustrative | Phase 12 | Tier 1 | MUST | Phase 5 | knowledge/ | Documentation review

## Do-Not-Build Requirements
From Phase 10 and Phase 12:
- DNB-001: Autonomous elevator control | NEVER
- DNB-002: Generic chatbot | NEVER
- DNB-003: Predictive maintenance/RUL | NEVER (input from upstream only)
- DNB-004: Digital twin | NEVER (MVP)
- DNB-005: Graph Neural Networks | NEVER (MVP)
- DNB-006: Physics-Informed Neural Networks | NEVER (MVP)
- DNB-007: Fleet dashboard analytics | NEVER (MVP)
- DNB-008: Mobile app | NEVER (MVP)
- DNB-009: Multi-agent framework (LangGraph/AutoGen/CrewAI) | NEVER (MVP)
- DNB-010: Kafka/event streaming | NEVER (MVP)
