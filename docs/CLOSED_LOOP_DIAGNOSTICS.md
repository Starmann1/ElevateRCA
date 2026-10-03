# ElevateRCA — Closed-Loop Diagnostics & Validation Gatekeeper

## 1. Post-Repair Validation Workflow

A diagnostic case cannot be closed based solely on a proposed fix. It must pass through the **Post-Repair Validation Gatekeeper**:

```
[Repair Completed] ──► [Test Cycles Run (>= 3)] ──► [Submit Validation]
                                                           │
                                ┌──────────────────────────┴──────────────────────────┐
                                │                                                     │
                             [Pass]                                                [Fail]
                                │                                                     │
                                ▼                                                     ▼
                             CLOSED                                              RCA_REOPENED
                   (Fault cleared & verified)                              (Recurrence added as evidence;
                                                                           re-enters investigation)
```
