"""
ElevateRCA - GUIDE Document Classifier and Metadata Rules
"""
from pathlib import Path
from typing import Dict, Any, Optional
from pipeline.models import DocumentType, AuthorityTier, DocumentMetadata


def classify_guide_file(filename: str) -> DocumentMetadata:
    """
    Classifies a GUIDE file into its authoritative document type, authority tier,
    subsystem, and configuration parameters per the Master Specification.
    """
    name_lower = filename.lower()
    
    # 1. SETS-01 Safety System Manuals (Configuration conditioned)
    if "sets_egov_8_9" in name_lower:
        return DocumentMetadata(
            document_id="DOC-SETS-EGOV-8-9",
            filename=filename,
            document_type=DocumentType.SAFETY_SYSTEM_MANUAL,
            authority=AuthorityTier.TIER_1,
            system="SETS-01",
            subsystem="Safety System",
            component="Electronic Governor",
            egov_setting="8_9",
            procedure_type="SAFETY_INSPECTION",
            title="SETS-01 Electronic Governor Inspection Manual (Settings 8 & 9)",
        )
    elif "sets_egov_a" in name_lower:
        return DocumentMetadata(
            document_id="DOC-SETS-EGOV-A",
            filename=filename,
            document_type=DocumentType.SAFETY_SYSTEM_MANUAL,
            authority=AuthorityTier.TIER_1,
            system="SETS-01",
            subsystem="Safety System",
            component="Electronic Governor",
            egov_setting="A",
            procedure_type="SAFETY_INSPECTION",
            title="SETS-01 Electronic Governor Inspection Manual (Setting A)",
        )
    elif "sets_egov_b" in name_lower:
        return DocumentMetadata(
            document_id="DOC-SETS-EGOV-B",
            filename=filename,
            document_type=DocumentType.SAFETY_SYSTEM_MANUAL,
            authority=AuthorityTier.TIER_1,
            system="SETS-01",
            subsystem="Safety System",
            component="Electronic Governor",
            egov_setting="B",
            procedure_type="SAFETY_INSPECTION",
            title="SETS-01 Electronic Governor Inspection Manual (Setting B)",
        )
    elif "sets_egov_d_e" in name_lower:
        return DocumentMetadata(
            document_id="DOC-SETS-EGOV-D-E",
            filename=filename,
            document_type=DocumentType.SAFETY_SYSTEM_MANUAL,
            authority=AuthorityTier.TIER_1,
            system="SETS-01",
            subsystem="Safety System",
            component="Electronic Governor",
            egov_setting="D_E",
            procedure_type="SAFETY_INSPECTION",
            title="SETS-01 Electronic Governor Inspection Manual (Settings D & E)",
        )
    elif "sets_egov_f" in name_lower:
        return DocumentMetadata(
            document_id="DOC-SETS-EGOV-F",
            filename=filename,
            document_type=DocumentType.SAFETY_SYSTEM_MANUAL,
            authority=AuthorityTier.TIER_1,
            system="SETS-01",
            subsystem="Safety System",
            component="Electronic Governor",
            egov_setting="F",
            procedure_type="SAFETY_INSPECTION",
            title="SETS-01 Electronic Governor Inspection Manual (Setting F)",
        )
    elif "sets-11" in name_lower:
        return DocumentMetadata(
            document_id="DOC-SETS-11",
            filename=filename,
            document_type=DocumentType.SAFETY_SYSTEM_MANUAL,
            authority=AuthorityTier.TIER_1,
            system="SETS-11",
            subsystem="Safety System",
            component="Digital Safety Bus",
            configuration="SETS-11 Architecture",
            procedure_type="SAFETY_INSPECTION",
            title="SETS-11 Advanced Safety System Maintenance Manual",
        )

    # 2. OEM Maintenance Procedures & References
    elif "kone guide maintainance" in name_lower or "kone guide maintanance" in name_lower:
        return DocumentMetadata(
            document_id="DOC-OEM-KONE-MAINT",
            filename=filename,
            document_type=DocumentType.MAINTENANCE_MANUAL,
            authority=AuthorityTier.TIER_1,
            manufacturer="KONE",
            system="Elevator Fleet",
            subsystem="General",
            procedure_type="PREVENTATIVE_MAINTENANCE",
            title="KONE General Maintenance & Safety Inspection Guide",
        )
    elif "oem 1" in name_lower:
        return DocumentMetadata(
            document_id="DOC-OEM-REF-1",
            filename=filename,
            document_type=DocumentType.OEM_REFERENCE,
            authority=AuthorityTier.TIER_1,
            manufacturer="OEM Standard",
            system="Controller & Drive",
            subsystem="Controller",
            procedure_type="DIAGNOSTIC_REFERENCE",
            title="OEM Standard Controller Diagnostic & Fault Code Reference",
        )

    # 3. Component & System Guides (Tier 2)
    elif "door_operations" in name_lower:
        return DocumentMetadata(
            document_id="DOC-DOOR-OPS",
            filename=filename,
            document_type=DocumentType.DOOR_SYSTEM_GUIDE,
            authority=AuthorityTier.TIER_2,
            system="Door Operator",
            subsystem="Door",
            component="Door Operator & Interlocks",
            procedure_type="ADJUSTMENT_AND_REPAIR",
            title="Elevator Door Operations & Kinematics Guide",
        )
    elif "gearless_traction_machine" in name_lower:
        return DocumentMetadata(
            document_id="DOC-BRAKE-GEARLESS",
            filename=filename,
            document_type=DocumentType.BRAKE_SYSTEM_GUIDE,
            authority=AuthorityTier.TIER_2,
            system="Traction Machine",
            subsystem="Brake",
            component="Gearless Electromagnetic Brake",
            configuration="Gearless PMSM (EcoDisc)",
            procedure_type="BRAKE_MAINTENANCE",
            title="Brake Maintenance for Gearless Traction Machines",
        )
    elif "geared_traction_machine" in name_lower:
        return DocumentMetadata(
            document_id="DOC-BRAKE-GEARED",
            filename=filename,
            document_type=DocumentType.BRAKE_SYSTEM_GUIDE,
            authority=AuthorityTier.TIER_2,
            system="Traction Machine",
            subsystem="Brake",
            component="Geared Traction Machine Brake",
            configuration="Geared Traction",
            procedure_type="BRAKE_MAINTENANCE",
            title="Brake Maintenance for Geared Traction Machines",
        )
    elif "brake_pad" in name_lower:
        return DocumentMetadata(
            document_id="DOC-BRAKE-PAD",
            filename=filename,
            document_type=DocumentType.COMPONENT_GUIDE,
            authority=AuthorityTier.TIER_2,
            system="Brake Assembly",
            subsystem="Brake",
            component="Brake Pad / Lining",
            procedure_type="WEAR_INSPECTION",
            title="Elevator Brake Pad & Lining Wear Limits",
        )
    elif "hoisting_rope" in name_lower:
        return DocumentMetadata(
            document_id="DOC-HOISTING-ROPE",
            filename=filename,
            document_type=DocumentType.HOISTING_SYSTEM_GUIDE,
            authority=AuthorityTier.TIER_2,
            system="Suspension",
            subsystem="Hoisting",
            component="Hoisting Ropes",
            procedure_type="ROPE_DISCARD_INSPECTION",
            title="Elevator Hoisting Rope Wear & Tension Inspection",
        )

    # 4. Troubleshooting Datasets (Tier 3)
    elif "elevator_troubleshooting_dataset" in name_lower:
        return DocumentMetadata(
            document_id="DOC-TROUBLESHOOTING-DS",
            filename=filename,
            document_type=DocumentType.TROUBLESHOOTING_DATASET,
            authority=AuthorityTier.TIER_3,
            system="Multi-System",
            subsystem="Multi-Subsystem",
            title="Standard Elevator Troubleshooting Dataset (15 Canonical Scenarios)",
        )

    # Default fallback
    return DocumentMetadata(
        document_id=f"DOC-{filename.upper()[:12]}",
        filename=filename,
        document_type=DocumentType.COMPONENT_GUIDE,
        authority=AuthorityTier.TIER_4,
        title=filename,
    )
