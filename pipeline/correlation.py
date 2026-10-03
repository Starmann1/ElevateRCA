"""
STAGE 2: ALARM CASCADE CORRELATION
Temporal grouping (15s window) and causal chain reconstruction based on physical mechanisms.
"""

from typing import List, Dict, Any, Tuple
from datetime import datetime, timezone
import yaml
import os

from pipeline.schemas import AlarmInput, FaultEpisode, PrimaryAlarm, ConsequentialAlarm


class AlarmCorrelator:
    """Stage 2: Correlates cascading alarm floods into a single fault episode."""

    def __init__(self, causal_links_path: str = "knowledge/causal_links.yaml"):
        self.causal_rules = []
        self.window_seconds = 15.0
        if os.path.exists(causal_links_path):
            with open(causal_links_path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
                self.causal_rules = data.get("cascade_rules", [])
                self.window_seconds = data.get("temporal_clustering_window_seconds", 15.0)

    def _parse_ts(self, ts_str: str) -> float:
        try:
            # Handle ISO string with or without Z
            clean_ts = ts_str.replace("Z", "+00:00")
            dt = datetime.fromisoformat(clean_ts)
            return dt.timestamp()
        except Exception:
            return 0.0

    def correlate_alarms(self, alarms: List[AlarmInput]) -> FaultEpisode:
        if not alarms:
            # Default empty / fallback episode
            return FaultEpisode(
                primary_alarm=PrimaryAlarm(
                    alarm_code="NONE",
                    alarm_type="unknown",
                    subsystem="sensor_env",
                    timestamp=datetime.now(timezone.utc).isoformat(),
                    severity="informational"
                ),
                consequential_alarms=[],
                time_span_seconds=0.0,
                episode_classification="No alarms reported; telemetry-only evaluation"
            )

        # Sort alarms chronologically
        sorted_alarms = sorted(alarms, key=lambda a: self._parse_ts(a.timestamp))
        earliest_ts = self._parse_ts(sorted_alarms[0].timestamp)
        latest_ts = self._parse_ts(sorted_alarms[-1].timestamp)
        time_span = max(0.0, latest_ts - earliest_ts)

        # Primary candidate starts as the chronologically earliest alarm
        primary_candidate = sorted_alarms[0]
        consequential_list: List[ConsequentialAlarm] = []

        # Find consequential alarms based on causal rules from the earliest matching trigger
        consequential_codes_found = set()
        
        # Check if an earlier alarm causes subsequent alarms
        for a_idx, a_curr in enumerate(sorted_alarms):
            for rule in self.causal_rules:
                trigger = rule.get("trigger_alarm")
                if a_curr.alarm_type == trigger or a_curr.alarm_code == trigger:
                    # If this is the earliest trigger found or primary_candidate wasn't a trigger, keep as primary
                    if a_idx == 0 or (primary_candidate.alarm_type not in [r.get("trigger_alarm") for r in self.causal_rules]):
                        if a_idx == 0:
                            primary_candidate = a_curr
                    for c_rule in rule.get("consequential_alarms", []):
                        c_code = c_rule.get("alarm_code")
                        rel = c_rule.get("relationship")
                        for a_sub in sorted_alarms:
                            if a_sub != primary_candidate and (a_sub.alarm_type == c_code or a_sub.alarm_code == c_code):
                                if a_sub.alarm_code not in consequential_codes_found:
                                    consequential_list.append(ConsequentialAlarm(
                                        alarm_code=a_sub.alarm_code,
                                        alarm_type=a_sub.alarm_type,
                                        causal_relationship=rel
                                    ))
                                    consequential_codes_found.add(a_sub.alarm_code)

        # Any other alarms in the cluster that weren't matched as primary or explicit rule
        for a in sorted_alarms:
            if a != primary_candidate and a.alarm_code not in consequential_codes_found:
                consequential_list.append(ConsequentialAlarm(
                    alarm_code=a.alarm_code,
                    alarm_type=a.alarm_type,
                    causal_relationship=f"Correlated within {self.window_seconds}s temporal fault window"
                ))
                consequential_codes_found.add(a.alarm_code)

        classification_str = (
            f"Single-origin cascade: 1 primary root cause ('{primary_candidate.alarm_code}'), "
            f"{len(consequential_list)} consequential alarm(s) within {time_span:.1f}s"
            if consequential_list else
            f"Isolated single alarm episode ('{primary_candidate.alarm_code}')"
        )

        return FaultEpisode(
            primary_alarm=PrimaryAlarm(
                alarm_code=primary_candidate.alarm_code,
                alarm_type=primary_candidate.alarm_type,
                subsystem=primary_candidate.subsystem,
                timestamp=primary_candidate.timestamp,
                severity=primary_candidate.severity
            ),
            consequential_alarms=consequential_list,
            time_span_seconds=round(time_span, 2),
            episode_classification=classification_str
        )
