# ElevateRCA — Diagnostic Case State Machine

## 1. Lifecycle States

```
NEW ──► TRIAGED ──► UNDER_INVESTIGATION ──► RCA_PROPOSED
                                                │
                                                ▼
                                        TECHNICIAN_REVIEW
                                                │
                                                ▼
                                       ADDITIONAL_EVIDENCE
                                                │
                                                ▼
                                           RCA_REVISED
                                                │
                                                ▼
                                     DIAGNOSTIC_CONFIRMATION
                                                │
                                                ▼
                                         CORRECTIVE_ACTION
                                                │
                                                ▼
                                      POST_REPAIR_VALIDATION
                                                │
                                 ┌──────────────┴──────────────┐
                                 │                             │
                              [Pass]                        [Fail]
                                 ▼                             ▼
                              CLOSED                      RCA_REOPENED
                                                               │
                                                               ▼
                                                      UNDER_INVESTIGATION
```

## 2. Hypothesis States

- `CANDIDATE`: Plausible root cause generated from initial fault/symptom mapping.
- `ACTIVE`: Currently under evaluation with preliminary supporting data.
- `SUPPORTED`: Validated by 2+ corroborating evidence items.
- `DOWNGRADED`: Penalized by contradictory physical observations.
- `RULED_OUT`: Actively eliminated by direct physical inspection.
- `CONFIRMED`: Verified definitively by physical diagnostic confirmation test.
