# ElevateRCA — Root Cause Analysis & Elimination Reasoning

## 1. Multi-Hypothesis Diagnostic Space

A symptom (e.g. *Door Closing Delay*) is not treated as a single failure mode. Instead, ElevateRCA maps the subsystem into candidate physical hypotheses:
1. `HYP-DOOR-ROLLER`: Roller bearing wear & flat spots
2. `HYP-DOOR-TRACK-BINDING`: Mechanical binding & sill debris resistance
3. `HYP-DOOR-INTERLOCK-MISALIGN`: Interlock contact wear & beak misalignment

## 2. Contradiction Detection & Alternative Elimination

Each hypothesis accumulates supporting and contradicting evidence:
- If a technician observes: *"Roller rotates freely, zero visible wear"*, `HYP-DOOR-ROLLER` is actively `RULED_OUT`.
- The system promotes `HYP-DOOR-TRACK-BINDING` based on positive resistance observations.
- Once a physical confirmation test is recorded (`FAIL` on pass criteria), the root cause is `CONFIRMED`.

## 3. Principled Abstention

If competing hypotheses have equal moderate support with insufficient differentiating evidence, the system refuses to guess and sets:
`current_root_cause = "AMBIGUOUS"` and `confidence_tier = INSUFFICIENT_EVIDENCE`.
