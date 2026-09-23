# KONE Elevate — Data Contracts

## Purpose
This document defines every typed data structure used across the ElevateRCA pipeline. These are planning-level specifications for the Pydantic models, database schemas, and inter-module contracts.

## Classification Legend
- **DOCUMENTED FACT**: Schema explicitly defined in source documents
- **ENGINEERING INFERENCE**: Schema derived from engineering requirements
- **PROTOTYPE SIMPLIFICATION**: Simplified version of a production requirement

---

## 1. Telemetry Contracts

### TelemetrySample
```python
class TelemetrySample(BaseModel):
    timestamp: datetime        # ISO 8601, UTC-normalized
    elevator_id: str           # Asset identifier
    signal_name: str           # e.g., 'motor_current_rms', 'door_cycle_time'
    value: float               # Numeric measurement
    unit: str                  # Physical unit (A, ms, °C, mm, etc.)
    quality: str               # 'good' | 'suspect' | 'bad' | 'missing'
    operating_state: str       # Current elevator state from state machine
```
Classification: DOCUMENTED FACT (Guidebook §AI, Phase 5 Project Understanding)

### AlarmEvent
```python
class AlarmEvent(BaseModel):
    timestamp: datetime
    elevator_id: str
    alarm_type: str            # e.g., 'motor_overcurrent', 'door_close_timeout'
    severity: str              # 'critical' | 'warning' | 'informational'
    subsystem: str             # 'drive_motor' | 'door' | 'brake' | 'encoder' | 'safety_chain'
    raw_payload: dict          # Original controller data
```
Classification: DOCUMENTED FACT (Guidebook §AI)

---

## 2. Signal Triage Contracts

### SignalBaseline
```python
@dataclass
class SignalBaseline:
    ewma: float
    ewma_var: float
    alpha: float = 0.05        # Smoothing factor
    cusum_pos: float = 0.0
    cusum_neg: float = 0.0
    k: float = 0.5             # CUSUM slack (std-devs)
    h: float = 5.0             # CUSUM alarm threshold (std-devs)
```
Classification: DOCUMENTED FACT (Guidebook §M, verbatim code)

### AnomalyScore
```python
class AnomalyScore(BaseModel):
    signal_name: str
    z_score: float
    sustained_deviation: bool
    anomaly_score: float       # Normalized [0, 1]
    operating_state: str
    timestamp: datetime
    elevator_id: str
```
Classification: ENGINEERING INFERENCE (derived from Guidebook §M update_and_score return)

---

## 3. Alarm Correlation Contracts

### FaultEpisode
```python
class FaultEpisode(BaseModel):
    episode_id: str
    elevator_id: str
    opened_at: datetime
    state: str                 # OPEN | TRIAGED | EVIDENCE_GATHERED | DIAGNOSED | SYNTHESIZED | UNDER_REVIEW | CLOSED
    primary_alarm: AlarmEvent
    consequential_alarms: list[AlarmEvent]
    anomaly_scores: list[AnomalyScore]  # Relevant signal anomalies
```
Classification: DOCUMENTED FACT (Guidebook §O, §AI, §N)

FaultEpisode State Machine:
```
OPEN → TRIAGED → EVIDENCE_GATHERED → DIAGNOSED → SYNTHESIZED → UNDER_REVIEW → CLOSED
```

---

## 4. Investigation Contracts

### InvestigationFrame
```python
class InvestigationFrame(BaseModel):
    episode_id: str
    elevator_id: str
    opened_at: datetime
    primary_alarm: AlarmEvent
    consequential_alarms: list[AlarmEvent]
    observations: list[str]    # Natural language observations
    telemetry_features: dict[str, float]  # Extracted features
    operating_state: str
    time_window: TimeWindow
```
Classification: DOCUMENTED FACT (Guidebook §T)

### TimeWindow
```python
class TimeWindow(BaseModel):
    start: datetime
    end: datetime
    trigger_timestamp: datetime
```

---

## 5. Evidence Contracts

### EvidenceBundle
```python
class EvidenceBundle(BaseModel):
    telemetry_evidence: list[TelemetryEvidence]
    alarm_evidence: list[AlarmEvidence]
    maintenance_evidence: list[MaintenanceEvidence]
    rag_sources: list[RAGSource]
```

### TelemetryEvidence
```python
class TelemetryEvidence(BaseModel):
    signal_name: str
    baseline_value: float
    observed_value: float
    deviation: float
    operating_state: str
    timestamp: datetime
    duration_ms: float
    quality: str
```

### RAGSource
```python
class RAGSource(BaseModel):
    text: str
    source: str               # Document identifier
    section: str              # Section/heading
    citation_type: str        # 'synthetic' | 'public-reference' | 'oem-manual'
    relevance_score: float
```

---

## 6. RCA Contracts

### HypothesisEvaluation
```python
class HypothesisEvaluation(BaseModel):
    hypothesis_id: str
    root_cause: str
    subsystem: str
    component: str
    failure_mode: str
    prior_probability: float
    posterior_probability: float
    evidence_for: list[str]
    evidence_against: list[str]
    rank: int
```
Classification: DOCUMENTED FACT (Guidebook §Q, Phase 7 §9.23)

