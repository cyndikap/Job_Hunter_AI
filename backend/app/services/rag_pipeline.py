from __future__ import annotations

import logging
import re
import time
from datetime import datetime, timezone
from typing import Any

from app.services.embedding_service import embedding_service
from app.services.vector_store import QdrantVectorStore

logger = logging.getLogger(__name__)


class RAGPipeline:
    def __init__(
        self,
        vector_store: QdrantVectorStore | None = None,
        embedding_service_instance=None,
        use_memory_fallback: bool = False,
    ) -> None:
        self.vector_store = vector_store or QdrantVectorStore(use_memory_fallback=use_memory_fallback)
        self.embedding_service = embedding_service_instance or embedding_service

    @staticmethod
    def clean_text(text: str) -> str:
        cleaned = re.sub(r"\s+", " ", (text or "").replace("\r", " ").replace("\n", " "))
        return cleaned.strip()

    @staticmethod
    def chunk_text(text: str, chunk_size: int = 800, overlap: int = 120) -> list[str]:
        cleaned = RAGPipeline.clean_text(text)
        if not cleaned:
            return []
        chunks: list[str] = []
        start = 0
        while start < len(cleaned):
            end = min(start + chunk_size, len(cleaned))
            chunk = cleaned[start:end]
            chunks.append(chunk)
            if end == len(cleaned):
                break
            start = max(end - overlap, start + 1)
        return chunks

    @staticmethod
    def _resolve_user_id(document: dict[str, Any], fallback_user_id: str | None = None) -> str:
        return str(document.get("user_id") or fallback_user_id or "anonymous")

    def index_documents(self, documents: list[dict[str, Any]], fallback_user_id: str | None = None) -> dict[str, Any]:
        start_total = time.monotonic()
        indexed_count = 0
        for document in documents:
            user_id = self._resolve_user_id(document, fallback_user_id)
            document_type = str(document.get("document_type") or "unknown")
            source_id = str(document.get("source_id") or document.get("id") or "source")
            created_at = document.get("created_at") or datetime.now(timezone.utc).isoformat()
            content = str(document.get("content") or "")
            chunks = self.chunk_text(content)
            if not chunks:
                chunks = [""]
            for chunk_index, chunk in enumerate(chunks):
                chunk_payload = {
                    "id": f"{document.get('id', source_id)}-{chunk_index}",
                    "user_id": user_id,
                    "document_type": document_type,
                    "source_id": source_id,
                    "content": chunk,
                    "created_at": created_at,
                    "metadata": {
                        "title": document.get("title") or document.get("name") or document_type,
                        "author": document.get("author"),
                        "source": document.get("source"),
                    },
                }
                embed_start = time.monotonic()
                embedding = self.embedding_service.get_embedding(chunk)
                embed_duration_ms = round((time.monotonic() - embed_start) * 1000, 2)
                logger.info(
                    "rag.embedding",
                    extra={
                        "user_id": user_id,
                        "document_type": document_type,
                        "source_id": source_id,
                        "duration_ms": embed_duration_ms,
                        "chunk_index": chunk_index,
                    },
                )
                self.vector_store.upsert_document(chunk_payload, embedding)
                indexed_count += 1

        total_duration_ms = round((time.monotonic() - start_total) * 1000, 2)
        logger.info(
            "rag.index.summary",
            extra={
                "collection": self.vector_store.collection_name,
                "indexed_count": indexed_count,
                "duration_ms": total_duration_ms,
            },
        )
        return {"status": "ok", "indexed_count": indexed_count, "collection": self.vector_store.collection_name}

    def search(self, query: str, user_id: str, limit: int = 5) -> dict[str, Any]:
        if not user_id:
            raise ValueError("user_id is required for vector search")
        start = time.monotonic()
        query_vector = self.embedding_service.get_embedding(query)
        hits = self.vector_store.search(vector=query_vector, user_id=user_id, limit=limit)
        duration_ms = round((time.monotonic() - start) * 1000, 2)
        logger.info(
            "rag.search",
            extra={
                "user_id": user_id,
                "limit": limit,
                "result_count": len(hits.get("results", [])),
                "duration_ms": duration_ms,
            },
        )
        return {
            "query": query,
            "user_id": user_id,
            "documents": [
                {
                    "id": item["id"],
                    "score": item["score"],
                    "document_type": item["document_type"],
                    "source_id": item["source_id"],
                    "content": item["content"],
                    "metadata": item["metadata"],
                    "created_at": item["created_at"],
                }
                for item in hits.get("results", [])
            ],
            "total": len(hits.get("results", [])),
        }

    def build_context(self, query: str, user_id: str, limit: int = 5) -> dict[str, Any]:
        search_result = self.search(query, user_id=user_id, limit=limit)
        documents = search_result["documents"]
        context_text = "\n\n---\n\n".join(item["content"] for item in documents if item.get("content"))
        justification = [
            {
                "document_id": item["id"],
                "score": item["score"],
                "document_type": item["document_type"],
                "excerpt": item["content"][:250],
            }
            for item in documents
        ]
        return {
            "query": query,
            "user_id": user_id,
            "documents": documents,
            "context_text": context_text,
            "justification": justification,
        }
