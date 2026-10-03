"""
ElevateRCA - Case State Machine, Lifecycle Controller & Iteration History Manager
Implements closed-loop iterative diagnostics:
NEW -> TRIAGED -> UNDER_INVESTIGATION -> RCA_PROPOSED -> TECHNICIAN_REVIEW ->
ADDITIONAL_EVIDENCE -> RCA_REVISED -> DIAGNOSTIC_CONFIRMATION ->
CORRECTIVE_ACTION -> POST_REPAIR_VALIDATION -> CLOSED / RCA_REOPENED
"""

import uuid
from typing import Dict, Any, Optional, List
from datetime import datetime, timezone

from pipeline.models import (
    DiagnosticCase,
    CaseIteration,
    CaseStatus,
    Hypothesis,
    HypothesisState,
    EvidenceItem,
    EvidenceType,
    EvidencePolarity,
    ReliabilityTier,
    DiagnosticTest,
    ValidationResult,
    ConfidenceTier,
)
from pipeline.rca import RCAEngine
from pipeline.technician import TechnicianFeedbackAgent
from pipeline.rag.retriever import EvidenceRetriever


class CaseStateManager:
    """
    Manages in-memory and persistent DiagnosticCase lifecycle, multi-iteration transitions,
    and audit trail assembly.
    """
    def __init__(self, retriever: Optional[EvidenceRetriever] = None):
        self.cases: Dict[str, DiagnosticCase] = {}
        self.retriever = retriever

    def create_case(
        self,
        asset_id: str,
        subsystem: str = "Door",
        symptoms: Optional[List[str]] = None,
        active_faults: Optional[List[str]] = None,
        configuration: Optional[Dict[str, Any]] = None,
    ) -> DiagnosticCase:
        """
        Initializes a NEW diagnostic case and runs initial triage and initial RCA (Iteration 1).
        """
        case_id = f"CASE-{datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:6].upper()}"
        
        case = DiagnosticCase(
            case_id=case_id,
            asset_id=asset_id,
            subsystem=subsystem,
            symptoms=symptoms or ["Abnormal door cycle behavior"],
            active_faults=active_faults or ["E501 Door Close Timeout"],
            status=CaseStatus.NEW,
            iteration=1,
        )

        if configuration:
            for k, v in configuration.items():
                if hasattr(case.configuration, k):
                    setattr(case.configuration, k, v)

        # Transition NEW -> TRIAGED -> UNDER_INVESTIGATION -> RCA_PROPOSED
        case.status = CaseStatus.UNDER_INVESTIGATION
        
        # 1. Query RAG for initial background context
        if self.retriever:
            rag_query = f"{case.subsystem} {' '.join(case.symptoms)}"
            rag_res = self.retriever.retrieve(
                query=rag_query,
                subsystem=case.subsystem,
                configuration=case.configuration,
                top_k=3,
            )
            case.source_references = rag_res.get("source_references", [])
            case.safety_constraints = rag_res.get("safety_constraints", [])

        # 2. Run Initial RCA Reasoning (Iteration 1)
        case = RCAEngine.evaluate_case(case, self.retriever)
        case.status = CaseStatus.RCA_PROPOSED

        # 3. Snapshot Iteration 1 into history
        iteration_snap = CaseIteration(
            iteration_number=1,
            trigger_event="Initial Incident Triage & Telemetry Anomaly Ingestion",
            hypotheses=[h.model_copy(deep=True) for h in case.hypotheses],
            leading_hypothesis_id=case.hypotheses[0].hypothesis_id if case.hypotheses else None,
            confidence_tier=case.confidence_tier,
            notes=f"Initial diagnosis: {case.current_root_cause}",
        )
        case.iterations.append(iteration_snap)

        self.cases[case_id] = case
        return case

    def submit_technician_feedback(
        self,
        case_id: str,
        feedback_text: str,
    ) -> DiagnosticCase:
        """
        Processes natural language technician observations.
        Transitions: TECHNICIAN_REVIEW -> ADDITIONAL_EVIDENCE -> RCA_REVISED (Iteration N+1).
        """
        case = self.cases.get(case_id)
        if not case:
            raise ValueError(f"Case '{case_id}' not found.")

        # 1. Interpret feedback into structured evidence
        new_evidence_items = TechnicianFeedbackAgent.interpret(feedback_text, default_subsystem=case.subsystem)
        case.evidence.extend(new_evidence_items)
        case.status = CaseStatus.ADDITIONAL_EVIDENCE

        # 2. Target RAG Retrieval for new observations
        if self.retriever and new_evidence_items:
            evidence_query = " ".join([ev.description for ev in new_evidence_items if ev.polarity.value != "NEUTRAL"])
            if evidence_query.strip():
                rag_res = self.retriever.retrieve(
                    query=evidence_query,
                    subsystem=case.subsystem,
                    configuration=case.configuration,
                    top_k=3,
                )
                for ref in rag_res.get("source_references", []):
                    if ref not in case.source_references:
                        case.source_references.append(ref)

        # 3. Increment iteration counter
        case.iteration += 1

        # 4. Re-evaluate Hypotheses with Contradiction & Alternative Elimination
        case = RCAEngine.evaluate_case(case, self.retriever)
        case.status = CaseStatus.RCA_REVISED

        # 5. Record Iteration Snapshot
        snap = CaseIteration(
            iteration_number=case.iteration,
            trigger_event=f"Technician Feedback Ingestion: '{feedback_text[:80]}...'",
            hypotheses=[h.model_copy(deep=True) for h in case.hypotheses],
            leading_hypothesis_id=case.hypotheses[0].hypothesis_id if case.hypotheses else None,
            confidence_tier=case.confidence_tier,
            evidence_added=new_evidence_items,
            notes=f"Revised diagnosis after feedback: {case.current_root_cause}",
        )
        case.iterations.append(snap)

        return case

    def record_diagnostic_test_result(
        self,
        case_id: str,
        test_id: str,
        outcome: str,  # PASS, FAIL, NOT_PERFORMED
        notes: Optional[str] = None,
    ) -> DiagnosticCase:
        """
        Records the outcome of a physical confirmation test.
        """
        case = self.cases.get(case_id)
        if not case:
            raise ValueError(f"Case '{case_id}' not found.")

        case.status = CaseStatus.DIAGNOSTIC_CONFIRMATION
        test_outcome_upper = outcome.upper().strip()

        # Find matching test
        matched_test = None
        for hypo in case.hypotheses:
            if hypo.confirmation_test and hypo.confirmation_test.test_id == test_id:
                matched_test = hypo.confirmation_test
                matched_test.status = test_outcome_upper
                matched_test.actual_result = notes or test_outcome_upper
                matched_test.recorded_at = datetime.now(timezone.utc)
                case.completed_tests.append(matched_test)

                # If test confirms root cause (FAIL on pass criteria = fault present)
                if test_outcome_upper == "FAIL":
                    hypo.state = HypothesisState.CONFIRMED
                    hypo.confidence_tier = ConfidenceTier.HIGH_SUPPORT
                    case.current_root_cause = f"CONFIRMED: {hypo.component} - {hypo.failure_mode}"
                    case.confidence_tier = ConfidenceTier.HIGH_SUPPORT
                    case.recommended_action = hypo.recommended_action
                    case.status = CaseStatus.CORRECTIVE_ACTION
                elif test_outcome_upper == "PASS":
                    hypo.state = HypothesisState.RULED_OUT
                    hypo.confidence_tier = ConfidenceTier.LOW_SUPPORT

        case.iteration += 1
        case = RCAEngine.evaluate_case(case, self.retriever)

        snap = CaseIteration(
            iteration_number=case.iteration,
            trigger_event=f"Confirmation Test Result Recorded: {test_id} -> {test_outcome_upper}",
            hypotheses=[h.model_copy(deep=True) for h in case.hypotheses],
            leading_hypothesis_id=case.hypotheses[0].hypothesis_id if case.hypotheses else None,
            confidence_tier=case.confidence_tier,
            notes=f"State after test {test_id}: {case.current_root_cause}",
        )
        case.iterations.append(snap)
        return case

    def submit_post_repair_validation(
        self,
        case_id: str,
        fault_cleared: bool,
        cycles_passed: int = 5,
        recurrence_observed: bool = False,
        notes: Optional[str] = None,
    ) -> DiagnosticCase:
        """
        Post-Repair Validation Gatekeeper:
        - If fault_cleared and not recurrence_observed -> CLOSED
        - If recurrence or not fault_cleared -> RCA_REOPENED
        """
        case = self.cases.get(case_id)
        if not case:
            raise ValueError(f"Case '{case_id}' not found.")

        validation = ValidationResult(
            validation_id=f"VAL-{uuid.uuid4().hex[:6].upper()}",
            fault_cleared=fault_cleared,
            cycles_passed=cycles_passed,
            recurrence_observed=recurrence_observed,
            technician_notes=notes,
        )
        case.validation_records.append(validation)
        case.status = CaseStatus.POST_REPAIR_VALIDATION

        if fault_cleared and not recurrence_observed and cycles_passed >= 3:
            case.status = CaseStatus.CLOSED
            closure_note = f"Case successfully closed: Post-repair validation passed ({cycles_passed} test cycles nominal)."
        else:
            case.status = CaseStatus.RCA_REOPENED
            closure_note = "Post-repair validation FAILED. Fault recurrence observed or fault failed to clear. Reopening RCA."
            case.iteration += 1
            # Add recurrence as evidence
            case.evidence.append(
                EvidenceItem(
                    evidence_id=f"REOPEN-EVD-{uuid.uuid4().hex[:6].upper()}",
                    type=EvidenceType.POST_REPAIR_VALIDATION,
                    description=f"Post-repair validation failed: {notes or 'Fault persisted upon cycle test'}",
                    source="Post-Repair Validation Gatekeeper",
                    component=case.subsystem,
                    polarity=EvidencePolarity.SUPPORTING,
                    reliability=ReliabilityTier.VERIFIED_SENSOR,
                )
            )
            case = RCAEngine.evaluate_case(case, self.retriever)

        case.iterations.append(
            CaseIteration(
                iteration_number=case.iteration,
                trigger_event="Post-Repair Validation Submission",
                hypotheses=[h.model_copy(deep=True) for h in case.hypotheses],
                leading_hypothesis_id=case.hypotheses[0].hypothesis_id if case.hypotheses else None,
                confidence_tier=case.confidence_tier,
                notes=closure_note,
            )
        )
        return case

    def get_case(self, case_id: str) -> Optional[DiagnosticCase]:
        return self.cases.get(case_id)
