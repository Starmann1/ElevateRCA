# KONE Elevate — Open Questions and Unknowns Register

## Purpose
This register tracks information gaps that cannot be resolved from available project documentation. Each unknown includes its impact, the temporary assumption used for the prototype, and what would be needed for production resolution.

## Format
For each unknown:
- **ID**: (U-001, U-002, etc.)
- **Unknown**: What is not known
- **Why It Matters**: Impact on the system
- **Evidence Currently Available**: What we do know
- **Impact Level**: HIGH / MEDIUM / LOW
- **Temporary Prototype Assumption**: What the prototype assumes
- **Production Resolution Required**: What would resolve this
- **Classification**: UNKNOWN / OPEN DECISION

## Unknowns:

### U-001: Proprietary KONE Telemetry Schema
- **Unknown**: The exact list of 200+ parameters monitored by KONE 24/7 Connected Services is not publicly documented.
- **Why It Matters**: Our telemetry processing needs actual parameters to map rules and models against.
- **Evidence Currently Available**: None (proprietary).
- **Impact Level**: HIGH
- **Temporary Prototype Assumption**: Prototype defines a synthetic telemetry contract based on public elevator engineering knowledge.
- **Production Resolution Required**: Would require KONE internal API documentation.
- **Classification**: UNKNOWN

### U-002: Proprietary KONE Fault Code Dictionary
- **Unknown**: KONE's internal numerical fault code taxonomy and controller-specific mappings are proprietary.
- **Why It Matters**: Accurate fault mapping is necessary for precise event correlation.
- **Evidence Currently Available**: None (proprietary).
- **Impact Level**: HIGH
- **Temporary Prototype Assumption**: Prototype uses generic fault categories (motor_overcurrent, door_close_timeout, etc.).
- **Production Resolution Required**: Would require access to KONE controller documentation.
- **Classification**: UNKNOWN

### U-003: KONE Alarm Severity Classification
- **Unknown**: How KONE internally classifies alarm severity levels and priority is not publicly documented.
- **Why It Matters**: Alert routing depends on correct prioritization.
- **Evidence Currently Available**: None (proprietary).
- **Impact Level**: MEDIUM
- **Temporary Prototype Assumption**: Prototype uses a simplified 3-tier severity model.
- **Production Resolution Required**: Would require KONE alarm management documentation.
- **Classification**: UNKNOWN

### U-004: Real-World Failure Rate Statistics
- **Unknown**: Real fleet failure statistics are needed to calculate prior probabilities.
- **Why It Matters**: Bayesian prior probabilities require accurate real-world frequencies.
- **Evidence Currently Available**: None (proprietary).
- **Impact Level**: HIGH
- **Temporary Prototype Assumption**: Prototype uses illustrative engineering-reasoned priors (e.g., mechanical_jam: 0.35).
- **Production Resolution Required**: Would require KONE CMMS data analysis.
- **Classification**: UNKNOWN

### U-005: KONE Controller Event Log Format
- **Unknown**: The exact format, fields, and encoding of KONE controller event logs is proprietary.
- **Why It Matters**: Need proper schema for event ingestion.
- **Evidence Currently Available**: None (proprietary).
- **Impact Level**: HIGH
- **Temporary Prototype Assumption**: Prototype defines a synthetic event schema.
- **Production Resolution Required**: Would require access to KONE DX Class controller specifications.
- **Classification**: UNKNOWN

### U-006: KONE Maintenance CMMS Platform
- **Unknown**: Whether KONE uses SAP PM, Maximo, ServiceNow, or a custom CMMS is not publicly confirmed.
- **Why It Matters**: Integration and closed-loop actions depend on CMMS capabilities.
- **Evidence Currently Available**: Unconfirmed.
- **Impact Level**: MEDIUM
- **Temporary Prototype Assumption**: Prototype defines a simple maintenance_record table.
- **Production Resolution Required**: Would require CMMS integration specifications.
- **Classification**: UNKNOWN

### U-007: Exact Sensor Sampling Rates
- **Unknown**: The specific sampling rates (Hz) for each telemetry parameter in KONE DX Class elevators.
- **Why It Matters**: Determines data volume, latency, and windowing configurations.
- **Evidence Currently Available**: None (proprietary hardware specs).
- **Impact Level**: MEDIUM
- **Temporary Prototype Assumption**: Prototype assumes reasonable engineering defaults (current: 1kHz, temperature: 1Hz, vibration: variable).
- **Production Resolution Required**: Would require hardware specifications.
- **Classification**: UNKNOWN

### U-008: KONE Edge Gateway Architecture
- **Unknown**: The exact firmware, protocols, and processing capabilities of KONE's edge IoT gateway.
- **Why It Matters**: Determines what logic can be pushed to the edge vs. cloud.
- **Evidence Currently Available**: None (proprietary).
- **Impact Level**: LOW
- **Temporary Prototype Assumption**: Prototype assumes direct telemetry availability.
- **Production Resolution Required**: Would require edge device documentation.
- **Classification**: UNKNOWN

