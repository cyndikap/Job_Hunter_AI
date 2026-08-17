from __future__ import annotations

from typing import Any


class RAGService:
    def __init__(self):
        self.documents: list[dict[str, Any]] = []

    def ingest(self, documents: list[dict[str, Any]]) -> None:
        self.documents.extend(documents)

    def search(self, query: str, limit: int = 5) -> list[dict[str, Any]]:
        query_lower = query.lower()
        hits = []
        for item in self.documents:
            text = " ".join(str(value).lower() for value in item.values() if value is not None)
            if query_lower in text:
                hits.append(item)
        return hits[:limit]


rag_service = RAGService()
