"""
ElevateRCA — GUIDE Corpus Ingestion Pipeline
Discovers, parses, and chunks GUIDE/ documents with full metadata and provenance.
Supports PDF (PyMuPDF), CSV, and JSON document types.
"""

import os
import re
import csv
import json
import hashlib
import logging
from typing import List, Dict, Any, Optional, Tuple

from pipeline.rag_schemas import (
    RAGChunk, DocumentMetadata, GUIDE_DOCUMENT_REGISTRY
)

logger = logging.getLogger("elevaterca.rag.ingest")


# =====================================================
# PDF PARSER — Extracts text with page/section awareness
# =====================================================

class PDFParser:
    """Parses PDF documents using PyMuPDF with page and section preservation."""

    @staticmethod
    def parse(filepath: str, filename: str) -> List[Dict[str, Any]]:
        """Parse a PDF file and return list of page-based text blocks with metadata."""
        try:
            import fitz  # PyMuPDF
        except ImportError:
            logger.warning("PyMuPDF (fitz) not available. PDF parsing disabled.")
            return []

        pages: List[Dict[str, Any]] = []
        try:
            doc = fitz.open(filepath)
            for page_num in range(len(doc)):
                page = doc[page_num]
                text = page.get_text("text")
                if text.strip():
                    # Extract tables as structured blocks
                    tables = PDFParser._extract_tables(page)
                    pages.append({
                        "page": page_num + 1,
                        "text": text.strip(),
                        "tables": tables,
                        "filename": filename,
                    })
            doc.close()
        except Exception as e:
            logger.error(f"Error parsing PDF {filepath}: {e}")
        return pages

    @staticmethod
    def _extract_tables(page) -> List[Dict[str, Any]]:
        """Extract tables from a PDF page if PyMuPDF supports it."""
        tables = []
        try:
            # PyMuPDF 1.23+ supports find_tables
            tab_finder = page.find_tables()
            if tab_finder and tab_finder.tables:
                for tab in tab_finder.tables:
                    table_data = tab.extract()
                    if table_data and len(table_data) > 1:
                        headers = table_data[0] if table_data[0] else []
                        rows = table_data[1:]
                        tables.append({
                            "headers": headers,
                            "rows": rows,
                            "text": PDFParser._table_to_text(headers, rows)
                        })
        except (AttributeError, Exception):
            # Table extraction not supported or failed — that's okay
            pass
        return tables


    @staticmethod
    def _table_to_text(headers: List, rows: List[List]) -> str:
        """Convert table data to readable text preserving structure."""
        lines = []
        if headers:
            clean_headers = [str(h).strip() if h else "" for h in headers]
            lines.append(" | ".join(clean_headers))
            lines.append("-" * 40)
        for row in rows:
            clean_row = [str(cell).strip() if cell else "" for cell in row]
            if any(clean_row):
                lines.append(" | ".join(clean_row))
        return "\n".join(lines)


# =====================================================
# SECTION DETECTOR — Identifies headings and sections
# =====================================================

class SectionDetector:
    """Detects section headings and classifies content types."""

    # Patterns for section headings
    HEADING_PATTERNS = [
        r"^\d+\.\d*\s+[A-Z]",          # "1.2 Section Title"
        r"^[A-Z][A-Z\s]{4,}$",          # "ALL CAPS HEADING"
        r"^Chapter\s+\d+",              # "Chapter 1"
        r"^Section\s+\d+",              # "Section 1"
        r"^SECTION\s+\d+",
        r"^\d+\)\s+[A-Z]",              # "1) Title"
    ]

    WARNING_KEYWORDS = [
        "WARNING", "CAUTION", "DANGER", "IMPORTANT",
        "DO NOT", "NEVER", "MUST NOT", "PROHIBITED"
    ]

    PROCEDURE_KEYWORDS = [
        "step", "procedure", "instruction", "check", "inspect",
        "verify", "measure", "adjust", "replace", "install",
        "remove", "disconnect", "connect"
    ]

    @staticmethod
    def detect_section(text: str) -> Optional[str]:
        """Extract section heading from text block."""
        first_line = text.split("\n")[0].strip()
        for pattern in SectionDetector.HEADING_PATTERNS:
            if re.match(pattern, first_line):
                return first_line[:100]
        return None

    @staticmethod
    def is_warning(text: str) -> bool:
        upper = text.upper()
        return any(kw in upper for kw in SectionDetector.WARNING_KEYWORDS)

    @staticmethod
    def is_procedure(text: str) -> bool:
        lower = text.lower()
        procedure_count = sum(1 for kw in SectionDetector.PROCEDURE_KEYWORDS if kw in lower)
        return procedure_count >= 2

    @staticmethod
    def contains_table_data(text: str) -> bool:
        """Heuristic: text contains tabular data (pipes, aligned columns, or numeric specs)."""
        lines = text.strip().split("\n")
        pipe_lines = sum(1 for l in lines if "|" in l)
        return pipe_lines >= 2


