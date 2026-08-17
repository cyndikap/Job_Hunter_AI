from __future__ import annotations


def build_system_prompt(question: str, context: str | None = None) -> str:
    base_prompt = (
        "Tu es Job Hunter AI, assistant personnel orienté carrière et recherche d'emploi. "
        "Réponds en français, de manière claire, concise et utile. "
        "Base-toi uniquement sur le contexte utilisateur fourni et n'invente jamais d'informations. "
        "Si le contexte est insuffisant, précise ce qui manque et propose une action concrète."
    )
    if not context:
        return f"{base_prompt}\n\nQuestion:\n{question}"
    return (
        f"{base_prompt}\n\nContexte utilisateur (RAG) :\n{context}\n\nQuestion:\n{question}"
    )
