from app.services.chat_service import ChatService


def test_chat_service_uses_rag_context_and_returns_sources(monkeypatch):
    class FakeLLM:
        def generate_response(self, query, context, user_id):
            assert user_id == "user-7"
            assert "Azure" in context
            return {
                "answer": "Réponse contextualisée",
                "provider": "ollama",
                "response_time_ms": 120,
                "sources": [
                    {"id": "doc-1", "document_type": "cv", "score": 0.92, "content": "Azure Data Engineer"}
                ],
            }

    class FakePipeline:
        def build_context(self, query, user_id, limit=5):
            return {
                "context_text": "Azure Data Engineer profile and Databricks experience.",
                "documents": [
                    {"id": "doc-1", "document_type": "cv", "score": 0.92, "content": "Azure Data Engineer"}
                ],
                "justification": [{"document_id": "doc-1", "document_type": "cv", "score": 0.92}],
            }

    service = ChatService(rag_pipeline=FakePipeline(), llm_provider=FakeLLM())
    result = service.chat("Parle-moi de mon profil", user_id="user-7")

    assert result["answer"] == "Réponse contextualisée"
    assert result["provider"] == "ollama"
    assert result["sources"][0]["document_type"] == "cv"
