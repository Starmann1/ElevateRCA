"""
ElevateRCA - High-Performance In-Process Vector & Metadata Store for GUIDE Corpus
Implements offline deterministic embeddings, metadata filtering, and hybrid search.
"""

from pathlib import Path
import os
import re
from typing import List, Dict, Any, Optional
import chromadb
from chromadb.api.types import Documents, EmbeddingFunction, Embeddings
from sklearn.feature_extraction.text import HashingVectorizer

from pipeline.models import DocumentChunk, ElevatorConfiguration
from pipeline.rag.parser import parse_pdf_document, parse_troubleshooting_dataset
from pipeline.rag.classifier import classify_guide_file


class FastOfflineEmbedding(EmbeddingFunction):
    """
    Deterministic, zero-download, high-speed L2-normalized embedding function.
    Runs 100% offline using scikit-learn HashingVectorizer (384 dimensions).
    """
    def __init__(self, n_features: int = 384):
        self.vectorizer = HashingVectorizer(
            n_features=n_features,
            norm="l2",
            alternate_sign=False,
            token_pattern=r"(?u)\b[\w\-\.]{2,}\b",
        )

    def __call__(self, input: Documents) -> Embeddings:
        matrix = self.vectorizer.transform(input)
        return matrix.toarray().tolist()


class GuideKnowledgeStore:
    """
    Manages indexing, storage, and retrieval for the 15 GUIDE technical files.
    """
    def __init__(self, persist_dir: Optional[str] = "./chroma_data"):
        self.persist_dir = persist_dir
        if persist_dir:
            os.makedirs(persist_dir, exist_ok=True)
            self.client = chromadb.PersistentClient(path=persist_dir)
        else:
            self.client = chromadb.Client()

        self.embedding_fn = FastOfflineEmbedding()
        self.collection = self.client.get_or_create_collection(
            name="elevaterca_guide_knowledge",
            embedding_function=self.embedding_fn,
            metadata={"hnsw:space": "cosine"},
        )
        self.raw_chunks: Dict[str, DocumentChunk] = {}
        self.ingestion_stats: Dict[str, Any] = {
            "total_files": 0,
            "total_chunks": 0,
            "table_chunks": 0,
            "warning_chunks": 0,
            "procedure_chunks": 0,
            "files_indexed": [],
        }

    def ingest_guide_directory(self, guide_dir: Path, force_reload: bool = False) -> Dict[str, Any]:
        """
        Discovers and ingests all 13 PDFs and 2 structured datasets in the GUIDE directory.
        """
        existing_count = self.collection.count()
        if existing_count > 0 and not force_reload:
            self.ingestion_stats["total_chunks"] = existing_count
            return self.ingestion_stats

        all_files = list(guide_dir.glob("*.*"))
        all_chunks: List[DocumentChunk] = []

        for fpath in all_files:
            if fpath.suffix.lower() == ".pdf":
                chunks = parse_pdf_document(fpath)
                all_chunks.extend(chunks)
                self.ingestion_stats["files_indexed"].append(fpath.name)
            elif fpath.name.lower() in [
                "elevator_troubleshooting_dataset.csv",
                "elevator_troubleshooting_dataset.json",
            ]:
                chunks = parse_troubleshooting_dataset(fpath)
                all_chunks.extend(chunks)
                self.ingestion_stats["files_indexed"].append(fpath.name)

        if not all_chunks:
            return self.ingestion_stats

        # Prepare batch vectors and metadata for ChromaDB
        ids = []
        documents = []
        metadatas = []

        for chunk in all_chunks:
            self.raw_chunks[chunk.chunk_id] = chunk
            ids.append(chunk.chunk_id)
            documents.append(chunk.content)

            # Flatten metadata for Chroma (strings, ints, floats, bools)
            meta_dict = {
                "document_id": chunk.metadata.document_id,
                "filename": chunk.metadata.filename,
                "document_type": chunk.metadata.document_type.value,
                "authority": chunk.metadata.authority.value,
                "system": chunk.metadata.system or "General",
                "subsystem": chunk.metadata.subsystem or "General",
                "component": chunk.metadata.component or "",
                "egov_setting": chunk.metadata.egov_setting or "NONE",
                "page": chunk.metadata.page or 0,
                "section": chunk.metadata.section or "General",
                "data_type": chunk.metadata.data_type,
            }
            metadatas.append(meta_dict)

            # Update stats
            if chunk.metadata.data_type == "TABLE":
                self.ingestion_stats["table_chunks"] += 1
            elif chunk.metadata.data_type == "WARNING":
                self.ingestion_stats["warning_chunks"] += 1
            elif chunk.metadata.data_type == "PROCEDURE":
                self.ingestion_stats["procedure_chunks"] += 1

        # Add to collection in chunks of 250
        batch_size = 250
        for i in range(0, len(ids), batch_size):
            self.collection.add(
                ids=ids[i : i + batch_size],
                documents=documents[i : i + batch_size],
                metadatas=metadatas[i : i + batch_size],
            )

        self.ingestion_stats["total_files"] = len(self.ingestion_stats["files_indexed"])
        self.ingestion_stats["total_chunks"] = len(ids)
        return self.ingestion_stats

    def query(
        self,
        query_text: str,
        where_filter: Optional[Dict[str, Any]] = None,
        n_results: int = 5,
    ) -> List[Dict[str, Any]]:
        """
        Executes metadata-filtered vector query.
        """
        if self.collection.count() == 0:
            return []

        results = self.collection.query(
            query_texts=[query_text],
            where=where_filter,
            n_results=min(n_results, self.collection.count()),
        )

        formatted_results = []
        if not results or not results["ids"] or not results["ids"][0]:
            return []

        for i in range(len(results["ids"][0])):
            cid = results["ids"][0][i]
            doc = results["documents"][0][i]
            meta = results["metadatas"][0][i]
            dist = results["distances"][0][i] if "distances" in results and results["distances"] else 0.5
            similarity = max(0.0, 1.0 - dist)

            formatted_results.append({
                "chunk_id": cid,
                "content": doc,
                "metadata": meta,
                "similarity": similarity,
            })

        return formatted_results
