from __future__ import annotations

import json
import logging
import math
import os
import time
from typing import Any, Iterable

logger = logging.getLogger(__name__)

try:
    from qdrant_client import QdrantClient
    from qdrant_client.http import models as qmodels
except Exception:  # pragma: no cover - optional dependency
    QdrantClient = None
    qmodels = None


class QdrantVectorStore:
    def __init__(
        self,
        collection_name: str = "jobhunter_vectors",
        url: str | None = None,
        api_key: str | None = None,
        vector_size: int = 768,
        use_memory_fallback: bool = False,
    ) -> None:
        self.collection_name = collection_name or "jobhunter_vectors"
        self.url = url or os.getenv("QDRANT_URL", "http://localhost:6333")
        self.api_key = api_key or os.getenv("QDRANT_API_KEY", "")
        self.vector_size = int(os.getenv("QDRANT_VECTOR_SIZE", str(vector_size)))
        self.use_memory_fallback = use_memory_fallback or QdrantClient is None
        self.client = None
        self._memory_store: list[dict[str, Any]] = []

        if not self.use_memory_fallback:
            try:
                self.client = QdrantClient(url=self.url, api_key=self.api_key or None)
                self._ensure_collection()
            except Exception as exc:  # pragma: no cover - environment dependent
                logger.warning("Qdrant unavailable, using in-memory fallback: %s", exc)
                self.use_memory_fallback = True

    def _ensure_collection(self) -> None:
        if self.use_memory_fallback or self.client is None:
            return
        try:
            collections = self.client.get_collections().collections
            names = {item.name for item in collections}
            if self.collection_name not in names:
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=qmodels.VectorParams(size=self.vector_size, distance="cosine"),
                )
        except Exception as exc:  # pragma: no cover - environment dependent
            logger.warning("Unable to create Qdrant collection %s: %s", self.collection_name, exc)
            self.use_memory_fallback = True

    def delete_collection(self) -> None:
        if self.client is not None:
            try:
                self.client.delete_collection(self.collection_name)
                self._memory_store = []
                return
            except Exception as exc:  # pragma: no cover
                logger.warning("Failed to delete collection %s: %s", self.collection_name, exc)
        self._memory_store = []

    def _memory_document(self, document: dict[str, Any], vector: list[float]) -> dict[str, Any]:
        payload = {
            "id": str(document.get("id", "doc")),
            "user_id": str(document.get("user_id", "anonymous")),
            "document_type": str(document.get("document_type", "unknown")),
            "source_id": str(document.get("source_id", "unknown")),
            "content": str(document.get("content", "")),
            "created_at": document.get("created_at") or document.get("metadata", {}).get("created_at"),
            "metadata": document.get("metadata", {}),
        }
        return {
            "id": payload["id"],
            "vector": vector,
            "payload": payload,
        }

    def upsert_document(self, document: dict[str, Any], vector: list[float]) -> dict[str, Any]:
        start = time.monotonic()
        doc_id = str(document.get("id", "doc"))
        payload = {
            "id": doc_id,
            "user_id": str(document.get("user_id", "anonymous")),
            "document_type": str(document.get("document_type", "unknown")),
            "source_id": str(document.get("source_id", "unknown")),
            "content": str(document.get("content", "")),
            "created_at": document.get("created_at") or document.get("metadata", {}).get("created_at"),
            "metadata": document.get("metadata", {}),
        }

        if self.client is not None and not self.use_memory_fallback:
            try:
                self.client.upsert(
                    collection_name=self.collection_name,
                    points=[
                        {
                            "id": doc_id,
                            "vector": vector,
                            "payload": payload,
                        }
                    ],
                )
                elapsed_ms = round((time.monotonic() - start) * 1000, 2)
                logger.info(
                    "qdrant.upsert",
                    extra={
                        "collection": self.collection_name,
                        "document_id": doc_id,
                        "user_id": payload["user_id"],
                        "document_type": payload["document_type"],
                        "duration_ms": elapsed_ms,
                    },
                )
                return {"status": "ok", "id": doc_id, "collection": self.collection_name}
            except Exception as exc:  # pragma: no cover
                logger.warning(
                    "qdrant.upsert.error",
                    extra={"collection": self.collection_name, "document_id": doc_id, "error": str(exc)},
                )
                self.use_memory_fallback = True

        memory_item = self._memory_document(document, vector)
        existing = [item for item in self._memory_store if item["id"] == doc_id and item["payload"]["user_id"] == payload["user_id"]]
        if existing:
            self._memory_store = [item for item in self._memory_store if item["id"] != doc_id or item["payload"]["user_id"] != payload["user_id"]]
        self._memory_store.append(memory_item)
        elapsed_ms = round((time.monotonic() - start) * 1000, 2)
        logger.info(
            "qdrant.upsert.fallback",
            extra={
                "collection": self.collection_name,
                "document_id": doc_id,
                "user_id": payload["user_id"],
                "document_type": payload["document_type"],
                "duration_ms": elapsed_ms,
            },
        )
        return {"status": "ok", "id": doc_id, "collection": self.collection_name, "fallback": True}

    def delete_document(self, document_id: str, user_id: str | None = None) -> dict[str, Any]:
        if self.client is not None and not self.use_memory_fallback:
            try:
                if user_id:
                    self.client.delete(
                        collection_name=self.collection_name,
                        points_selector=qmodels.Filter(
                            must=[
                                qmodels.FieldCondition(key="user_id", match=qmodels.MatchValue(value=user_id)),
                                qmodels.FieldCondition(key="id", match=qmodels.MatchValue(value=document_id)),
                            ]
                        ),
                    )
                else:
                    self.client.delete(
                        collection_name=self.collection_name,
                        points_selector=document_id,
                    )
                return {"status": "ok", "deleted": True, "id": document_id}
            except Exception as exc:  # pragma: no cover
                logger.warning("Qdrant delete failed for %s: %s", document_id, exc)
                self.use_memory_fallback = True

        filtered = []
        deleted = False
        for item in self._memory_store:
            keep = item["id"] != document_id
            if user_id is not None and item["payload"].get("user_id") != str(user_id):
                keep = True
            if not keep:
                deleted = True
            if keep:
                filtered.append(item)
        self._memory_store = filtered
        return {"status": "ok", "deleted": deleted, "id": document_id, "fallback": True}

    def search(
        self,
        vector: list[float],
        user_id: str | None = None,
        limit: int = 5,
        score_threshold: float = 0.0,
    ) -> dict[str, Any]:
        start = time.monotonic()
        if self.client is not None and not self.use_memory_fallback:
            try:
                query_filter = None
                if user_id:
                    query_filter = qmodels.Filter(
                        must=[qmodels.FieldCondition(key="user_id", match=qmodels.MatchValue(value=user_id))]
                    )
                hits = self.client.search(
                    collection_name=self.collection_name,
                    query_vector=vector,
                    query_filter=query_filter,
                    limit=limit,
                    with_payload=True,
                    with_vectors=False,
                )
                results = []
                for hit in hits:
                    score = float(hit.score or 0.0)
                    if score < score_threshold:
                        continue
                    payload = hit.payload or {}
                    results.append(
                        {
                            "id": str(hit.id),
                            "score": score,
                            "user_id": payload.get("user_id"),
                            "document_type": payload.get("document_type"),
                            "source_id": payload.get("source_id"),
                            "content": payload.get("content"),
                            "metadata": payload.get("metadata", {}),
                            "created_at": payload.get("created_at"),
                        }
                    )
                elapsed_ms = round((time.monotonic() - start) * 1000, 2)
                logger.info(
                    "qdrant.search",
                    extra={
                        "collection": self.collection_name,
                        "user_id": user_id,
                        "limit": limit,
                        "result_count": len(results),
                        "duration_ms": elapsed_ms,
                    },
                )
                return {"status": "ok", "results": results, "collection": self.collection_name}
            except Exception as exc:  # pragma: no cover
                logger.warning(
                    "qdrant.search.error",
                    extra={"collection": self.collection_name, "user_id": user_id, "error": str(exc)},
                )
                self.use_memory_fallback = True

        filtered = [item for item in self._memory_store if user_id is None or item["payload"].get("user_id") == str(user_id)]
        results = []
        for item in filtered:
            score = self._cosine_similarity(vector, item["vector"])
            if score < score_threshold:
                continue
            payload = item["payload"]
            results.append(
                {
                    "id": item["id"],
                    "score": score,
                    "user_id": payload.get("user_id"),
                    "document_type": payload.get("document_type"),
                    "source_id": payload.get("source_id"),
                    "content": payload.get("content"),
                    "metadata": payload.get("metadata", {}),
                    "created_at": payload.get("created_at"),
                }
            )
        results.sort(key=lambda item: item["score"], reverse=True)
        elapsed_ms = round((time.monotonic() - start) * 1000, 2)
        logger.info(
            "qdrant.search.fallback",
            extra={
                "collection": self.collection_name,
                "user_id": user_id,
                "limit": limit,
                "result_count": len(results[:limit]),
                "duration_ms": elapsed_ms,
            },
        )
        return {"status": "ok", "results": results[:limit], "collection": self.collection_name, "fallback": True}

    @staticmethod
    def _cosine_similarity(v1: list[float], v2: list[float]) -> float:
        if not v1 or not v2 or len(v1) != len(v2):
            return 0.0
        dot = sum(a * b for a, b in zip(v1, v2))
        norm_a = math.sqrt(sum(a * a for a in v1))
        norm_b = math.sqrt(sum(b * b for b in v2))
        if not norm_a or not norm_b:
            return 0.0
        return dot / (norm_a * norm_b)
