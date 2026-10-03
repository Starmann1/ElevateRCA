"""
ElevateRCA - Core Domain Models & Typed Data Contracts
Author: Team NexGen / Arul Amudhan G
"""

from __future__ import annotations
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, Field


# ============================================================================
# Enums
# ============================================================================

class CaseStatus(str, Enum):
    NEW = "NEW"
    TRIAGED = "TRIAGED"
    UNDER_INVESTIGATION = "UNDER_INVESTIGATION"
    RCA_PROPOSED = "RCA_PROPOSED"
    TECHNICIAN_REVIEW = "TECHNICIAN_REVIEW"
    ADDITIONAL_EVIDENCE = "ADDITIONAL_EVIDENCE"
    RCA_REVISED = "RCA_REVISED"
    DIAGNOSTIC_CONFIRMATION = "DIAGNOSTIC_CONFIRMATION"
    CORRECTIVE_ACTION = "CORRECTIVE_ACTION"
    POST_REPAIR_VALIDATION = "POST_REPAIR_VALIDATION"
    CLOSED = "CLOSED"
    RCA_REOPENED = "RCA_REOPENED"


class HypothesisState(str, Enum):
    CANDIDATE = "CANDIDATE"
    ACTIVE = "ACTIVE"
    SUPPORTED = "SUPPORTED"
    DOWNGRADED = "DOWNGRADED"
    RULED_OUT = "RULED_OUT"
    CONFIRMED = "CONFIRMED"


class EvidenceType(str, Enum):
    TELEMETRY = "TELEMETRY"
    FAULT_LOG = "FAULT_LOG"
    HISTORICAL_DATA = "HISTORICAL_DATA"
    MAINTENANCE_HISTORY = "MAINTENANCE_HISTORY"
    OEM_DOCUMENTATION = "OEM_DOCUMENTATION"
    DIAGNOSTIC_TEST_RESULT = "DIAGNOSTIC_TEST_RESULT"
    PHYSICAL_INSPECTION = "PHYSICAL_INSPECTION"
    TECHNICIAN_OBSERVATION = "TECHNICIAN_OBSERVATION"
    TECHNICIAN_OPINION = "TECHNICIAN_OPINION"
    POST_REPAIR_VALIDATION = "POST_REPAIR_VALIDATION"


class EvidencePolarity(str, Enum):
    SUPPORTING = "SUPPORTING"
    CONTRADICTING = "CONTRADICTING"
    NEUTRAL = "NEUTRAL"


class ReliabilityTier(str, Enum):
    VERIFIED_SENSOR = "VERIFIED_SENSOR"
    PHYSICAL_INSPECTION = "PHYSICAL_INSPECTION"
    OEM_AUTHORITY = "OEM_AUTHORITY"
    TECHNICIAN_REPORTED = "TECHNICIAN_REPORTED"
    TECHNICIAN_OPINION = "TECHNICIAN_OPINION"
    UNVERIFIED = "UNVERIFIED"


class AuthorityTier(str, Enum):
    TIER_1 = "TIER_1"  # OEM Maintenance Manuals, OEM Fault Codes, SETS
    TIER_2 = "TIER_2"  # Component/System Guides (Brake, Door, Hoisting)
    TIER_3 = "TIER_3"  # Structured Troubleshooting Dataset (CSV/JSON)
    TIER_4 = "TIER_4"  # General Engineering / External Knowledge


class ConfidenceTier(str, Enum):
    HIGH_SUPPORT = "HIGH_SUPPORT"
    MODERATE_SUPPORT = "MODERATE_SUPPORT"
    LOW_SUPPORT = "LOW_SUPPORT"
    INSUFFICIENT_EVIDENCE = "INSUFFICIENT_EVIDENCE"


class DocumentType(str, Enum):
    SAFETY_SYSTEM_MANUAL = "SAFETY_SYSTEM_MANUAL"
    MAINTENANCE_MANUAL = "MAINTENANCE_MANUAL"
    TROUBLESHOOTING_MANUAL = "TROUBLESHOOTING_MANUAL"
    FAULT_CODE_REFERENCE = "FAULT_CODE_REFERENCE"
    COMPONENT_GUIDE = "COMPONENT_GUIDE"
    MECHANICAL_SYSTEM_GUIDE = "MECHANICAL_SYSTEM_GUIDE"
    DOOR_SYSTEM_GUIDE = "DOOR_SYSTEM_GUIDE"
    BRAKE_SYSTEM_GUIDE = "BRAKE_SYSTEM_GUIDE"
    HOISTING_SYSTEM_GUIDE = "HOISTING_SYSTEM_GUIDE"
    OEM_REFERENCE = "OEM_REFERENCE"
    TROUBLESHOOTING_DATASET = "TROUBLESHOOTING_DATASET"


# ============================================================================
# RAG & Document Metadata Contracts
# ============================================================================

class DocumentMetadata(BaseModel):
    document_id: str
    filename: str
    document_type: DocumentType
    authority: AuthorityTier
    manufacturer: str = "OEM / KONE"
    system: str = "Elevator"
    subsystem: str = "General"
    component: Optional[str] = None
    failure_mode: Optional[str] = None
    fault_code: Optional[str] = None
    model: str = "All"
    configuration: Optional[str] = None
    egov_setting: Optional[str] = None
    espd_setting: Optional[str] = None
    procedure_type: Optional[str] = None
    section: Optional[str] = None
    page: Optional[int] = None
    source: str = "GUIDE"
    title: Optional[str] = None
    data_type: str = "TEXT"  # TEXT, TABLE, WARNING, PROCEDURE


