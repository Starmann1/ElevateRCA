"""
ElevateRCA - Canonical End-to-End Diagnostic Demonstration Test
Executes the exact multi-iteration demo sequence defined in Section 41 of Master Specification.
"""

from pathlib import Path
from pipeline.models import (
    CaseStatus,
    HypothesisState,
    ConfidenceTier,
)
from pipeline.state import CaseStateManager
from pipeline.rag.store import GuideKnowledgeStore
from pipeline.rag.retriever import EvidenceRetriever
from pipeline.report import DiagnosticReportGenerator


def test_canonical_e2e_demo_scenario():
    # 0. Initialize RAG with GUIDE folder
    guide_dir = Path("GUIDE")
    store = GuideKnowledgeStore(persist_dir="./chroma_data")
    if store.collection.count() == 0 and guide_dir.exists():
        store.ingest_guide_directory(guide_dir)
    retriever = EvidenceRetriever(store)
    manager = CaseStateManager(retriever=retriever)

    # 1. INITIAL INCIDENT & TRIAGE (Iteration 1)
    case = manager.create_case(
        asset_id="ELEV-DX-04",
        subsystem="Door",
        symptoms=["Door closing timeout", "Increased cycle time (4.8s)", "Vibration during travel"],
        active_faults=["E501 Door Close Timeout"],
        configuration={
            "model": "KONE MonoSpace DX",
            "controller": "KXC Standard",
            "machine_type": "Gearless Traction (EcoDisc)",
            "door_operator": "Belt-Driven Linear Operator",
            "egov": "A",
        },
    )

    assert case.iteration == 1
    assert case.status == CaseStatus.RCA_PROPOSED
    assert len(case.hypotheses) >= 3
    # Initial candidates include roller bearing wear
    roller_hypo = next(h for h in case.hypotheses if h.hypothesis_id == "HYP-DOOR-ROLLER")
    assert roller_hypo.state in [HypothesisState.ACTIVE, HypothesisState.CANDIDATE]

    # 2. TECHNICIAN INSPECTION & EVIDENCE INGESTION (Iteration 2)
    # Technician provides negative evidence on roller + positive evidence on binding
    feedback = (
        "I inspected the roller: there is no visible wear and it rotates freely. "
        "The door becomes harder to move near fully closed with mechanical resistance."
    )
    case = manager.submit_technician_feedback(case.case_id, feedback)

    assert case.iteration == 2
    assert case.status == CaseStatus.RCA_REVISED

    # Roller hypothesis is actively RULED OUT
    roller_hypo = next(h for h in case.hypotheses if h.hypothesis_id == "HYP-DOOR-ROLLER")
    assert roller_hypo.state == HypothesisState.RULED_OUT
    assert len(roller_hypo.contradicting_evidence) >= 1

    # Mechanical binding hypothesis is promoted to leading
    track_hypo = next(h for h in case.hypotheses if h.hypothesis_id == "HYP-DOOR-TRACK-BINDING")
    assert track_hypo.state in [HypothesisState.ACTIVE, HypothesisState.SUPPORTED]
    assert "Door Track / Sill" in case.current_root_cause

    # 3. CONFIRMATION TEST EXECUTION (Iteration 3)
    # Technician executes TEST-TRACK-01 (checks sill groove) and finds grit/obstruction
    case = manager.record_diagnostic_test_result(
        case.case_id,
        test_id="TEST-TRACK-01",
        outcome="FAIL",
        notes="Grit and construction dust found accumulated in landing door sill track groove.",
    )

    assert case.iteration == 3
    assert case.status == CaseStatus.CORRECTIVE_ACTION
    assert "CONFIRMED" in case.current_root_cause
    assert case.confidence_tier == ConfidenceTier.HIGH_SUPPORT
    assert case.recommended_action is not None
    assert "ACT-DOOR-SILL-CLEAN" in case.recommended_action.action_id
    assert len(case.recommended_action.required_parts) > 0

    # 4. POST-REPAIR VALIDATION & CLOSURE (Iteration 4)
    case = manager.submit_post_repair_validation(
        case.case_id,
        fault_cleared=True,
        cycles_passed=5,
        recurrence_observed=False,
        notes="Sill vacuumed and lubricated. 5 test cycles passed with nominal closing time (2.8s).",
    )

    assert case.status == CaseStatus.CLOSED
    assert len(case.validation_records) == 1
    assert case.validation_records[0].fault_cleared is True

    # 5. AUDIT REPORT VERIFICATION
    report_md = DiagnosticReportGenerator.generate_report(case)
    assert "1. INCIDENT SUMMARY" in report_md
    assert "4. PRIMARY ROOT-CAUSE HYPOTHESIS" in report_md
    assert "10. WHAT WOULD CHANGE THE DIAGNOSIS?" in report_md
    assert "17. POST-REPAIR VALIDATION" in report_md
    assert "21. CONFIDENCE / EVIDENCE STATUS" in report_md
    assert "CONFIRMED" in report_md
    assert "RULED_OUT" in report_md
