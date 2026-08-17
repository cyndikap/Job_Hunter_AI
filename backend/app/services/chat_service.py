from __future__ import annotations

from typing import Any

from app.prompts.system_prompt import build_system_prompt
from app.services.conversation_memory import ConversationMemory
from app.services.llm_monitoring import LLMMonitoring
from app.services.llm_provider import llm_provider as default_llm_provider
from app.services.rag_pipeline import RAGPipeline


class ChatService:
    def __init__(
        self,
        rag_pipeline: RAGPipeline | None = None,
        llm_provider: Any | None = None,
        conversation_memory: ConversationMemory | None = None,
        llm_monitoring: LLMMonitoring | None = None,
    ) -> None:
        self.rag_pipeline = rag_pipeline or RAGPipeline()
        self.llm_provider = llm_provider or default_llm_provider
        self.conversation_memory = conversation_memory or ConversationMemory()
        self.llm_monitoring = llm_monitoring or LLMMonitoring()

    def _generate_llm_response(self, query: str, context: str, user_id: str) -> dict[str, Any]:
        if hasattr(self.llm_provider, "generate_response"):
            return self.llm_provider.generate_response(query, context, user_id)
        return self.llm_provider.generate(question=query, context=context, user_id=user_id)

    def chat(self, query: str, user_id: str, limit: int = 5) -> dict[str, Any]:
        if not query or not str(query).strip():
            raise ValueError("query is required")
        if not user_id:
            raise ValueError("user_id is required")

        normalized_query = str(query).strip()
        rag_context = self.rag_pipeline.build_context(normalized_query, user_id=user_id, limit=limit)
        context_text = rag_context.get("context_text") or ""
        llm_result = self._generate_llm_response(normalized_query, context_text, user_id)

        if not isinstance(llm_result, dict):
            llm_result = {"answer": str(llm_result), "provider": "unknown", "response_time_ms": 0, "sources": []}

        llm_result.setdefault("answer", "")
        llm_result.setdefault("provider", "unknown")
        llm_result.setdefault("response_time_ms", 0)
        llm_result.setdefault("sources", [])

        documents = rag_context.get("documents", [])
        sources = llm_result.get("sources") or [
            {
                "id": item.get("id"),
                "document_type": item.get("document_type"),
                "score": item.get("score"),
                "content": item.get("content"),
                "source_id": item.get("source_id"),
            }
            for item in documents
        ]

        self.conversation_memory.add_turn(
            user_id=user_id,
            question=normalized_query,
            answer=str(llm_result["answer"]),
            provider=str(llm_result["provider"]),
            context_documents=sources,
        )
        self.llm_monitoring.record_request(provider=str(llm_result["provider"]), duration_ms=float(llm_result.get("response_time_ms") or 0))

        if llm_result.get("error"):
            self.llm_monitoring.record_error(str(llm_result["error"]))

        return {
            "answer": str(llm_result["answer"]),
            "provider": str(llm_result["provider"]),
            "response_time_ms": float(llm_result.get("response_time_ms") or 0),
            "sources": sources,
            "user_id": user_id,
            "context": {
                "documents": documents,
                "justification": rag_context.get("justification", []),
            },
            "system_prompt": build_system_prompt(normalized_query, context_text),
        }


chat_service = ChatService()
