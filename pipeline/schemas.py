"""
ElevateRCA Data Schemas — Strict Pydantic Contracts
Directly adhering to Part 3 (Input Format) and Part 7 (ExplainabilityTrace Output Format).
"""

from typing import List, Optional, Any, Dict, Literal, Union

from pydantic import BaseModel, Field
from datetime import datetime


# ==========================================
# PART 3: INPUT SCHEMA (KONE SOFTWARE OUTPUT)
# ==========================================

class AlarmInput(BaseModel):
    alarm_code: str = Field(..., description="e.g., E-101, DOOR_TIMEOUT, motor_overcurrent")
    alarm_type: str = Field(..., description="e.g., motor_overcurrent, drive_trip, door_close_timeout")
    severity: Literal["critical", "warning", "informational"] = Field(default="critical")
    subsystem: Literal["drive_motor", "door", "brake_traction", "safety_chain", "encoder_position", "sensor_env"] = Field(...)
    timestamp: str = Field(..., description="ISO 8601 timestamp")
    state: Literal["ACTIVE", "CLEARED", "LATCHED", "HISTORICAL"] = Field(default="ACTIVE")


class TelemetryInput(BaseModel):
    signal_name: str = Field(..., description="e.g., motor_current_rms, igbt_temp, vibration_rms")
    value: Union[float, int, str, bool] = Field(..., description="Signal reading")
    unit: str = Field(..., description="Unit of measurement: A, ms, °C, mm, rpm, V, %, state, bool")
    quality: Literal["good", "suspect", "bad", "missing"] = Field(default="good")
    timestamp: str = Field(..., description="ISO 8601 timestamp")
    baseline_value: Optional[Union[float, int, str, bool]] = Field(None, description="Nominal baseline value")
    deviation_pct: Optional[float] = Field(None, description="Percentage deviation from baseline")



class MaintenanceRecordInput(BaseModel):
    date: str = Field(..., description="ISO 8601 date of service")
    component: str = Field(...)
    action: str = Field(...)
    technician_notes: str = Field(default="")
    part_replaced: bool = Field(default=False)


class KONEFaultInput(BaseModel):
    elevator_id: str = Field(..., description="Asset identifier, e.g., KONE-ELV-9421")
    timestamp_utc: str = Field(..., description="Time of fault trigger in ISO 8601")
    operating_state: Literal["IDLE", "ACCELERATING", "CONSTANT_SPEED", "DECELERATING", "DOOR_OPEN", "DOOR_CLOSE", "FAULT_STOP"] = Field(...)
    alarms: List[AlarmInput] = Field(default_factory=list)
    telemetry: List[TelemetryInput] = Field(default_factory=list)
    maintenance_history: List[MaintenanceRecordInput] = Field(default_factory=list)
    technician_free_text: Optional[str] = Field(None, description="Technician observations")
    elevator_model: Optional[str] = Field("KONE MonoSpace 500", description="Elevator model name")
    installation_age_years: Optional[float] = Field(4.5, description="Age in years")
    verification_stage: Optional[str] = Field("SINGLE_STAGE", description="SINGLE_STAGE or TWO_STAGE verification workflow")



# =======================================================
# PART 7: OUTPUT SCHEMA (EXPLAINABILITY TRACE & SYNTHESIS)
# =======================================================

class PrimaryAlarm(BaseModel):
    alarm_code: str
    alarm_type: str
    subsystem: str
    timestamp: str
    severity: str


class ConsequentialAlarm(BaseModel):
    alarm_code: str
    alarm_type: str
    causal_relationship: str


class FaultEpisode(BaseModel):
    primary_alarm: PrimaryAlarm
    consequential_alarms: List[ConsequentialAlarm] = Field(default_factory=list)
    time_span_seconds: float
    episode_classification: str


