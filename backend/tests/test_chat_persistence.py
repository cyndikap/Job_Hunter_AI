from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.services.conversation_memory import ConversationMemory


def test_conversation_memory_persists_retrieves_turns():
    engine = create_engine("sqlite:///:memory:")
    SessionLocal = sessionmaker(bind=engine)
    memory = ConversationMemory(session_factory=SessionLocal)

    record = memory.add_turn(
        user_id="user-88",
        question="Quels sont mes meilleurs atouts ?",
        answer="Votre profil est fort sur Azure et SQL.",
        provider="ollama",
        context_documents=[{"id": "doc-1", "document_type": "cv", "score": 0.91}],
    )

    assert record["user_id"] == "user-88"
    rows = memory.get_recent("user-88", limit=5)
    assert rows[0]["answer"] == "Votre profil est fort sur Azure et SQL."
    assert rows[0]["provider"] == "ollama"
