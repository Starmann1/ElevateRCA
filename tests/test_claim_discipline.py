"""
Unit tests for Safety Guardrails and Claim Discipline (Part 2 & Part 8).
"""

import pytest
from pipeline.guardrails import SafetyGuardrails, MANDATORY_DISCLAIMER


def test_safety_boundary_prohibitions():
    # Attempting to issue prohibited commands must raise PermissionError
    with pytest.raises(PermissionError):
        SafetyGuardrails.validate_advisory_state({"command_motor": "STOP", "speed": 0})

    with pytest.raises(PermissionError):
        SafetyGuardrails.validate_advisory_state({"reset_safety_chain": True})

    # Read-only observation actions pass
    assert SafetyGuardrails.validate_advisory_state({"observe_telemetry": True, "generate_report": True})


def test_forbidden_phrases_detection():
    bad_text = "This definitely is an IGBT fault and will save 12 hours of downtime. I am certain."
    violations = SafetyGuardrails.check_claim_discipline(bad_text)
    assert len(violations) >= 3

    good_text = "Evidence suggests IGBT inverter fault with calibrated confidence 74%. Advisory only."
    violations_clean = SafetyGuardrails.check_claim_discipline(good_text)
    assert len(violations_clean) == 0


def test_mandatory_disclaimer():
    text = "Report completed."
    with_disclaimer = SafetyGuardrails.enforce_disclaimer(text)
    assert MANDATORY_DISCLAIMER in with_disclaimer
