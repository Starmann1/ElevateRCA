"""
ElevateRCA — Hybrid RAG Retrieval Module
Combines semantic search, keyword matching, fault-code matching,
component/subsystem filtering, configuration filtering, and
authority-ranked document retrieval.
"""

import re
import logging
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional

from pipeline.rag_schemas import (
    RAGSource, RAGEvidence, AUTHORITY_LEVELS
)
from pipeline.rag_store import RAGVectorStore

logger = logging.getLogger("elevaterca.rag.retrieval")


# =====================================================
# FAULT CODE PATTERNS — For keyword extraction
# =====================================================

FAULT_CODE_PATTERN = re.compile(r"\b[Ff]\d{2}\b")

SUBSYSTEM_KEYWORDS = {
    "door": [
        "door", "sill", "roller", "hanger", "photoeye", "light curtain",
        "interlock", "lock", "belt", "operator", "close", "open",
        "reopen", "obstruction", "nudging", "curtain", "safety edge"
    ],
    "brake_traction": [
        "brake", "pad", "lining", "traction", "rope", "hoisting",
        "sheave", "friction", "release", "coil", "solenoid",
        "air gap", "microswitch"
    ],
    "drive_motor": [
        "motor", "drive", "igbt", "inverter", "vfd", "current",
        "winding", "ecodisc", "pmsm", "overcurrent", "phase",
        "bearing", "stator"
    ],
    "encoder_position": [
        "encoder", "position", "leveling", "sets", "egov",
        "pulse", "speed", "feedback", "calibration", "vane"
    ],
    "safety_chain": [
        "safety", "chain", "governor", "buffer", "interlock",
        "emergency", "stop", "relay", "overspeed"
    ],
    "sensor_env": [
        "sensor", "temperature", "ambient", "machine room",
        "humidity", "vibration", "load", "weighing"
    ],
}

COMPONENT_KEYWORDS = {
    "photoeye": ["photoeye", "photo-eye", "light curtain", "optical sensor", "3d curtain"],
    "door_roller": ["roller", "hanger roller", "door roller", "bearing"],
    "door_belt": ["belt", "drive belt", "belt slip", "belt tension"],
    "door_lock": ["lock", "interlock", "door lock", "landing lock"],
    "door_sill": ["sill", "sill gap", "sill debris", "landing sill"],
    "door_motor": ["door motor", "door operator", "operator motor"],
    "brake_pad": ["brake pad", "pad thickness", "friction lining", "brake lining"],
    "brake_coil": ["brake coil", "solenoid", "brake release"],
    "hoisting_rope": ["rope", "hoisting rope", "wire rope", "suspension rope"],
    "SETS": ["sets", "egov", "terminal slowdown", "position detection"],
    "encoder": ["encoder", "optical encoder", "pulse loss", "quadrature"],
}


