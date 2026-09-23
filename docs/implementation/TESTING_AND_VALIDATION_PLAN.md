# KONE Elevate — Testing and Validation Plan

## Philosophy
"Architecture ≠ validation. AI sophistication ≠ diagnostic correctness. A convincing explanation ≠ a correct root cause." (Phase 9)

> [!IMPORTANT]
> **DOCUMENTED FACT**: This document defines the complete testing and validation strategy, drawing from Phase 9 requirements.

## Validation Hierarchy (9 Layers)
Each layer's failure invalidates all layers above it.
1. DATA VALIDATION
2. SIGNAL VALIDATION
3. EVENT/ALARM VALIDATION
4. ANOMALY VALIDATION
5. FAULT ISOLATION VALIDATION
6. RCA VALIDATION
7. EXPLANATION VALIDATION
8. HUMAN-USABILITY VALIDATION
9. SYSTEM-LEVEL VALIDATION

## Ground Truth Tiers
> [!NOTE]
> **DOCUMENTED INTENT**: From Phase 9 §11.3

- **Tier 1 — True Ground Truth**: Physics-controlled injection (simulator with known faults)
- **Tier 2 — Expert-Labeled**: Senior engineer consensus
- **Tier 3 — Inferred**: Historical work order reconstruction (weakest)

> [!WARNING]
> **PROTOTYPE SIMPLIFICATION**: For MVP, only Tier 1 (simulator) is available.

## Test Levels

### Unit Tests
- **Signal Triage**: Test `update_and_score()` with known inputs; verify z-score calculation, CUSUM accumulation, `sustained_deviation` flag.
- **Alarm Correlation**: Test `cluster_alarms()` with predefined alarm sequences; verify primary/consequential separation, time window enforcement.
- **Bayesian RCA**: Test pgmpy model with known evidence; verify posterior probabilities match manual calculation.
- **Confidence Decision**: Test `decide()` function with boundary values (0.44, 0.45, 0.74, 0.75).
- **Knowledge Loading**: Test YAML parsing for `failure_modes.yaml`, `causal_links.yaml`, `corrective_actions.yaml`.
- **Data Validation**: Test Pydantic model validation with valid, invalid, and edge-case inputs.

### Integration Tests
- **Pipeline End-to-End**: Simulator → Triage → Correlation → RCA → Confidence → ExplainabilityTrace.
- **RAG Retrieval**: Known query returns expected corpus chunks.
- **LLM Structured Output**: Mock Anthropic client for CI; verify schema compliance.
- **API Endpoint**: POST telemetry → GET diagnosis chain.
- **Database Round-Trip**: Write/read all model types through API.

### Scenario-Based Tests
Define the 5 core demo scenarios as test cases:

1. **Scenario 1: Motor Overcurrent (Differential Diagnosis)**
   - **Inject**: Brake drag (elevated current correlated with brake timing)
   - **Expected**: Brake drag ranked #1; IGBT eliminated (drive self-test clean, temperature normal); mechanical obstruction ranked #2
   - **Verify**: Top-1 root cause accuracy, alternative elimination

2. **Scenario 2: Door Degradation (Gradual Drift)**
   - **Inject**: Photo-eye optical degradation over 14 days
   - **Expected**: Photo-eye degradation ranked #1; physical obstruction eliminated
   - **Verify**: Temporal trend detection, correct subsystem isolation

3. **Scenario 3: Encoder/Position Anomaly (Cross-Sensor Validation)**
   - **Inject**: Encoder drift while independent leveling sensor reports correct position
   - **Expected**: Encoder degradation ranked #1; traction slip eliminated by sensor cross-check
   - **Verify**: Cross-sensor disagreement detection

4. **Scenario 4: Alarm Cascade (Primary vs Consequential)**
   - **Inject**: IGBT failure causing 5 cascading alarms in 800ms
   - **Expected**: 1 episode, 1 primary alarm (IGBT overcurrent), 4 consequential
   - **Verify**: Episode count=1, primary identification correct

5. **Scenario 5: Insufficient Evidence (Abstention)**
   - **Inject**: Conflicting evidence (drive thermal + brake mechanical, insufficient differentiation)
   - **Expected**: System abstains, confidence < 0.45, explicit abstention message
   - **Verify**: Abstention triggered, no false high-confidence guess

