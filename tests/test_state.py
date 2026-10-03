"""
Unit & Integration Tests for CaseStateManager, Iterative RCA, Contradiction Detection,
and Closed-Loop Validation Lifecycle.
"""

from pipeline.models import (
    CaseStatus,
    HypothesisState,
    ConfidenceTier,
)
from pipeline.state import CaseStateManager


def test_closed_loop_diagnostic_lifecycle():
    manager = CaseStateManager(retriever=None)

    # STEP 1: Case Creation & Initial RCA (Iteration 1)
    case = manager.create_case(
        asset_id="ELEV-DX-04",
        subsystem="Door",
        symptoms=["Door close timeout", "Increased cycle time"],
        active_faults=["E501 Door Close Timeout"],
    )
    assert case.iteration == 1
    assert case.status == CaseStatus.RCA_PROPOSED
    assert len(case.hypotheses) >= 3

    # Initially, roller degradation is an active candidate
    roller_hypo = next(h for h in case.hypotheses if h.hypothesis_id == "HYP-DOOR-ROLLER")
    assert roller_hypo.state in [HypothesisState.ACTIVE, HypothesisState.CANDIDATE]

    # STEP 2: Technician Feedback (Negative evidence on roller + Positive evidence on binding)
    feedback_text = (
        "I inspected the roller: there is no visible wear and it rotates freely. "
        "The door becomes harder to move near fully closed with mechanical resistance."
    )
    case = manager.submit_technician_feedback(case.case_id, feedback_text)

    # Iteration must increment to 2
    assert case.iteration == 2
    assert case.status == CaseStatus.RCA_REVISED

    # Roller hypothesis must be RULED OUT by negative evidence
    roller_hypo = next(h for h in case.hypotheses if h.hypothesis_id == "HYP-DOOR-ROLLER")
    assert roller_hypo.state == HypothesisState.RULED_OUT
    assert len(roller_hypo.contradicting_evidence) >= 1

    # Track binding hypothesis must now be active/supported and leading
    track_hypo = next(h for h in case.hypotheses if h.hypothesis_id == "HYP-DOOR-TRACK-BINDING")
    assert track_hypo.state in [HypothesisState.ACTIVE, HypothesisState.SUPPORTED]
    assert "Door Track / Sill" in case.current_root_cause

    # STEP 3: Diagnostic Confirmation Test Execution
    # Technician performs physical check on track groove and confirms debris
    case = manager.record_diagnostic_test_result(
        case.case_id,
        test_id="TEST-TRACK-01",
        outcome="FAIL",
        notes="Heavy grit and debris discovered packed into bottom sill groove at floor sill.",
    )

    assert case.iteration == 3
    assert case.status == CaseStatus.CORRECTIVE_ACTION
    assert "CONFIRMED" in case.current_root_cause
    assert case.confidence_tier == ConfidenceTier.HIGH_SUPPORT
    assert case.recommended_action is not None
    assert "ACT-DOOR-SILL-CLEAN" in case.recommended_action.action_id

    # STEP 4: Post-Repair Validation & Case Closure
    case = manager.submit_post_repair_validation(
        case.case_id,
        fault_cleared=True,
        cycles_passed=5,
        recurrence_observed=False,
        notes="Debris vacuumed, sill guide shoes inspected, 5 test door cycles nominal.",
    )

    assert case.status == CaseStatus.CLOSED
    assert len(case.validation_records) == 1
    assert case.validation_records[0].fault_cleared is True


def test_post_repair_validation_failure_reopens_rca():
    manager = CaseStateManager(retriever=None)

    case = manager.create_case(
        asset_id="ELEV-DX-04",
        subsystem="Door",
        symptoms=["Door close timeout"],
        active_faults=["E501 Door Close Timeout"],
    )

    # Submit validation with failure (fault recurred)
    case = manager.submit_post_repair_validation(
        case.case_id,
        fault_cleared=False,
        cycles_passed=1,
        recurrence_observed=True,
        notes="Door jammed again on 2nd cycle test.",
    )

    # Case must transition to RCA_REOPENED, NOT CLOSED!
    assert case.status == CaseStatus.RCA_REOPENED
    assert case.iteration == 2
    # Recurrence must be recorded as new evidence
    assert any("reopen" in ev.evidence_id.lower() or "post-repair" in ev.description.lower() for ev in case.evidence)
