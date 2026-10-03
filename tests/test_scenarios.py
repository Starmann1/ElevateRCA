"""
Comprehensive End-to-End Tests for ElevateRCA Engine
Validates all 5 canonical scenarios and the Scenario 6 Abstention Benchmark.
"""

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from pipeline.engine import ElevateRCAEngine
from simulator.scenarios import ScenarioFactory





def test_scenario_1_igbt_overcurrent(engine):
    """Scenario 1: Drive IGBT failure must be ranked #1 with HIGH confidence tier."""
    payload = ScenarioFactory.scenario_1_igbt_overcurrent()
    trace = engine.analyze(payload)

    # 1. Primary alarm and cascade
    assert trace.fault_episode.primary_alarm.alarm_code == "motor_overcurrent"
    assert len(trace.fault_episode.consequential_alarms) >= 1

    # 2. Hypothesis #1 should be IGBT Failure
    top_h = trace.hypotheses[0]
    assert "IGBT" in top_h.root_cause
    assert top_h.posterior_probability >= 0.65

    # 3. Mechanical obstruction must be eliminated by drive self-test failure
    eliminated = [h for h in trace.hypotheses if "Mechanical Obstruction" in h.root_cause]
    assert len(eliminated) > 0
    assert eliminated[0].status == "ELIMINATED"

    # 4. Conclusion & Action
    assert not trace.rca_conclusion.abstained
    assert trace.rca_conclusion.root_cause_confidence_tier == "HIGH"
    assert "IGBT" in trace.corrective_recommendation.recommended_action
    assert len(trace.corrective_recommendation.do_not_do) > 0


def test_scenario_2_mechanical_jam(engine):
    """Scenario 2: Mechanical obstruction must be ranked #1 because drive self-test passed."""
    payload = ScenarioFactory.scenario_2_mechanical_jam()
    trace = engine.analyze(payload)

    top_h = trace.hypotheses[0]
    assert "Mechanical Obstruction" in top_h.root_cause
    assert top_h.posterior_probability >= 0.50

    # IGBT should be eliminated because drive self-test PASSED
    igbt_h = next(h for h in trace.hypotheses if "IGBT" in h.root_cause)
    assert igbt_h.status == "ELIMINATED"


def test_scenario_3_door_photoeye_drift(engine):
    """Scenario 3: Light curtain degradation ranked #1 for varying door cycle reopenings."""
    payload = ScenarioFactory.scenario_3_door_photoeye_drift()
    trace = engine.analyze(payload)

    assert trace.fault_episode.primary_alarm.alarm_code == "door_obstruction_detected"
    top_h = trace.hypotheses[0]
    assert "Photo-eye" in top_h.root_cause or "Light Curtain" in top_h.root_cause
    assert top_h.posterior_probability >= 0.50
    assert "LIGHT_CURTAIN" in trace.corrective_recommendation.recommended_action


def test_scenario_4_encoder_fault(engine):
    """Scenario 4: Encoder signal degradation ranked #1 when independent sensor is normal."""
    payload = ScenarioFactory.scenario_4_encoder_fault()
    trace = engine.analyze(payload)

    top_h = trace.hypotheses[0]
    assert "Encoder" in top_h.root_cause
    assert top_h.posterior_probability >= 0.50
    assert "ENCODER" in trace.corrective_recommendation.recommended_action


def test_scenario_5_brake_drag_timing(engine):
    """Scenario 5: Brake release delay with normal torque points to brake subsystem."""
    payload = ScenarioFactory.scenario_5_brake_drag_timing()
    trace = engine.analyze(payload)

    top_h = trace.hypotheses[0]
    assert "Brake Release Timing" in top_h.root_cause
    assert top_h.posterior_probability >= 0.55
    assert not trace.rca_conclusion.abstained


def test_scenario_6_abstention(engine):
    """Scenario 6: Conflicting/degraded telemetry must trigger principled abstention."""
    payload = ScenarioFactory.scenario_6_abstention_conflicting()
    trace = engine.analyze(payload)

    assert trace.rca_conclusion.abstained
    assert trace.rca_conclusion.root_cause_confidence_tier == "ABSTAIN"
    assert "Insufficient evidence" in trace.rca_conclusion.causal_narrative
    assert "PHYSICAL" in trace.corrective_recommendation.recommended_action