### Negative Tests
- **Sensor Noise Burst**: Inject noise with no physical fault; verify no false episode creation.
- **Out-of-Range Values**: Inject physically impossible values; verify rejection.
- **Missing Data**: Inject gaps; verify explicit missing-data flags (not assumed normal).
- **Empty Evidence**: Verify graceful abstention when no evidence available.

## Evaluation Metrics
> [!NOTE]
> **DOCUMENTED FACT**: From Phase 9 §11.12-§11.21

### Detection Metrics
- **Precision** = TP/(TP+FP)
- **Recall** = TP/(TP+FN)
- **F1** = 2*P*R/(P+R)
- **False Positive Rate** = FP/(FP+TN)
- **Detection Latency** (time from fault onset to anomaly trigger)

### Fault Isolation Metrics
- Top-1 Subsystem Accuracy
- Top-3 Subsystem Accuracy
- Macro-F1 across fault classes

### RCA Metrics
- Root-Cause Top-1 Accuracy
- Root-Cause Top-3 Accuracy
- Causal Chain Correctness
- Alternative-Cause Elimination Accuracy
- Primary vs Consequential Alarm Classification Accuracy

### Retrieval Quality Metrics
- Precision@k, Recall@k
- MRR (Mean Reciprocal Rank)
- Context Relevance ratio

### Explanation Quality Metrics
- Citation Correctness (every claim traceable to source)
- Hallucination Rate (claims without evidence)
- Evidence Consistency

### Confidence Calibration
- Reliability Diagram (predicted confidence vs actual accuracy)
- Brier Score
- Expected Calibration Error (ECE)

### Abstention Evaluation
- Coverage (proportion answered)
- Selective Accuracy (accuracy on answered cases only)
- Risk-Coverage Curve

## Error Taxonomy (E1-E14)
> [!NOTE]
> **DOCUMENTED FACT**: From Phase 9 §11.35.

| Error Code | Category | Description | Example | Detection Method | Severity |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **E1** | Data | Corrupted/missing input | NaN in current array | Pydantic validation | High |
| **E2** | Signal | Noise mistaken for signal | EMI spike treated as fault | CUSUM filter failure | Medium |
| **E3** | Correlation | Missed causal link | Primary/Consequential split failed | Time-window assertion | High |
| **E4** | Detection | Anomaly missed | Slow drift undetected | Latency metric | High |
| **E5** | Isolation | Wrong subsystem | Identified Drive instead of Motor | Top-1 accuracy drop | Critical |
| **E6** | Root Cause | Wrong fault mechanism | Blamed wear instead of break | Top-1 RCA failure | Critical |
| **E7** | Evidence Attribution | Evidence misaligned | Used temp to prove pos error | Evidence trace | High |
| **E8** | Retrieval | Missing context | RAG missed bulletin | Recall@k drop | Medium |
| **E9** | Hallucination | Invented claim | Cited non-existent PDF | Citation parser | Critical |
| **E10** | Temporal | Wrong sequence | Effect preceded cause | Sequence validation | High |
| **E11** | Confidence | Overconfident | 95% on guess | Reliability diagram | Critical |
| **E12** | Abstention | Failed to abstain | Guessed with low info | Coverage metric | High |
| **E13** | Human Factor | Usability failure | User can't override | UX survey | Medium |
| **E14** | Security | Safety boundary breach | Attempt to send control cmd | AST check | Critical |

## Acceptance Gates
> [!NOTE]
> **DOCUMENTED FACT**: From Phase 9 §11.44

- **Gate 1 (Data Quality)**: 100% rejection of impossible values.
- **Gate 2 (Signal Processing)**: Feature extraction within tolerance.
- **Gate 3 (Fault Detection)**: Precision/Recall targets met.
- **Gate 4 (Fault Isolation)**: Top-3 accuracy on curated scenarios.
- **Gate 5 (RCA)**: Root-cause ranking accuracy passed.
- **Gate 6 (Evidence Grounding)**: Zero unsupported claims.
- **Gate 7 (Confidence)**: Selective accuracy > forced accuracy.
- **Gate 8 (Human Usability)**: Clear override mechanisms work.
- **Gate 9 (Safety/Security)**: No control commands possible.
- **Gate 10 (Demo Readiness)**: All 5 scenarios pass.

## Test Commands
> [!TIP]
> **ENGINEERING INFERENCE**: Use these commands to execute the validation suites locally or in CI pipelines.

The test suite will be run with:
```bash
pytest tests/ -v --tb=short
```

Individual scenario tests:
```bash
pytest tests/test_scenarios.py -v -k scenario_N
```
