"""
ElevateRCA - Diagnostic Case API Endpoints
"""

from typing import Dict, Any, Optional, List
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field

from pipeline.models import DiagnosticCase
from pipeline.state import CaseStateManager
from pipeline.report import DiagnosticReportGenerator

router = APIRouter(prefix="/cases", tags=["Diagnostic Cases"])

# Singleton case manager instance for API process
_case_manager: Optional[CaseStateManager] = None


def get_case_manager() -> CaseStateManager:
    global _case_manager
    if _case_manager is None:
        from pipeline.rag.store import GuideKnowledgeStore
        from pipeline.rag.retriever import EvidenceRetriever
        store = GuideKnowledgeStore()
        retriever = EvidenceRetriever(store)
        _case_manager = CaseStateManager(retriever=retriever)
    return _case_manager


# Request schemas
class CreateCaseRequest(BaseModel):
    asset_id: str
    subsystem: str = "Door"
    symptoms: List[str] = Field(default_factory=lambda: ["Door closing cycle slow"])
    active_faults: List[str] = Field(default_factory=lambda: ["E501 Door Close Timeout"])
    configuration: Optional[Dict[str, Any]] = None


class TechnicianFeedbackRequest(BaseModel):
    feedback_text: str


class DiagnosticTestResultRequest(BaseModel):
    test_id: str
    outcome: str  # PASS, FAIL, NOT_PERFORMED
    notes: Optional[str] = None


class PostRepairValidationRequest(BaseModel):
    fault_cleared: bool
    cycles_passed: int = 5
    recurrence_observed: bool = False
    notes: Optional[str] = None


@router.post("", response_model=DiagnosticCase)
def create_case(
    req: CreateCaseRequest,
    manager: CaseStateManager = Depends(get_case_manager),
):
    """Creates a new diagnostic case and runs initial triage & Iteration 1 RCA."""
    return manager.create_case(
        asset_id=req.asset_id,
        subsystem=req.subsystem,
        symptoms=req.symptoms,
        active_faults=req.active_faults,
        configuration=req.configuration,
    )


@router.get("/{case_id}", response_model=DiagnosticCase)
def get_case(
    case_id: str,
    manager: CaseStateManager = Depends(get_case_manager),
):
    """Retrieves current case state, competing hypotheses, and iteration history."""
    case = manager.get_case(case_id)
    if not case:
        raise HTTPException(status_code=404, detail=f"Case '{case_id}' not found.")
    return case


@router.post("/{case_id}/technician-feedback", response_model=DiagnosticCase)
def submit_feedback(
    case_id: str,
    req: TechnicianFeedbackRequest,
    manager: CaseStateManager = Depends(get_case_manager),
):
    """
    Submits informal technician field observation.
    Triggers structured evidence interpretation, targeted RAG retrieval,
    and advances case to Iteration N+1 (RCA_REVISED).
    """
    try:
        return manager.submit_technician_feedback(case_id, req.feedback_text)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/{case_id}/diagnostic-test", response_model=DiagnosticCase)
def record_test(
    case_id: str,
    req: DiagnosticTestResultRequest,
    manager: CaseStateManager = Depends(get_case_manager),
):
    """Records the outcome of a physical confirmation test and updates hypothesis confirmation."""
    try:
        return manager.record_diagnostic_test_result(
            case_id=case_id,
            test_id=req.test_id,
            outcome=req.outcome,
            notes=req.notes,
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/{case_id}/post-repair-validation", response_model=DiagnosticCase)
def submit_validation(
    case_id: str,
    req: PostRepairValidationRequest,
    manager: CaseStateManager = Depends(get_case_manager),
):
    """
    Validates physical repair:
    - If passed: Case transitions to CLOSED.
    - If failed / recurrence: Case transitions to RCA_REOPENED.
    """
    try:
        return manager.submit_post_repair_validation(
            case_id=case_id,
            fault_cleared=req.fault_cleared,
            cycles_passed=req.cycles_passed,
            recurrence_observed=req.recurrence_observed,
            notes=req.notes,
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/{case_id}/report")
def get_report(
    case_id: str,
    manager: CaseStateManager = Depends(get_case_manager),
):
    """Generates the full 21-section Markdown audit report."""
    case = manager.get_case(case_id)
    if not case:
        raise HTTPException(status_code=404, detail=f"Case '{case_id}' not found.")
    report_text = DiagnosticReportGenerator.generate_report(case)
    return {"case_id": case_id, "report_markdown": report_text}
