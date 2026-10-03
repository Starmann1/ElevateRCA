"""
ElevateRCA - Structure-Aware PDF and Dataset Parser for GUIDE Corpus
Preserves sections, procedures, warnings, tables, and configuration boundaries.
"""

from pathlib import Path
import csv
import json
import re
from typing import List, Dict, Any, Optional
import fitz  # PyMuPDF

from pipeline.models import (
    DocumentChunk,
    DocumentMetadata,
    DocumentType,
    AuthorityTier,
)
from pipeline.rag.classifier import classify_guide_file


def _format_table_markdown(table) -> str:
    """Converts a fitz table object to a clean Markdown representation."""
    try:
        df = table.to_pandas()
        if df is not None and not df.empty:
            df.columns = [str(c).replace("\n", " ").strip() for c in df.columns]
            return df.fillna("").to_markdown(index=False)
    except Exception:
        pass
    
    try:
        rows = table.extract()
        if not rows:
            return ""
        md_lines = []
        headers = [str(cell or "").replace("\n", " ").strip() for cell in rows[0]]
        md_lines.append("| " + " | ".join(headers) + " |")
        md_lines.append("| " + " | ".join(["---"] * len(headers)) + " |")
        for row in rows[1:]:
            cells = [str(cell or "").replace("\n", " ").strip() for cell in row]
            md_lines.append("| " + " | ".join(cells) + " |")
        return "\n".join(md_lines)
    except Exception:
        return ""


def parse_pdf_document(pdf_path: Path, metadata: Optional[DocumentMetadata] = None) -> List[DocumentChunk]:
    """
    Structure-aware parser for technical elevator PDFs.
    Extracts text, preserves section headings, detects tables, isolates warnings,
    and attaches exact page/context provenance.
    """
    if metadata is None:
        metadata = classify_guide_file(pdf_path.name)

    chunks: List[DocumentChunk] = []
    doc = fitz.open(str(pdf_path))
    
    current_section = "General / Overview"
    
    for page_idx in range(len(doc)):
        page = doc[page_idx]
        page_num = page_idx + 1
        page_text = page.get_text()
        
        if not page_text.strip():
            continue

        # Detect potential section headers
        lines = page_text.splitlines()
        for line in lines[:5]:
            clean_line = line.strip()
            if (
                re.match(r"^(SECTION|\d+(\.\d+)*)\s+[A-Z]", clean_line, re.IGNORECASE)
                or (len(clean_line) < 60 and clean_line.isupper() and len(clean_line) > 4)
            ):
                current_section = clean_line
                break

        # 1. Fast Table Extraction: Only check find_tables if page text hints at table structure
        has_table_hints = bool(re.search(r"\b(table|parameter|specification|limit|clearance|setting|nominal|standard|air gap)\b", page_text, re.I))
        if has_table_hints:
            try:
                tab_finder = page.find_tables()
                if tab_finder.tables:
                    for t_idx, table in enumerate(tab_finder.tables):
                        table_md = _format_table_markdown(table)
                        if table_md and len(table_md.strip()) > 20:
                            t_meta = metadata.model_copy(deep=True)
                            t_meta.section = current_section
                            t_meta.page = page_num
                            t_meta.data_type = "TABLE"
                            
                            table_content = (
                                f"[Source: {metadata.filename} | Page: {page_num} | Section: {current_section} | Data: Table]\n"
                                f"### Table: Parameter Specifications & Limits (Page {page_num})\n"
                                f"{table_md}"
                            )
                            chunks.append(
                                DocumentChunk(
                                    chunk_id=f"{metadata.document_id}-P{page_num}-TBL{t_idx+1}",
                                    content=table_content,
                                    metadata=t_meta,
                                    tables=[{"markdown": table_md, "page": page_num}],
                                )
                            )
            except Exception:
                pass

        # 2. Extract and chunk text blocks
        paragraphs = re.split(r"\n\s*\n", page_text)
        
        current_chunk_text = []
        chunk_token_count = 0
        p_idx = 1
        
        for para in paragraphs:
            clean_para = para.strip()
            if not clean_para or len(clean_para) < 25:
                continue
            
            is_warning = bool(re.search(r"\b(DANGER|WARNING|CAUTION|SAFETY NOTICE|LOCKOUT|LOTO)\b", clean_para, re.I))
            current_chunk_text.append(clean_para)
            chunk_token_count += len(clean_para.split())
            
            if chunk_token_count >= 200 or is_warning:
                p_meta = metadata.model_copy(deep=True)
                p_meta.section = current_section
                p_meta.page = page_num
                p_meta.data_type = "WARNING" if is_warning else "PROCEDURE"
                
                body = "\n\n".join(current_chunk_text)
                header = (
                    f"[Source: {metadata.filename} | Page: {page_num} | Section: {current_section} | "
                    f"Subsystem: {metadata.subsystem} | Config: {metadata.egov_setting or metadata.configuration or 'General'}]\n"
                )
                
                chunks.append(
                    DocumentChunk(
                        chunk_id=f"{metadata.document_id}-P{page_num}-C{p_idx}",
                        content=header + body,
                        metadata=p_meta,
                    )
                )
                current_chunk_text = []
                chunk_token_count = 0
                p_idx += 1
        
        if current_chunk_text:
            p_meta = metadata.model_copy(deep=True)
            p_meta.section = current_section
            p_meta.page = page_num
            p_meta.data_type = "TEXT"
            
            body = "\n\n".join(current_chunk_text)
            header = (
                f"[Source: {metadata.filename} | Page: {page_num} | Section: {current_section} | "
                f"Subsystem: {metadata.subsystem} | Config: {metadata.egov_setting or metadata.configuration or 'General'}]\n"
            )
            chunks.append(
                DocumentChunk(
                    chunk_id=f"{metadata.document_id}-P{page_num}-C{p_idx}",
                    content=header + body,
                    metadata=p_meta,
                )
            )

    return chunks