### ArbitrationResult
```python
class ArbitrationResult(BaseModel):
    bn_top_hypothesis: str
    llm_agreed: bool
    override_reason: Optional[str]
```
Classification: DOCUMENTED FACT (Guidebook §AN)

---

## 7. Confidence & Abstention Contracts

### ConfidenceDecision
```python
class ConfidenceDecision(BaseModel):
    root_cause_confidence: float   # BN posterior for top hypothesis
    action_confidence: float       # HIGH only if RC confidence HIGH AND action lookup match
    confidence_tier: str           # 'HIGH' | 'MEDIUM' | 'LOW'
    abstention_reason: Optional[str]
```
Classification: DOCUMENTED FACT (Guidebook §U)
Decision thresholds:
- HIGH: root_cause_confidence >= 0.75 AND action_confidence >= 0.75
- MEDIUM: root_cause_confidence >= 0.45
- LOW: root_cause_confidence < 0.45 (ABSTAIN)

---

## 8. Output Contracts

### ExplainabilityTrace
Document the full ExplainabilityTrace JSON schema with all fields from Guidebook §V:
```json
{
  "episode_id": "string",
  "unit_id": "string",
  "opened_at": "ISO8601",
  "primary_alarm": "AlarmEvent",
  "consequential_alarms": "[AlarmEvent]",
  "observations": "[string]",
  "derived_features": "dict",
  "affected_subsystem": "string",
  "hypotheses": "[HypothesisEvaluation]",
  "arbitration": "ArbitrationResult",
  "retrieved_sources": "[RAGSource]",
  "root_cause": "string",
  "root_cause_confidence": "float",
  "recommended_action": "string",
  "action_confidence": "float",
  "confidence_tier": "string",
  "uncertainty_notes": "[string]",
  "abstention_reason": "string|null",
  "technician_render": "TechnicianView",
  "manager_render": "ManagerView",
  "technician_feedback": "null",
  "final_validated_outcome": "null",
  "schema_version": "1.1"
}
```

### TechnicianView
```python
class TechnicianView(BaseModel):
    root_cause: str
    confidence: float
    evidence_for: list[str]
    ruled_out: list[str]
    recommended_action: str
    parts: list[str]
    tools: list[str]
    verification_steps: list[str]
```

### ManagerView
```python
class ManagerView(BaseModel):
    status: str
    eta_minutes: Optional[int]
    escalation_needed: bool
    plain_language_summary: str
```

---

## 9. Human Review Contracts

### TechnicianFeedback
```python
class TechnicianFeedback(BaseModel):
    case_id: str
    predicted_root_cause: str
    actual_root_cause: str
    prediction_correct: bool
    predicted_subsystem: str
    actual_subsystem: str
    recommended_action: str
    action_accepted: bool
    technician_correction: Optional[str]
    evidence_missing: bool
    alarm_correlation_correct: bool
    confidence_appropriate: bool
    additional_notes: str
    timestamp: datetime
    technician_role: str
```
Classification: DOCUMENTED FACT (Guidebook §Y)

### ValidatedOutcome
```python
class ValidatedOutcome(BaseModel):
    episode_id: str
    final_root_cause: str
    final_action: str
    validated_at: datetime
```
Classification: DOCUMENTED FACT (Guidebook §AI)

---

## 10. Knowledge Base Contracts

### FailureMode (YAML structure)
```yaml
subsystems:
  {subsystem_name}:
    components: [string]
    failure_modes:
      - id: string
        component: string
        symptoms: [string]
        telemetry_signature: dict
        prior_probability: float     # [D] illustrative, not KONE-validated
        corrective_action: string    # key into corrective_actions.yaml
```

### CausalLinks (YAML structure)
```yaml
causal_links:
  {primary_alarm_type}: [consequential_alarm_types]
```

### CorrectiveAction (YAML structure)
```yaml
{action_key}:
  description: string
  parts: [string]
  tools: [string]
  typical_repair_minutes: int
  safety_gated: bool
```

---

## 11. Simulator Contracts

### SubsystemSimulator Protocol
```python
class SubsystemSimulator(Protocol):
    def step(self, dt: float, command: dict) -> dict: ...
    def inject_fault(self, fault_type: str, severity: float, start_time: float) -> None: ...
    def active_faults(self) -> list[dict]: ...
```

### FaultGroundTruth
```python
class FaultGroundTruth(BaseModel):
    fault_id: str
    subsystem: str
    component: str
    root_cause: str
    start_time: float
    end_time: float
    severity: float
    affected_signals: list[str]
    expected_alarms: list[str]
```
Classification: DOCUMENTED FACT (Guidebook §L)

## 12. API Request/Response Contracts
Document the key API endpoint contracts from Guidebook §AJ including request bodies and response schemas for:
- POST /telemetry
- POST /events
- POST /fault-injection (demo only)
- GET /fault-episodes
- GET /diagnosis/{episode_id}
- GET /explainability/{episode_id}
- POST /diagnosis/{episode_id}/review
- POST /feedback
