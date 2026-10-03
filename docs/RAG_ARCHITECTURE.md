# ElevateRCA — RAG Knowledge & Ingestion Architecture

## 1. Corpus Hierarchy & Authority

| Tier | Documents | Priority Multiplier |
|---|---|---|
| **Tier 1 (OEM / Safety Authority)** | `kone guide maintainance procdure.pdf`, `OEM 1.pdf`, `sets_egov_*.pdf`, `sets-11.pdf` | 1.35x |
| **Tier 2 (Component Manuals)** | `elevator_door_operations.pdf`, `brake_of_*.pdf`, `elevator_brake_pad.pdf`, `elevator_hoisting_rope.pdf` | 1.15x |
| **Tier 3 (Structured Dataset)** | `elevator_troubleshooting_dataset.csv`, `elevator_troubleshooting_dataset.json` | 1.00x |
| **Tier 4 (External Knowledge)** | General engineering principles | 0.85x |

## 2. Ingestion & Preservation

- **Structure-Aware Chunking:** Preserves section titles, page provenance, and breadcrumbs.
- **Table Preservation:** Markdown table extraction retains nominal clearances, air gaps, and tolerances.
- **Safety Isolator:** Warnings, cautions, and LOTO steps are parsed and returned as `safety_constraints`.
- **Configuration Gatekeeper:** Configuration settings (e.g., `EGOV=A` or `Machine=Gearless`) strictly filter out non-matching manual chunks.
