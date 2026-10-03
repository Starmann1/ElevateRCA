"""
Comprehensive Unit Tests for EWMA & CUSUM Anomaly Detection in ElevateRCA
Verifies:
1. EWMATracker smoothing, variance tracking, and z-score computation.
2. CUSUMTracker two-sided cumulative sums (S_H, S_L), slack parameter absorption,
   and persistent drift detection (positive and negative shifts).
3. SignalTriager multi-method anomaly detection integrating EWMA, CUSUM,
   engineering norms, sensor quality gating, and state context.
"""

import pytest
import numpy as np
from pipeline.triage import EWMATracker, CUSUMTracker, SignalTriager, ENGINEERING_NORMS
from pipeline.schemas import TelemetryInput


# ============================================================================
# 1. EWMA TRACKER TESTS
# ============================================================================

def test_ewma_tracker_nominal():
    tracker = EWMATracker(alpha=0.2, baseline_mean=12.0, baseline_std=1.2)
    # Consecutive nominal readings near 12.0
    for val in [12.0, 12.2, 11.9, 12.1, 12.05]:
        z = tracker.update(val)
        assert z < 1.0, f"Expected small z-score for nominal values, got {z}"

    smoothed = tracker.get_smoothed_value()
    assert 11.9 <= smoothed <= 12.3


def test_ewma_tracker_step_shift():
    tracker = EWMATracker(alpha=0.3, baseline_mean=12.0, baseline_std=1.2)
    # Sudden large step shift to 25.0A (severe overcurrent)
    z = tracker.update(25.0)
    assert z >= 3.0, f"Expected z-score >= 3.0 for 25.0A vs baseline 12.0A, got {z}"


def test_ewma_tracker_series():
    tracker = EWMATracker(alpha=0.25)
    data = [10.0, 10.5, 10.2, 10.1, 10.3, 18.0]
    z_scores = tracker.update_series(data)
    assert len(z_scores) == len(data)
    # Last reading is a massive jump
    assert z_scores[-1] > z_scores[2]


# ============================================================================
# 2. CUSUM TRACKER TESTS
# ============================================================================

def test_cusum_nominal_no_drift():
    # Door cycle time baseline: 2800ms, std: 150ms
    cusum = CUSUMTracker(target=2800.0, std=150.0, k_factor=0.5, h_factor=4.5)
    
    # Random normal fluctuations around target
    np.random.seed(42)
    fluctuations = [2800.0 + np.random.normal(0, 30) for _ in range(20)]
    
    for val in fluctuations:
        res = cusum.update(val)
        assert not res["drift_detected"], "Nominal fluctuations must not trigger drift"
        assert res["drift_direction"] == "NONE"


def test_cusum_persistent_positive_drift():
    # Persistent upward drift: e.g. door track friction causing cycle time to creep up
    # target = 2800ms, k = 75ms (0.5*150), h = 675ms (4.5*150)
    cusum = CUSUMTracker(target=2800.0, std=150.0, k_factor=0.5, h_factor=4.5)
    
    # 8 consecutive cycle readings at 3200ms (+400ms above baseline, well above k=75ms)
    drift_detected = False
    for i in range(8):
        res = cusum.update(3200.0)
        if res["drift_detected"]:
            drift_detected = True
            assert res["drift_direction"] == "UP"
            assert res["s_high"] >= cusum.h
            break

    assert drift_detected, "Persistent +400ms shift must be caught by CUSUM"


def test_cusum_persistent_negative_drift():
    # Persistent downward drift: e.g. DC bus voltage sag
    # target = 560V, std = 15V, k = 7.5V, h = 67.5V
    cusum = CUSUMTracker(target=560.0, std=15.0, k_factor=0.5, h_factor=4.5)

    drift_detected = False
    for i in range(8):
        res = cusum.update(510.0)  # -50V below target
        if res["drift_detected"]:
            drift_detected = True
            assert res["drift_direction"] == "DOWN"
            assert res["s_low"] >= cusum.h
            break

    assert drift_detected, "Persistent negative shift must be detected by lower CUSUM"


def test_cusum_reset():
    cusum = CUSUMTracker(target=100.0, std=10.0)
    cusum.update(150.0)
    cusum.update(150.0)
    assert cusum.s_high > 0
    cusum.reset()
    assert cusum.s_high == 0.0
    assert cusum.s_low == 0.0
    assert cusum.run_length_high == 0


# ============================================================================
# 3. SIGNAL TRIAGER (MULTI-METHOD ANOMALY DETECTION) TESTS
# ============================================================================

def test_triager_sensor_quality_gating():
    triager = SignalTriager()
    bad_telemetry = TelemetryInput(
        signal_name="motor_current_rms",
        value=999.0,
        unit="A",
        quality="bad",
        timestamp="2026-10-03T10:00:00Z"
    )
    result = triager.classify_signal(bad_telemetry, operating_state="CONSTANT_SPEED")
    assert result["classification"] == "UNRELIABLE_SENSOR"
    assert result["diagnostic_value"] == "NONE"


def test_triager_missing_sensor():
    triager = SignalTriager()
    missing_telemetry = TelemetryInput(
        signal_name="vibration_rms",
        value=0.0,
        unit="m/s2",
        quality="missing",
        timestamp="2026-10-03T10:00:00Z"
    )
    result = triager.classify_signal(missing_telemetry, operating_state="CONSTANT_SPEED")
    assert result["classification"] == "MISSING"
    assert result["diagnostic_value"] == "NONE"


def test_triager_state_context_anomaly():
    triager = SignalTriager()
    # Motor current is 4.5A while operating_state is IDLE (severe anomaly even though 4.5A < 12A nominal travel current)
    idle_current = TelemetryInput(
        signal_name="motor_current_rms",
        value=4.5,
        unit="A",
        quality="good",
        timestamp="2026-10-03T10:00:00Z",
        baseline_value=12.0
    )
    result = triager.classify_signal(idle_current, operating_state="IDLE")
    assert result["classification"] == "SEVERELY_ELEVATED"
    assert result["detection_method"] == "STATE_CONTEXT_ANOMALY"


def test_triager_cusum_drift_integration():
    triager = SignalTriager()
    # Feed repeated door_cycle_time_ms readings that accumulate drift
    readings = [3300.0, 3350.0, 3400.0, 3450.0, 3500.0, 3550.0]
    last_res = None
    for r in readings:
        t = TelemetryInput(
            signal_name="door_cycle_time_ms",
            value=r,
            unit="ms",
            quality="good",
            timestamp="2026-10-03T10:00:00Z",
            baseline_value=2800.0
        )
        last_res = triager.classify_signal(t, operating_state="DOOR_CLOSE")

    assert last_res["cusum_drift"] is True
    assert last_res["classification"] in ["DRIFT", "SEVERELY_ELEVATED"]
    assert "CUSUM" in last_res["detection_method"]
