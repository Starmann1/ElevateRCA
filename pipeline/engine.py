"""
ElevateRCA Master Engine — 5-Stage Diagnostic Pipeline
Coordinates Stage 1 through Stage 5 and builds the complete ExplainabilityTrace.
Now includes GUIDE RAG corpus integration for evidence-grounded diagnostics.
"""

from datetime import datetime, timezone
from typing import Dict, Any, List, Union, Optional
import uuid
import os
import logging

from pipeline.schemas import (
    KONEFaultInput, ExplainabilityTrace, Metadata
)
from pipeline.triage import SignalTriager
from pipeline.correlation import AlarmCorrelator
from pipeline.evidence import EvidenceAssembler
from pipeline.bayesian_rca import BayesianRCAEngine
from pipeline.synthesis import DiagnosisSynthesizer
from pipeline.guardrails import SafetyGuardrails

logger = logging.getLogger("elevaterca.engine")


class ElevateRCAEngine:
    """Master orchestrator for the 5-Stage RCA Pipeline.
    
    Now with optional GUIDE RAG corpus integration:
    - Auto-discovers and indexes GUIDE/ documents on first use
    - Adds technical evidence from GUIDE corpus to Stage 3
    - Preserves full backward compatibility when RAG is not available
    """

    def __init__(
        self,
        failure_modes_path: str = "knowledge/failure_modes.yaml",
        causal_links_path: str = "knowledge/causal_links.yaml",
        corrective_actions_path: str = "knowledge/corrective_actions.yaml",
        guide_dir: str = "GUIDE",
        enable_rag: bool = True,
        chroma_persist_dir: str = ".chroma_db",
    ):
        self.triager = SignalTriager()
        self.correlator = AlarmCorrelator(causal_links_path)
        self.rca_engine = BayesianRCAEngine(failure_modes_path)
        self.synthesizer = DiagnosisSynthesizer(corrective_actions_path)

        # Initialize RAG system (optional — graceful fallback if unavailable)
        self._rag_retriever = None
        self._rag_store = None
        self._guide_dir = guide_dir
        self._chroma_persist_dir = chroma_persist_dir
        self._rag_initialized = False

        if enable_rag:
            self._init_rag()

        # Create EvidenceAssembler with or without RAG
        self.evidence_assembler = EvidenceAssembler(rag_retriever=self._rag_retriever)

    def _init_rag(self):
        """Initialize the RAG system: vector store + retriever.
        Gracefully handles missing dependencies or GUIDE directory.
        """
        try:
            from pipeline.rag_store import RAGVectorStore
            from pipeline.rag_retrieval import HybridRetriever
            from pipeline.rag_ingest import GUIDECorpusIngester

            # Check if GUIDE directory exists
            if not os.path.isdir(self._guide_dir):
                logger.info(f"GUIDE directory not found at '{self._guide_dir}' — RAG disabled")
                return

            # Initialize ChromaDB store
            self._rag_store = RAGVectorStore(persist_dir=self._chroma_persist_dir)

            # Auto-index if not already indexed
            if not self._rag_store.is_indexed:
                logger.info("GUIDE corpus not yet indexed — starting ingestion...")
                ingester = GUIDECorpusIngester(guide_dir=self._guide_dir)
                chunks = ingester.ingest_all()
                if chunks:
                    indexed = self._rag_store.index_chunks(chunks)
                    logger.info(f"GUIDE corpus indexed: {indexed} chunks from {len(ingester.discover_documents())} documents")
                else:
                    logger.warning("No chunks produced from GUIDE corpus")
            else:
                stats = self._rag_store.get_index_stats()
                logger.info(f"GUIDE corpus already indexed: {stats['total_chunks']} chunks")

            # Create retriever
            self._rag_retriever = HybridRetriever(store=self._rag_store)
            self._rag_initialized = True
            logger.info("RAG system initialized successfully")

        except ImportError as e:
            logger.info(f"RAG dependencies not available ({e}) — RAG disabled")
        except Exception as e:
            logger.warning(f"RAG initialization failed (non-fatal): {e}")

    @property
    def rag_enabled(self) -> bool:
        """Check if RAG is active."""
        return self._rag_initialized and self._rag_retriever is not None

    def reindex_guide_corpus(self) -> Dict[str, Any]:
        """Force re-indexing of the GUIDE corpus. Returns index stats."""
        if self._rag_store is None:
            return {"error": "RAG store not initialized"}

        try:
            from pipeline.rag_ingest import GUIDECorpusIngester

            self._rag_store.clear()
            ingester = GUIDECorpusIngester(guide_dir=self._guide_dir)
            chunks = ingester.ingest_all()
            indexed = self._rag_store.index_chunks(chunks) if chunks else 0
            return self._rag_store.get_index_stats()
        except Exception as e:
            return {"error": str(e)}

    def analyze(self, fault_input: Union[KONEFaultInput, dict]) -> ExplainabilityTrace:
        """Executes all 5 stages in order."""
        if isinstance(fault_input, dict):
            fault_input = KONEFaultInput(**fault_input)
            
        # Reset triager trackers per fault episode analysis
        self.triager.reset()

        # STAGE 1: Signal Triage & Anomaly Detection
        triaged_signals = self.triager.triage_all(fault_input.telemetry, fault_input.operating_state)

        # STAGE 2: Alarm Cascade Correlation
        fault_episode = self.correlator.correlate_alarms(fault_input.alarms)

        # STAGE 3: Evidence Retrieval & Assembly (now includes RAG)
        evidence_bundle = self.evidence_assembler.assemble_bundle(fault_input, fault_episode, triaged_signals)

        # STAGE 4: Fault Tree Traversal & Bayesian Posterior Ranking
        hypotheses = self.rca_engine.evaluate_subsystem(fault_input, fault_episode, triaged_signals)

        # STAGE 5: Confidence Decision & Synthesis
        rca_conclusion, recommendation, tech_view, mgr_view = self.synthesizer.synthesize(
            fault_input, fault_episode, evidence_bundle, hypotheses
        )

        # Evidence Gaps Identification
        evidence_gaps = []
        if not fault_input.maintenance_history:
            evidence_gaps.append("Component maintenance history not provided")
        if hypotheses and hypotheses[0].expected_but_missing_evidence:
            evidence_gaps.extend(hypotheses[0].expected_but_missing_evidence)
        if not self.rag_enabled:
            evidence_gaps.append("GUIDE RAG corpus not indexed — technical document evidence unavailable")

        # Claim discipline validation
        all_narrative = f"{rca_conclusion.causal_narrative} {tech_view.summary} {mgr_view.summary}"
        claim_flags = SafetyGuardrails.check_claim_discipline(all_narrative)

        # Pipeline stages completed
        pipeline_stages = [
            "signal_triage",
            "alarm_correlation",
            "evidence_assembly",
            "fault_tree_traversal",
            "bayesian_ranking",
            "confidence_synthesis"
        ]
        if self.rag_enabled:
            pipeline_stages.insert(3, "guide_rag_retrieval")

        # Metadata
        metadata = Metadata(
            pipeline_stages_completed=pipeline_stages,
            evidence_gaps=evidence_gaps,
            claim_discipline_flags=claim_flags,
            data_provenance_note=(
                "All analysis based on provided KONE software output. "
                "No assumptions made about missing values. "
                "Probabilities are calibrated engineering estimates, not validated fleet statistics."
            ),
            human_verification_required=True,
            advisory_only=True
        )

        # Generate Investigation ID
        timestamp_clean = fault_input.timestamp_utc.replace(":", "").replace("-", "").replace(".", "")[:15]
        investigation_id = f"ELV-{fault_input.elevator_id}-{timestamp_clean}"

        # Extract RAG source provenance for trace
        rag_sources = self.evidence_assembler.get_rag_sources_summary(evidence_bundle)

        # Generate Comprehensive Engineering Report
        investigation_report = self.synthesizer.generate_investigation_report_markdown(
            fault_input=fault_input,
            episode=fault_episode,
            evidence_bundle=evidence_bundle,
            hypotheses=hypotheses,
            rca_conclusion=rca_conclusion,
            recommendation=recommendation,
            investigation_id=investigation_id
        )

        return ExplainabilityTrace(
            investigation_id=investigation_id,
            elevator_id=fault_input.elevator_id,
            analysis_timestamp=datetime.now(timezone.utc).isoformat(),
            fault_episode=fault_episode,
            evidence_bundle=evidence_bundle,
            hypotheses=hypotheses,
            rca_conclusion=rca_conclusion,
            corrective_recommendation=recommendation,
            technician_view=tech_view,
            building_manager_view=mgr_view,
            metadata=metadata,
            detailed_investigation_report=investigation_report,
            verification_stage=getattr(fault_input, "verification_stage", "SINGLE_STAGE") or "SINGLE_STAGE",
            rag_sources=rag_sources,
        )
