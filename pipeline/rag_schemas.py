"""
ElevateRCA — RAG Data Schemas
Pydantic models for GUIDE corpus ingestion, retrieval, and evidence integration.
These schemas are ADDITIVE — they do not modify existing pipeline schemas.
"""

from typing import List, Optional, Dict, Any, Literal
from pydantic import BaseModel, Field


# =====================================================
# DOCUMENT AUTHORITY LEVELS (Section 8 of spec)
# =====================================================
AUTHORITY_LEVELS = {
    "OEM_REFERENCE": 1,       # Configuration-specific OEM documentation
    "COMPONENT_GUIDE": 2,     # Component/system documentation (door, brake, rope)
    "TROUBLESHOOTING": 3,     # Structured troubleshooting dataset
    "PROJECT_KNOWLEDGE": 4,   # YAML knowledge base files
    "GENERAL_KNOWLEDGE": 5,   # General LLM knowledge (lowest)
}


class DocumentMetadata(BaseModel):
    """Metadata for a GUIDE corpus document — tracks provenance, configuration, and authority."""
    document_id: str = Field(..., description="Unique document identifier")
    filename: str = Field(..., description="Original filename in GUIDE/")
    source_type: Literal["GUIDE"] = Field(default="GUIDE")
    authority: Literal[
        "OEM_REFERENCE", "COMPONENT_GUIDE", "TROUBLESHOOTING", "PROJECT_KNOWLEDGE", "GENERAL_KNOWLEDGE"
    ] = Field(..., description="Document authority level")
    manufacturer: str = Field(default="KONE")

    # Subsystem/Component targeting
    system: Optional[str] = Field(None, description="e.g., elevator, door, brake")
    subsystem: Optional[str] = Field(None, description="e.g., door, brake_traction, drive_motor")
    component: Optional[str] = Field(None, description="e.g., roller, photoeye, brake_pad")

    # Document classification
    document_type: Optional[str] = Field(None, description="e.g., maintenance_procedure, troubleshooting, OEM_spec")

    # Configuration targeting — CRITICAL for correct retrieval
    model: Optional[str] = Field(None, description="Elevator model if applicable")
    egov: Optional[str] = Field(None, description="EGOV setting: 8_9, A, B, D_E, F")
    espd: Optional[str] = Field(None, description="ESPD setting if applicable")
    configuration: Optional[str] = Field(None, description="Configuration identifier")

    # Procedure classification
    procedure_type: Optional[str] = Field(None, description="e.g., inspection, adjustment, replacement")
    fault_code: Optional[str] = Field(None, description="Linked fault code if applicable")

    # Document sections
    section: Optional[str] = Field(None)
    page: int = Field(default=0)

    # Revision tracking
    revision: Optional[str] = Field(None)
    issue_date: Optional[str] = Field(None)

    # Chunk tracking
    chunk_id: Optional[str] = Field(None)
    total_chunks: int = Field(default=0)


class RAGChunk(BaseModel):
    """A single chunk from an ingested GUIDE document with full provenance."""
    chunk_id: str = Field(..., description="Unique chunk identifier")
    text: str = Field(..., description="Chunk text content")
    document_id: str = Field(..., description="Parent document ID")
    filename: str = Field(..., description="Source filename")
    page: int = Field(default=0, description="Source page number (1-indexed, 0=unknown)")
    section: Optional[str] = Field(None, description="Section/heading if available")

    # Metadata for filtering
    source_type: str = Field(default="GUIDE")
    authority: str = Field(default="COMPONENT_GUIDE")
    subsystem: Optional[str] = Field(None)
    component: Optional[str] = Field(None)
    system: Optional[str] = Field(None)
    document_type: Optional[str] = Field(None)
    egov: Optional[str] = Field(None)
    configuration: Optional[str] = Field(None)
    manufacturer: str = Field(default="KONE")

    # For structured data (tables, specs)
    is_table: bool = Field(default=False)
    is_procedure: bool = Field(default=False)
    is_warning: bool = Field(default=False)


class RAGSource(BaseModel):
    """A retrieved RAG source attached to evidence — provides full traceability."""
    source: str = Field(..., description="Source document filename")
    page: int = Field(default=0, description="Page number")
    section: Optional[str] = Field(None, description="Section heading")
    chunk_id: str = Field(default="", description="Chunk identifier")
    authority: str = Field(default="COMPONENT_GUIDE", description="Authority level")
    relevance_score: float = Field(default=0.0, description="Retrieval relevance score")
    applicability: Literal["MATCHED", "CONDITIONAL", "CONFIGURATION_UNKNOWN", "NOT_APPLICABLE"] = Field(
        default="MATCHED", description="Configuration applicability status"
    )
    evidence_text: str = Field(default="", description="Retrieved text content")
    supports: List[str] = Field(default_factory=list, description="Hypothesis IDs this supports")
    contradicts: List[str] = Field(default_factory=list, description="Hypothesis IDs this contradicts")


class RAGEvidence(BaseModel):
    """Aggregated RAG evidence for a diagnostic investigation."""
    sources: List[RAGSource] = Field(default_factory=list)
    query_subsystem: Optional[str] = Field(None)
    query_component: Optional[str] = Field(None)
    query_fault_code: Optional[str] = Field(None)
    total_documents_searched: int = Field(default=0)
    configuration_filter_applied: bool = Field(default=False)
    retrieval_timestamp: Optional[str] = Field(None)