def parse_troubleshooting_dataset(file_path: Path) -> List[DocumentChunk]:
    """
    Parses elevator_troubleshooting_dataset (.csv or .json) into 15 rich, structured
    DocumentChunk entities. Preserves all 10 schema fields with Tier 3 authority.
    Disambiguates chunk_id based on file extension.
    """
    chunks: List[DocumentChunk] = []
    records: List[Dict[str, Any]] = []
    fmt_tag = file_path.suffix.lstrip(".").lower()

    if file_path.suffix.lower() == ".json":
        with open(file_path, "r", encoding="utf-8") as f:
            records = json.load(f)
    elif file_path.suffix.lower() == ".csv":
        with open(file_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            records = list(reader)

    base_metadata = classify_guide_file(file_path.name)

    for rec in records:
        rec_id = rec.get("id", "UNKNOWN")
        component = rec.get("component", "General")
        symptom = rec.get("symptom", "")
        alarm = rec.get("alarm", "None")
        evidence = rec.get("evidence", "")
        causes = rec.get("possible_causes", "")
        maint_check = rec.get("maintenance_check", "")
        action = rec.get("recommended_action", "")
        priority = rec.get("priority", "Medium")
        root_cause_cat = rec.get("root_cause_category", "General")

        rec_meta = base_metadata.model_copy(deep=True)
        rec_meta.component = component
        rec_meta.subsystem = root_cause_cat
        rec_meta.fault_code = alarm
        rec_meta.section = f"Scenario {rec_id} - {component}"
        rec_meta.data_type = "STRUCTURED_RECORD"

        formatted_content = (
            f"[Source: {file_path.name} | Scenario: {rec_id} | Component: {component} | Priority: {priority}]\n"
            f"**Fault ID:** {rec_id}\n"
            f"**Component:** {component} ({root_cause_cat})\n"
            f"**Reported Symptom:** {symptom}\n"
            f"**Associated Alarm:** {alarm}\n"
            f"**Observable Evidence:** {evidence}\n"
            f"**Candidate Causes:** {causes}\n"
            f"**Maintenance Check:** {maint_check}\n"
            f"**Recommended Action:** {action}\n"
            f"**Severity Priority:** {priority}\n"
        )

        chunks.append(
            DocumentChunk(
                chunk_id=f"CHUNK-{fmt_tag.upper()}-{rec_id}",
                content=formatted_content,
                metadata=rec_meta,
            )
        )

    return chunks
