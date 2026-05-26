"""LLM client factory — supports OpenAI & Anthropic with two thinking tiers."""

from __future__ import annotations

import os

from dotenv import load_dotenv

load_dotenv()

_PROVIDER = os.getenv("LLM_PROVIDER", "openai")


def get_llm(tier: str = "quick"):
    """Return a chat model instance.

    Args:
        tier: 'quick' for analysts (fast, cheap) or 'deep' for managers (strong reasoning).
    """
    if _PROVIDER == "anthropic":
        from langchain_anthropic import ChatAnthropic

        model = "claude-sonnet-4-20250514" if tier == "quick" else "claude-opus-4-20250514"
        return ChatAnthropic(model=model, temperature=0)

    from langchain_openai import ChatOpenAI

    model = "gpt-4o-mini" if tier == "quick" else "gpt-4o"
    return ChatOpenAI(model=model, temperature=0)