class DocumentChunk(BaseModel):
    chunk_id: str
    content: str
    metadata: DocumentMetadata
    tables: List[Dict[str, Any]] = Field(default_factory=list)


# ============================================================================
# Evidence Models
# ============================================================================

class EvidenceItem(BaseModel):
    evidence_id: str
    type: EvidenceType
    description: str
    source: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    component: Optional[str] = None
    parameter: Optional[str] = None
    measurement: Optional[Union[float, str]] = None
    unit: Optional[str] = None
    polarity: EvidencePolarity = EvidencePolarity.NEUTRAL
    reliability: ReliabilityTier = ReliabilityTier.TECHNICIAN_REPORTED
    linked_hypotheses: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)


# ============================================================================
# Diagnostic Test & Action Models
# ============================================================================

class DiagnosticTest(BaseModel):
    test_id: str
    purpose: str
    procedure: str
    source_reference: Optional[str] = None
    expected_result: str
    pass_interpretation: str
    fail_interpretation: str
    safety_prerequisites: str
    target_component: Optional[str] = None
    status: str = "PENDING"  # PENDING, PASS, FAIL, NOT_PERFORMED, NOT_APPLICABLE
    actual_result: Optional[str] = None
    recorded_at: Optional[datetime] = None


class CorrectiveAction(BaseModel):
    action_id: str
    title: str
    procedure: str
    source_document: Optional[str] = None
    page: Optional[int] = None
    section: Optional[str] = None
    safety_warnings: List[str] = Field(default_factory=list)
    required_parts: List[str] = Field(default_factory=list)
    required_tools: List[str] = Field(default_factory=list)
    post_repair_validation: List[str] = Field(default_factory=list)
    requires_confirmation_first: bool = True


class ValidationResult(BaseModel):
    validation_id: str
    fault_cleared: bool
    initialization_completed: bool = True
    relearning_completed: bool = True
    sensor_values_normal: bool = True
    cycles_passed: int = 5
    recurrence_observed: bool = False
    technician_notes: Optional[str] = None
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


# ============================================================================
# Hypothesis Model
# ============================================================================

class Hypothesis(BaseModel):
    hypothesis_id: str
    subsystem: str
    component: str
    failure_mode: str
    state: HypothesisState = HypothesisState.CANDIDATE
    confidence_tier: ConfidenceTier = ConfidenceTier.MODERATE_SUPPORT
    supporting_evidence: List[str] = Field(default_factory=list)
    contradicting_evidence: List[str] = Field(default_factory=list)
    missing_evidence: List[str] = Field(default_factory=list)
    confirmation_test: Optional[DiagnosticTest] = None
    recommended_action: Optional[CorrectiveAction] = None
    reasoning: Optional[str] = None
    source_citations: List[str] = Field(default_factory=list)
    prior_probability: float = 0.20
    posterior_probability: Optional[float] = None


# ============================================================================
# Diagnostic Case Iteration & Persistent State
# ============================================================================

class CaseIteration(BaseModel):
    iteration_number: int
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    trigger_event: str
    hypotheses: List[Hypothesis] = Field(default_factory=list)
    leading_hypothesis_id: Optional[str] = None
    confidence_tier: ConfidenceTier = ConfidenceTier.INSUFFICIENT_EVIDENCE
    evidence_added: List[EvidenceItem] = Field(default_factory=list)
    notes: Optional[str] = None


class ElevatorConfiguration(BaseModel):
    model: str = "KONE MonoSpace DX"
    controller: str = "KXC Standard"
    machine_type: str = "Gearless Traction (EcoDisc)"
    door_operator: str = "Belt-Driven Linear Operator"
    egov: Optional[str] = None  # SETS-01 Setting: 8, 9, A, B, D, E, F
    espd: Optional[str] = None
    safety_system: str = "SETS-01"


class DiagnosticCase(BaseModel):
    case_id: str
    asset_id: str
    configuration: ElevatorConfiguration = Field(default_factory=ElevatorConfiguration)
    subsystem: str = "Door"
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    iteration: int = 1
    status: CaseStatus = CaseStatus.NEW

    # Active lists
    active_faults: List[str] = Field(default_factory=list)
    symptoms: List[str] = Field(default_factory=list)
    evidence: List[EvidenceItem] = Field(default_factory=list)
    hypotheses: List[Hypothesis] = Field(default_factory=list)
    pending_tests: List[DiagnosticTest] = Field(default_factory=list)
    completed_tests: List[DiagnosticTest] = Field(default_factory=list)
    validation_records: List[ValidationResult] = Field(default_factory=list)

    # Current diagnostic conclusion
    current_root_cause: Optional[str] = None
    confidence_tier: ConfidenceTier = ConfidenceTier.INSUFFICIENT_EVIDENCE
    recommended_action: Optional[CorrectiveAction] = None
    required_parts: List[str] = Field(default_factory=list)
    required_tools: List[str] = Field(default_factory=list)

    # Full history
    iterations: List[CaseIteration] = Field(default_factory=list)
    source_references: List[str] = Field(default_factory=list)
    safety_constraints: List[str] = Field(default_factory=list)
