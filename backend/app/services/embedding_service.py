from __future__ import annotations

import hashlib
import json
import logging
import os
from typing import Any

import httpx

logger = logging.getLogger(__name__)

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_EMBED_MODEL = os.getenv("OLLAMA_EMBED_MODEL", "nomic-embed-text")
DEFAULT_VECTOR_SIZE = int(os.getenv("QDRANT_VECTOR_SIZE", "768"))


class EmbeddingService:
    def __init__(self, model: str | None = None, base_url: str | None = None):
        self.model = model or OLLAMA_EMBED_MODEL
        self.base_url = (base_url or OLLAMA_BASE_URL).rstrip("/")

    def get_embedding(self, text: str) -> list[float]:
        normalized = (text or "").strip()
        if not normalized:
            return [0.0 for _ in range(DEFAULT_VECTOR_SIZE)]

        try:
            response = httpx.post(
                f"{self.base_url}/api/embeddings",
                json={"model": self.model, "prompt": normalized},
                timeout=15,
            )
            response.raise_for_status()
            payload = response.json()
            embedding = payload.get("embedding")
            if isinstance(embedding, list) and embedding:
                return [float(value) for value in embedding]
        except Exception as exc:  # pragma: no cover - dependency optional
            logger.warning("Ollama embedding failed, using deterministic fallback: %s", exc)

        return self._hash_fallback_embedding(normalized)

    def _hash_fallback_embedding(self, text: str) -> list[float]:
        digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
        vector: list[float] = []
        for index in range(DEFAULT_VECTOR_SIZE):
            value = int(digest[(index * 2) % len(digest):(index * 2 + 2) % len(digest) or len(digest)], 16)
            vector.append((value / 255.0) * 2.0 - 1.0)
        return vector


embedding_service = EmbeddingService()
