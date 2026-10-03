# ElevateRCA — Technician Feedback Interpretation Agent

## 1. Natural Language to Structured Evidence

The Technician Feedback Agent parses informal field notes into typed `EvidenceItem` records:
- **Physical Inspection:** `"I inspected the skate roller. No visible wear."`
  - Polarity: `CONTRADICTING`
  - Reliability: `PHYSICAL_INSPECTION`
- **Quantitative Measurement:** `"The door takes 4.8 seconds to close."`
  - Parameter: `door_closing_time`
  - Measurement: `4.8` | Unit: `seconds`
  - Polarity: `SUPPORTING`
- **Subjective Impression:** `"I think the motor is fine."`
  - Type: `TECHNICIAN_OPINION`
  - Reliability: `TECHNICIAN_OPINION`
  - Polarity: `NEUTRAL` (Discounted from definitive diagnostic weight)
