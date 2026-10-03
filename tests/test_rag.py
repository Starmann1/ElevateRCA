"""
Unit & Integration Tests for GUIDE RAG Pipeline
"""
import pytest
from pathlib import Path

from pipeline.models import (
    DocumentType,
    AuthorityTier,
    ElevatorConfiguration,
)
from pipeline.rag.classifier import classify_guide_file
from pipeline.rag.parser import parse_troubleshooting_dataset, parse_pdf_document
from pipeline.rag.store import GuideKnowledgeStore
from pipeline.rag.retriever import EvidenceRetriever


def test_guide_file_classification():
    # SETS-01 specific manual classification
    meta_a = classify_guide_file("sets_egov_a.pdf")
    assert meta_a.document_type == DocumentType.SAFETY_SYSTEM_MANUAL
    assert meta_a.authority == AuthorityTier.TIER_1
    assert meta_a.egov_setting == "A"

    meta_8_9 = classify_guide_file("sets_egov_8_9.pdf")
    assert meta_8_9.egov_setting == "8_9"

    # Component guides
    meta_door = classify_guide_file("elevator_door_operations.pdf")
    assert meta_door.document_type == DocumentType.DOOR_SYSTEM_GUIDE
    assert meta_door.authority == AuthorityTier.TIER_2

    # OEM maintenance
    meta_kone = classify_guide_file("kone guide maintainance procdure.pdf")
    assert meta_kone.authority == AuthorityTier.TIER_1
    assert meta_kone.document_type == DocumentType.MAINTENANCE_MANUAL


def test_troubleshooting_dataset_parsing(guide_path):
    csv_file = guide_path / "elevator_troubleshooting_dataset.csv"
    assert csv_file.exists()
    
    chunks = parse_troubleshooting_dataset(csv_file)
    assert len(chunks) == 15
    
    # Check ELV-005 (Door System)
    door_chunk = next(c for c in chunks if "ELV-005" in c.chunk_id)
    assert "Door operator issue" in door_chunk.content
    assert door_chunk.metadata.authority == AuthorityTier.TIER_3
    assert door_chunk.metadata.component == "Door System"


def test_rag_ingestion_and_retrieval(guide_path, tmp_path):
    # Use temporary Chroma storage directory
    store = GuideKnowledgeStore(persist_dir=str(tmp_path / "chroma_test"))
    stats = store.ingest_guide_directory(guide_path, force_reload=True)
    
    assert stats["total_files"] >= 15
    assert stats["total_chunks"] > 50
    assert stats["table_chunks"] > 0
    
    retriever = EvidenceRetriever(store)
    
    # Test 1: Door Query with Gearless Configuration
    cfg_gearless = ElevatorConfiguration(machine_type="Gearless Traction (EcoDisc)", egov="A")
    res_door = retriever.retrieve("door skate roller clearance", subsystem="Door", configuration=cfg_gearless)
    
    assert len(res_door["retrieved_evidence"]) > 0
    top_source = res_door["retrieved_evidence"][0]["source"]
    assert "door" in top_source.lower() or "troubleshooting" in top_source.lower()

    # Test 2: Configuration Applicability Isolation (EGOV=A must not retrieve EGOV=F or 8_9)
    res_sets = retriever.retrieve("governor reference position calibration", configuration=cfg_gearless)
    for ev in res_sets["retrieved_evidence"]:
        src = ev["source"].lower()
        if "sets_egov" in src:
            assert "egov_a" in src, f"Inapplicable SETS manual retrieved: {src}"

    # Test 3: Unknown Configuration Gatekeeper
    cfg_unknown = ElevatorConfiguration(egov=None)
    res_unknown = retriever.retrieve("SETS trip setting", configuration=cfg_unknown)
    assert "unknown" in res_unknown["configuration_status"].lower()
