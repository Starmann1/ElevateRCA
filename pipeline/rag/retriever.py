"""
ElevateRCA - Hybrid Evidence Retriever with Configuration Gatekeeping and Authority Ranking
"""

import re
from typing import List, Dict, Any, Optional
from pipeline.models import ElevatorConfiguration, AuthorityTier
from pipeline.rag.store import GuideKnowledgeStore


class EvidenceRetriever:
    """
    Hybrid retriever enforcing:
    1. Configuration Applicability Gatekeeping (SETS EGOV / Gearless vs Geared)
    2. Authority Tier Ranking (Tier 1 > Tier 2 > Tier 3)
    3. Structured Evidence Package assembly
    4. Safety Constraint Isolation
    """
    def __init__(self, store: GuideKnowledgeStore):
        self.store = store

    def retrieve(
        self,
        query: str,
        subsystem: Optional[str] = None,
        component: Optional[str] = None,
        configuration: Optional[ElevatorConfiguration] = None,
        top_k: int = 5,
    ) -> Dict[str, Any]:
        """
        Retrieves grounded evidence from the GUIDE store tailored to the query and configuration.
        """
        # 1. Applicability Filtering
        where_filter = None
        egov_cfg = configuration.egov if configuration else None
        
        # Build query results
        raw_results = self.store.query(query_text=query, where_filter=where_filter, n_results=top_k * 3)
        
        # If no results or empty, return clean package
        if not raw_results:
            return {
                "query": query,
                "subsystem": subsystem or "General",
                "retrieved_evidence": [],
                "safety_constraints": [],
                "candidate_components": [],
                "candidate_failure_modes": [],
                "diagnostic_procedures": [],
                "expected_values": [],
                "corrective_actions": [],
                "source_references": [],
                "configuration_status": "OK",
            }

        filtered_and_ranked = []
        safety_constraints = []
        seen_sources = set()
        config_warning = None

        for item in raw_results:
            meta = item["metadata"]
            doc_egov = meta.get("egov_setting", "NONE")
            filename = meta.get("filename", "")
            
            # --- Check SETS EGOV Applicability ---
            if doc_egov and doc_egov != "NONE":
                if egov_cfg is None:
                    # Elevator configuration is UNKNOWN: exclude specific SETS manuals to prevent misdiagnosis
                    config_warning = "Elevator SETS EGOV setting is unknown. Specific SETS-01 calibration manuals suppressed."
                    continue
                else:
                    norm_cfg = egov_cfg.replace("-", "_").upper()
                    norm_doc = doc_egov.replace("-", "_").upper()
                    if norm_cfg not in norm_doc and norm_doc not in norm_cfg:
                        # Inapplicable SETS manual for this elevator: filter out!
                        continue

            # --- Check Machine Type Applicability ---
            if configuration and configuration.machine_type:
                is_gearless = "gearless" in configuration.machine_type.lower()
                if is_gearless and "brake_of_geared" in filename.lower():
                    # Elevators with gearless machines should not use geared machine brake tolerances
                    continue
                elif not is_gearless and "brake_of_gearless" in filename.lower():
                    continue

            # --- Calculate Authority Multiplier ---
            auth = meta.get("authority", "TIER_4")
            if auth == AuthorityTier.TIER_1.value:
                multiplier = 1.35
            elif auth == AuthorityTier.TIER_2.value:
                multiplier = 1.15
            elif auth == AuthorityTier.TIER_3.value:
                multiplier = 1.00
            else:
                multiplier = 0.85

            ranked_score = item["similarity"] * multiplier

            # Extract warnings and safety constraints
            if meta.get("data_type") == "WARNING" or "LOTO" in item["content"] or "WARNING" in item["content"]:
                safety_constraints.append(f"[{filename} p.{meta.get('page')}] {item['content'].splitlines()[-1]}")

            source_ref = f"{filename} (Page {meta.get('page')}, Section: {meta.get('section')})"
            seen_sources.add(source_ref)

            evidence_entry = {
                "source": filename,
                "section": meta.get("section", "General"),
                "page": meta.get("page", 1),
                "evidence": item["content"],
                "authority": auth,
                "applicability": f"Config: {doc_egov}" if doc_egov != "NONE" else "Universal",
                "relevance": round(ranked_score, 3),
                "data_type": meta.get("data_type", "TEXT"),
            }
            filtered_and_ranked.append(evidence_entry)

        # Sort by authority-weighted relevance
        filtered_and_ranked.sort(key=lambda x: x["relevance"], reverse=True)
        final_evidence = filtered_and_ranked[:top_k]

        # Extract structured procedures, candidates, and expected values
        diagnostic_procs = []
        expected_values = []
        candidate_causes = []

        for ev in final_evidence:
            text = ev["evidence"]
            # Look for candidate causes in text
            if "Candidate Causes:" in text or "Possible Causes:" in text:
                matches = re.findall(r"(?:Candidate Causes|Possible Causes):\s*([^\n]+)", text, re.I)
                for m in matches:
                    candidate_causes.extend([c.strip() for c in m.split(";") if c.strip()])
            
            # Look for maintenance procedures / checks
            if "Maintenance Check:" in text or "Recommended Action:" in text or "Procedure:" in text:
                matches = re.findall(r"(?:Maintenance Check|Recommended Action|Procedure):\s*([^\n]+)", text, re.I)
                for m in matches:
                    diagnostic_procs.append(f"[{ev['source']} p.{ev['page']}] {m.strip()}")

            # Extract numeric parameters / tolerances / tables
            if ev["data_type"] == "TABLE":
                expected_values.append({
                    "source": ev["source"],
                    "page": ev["page"],
                    "table_excerpt": text[:300] + "...",
                })

        return {
            "query": query,
            "subsystem": subsystem or "General",
            "retrieved_evidence": final_evidence,
            "safety_constraints": list(set(safety_constraints))[:5],
            "candidate_components": list(set([component] if component else [])),
            "candidate_failure_modes": list(set(candidate_causes))[:6],
            "diagnostic_procedures": list(set(diagnostic_procs))[:5],
            "expected_values": expected_values[:3],
            "corrective_actions": [p for p in diagnostic_procs if "Replace" in p or "Adjust" in p or "Service" in p],
            "source_references": list(seen_sources)[:8],
            "configuration_status": config_warning or "CONFIG_VALIDATED",
        }