class HybridRetriever:
    """Performs hybrid retrieval combining semantic, keyword, and metadata-filtered search.
    
    Retrieval strategy:
    1. Semantic search with subsystem filter (primary)
    2. Keyword search for fault codes and component terms
    3. Configuration-aware filtering for SETS/EGOV documents
    4. Authority-ranked result merging
    5. Configuration applicability tagging
    """

    def __init__(self, store: RAGVectorStore):
        self.store = store

    def retrieve(
        self,
        query_text: str,
        subsystem: Optional[str] = None,
        component: Optional[str] = None,
        fault_codes: Optional[List[str]] = None,
        elevator_model: Optional[str] = None,
        egov: Optional[str] = None,
        configuration: Optional[str] = None,
        n_results: int = 10,
    ) -> RAGEvidence:
        """Perform hybrid retrieval and return structured RAG evidence.
        
        Args:
            query_text: Natural language query or alarm description
            subsystem: Pipeline subsystem to filter by
            component: Specific component to filter by
            fault_codes: List of fault codes (e.g., ["F14", "F74"])
            elevator_model: Elevator model for configuration matching
            egov: EGOV setting for SETS configuration matching
            configuration: Specific configuration filter
            n_results: Maximum results to return
        
        Returns:
            RAGEvidence with scored, authority-ranked sources
        """
        if not self.store.is_indexed:
            logger.warning("RAG store is not indexed. Returning empty evidence.")
            return RAGEvidence(
                sources=[],
                query_subsystem=subsystem,
                query_component=component,
                query_fault_code=fault_codes[0] if fault_codes else None,
                retrieval_timestamp=datetime.now(timezone.utc).isoformat()
            )

        # Auto-detect subsystem from query if not specified
        if not subsystem:
            subsystem = self._detect_subsystem(query_text)

        # Auto-detect components from query
        if not component:
            component = self._detect_component(query_text)

        # Extract fault codes from query text
        if not fault_codes:
            fault_codes = self._extract_fault_codes(query_text)

        all_results: List[Dict[str, Any]] = []

        # 1. SEMANTIC SEARCH with subsystem filter
        semantic_results = self.store.query(
            query_text=query_text,
            n_results=n_results,
            subsystem=subsystem,
        )
        all_results.extend(semantic_results)

        # 2. SEMANTIC SEARCH without subsystem filter (broader context)
        if len(semantic_results) < n_results // 2:
            broader_results = self.store.query(
                query_text=query_text,
                n_results=n_results // 2,
            )
            all_results.extend(broader_results)

        # 3. KEYWORD SEARCH for fault codes
        if fault_codes:
            for fc in fault_codes:
                kw_results = self.store.keyword_search(
                    keywords=[fc],
                    n_results=5,
                    subsystem=subsystem,
                )
                all_results.extend(kw_results)

        # 4. KEYWORD SEARCH for component terms
        if component:
            comp_keywords = COMPONENT_KEYWORDS.get(component, [component])
            kw_results = self.store.keyword_search(
                keywords=comp_keywords[:3],
                n_results=5,
                subsystem=subsystem,
            )
            all_results.extend(kw_results)

        # 5. CONFIGURATION-SPECIFIC search for SETS documents
        if egov or (subsystem == "encoder_position" and "sets" in query_text.lower()):
            config_results = self.store.query(
                query_text=query_text,
                n_results=5,
                egov=egov,
                component="SETS",
            )
            all_results.extend(config_results)

        # Deduplicate by chunk_id
        seen = set()
        unique_results = []
        for r in all_results:
            cid = r.get("chunk_id", "")
            if cid and cid not in seen:
                seen.add(cid)
                unique_results.append(r)

        # Score and rank
        ranked_results = self._rank_results(
            unique_results,
            query_text=query_text,
            subsystem=subsystem,
            component=component,
            egov=egov,
            configuration=configuration,
        )

        # Convert to RAGSource objects
        sources = []
        for r in ranked_results[:n_results]:
            applicability = self._determine_applicability(r, egov, configuration)
            source = RAGSource(
                source=r.get("filename", ""),
                page=r.get("page", 0),
                section=r.get("section", ""),
                chunk_id=r.get("chunk_id", ""),
                authority=r.get("authority", "COMPONENT_GUIDE"),
                relevance_score=r.get("final_score", r.get("relevance_score", 0.0)),
                applicability=applicability,
                evidence_text=self._truncate_text(r.get("text", ""), max_len=500),
                supports=[],
                contradicts=[],
            )
            sources.append(source)

        return RAGEvidence(
            sources=sources,
            query_subsystem=subsystem,
            query_component=component,
            query_fault_code=fault_codes[0] if fault_codes else None,
            total_documents_searched=self.store.document_count,
            configuration_filter_applied=bool(egov or configuration),
            retrieval_timestamp=datetime.now(timezone.utc).isoformat()
        )

    # =====================================================
    # RANKING AND SCORING
    # =====================================================

    def _rank_results(
        self,
        results: List[Dict[str, Any]],
        query_text: str,
        subsystem: Optional[str],
        component: Optional[str],
        egov: Optional[str],
        configuration: Optional[str],
    ) -> List[Dict[str, Any]]:
        """Re-rank results using authority, subsystem match, and configuration relevance."""
        for r in results:
            base_score = r.get("relevance_score", 0.0)

            # Authority boost (lower number = higher authority)
            auth_level = AUTHORITY_LEVELS.get(r.get("authority", ""), 5)
            authority_boost = (6 - auth_level) * 0.05  # 0.05 to 0.25 boost

            # Subsystem match boost
            subsystem_boost = 0.0
            if subsystem and r.get("subsystem") == subsystem:
                subsystem_boost = 0.15

            # Component match boost
            component_boost = 0.0
            if component and r.get("component") and component.lower() in r["component"].lower():
                component_boost = 0.10

            # Configuration match boost/penalty
            config_boost = 0.0
            if egov:
                r_egov = r.get("egov", "")
                if r_egov == egov:
                    config_boost = 0.20  # Exact config match
                elif r_egov and r_egov != egov:
                    config_boost = -0.30  # Wrong configuration — penalize heavily
            
            if configuration:
                r_config = r.get("configuration", "")
                if r_config == configuration:
                    config_boost = max(config_boost, 0.15)
                elif r_config and r_config != configuration:
                    config_boost = min(config_boost, -0.20)

            # Procedure/table boost for maintenance queries
            content_boost = 0.0
            if r.get("is_procedure") and any(w in query_text.lower() for w in ["inspect", "check", "procedure", "maintenance", "repair"]):
                content_boost = 0.05
            if r.get("is_warning"):
                content_boost += 0.03
            if r.get("is_table") and any(w in query_text.lower() for w in ["spec", "tolerance", "value", "measurement"]):
                content_boost += 0.05

            final_score = base_score + authority_boost + subsystem_boost + component_boost + config_boost + content_boost
            r["final_score"] = round(max(0.0, min(1.0, final_score)), 4)

        # Sort by final score descending
        results.sort(key=lambda x: x["final_score"], reverse=True)
        return results

    # =====================================================
    # DETECTION / EXTRACTION HELPERS
    # =====================================================

    @staticmethod
    def _detect_subsystem(query: str) -> Optional[str]:
        """Detect subsystem from query text using keyword matching."""
        query_lower = query.lower()
        scores: Dict[str, int] = {}

        for subsystem, keywords in SUBSYSTEM_KEYWORDS.items():
            score = sum(1 for kw in keywords if kw in query_lower)
            if score > 0:
                scores[subsystem] = score

        if scores:
            return max(scores, key=scores.get)
        return None

    @staticmethod
    def _detect_component(query: str) -> Optional[str]:
        """Detect component from query text."""
        query_lower = query.lower()
        for component, keywords in COMPONENT_KEYWORDS.items():
            for kw in keywords:
                if kw in query_lower:
                    return component
        return None

    @staticmethod
    def _extract_fault_codes(query: str) -> List[str]:
        """Extract KONE fault codes (F14, F24, etc.) from query."""
        codes = FAULT_CODE_PATTERN.findall(query.upper())
        return [c.upper() for c in codes]

    @staticmethod
    def _determine_applicability(
        result: Dict[str, Any],
        target_egov: Optional[str],
        target_config: Optional[str],
    ) -> str:
        """Determine configuration applicability of a result."""
        r_egov = result.get("egov", "")
        r_config = result.get("configuration", "")

        # If result has a specific EGOV and we have a target
        if r_egov and target_egov:
            if r_egov == target_egov:
                return "MATCHED"
            else:
                return "NOT_APPLICABLE"

        # If result has EGOV but we don't know the target
        if r_egov and not target_egov:
            return "CONFIGURATION_UNKNOWN"

        # If result has specific configuration
        if r_config and target_config:
            if r_config == target_config:
                return "MATCHED"
            else:
                return "CONDITIONAL"

        if r_config and not target_config:
            return "CONDITIONAL"

        # No configuration constraints
        return "MATCHED"

    @staticmethod
    def _truncate_text(text: str, max_len: int = 500) -> str:
        """Truncate text to max length, preserving word boundaries."""
        if len(text) <= max_len:
            return text
        truncated = text[:max_len].rsplit(" ", 1)[0]
        return truncated + "..."


# =====================================================
# CONVENIENCE: Build retrieval query from fault input
# =====================================================

def build_rag_query(
    primary_alarm_type: str,
    subsystem: str,
    alarm_codes: List[str],
    technician_text: Optional[str] = None,
    top_hypothesis: Optional[str] = None,
) -> str:
    """Build a natural language retrieval query from diagnostic context.
    
    Combines alarm type, subsystem, fault codes, and technician observations
    into an effective retrieval query.
    """
    parts = []

    # Primary alarm context
    alarm_readable = primary_alarm_type.replace("_", " ")
    parts.append(f"{alarm_readable}")

    # Subsystem context
    subsystem_readable = subsystem.replace("_", " ")
    parts.append(f"{subsystem_readable}")

    # Top hypothesis context
    if top_hypothesis:
        parts.append(top_hypothesis)

    # Fault codes
    for code in alarm_codes[:3]:
        parts.append(code)

    # Technician observations (extract key terms)
    if technician_text:
        # Take first sentence or up to 100 chars
        tech_short = technician_text.split(".")[0][:100]
        parts.append(tech_short)

    return " ".join(parts)
