from __future__ import annotations

from langchain_ollama import ChatOllama


def build_llm(*, model: str, temperature: float = 0.0) -> ChatOllama:
    return ChatOllama(model=model, temperature=temperature)

