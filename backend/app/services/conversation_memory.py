from __future__ import annotations

import json
from collections import defaultdict, deque
from datetime import datetime, timezone
from typing import Any

from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models_sqlalchemy import ConversationTurn


class ConversationMemory:
    def __init__(self, session_factory: Any | None = None) -> None:
        self.session_factory = session_factory or SessionLocal
        self._store: dict[str, deque[dict[str, Any]]] = defaultdict(deque)

    def _serialize_context(self, context_documents: list[dict[str, Any]] | None) -> str:
        return json.dumps(context_documents or [], ensure_ascii=False)

    def add_turn(
        self,
        user_id: str,
        question: str,
        answer: str,
        provider: str | None = None,
        context_documents: list[dict[str, Any]] | None = None,
    ) -> dict[str, Any]:
        record = {
            "user_id": user_id,
            "question": question,
            "answer": answer,
            "provider": provider or "unknown",
            "context_documents": context_documents or [],
            "created_at": datetime.now(timezone.utc).isoformat(),
        }

        try:
            with self.session_factory() as session:
                turn = ConversationTurn(
                    user_id=user_id,
                    question=question,
                    answer=answer,
                    provider=provider or "unknown",
                    context_documents=self._serialize_context(context_documents),
                )
                session.add(turn)
                session.commit()
                session.refresh(turn)
                record["id"] = turn.id
        except Exception:
            self._store[user_id].append(record)
            while len(self._store[user_id]) > 20:
                self._store[user_id].popleft()

        return record

    def get_recent(self, user_id: str, limit: int = 10) -> list[dict[str, Any]]:
        try:
            with self.session_factory() as session:
                rows = (
                    session.query(ConversationTurn)
                    .filter(ConversationTurn.user_id == user_id)
                    .order_by(ConversationTurn.id.desc())
                    .limit(limit)
                    .all()
                )
                return [
                    {
                        "id": row.id,
                        "user_id": str(row.user_id),
                        "question": row.question,
                        "answer": row.answer,
                        "provider": row.provider,
                        "context_documents": json.loads(row.context_documents or "[]"),
                        "created_at": row.created_at.isoformat() if row.created_at else None,
                    }
                    for row in rows
                ][::-1]
        except Exception:
            return list(self._store.get(user_id, []))[-limit:]
