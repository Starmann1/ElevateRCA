# KONE Elevate — Demo Execution Plan

## Demo Philosophy
- **Demonstration-First Design**: The demo is not an afterthought; the system is built to demonstrate
- **Observable Workflow**: Never say "the AI thinks..."; show the evidence graph
- **Epistemic Humility**: The abstention demo (Case 5) is the FLAGSHIP case

## Demo Timeline (8-10 Minutes)

### Minutes 0-2: Problem Context
- Present the alarm flood problem: 1 root cause → 5 cascading alarms → confused technician
- Show: "Fault Code ≠ Root Cause" with the motor overcurrent example (9 possible causes)
- Key claim: "Current systems tell you WHAT happened; we tell you WHY"
- Show: Industry Capability Maturity Model (Levels 0-7, competitors at Level 3-4, we target 5-6)

### Minutes 2-4: Live Pipeline Demonstration
- **Case 1 — Motor Overcurrent (Differential Diagnosis)**
  - Trigger: Inject brake drag fault into simulator
  - Show live: RAW TELEMETRY → ANOMALY DETECTION (EWMA/CUSUM flags sustained current deviation) → CASCADE GROUPING (overcurrent + drive trip → 1 episode) → EVIDENCE RETRIEVAL (RAG pulls troubleshooting docs) → HYPOTHESIS GENERATION (9 candidates from fault tree) → ALTERNATIVE ELIMINATION (IGBT eliminated: drive self-test clean; winding fault eliminated: phases balanced) → BAYESIAN RANKING (brake drag: 71%, mechanical jam: 19%) → CONFIDENCE TIER: HIGH
  - Judge takeaway: "This isn't a lookup table; it performs differential diagnosis"

### Minutes 4-5: Alarm Cascade Demo
- **Case 4 — Alarm Cascade**
  - Trigger: IGBT failure → 5 alarms in 800ms
  - Show: System identifies 1 primary alarm, 4 consequential
  - Show: Consequential alarm suppression
  - Judge takeaway: "One root fault, not five independent problems"

### Minutes 5-7: The Flagship Abstention Case
- **Case 5 — Insufficient Evidence (Abstention)**
  - Trigger: Conflicting evidence (drive thermal vs brake mechanical)
  - Show: System REFUSES to make a high-confidence guess
  - Show: Explicit output: "Insufficient evidence to distinguish between Drive Thermal Drift (42%) and Brake Mechanical Adjustment (40%). Recommended: Manual inspection of brake air gap and drive heatsink fan."
  - Judge takeaway: "The system knows what it doesn't know"

### Minutes 7-8: ExplainabilityTrace & Human Review
- Show the complete ExplainabilityTrace for Case 1:
  - Observation → Evidence For/Against → Hypotheses Evaluated → Alternatives Eliminated → Confidence → Source Citations
- Show the dual-audience rendering:
  - Technician view: Step-by-step verification, parts, tools
  - Manager view: Status, ETA, escalation flag
- Show: Human review workflow (accept/edit/reject)

### Minutes 8-10: Q&A Defense
- Prepared responses for judge questions (from Phase 11):
  - "Doesn't KONE already have GenAI?" → Yes, but not structured differential diagnosis
  - "Doesn't TKE do agentic AI?" → Yes, but no evidence of causal RCA
  - "Can anyone build this in a weekend?" → LLM+RAG yes; the domain ontology, elimination logic, and validation no
  - "What about real data?" → Honest about synthetic; validated components with real public datasets
  - "Is this safe?" → Zero control path; read-only; human-in-the-loop permanent

## 5 Demo Scenarios Detail

For each scenario, define:
- Scenario name and ID
- Fault injected (simulator command)
- Expected telemetry behavior
- Expected alarm sequence
- Expected episode formation
- Expected hypothesis ranking
- Expected eliminated alternatives with reasoning
- Expected confidence tier
- Expected ExplainabilityTrace content
- What this proves to judges

### Scenario 1: Motor Overcurrent / Brake Drag
- Scenario name and ID: Case 1 - Motor Overcurrent
- Fault injected: `inject_fault brake_drag_severe`
- Expected telemetry behavior: Sustained 15% increase in phase current during acceleration and steady-state
- Expected alarm sequence: `WARN_CURRENT_HIGH` followed by `ERR_DRIVE_TRIP`
- Expected episode formation: Single episode containing overcurrent and drive trip, span 2000ms
- Expected hypothesis ranking: Brake drag (71%), Mechanical jam (19%)
- Expected eliminated alternatives with reasoning: IGBT failure (eliminated, drive self-test clean), Winding fault (eliminated, phases balanced)
- Expected confidence tier: HIGH
- Expected ExplainabilityTrace content: Traces from raw current anomaly -> causal graph -> hypothesis elimination
- What this proves to judges: Differential diagnosis replacing lookup tables

