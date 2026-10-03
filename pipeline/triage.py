"""
STAGE 1: SIGNAL TRIAGE & ANOMALY DETECTION
Implements EWMA / CUSUM anomaly detection, state-aware baseline deviations,
and signal quality gating for autonomous elevator fault isolation and root-cause analysis.
"""

from typing import List, Dict, Any, Optional, Union
import numpy as np
from pipeline.schemas import TelemetryInput


# Standard engineering norms for KONE MonoSpace / MiniSpace (EcoDisc)
ENGINEERING_NORMS = {
    "motor_current_rms": {"unit": "A", "baseline": 12.0, "std": 1.2, "elevated_pct": 30.0, "severe_pct": 80.0},
    "igbt_temp": {"unit": "°C", "baseline": 45.0, "std": 3.0, "elevated_pct": 25.0, "severe_pct": 55.0},
    "motor_temp": {"unit": "°C", "baseline": 50.0, "std": 3.5, "elevated_pct": 30.0, "severe_pct": 60.0},
    "vibration_rms": {"unit": "m/s2", "baseline": 0.08, "std": 0.015, "elevated_pct": 50.0, "severe_pct": 150.0},
    "door_cycle_time_ms": {"unit": "ms", "baseline": 2800.0, "std": 150.0, "elevated_pct": 25.0, "severe_pct": 50.0},
    "door_motor_current": {"unit": "A", "baseline": 1.5, "std": 0.2, "elevated_pct": 40.0, "severe_pct": 100.0},
    "brake_release_delay": {"unit": "ms", "baseline": 150.0, "std": 20.0, "elevated_pct": 50.0, "severe_pct": 100.0},
    "brake_coil_current": {"unit": "A", "baseline": 2.2, "std": 0.25, "elevated_pct": 20.0, "severe_pct": 50.0},
    "position_actual_divergence": {"unit": "mm", "baseline": 1.0, "std": 0.3, "elevated_pct": 100.0, "severe_pct": 300.0},
    "position_drift_mm": {"unit": "mm", "baseline": 0.5, "std": 0.2, "elevated_pct": 100.0, "severe_pct": 300.0},
    "leveling_deviation_mm": {"unit": "mm", "baseline": 2.0, "std": 0.5, "elevated_pct": 100.0, "severe_pct": 250.0},
    "speed_feedback_deviation": {"unit": "rpm", "baseline": 5.0, "std": 1.0, "elevated_pct": 40.0, "severe_pct": 100.0},
    "dc_bus_voltage": {"unit": "V", "baseline": 560.0, "std": 15.0, "elevated_pct": 15.0, "severe_pct": 30.0},
    "machine_room_temp_c": {"unit": "°C", "baseline": 24.0, "std": 2.0, "elevated_pct": 35.0, "severe_pct": 70.0}
}


class EWMATracker:
    """
    Exponentially Weighted Moving Average (EWMA) tracker for streaming elevator telemetry.
    Smooths high-frequency noise and detects persistent mean shifts.
    """
    def __init__(self, alpha: float = 0.2, baseline_mean: Optional[float] = None, baseline_std: Optional[float] = None):
        self.alpha = alpha
        self.mean: Optional[float] = baseline_mean
        self.baseline_std: Optional[float] = baseline_std
        self.var: Optional[float] = (baseline_std ** 2) if baseline_std else None
        self.step_count = 0

    def update(self, value: float) -> float:
        """
        Updates the EWMA model with a new measurement and returns the normalized z-score.
        """
        self.step_count += 1
        if self.mean is None:
            self.mean = value
            self.var = (self.baseline_std ** 2) if self.baseline_std else 0.0
            return 0.0
        
        diff = value - self.mean
        current_std = np.sqrt(self.var) if (self.var and self.var > 1e-6) else (self.baseline_std or 1.0)
        z_score = abs(diff) / current_std

        self.mean = self.alpha * value + (1 - self.alpha) * self.mean
        if self.var is None or self.var < 1e-6:
            self.var = diff ** 2
        else:
            self.var = (1 - self.alpha) * (self.var + self.alpha * (diff ** 2))
        
        return float(z_score)

    def update_series(self, values: List[float]) -> List[float]:
        """Processes a sequence of measurements and returns list of z-scores."""
        return [self.update(v) for v in values]

    def get_smoothed_value(self) -> Optional[float]:
        return self.mean