class EvidenceItem(BaseModel):
    signal_or_record: str
    value: str
    provenance: Literal["MEASURED", "LOGGED", "HISTORICAL", "INFERRED", "UNAVAILABLE", "RAG_RETRIEVED"]
    quality: Literal["good", "suspect", "bad", "missing"]
    diagnostic_value: Literal["HIGH", "MEDIUM", "LOW", "NONE"]
    relevant_to_hypotheses: List[str]
    support_type: Literal["POSITIVE", "NEGATIVE", "NEUTRAL"] = Field(default="POSITIVE")
    # RAG source traceability (backward-compatible — all optional)
    source_document: Optional[str] = Field(None, description="Source document filename for RAG evidence")
    source_page: Optional[int] = Field(None, description="Page number in source document")
    source_section: Optional[str] = Field(None, description="Section heading in source document")
    source_authority: Optional[str] = Field(None, description="Authority level: OEM_REFERENCE, COMPONENT_GUIDE, etc.")
    source_chunk_id: Optional[str] = Field(None, description="Chunk ID for full traceability")


class SupportingEvidence(BaseModel):
    evidence: str
    provenance: Literal["MEASURED", "LOGGED", "HISTORICAL", "INFERRED", "UNAVAILABLE"]
    strength: Literal["STRONG", "MODERATE", "WEAK"]


class ContradictingEvidence(BaseModel):
    evidence: str
    provenance: Literal["MEASURED", "LOGGED", "HISTORICAL", "INFERRED", "UNAVAILABLE"]
    strength: Literal["STRONG", "MODERATE", "WEAK"]


class HypothesisEvaluation(BaseModel):
    rank: int
    hypothesis_id: str
    root_cause: str
    subsystem: str
    posterior_probability: float
    status: Literal["ACTIVE", "ELIMINATED", "WEAKLY_SUPPORTED"]
    supporting_evidence: List[SupportingEvidence] = Field(default_factory=list)
    contradicting_evidence: List[ContradictingEvidence] = Field(default_factory=list)
    eliminated_reason: Optional[str] = None
    expected_but_missing_evidence: List[str] = Field(default_factory=list)


class RCAConclusion(BaseModel):
    root_cause: str
    subsystem: str
    component: str
    causal_narrative: str
    root_cause_confidence: float
    root_cause_confidence_tier: Literal["HIGH", "MEDIUM", "LOW", "ABSTAIN"]
    action_confidence: float
    action_confidence_tier: Literal["HIGH", "MEDIUM", "LOW", "ABSTAIN"]
    abstained: bool
    abstention_reason: Optional[str] = None


class CorrectiveRecommendation(BaseModel):
    recommended_action: str
    specific_steps: List[str]
    do_not_do: List[str]
    estimated_severity: Literal["HIGH", "MEDIUM", "LOW", "CRITICAL"]
    source: str = "corrective_actions_lookup_table"
    warning: str = "This is a RECOMMENDATION only. A qualified elevator technician must verify findings and authorize all corrective actions."


class TechnicianView(BaseModel):
    summary: str
    key_evidence: List[str]
    next_step: str
    confidence_statement: str


class BuildingManagerView(BaseModel):
    summary: str
    expected_downtime: str
    safety_status: str
    action_required: str


class Metadata(BaseModel):
    pipeline_stages_completed: List[str]
    evidence_gaps: List[str]
    claim_discipline_flags: List[str]
    data_provenance_note: str = (
        "All analysis based on provided KONE software output. "
        "No assumptions made about missing values. "
        "Probabilities are engineering estimates, not validated fleet statistics."
    )
    human_verification_required: bool = True
    advisory_only: bool = True


class ExplainabilityTrace(BaseModel):
    investigation_id: str
    elevator_id: str
    analysis_timestamp: str
    fault_episode: FaultEpisode
    evidence_bundle: List[EvidenceItem]
    hypotheses: List[HypothesisEvaluation]
    rca_conclusion: RCAConclusion
    corrective_recommendation: CorrectiveRecommendation
    technician_view: TechnicianView
    building_manager_view: BuildingManagerView
    metadata: Metadata
    detailed_investigation_report: Optional[str] = None
    verification_stage: Optional[str] = "SINGLE_STAGE"
    # RAG source provenance (backward-compatible — defaults to empty)
    rag_sources: Optional[List[Dict[str, Any]]] = Field(
        default_factory=list,
        description="RAG GUIDE corpus sources used in evidence assembly"
    )
