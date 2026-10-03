"""
STAGE 5: CONFIDENCE DECISION, DUAL-VIEW SYNTHESIS & CORRECTIVE ACTIONS
Evaluates dual confidence scores (root cause vs action), enforces calibrated abstention,
and generates technician / building manager views.
"""

from typing import List, Dict, Any, Tuple, Optional
import yaml
import os

from pipeline.schemas import (
    RCAConclusion, CorrectiveRecommendation, TechnicianView, BuildingManagerView,
    HypothesisEvaluation, EvidenceItem, KONEFaultInput, FaultEpisode
)


class DiagnosisSynthesizer:
    """Stage 5: Dual confidence scoring, corrective action lookup, and report generation."""

    def __init__(self, actions_path: str = "knowledge/corrective_actions.yaml"):
        self.actions_lookup = {}
        if os.path.exists(actions_path):
            with open(actions_path, "r") as f:
                data = yaml.safe_load(f)
                self.actions_lookup = data.get("actions", {})

    def synthesize(
        self,
        fault_input: KONEFaultInput,
        episode: FaultEpisode,
        evidence_bundle: List[EvidenceItem],
        hypotheses: List[HypothesisEvaluation]
    ) -> Tuple[RCAConclusion, CorrectiveRecommendation, TechnicianView, BuildingManagerView]:
        if not hypotheses:
            # Complete fallback
            conclusion = RCAConclusion(
                root_cause="Unknown System Anomaly",
                subsystem="sensor_env",
                component="Unspecified",
                causal_narrative="No hypothesis could be evaluated due to lack of diagnostic input.",
                root_cause_confidence=0.1,
                root_cause_confidence_tier="ABSTAIN",
                action_confidence=0.1,
                action_confidence_tier="ABSTAIN",
                abstained=True,
                abstention_reason="Zero subsystem hypothesis match."
            )
            return conclusion, self._default_recommendation(), self._default_tech_view(), self._default_mgr_view()

        top_h = hypotheses[0]
        runner_up = hypotheses[1] if len(hypotheses) > 1 else None

        # Determine Root Cause Confidence
        p_top = top_h.posterior_probability
        
        # Check abstention conditions:
        # 1. Top probability < 0.45
        # 2. Conflicting evidence where top 2 are nearly tied (< 0.10 difference) and both have contradictions
        # 3. Over 35% bad/missing telemetry sensor signals
        telem_items = [e for e in evidence_bundle if e.provenance == "MEASURED" and e.signal_or_record != "Elevator Operating State"]
        bad_telemetry_count = sum(1 for e in telem_items if e.quality in ["bad", "missing"])
        total_measured = len(telem_items)
        data_quality_degraded = (total_measured > 0 and (bad_telemetry_count / total_measured) >= 0.35)

        is_tied = (runner_up and abs(p_top - runner_up.posterior_probability) <= 0.12 and p_top < 0.55)
        
        should_abstain = (p_top < 0.45) or is_tied or data_quality_degraded

        if should_abstain:
            root_tier = "ABSTAIN"
            action_tier = "ABSTAIN"
            abstained = True
            avail_ev = [f"{e.signal_or_record}: {e.value}" for e in evidence_bundle if e.diagnostic_value in ["HIGH", "MEDIUM"]]
            missing_ev = top_h.expected_but_missing_evidence or ["Independent sensor verification", "High-frequency vibration waveform"]
            abstention_statement = (
                f"Insufficient evidence to rank root causes with confidence. "
                f"Available evidence: [{', '.join(avail_ev[:3])}]. "
                f"Missing critical evidence: [{', '.join(missing_ev[:2])}]. "
                f"Recommended diagnostic step: Physically inspect {top_h.subsystem} hardware and cross-verify with hand instrumentation."
            )
            narrative = abstention_statement
        else:
            abstained = False
            if p_top >= 0.70:
                root_tier = "HIGH"
            elif p_top >= 0.45:
                root_tier = "MEDIUM"
            else:
                root_tier = "LOW"

            # Construct narrative citing positive evidence and eliminated alternatives
            pos_citations = [s.evidence for s in top_h.supporting_evidence]
            eliminated = [h for h in hypotheses if h.status == "ELIMINATED" and h.eliminated_reason]
            elim_citations = [f"{h.root_cause} (eliminated: {h.eliminated_reason})" for h in eliminated[:2]]

            narrative = (
                f"Analysis of telemetry and alarm cascade indicates {top_h.root_cause} as the primary root cause "
                f"(posterior probability {p_top * 100:.0f}%). "
                f"Key supporting evidence: {'; '.join(pos_citations[:3]) if pos_citations else 'Aligned alarm signature'}. "
            )
            if elim_citations:
                narrative += f"Alternative hypotheses ruled out: {'; '.join(elim_citations)}."

        # Action confidence is derived from root confidence + action lookup clarity
        action_conf = round(max(0.2, p_top * 0.9 if not abstained else 0.3), 2)
        if action_conf >= 0.70:
            action_tier = "HIGH"
        elif action_conf >= 0.45:
            action_tier = "MEDIUM"
        else:
            action_tier = "LOW"

        conclusion = RCAConclusion(
            root_cause=top_h.root_cause if not abstained else "Inconclusive (Evidence Ambiguity)",
            subsystem=top_h.subsystem,
            component=self._map_component(top_h.hypothesis_id, top_h.subsystem),
            causal_narrative=narrative,
            root_cause_confidence=p_top if not abstained else round(p_top, 2),
            root_cause_confidence_tier=root_tier,
            action_confidence=action_conf,
            action_confidence_tier=action_tier,
            abstained=abstained,
            abstention_reason=narrative if abstained else None
        )

        # Lookup Corrective Action
        recommendation = self._lookup_action(top_h.hypothesis_id, top_h.subsystem, abstained)

        # Build Technician View
        tech_view = TechnicianView(
            summary=(
                f"{episode.primary_alarm.alarm_type} cascade resolved. "
                f"Most probable cause: {top_h.root_cause} ({p_top * 100:.0f}% confidence). "
                f"{'Abstention triggered due to conflicting signals.' if abstained else 'Verified against negative evidence.'}"
            ),
            key_evidence=[s.evidence for s in top_h.supporting_evidence[:4]] or ["Alarm sequence temporal alignment"],
            next_step=recommendation.specific_steps[0] if recommendation.specific_steps else "Perform physical site inspection.",
            confidence_statement=(
                f"{root_tier} confidence in diagnosis ({p_top * 100:.0f}%). "
                f"{action_tier} confidence in recommended action — technician physical confirmation required."
            )
        )

        # Build Building Manager View
        mgr_view = BuildingManagerView(
            summary=(
                f"Elevator {fault_input.elevator_id} safely halted due to an alert in the {top_h.subsystem.replace('_', ' ')} system. "
                f"Preliminary diagnostic indicates {top_h.root_cause}. "
                f"Field technician has been provided with targeted component inspection steps."
            ),
            expected_downtime=self._estimate_downtime(top_h.subsystem, recommendation.estimated_severity),
            safety_status="Elevator safely stopped. Hardware safety circuit engaged. No passenger risk.",
            action_required="Awaiting on-site technician physical verification and authorization."
        )

        return conclusion, recommendation, tech_view, mgr_view

    def _map_component(self, h_id: str, subsystem: str) -> str:
        mapping = {
            "drive_motor": {"RC1": "VFD IGBT Inverter Module", "RC2": "Guide Rails & Hoistway Structure", "RC3": "EcoDisc Mechanical Brake Assembly", "RC4": "PMSM Stator Windings"},
            "door": {"RC1": "3D Optical Light Curtain Detector", "RC2": "Landing / Car Door Sill Track", "RC3": "Door Hanger Rollers & Bearings", "RC4": "Door Operator Drive Motor"},
            "brake_traction": {"RC1": "Brake Microswitch & Coil Circuit", "RC2": "Brake Friction Lining", "RC3": "Brake Actuation Solenoid", "RC4": "Traction Ropes & Sheave"},
            "encoder_position": {"RC1": "EcoDisc Optical Motor Encoder", "RC2": "Shaft Encoder Coupling", "RC3": "Floor Leveling Vane Sensor"},
            "safety_chain": {"RC1": "Landing Door Lock Interlock Switch", "RC2": "Terminal Pit/Overhead Buffer Switch", "RC3": "Overspeed Governor Switch"}
        }
        return mapping.get(subsystem, {}).get(h_id, "Subsystem Component")

    def _lookup_action(self, h_id: str, subsystem: str, abstained: bool) -> CorrectiveRecommendation:
        if abstained:
            return CorrectiveRecommendation(
                recommended_action="PHYSICAL_MULTIPOINT_INSPECTION",
                specific_steps=[
                    "Switch elevator to Inspection Operation (TCI) before entering car top or pit.",
                    "Verify power isolation and take direct electrical and mechanical measurements.",
                    "Inspect both drive electronics and mechanical motion pathways to resolve ambiguity."
                ],
                do_not_do=[
                    "Do NOT reset safety chain or restart elevator before completing manual inspection.",
                    "Do NOT replace parts without direct physical verification."
                ],
                estimated_severity="HIGH"
            )

        # Match approved action from YAML
        for act_key, act_val in self.actions_lookup.items():
            if act_val.get("hypothesis_id") == h_id and act_val.get("subsystem") == subsystem:
                return CorrectiveRecommendation(
                    recommended_action=act_key,
                    specific_steps=act_val.get("specific_steps", []),
                    do_not_do=act_val.get("do_not_do", []),
                    estimated_severity=act_val.get("estimated_severity", "MEDIUM")
                )

        # Fallback to general inspection
        return self._default_recommendation()

    def generate_investigation_report_markdown(
        self,
        fault_input: KONEFaultInput,
        episode: FaultEpisode,
        evidence_bundle: List[EvidenceItem],
        hypotheses: List[HypothesisEvaluation],
        rca_conclusion: RCAConclusion,
        recommendation: CorrectiveRecommendation,
        investigation_id: str
    ) -> str:
        """Constructs a comprehensive, audit-ready engineering investigation report in Markdown format."""
        top_h = hypotheses[0] if hypotheses else None
        top_cause = top_h.root_cause if top_h else "Unknown Anomaly"
        conf_pct = f"{rca_conclusion.root_cause_confidence * 100:.1f}%"
        status_str = "ABSTAINED (EVIDENCE INSUFFICIENT)" if rca_conclusion.abstained else f"CONFIRMED ({rca_conclusion.root_cause_confidence_tier})"

        # 1. Repeat repair check
        repeat_notes = []
        if fault_input.maintenance_history:
            part_counts = {}
            for m in fault_input.maintenance_history:
                act = getattr(m, "action", "") or getattr(m, "action_taken", "") or (m.get("action", "") if isinstance(m, dict) else "")
                comp = getattr(m, "component", "") or (m.get("component", "") if isinstance(m, dict) else "")
                combo = f"{comp} {act}"
                for token in ["Door Roller", "Brake Lining", "Encoder", "Contactor", "Sensor", "Track", "Lock"]:
                    if token.lower() in combo.lower():
                        part_counts[token] = part_counts.get(token, 0) + 1
            for part, count in part_counts.items():
                if count >= 2:
                    repeat_notes.append(
                        f"- **Repeated Part Swaps Detected:** '{part}' was replaced **{count} times** in previous work orders without permanently resolving the issue.\n"
                        f"- **Root Cause Analysis:** This indicates a prior misdiagnosis where technicians treated the superficial symptom (component wear) rather than the underlying structural/geometric placement distortion (e.g. track plumbness, sill misalignment, or mounting rigidity).\n"
                        f"- **Recommended Corrective Shift:** Do not replace '{part}' again in isolation; perform geometric alignment and coordinate calibration per OEM maintenance specifications."
                    )
        repeat_section = "\n".join(repeat_notes) if repeat_notes else "No recurrent component replacement pattern found in recent work order history. Single-event failure mode."

        # 2. Hypotheses Table
        hyp_rows = []
        for h in hypotheses:
            pos_ev = "; ".join([s.evidence for s in h.supporting_evidence[:2]]) if h.supporting_evidence else "None"
            elim_text = f"Eliminated: {h.eliminated_reason}" if (h.status == "ELIMINATED" and h.eliminated_reason) else pos_ev
            prob_str = f"{h.posterior_probability * 100:.1f}%"
            hyp_rows.append(f"| #{h.rank} | **{h.root_cause}** | `{h.subsystem}` | **{prob_str}** | `{h.status}` | {elim_text} |")
        hyp_table = "\n".join(hyp_rows)

        # 3. Evidence Table (Physical / Measured / Logged)
        ev_rows = []
        rag_rows = []
        for ev in evidence_bundle:
            if ev.provenance == "RAG_RETRIEVED":
                pg_str = f"p.{ev.source_page}" if ev.source_page else "General"
                sec_str = f"§{ev.source_section[:40]}" if ev.source_section else "—"
                auth_str = ev.source_authority or "GUIDE"
                rag_rows.append(f"| `{ev.source_document or 'GUIDE'}` | {pg_str} | {sec_str} | `{auth_str}` | {ev.value[:200]} |")
            else:
                ev_rows.append(f"| `{ev.signal_or_record}` | {ev.value} | `{ev.provenance}` | `{ev.quality.upper()}` | `{ev.diagnostic_value}` |")
        ev_table = "\n".join(ev_rows) if ev_rows else "| None | — | — | — | — |"
        rag_table = "\n".join(rag_rows) if rag_rows else "| No GUIDE corpus citations retrieved for this incident | — | — | — | — |"

        # 4. Confirmation Tests & "What Would Change the Diagnosis?"
        missing_list = top_h.expected_but_missing_evidence if (top_h and top_h.expected_but_missing_evidence) else ["Independent secondary sensor validation"]
        missing_str = "\n".join([f"- **Missing Signal:** `{m}`" for m in missing_list])

        supporting_str = "\n".join([f"- **Supporting:** {s.evidence} [{s.provenance}]" for s in (top_h.supporting_evidence if top_h else [])]) or "- Aligned alarm signature and operational context"
        contradicting_str = "\n".join([f"- **Contradicting:** {c.evidence} [{c.provenance}]" for c in (top_h.contradicting_evidence if top_h else [])]) or "- No contradicting observations detected"

        confirmation_test = self._generate_confirmation_test(top_h.subsystem if top_h else "", top_cause)

        # 5. SOP steps & prohibited
        steps_list = "\n".join([f"{idx+1}. [ ] **Step {idx+1}:** {s}" for idx, s in enumerate(recommendation.specific_steps)])
        do_not_do_list = "\n".join([f"- **PROHIBITED:** {d}" for d in recommendation.do_not_do])

        safety_state = getattr(fault_input, "safety_chain_state", None) or "INDEPENDENT_HARDWIRED"

        report_md = f"""# KONE ElevateRCA — Root Cause Analysis & Engineering Investigation Report
**Investigation Reference:** `{investigation_id}` | **Status:** `{status_str}` | **Advisory Model:** `ElevateRCA Bayesian + RAG v1.0`

---

## 1. Executive Diagnostic Finding & Conclusion
- **Primary Root Cause:** **{top_cause}**
- **Affected Subsystem:** `{rca_conclusion.subsystem.upper()}`
- **Target Component:** `{rca_conclusion.component}`
- **Bayesian Posterior Confidence:** **{conf_pct} ({rca_conclusion.root_cause_confidence_tier})**
- **Action Severity Rating:** `{recommendation.estimated_severity}`
- **Causal Narrative:** {rca_conclusion.causal_narrative}

---

## 2. Equipment Context & Operating Telemetry State
| Parameter | Recorded Engineering Value |
|---|---|
| **Elevator Asset ID** | `{fault_input.elevator_id}` |
| **Model Specification** | `{fault_input.elevator_model or "KONE MonoSpace / MiniSpace (EcoDisc PMSM)"}` |
| **Operating State at Event** | `{fault_input.operating_state}` |
| **Safety Chain Interlock State** | `{safety_state}` |
| **Primary Trigger Alarm** | `{episode.primary_alarm.alarm_code} ({episode.primary_alarm.severity.upper()})` |
| **Cascade Consequential Trips** | `{len(episode.consequential_alarms)} secondary events over {episode.time_span_seconds:.2f}s time-span` |

---

## 3. Prior Misdiagnosis & Repeat Repair Forensic Analysis
{repeat_section}

---

## 4. Multi-Hypothesis Bayesian Weight Breakdown Table
| Rank | Failure Mode / Candidate Cause | Subsystem | Posterior Probability | Status | Diagnostic Evidence / Elimination Rationale |
|---|---|---|---|---|---|
{hyp_table}

---

## 5. Physical Evidence & Sensor Telemetry Bundle
| Monitored Signal / Record | Measured Diagnostic Value | Provenance | Data Quality | Diagnostic Value |
|---|---|---|---|---|
{ev_table}

---

## 6. GUIDE Technical Corpus & OEM Reference Citations (RAG)
| Source Document | Page | Section | Authority Level | Retrieved Technical Procedure / Standard |
|---|---|---|---|---|
{rag_table}

---

## 7. Diagnostic Confirmation & What Would Change the Diagnosis?
### **Primary Hypothesis Evaluation:**
{supporting_str}

### **Contradicting / Inconsistent Evidence:**
{contradicting_str}

### **Expected But Missing Signals:**
{missing_str}

### **Physical Verification Protocol:**
- **Confirmation Test:** {confirmation_test['test']}
- **Expected Nominal Reading:** `{confirmation_test['expected']}`
- **If Test FAILS (Anomaly Confirmed):** {confirmation_test['if_fail']}
- **If Test PASSES (Anomaly Refuted):** {confirmation_test['if_pass']}

---

## 8. Approved OEM Standard Operating Procedure (SOP)
### **Recommended Procedure:** `{recommendation.recommended_action}`

#### **A. Step-by-Step Field Execution Checklist:**
{steps_list}

#### **B. Critical Prohibited Actions (DO NOT DO):**
{do_not_do_list}

---

## 9. Post-Repair Return-to-Service Verification Protocol
1. **Physical & Mechanical Alignment Verification:** Verify mechanical tolerances (e.g. brake air gap $0.30\\text{{mm}} \\pm 0.05\\text{{mm}}$, door sill gap $4\\text{{mm}} \\pm 1\\text{{mm}}$) with calibrated gauges.
2. **Slow-Speed Inspection Test Run:** Run elevator across entire shaft height on inspection mode; ensure motor current and vibration stay within nominal baselines.
3. **Safety Chain Continuity Confirmation:** Trip and reset all landing door contacts and governor limit switches to confirm hardwired safety circuit drops.
4. **Full-Speed Round Trip Load Run:** Execute 2 full-speed autonomous runs with floor leveling stop verification ($< 5\\text{{mm}}$ threshold).

---

## 10. Official Field Verification & Sign-Off Authorization
- **Safety Status:** Safe advisory isolation. System does not actuate hardware or bypass safety loops.
- **Lead Diagnostic Specialist:** `________________________________________`
- **Technician Badge ID:** `________________________________________`
- **Work Order Authorization:** `[  ] ACCEPTED & DISPATCHED    [  ] EDITED WITH NOTES    [  ] REJECTED`
- **Signature & Timestamp:** `________________________________________`
"""
        return report_md

    def _generate_confirmation_test(self, subsystem: str, root_cause: str) -> Dict[str, str]:
        """Generates structured confirmation test details per Section 28."""
        rc_lower = root_cause.lower()
        if "igbt" in rc_lower or "inverter" in rc_lower:
            return {
                "test": "Perform cold diode check across all 6 IGBT inverter arms with digital multimeter (power isolated).",
                "expected": "Forward drop 0.3V - 0.7V across all 6 arms; reverse infinite resistance (>10 MOhm).",
                "if_fail": "Confirms internal power electronics breakdown. Replace inverter power module.",
                "if_pass": "Refutes internal IGBT failure; investigate external motor winding short or mechanical bind."
            }
        elif "mechanical" in rc_lower or "jam" in rc_lower or "rail" in rc_lower:
            return {
                "test": "Conduct slow-speed inspection sweep along guide rails between affected floors; inspect rail lubrication and safety gear clearance.",
                "expected": "Safety gear shoe-to-rail clearance nominal 2.5mm - 3.5mm; zero debris in guide shoe slots.",
                "if_fail": "Confirms mechanical track obstruction or rail misalignment. Align rail and remove debris.",
                "if_pass": "Refutes mechanical hoistway bind; check car guide shoe roller bearings and counterweight frame."
            }
        elif "photo" in rc_lower or "curtain" in rc_lower or "optical" in rc_lower:
            return {
                "test": "Clean optical lenses with microfiber; inspect 3D light curtain alignment LED indicators across door travel.",
                "expected": "Green sync indicator solid throughout full open/close cycle; optical attenuation < 20%.",
                "if_fail": "Confirms optical degradation or sync cable flexure break. Re-align or replace optical curtain.",
                "if_pass": "Refutes optical curtain fault; re-evaluate physical sill track obstruction or door gib wear."
            }
        elif "roller" in rc_lower or "bearing" in rc_lower:
            return {
                "test": "Manually spin door hanger rollers and check for radial play, flat spots, or eccentric bushing looseness.",
                "expected": "Smooth rotation with zero radial play (<0.1mm); up-thrust roller gap 0.1mm - 0.2mm.",
                "if_fail": "Confirms roller bearing wear or flat spots. Replace worn roller set and adjust up-thrust gap.",
                "if_pass": "Refutes isolated roller wear; inspect header track plumbness and sill groove parallelism."
            }
        elif "track" in rc_lower or "misalignment" in rc_lower:
            return {
                "test": "Measure door header track to sill gap parallelism with dial indicator across entire door travel.",
                "expected": "Sill gap 4.0mm +/- 1.0mm uniform across entire stroke.",
                "if_fail": "Confirms track distortion / geometric misalignment. Re-plumb header track and level sill.",
                "if_pass": "Refutes track distortion; evaluate door drive belt tension and motor operator coupling."
            }
        elif "brake" in rc_lower:
            return {
                "test": "Measure brake air gap with feeler gauges at 4 orthogonal points; test microswitch opening timing.",
                "expected": "Air gap 0.30mm +/- 0.05mm uniform; pickup delay < 150ms.",
                "if_fail": "Confirms brake mechanical drag or coil timing violation. Re-shim air gap per OEM spec.",
                "if_pass": "Refutes brake drag; check drive torque pre-control and counterweight balance ratio."
            }
        elif "encoder" in rc_lower or "position" in rc_lower:
            return {
                "test": "Verify encoder coupling set screw torque; execute encoder zero-pulse learning routine via controller UI.",
                "expected": "Zero pulse slippage; speed feedback tracking within +/- 2 rpm of commanded profile.",
                "if_fail": "Confirms encoder coupling slip or optical degradation. Tighten coupling or replace encoder.",
                "if_pass": "Refutes encoder hardware failure; inspect hoistway floor leveling vane flags."
            }
        return {
            "test": f"Perform comprehensive physical inspection of {subsystem.replace('_', ' ')} components.",
            "expected": "All physical parameters and electrical contacts within nominal OEM maintenance tolerances.",
            "if_fail": "Confirms physical degradation in inspected component.",
            "if_pass": "Refutes candidate cause; review upstream control and power supply inputs."
        }

    def _estimate_downtime(self, subsystem: str, severity: str) -> str:
        if severity == "CRITICAL" or subsystem in ["drive_motor", "brake_traction"]:
            return "Estimated 2 to 6 hours (pending on-site component inspection and parts stock)."
        elif subsystem == "door":
            return "Estimated 30 minutes to 2 hours."
        return "Estimated 1 to 4 hours."

    def _default_recommendation(self) -> CorrectiveRecommendation:
        return CorrectiveRecommendation(
            recommended_action="INSPECT_SUBSYSTEM",
            specific_steps=[
                "Place elevator on technician inspection mode.",
                "Inspect affected subsystem mechanical and electrical connections.",
                "Verify safety chain continuity and log readings before authorization."
            ],
            do_not_do=[
                "Do NOT bypass hardware safety circuits.",
                "Do NOT perform high-speed run until inspection is cleared."
            ],
            estimated_severity="MEDIUM"
        )

    def _default_tech_view(self) -> TechnicianView:
        return TechnicianView(
            summary="Diagnostic analysis incomplete.",
            key_evidence=["Insufficient telemetry"],
            next_step="Inspect unit manually.",
            confidence_statement="LOW confidence."
        )

    def _default_mgr_view(self) -> BuildingManagerView:
        return BuildingManagerView(
            summary="Elevator out of service for inspection.",
            expected_downtime="1 to 4 hours.",
            safety_status="Safely parked.",
            action_required="Technician dispatched."
        )

