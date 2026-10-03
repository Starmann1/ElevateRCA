# ElevateRCA — RAG GUIDE Corpus Specification & Registry

> **Document Version:** 1.0.0  
> **Status:** Active Reference  
> **Scope:** Primary RAG Knowledge Base (`GUIDE/` folder)  
> **Authority Level:** Highest technical ground truth for ElevateRCA diagnostics

---

## 1. Executive Overview

The `GUIDE/` directory serves as the **First-Class Technical Knowledge Base** for the ElevateRCA diagnostic intelligence layer. It contains authoritative OEM maintenance manuals, electrical/mechanical safety system inspection guides (SETS), component specifications, and structured troubleshooting records.

In ElevateRCA:
$$\text{RETRIEVED DOCUMENTATION} > \text{LLM GENERAL KNOWLEDGE}$$

The diagnostic engine must never synthesize or fabricate maintenance procedures, inspection thresholds, or safety actions beyond what is documented in this corpus.

---

## 2. Complete GUIDE Document Registry

The corpus comprises **15 authoritative technical documents** categorized across 4 authority tiers:

| # | Filename | Document Type | Subsystem | Configuration / Applicability | Authority Tier | Primary Purpose / Diagnostic Role | Ingestion Strategy |
|---|---|---|---|---|---|---|---|
| 1 | `brake_of_geared_traction_machine.pdf` | `BRAKE_SYSTEM_GUIDE` | Brake / Traction | Geared traction machines | Tier 2 (Component) | Mechanical brake air gap, plunger stroke, lining wear limits, lubrication, torque check | Structure-aware PDF parsing (sections, tables, wear limits) |
| 2 | `brake_of_gearless_traction_machine.pdf` | `BRAKE_SYSTEM_GUIDE` | Brake / Traction | Gearless traction machines (EcoDisc / PMSM) | Tier 2 (Component) | Gearless disc/drum brake inspection, coil resistance, release timing, microswitch clearance | Structure-aware PDF parsing (clearance tables, timing tolerances) |
| 3 | `elevator_brake_pad.pdf` | `COMPONENT_GUIDE` | Brake | Brake pad / lining assembly | Tier 2 (Component) | Friction material limits, contamination checks (oil/grease), glazing criteria, replacement threshold | Table extraction for pad thickness and wear limits |
| 4 | `elevator_door_operations.pdf` | `DOOR_SYSTEM_GUIDE` | Door System | Landing & car doors, belt/operator | Tier 2 (Component) | Door cycle timing, belt tension, skate roller clearance, interlock adjustment, photo-eye alignment | Step-by-step procedures, timing tables, roller adjustment limits |
| 5 | `elevator_hoisting_rope.pdf` | `HOISTING_SYSTEM_GUIDE` | Hoisting / Traction | Suspension & governor ropes | Tier 2 (Component) | Crown wire breakage limits, diameter reduction limits, unequal tension diagnosis, lubrication | Rope discard criteria tables (ISO 4344 / EN 81) |
| 6 | `sets_egov_8_9.pdf` | `SAFETY_SYSTEM_MANUAL` | SETS-01 Safety System | `EGOV = 8` or `9` | Tier 1 (Diagnostic Auth) | Electronic governor inspection, overspeed trip threshold, switch gap, calibration for settings 8 & 9 | Preserved conditional applicability (`EGOV=8|9`), calibration tables |
| 7 | `sets_egov_a.pdf` | `SAFETY_SYSTEM_MANUAL` | SETS-01 Safety System | `EGOV = A` | Tier 1 (Diagnostic Auth) | Safety circuit terminal checks, governor setting A verification, test mode procedure | Preserved conditional applicability (`EGOV=A`), terminal maps |
| 8 | `sets_egov_b.pdf` | `SAFETY_SYSTEM_MANUAL` | SETS-01 Safety System | `EGOV = B` | Tier 1 (Diagnostic Auth) | Electrical governor setting B parameters, trip speed verification, sensor alignment | Preserved conditional applicability (`EGOV=B`), sensor tables |
| 9 | `sets_egov_d_e.pdf` | `SAFETY_SYSTEM_MANUAL` | SETS-01 Safety System | `EGOV = D` or `E` | Tier 1 (Diagnostic Auth) | Electronic governor parameters D & E, deceleration monitor, safety gear engagement test | Preserved conditional applicability (`EGOV=D|E`), test points |
| 10 | `sets_egov_f.pdf` | `SAFETY_SYSTEM_MANUAL` | SETS-01 Safety System | `EGOV = F` | Tier 1 (Diagnostic Auth) | Governor variant F parameters, buffer stroke, safety switch contacts | Preserved conditional applicability (`EGOV=F`), electrical tolerances |
| 11 | `sets-11.pdf` | `SAFETY_SYSTEM_MANUAL` | SETS-11 Safety System | `SETS-11` Architecture | Tier 1 (Diagnostic Auth) | Next-generation SETS-11 safety system inspection, digital safety chain bus diagnostics | Architectural separation from SETS-01, safety bus codes |
| 12 | `kone guide maintainance procdure.pdf` | `MAINTENANCE_MANUAL` | General Elevator Systems | KONE Fleet / MonoSpace / MiniSpace | Tier 1 (OEM Authority) | Comprehensive routine preventative maintenance schedules, safety lockout (LOTO), lubricant types | Section/chapter hierarchy, LOTO warnings, periodic inspection intervals |
| 13 | `OEM 1.pdf` | `OEM_REFERENCE` | Controller & Drive | OEM Standard Controllers | Tier 1 (OEM Authority) | Controller fault codes, PCB terminal diagnostics, drive trip reset constraints, power supply specs | Fault code lookup tables, terminal definitions, safety warnings |
| 14 | `elevator_troubleshooting_dataset.csv` | `TROUBLESHOOTING_DATASET` | Multi-Subsystem (15 components) | Cross-Fleet Generic | Tier 3 (Structured Dataset) | 15 canonical fault/symptom/cause/check/action mapping rows (ELV-001 to ELV-015) | Row-to-structured entity conversion, exact keyword indexing |
| 15 | `elevator_troubleshooting_dataset.json` | `TROUBLESHOOTING_DATASET` | Multi-Subsystem (15 components) | Cross-Fleet Generic | Tier 3 (Structured Dataset) | Structured JSON equivalent of CSV dataset (id, component, symptom, alarm, evidence, causes) | JSON record parsing, direct field indexing into metadata store |

