"""
ElevateRCA - Iterative Root Cause Analysis Engine
Evaluates multi-hypothesis space, computes qualitative support tiers,
detects contradictions, executes alternative cause elimination, and enforces principled abstention.
"""

from typing import List, Dict, Any, Optional, Tuple
from pipeline.models import (
    DiagnosticCase,
    Hypothesis,
    HypothesisState,
    EvidenceItem,
    EvidenceType,
    EvidencePolarity,
    ReliabilityTier,
    ConfidenceTier,
    DiagnosticTest,
    CorrectiveAction,
)
from pipeline.rag.retriever import EvidenceRetriever


class RCAEngine:
    """
    RCA Reasoning Core with active alternative elimination and contradiction detection.
    """

    @classmethod
    def evaluate_case(
        cls,
        case: DiagnosticCase,
        retriever: Optional[EvidenceRetriever] = None,
    ) -> DiagnosticCase:
        """
        Runs an RCA evaluation cycle on the DiagnosticCase.
        Evaluates supporting, contradicting, and missing evidence for all candidate hypotheses.
        """
        if not case.hypotheses:
            case.hypotheses = cls._generate_initial_hypotheses(case)

        # Cross-reference every active hypothesis against all accumulated evidence
        for hypo in case.hypotheses:
            if hypo.state == HypothesisState.RULED_OUT:
                continue

            supporting = []
            contradicting = []

            for ev in case.evidence:
                comp_match = False
                if ev.component and hypo.component:
                    comp_match = (
                        ev.component.lower() in hypo.component.lower()
                        or hypo.component.lower() in ev.component.lower()
                    )

                if ev.polarity == EvidencePolarity.CONTRADICTING:
                    if comp_match or any(word in ev.description.lower() for word in hypo.failure_mode.lower().split()):
                        contradicting.append(f"[{ev.source}] {ev.description}")
                elif ev.polarity == EvidencePolarity.SUPPORTING:
                    if comp_match or any(word in ev.description.lower() for word in hypo.failure_mode.lower().split()):
                        supporting.append(f"[{ev.source}] {ev.description}")

            hypo.supporting_evidence = list(set(supporting))
            hypo.contradicting_evidence = list(set(contradicting))

            # Maintain CONFIRMED state if already confirmed by physical test
            if hypo.state == HypothesisState.CONFIRMED:
                hypo.confidence_tier = ConfidenceTier.HIGH_SUPPORT
                continue

            # Update hypothesis state based on contradiction vs support
            if len(hypo.contradicting_evidence) > 0:
                if any("no visible wear" in c.lower() or "rotates freely" in c.lower() for c in hypo.contradicting_evidence):
                    hypo.state = HypothesisState.RULED_OUT
                    hypo.confidence_tier = ConfidenceTier.LOW_SUPPORT
                    hypo.reasoning = "Ruled out: Direct physical inspection verified component is undamaged and functioning freely."
                else:
                    hypo.state = HypothesisState.DOWNGRADED
                    hypo.confidence_tier = ConfidenceTier.LOW_SUPPORT
                    hypo.reasoning = f"Downgraded due to {len(hypo.contradicting_evidence)} contradictory findings."
            elif len(hypo.supporting_evidence) >= 2:
                hypo.state = HypothesisState.SUPPORTED
                hypo.confidence_tier = ConfidenceTier.HIGH_SUPPORT
                hypo.reasoning = f"Strongly supported by {len(hypo.supporting_evidence)} corroborating evidence items."
            elif len(hypo.supporting_evidence) == 1:
                hypo.state = HypothesisState.ACTIVE
                hypo.confidence_tier = ConfidenceTier.MODERATE_SUPPORT
                hypo.reasoning = "Active candidate with preliminary corroboration; pending definitive confirmation test."
            else:
                hypo.state = HypothesisState.ACTIVE
                hypo.confidence_tier = ConfidenceTier.LOW_SUPPORT
                hypo.reasoning = "Plausible candidate under current symptom profile; awaiting targeted physical inspection."

        # Compute Bayesian posterior probabilities across all hypotheses
        raw_scores = {}
        for h in case.hypotheses:
            prior = getattr(h, "prior_probability", 0.20) or 0.20
            likelihood = 1.0
            if h.state == HypothesisState.CONFIRMED:
                likelihood *= 15.0
            elif h.state == HypothesisState.SUPPORTED:
                likelihood *= (2.5 ** len(h.supporting_evidence))
            elif h.state == HypothesisState.ACTIVE:
                likelihood *= (1.8 if len(h.supporting_evidence) == 1 else 1.0)
            elif h.state == HypothesisState.DOWNGRADED:
                likelihood *= 0.2
            elif h.state == HypothesisState.RULED_OUT:
                likelihood *= 0.01
            raw_scores[h.hypothesis_id] = prior * likelihood

        total_raw = sum(raw_scores.values()) or 1.0
        for h in case.hypotheses:
            h.posterior_probability = round(raw_scores.get(h.hypothesis_id, 0.0) / total_raw, 2)

        # Re-rank active hypotheses
        active_hypos = [h for h in case.hypotheses if h.state != HypothesisState.RULED_OUT]
        
        def _sort_key(h: Hypothesis):
            if h.state == HypothesisState.CONFIRMED:
                state_val = 4
            elif h.state == HypothesisState.SUPPORTED:
                state_val = 3
            elif h.state == HypothesisState.ACTIVE:
                state_val = 2
            else:
                state_val = 1
            return (state_val, len(h.supporting_evidence), -len(h.contradicting_evidence))

        active_hypos.sort(key=_sort_key, reverse=True)

        if not active_hypos:
            case.current_root_cause = "INCONCLUSIVE — All candidate causes ruled out by evidence"
            case.confidence_tier = ConfidenceTier.INSUFFICIENT_EVIDENCE
            case.recommended_action = None
        elif (
            len(active_hypos) >= 2
            and active_hypos[0].state != HypothesisState.CONFIRMED
            and active_hypos[0].confidence_tier == active_hypos[1].confidence_tier == ConfidenceTier.MODERATE_SUPPORT
        ):
            case.current_root_cause = f"AMBIGUOUS — Indistinguishable between '{active_hypos[0].failure_mode}' and '{active_hypos[1].failure_mode}'"
            case.confidence_tier = ConfidenceTier.INSUFFICIENT_EVIDENCE
            case.recommended_action = None
        else:
            leading = active_hypos[0]
            if leading.state == HypothesisState.CONFIRMED:
                case.current_root_cause = f"CONFIRMED: {leading.component} - {leading.failure_mode}"
            else:
                case.current_root_cause = f"{leading.component}: {leading.failure_mode}"
            case.confidence_tier = leading.confidence_tier
            case.recommended_action = leading.recommended_action

        return case

    @classmethod
    def _generate_initial_hypotheses(cls, case: DiagnosticCase) -> List[Hypothesis]:
        subsystem = case.subsystem.lower()
        hypos: List[Hypothesis] = []

        if "door" in subsystem:
            hypos.append(
                Hypothesis(
                    hypothesis_id="HYP-DOOR-ROLLER",
                    subsystem="Door",
                    component="Skate Roller",
                    failure_mode="Roller Bearing Wear & Flat Spots",
                    state=HypothesisState.ACTIVE,
                    confidence_tier=ConfidenceTier.MODERATE_SUPPORT,
                    confirmation_test=DiagnosticTest(
                        test_id="TEST-ROLLER-01",
                        purpose="Inspect door skate roller bearing clearance and rotation",
                        procedure="Disconnect door drive belt. Manually rotate skate rollers and feel for binding, flat spots, or axial play.",
                        source_reference="elevator_door_operations.pdf p.14",
                        expected_result="Rollers spin smoothly with zero radial play and no flat spots.",
                        pass_interpretation="Skate roller mechanically sound; rules out roller bearing degradation.",
                        fail_interpretation="Bearing binding or flat spot confirmed; proceed to skate roller replacement.",
                        safety_prerequisites="Engage door disconnect switch; verify car at landing level.",
                        target_component="Skate Roller",
                    ),
                    recommended_action=CorrectiveAction(
                        action_id="ACT-DOOR-ROLLER-REPLACE",
                        title="Replace Worn Door Skate Rollers",
                        procedure="Unbolt skate assembly, replace worn rollers with OEM spec polyurethane rollers, adjust eccentric bushing to 0.5mm track clearance.",
                        source_document="elevator_door_operations.pdf",
                        page=15,
                        section="Section 4.1: Roller Replacement",
                        safety_warnings=["Verify car door drive power is isolated before loosening skate bolts."],
                        required_parts=["Door Skate Polyurethane Roller (Pair)", "Lock Washers"],
                        required_tools=["13mm open-ended wrench", "Feeler gauge set (0.1 - 1.0mm)"],
                        post_repair_validation=["Verify smooth silent door travel", "Measure door closing time (target: < 3.2s)"],
                        requires_confirmation_first=True,
                    ),
                )
            )

            hypos.append(
                Hypothesis(
                    hypothesis_id="HYP-DOOR-TRACK-BINDING",
                    subsystem="Door",
                    component="Door Track / Sill",
                    failure_mode="Mechanical Binding & Sill Debris Resistance",
                    state=HypothesisState.CANDIDATE,
                    confidence_tier=ConfidenceTier.LOW_SUPPORT,
                    confirmation_test=DiagnosticTest(
                        test_id="TEST-TRACK-01",
                        purpose="Inspect door sill groove and track for physical obstruction",
                        procedure="Inspect sill groove along entire travel length. Manually slide doors through final 100mm of closure.",
                        source_reference="elevator_door_operations.pdf p.18",
                        expected_result="Doors glide effortlessly into interlock catch without resistance (< 15 N push force).",
                        pass_interpretation="Track and sill clean and clear.",
                        fail_interpretation="Mechanical binding or debris in sill confirmed.",
                        safety_prerequisites="Stop elevator at floor level; engage inspection mode.",
                        target_component="Door Track / Sill",
                    ),
                    recommended_action=CorrectiveAction(
                        action_id="ACT-DOOR-SILL-CLEAN",
                        title="Clear and Realign Door Sill Groove",
                        procedure="Vacuum debris from landing sill grooves. Check door shoe guide clearance (nominal: 2.0mm). Apply dry silicone lubricant if specified.",
                        source_document="elevator_door_operations.pdf",
                        page=19,
                        section="Section 5.2: Sill Maintenance",
                        safety_warnings=["Do not use heavy oil or grease on door sill tracks (attracts dust)."],
                        required_parts=["Replacement Sill Guide Shoes (if worn)"],
                        required_tools=["Industrial vacuum", "Wire groove scraper", "Feeler gauge"],
                        post_repair_validation=["Cycle doors 5 times", "Confirm closing force < 150 N"],
                        requires_confirmation_first=True,
                    ),
                )
            )

            hypos.append(
                Hypothesis(
                    hypothesis_id="HYP-DOOR-INTERLOCK-MISALIGN",
                    subsystem="Door",
                    component="Door Interlock",
                    failure_mode="Interlock Contact Wear & Roller Misalignment",
                    state=HypothesisState.CANDIDATE,
                    confidence_tier=ConfidenceTier.LOW_SUPPORT,
                    confirmation_test=DiagnosticTest(
                        test_id="TEST-INTERLOCK-01",
                        purpose="Measure door lock beak engagement and contact wipe",
                        procedure="Observe interlock beak drop when doors reach fully closed position. Check contact wipe depth.",
                        source_reference="elevator_door_operations.pdf p.22",
                        expected_result="Interlock beak drops smoothly with >= 7mm contact engagement.",
                        pass_interpretation="Door interlock alignment correct.",
                        fail_interpretation="Interlock contact misaligned or worn.",
                        safety_prerequisites="Never bypass the safety chain circuit!",
                        target_component="Door Interlock",
                    ),
                    recommended_action=CorrectiveAction(
                        action_id="ACT-INTERLOCK-ADJUST",
                        title="Adjust and Clean Landing Door Interlock Contacts",
                        procedure="Clean silver contacts with approved contact cleaner. Adjust latch stop to ensure 8mm minimum engagement. Tighten mounting hardware.",
                        source_document="elevator_door_operations.pdf",
                        page=23,
                        section="Section 6.3: Interlock Adjustment",
                        safety_warnings=["Do not file safety contacts. Replace contact blocks if pitted."],
                        required_parts=["Door Interlock Contact Block Assembly"],
                        required_tools=["Metric socket set", "Torque wrench (8 Nm)", "Digital multimeter"],
                        post_repair_validation=["Verify safety chain continuity upon lock closure", "No intermittent safety circuit trips"],
                        requires_confirmation_first=True,
                    ),
                )
            )

        elif "brake" in subsystem:
            hypos.append(
                Hypothesis(
                    hypothesis_id="HYP-BRAKE-AIRGAP",
                    subsystem="Brake",
                    component="Brake Assembly",
                    failure_mode="Excessive Brake Air Gap / Microswitch Lag",
                    state=HypothesisState.ACTIVE,
                    confidence_tier=ConfidenceTier.MODERATE_SUPPORT,
                    confirmation_test=DiagnosticTest(
                        test_id="TEST-BRAKE-01",
                        purpose="Measure brake plunger air gap on both left and right shoes",
                        procedure="Insert feeler gauges around the perimeter of the brake armature while de-energized.",
                        source_reference="brake_of_gearless_traction_machine.pdf p.8",
                        expected_result="Air gap measures 0.25mm - 0.35mm uniformly.",
                        pass_interpretation="Brake air gap within OEM specification.",
                        fail_interpretation="Air gap out of tolerance; requires adjustment.",
                        safety_prerequisites="Secure elevator with car sling safety gear before adjusting machine brakes.",
                        target_component="Brake Assembly",
                    ),
                )
            )

        else:
            hypos.append(
                Hypothesis(
                    hypothesis_id="HYP-GENERIC-FAULT",
                    subsystem=case.subsystem,
                    component="Subsystem Equipment",
                    failure_mode="General Component Degradation",
                    state=HypothesisState.ACTIVE,
                    confidence_tier=ConfidenceTier.LOW_SUPPORT,
                )
            )

        return hypos
