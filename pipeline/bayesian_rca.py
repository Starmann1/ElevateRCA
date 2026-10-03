"""
STAGE 4: FAULT TREE TRAVERSAL & BAYESIAN RANKING
Applies the 4-step Q1-Q4 discipline, evaluates negative evidence states (TRUE_NEGATIVE, MISSING_DATA),
incorporates EWMA & CUSUM statistical drift signals,
and computes Bayesian posterior probabilities across 6-9 competing hypotheses.
"""

from typing import List, Dict, Any, Tuple, Optional
import yaml
import os

from pipeline.schemas import (
    HypothesisEvaluation, SupportingEvidence, ContradictingEvidence,
    KONEFaultInput, FaultEpisode
)


class BayesianRCAEngine:
    """Stage 4: Traverses subsystem fault trees and performs Bayesian ranking."""

    def __init__(self, failure_modes_path: str = "knowledge/failure_modes.yaml"):
        self.subsystems_kb = {}
        if os.path.exists(failure_modes_path):
            with open(failure_modes_path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
                self.subsystems_kb = data.get("subsystems", {})

    def evaluate_subsystem(
        self,
        fault_input: KONEFaultInput,
        episode: FaultEpisode,
        triaged_signals: List[Dict[str, Any]]
    ) -> List[HypothesisEvaluation]:
        # 4a: Identify Subsystem
        subsystem_key = episode.primary_alarm.subsystem
        if subsystem_key not in self.subsystems_kb:
            subsystem_key = "drive_motor"  # Default fallback

        subsystem_data = self.subsystems_kb.get(subsystem_key, {})
        hypotheses_defs = subsystem_data.get("hypotheses", [])

        # Build signal lookup map for fast query
        signal_map = {s["signal_name"]: s for s in triaged_signals}
        
        # Check for simulated discrete state flags (e.g. drive_self_test, independent_leveling_sensor)
        discrete_flags: Dict[str, Any] = {}
        for s in triaged_signals:
            discrete_flags[s["signal_name"]] = s["value"]

        # Parse text notes for flags like "drive self-test failed"
        all_text = (fault_input.technician_free_text or "").lower()
        if "drive self-test failed" in all_text or "drive self test failed" in all_text or "drive internal fault" in all_text:
            discrete_flags["drive_self_test"] = "FAILED"
            discrete_flags["drive_internal_fault_flag"] = "TRUE"
        elif "drive self-test passed" in all_text or "drive healthy" in all_text:
            discrete_flags["drive_self_test"] = "PASSED"
            discrete_flags["drive_internal_fault_flag"] = "FALSE"

        if "consistent location" in all_text:
            discrete_flags["reopen_location_consistent"] = "TRUE"
        elif "random location" in all_text or "varying location" in all_text or "inconsistent location" in all_text or "varying door" in all_text:
            discrete_flags["reopen_location_consistent"] = "FALSE"

        if "photo-eye" in all_text or "photoeye" in all_text or "curtain" in all_text:
            if "erratic" in all_text or "drift" in all_text or "intermittent" in all_text:
                discrete_flags["photoeye_state_erratic"] = "TRUE"

        if "independent" in all_text:
            if "correct" in all_text or "exact" in all_text or "not corroborate" in all_text or "normal" in all_text:
                discrete_flags["independent_leveling_sensor_drift"] = "FALSE"
            elif "also drift" in all_text or "also showed drift" in all_text:
                discrete_flags["independent_leveling_sensor_drift"] = "TRUE"

        # Check Maintenance History for Repeat Repair / Prior Misdiagnosis Patterns
        repeat_replaced_components: Dict[str, int] = {}
        if fault_input.maintenance_history:
            for rec in fault_input.maintenance_history:
                if rec.part_replaced or "replaced" in rec.action.lower():
                    comp_norm = rec.component.lower()
                    repeat_replaced_components[comp_norm] = repeat_replaced_components.get(comp_norm, 0) + 1

        raw_scores: Dict[str, float] = {}
        evaluations: List[Dict[str, Any]] = []

        for h_def in hypotheses_defs:
            h_id = h_def["id"]
            h_name = h_def["name"]
            prior = h_def.get("prior", 0.15)
            
            supporting: List[SupportingEvidence] = []
            contradicting: List[ContradictingEvidence] = []
            missing: List[str] = []
            eliminated_reason: Optional[str] = None
            
            likelihood_factor = 1.0

            # Check for Repeat Repair / Misdiagnosis Prior Boost
            repeat_target = h_def.get("repeat_repair_component")
            if repeat_target:
                for c_name, count in repeat_replaced_components.items():
                    if repeat_target.lower() in c_name and count >= 2:
                        supporting.append(SupportingEvidence(
                            evidence=f"Repeat repair pattern detected: '{repeat_target}' replaced {count} times in service history without resolving issue (indicates underlying geometric alignment/placement fault rather than component wear)",
                            provenance="HISTORICAL",
                            strength="STRONG"
                        ))
                        likelihood_factor *= 3.5

            # Q1-Q4 Evaluation across expected signals
            expected_signals = h_def.get("expected_signals", {})
            for sig_name, condition in expected_signals.items():
                if sig_name in signal_map:
                    sig_info = signal_map[sig_name]
                    # Quality gate: if bad/missing -> MISSING_DATA state
                    if sig_info["quality"] in ["bad", "missing"]:
                        missing.append(f"{sig_name} quality is '{sig_info['quality']}' (zero diagnostic value)")
                        continue

                    exp_anomaly = condition.get("anomaly")
                    actual_anomaly = sig_info["classification"]

                    # Harmonize positive match conditions (e.g. DRIFT, ELEVATED, SEVERELY_ELEVATED)
                    is_pos_match = False
                    if exp_anomaly == actual_anomaly:
                        is_pos_match = True
                    elif exp_anomaly in ["ELEVATED", "DRIFT"] and actual_anomaly in ["ELEVATED", "SEVERELY_ELEVATED", "DRIFT"]:
                        is_pos_match = True
                    elif exp_anomaly == "SEVERELY_ELEVATED" and actual_anomaly in ["SEVERELY_ELEVATED", "SPIKE"]:
                        is_pos_match = True

                    if is_pos_match:
                        # Positive evidence match!
                        det_method = sig_info.get("detection_method", "THRESHOLD")
                        extra_stat = ""
                        if sig_info.get("cusum_drift"):
                            extra_stat = f" [CUSUM persistent drift: {sig_info.get('cusum_direction')} (S_H={sig_info.get('cusum_s_high')})]"
                        elif sig_info.get("ewma_z_score", 0) >= 2.0:
                            extra_stat = f" [EWMA z-score={sig_info.get('ewma_z_score')}]"

                        supporting.append(SupportingEvidence(
                            evidence=f"{sig_name} = {sig_info['value']} {sig_info.get('unit', '')} ({sig_info.get('deviation_pct', 0):+}% vs baseline) [{actual_anomaly}]{extra_stat}",
                            provenance="MEASURED",
                            strength="STRONG" if actual_anomaly == "SEVERELY_ELEVATED" or sig_info.get("cusum_drift") else "MODERATE"
                        ))
                        likelihood_factor *= (3.5 if actual_anomaly == "SEVERELY_ELEVATED" else 2.2)
                    elif exp_anomaly == "NORMAL" and actual_anomaly == "NORMAL":
                        # Expected normal is positive confirmation
                        supporting.append(SupportingEvidence(
                            evidence=f"{sig_name} is NORMAL as expected ({sig_info['value']} {sig_info.get('unit', '')})",
                            provenance="MEASURED",
                            strength="MODERATE"
                        ))
                        likelihood_factor *= 1.4
                    elif actual_anomaly == "NORMAL" and exp_anomaly in ["ELEVATED", "SEVERELY_ELEVATED", "SPIKE"]:
                        # TRUE_NEGATIVE: Expected high, but measured normal!
                        contradicting.append(ContradictingEvidence(
                            evidence=f"{sig_name} is NORMAL ({sig_info['value']} {sig_info.get('unit', '')}) when {exp_anomaly} was expected",
                            provenance="MEASURED",
                            strength="STRONG"
                        ))
                        likelihood_factor *= 0.25
                elif sig_name in discrete_flags:
                    val = str(discrete_flags[sig_name]).upper()
                    exp_val = str(condition.get("state", "")).upper()
                    if exp_val and val == exp_val:
                        supporting.append(SupportingEvidence(
                            evidence=f"{sig_name} state is {val}",
                            provenance="LOGGED",
                            strength="STRONG"
                        ))
                        likelihood_factor *= 3.0
                    elif exp_val and val != exp_val:
                        contradicting.append(ContradictingEvidence(
                            evidence=f"{sig_name} is {val} (expected {exp_val})",
                            provenance="LOGGED",
                            strength="STRONG"
                        ))
                        likelihood_factor *= 0.1
                else:
                    # UNOBSERVED / MISSING
                    missing.append(f"{sig_name} not available in provided telemetry")

            # Check explicit contradictions
            for contradiction_rule in h_def.get("contradictions", []):
                # E.g. "drive_self_test == PASSED"
                if "drive_self_test == PASSED" in contradiction_rule and discrete_flags.get("drive_self_test") == "PASSED":
                    contradicting.append(ContradictingEvidence(
                        evidence="Drive self-test PASSED (indicates drive internal health)",
                        provenance="LOGGED",
                        strength="STRONG"
                    ))
                    likelihood_factor *= 0.05
                    eliminated_reason = h_def.get("elimination_rule", "Contradicted by clean drive self-test.")
                elif "drive_self_test == FAILED" in contradiction_rule and discrete_flags.get("drive_self_test") == "FAILED":
                    contradicting.append(ContradictingEvidence(
                        evidence="Drive self-test FAILED (indicates drive-internal electrical fault, not external)",
                        provenance="LOGGED",
                        strength="STRONG"
                    ))
                    likelihood_factor *= 0.05
                    eliminated_reason = h_def.get("elimination_rule", "Drive self-test failure contradicts external cause.")
                elif "operating_state == DOOR_OPEN" in contradiction_rule and fault_input.operating_state == "DOOR_OPEN":
                    contradicting.append(ContradictingEvidence(
                        evidence="Fault occurred during DOOR_OPEN state (incompatible with travel-only obstruction)",
                        provenance="MEASURED",
                        strength="STRONG"
                    ))
                    likelihood_factor *= 0.1
                    eliminated_reason = "Fault occurred when stationary with doors open."
                elif "reopen_location_consistent == FALSE" in contradiction_rule and discrete_flags.get("reopen_location_consistent") == "FALSE":
                    contradicting.append(ContradictingEvidence(
                        evidence="Reopen location is inconsistent/varying across door cycles",
                        provenance="MEASURED",
                        strength="STRONG"
                    ))
                    likelihood_factor *= 0.15
                    eliminated_reason = "Varying reopen location refutes fixed physical obstruction."

            # Calculate raw Bayesian posterior weight
            posterior_raw = prior * likelihood_factor
            raw_scores[h_id] = posterior_raw

            evaluations.append({
                "hypothesis_id": h_id,
                "root_cause": h_name,
                "subsystem": subsystem_key,
                "raw_posterior": posterior_raw,
                "supporting": supporting,
                "contradicting": contradicting,
                "eliminated_reason": eliminated_reason,
                "missing": missing
            })

        # Bayesian Normalization (sum to 1.0)
        total_raw = sum(raw_scores.values()) if sum(raw_scores.values()) > 0 else 1.0
        
        results: List[HypothesisEvaluation] = []
        # Sort by raw posterior descending
        sorted_evals = sorted(evaluations, key=lambda x: x["raw_posterior"], reverse=True)

        for rank_idx, item in enumerate(sorted_evals, 1):
            normalized_prob = item["raw_posterior"] / total_raw
            status = "ACTIVE"
            if item["eliminated_reason"] or normalized_prob < 0.08:
                status = "ELIMINATED" if (item["eliminated_reason"] or len(item["contradicting"]) > 0) else "WEAKLY_SUPPORTED"
            elif normalized_prob < 0.20:
                status = "WEAKLY_SUPPORTED"

            results.append(HypothesisEvaluation(
                rank=rank_idx,
                hypothesis_id=item["hypothesis_id"],
                root_cause=item["root_cause"],
                subsystem=item["subsystem"],
                posterior_probability=round(normalized_prob, 2),
                status=status,
                supporting_evidence=item["supporting"],
                contradicting_evidence=item["contradicting"],
                eliminated_reason=item["eliminated_reason"],
                expected_but_missing_evidence=item["missing"]
            ))

        return results