---

## 3. Authority Hierarchy & Conflict Resolution

When multiple retrieved chunks address the same diagnostic symptom or component, the system prioritizes evidence according to strict hierarchical precedence:

```
┌────────────────────────────────────────────────────────┐
│ TIER 1 — OEM / DIAGNOSTIC AUTHORITY                     │
│ • kone guide maintainance procdure.pdf                  │
│ • OEM 1.pdf                                            │
│ • Model/Configuration-Specific SETS Manuals (8_9..f, 11)│
└───────────────────────────┬────────────────────────────┘
                            │ Overrides
                            ▼
┌────────────────────────────────────────────────────────┐
│ TIER 2 — COMPONENT & SYSTEM MANUALS                    │
│ • brake_of_gearless_traction_machine.pdf               │
│ • brake_of_geared_traction_machine.pdf                 │
│ • elevator_door_operations.pdf                         │
│ • elevator_brake_pad.pdf / elevator_hoisting_rope.pdf   │
└───────────────────────────┬────────────────────────────┘
                            │ Overrides
                            ▼
┌────────────────────────────────────────────────────────┐
│ TIER 3 — STRUCTURED TROUBLESHOOTING DATASET            │
│ • elevator_troubleshooting_dataset.csv                 │
│ • elevator_troubleshooting_dataset.json                │
└───────────────────────────┬────────────────────────────┘
                            │ Overrides
                            ▼
┌────────────────────────────────────────────────────────┐
│ TIER 4 — GENERAL / EXTERNAL DOMAIN KNOWLEDGE           │
│ • Pretrained LLM parametric knowledge                  │
│ • Public academic publications                         │
└────────────────────────────────────────────────────────┘
```

### Conflict Resolution Rules
1. **Configuration Specificity Rule:** A manual matching the specific elevator configuration (e.g., `EGOV=A` or `Machine=Gearless`) strictly supersedes general component manuals.
2. **Safety Primacy Rule:** In any conflict between operational adjustment and safety clearance/trip settings, the safety document (SETS or LOTO procedure) takes precedence.
3. **Explicit Conflict Flagging:** If two Tier 1 documents present contradictory numerical limits for the same setting, ElevateRCA flags `DOCUMENTATION_CONFLICT` and requests human supervisory verification rather than averaging or guessing.

---

## 4. Document Applicability & Configuration Filtering

