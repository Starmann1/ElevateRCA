"""
ElevateRCA - Technician Feedback & Natural Language Evidence Interpretation Agent
Converts informal field technician feedback, measurements, and inspections into structured, auditable evidence.
"""

import re
import uuid
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone

from pipeline.models import (
    EvidenceItem,
    EvidenceType,
    EvidencePolarity,
    ReliabilityTier,
)


COMPONENT_MAP = {
    "skate roller": ["skate roller", "skate", "door roller", "hanger roller", "roller"],
    "door interlock": ["interlock", "door lock", "lock contact", "interlock switch"],
    "door operator": ["door operator", "door motor", "operator motor", "door drive"],
    "door belt": ["door belt", "drive belt", "belt"],
    "photo-eye": ["photo-eye", "photo eye", "light curtain", "curtain of light", "optical sensor", "door sensor"],
    "door track / sill": ["door track", "track", "sill", "groove", "guide shoes"],
    "brake assembly": ["brake", "brake coil", "brake plunger", "brake switch", "microswitch"],
    "brake pad": ["brake pad", "brake lining", "lining", "pad"],
    "traction machine": ["traction machine", "motor", "pmsm", "ecodisc", "stator"],
    "hoist ropes": ["hoist rope", "hoisting rope", "suspension rope", "cables", "ropes"],
    "governor": ["governor", "overspeed governor", "egov", "sets"],
    "encoder": ["encoder", "pulse generator", "speed feedback", "tachometer"],
    "safety chain": ["safety chain", "safety circuit", "safety switch", "stop switch"],
}

CONTRADICTION_PATTERNS = [
    r"\b(no visible wear|no wear|zero wear|rotates freely|spins freely|clean|good condition|within spec|nominal|normal|passes|clear|intact)\b",
    r"\b(not (worn|damaged|broken|loose|binding|dragging|stuck))\b",
]

SUPPORTING_PATTERNS = [
    r"\b(worn|damaged|binding|resistance|hard to move|dragging|stuck|noisy|vibrating|overheating|loose|cracked|scorched|seized|chattering)\b",
    r"\b(excessive (wear|play|clearance|noise|heat|delay))\b",
]

OPINION_PATTERNS = [
    r"\b(i think|i feel|in my opinion|seems to be|probably|might be|looks okay to me|suspect|guess)\b"
]

MEASUREMENT_PATTERNS = [
    r"(\b\d+(\.\d+)?)\s*(seconds?|sec|s|mm|m|meters?|inches?|in|ohms?|kpa|bar|volts?|v|amps?|amperes?|a|°c|c|deg|rpm)\b"
]


class TechnicianFeedbackAgent:
    """
    Interprets technician notes into structured evidence records.
    Strictly decouples verified physical findings from subjective opinions.
    """

    @classmethod
    def interpret(cls, text: str, default_subsystem: str = "General") -> List[EvidenceItem]:
        """
        Parses multi-sentence technician text into discrete, typed EvidenceItem records.
        """
        if not text or not text.strip():
            return []

        # Split sentences carefully without splitting on decimal numbers (e.g. 4.8 or 0.5)
        raw_sentences = re.split(r"(?<!\d)\.(?!\d)|[;\n]+", text)
        evidence_items: List[EvidenceItem] = []
        last_component = None

        for s in raw_sentences:
            sentence = s.strip()
            if not sentence or len(sentence) < 3:
                continue

            item_id = f"TECH-EVD-{uuid.uuid4().hex[:8].upper()}"
            matched_component = None
            for comp_name, aliases in COMPONENT_MAP.items():
                for alias in aliases:
                    if re.search(r"\b" + re.escape(alias) + r"\b", sentence, re.I):
                        matched_component = comp_name
                        last_component = comp_name
                        break
                if matched_component:
                    break

            # Carry over component context if sentence refers to it with pronouns
            if not matched_component and last_component and re.search(r"\b(it|they|this|the component|part)\b", sentence, re.I):
                matched_component = last_component

            # 1. Check for Quantitative Measurement
            meas_match = re.search(MEASUREMENT_PATTERNS[0], sentence, re.I)
            if meas_match:
                val = float(meas_match.group(1))
                unit = meas_match.group(3).lower()
                
                param = "measurement"
                if "close" in sentence.lower() or "shut" in sentence.lower():
                    param = "door_closing_time"
                elif "open" in sentence.lower():
                    param = "door_opening_time"
                elif "gap" in sentence.lower() or "clearance" in sentence.lower():
                    param = "clearance_gap"
                elif "temp" in sentence.lower():
                    param = "temperature"
                elif "current" in sentence.lower():
                    param = "motor_current"

                evidence_items.append(
                    EvidenceItem(
                        evidence_id=item_id,
                        type=EvidenceType.PHYSICAL_INSPECTION,
                        description=sentence,
                        source="Technician Field Measurement",
                        component=matched_component or "Subsystem Component",
                        parameter=param,
                        measurement=val,
                        unit=unit,
                        polarity=EvidencePolarity.SUPPORTING,
                        reliability=ReliabilityTier.PHYSICAL_INSPECTION,
                        metadata={"raw_sentence": sentence},
                    )
                )
                continue

            # 2. Check for Technician Opinion
            is_opinion = any(re.search(p, sentence, re.I) for p in OPINION_PATTERNS)
            if is_opinion:
                evidence_items.append(
                    EvidenceItem(
                        evidence_id=item_id,
                        type=EvidenceType.TECHNICIAN_OPINION,
                        description=sentence,
                        source="Technician Opinion / Subjective Note",
                        component=matched_component or "Subsystem Component",
                        polarity=EvidencePolarity.NEUTRAL,
                        reliability=ReliabilityTier.TECHNICIAN_OPINION,
                        metadata={"opinion_flag": True, "raw_sentence": sentence},
                    )
                )
                continue

            # 3. Check for Physical Inspection Finding (Positive vs Contradictory / Negative)
            is_negative_finding = any(re.search(p, sentence, re.I) for p in CONTRADICTION_PATTERNS)
            is_positive_finding = any(re.search(p, sentence, re.I) for p in SUPPORTING_PATTERNS)

            polarity = EvidencePolarity.NEUTRAL
            if is_negative_finding:
                polarity = EvidencePolarity.CONTRADICTING
            elif is_positive_finding:
                polarity = EvidencePolarity.SUPPORTING

            evidence_items.append(
                EvidenceItem(
                    evidence_id=item_id,
                    type=EvidenceType.PHYSICAL_INSPECTION,
                    description=sentence,
                    source="Technician Physical Inspection",
                    component=matched_component or "Mechanical Component",
                    polarity=polarity,
                    reliability=ReliabilityTier.PHYSICAL_INSPECTION,
                    metadata={
                        "is_negative_finding": is_negative_finding,
                        "raw_sentence": sentence,
                    },
                )
            )

        return evidence_items
