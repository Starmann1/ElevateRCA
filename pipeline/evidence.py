"""
STAGE 3: EVIDENCE RETRIEVAL & ASSEMBLY
Aggregates quantitative telemetry, alarm sequences, maintenance records, free text,
and GUIDE RAG evidence with provenance and positive/negative support tagging.
"""

from typing import List, Dict, Any, Optional
import logging
from pipeline.schemas import (
    EvidenceItem, KONEFaultInput, FaultEpisode
)

logger = logging.getLogger("elevaterca.evidence")


class EvidenceAssembler:
    """Stage 3: Builds the unified Evidence Bundle with strict provenance and quality tracking.
    
    Evidence channels:
    1. Telemetry [MEASURED]
    2. Alarm Sequence [LOGGED]
    3. Operating State [MEASURED]
    4. Maintenance History [HISTORICAL]
    5. Technician Free Text [LOGGED]
    6. GUIDE RAG Technical Evidence [RAG_RETRIEVED]  ← NEW
    """

    def __init__(self, rag_retriever=None):
        """Initialize with optional RAG retriever for GUIDE corpus search.
        
        Args:
            rag_retriever: Optional HybridRetriever instance. If None, RAG is disabled.
        """
        self._rag_retriever = rag_retriever

    @staticmethod
    def _assemble_core_bundle(
        fault_input: KONEFaultInput,
        episode: FaultEpisode,
        triaged_signals: List[Dict[str, Any]]
    ) -> List[EvidenceItem]:
        """Assemble the core evidence bundle from telemetry, alarms, maintenance, and text.
        This is the ORIGINAL evidence assembly logic — preserved exactly."""
        bundle: List[EvidenceItem] = []

        # 1. Telemetry Evidence [MEASURED]
        for sig in triaged_signals:
            sig_name = sig["signal_name"]
            val_str = f"{sig['value']} {sig.get('unit', '')}"
            dev_str = f" ({sig['deviation_pct']:+}% vs {sig.get('baseline')} {sig.get('unit', '')})" if "deviation_pct" in sig else ""
            full_val_str = f"{val_str}{dev_str} [{sig['classification']}]"

            # Determine hypothesis relevance mappings
            hypo_rel = []
            if "current" in sig_name or "igbt" in sig_name:
                hypo_rel.extend(["RC1", "RC2", "RC3", "RC4", "RC5"])
            if "vibration" in sig_name:
                hypo_rel.extend(["RC2", "RC7", "RC5"])
            if "brake" in sig_name:
                hypo_rel.extend(["RC1", "RC2", "RC3"])
            if "door" in sig_name or "photoeye" in sig_name:
                hypo_rel.extend(["RC1", "RC2", "RC3", "RC4"])
            if "encoder" in sig_name or "leveling" in sig_name or "position" in sig_name:
                hypo_rel.extend(["RC1", "RC2", "RC3", "RC4"])

            bundle.append(EvidenceItem(
                signal_or_record=sig_name,
                value=full_val_str,
                provenance="MEASURED",
                quality=sig["quality"],
                diagnostic_value=sig["diagnostic_value"],
                relevant_to_hypotheses=hypo_rel,
                support_type="POSITIVE" if sig["classification"] in ["ELEVATED", "SEVERELY_ELEVATED", "SPIKE", "DRIFT"] else "NEUTRAL"
            ))

        # 2. Alarm Sequence Evidence [LOGGED]
        if episode.primary_alarm.alarm_code != "NONE":
            bundle.append(EvidenceItem(
                signal_or_record="Primary Alarm Event",
                value=f"{episode.primary_alarm.alarm_code} ({episode.primary_alarm.alarm_type}) at {episode.primary_alarm.timestamp}",
                provenance="LOGGED",
                quality="good",
                diagnostic_value="HIGH",
                relevant_to_hypotheses=["RC1", "RC2", "RC3", "RC4"],
                support_type="POSITIVE"
            ))

        for c_alarm in episode.consequential_alarms:
            bundle.append(EvidenceItem(
                signal_or_record="Consequential Alarm Event",
                value=f"{c_alarm.alarm_code}: {c_alarm.causal_relationship}",
                provenance="LOGGED",
                quality="good",
                diagnostic_value="MEDIUM",
                relevant_to_hypotheses=["RC1", "RC2", "RC3"],
                support_type="POSITIVE"
            ))

        # 3. Operating State [MEASURED / INFERRED]
        bundle.append(EvidenceItem(
            signal_or_record="Elevator Operating State",
            value=f"{fault_input.operating_state} (Model: {fault_input.elevator_model or 'KONE MonoSpace'})",
            provenance="MEASURED",
            quality="good",
            diagnostic_value="HIGH",
            relevant_to_hypotheses=["RC1", "RC2", "RC3"],
            support_type="NEUTRAL"
        ))

        # 4. Maintenance History Evidence [HISTORICAL]
        if fault_input.maintenance_history:
            for rec in fault_input.maintenance_history:
                notes = f" - Notes: {rec.technician_notes}" if rec.technician_notes else ""
                bundle.append(EvidenceItem(
                    signal_or_record=f"Maintenance on {rec.component} ({rec.date[:10]})",
                    value=f"Action: {rec.action} (Part Replaced: {rec.part_replaced}){notes}",
                    provenance="HISTORICAL",
                    quality="good",
                    diagnostic_value="MEDIUM",
                    relevant_to_hypotheses=["RC1", "RC2", "RC6"],
                    support_type="NEUTRAL"
                ))
        else:
            bundle.append(EvidenceItem(
                signal_or_record="Maintenance Records",
                value="No prior maintenance history provided in input payload",
                provenance="UNAVAILABLE",
                quality="missing",
                diagnostic_value="NONE",
                relevant_to_hypotheses=[],
                support_type="NEUTRAL"
            ))

        # 5. Technician Free Text [INFERRED / LOGGED]
        if fault_input.technician_free_text:
            bundle.append(EvidenceItem(
                signal_or_record="Technician Observation Note",
                value=f'"{fault_input.technician_free_text}"',
                provenance="LOGGED",
                quality="good",
                diagnostic_value="MEDIUM",
                relevant_to_hypotheses=["RC1", "RC2", "RC3"],
                support_type="POSITIVE"
            ))

        return bundle

    def assemble_bundle(
        self,
        fault_input: KONEFaultInput,
        episode: FaultEpisode,
        triaged_signals: List[Dict[str, Any]]
    ) -> List[EvidenceItem]:
        """Assemble the complete evidence bundle including RAG evidence.
        
        This method preserves full backward compatibility:
        - Without RAG retriever: returns same output as original
        - With RAG retriever: adds GUIDE technical evidence to the bundle
        """
        # Assemble core evidence (original logic)
        bundle = self._assemble_core_bundle(fault_input, episode, triaged_signals)

        # 6. GUIDE RAG Technical Evidence [RAG_RETRIEVED] — NEW
        if self._rag_retriever is not None:
            rag_evidence = self._retrieve_rag_evidence(fault_input, episode)
            if rag_evidence:
                bundle.extend(rag_evidence)
                logger.info(f"Added {len(rag_evidence)} RAG evidence items to bundle")

        return bundle

    def _retrieve_rag_evidence(
        self,
        fault_input: KONEFaultInput,
        episode: FaultEpisode,
    ) -> List[EvidenceItem]:
        """Retrieve GUIDE technical evidence using RAG.
        
        Returns EvidenceItems with RAG_RETRIEVED provenance and full source citations.
        """
        if self._rag_retriever is None:
            return []

        rag_items: List[EvidenceItem] = []

        try:
            from pipeline.rag_retrieval import build_rag_query

            # Build query from diagnostic context
            alarm_codes = []
            if episode.primary_alarm.alarm_code != "NONE":
                alarm_codes.append(episode.primary_alarm.alarm_code)
            for ca in episode.consequential_alarms:
                alarm_codes.append(ca.alarm_code)

            query = build_rag_query(
                primary_alarm_type=episode.primary_alarm.alarm_type,
                subsystem=episode.primary_alarm.subsystem,
                alarm_codes=alarm_codes,
                technician_text=fault_input.technician_free_text,
            )

            # Perform hybrid retrieval
            rag_result = self._rag_retriever.retrieve(
                query_text=query,
                subsystem=episode.primary_alarm.subsystem,
                fault_codes=alarm_codes,
                elevator_model=fault_input.elevator_model,
                n_results=8,
            )

            # Convert RAG sources to EvidenceItems
            for source in rag_result.sources:
                if source.relevance_score < 0.15:
                    continue  # Skip very low relevance results

                # Determine diagnostic value based on authority and relevance
                if source.relevance_score >= 0.7 and source.authority in ["OEM_REFERENCE", "COMPONENT_GUIDE"]:
                    diag_value = "HIGH"
                elif source.relevance_score >= 0.4:
                    diag_value = "MEDIUM"
                else:
                    diag_value = "LOW"

                # Build evidence description
                source_ref = f"[{source.source}"
                if source.page:
                    source_ref += f", p.{source.page}"
                if source.section:
                    source_ref += f", §{source.section[:50]}"
                source_ref += f", {source.authority}]"

                # Mark applicability
                applicability_note = ""
                if source.applicability == "CONFIGURATION_UNKNOWN":
                    applicability_note = " [⚠ Configuration applicability unknown — verify before applying]"
                elif source.applicability == "CONDITIONAL":
                    applicability_note = " [Conditionally applicable — verify configuration match]"
                elif source.applicability == "NOT_APPLICABLE":
                    continue  # Skip non-applicable documents

                # Truncate evidence text for the value field
                evidence_preview = source.evidence_text[:300] if source.evidence_text else "Technical reference available"

                rag_items.append(EvidenceItem(
                    signal_or_record=f"GUIDE Technical Reference {source_ref}",
                    value=f"{evidence_preview}{applicability_note}",
                    provenance="RAG_RETRIEVED",
                    quality="good",
                    diagnostic_value=diag_value,
                    relevant_to_hypotheses=source.supports if source.supports else ["RC1", "RC2", "RC3"],
                    support_type="POSITIVE" if source.supports else "NEUTRAL",
                    source_document=source.source,
                    source_page=source.page if source.page else None,
                    source_section=source.section,
                    source_authority=source.authority,
                    source_chunk_id=source.chunk_id,
                ))

        except Exception as e:
            logger.warning(f"RAG retrieval failed (non-fatal): {e}")
            # RAG failure is non-fatal — the pipeline continues without RAG evidence

        return rag_items

    def get_rag_sources_summary(self, evidence_bundle: List[EvidenceItem]) -> List[Dict[str, Any]]:
        """Extract RAG source summary from evidence bundle for ExplainabilityTrace."""
        rag_sources = []
        for item in evidence_bundle:
            if item.provenance == "RAG_RETRIEVED" and item.source_document:
                rag_sources.append({
                    "source": item.source_document,
                    "page": item.source_page,
                    "section": item.source_section,
                    "authority": item.source_authority,
                    "chunk_id": item.source_chunk_id,
                    "diagnostic_value": item.diagnostic_value,
                    "support_type": item.support_type,
                })
        return rag_sources
