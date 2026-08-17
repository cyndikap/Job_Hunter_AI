from __future__ import annotations

import logging
import os
import time
from typing import Any

import httpx

logger = logging.getLogger(__name__)


class LLMProvider:
    def __init__(
        self,
        ollama_base_url: str | None = None,
        ollama_model: str | None = None,
        mistral_api_key: str | None = None,
        mistral_model: str | None = None,
        max_retries: int | None = None,
        retry_backoff_seconds: float | None = None,
    ) -> None:
        self.ollama_base_url = (ollama_base_url or os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")).rstrip("/")
        self.ollama_model = ollama_model or os.getenv("OLLAMA_MODEL", "llama3.2")
        self.mistral_api_key = mistral_api_key or os.getenv("MISTRAL_API_KEY", "")
        self.mistral_model = mistral_model or os.getenv("MISTRAL_MODEL", "mistral-small-latest")
        self.max_retries = int(max_retries if max_retries is not None else os.getenv("LLM_MAX_RETRIES", "2"))
        self.retry_backoff_seconds = float(
            retry_backoff_seconds if retry_backoff_seconds is not None else os.getenv("LLM_RETRY_BACKOFF_SECONDS", "0.5")
        )
        self.mistral_base_url = "https://api.mistral.ai/v1/chat/completions"

    def _build_prompt(self, question: str, context: str | None = None) -> str:
        if context:
            return (
                "Tu es un assistant Job Hunter AI. Réponds en français, basé uniquement sur le contexte utilisateur fourni.\n\n"
                f"Contexte:\n{context}\n\nQuestion:\n{question}"
            )
        return f"Tu es un assistant Job Hunter AI. Réponds en français.\n\nQuestion:\n{question}"

    def _call_ollama(self, prompt: str) -> str:
        response = httpx.post(
            f"{self.ollama_base_url}/api/generate",
            json={"model": self.ollama_model, "prompt": prompt, "stream": False},
            timeout=30,
            headers={"Content-Type": "application/json"},
        )
        response.raise_for_status()
        payload = response.json()
        return str(payload.get("response") or "")

    def _call_mistral(self, prompt: str) -> str:
        if not self.mistral_api_key:
            raise RuntimeError("Mistral API key not configured")

        response = httpx.post(
            self.mistral_base_url,
            json={
                "model": self.mistral_model,
                "messages": [{"role": "user", "content": prompt}],
            },
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.mistral_api_key}",
            },
            timeout=30,
        )
        response.raise_for_status()
        payload = response.json()
        choices = payload.get("choices") or []
        if not choices:
            raise RuntimeError("Mistral response contained no choices")
        message = choices[0].get("message", {})
        return str(message.get("content") or "")

    def _call_with_retries(self, provider_name: str, caller, prompt: str, user_id: str | None = None) -> str:
        last_error: Exception | None = None
        for attempt in range(self.max_retries + 1):
            try:
                started_at = time.monotonic()
                answer = caller(prompt)
                duration_ms = round((time.monotonic() - started_at) * 1000, 2)
                logger.info(
                    "llm.provider.response",
                    extra={
                        "provider": provider_name,
                        "user_id": user_id,
                        "attempt": attempt + 1,
                        "duration_ms": duration_ms,
                    },
                )
                return answer
            except Exception as exc:  # pragma: no cover - network/fallback behavior
                last_error = exc
                logger.warning(
                    "llm.provider.failed",
                    extra={
                        "provider": provider_name,
                        "user_id": user_id,
                        "attempt": attempt + 1,
                        "error": str(exc),
                    },
                )
                if attempt < self.max_retries:
                    time.sleep(self.retry_backoff_seconds * (attempt + 1))
        raise RuntimeError(str(last_error) if last_error else f"Provider {provider_name} failed")

    def generate(self, question: str, context: str | None = None, user_id: str | None = None) -> dict[str, Any]:
        prompt = self._build_prompt(question, context)
        attempts = [
            ("ollama", self._call_ollama),
            ("mistral", self._call_mistral),
        ]

        last_error: Exception | None = None
        for provider_name, caller in attempts:
            try:
                started_at = time.monotonic()
                answer = self._call_with_retries(provider_name, caller, prompt, user_id=user_id)
                duration_ms = round((time.monotonic() - started_at) * 1000, 2)
                logger.info(
                    "llm.provider.finalized",
                    extra={
                        "provider": provider_name,
                        "user_id": user_id,
                        "question_length": len(question),
                        "duration_ms": duration_ms,
                    },
                )
                return {
                    "provider": provider_name,
                    "answer": answer,
                    "user_id": user_id,
                    "context_used": bool(context),
                    "error": None,
                    "response_time_ms": duration_ms,
                }
            except Exception as exc:  # pragma: no cover - network/fallback behavior
                last_error = exc
                logger.warning(
                    "llm.provider.failed_provider",
                    extra={
                        "provider": provider_name,
                        "user_id": user_id,
                        "error": str(exc),
                    },
                )
                continue

        logger.error(
            "llm.provider.all_failed",
            extra={"user_id": user_id, "error": str(last_error) if last_error else "unknown"},
        )
        return {
            "provider": "error",
            "answer": "Je n’ai pas pu générer de réponse avec les providers configurés.",
            "user_id": user_id,
            "context_used": bool(context),
            "error": str(last_error) if last_error else "unknown",
            "response_time_ms": 0,
        }

    def generate_response(self, question: str, context: str | None = None, user_id: str | None = None) -> dict[str, Any]:
        return self.generate(question=question, context=context, user_id=user_id)


llm_provider = LLMProvider()
