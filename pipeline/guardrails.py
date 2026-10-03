"""
ElevateRCA — Safety Boundaries & Claim Discipline Guardrails (Part 2 & Part 8)
Guarantees strict read-only advisory operation and eliminates uncalibrated/prohibited claims.
"""

import re
from typing import List, Tuple, Dict, Any


FORBIDDEN_PHRASES = [
    (r"kone has no rca capability", "Cannot claim competitor lacks RCA — state 'Not publicly established that KONE demonstrates this specific capability'"),
    (r"this definitely is", "Cannot claim certainty — express as probability with evidence citations"),
    (r"the elevator is safe to restart", "Never authorize restart — safety reset belongs strictly to qualified technicians"),
    (r"will save \d+ hours of downtime", "Cannot claim specific downtime or financial savings — unvalidated hypothesis"),
    (r"based on our production data", "Cannot claim production data — use 'based on engineering knowledge'"),
    (r"our system is the first to do this", "Cannot make first-mover promotional claims"),
    (r"i am certain", "Cannot express certainty — always report calibrated numeric confidence score"),
    (r"guarantee(?:s|d)? fix", "Cannot guarantee repairs or outcomes — advisory only"),
]

MANDATORY_DISCLAIMER = "⚠️ HUMAN VERIFICATION REQUIRED — This analysis is advisory only. A qualified elevator technician must inspect and authorize all actions."


class SafetyGuardrails:
    """Enforces Part 2 Hard Prohibitions and Part 8 Claim Discipline."""

    @staticmethod
    def validate_advisory_state(action_payload: Dict[str, Any]) -> bool:
        """Ensures system cannot generate actuator commands or safety chain bypasses."""
        prohibited_keys = ["command_motor", "reset_safety_chain", "override_brake", "bypass_interlock", "dispatch_work_order"]
        for key in prohibited_keys:
            if key in action_payload:
                raise PermissionError(f"HARD SAFETY VIOLATION: ElevateRCA is prohibited from executing command '{key}'.")
        return True

    @staticmethod
    def check_claim_discipline(text: str) -> List[str]:
        """Scans generated text for any Part 8 forbidden phrases and returns violation flags."""
        violations = []
        lower_text = text.lower()
        for pattern, explanation in FORBIDDEN_PHRASES:
            if re.search(pattern, lower_text):
                violations.append(f"CLAIM DISCIPLINE VIOLATION [{pattern}]: {explanation}")
        return violations

    @staticmethod
    def enforce_disclaimer(response_text: str) -> str:
        """Appends mandatory human verification disclaimer if missing."""
        if MANDATORY_DISCLAIMER not in response_text:
            return f"{response_text}\n\n{MANDATORY_DISCLAIMER}"
        return response_text