class TechnicianObservation(BaseModel):
    """Structured representation of technician free-text evidence (Section 25)."""
    type: Literal[
        "PHYSICAL_INSPECTION", "MEASUREMENT", "OPERATIONAL_TEST",
        "VISUAL_OBSERVATION", "OPINION", "UNSTRUCTURED"
    ] = Field(default="UNSTRUCTURED")
    component: Optional[str] = Field(None, description="Component referenced")
    finding: str = Field(..., description="What was found/observed")
    value: Optional[str] = Field(None, description="Measured value if applicable")
    unit: Optional[str] = Field(None, description="Unit of measurement")
    support_type: Literal["POSITIVE", "NEGATIVE", "NEUTRAL"] = Field(default="NEUTRAL")
    provenance: Literal["TECHNICIAN_REPORTED"] = Field(default="TECHNICIAN_REPORTED")
    confidence: Literal["HIGH", "MEDIUM", "LOW"] = Field(
        default="MEDIUM",
        description="HIGH for measurements, MEDIUM for observations, LOW for opinions"
    )


# =====================================================
# GUIDE DOCUMENT REGISTRY — maps filenames to metadata
# =====================================================
GUIDE_DOCUMENT_REGISTRY: Dict[str, Dict[str, Any]] = {
    "elevator_door_operations.pdf": {
        "authority": "COMPONENT_GUIDE",
        "system": "elevator",
        "subsystem": "door",
        "component": "door_system",
        "document_type": "operations_guide",
        "egov": None,
        "configuration": None,
    },
    "brake_of_geared_traction_machine.pdf": {
        "authority": "COMPONENT_GUIDE",
        "system": "elevator",
        "subsystem": "brake_traction",
        "component": "brake",
        "document_type": "technical_guide",
        "egov": None,
        "configuration": "geared_traction",
    },
    "brake_of_gearless_traction_machine.pdf": {
        "authority": "COMPONENT_GUIDE",
        "system": "elevator",
        "subsystem": "brake_traction",
        "component": "brake",
        "document_type": "technical_guide",
        "egov": None,
        "configuration": "gearless_traction",
    },
    "elevator_brake_pad.pdf": {
        "authority": "COMPONENT_GUIDE",
        "system": "elevator",
        "subsystem": "brake_traction",
        "component": "brake_pad",
        "document_type": "technical_guide",
        "egov": None,
        "configuration": None,
    },
    "elevator_hoisting_rope.pdf": {
        "authority": "COMPONENT_GUIDE",
        "system": "elevator",
        "subsystem": "brake_traction",
        "component": "hoisting_rope",
        "document_type": "technical_guide",
        "egov": None,
        "configuration": None,
    },
    "sets_egov_8_9.pdf": {
        "authority": "OEM_REFERENCE",
        "system": "elevator",
        "subsystem": "encoder_position",
        "component": "SETS",
        "document_type": "configuration_guide",
        "egov": "8_9",
        "configuration": "SETS_EGOV_8_9",
    },
    "sets_egov_a.pdf": {
        "authority": "OEM_REFERENCE",
        "system": "elevator",
        "subsystem": "encoder_position",
        "component": "SETS",
        "document_type": "configuration_guide",
        "egov": "A",
        "configuration": "SETS_EGOV_A",
    },
    "sets_egov_b.pdf": {
        "authority": "OEM_REFERENCE",
        "system": "elevator",
        "subsystem": "encoder_position",
        "component": "SETS",
        "document_type": "configuration_guide",
        "egov": "B",
        "configuration": "SETS_EGOV_B",
    },
    "sets_egov_d_e.pdf": {
        "authority": "OEM_REFERENCE",
        "system": "elevator",
        "subsystem": "encoder_position",
        "component": "SETS",
        "document_type": "configuration_guide",
        "egov": "D_E",
        "configuration": "SETS_EGOV_D_E",
    },
    "sets_egov_f.pdf": {
        "authority": "OEM_REFERENCE",
        "system": "elevator",
        "subsystem": "encoder_position",
        "component": "SETS",
        "document_type": "configuration_guide",
        "egov": "F",
        "configuration": "SETS_EGOV_F",
    },
    "sets-11.pdf": {
        "authority": "OEM_REFERENCE",
        "system": "elevator",
        "subsystem": "encoder_position",
        "component": "SETS",
        "document_type": "configuration_guide",
        "egov": None,
        "configuration": "SETS_11",
    },
    "kone guide maintainance procdure.pdf": {
        "authority": "OEM_REFERENCE",
        "system": "elevator",
        "subsystem": None,
        "component": None,
        "document_type": "maintenance_procedure",
        "egov": None,
        "configuration": None,
    },
    "OEM 1.pdf": {
        "authority": "OEM_REFERENCE",
        "system": "elevator",
        "subsystem": None,
        "component": None,
        "document_type": "OEM_spec",
        "egov": None,
        "configuration": None,
    },
    "elevator_troubleshooting_dataset.csv": {
        "authority": "TROUBLESHOOTING",
        "system": "elevator",
        "subsystem": None,
        "component": None,
        "document_type": "troubleshooting_dataset",
        "egov": None,
        "configuration": None,
    },
    "elevator_troubleshooting_dataset.json": {
        "authority": "TROUBLESHOOTING",
        "system": "elevator",
        "subsystem": None,
        "component": None,
        "document_type": "troubleshooting_dataset",
        "egov": None,
        "configuration": None,
    },
}