### U-009: KONE Internal RCA Capabilities
- **Unknown**: Whether KONE internally has structured multi-hypothesis RCA capabilities not publicly documented.
- **Why It Matters**: Understanding the baseline helps position the value proposition.
- **Evidence Currently Available**: Absence of public evidence.
- **Impact Level**: LOW
- **Temporary Prototype Assumption**: Prototype positions based on absence of public evidence only. Must never claim "KONE has no RCA" — only "not publicly established".
- **Production Resolution Required**: Internal review of KONE intellectual property.
- **Classification**: UNKNOWN

### U-010: Corrective Action Procedures
- **Unknown**: Real KONE-specific maintenance procedures, parts numbers, and repair sequences.
- **Why It Matters**: The RCA tool should recommend actual KONE SOPs.
- **Evidence Currently Available**: None (proprietary service manuals).
- **Impact Level**: MEDIUM
- **Temporary Prototype Assumption**: Prototype uses generic engineering procedures from public sources.
- **Production Resolution Required**: Would require KONE service manual integration.
- **Classification**: UNKNOWN

### U-011: Real Door Cycle Timing Parameters
- **Unknown**: Exact normal door cycle time ranges, tolerances, and timeout thresholds for KONE doors.
- **Why It Matters**: Rule-based detection relies on accurate thresholds.
- **Evidence Currently Available**: None (proprietary hardware specs).
- **Impact Level**: HIGH
- **Temporary Prototype Assumption**: Prototype uses illustrative values (e.g., normal close: 3-5 seconds).
- **Production Resolution Required**: Would require door operator specifications.
- **Classification**: UNKNOWN

### U-012: Brake Air Gap Specifications
- **Unknown**: Exact brake air gap tolerances, release/engage timing specifications for KONE EcoDisc brakes.
- **Why It Matters**: Fault signatures for brake dragging or failures depend on these metrics.
- **Evidence Currently Available**: None (proprietary specs).
- **Impact Level**: HIGH
- **Temporary Prototype Assumption**: Prototype uses generic brake timing thresholds.
- **Production Resolution Required**: Would require brake specification documents.
- **Classification**: UNKNOWN

### U-013: Safety Chain Circuit Details
- **Unknown**: The exact configuration, contact count, and monitoring points of KONE safety chains.
- **Why It Matters**: Pinpointing the exact safety node that broke the chain.
- **Evidence Currently Available**: None (proprietary schematics).
- **Impact Level**: MEDIUM
- **Temporary Prototype Assumption**: Prototype treats safety chain as a binary open/closed signal.
- **Production Resolution Required**: Would require safety circuit schematics.
- **Classification**: UNKNOWN

### U-014: Production Deployment Topology
- **Unknown**: The exact cloud architecture, network topology, and security zones for production deployment.
- **Why It Matters**: System needs to conform to KONE IT security and networking standards.
- **Evidence Currently Available**: None.
- **Impact Level**: LOW
- **Temporary Prototype Assumption**: Prototype uses a single-machine Docker Compose deployment.
- **Production Resolution Required**: Would require enterprise architecture review.
- **Classification**: OPEN DECISION

### U-015: Real KONE Technician Workflow Integration
- **Unknown**: How KONE technicians currently receive and process diagnostic information in the field.
- **Why It Matters**: Front-end UX should mesh smoothly with their existing process.
- **Evidence Currently Available**: None.
- **Impact Level**: MEDIUM
- **Temporary Prototype Assumption**: Prototype provides a web-based technician interface.
- **Production Resolution Required**: Would require workflow analysis and mobile app integration.
- **Classification**: OPEN DECISION

### U-016: Safety Certification Requirements
- **Unknown**: Exact IEC 61508/PESSRAL certification requirements if the system were to be production-deployed.
- **Why It Matters**: Dictates rigor of development and verification testing for production.
- **Evidence Currently Available**: None.
- **Impact Level**: HIGH
- **Temporary Prototype Assumption**: Prototype explicitly stays outside safety-critical scope.
- **Production Resolution Required**: Would require safety certification assessment.
- **Classification**: OPEN DECISION

## Summary Impact Matrix

| Unknown ID | Impact Level | Affects MVP? | Prototype Mitigation | Production Blocker? |
| :--- | :--- | :--- | :--- | :--- |
| U-001 | HIGH | No | Synthetic telemetry contract | Yes |
| U-002 | HIGH | No | Generic fault categories | Yes |
| U-003 | MEDIUM | No | Simplified 3-tier severity | Yes |
| U-004 | HIGH | No | Illustrative engineering priors | Yes |
| U-005 | HIGH | No | Synthetic event schema | Yes |
| U-006 | MEDIUM | No | Simple maintenance_record table | Yes |
| U-007 | MEDIUM | No | Engineering defaults (e.g., 1kHz) | Yes |
| U-008 | LOW | No | Assume direct telemetry | No |
| U-009 | LOW | No | Position based on absence of evidence | No |
| U-010 | MEDIUM | No | Generic procedures | Yes |
| U-011 | HIGH | No | Illustrative values | Yes |
| U-012 | HIGH | No | Generic thresholds | Yes |
| U-013 | MEDIUM | No | Binary open/closed signal | Yes |
| U-014 | LOW | No | Docker Compose deployment | Yes |
| U-015 | MEDIUM | No | Web-based interface | Yes |
| U-016 | HIGH | No | Stays outside safety scope | Yes |
