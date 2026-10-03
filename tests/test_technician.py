"""
Unit Tests for Technician Feedback Interpretation Agent
"""
from pipeline.models import EvidenceType, EvidencePolarity, ReliabilityTier
from pipeline.technician import TechnicianFeedbackAgent


def test_technician_measurement_extraction():
    text = "The door takes 4.8 seconds to close. Clearance gap is 0.5 mm."
    items = TechnicianFeedbackAgent.interpret(text)
    
    assert len(items) == 2
    meas1 = items[0]
    assert meas1.type == EvidenceType.PHYSICAL_INSPECTION
    assert meas1.measurement == 4.8
    assert meas1.unit == "seconds"
    assert meas1.parameter == "door_closing_time"

    meas2 = items[1]
    assert meas2.measurement == 0.5
    assert meas2.unit == "mm"
    assert meas2.parameter == "clearance_gap"


def test_technician_negative_evidence_polarity():
    # Negative evidence that actively contradicts a roller wear hypothesis
    text = "I inspected the roller: there is no visible wear and it rotates freely."
    items = TechnicianFeedbackAgent.interpret(text)
    
    assert len(items) >= 1
    assert any(it.polarity == EvidencePolarity.CONTRADICTING for it in items)
    contradicting_item = next(it for it in items if it.polarity == EvidencePolarity.CONTRADICTING)
    assert contradicting_item.type == EvidenceType.PHYSICAL_INSPECTION
    assert "roller" in contradicting_item.component.lower()


def test_technician_supporting_evidence_polarity():
    # Positive fault evidence that supports a mechanical binding hypothesis
    text = "The door becomes harder to move near fully closed with mechanical resistance."
    items = TechnicianFeedbackAgent.interpret(text)
    
    assert len(items) >= 1
    item = items[0]
    assert item.polarity == EvidencePolarity.SUPPORTING
    assert item.reliability == ReliabilityTier.PHYSICAL_INSPECTION


def test_technician_opinion_isolation():
    text = "I think the motor is fine, but in my opinion the belt might be loose."
    items = TechnicianFeedbackAgent.interpret(text)
    
    for item in items:
        assert item.type == EvidenceType.TECHNICIAN_OPINION
        assert item.reliability == ReliabilityTier.TECHNICIAN_OPINION
        assert item.polarity == EvidencePolarity.NEUTRAL
