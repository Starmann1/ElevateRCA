"""
ElevateRCA — ChromaDB Vector Store for GUIDE Corpus
Manages embedding, indexing, and retrieval from the GUIDE document corpus.
Uses ChromaDB PersistentClient per ADR-009.
"""

import os
import logging
import hashlib
from typing import List, Dict, Any, Optional

from pipeline.rag_schemas import RAGChunk, AUTHORITY_LEVELS

logger = logging.getLogger("elevaterca.rag.store")


# =====================================================
# EMBEDDING FUNCTION — Native ChromaDB SentenceTransformers Singleton
# =====================================================

_SHARED_EF = None


def get_sentence_transformer_ef(model_name: str = "all-MiniLM-L6-v2"):
    """Get or create singleton native SentenceTransformerEmbeddingFunction."""
    global _SHARED_EF
    if _SHARED_EF is None:
        try:
            import os
            # Prevent slow external network checks since weights are already cached locally
            os.environ.setdefault("HF_HUB_OFFLINE", "1")
            os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")
            import chromadb.utils.embedding_functions as ef
            _SHARED_EF = ef.SentenceTransformerEmbeddingFunction(model_name=model_name)
            logger.info(f"Initialized native ChromaDB SentenceTransformerEmbeddingFunction: {model_name}")
        except Exception as e:
            logger.warning(f"Could not initialize SentenceTransformerEmbeddingFunction: {e}")
            _SHARED_EF = None
    return _SHARED_EF


# =====================================================
# RAG VECTOR STORE — ChromaDB-backed document index
# =====================================================

