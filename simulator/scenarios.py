"""
ElevateRCA Canonical Scenarios Generator (Part 6)
Builds standardized test payloads matching KONE software output for all 5 canonical scenarios
plus the Scenario 6 Abstention Benchmark.
"""

from datetime import datetime, timezone
from typing import Dict, Any
from pipeline.schemas import KONEFaultInput, AlarmInput, TelemetryInput, MaintenanceRecordInput


class ScenarioFactory:
    """Creates ground-truth KONE software output payloads for benchmarking and demonstrations."""

    @staticmethod
    def scenario_1_igbt_overcurrent(elevator_id: str = "KONE-MONO-501") -> KONEFaultInput:
        """Scenario 1: IGBT Inverter Power Electronics Breakdown."""
        ts = "2026-09-24T10:14:22.100Z"
        return KONEFaultInput(
            elevator_id=elevator_id,
            timestamp_utc=ts,
            operating_state="ACCELERATING",
            elevator_model="KONE MonoSpace 500 (EcoDisc MX10)",
            installation_age_years=3.2,
            alarms=[
                AlarmInput(
                    alarm_code="motor_overcurrent",
                    alarm_type="motor_overcurrent",
                    severity="critical",
                    subsystem="drive_motor",
                    timestamp="2026-09-24T10:14:22.100Z",
                    state="ACTIVE"
                ),
                AlarmInput(
                    alarm_code="drive_trip",
                    alarm_type="drive_trip",
                    severity="critical",
                    subsystem="drive_motor",
                    timestamp="2026-09-24T10:14:22.450Z",
                    state="ACTIVE"
                ),
                AlarmInput(
                    alarm_code="safety_chain_trip",
                    alarm_type="safety_chain_trip",
                    severity="critical",
                    subsystem="safety_chain",
                    timestamp="2026-09-24T10:14:23.000Z",
                    state="ACTIVE"
                )
            ],
            telemetry=[
                TelemetryInput(signal_name="motor_current_rms", value=28.4, unit="A", quality="good", timestamp=ts, baseline_value=12.0, deviation_pct=136.7),
                TelemetryInput(signal_name="igbt_temp", value=78.5, unit="°C", quality="good", timestamp=ts, baseline_value=45.0, deviation_pct=74.4),
                TelemetryInput(signal_name="vibration_rms", value=0.07, unit="m/s2", quality="good", timestamp=ts, baseline_value=0.08, deviation_pct=-12.5),
                TelemetryInput(signal_name="motor_temp", value=48.0, unit="°C", quality="good", timestamp=ts, baseline_value=50.0, deviation_pct=-4.0),
                TelemetryInput(signal_name="brake_release_delay", value=145.0, unit="ms", quality="good", timestamp=ts, baseline_value=150.0, deviation_pct=-3.3)
            ],
            maintenance_history=[
                MaintenanceRecordInput(
                    date="2026-06-12T09:00:00Z",
                    component="EcoDisc Motor",
                    action="Routine 3-year mechanical inspection",
                    technician_notes="Motor bearings nominal, shaft play 0.02mm within tolerance",
                    part_replaced=False
                )
            ],
            technician_free_text="Car stopped suddenly during upward acceleration from Floor 2. Drive self-test FAILED with internal inverter bridge fault code."
        )

    @staticmethod
    def scenario_2_mechanical_jam(elevator_id: str = "KONE-MONO-502") -> KONEFaultInput:
        """Scenario 2: Hoistway / Guide Rail Mechanical Obstruction."""
        ts = "2026-09-24T11:05:10.000Z"
        return KONEFaultInput(
            elevator_id=elevator_id,
            timestamp_utc=ts,
            operating_state="CONSTANT_SPEED",
            elevator_model="KONE MonoSpace 700",
            installation_age_years=5.1,
            alarms=[
                AlarmInput(
                    alarm_code="motor_overcurrent",
                    alarm_type="motor_overcurrent",
                    severity="critical",
                    subsystem="drive_motor",
                    timestamp="2026-09-24T11:05:10.000Z",
                    state="ACTIVE"
                ),
                AlarmInput(
                    alarm_code="drive_trip",
                    alarm_type="drive_trip",
                    severity="critical",
                    subsystem="drive_motor",
                    timestamp="2026-09-24T11:05:10.600Z",
                    state="ACTIVE"
                ),
                AlarmInput(
                    alarm_code="leveling_fault",
                    alarm_type="leveling_deviation",
                    severity="warning",
                    subsystem="encoder_position",
                    timestamp="2026-09-24T11:05:12.100Z",
                    state="ACTIVE"
                )
            ],
            telemetry=[
                TelemetryInput(signal_name="motor_current_rms", value=22.8, unit="A", quality="good", timestamp=ts, baseline_value=12.0, deviation_pct=90.0),
                TelemetryInput(signal_name="vibration_rms", value=0.28, unit="m/s2", quality="good", timestamp=ts, baseline_value=0.08, deviation_pct=250.0),
                TelemetryInput(signal_name="motor_temp", value=68.0, unit="°C", quality="good", timestamp=ts, baseline_value=50.0, deviation_pct=36.0),
                TelemetryInput(signal_name="igbt_temp", value=49.0, unit="°C", quality="good", timestamp=ts, baseline_value=45.0, deviation_pct=8.8),
                TelemetryInput(signal_name="brake_release_delay", value=152.0, unit="ms", quality="good", timestamp=ts, baseline_value=150.0, deviation_pct=1.3)
            ],
            maintenance_history=[],
            technician_free_text="Car shuddered mid-shaft between floors 4 and 5 before stopping. Drive self-test PASSED, drive healthy internally."
        )

    @staticmethod
    def scenario_3_door_photoeye_drift(elevator_id: str = "KONE-MINI-301") -> KONEFaultInput:
        """Scenario 3: Door 3D Light Curtain Optical Degradation / Reopen Drift."""
        ts = "2026-09-24T11:42:00.000Z"
        return KONEFaultInput(
            elevator_id=elevator_id,
            timestamp_utc=ts,
            operating_state="DOOR_CLOSE",
            elevator_model="KONE MiniSpace",
            installation_age_years=6.0,
            alarms=[
                AlarmInput(
                    alarm_code="door_obstruction_detected",
                    alarm_type="door_obstruction_detected",
                    severity="warning",
                    subsystem="door",
                    timestamp="2026-09-24T11:41:50.000Z",
                    state="ACTIVE"
                ),
                AlarmInput(
                    alarm_code="door_close_timeout",
                    alarm_type="door_close_timeout",
                    severity="critical",
                    subsystem="door",
                    timestamp="2026-09-24T11:42:00.000Z",
                    state="ACTIVE"
                ),
                AlarmInput(
                    alarm_code="door_reopen_count_exceeded",
                    alarm_type="door_reopen_count_exceeded",
                    severity="warning",
                    subsystem="door",
                    timestamp="2026-09-24T11:42:02.000Z",
                    state="ACTIVE"
                )
            ],
            telemetry=[
                TelemetryInput(signal_name="door_cycle_time_ms", value=4450.0, unit="ms", quality="good", timestamp=ts, baseline_value=2800.0, deviation_pct=58.9),
                TelemetryInput(signal_name="door_motor_current", value=1.6, unit="A", quality="good", timestamp=ts, baseline_value=1.5, deviation_pct=6.7)
            ],
            maintenance_history=[
                MaintenanceRecordInput(
                    date="2026-08-01T10:00:00Z",
                    component="Door Track",
                    action="Track cleaning and sill debris removal",
                    technician_notes="Sill cleared, door motion tested smoothly",
                    part_replaced=False
                )
            ],
            technician_free_text="Doors cycling multiple times on ground floor without passenger in doorway. Reopening occurs at random varying door positions, photo-eye signal erratic."
        )

    @staticmethod
    def scenario_4_encoder_fault(elevator_id: str = "KONE-MONO-504") -> KONEFaultInput:
        """Scenario 4: EcoDisc Motor Optical Encoder Pulse Loss / Leveling Drift."""
        ts = "2026-09-24T12:01:15.000Z"
        return KONEFaultInput(
            elevator_id=elevator_id,
            timestamp_utc=ts,
            operating_state="DECELERATING",
            elevator_model="KONE MonoSpace 500",
            installation_age_years=2.8,
            alarms=[
                AlarmInput(
                    alarm_code="leveling_deviation",
                    alarm_type="leveling_deviation",
                    severity="warning",
                    subsystem="encoder_position",
                    timestamp="2026-09-24T12:01:15.000Z",
                    state="ACTIVE"
                ),
                AlarmInput(
                    alarm_code="encoder_fault",
                    alarm_type="encoder_fault",
                    severity="critical",
                    subsystem="encoder_position",
                    timestamp="2026-09-24T12:01:16.200Z",
                    state="ACTIVE"
                ),
                AlarmInput(
                    alarm_code="position_mismatch",
                    alarm_type="position_mismatch",
                    severity="warning",
                    subsystem="encoder_position",
                    timestamp="2026-09-24T12:01:17.000Z",
                    state="ACTIVE"
                )
            ],
            telemetry=[
                TelemetryInput(signal_name="position_actual_divergence", value=6.8, unit="mm", quality="good", timestamp=ts, baseline_value=1.0, deviation_pct=580.0),
                TelemetryInput(signal_name="leveling_deviation_mm", value=8.5, unit="mm", quality="good", timestamp=ts, baseline_value=2.0, deviation_pct=325.0),
                TelemetryInput(signal_name="speed_feedback_deviation", value=14.2, unit="rpm", quality="good", timestamp=ts, baseline_value=5.0, deviation_pct=184.0),
                TelemetryInput(signal_name="motor_current_rms", value=13.1, unit="A", quality="good", timestamp=ts, baseline_value=12.0, deviation_pct=9.2)
            ],
            maintenance_history=[],
            technician_free_text="Car stopped 8.5mm above floor sill. Independent optical floor leveling sensor reports car is in exact correct floor zone, encoder count drifted."
        )

    @staticmethod
    def scenario_5_brake_drag_timing(elevator_id: str = "KONE-MONO-505") -> KONEFaultInput:
        """Scenario 5: EcoDisc Brake Release Timing Delay / Pad Drag."""
        ts = "2026-09-24T12:15:30.000Z"
        return KONEFaultInput(
            elevator_id=elevator_id,
            timestamp_utc=ts,
            operating_state="ACCELERATING",
            elevator_model="KONE MonoSpace 500",
            installation_age_years=4.0,
            alarms=[
                AlarmInput(
                    alarm_code="brake_fault",
                    alarm_type="brake_fault",
                    severity="critical",
                    subsystem="brake_traction",
                    timestamp="2026-09-24T12:15:30.000Z",
                    state="ACTIVE"
                ),
                AlarmInput(
                    alarm_code="brake_timing_violation",
                    alarm_type="brake_timing_violation",
                    severity="critical",
                    subsystem="brake_traction",
                    timestamp="2026-09-24T12:15:30.350Z",
                    state="ACTIVE"
                ),
                AlarmInput(
                    alarm_code="position_drift",
                    alarm_type="position_drift",
                    severity="warning",
                    subsystem="brake_traction",
                    timestamp="2026-09-24T12:15:31.000Z",
                    state="ACTIVE"
                )
            ],
            telemetry=[
                TelemetryInput(signal_name="brake_release_delay", value=360.0, unit="ms", quality="good", timestamp=ts, baseline_value=150.0, deviation_pct=140.0),
                TelemetryInput(signal_name="position_drift_mm", value=4.2, unit="mm", quality="good", timestamp=ts, baseline_value=0.5, deviation_pct=740.0),
                TelemetryInput(signal_name="motor_current_rms", value=13.0, unit="A", quality="good", timestamp=ts, baseline_value=12.0, deviation_pct=8.3),
                TelemetryInput(signal_name="igbt_temp", value=44.0, unit="°C", quality="good", timestamp=ts, baseline_value=45.0, deviation_pct=-2.2)
            ],
            maintenance_history=[],
            technician_free_text="Brake release lag detected. Motor torque demand was normal for load; electrical drive diagnostics report zero inverter faults."
        )

    @staticmethod
    def scenario_6_abstention_conflicting(elevator_id: str = "KONE-MONO-506") -> KONEFaultInput:
        """Scenario 6: Conflicting & Degraded Signals Triggering Principled Abstention."""
        ts = "2026-09-24T12:30:00.000Z"
        return KONEFaultInput(
            elevator_id=elevator_id,
            timestamp_utc=ts,
            operating_state="CONSTANT_SPEED",
            elevator_model="KONE MonoSpace 500",
            installation_age_years=7.0,
            alarms=[
                AlarmInput(
                    alarm_code="motor_overcurrent",
                    alarm_type="motor_overcurrent",
                    severity="warning",
                    subsystem="drive_motor",
                    timestamp="2026-09-24T12:30:00.000Z",
                    state="ACTIVE"
                )
            ],
            telemetry=[
                TelemetryInput(signal_name="motor_current_rms", value=14.5, unit="A", quality="good", timestamp=ts, baseline_value=12.0, deviation_pct=20.8),
                TelemetryInput(signal_name="igbt_temp", value=0.0, unit="°C", quality="bad", timestamp=ts, baseline_value=45.0, deviation_pct=0.0),
                TelemetryInput(signal_name="vibration_rms", value=0.08, unit="m/s2", quality="good", timestamp=ts, baseline_value=0.08, deviation_pct=0.0),
                TelemetryInput(signal_name="brake_release_delay", value=150.0, unit="ms", quality="good", timestamp=ts, baseline_value=150.0, deviation_pct=0.0),
                TelemetryInput(signal_name="motor_temp", value=0.0, unit="°C", quality="missing", timestamp=ts, baseline_value=50.0, deviation_pct=0.0)
            ],
            maintenance_history=[],
            technician_free_text="Slight overcurrent with normal vibration and normal brake delay. Drive self-test PASSED. Temperature sensors malfunctioning."
        )
