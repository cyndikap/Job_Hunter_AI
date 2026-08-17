from app.services.chat_service import ChatService


def test_rag_chat_flow_keeps_user_isolation_and_produces_context():
    class FakePipeline:
        def build_context(self, query, user_id, limit=5):
            assert user_id == "user-10"
            return {
                "context_text": "Contexte de user-10: Azure, Data Engineering, Databricks.",
                "documents": [
                    {"id": "doc-x", "document_type": "cv", "score": 0.88, "content": "Azure Databricks"}
                ],
                "justification": [{"document_id": "doc-x", "document_type": "cv", "score": 0.88}],
            }

    class FakeLLM:
        def generate_response(self, query, context, user_id):
            assert user_id == "user-10"
            assert "Azure" in context
            return {
                "answer": "Votre profil met en avant Azure et Databricks.",
                "provider": "ollama",
                "response_time_ms": 432,
                "sources": [{"id": "doc-x", "document_type": "cv", "score": 0.88}],
            }

    service = ChatService(rag_pipeline=FakePipeline(), llm_provider=FakeLLM())
    result = service.chat("Quels sont mes points forts ?", user_id="user-10")

    assert result["answer"].startswith("Votre profil met")
    assert all(item["document_type"] == "cv" for item in result["sources"])
    assert result["provider"] == "ollama"
