"""
Unit tests for ElevateRCA domain models.
"""
from datetime import datetime, timezone
from pipeline.models import (
    DiagnosticCase,
    ElevatorConfiguration,
    CaseStatus,
    Hypothesis,
    HypothesisState,
    EvidenceItem,
    EvidenceType,
    EvidencePolarity,
    ReliabilityTier,
    DiagnosticTest,
    CorrectiveAction,
    ValidationResult,
    ConfidenceTier,
)


def test_diagnostic_case_creation():
    case = DiagnosticCase(
        case_id="CASE-2026-001",
        asset_id="ELEV-DX-04",
        subsystem="Door",
        symptoms=["Door takes too long to close", "Vibration on closure"],
        active_faults=["E501 Door Close Timeout"],
    )
    assert case.case_id == "CASE-2026-001"
    assert case.asset_id == "ELEV-DX-04"
    assert case.status == CaseStatus.NEW
    assert case.iteration == 1
    assert len(case.symptoms) == 2


def test_evidence_item_classification():
    # Physical inspection with negative evidence
    evidence = EvidenceItem(
        evidence_id="EVD-001",
        type=EvidenceType.PHYSICAL_INSPECTION,
        description="Skate roller inspected. No visible wear detected.",
        source="Field Technician Report",
        component="Skate Roller",
        polarity=EvidencePolarity.CONTRADICTING,
        reliability=ReliabilityTier.PHYSICAL_INSPECTION,
    )
    assert evidence.type == EvidenceType.PHYSICAL_INSPECTION
    assert evidence.polarity == EvidencePolarity.CONTRADICTING
    assert evidence.reliability == ReliabilityTier.PHYSICAL_INSPECTION


def test_measurement_evidence():
    # Quantitative measurement evidence
    evidence = EvidenceItem(
        evidence_id="EVD-002",
        type=EvidenceType.PHYSICAL_INSPECTION,
        description="Door closing duration measured with stopwatch",
        source="Field Technician",
        component="Door Operator",
        parameter="door_closing_time",
        measurement=4.8,
        unit="seconds",
        polarity=EvidencePolarity.SUPPORTING,
    )
    assert evidence.measurement == 4.8
    assert evidence.unit == "seconds"


def test_hypothesis_state_transitions():
    hypo = Hypothesis(
        hypothesis_id="HYP-001",
        subsystem="Door",
        component="Skate Roller",
        failure_mode="Roller Bearing Wear",
        state=HypothesisState.CANDIDATE,
    )
    assert hypo.state == HypothesisState.CANDIDATE
    
    # Transition to ACTIVE, then DOWNGRADED
    hypo.state = HypothesisState.ACTIVE
    assert hypo.state == HypothesisState.ACTIVE
    
    hypo.state = HypothesisState.DOWNGRADED
    hypo.contradicting_evidence.append("Technician reports zero visible wear on skate roller")
    assert hypo.state == HypothesisState.DOWNGRADED
    assert len(hypo.contradicting_evidence) == 1


def test_post_repair_validation():
    val = ValidationResult(
        validation_id="VAL-001",
        fault_cleared=True,
        initialization_completed=True,
        relearning_completed=True,
        sensor_values_normal=True,
        cycles_passed=10,
        recurrence_observed=False,
    )
    assert val.fault_cleared is True
    assert val.recurrence_observed is False