### Scenario 2: Door Degradation / Photo-Eye Drift
- Scenario name and ID: Case 2 - Door Degradation
- Fault injected: `inject_fault photo_eye_drift_longitudinal`
- Expected telemetry behavior: Gradual door cycle time increase + photo-eye instability over 14 simulated days
- Expected alarm sequence: Intermittent `WARN_DOOR_OBSTRUCTION`
- Expected episode formation: Multi-day trend episode
- Expected hypothesis ranking: Photo-eye degradation (#1)
- Expected eliminated alternatives with reasoning: Physical obstruction eliminated (occurs multi-cycle, at random positions, unlike stationary blockage)
- Expected confidence tier: MEDIUM
- Expected ExplainabilityTrace content: Temporal trend line analysis, ruling out instantaneous mechanical blockage
- What this proves to judges: Temporal trend detection, longitudinal analysis

### Scenario 3: Encoder/Position Anomaly
- Scenario name and ID: Case 3 - Encoder Anomaly
- Fault injected: `inject_fault encoder_drift`
- Expected telemetry behavior: Encoder position deviates from true position, causing leveling error
- Expected alarm sequence: `ERR_LEVELING_FAILED`, `WARN_POSITION_MISMATCH`
- Expected episode formation: Single episode around leveling event
- Expected hypothesis ranking: Encoder degradation (#1)
- Expected eliminated alternatives with reasoning: Traction slip eliminated by cross-validation with independent leveling sensor showing correct position
- Expected confidence tier: HIGH
- Expected ExplainabilityTrace content: Cross-sensor validation logic prioritizing independent physical sensor over derived encoder position
- What this proves to judges: "System doubts the sensor before blaming the elevator"

### Scenario 4: Alarm Cascade / IGBT Failure
- Scenario name and ID: Case 4 - Alarm Cascade
- Fault injected: `inject_fault igbt_overcurrent`
- Expected telemetry behavior: Instantaneous current spike, drive shutdown
- Expected alarm sequence: `ERR_IGBT_FAULT`, `ERR_OVERCURRENT`, `ERR_DRIVE_TRIP`, `ERR_BRAKE_DROP`, `ERR_SAFETY_CHAIN` (5 alarms in 800ms)
- Expected episode formation: 1 episode, IGBT as primary, 4 consequential
- Expected hypothesis ranking: IGBT Failure (95%)
- Expected eliminated alternatives with reasoning: Other mechanical issues eliminated by instantaneous electrical failure signature
- Expected confidence tier: HIGH
- Expected ExplainabilityTrace content: Consequential alarm suppression graph
- What this proves to judges: Alarm flood rationalization

### Scenario 5: Conflicting Evidence / Abstention
- Scenario name and ID: Case 5 - Conflicting Evidence
- Fault injected: `inject_fault ambiguous_thermal_brake`
- Expected telemetry behavior: Slight thermal increase + slight mechanical drag signature
- Expected alarm sequence: `WARN_TEMP_HIGH`, `WARN_CURRENT_HIGH`
- Expected episode formation: Single ambiguous episode
- Expected hypothesis ranking: Drive Thermal Drift (42%), Brake Mechanical Adjustment (40%)
- Expected eliminated alternatives with reasoning: Overload eliminated (load weigh sensor normal)
- Expected confidence tier: LOW
- Expected ExplainabilityTrace content: Explicitly shows conflicting evidence vectors canceling each other out
- What this proves to judges: Epistemic humility, principled abstention

## Fallback Plan
From master prompt — Demo-Safe Fallback Architecture:
- If LLM API fails: Fall back to deterministic BN + rule-based synthesis (no natural language)
- If RAG fails: Fall back to fault-tree-only diagnosis (no document citations)
- If database fails: Use in-memory episode state
- If dashboard fails: Use API endpoints directly with curl/Postman
- If simulator fails: Use pre-generated static scenario data

## Pre-Demo Checklist
1. All 5 scenarios pass in automated test suite
2. Docker Compose up with no errors
3. API health check returns 200
4. Dashboard loads and displays fleet view
5. LLM API key valid and rate limit not exceeded
6. Pre-generated fallback scenario data available
7. Demo script printed and rehearsed
8. Backup laptop with identical environment

## Judge Q&A Preparation
For each of the 5 defensible differentiators, prepare:
- 30-second elevator pitch
- Technical depth explanation (2 minutes)
- Evidence citation from source documents
- Honest limitation acknowledgment