### The SETS-01 Matrix Challenge
The SETS-01 electronic governor documentation is divided into 5 distinct configuration manuals based on the hardware setting dial:
- `sets_egov_8_9.pdf` $\rightarrow$ Settings `8` or `9`
- `sets_egov_a.pdf` $\rightarrow$ Setting `A`
- `sets_egov_b.pdf` $\rightarrow$ Setting `B`
- `sets_egov_d_e.pdf` $\rightarrow$ Settings `D` or `E`
- `sets_egov_f.pdf` $\rightarrow$ Setting `F`
- `sets-11.pdf` $\rightarrow$ Generation 11 system (distinct hardware architecture)

### Applicability Gatekeeper Rule
```python
if case.configuration.get("egov") == "A":
    allowed_sets_docs = ["sets_egov_a.pdf"]
elif case.configuration.get("egov") in ["8", "9"]:
    allowed_sets_docs = ["sets_egov_8_9.pdf"]
elif case.configuration.get("egov") is None:
    # UNKNOWN CONFIGURATION:
    # Do not retrieve from configuration-specific manuals.
    # Surface warning: "SETS EGOV configuration unknown; manual inspection required."
    allowed_sets_docs = []
```

---

## 5. Ingestion & Chunking Specification

### 5.1 PDF Structure-Aware Chunking
Blind character-count or fixed-token splitting destroys procedural integrity and detaches warnings from actions. The ingestion pipeline implements **Structure-Aware Chunking**:
1. **Hierarchy Preservation:** Document $\rightarrow$ Section $\rightarrow$ Subsection $\rightarrow$ Procedure $\rightarrow$ Step.
2. **Context Header Injection:** Every chunk prepends breadcrumb context:
   `[Document: {filename} | Section: {section_title} | Page: {page_no} | Config: {egov/model}]`
3. **Table Isolation:** Tables are parsed as discrete Markdown or JSON chunks with column headers intact. A table row is never split across chunks.
4. **Safety Warning Binding:** Warnings ("DANGER", "WARNING", "CAUTION", "LOTO") are atomically bound to the step they precede.

### 5.2 Structured Dataset Ingestion (CSV / JSON)
Rather than ingesting CSV/JSON as flat text lines, each of the 15 records (`ELV-001` through `ELV-015`) is converted into a rich semantic entity:
```json
{
  "record_id": "ELV-005",
  "component": "Door System",
  "symptom": "Doors do not open or close normally",
  "alarm": "Door fault / safety-chain fault if reported",
  "evidence": "Door movement is slow, incomplete, noisy, or inconsistent",
  "possible_causes": ["Door operator issue", "track/roller wear", "obstruction", "sensor or interlock issue"],
  "maintenance_check": "Observe door operation and inspect accessible door components and safety signals",
  "recommended_action": "Keep the elevator out of normal service if the door safety function is abnormal; qualified inspection required",
  "priority": "Critical",
  "root_cause_category": "Door",
  "document_type": "TROUBLESHOOTING_DATASET",
  "authority": "TIER_3"
}
```

---

## 6. Metadata Schema Specification

Every stored vector and metadata document adheres to the strict schema below:

```json
{
  "document_id": "DOC-DOOR-004-P12",
  "filename": "elevator_door_operations.pdf",
  "document_type": "DOOR_SYSTEM_GUIDE",
  "authority": "TIER_2",
  "manufacturer": "OEM Generic / KONE Reference",
  "system": "Door Operator",
  "subsystem": "Door",
  "component": "Skate Roller / Drive Belt",
  "failure_mode": "Roller Wear / Timing Slip",
  "fault_code": "E501",
  "model": "All",
  "configuration": "Belt-Driven Operator",
  "egov_setting": null,
  "espd_setting": null,
  "procedure_type": "INSPECTION_AND_ADJUSTMENT",
  "section": "3.2 Skate Roller Clearance",
  "page": 12,
  "source": "GUIDE"
}
```

---

## 7. Status & Verification Plan

| Metric / Stage | Target | Verification Method |
|---|---|---|
| **Files Discovered** | 15 / 15 | Filesystem scan across `GUIDE/` |
| **PDF Extraction** | 13 PDFs parsed with page/section bounds | Page count and non-empty text audit |
| **Dataset Ingestion** | 15 CSV rows + 15 JSON records parsed | Schema key validation against model |
| **Table Extraction** | Minimum 25 critical parameter tables preserved | Table markdown validation |
| **Metadata Tagging** | 100% of chunks contain `authority`, `subsystem`, `page` | Schema enforcement test |
| **Retrieval Accuracy** | Query for "door skate roller" returns `elevator_door_operations.pdf` top-1 | Hybrid retrieval test suite |
| **Configuration Isolation** | Query with `EGOV=A` never retrieves `sets_egov_f.pdf` chunks | Applicability filter test |