class RAGVectorStore:
    """ChromaDB-backed vector store for GUIDE corpus chunks.
    
    Supports:
    - Persistent storage (survives restarts)
    - Metadata-filtered queries
    - Hybrid retrieval (semantic + metadata filters)
    - Authority-ranked results
    """

    COLLECTION_NAME = "elevaterca_guide_corpus"

    def __init__(
        self,
        persist_dir: str = ".chroma_db",
        embedding_model: str = "all-MiniLM-L6-v2"
    ):
        self.persist_dir = persist_dir
        self.embedding_model = embedding_model
        self._client = None
        self._collection = None
        self._embed_fn = get_sentence_transformer_ef(embedding_model)
        self._initialized = False

    def _ensure_initialized(self):
        """Lazy initialization of ChromaDB client and collection."""
        if self._initialized:
            return

        try:
            import chromadb
            from chromadb.config import Settings

            os.makedirs(self.persist_dir, exist_ok=True)

            self._client = chromadb.PersistentClient(
                path=self.persist_dir,
                settings=Settings(anonymized_telemetry=False)
            )

            # Create or get the collection with native embedding function
            if self._embed_fn is not None:
                self._collection = self._client.get_or_create_collection(
                    name=self.COLLECTION_NAME,
                    embedding_function=self._embed_fn,
                    metadata={"hnsw:space": "cosine"}
                )
            else:
                self._collection = self._client.get_or_create_collection(
                    name=self.COLLECTION_NAME,
                    metadata={"hnsw:space": "cosine"}
                )

            self._initialized = True
            logger.info(f"ChromaDB initialized at {self.persist_dir}, "
                        f"collection '{self.COLLECTION_NAME}' has {self._collection.count()} documents")

        except ImportError:
            logger.error("chromadb not installed. Run: pip install chromadb")
            raise
        except Exception as e:
            logger.error(f"Failed to initialize ChromaDB: {e}")
            raise

    @property
    def is_indexed(self) -> bool:
        """Check if the corpus has been indexed."""
        try:
            self._ensure_initialized()
            return self._collection.count() > 0
        except Exception:
            return False

    @property
    def document_count(self) -> int:
        """Number of indexed chunks."""
        try:
            self._ensure_initialized()
            return self._collection.count()
        except Exception:
            return 0

    def index_chunks(self, chunks: List[RAGChunk], batch_size: int = 100) -> int:
        """Index a list of RAGChunks into ChromaDB.
        
        Returns the number of chunks indexed.
        """
        self._ensure_initialized()

        if not chunks:
            logger.warning("No chunks to index")
            return 0

        indexed = 0
        for i in range(0, len(chunks), batch_size):
            batch = chunks[i:i + batch_size]
            ids = []
            documents = []
            metadatas = []

            for chunk in batch:
                ids.append(chunk.chunk_id)
                documents.append(chunk.text)
                metadatas.append(self._chunk_to_metadata(chunk))

            try:
                self._collection.upsert(
                    ids=ids,
                    documents=documents,
                    metadatas=metadatas
                )
                indexed += len(batch)
            except Exception as e:
                logger.error(f"Error indexing batch {i}-{i + len(batch)}: {e}")

        logger.info(f"Indexed {indexed} chunks into ChromaDB")
        return indexed

    def query(
        self,
        query_text: str,
        n_results: int = 10,
        subsystem: Optional[str] = None,
        component: Optional[str] = None,
        authority: Optional[str] = None,
        egov: Optional[str] = None,
        configuration: Optional[str] = None,
        document_type: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """Query the vector store with semantic search and metadata filters.
        
        Returns list of results with text, metadata, and relevance scores.
        """
        self._ensure_initialized()

        if self._collection.count() == 0:
            return []

        # Build metadata filter
        where_filter = self._build_filter(
            subsystem=subsystem,
            component=component,
            authority=authority,
            egov=egov,
            configuration=configuration,
            document_type=document_type,
        )

        try:
            query_params = {
                "query_texts": [query_text],
                "n_results": min(n_results, self._collection.count()),
            }
            if where_filter:
                query_params["where"] = where_filter

            results = self._collection.query(**query_params)

            return self._format_results(results)

        except Exception as e:
            logger.error(f"Query error: {e}")
            # Retry without filter if filter caused the error
            if where_filter:
                try:
                    results = self._collection.query(
                        query_texts=[query_text],
                        n_results=min(n_results, self._collection.count()),
                    )
                    return self._format_results(results)
                except Exception as e2:
                    logger.error(f"Fallback query also failed: {e2}")
            return []

    def keyword_search(
        self,
        keywords: List[str],
        n_results: int = 10,
        subsystem: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """Perform keyword-based search using ChromaDB's document contains filter.
        Uses collection.get() for zero-overhead document filtering without vector re-computation.
        """
        self._ensure_initialized()

        if self._collection.count() == 0:
            return []

        all_results: List[Dict[str, Any]] = []

        for keyword in keywords:
            try:
                where_doc = {"$contains": keyword}
                where_filter = None
                if subsystem:
                    where_filter = {"subsystem": subsystem}

                get_params = {
                    "where_document": where_doc,
                    "limit": min(n_results, self._collection.count()),
                }
                if where_filter:
                    get_params["where"] = where_filter

                results = self._collection.get(**get_params)
                formatted = self._format_get_results(results)
                all_results.extend(formatted)

            except Exception as e:
                logger.debug(f"Keyword search for '{keyword}' failed: {e}")
                continue

        # Deduplicate by chunk_id
        seen = set()
        unique_results = []
        for r in all_results:
            cid = r.get("chunk_id", "")
            if cid not in seen:
                seen.add(cid)
                unique_results.append(r)

        return unique_results[:n_results]

    @staticmethod
    def _format_get_results(get_results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Format collection.get() results into structured dicts with fixed high relevance."""
        formatted = []
        if not get_results or not get_results.get("ids"):
            return formatted

        ids = get_results.get("ids", [])
        documents = get_results.get("documents", []) or []
        metadatas = get_results.get("metadatas", []) or []

        for i in range(len(ids)):
            meta = metadatas[i] if i < len(metadatas) else {}
            text = documents[i] if i < len(documents) else ""

            formatted.append({
                "chunk_id": ids[i],
                "text": text,
                "relevance_score": 0.85,
                "filename": meta.get("filename", ""),
                "page": meta.get("page", 0),
                "section": meta.get("section", ""),
                "authority": meta.get("authority", ""),
                "subsystem": meta.get("subsystem", ""),
                "component": meta.get("component", ""),
                "egov": meta.get("egov", ""),
                "configuration": meta.get("configuration", ""),
                "document_type": meta.get("document_type", ""),
                "is_table": meta.get("is_table", False),
                "is_procedure": meta.get("is_procedure", False),
                "is_warning": meta.get("is_warning", False),
            })
        return formatted

    def clear(self):
        """Clear the entire collection (for reindexing)."""
        self._ensure_initialized()
        try:
            self._client.delete_collection(self.COLLECTION_NAME)
            # Recreate empty collection
            if self._embed_fn is not None:
                self._collection = self._client.create_collection(
                    name=self.COLLECTION_NAME,
                    embedding_function=self._embed_fn,
                    metadata={"hnsw:space": "cosine"}
                )
            else:
                self._collection = self._client.create_collection(
                    name=self.COLLECTION_NAME,
                    metadata={"hnsw:space": "cosine"}
                )
            logger.info("ChromaDB collection cleared and recreated")
        except Exception as e:
            logger.error(f"Error clearing collection: {e}")

    def get_index_stats(self) -> Dict[str, Any]:
        """Get statistics about the indexed corpus."""
        self._ensure_initialized()
        count = self._collection.count()

        # Sample some metadata to understand coverage
        subsystems = set()
        authorities = set()
        filenames = set()

        if count > 0:
            try:
                sample = self._collection.get(include=["metadatas"])
                for meta in (sample.get("metadatas") or []):
                    if meta.get("subsystem"):
                        subsystems.add(meta["subsystem"])
                    if meta.get("authority"):
                        authorities.add(meta["authority"])
                    if meta.get("filename"):
                        filenames.add(meta["filename"])
            except Exception:
                pass

        return {
            "total_chunks": count,
            "subsystems_covered": sorted(subsystems),
            "authority_levels": sorted(authorities),
            "documents_indexed": sorted(filenames),
            "persist_dir": self.persist_dir,
        }

    # =====================================================
    # INTERNAL HELPERS
    # =====================================================

    @staticmethod
    def _chunk_to_metadata(chunk: RAGChunk) -> Dict[str, Any]:
        """Convert RAGChunk fields to ChromaDB metadata dict.
        ChromaDB requires metadata values to be str, int, float, or bool.
        """
        meta = {
            "filename": chunk.filename,
            "document_id": chunk.document_id,
            "page": chunk.page,
            "source_type": chunk.source_type,
            "authority": chunk.authority,
            "manufacturer": chunk.manufacturer,
            "is_table": chunk.is_table,
            "is_procedure": chunk.is_procedure,
            "is_warning": chunk.is_warning,
        }

        # Add optional fields only if they have values
        if chunk.subsystem:
            meta["subsystem"] = chunk.subsystem
        if chunk.component:
            meta["component"] = chunk.component
        if chunk.system:
            meta["system"] = chunk.system
        if chunk.document_type:
            meta["document_type"] = chunk.document_type
        if chunk.egov:
            meta["egov"] = chunk.egov
        if chunk.configuration:
            meta["configuration"] = chunk.configuration
        if chunk.section:
            meta["section"] = chunk.section[:200]  # Truncate long sections

        return meta

    @staticmethod
    def _build_filter(
        subsystem: Optional[str] = None,
        component: Optional[str] = None,
        authority: Optional[str] = None,
        egov: Optional[str] = None,
        configuration: Optional[str] = None,
        document_type: Optional[str] = None,
    ) -> Optional[Dict[str, Any]]:
        """Build ChromaDB where filter from parameters."""
        conditions = []

        if subsystem:
            conditions.append({"subsystem": subsystem})
        if component:
            conditions.append({"component": component})
        if authority:
            conditions.append({"authority": authority})
        if egov:
            conditions.append({"egov": egov})
        if configuration:
            conditions.append({"configuration": configuration})
        if document_type:
            conditions.append({"document_type": document_type})

        if not conditions:
            return None
        if len(conditions) == 1:
            return conditions[0]
        return {"$and": conditions}

    @staticmethod
    def _format_results(raw_results: Dict) -> List[Dict[str, Any]]:
        """Format raw ChromaDB results into structured dicts."""
        formatted = []

        if not raw_results or not raw_results.get("ids"):
            return formatted

        ids = raw_results["ids"][0] if raw_results["ids"] else []
        documents = raw_results["documents"][0] if raw_results.get("documents") else []
        metadatas = raw_results["metadatas"][0] if raw_results.get("metadatas") else []
        distances = raw_results["distances"][0] if raw_results.get("distances") else []

        for i in range(len(ids)):
            # Convert cosine distance to similarity score
            distance = distances[i] if i < len(distances) else 1.0
            similarity = max(0.0, 1.0 - distance)

            meta = metadatas[i] if i < len(metadatas) else {}
            text = documents[i] if i < len(documents) else ""

            formatted.append({
                "chunk_id": ids[i],
                "text": text,
                "relevance_score": round(similarity, 4),
                "filename": meta.get("filename", ""),
                "page": meta.get("page", 0),
                "section": meta.get("section", ""),
                "authority": meta.get("authority", ""),
                "subsystem": meta.get("subsystem", ""),
                "component": meta.get("component", ""),
                "egov": meta.get("egov", ""),
                "configuration": meta.get("configuration", ""),
                "document_type": meta.get("document_type", ""),
                "is_table": meta.get("is_table", False),
                "is_procedure": meta.get("is_procedure", False),
                "is_warning": meta.get("is_warning", False),
            })

        # Sort by relevance score descending, then by authority level
        formatted.sort(
            key=lambda x: (
                x["relevance_score"],
                -AUTHORITY_LEVELS.get(x["authority"], 5)
            ),
            reverse=True
        )

        return formatted