class CUSUMTracker:
    """
    Two-Sided Tabular Cumulative Sum (CUSUM) Control Chart.
    Optimized for early detection of subtle, persistent parameter drifts
    (e.g., door track friction accumulation, brake pad clearance wear, motor thermal drift).
    
    Equations:
      S_H(t) = max(0, S_H(t-1) + (x_t - target - k))
      S_L(t) = max(0, S_L(t-1) - (x_t - target + k))
    """
    def __init__(
        self,
        target: float,
        std: Optional[float] = None,
        k_factor: float = 0.5,
        h_factor: float = 4.5
    ):
        self.target = float(target)
        self.std = float(std) if std and std > 0 else max(abs(self.target) * 0.1, 1.0)
        self.k = float(k_factor * self.std)  # Slack parameter / allowance
        self.h = float(h_factor * self.std)  # Decision interval threshold
        
        self.s_high = 0.0
        self.s_low = 0.0
        self.run_length_high = 0
        self.run_length_low = 0
        self.total_observations = 0

    def update(self, value: float) -> Dict[str, Any]:
        """
        Updates the CUSUM state with a new scalar observation.
        Returns drift metrics and boolean out-of-control anomaly indicator.
        """
        self.total_observations += 1
        x = float(value)
        
        # Upper CUSUM (detects positive drift)
        sh_cand = self.s_high + (x - self.target - self.k)
        if sh_cand > 0:
            self.s_high = sh_cand
            self.run_length_high += 1
        else:
            self.s_high = 0.0
            self.run_length_high = 0

        # Lower CUSUM (detects negative drift)
        sl_cand = self.s_low - (x - self.target + self.k)
        if sl_cand > 0:
            self.s_low = sl_cand
            self.run_length_low += 1
        else:
            self.s_low = 0.0
            self.run_length_low = 0

        drift_detected = False
        drift_direction = "NONE"

        if self.s_high >= self.h:
            drift_detected = True
            drift_direction = "UP"
        elif self.s_low >= self.h:
            drift_detected = True
            drift_direction = "DOWN"

        return {
            "value": x,
            "s_high": round(self.s_high, 4),
            "s_low": round(self.s_low, 4),
            "threshold_h": round(self.h, 4),
            "slack_k": round(self.k, 4),
            "drift_detected": drift_detected,
            "drift_direction": drift_direction,
            "run_length": self.run_length_high if drift_direction == "UP" else (self.run_length_low if drift_direction == "DOWN" else 0)
        }

    def update_series(self, values: List[float]) -> List[Dict[str, Any]]:
        return [self.update(v) for v in values]

    def reset(self):
        self.s_high = 0.0
        self.s_low = 0.0
        self.run_length_high = 0
        self.run_length_low = 0


