# ElevateRCA — Canonical Multi-Iteration Demonstration Scenario

## Scenario Overview: Door Closing Timeout Incident

- **Asset:** `ELEV-DX-04` (KONE MonoSpace DX, Gearless Traction, SETS-01 `EGOV=A`)
- **Trigger:** Alarm `E501 Door Close Timeout`

### Timeline:

1. **Iteration 1 (AI Incident Triage):**
   - Telemetry indicates closing time of 4.8s.
   - Competing hypotheses generated: Roller bearing degradation (`HYP-DOOR-ROLLER`), track binding (`HYP-DOOR-TRACK-BINDING`), interlock misalignment (`HYP-DOOR-INTERLOCK-MISALIGN`).
   - RAG retrieves `elevator_door_operations.pdf` Section 4.1.

2. **Iteration 2 (Technician Inspection):**
   - Technician notes: *"I inspected the roller: there is no visible wear and it rotates freely. The door becomes harder to move near fully closed."*
   - Feedback agent extracts negative evidence on roller $\rightarrow$ `HYP-DOOR-ROLLER` is **RULED OUT**.
   - Mechanical track binding is promoted to leading hypothesis.

3. **Iteration 3 (Diagnostic Confirmation Test):**
   - Technician runs `TEST-TRACK-01` (inspect sill groove).
   - Finding: Heavy construction grit and dust discovered in sill groove. Test outcome: `FAIL` (fault confirmed).
   - Hypothesis `HYP-DOOR-TRACK-BINDING` transitions to **CONFIRMED**.
   - Corrective action generated: `ACT-DOOR-SILL-CLEAN` with required parts and tools.

4. **Iteration 4 (Post-Repair Validation & Closure):**
   - Technician cleans sill and runs 5 test door cycles without faults.
   - Post-repair validation submitted $\rightarrow$ Case status transitions to **CLOSED**.
   - Final 21-section audit report exported.