# =====================================================
# SEMANTIC CHUNKER — Splits text into meaningful chunks
# =====================================================

class SemanticChunker:
    """Chunks text content with section/page awareness, preserving context."""

    def __init__(self, max_chunk_size: int = 800, overlap: int = 100):
        self.max_chunk_size = max_chunk_size
        self.overlap = overlap

    def chunk_page_text(
        self,
        text: str,
        filename: str,
        page: int,
        document_meta: Dict[str, Any]
    ) -> List[RAGChunk]:
        """Chunk a single page of text into RAGChunks with metadata."""
        chunks: List[RAGChunk] = []

        # Split by paragraphs (double newline)
        paragraphs = re.split(r"\n\s*\n", text)

        current_section = None
        current_chunk_text = ""
        chunk_idx = 0

        for para in paragraphs:
            para = para.strip()
            if not para:
                continue

            # Check if this is a section heading
            detected = SectionDetector.detect_section(para)
            if detected:
                current_section = detected

            # If adding this paragraph exceeds max size, flush current chunk
            if current_chunk_text and len(current_chunk_text) + len(para) > self.max_chunk_size:
                chunk = self._create_chunk(
                    text=current_chunk_text,
                    filename=filename,
                    page=page,
                    section=current_section,
                    chunk_idx=chunk_idx,
                    document_meta=document_meta
                )
                chunks.append(chunk)
                chunk_idx += 1

                # Keep overlap
                words = current_chunk_text.split()
                overlap_words = words[-self.overlap // 5:] if len(words) > self.overlap // 5 else []
                current_chunk_text = " ".join(overlap_words) + "\n\n" if overlap_words else ""

            current_chunk_text += para + "\n\n"

        # Flush remaining
        if current_chunk_text.strip():
            chunk = self._create_chunk(
                text=current_chunk_text.strip(),
                filename=filename,
                page=page,
                section=current_section,
                chunk_idx=chunk_idx,
                document_meta=document_meta
            )
            chunks.append(chunk)

        return chunks

    def chunk_table(
        self,
        table_text: str,
        filename: str,
        page: int,
        document_meta: Dict[str, Any],
        chunk_idx: int
    ) -> RAGChunk:
        """Create a chunk specifically for table data."""
        return self._create_chunk(
            text=table_text,
            filename=filename,
            page=page,
            section="Table Data",
            chunk_idx=chunk_idx,
            document_meta=document_meta,
            is_table=True
        )

    def _create_chunk(
        self,
        text: str,
        filename: str,
        page: int,
        section: Optional[str],
        chunk_idx: int,
        document_meta: Dict[str, Any],
        is_table: bool = False
    ) -> RAGChunk:
        """Create a RAGChunk with full metadata."""
        doc_id = document_meta.get("document_id", filename)
        chunk_id = f"{doc_id}_p{page}_c{chunk_idx}"

        return RAGChunk(
            chunk_id=chunk_id,
            text=text,
            document_id=doc_id,
            filename=filename,
            page=page,
            section=section,
            source_type="GUIDE",
            authority=document_meta.get("authority", "COMPONENT_GUIDE"),
            subsystem=document_meta.get("subsystem"),
            component=document_meta.get("component"),
            system=document_meta.get("system", "elevator"),
            document_type=document_meta.get("document_type"),
            egov=document_meta.get("egov"),
            configuration=document_meta.get("configuration"),
            is_table=is_table,
            is_procedure=SectionDetector.is_procedure(text),
            is_warning=SectionDetector.is_warning(text),
        )


# =====================================================
# CSV/JSON PARSER — Troubleshooting dataset
# =====================================================

class TroubleshootingParser:
    """Parses the elevator troubleshooting CSV and JSON datasets."""

    @staticmethod
    def parse_csv(filepath: str) -> List[RAGChunk]:
        """Parse troubleshooting CSV into searchable chunks."""
        chunks: List[RAGChunk] = []
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for idx, row in enumerate(reader):
                    text = TroubleshootingParser._row_to_text(row)
                    doc_id = f"troubleshooting_csv_{row.get('id', idx)}"

                    # Map component to subsystem
                    subsystem = TroubleshootingParser._map_component_to_subsystem(
                        row.get("component", ""), row.get("root_cause_category", "")
                    )

                    chunks.append(RAGChunk(
                        chunk_id=doc_id,
                        text=text,
                        document_id="elevator_troubleshooting_dataset.csv",
                        filename="elevator_troubleshooting_dataset.csv",
                        page=0,
                        section=f"Troubleshooting: {row.get('component', 'Unknown')}",
                        source_type="GUIDE",
                        authority="TROUBLESHOOTING",
                        subsystem=subsystem,
                        component=row.get("component"),
                        system="elevator",
                        document_type="troubleshooting_dataset",
                        is_procedure=True,
                    ))
        except Exception as e:
            logger.error(f"Error parsing CSV {filepath}: {e}")
        return chunks

    @staticmethod
    def parse_json(filepath: str) -> List[RAGChunk]:
        """Parse troubleshooting JSON into searchable chunks."""
        chunks: List[RAGChunk] = []
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                records = json.load(f)

            for idx, row in enumerate(records):
                text = TroubleshootingParser._row_to_text(row)
                doc_id = f"troubleshooting_json_{row.get('id', idx)}"

                subsystem = TroubleshootingParser._map_component_to_subsystem(
                    row.get("component", ""), row.get("root_cause_category", "")
                )

                chunks.append(RAGChunk(
                    chunk_id=doc_id,
                    text=text,
                    document_id="elevator_troubleshooting_dataset.json",
                    filename="elevator_troubleshooting_dataset.json",
                    page=0,
                    section=f"Troubleshooting: {row.get('component', 'Unknown')}",
                    source_type="GUIDE",
                    authority="TROUBLESHOOTING",
                    subsystem=subsystem,
                    component=row.get("component"),
                    system="elevator",
                    document_type="troubleshooting_dataset",
                    is_procedure=True,
                ))
        except Exception as e:
            logger.error(f"Error parsing JSON {filepath}: {e}")
        return chunks

    @staticmethod
    def _row_to_text(row: Dict[str, Any]) -> str:
        """Convert a troubleshooting record to searchable text."""
        parts = []
        if row.get("component"):
            parts.append(f"Component: {row['component']}")
        if row.get("symptom"):
            parts.append(f"Symptom: {row['symptom']}")
        if row.get("alarm"):
            parts.append(f"Alarm: {row['alarm']}")
        if row.get("evidence"):
            parts.append(f"Evidence: {row['evidence']}")
        if row.get("possible_causes"):
            parts.append(f"Possible Causes: {row['possible_causes']}")
        if row.get("maintenance_check"):
            parts.append(f"Maintenance Check: {row['maintenance_check']}")
        if row.get("recommended_action"):
            parts.append(f"Recommended Action: {row['recommended_action']}")
        if row.get("priority"):
            parts.append(f"Priority: {row['priority']}")
        if row.get("root_cause_category"):
            parts.append(f"Root Cause Category: {row['root_cause_category']}")
        return "\n".join(parts)

    @staticmethod
    def _map_component_to_subsystem(component: str, category: str) -> Optional[str]:
        """Map troubleshooting component/category to pipeline subsystem."""
        comp_lower = component.lower()
        cat_lower = category.lower()

        if "door" in comp_lower or "door" in cat_lower:
            return "door"
        if "brake" in comp_lower or "brake" in cat_lower:
            return "brake_traction"
        if any(w in comp_lower for w in ["traction", "rope", "hoist"]):
            return "brake_traction"
        if any(w in comp_lower for w in ["motor", "drive", "inverter", "controller"]):
            return "drive_motor"
        if any(w in comp_lower for w in ["encoder", "leveling", "feedback"]):
            return "encoder_position"
        if any(w in comp_lower for w in ["safety", "governor"]):
            return "safety_chain"
        if any(w in comp_lower for w in ["machine room", "environment", "emergency"]):
            return "sensor_env"
        return None


# =====================================================
# GUIDE CORPUS INGESTER — Master orchestrator
# =====================================================

class GUIDECorpusIngester:
    """Discovers and ingests all GUIDE/ documents into RAGChunks."""

    def __init__(self, guide_dir: str = "GUIDE", max_chunk_size: int = 800):
        self.guide_dir = guide_dir
        self.chunker = SemanticChunker(max_chunk_size=max_chunk_size)
        self.pdf_parser = PDFParser()

    def discover_documents(self) -> List[str]:
        """Discover all documents in the GUIDE directory."""
        if not os.path.isdir(self.guide_dir):
            logger.warning(f"GUIDE directory not found: {self.guide_dir}")
            return []

        files = []
        for f in sorted(os.listdir(self.guide_dir)):
            full_path = os.path.join(self.guide_dir, f)
            if os.path.isfile(full_path):
                files.append(f)
        return files

    def get_document_metadata(self, filename: str) -> Dict[str, Any]:
        """Get metadata for a document from the registry."""
        # Check exact match first
        if filename in GUIDE_DOCUMENT_REGISTRY:
            meta = dict(GUIDE_DOCUMENT_REGISTRY[filename])
            meta["document_id"] = self._make_doc_id(filename)
            return meta

        # Fallback: derive metadata from filename
        meta = {
            "document_id": self._make_doc_id(filename),
            "authority": "COMPONENT_GUIDE",
            "system": "elevator",
            "subsystem": None,
            "component": None,
            "document_type": "unknown",
            "egov": None,
            "configuration": None,
        }

        fn_lower = filename.lower()
        if "door" in fn_lower:
            meta["subsystem"] = "door"
        elif "brake" in fn_lower:
            meta["subsystem"] = "brake_traction"
        elif "rope" in fn_lower or "hoist" in fn_lower:
            meta["subsystem"] = "brake_traction"
        elif "sets" in fn_lower or "egov" in fn_lower:
            meta["subsystem"] = "encoder_position"
            meta["component"] = "SETS"
        elif "motor" in fn_lower or "drive" in fn_lower:
            meta["subsystem"] = "drive_motor"

        return meta

    def ingest_all(self) -> List[RAGChunk]:
        """Ingest all GUIDE documents and return list of all chunks."""
        all_chunks: List[RAGChunk] = []
        documents = self.discover_documents()

        if not documents:
            logger.warning("No documents found in GUIDE directory")
            return all_chunks

        logger.info(f"Discovered {len(documents)} documents in GUIDE/")

        for filename in documents:
            filepath = os.path.join(self.guide_dir, filename)
            meta = self.get_document_metadata(filename)

            if filename.endswith(".pdf"):
                chunks = self._ingest_pdf(filepath, filename, meta)
            elif filename.endswith(".csv"):
                chunks = TroubleshootingParser.parse_csv(filepath)
            elif filename.endswith(".json"):
                chunks = TroubleshootingParser.parse_json(filepath)
            else:
                logger.info(f"Skipping unsupported file type: {filename}")
                continue

            logger.info(f"  {filename}: {len(chunks)} chunks")
            all_chunks.extend(chunks)

        logger.info(f"Total chunks ingested: {len(all_chunks)}")
        return all_chunks

    def _ingest_pdf(self, filepath: str, filename: str, meta: Dict[str, Any]) -> List[RAGChunk]:
        """Ingest a single PDF document."""
        pages = self.pdf_parser.parse(filepath, filename)
        all_chunks: List[RAGChunk] = []

        for page_data in pages:
            page_num = page_data["page"]
            text = page_data["text"]

            # Chunk the page text
            text_chunks = self.chunker.chunk_page_text(
                text=text,
                filename=filename,
                page=page_num,
                document_meta=meta
            )
            all_chunks.extend(text_chunks)

            # Also create chunks for any extracted tables
            for t_idx, table in enumerate(page_data.get("tables", [])):
                if table.get("text"):
                    table_chunk = self.chunker.chunk_table(
                        table_text=table["text"],
                        filename=filename,
                        page=page_num,
                        document_meta=meta,
                        chunk_idx=len(all_chunks) + t_idx
                    )
                    all_chunks.append(table_chunk)

        return all_chunks

    @staticmethod
    def _make_doc_id(filename: str) -> str:
        """Generate a deterministic document ID from filename."""
        name_clean = re.sub(r"[^a-zA-Z0-9]", "_", filename.rsplit(".", 1)[0])
        return f"guide_{name_clean}".lower()
