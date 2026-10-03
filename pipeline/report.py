"""
ElevateRCA - Comprehensive 21-Section Audit Report Generator
Complies strictly with Section 30 of the Master Specification.
"""

from datetime import datetime, timezone
from typing import Dict, Any, List
from pipeline.models import (
    DiagnosticCase,
    CaseStatus,
    HypothesisState,
    ConfidenceTier,
    EvidenceType,
    EvidencePolarity,
)


class DiagnosticReportGenerator:
    """
    Renders the complete 21-Section ElevateRCA Diagnostic Case Report in structured Markdown.
    """

    @classmethod
    def generate_report(cls, case: DiagnosticCase) -> str:
        lines: List[str] = []

        def add_header(title: str, level: int = 2):
            lines.append(f"\n{'#' * level} {title}\n")

        # Title
        lines.append(f"# ElevateRCA Diagnostic Case Audit Report")
        lines.append(f"**Case Reference:** `{case.case_id}` | **Generated:** {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}")
        lines.append("---")

        # 1. INCIDENT SUMMARY
        add_header("1. INCIDENT SUMMARY")
        lines.append(f"* **Initial Trigger:** {', '.join(case.active_faults) or 'None'}")
        lines.append(f"* **Reported Symptoms:** {', '.join(case.symptoms)}")
        lines.append(f"* **Current Case Status:** `{case.status.value}`")
        lines.append(f"* **Current Iteration:** {case.iteration}")

        # 2. ASSET / CONFIGURATION
        add_header("2. ASSET / CONFIGURATION")
        cfg = case.configuration
        lines.append(f"| Parameter | Value |")
        lines.append(f"| :--- | :--- |")
        lines.append(f"| **Asset Identifier** | `{case.asset_id}` |")
        lines.append(f"| **Elevator Model** | {cfg.model} |")
        lines.append(f"| **Machine Type** | {cfg.machine_type} |")
        lines.append(f"| **Controller** | {cfg.controller} |")
        lines.append(f"| **Door Operator** | {cfg.door_operator} |")
        lines.append(f"| **Safety System** | {cfg.safety_system} (EGOV Setting: `{cfg.egov or 'UNKNOWN / GENERAL'}`) |")

        # 3. CURRENT DIAGNOSTIC STATUS
        add_header("3. CURRENT DIAGNOSTIC STATUS")
        lines.append(f"* **Diagnostic Conclusion:** **{case.current_root_cause or 'Under Investigation'}**")
        lines.append(f"* **Confidence Tier:** `{case.confidence_tier.value}`")

        # 4. PRIMARY ROOT-CAUSE HYPOTHESIS
        add_header("4. PRIMARY ROOT-CAUSE HYPOTHESIS")
        active_hypos = [h for h in case.hypotheses if h.state != HypothesisState.RULED_OUT]
        if active_hypos:
            primary = active_hypos[0]
            lines.append(f"### {primary.component}: {primary.failure_mode}")
            lines.append(f"* **State:** `{primary.state.value}`")
            lines.append(f"* **Support Tier:** `{primary.confidence_tier.value}`")
            lines.append(f"* **Engineering Rationale:** {primary.reasoning or 'Awaiting further sensor correlation.'}")
        else:
            lines.append("No active primary hypothesis remains. All evaluated causes have been ruled out.")

        # 5. SUPPORTING EVIDENCE
        add_header("5. SUPPORTING EVIDENCE")
        supp_items = [ev for ev in case.evidence if ev.polarity == EvidencePolarity.SUPPORTING]
        if supp_items:
            for ev in supp_items:
                meas_str = f" [Measured: {ev.measurement} {ev.unit}]" if ev.measurement is not None else ""
                lines.append(f"* **[{ev.type.value} - {ev.reliability.value}]** {ev.description}{meas_str} *(Source: {ev.source})*")
        else:
            lines.append("No supporting physical evidence currently recorded.")

        # 6. CONTRADICTING EVIDENCE
        add_header("6. CONTRADICTING EVIDENCE")
        contra_items = [ev for ev in case.evidence if ev.polarity == EvidencePolarity.CONTRADICTING]
        if contra_items:
            for ev in contra_items:
                lines.append(f"* **[{ev.type.value} - {ev.reliability.value}]** {ev.description} *(Source: {ev.source})*")
        else:
            lines.append("No contradictory physical evidence currently recorded.")

        # 7. ALTERNATIVE HYPOTHESES
        add_header("7. ALTERNATIVE HYPOTHESES")
        alt_hypos = active_hypos[1:] if len(active_hypos) > 1 else []
        if alt_hypos:
            for h in alt_hypos:
                lines.append(f"* **{h.component} ({h.failure_mode}):** Status `{h.state.value}`, Confidence `{h.confidence_tier.value}`")
        else:
            lines.append("No competing alternative hypotheses currently active.")

        # 8. RULED-OUT / DOWNGRADED CAUSES
        add_header("8. RULED-OUT / DOWNGRADED CAUSES")
        ruled_out = [h for h in case.hypotheses if h.state in [HypothesisState.RULED_OUT, HypothesisState.DOWNGRADED]]
        if ruled_out:
            for h in ruled_out:
                lines.append(f"* **{h.component} ({h.failure_mode}):** `{h.state.value}`")
                lines.append(f"  * *Reasoning:* {h.reasoning}")
                if h.contradicting_evidence:
                    lines.append(f"  * *Contradictory Finding:* {h.contradicting_evidence[0]}")
        else:
            lines.append("None.")

        # 9. DIAGNOSTIC CONFIRMATION TEST
        add_header("9. DIAGNOSTIC CONFIRMATION TEST")
        if active_hypos and active_hypos[0].confirmation_test:
            test = active_hypos[0].confirmation_test
            lines.append(f"**Test ID:** `{test.test_id}` | **Target:** {test.target_component}")
            lines.append(f"* **Purpose:** {test.purpose}")
            lines.append(f"* **Procedure:** {test.procedure}")
            lines.append(f"* **Expected Result (Nominal):** `{test.expected_result}`")
            lines.append(f"* **Safety Prerequisite:** ⚠️ *{test.safety_prerequisites}*")
            lines.append(f"* **OEM Citation:** {test.source_reference}")
        else:
            lines.append("No confirmation test required at current stage.")

        # 10. WHAT WOULD CHANGE THE DIAGNOSIS?
        add_header("10. WHAT WOULD CHANGE THE DIAGNOSIS?")
        if active_hypos and active_hypos[0].confirmation_test:
            test = active_hypos[0].confirmation_test
            lines.append(f"1. **Current Hypothesis:** {active_hypos[0].component} - {active_hypos[0].failure_mode}")
            lines.append(f"2. **Supporting Evidence:** {len(active_hypos[0].supporting_evidence)} items recorded")
            lines.append(f"3. **Contradicting Evidence:** {len(active_hypos[0].contradicting_evidence)} items recorded")
            lines.append(f"4. **Missing Evidence:** Physical verification of: {test.purpose}")
            lines.append(f"5. **Confirmation Test:** {test.procedure}")
            lines.append(f"6. **Expected Nominal Result:** {test.expected_result}")
            lines.append(f"7. **Interpretation IF PASS:** {test.pass_interpretation}")
            lines.append(f"8. **Interpretation IF FAIL:** {test.fail_interpretation}")
        else:
            lines.append("Diagnostic certainty established or awaiting initial triage.")

        # 11. AFFECTED COMPONENTS
        add_header("11. AFFECTED COMPONENTS")
        comps = set(h.component for h in active_hypos)
        lines.append(", ".join(comps) if comps else "None identified.")

        # 12. FAILURE MECHANISM
        add_header("12. FAILURE MECHANISM")
        if active_hypos:
            lines.append(f"Physical failure mode identified: **{active_hypos[0].failure_mode}** in subsystem **{active_hypos[0].subsystem}**.")
        else:
            lines.append("Unresolved.")

        # 13. CORRECTIVE ACTION
        add_header("13. CORRECTIVE ACTION")
        if case.recommended_action:
            act = case.recommended_action
            lines.append(f"### {act.title}")
            lines.append(f"* **Action ID:** `{act.action_id}`")
            lines.append(f"* **Procedure:** {act.procedure}")
            lines.append(f"* **Source Manual:** {act.source_document} (Page {act.page}, {act.section})")
            if act.safety_warnings:
                lines.append(f"* **Safety Warning:** ⚠️ *{act.safety_warnings[0]}*")
        else:
            lines.append("Corrective action deferred until diagnostic confirmation test is executed.")

        # 14. REQUIRED PARTS
        add_header("14. REQUIRED PARTS")
        if case.recommended_action and case.recommended_action.required_parts:
            for p in case.recommended_action.required_parts:
                lines.append(f"* [ ] {p}")
        else:
            lines.append("None specified.")

        # 15. REQUIRED TOOLS
        add_header("15. REQUIRED TOOLS")
        if case.recommended_action and case.recommended_action.required_tools:
            for t in case.recommended_action.required_tools:
                lines.append(f"* [ ] {t}")
        else:
            lines.append("Standard elevator technician toolkit.")

        # 16. PREVENTIVE ACTION
        add_header("16. PREVENTIVE ACTION")
        lines.append(f"Implement periodic maintenance check according to `{case.configuration.model}` maintenance schedule.")

        # 17. POST-REPAIR VALIDATION
        add_header("17. POST-REPAIR VALIDATION")
        if case.validation_records:
            val = case.validation_records[-1]
            status_str = "PASSED" if val.fault_cleared and not val.recurrence_observed else "FAILED"
            lines.append(f"* **Validation Status:** `{status_str}`")
            lines.append(f"* **Fault Cleared:** `{val.fault_cleared}` | **Test Cycles Completed:** {val.cycles_passed}")
            lines.append(f"* **Recurrence Observed:** `{val.recurrence_observed}`")
            if val.technician_notes:
                lines.append(f"* **Technician Sign-off Notes:** {val.technician_notes}")
        else:
            lines.append("Pending execution after physical repair.")

        # 18. SOURCE DOCUMENTS
        add_header("18. SOURCE DOCUMENTS")
        if case.source_references:
            for ref in case.source_references:
                lines.append(f"* 📄 {ref}")
        else:
            lines.append("No OEM references retrieved.")

        # 19. DIAGNOSTIC ITERATION HISTORY
        add_header("19. DIAGNOSTIC ITERATION HISTORY")
        for it in case.iterations:
            lines.append(f"**Iteration {it.iteration_number}** ({it.timestamp.strftime('%H:%M:%S UTC')}): {it.trigger_event}")
            if it.notes:
                lines.append(f"  * *Outcome:* {it.notes}")

        # 20. TECHNICIAN FEEDBACK HISTORY
        add_header("20. TECHNICIAN FEEDBACK HISTORY")
        tech_evd = [e for e in case.evidence if e.type in [EvidenceType.PHYSICAL_INSPECTION, EvidenceType.TECHNICIAN_OBSERVATION, EvidenceType.TECHNICIAN_OPINION]]
        if tech_evd:
            for e in tech_evd:
                lines.append(f"* **[{e.type.value}]** {e.description} *(Reliability: {e.reliability.value})*")
        else:
            lines.append("No technician notes recorded.")

        # 21. CONFIDENCE / EVIDENCE STATUS
        add_header("21. CONFIDENCE / EVIDENCE STATUS")
        lines.append(f"* **System Confidence Tier:** `{case.confidence_tier.value}`")
        lines.append(f"* **Abstention State:** {'ACTIVE (Refusing to speculate)' if case.confidence_tier == ConfidenceTier.INSUFFICIENT_EVIDENCE else 'INACTIVE'}")
        lines.append(f"* **Human Sign-Off Status:** {'VERIFIED & COMPLETED' if case.status == CaseStatus.CLOSED else 'AWAITING TECHNICIAN ACTION'}")

        return "\n".join(lines)