class SignalTriager:
    """
    Stage 1: Analyzes and classifies all input telemetry signals using
    instantaneous engineering norm thresholding, EWMA tracking, and CUSUM drift detection.
    """
    def __init__(self):
        self.ewma_trackers: Dict[str, EWMATracker] = {}
        self.cusum_trackers: Dict[str, CUSUMTracker] = {}

    def reset(self):
        """Resets all tracking states for clean episode analysis."""
        self.ewma_trackers.clear()
        self.cusum_trackers.clear()

    def _get_or_create_ewma(self, signal_name: str, baseline: float, std: float) -> EWMATracker:
        if signal_name not in self.ewma_trackers:
            self.ewma_trackers[signal_name] = EWMATracker(alpha=0.25, baseline_mean=baseline, baseline_std=std)
        return self.ewma_trackers[signal_name]

    def _get_or_create_cusum(self, signal_name: str, baseline: float, std: float) -> CUSUMTracker:
        if signal_name not in self.cusum_trackers:
            self.cusum_trackers[signal_name] = CUSUMTracker(target=baseline, std=std, k_factor=0.5, h_factor=4.0)
        return self.cusum_trackers[signal_name]

    def classify_signal(self, telemetry: TelemetryInput, operating_state: str) -> Dict[str, Any]:
        # Quality Gate Check: Bad or missing signals provide zero diagnostic value
        if telemetry.quality in ["bad", "missing"]:
            return {
                "signal_name": telemetry.signal_name,
                "value": telemetry.value,
                "classification": "MISSING" if telemetry.quality == "missing" else "UNRELIABLE_SENSOR",
                "quality": telemetry.quality,
                "diagnostic_value": "NONE",
                "deviation_pct": 0.0,
                "state_context": operating_state,
                "ewma_z_score": 0.0,
                "cusum_drift": False,
                "detection_method": "QUALITY_GATE",
                "notes": f"Signal quality is '{telemetry.quality}' — zero diagnostic value for hypothesis scoring."
            }

        norm = ENGINEERING_NORMS.get(telemetry.signal_name)
        baseline = telemetry.baseline_value
        if baseline is None:
            baseline = norm["baseline"] if norm else telemetry.value

        std_dev = norm.get("std", 1.0) if norm else max(abs(float(baseline) if isinstance(baseline, (int, float)) else 1.0) * 0.1, 1.0)

        # Safe numeric parsing for float calculations
        def to_float_safe(v):
            if isinstance(v, bool):
                return 1.0 if v else 0.0
            if isinstance(v, (int, float)):
                return float(v)
            if isinstance(v, str):
                u = v.upper().strip()
                if u in ["TRUE", "1", "HIGH", "ACTIVE", "CLOSED", "BROKEN"]:
                    return 1.0
                if u in ["FALSE", "0", "LOW", "INACTIVE", "OPEN", "CLEAR"]:
                    return 0.0
                try:
                    return float(v)
                except ValueError:
                    return 0.0
            return 0.0

        val_num = to_float_safe(telemetry.value)
        base_num = to_float_safe(baseline)

        if base_num != 0:
            dev_pct = ((val_num - base_num) / base_num) * 100.0
        else:
            dev_pct = (val_num - base_num) * 100.0

        if telemetry.deviation_pct is not None:
            dev_pct = telemetry.deviation_pct

        # Anomaly thresholding
        elevated_thresh = norm["elevated_pct"] if norm else 25.0
        severe_thresh = norm["severe_pct"] if norm else 60.0

        # Run EWMA Tracker
        ewma_tracker = self._get_or_create_ewma(telemetry.signal_name, base_num, std_dev)
        ewma_z = ewma_tracker.update(val_num)

        # Run CUSUM Tracker
        cusum_tracker = self._get_or_create_cusum(telemetry.signal_name, base_num, std_dev)
        cusum_res = cusum_tracker.update(val_num)

        classification = "NORMAL"
        diagnostic_val = "LOW"
        detection_method = "NOMINAL"

        # Multi-Method Autonomous Fault Isolation
        if dev_pct >= severe_thresh or ewma_z >= 3.5:
            classification = "SEVERELY_ELEVATED"
            diagnostic_val = "HIGH"
            detection_method = "EWMA_SEVERE" if ewma_z >= 3.5 else "THRESHOLD_SEVERE"
        elif dev_pct >= elevated_thresh or ewma_z >= 2.0 or cusum_res["drift_detected"]:
            if cusum_res["drift_detected"] and abs(dev_pct) < severe_thresh:
                classification = "DRIFT"
                detection_method = "CUSUM_PERSISTENT_DRIFT"
            else:
                classification = "ELEVATED"
                detection_method = "EWMA_SHIFT" if ewma_z >= 2.0 else "THRESHOLD_ELEVATED"
            diagnostic_val = "HIGH"
        elif dev_pct <= -elevated_thresh or cusum_res["drift_direction"] == "DOWN":
            classification = "DROPPING"
            diagnostic_val = "MEDIUM"
            detection_method = "CUSUM_NEGATIVE_DRIFT" if cusum_res["drift_direction"] == "DOWN" else "THRESHOLD_DROPPING"
        else:
            classification = "NORMAL"
            diagnostic_val = "LOW"

        # Operating state context modifier
        # For example, motor current during DOOR_OPEN or IDLE is abnormal even if moderately low
        if operating_state in ["IDLE", "DOOR_OPEN"] and telemetry.signal_name == "motor_current_rms" and val_num > 2.0:
            classification = "SEVERELY_ELEVATED"
            diagnostic_val = "HIGH"
            detection_method = "STATE_CONTEXT_ANOMALY"

        return {
            "signal_name": telemetry.signal_name,
            "value": telemetry.value,
            "unit": telemetry.unit,
            "baseline": baseline,
            "deviation_pct": round(dev_pct, 2),
            "classification": classification,
            "quality": telemetry.quality,
            "diagnostic_value": diagnostic_val,
            "operating_state": operating_state,
            "provenance": "MEASURED",
            "ewma_z_score": round(ewma_z, 2),
            "ewma_smoothed": round(ewma_tracker.get_smoothed_value() or val_num, 3),
            "cusum_drift": cusum_res["drift_detected"],
            "cusum_direction": cusum_res["drift_direction"],
            "cusum_s_high": cusum_res["s_high"],
            "cusum_s_low": cusum_res["s_low"],
            "detection_method": detection_method
        }

    def triage_all(self, telemetry_list: List[TelemetryInput], operating_state: str) -> List[Dict[str, Any]]:
        """Processes all telemetry signals and returns classified anomaly results."""
        return [self.classify_signal(t, operating_state) for t in telemetry_list]
