from app.services.llm_provider import LLMProvider


def test_ollama_primary_provider_returns_text(monkeypatch):
    class FakeResponse:
        def __init__(self, payload):
            self.payload = payload

        def raise_for_status(self):
            return None

        def json(self):
            return self.payload

    def fake_post(url, json=None, timeout=None, headers=None):
        assert "11434" in url
        return FakeResponse({"response": "Réponse Ollama locale"})

    monkeypatch.setenv("OLLAMA_BASE_URL", "http://localhost:11434")
    monkeypatch.setenv("OLLAMA_MODEL", "llama3.2")
    monkeypatch.setattr("app.services.llm_provider.httpx.post", fake_post)

    provider = LLMProvider()
    result = provider.generate("Que faire ?", context="Contexte de test", user_id="user-1")

    assert result["provider"] == "ollama"
    assert "Réponse Ollama locale" in result["answer"]


def test_mistral_fallback_is_used_when_ollama_fails(monkeypatch):
    class FakeResponse:
        def __init__(self, payload):
            self.payload = payload

        def raise_for_status(self):
            return None

        def json(self):
            return self.payload

    def fake_post(url, json=None, timeout=None, headers=None):
        if "11434" in url:
            raise RuntimeError("ollama indisponible")
        return FakeResponse({"choices": [{"message": {"content": "Réponse Mistral fallback"}}]})

    monkeypatch.setenv("OLLAMA_BASE_URL", "http://localhost:11434")
    monkeypatch.setenv("OLLAMA_MODEL", "llama3.2")
    monkeypatch.setenv("MISTRAL_API_KEY", "demo-key")
    monkeypatch.setenv("MISTRAL_MODEL", "mistral-small-latest")
    monkeypatch.setattr("app.services.llm_provider.httpx.post", fake_post)

    provider = LLMProvider()
    result = provider.generate("Que faire ?", context="Contexte de test", user_id="user-2")

    assert result["provider"] == "mistral"
    assert "Réponse Mistral fallback" in result["answer"]


def test_ollama_retries_transient_failure(monkeypatch):
    class FakeResponse:
        def __init__(self, payload):
            self.payload = payload

        def raise_for_status(self):
            return None

        def json(self):
            return self.payload

    calls = {"count": 0}

    def fake_post(url, json=None, timeout=None, headers=None):
        calls["count"] += 1
        if calls["count"] == 1:
            raise RuntimeError("ollama temporairement indisponible")
        return FakeResponse({"response": "Réponse Ollama après retry"})

    monkeypatch.setenv("OLLAMA_BASE_URL", "http://localhost:11434")
    monkeypatch.setenv("OLLAMA_MODEL", "llama3.2")
    monkeypatch.setattr("app.services.llm_provider.httpx.post", fake_post)

    provider = LLMProvider()
    result = provider.generate("Que faire ?", context="Contexte de test", user_id="user-3")

    assert result["provider"] == "ollama"
    assert "Réponse Ollama après retry" in result["answer"]
    assert calls["count"] == 2
