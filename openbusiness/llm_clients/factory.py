"""LLM client factory — reads provider/model from config module."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable

from openbusiness.llm_clients import config


MODEL_TIERS = ("quick", "deep")


@dataclass(frozen=True)
class ProviderAdapter:
    """Concrete model client adapter at the provider seam."""

    name: str
    build: Callable[[str], Any]


def normalize_tier(tier: str) -> str:
    """Normalize and validate a model tier."""
    normalized = tier.strip().lower()
    if normalized not in MODEL_TIERS:
        raise ValueError(f"Unsupported LLM tier: {tier!r}. Use one of: {', '.join(MODEL_TIERS)}.")
    return normalized


def _provider_model(provider: str, tier: str, quick_default: str, deep_default: str) -> str:
    default = quick_default if tier == "quick" else deep_default
    return config.get(f"{provider}_{tier}_model", default)


def _build_openai(tier: str) -> Any:
    from langchain_openai import ChatOpenAI

    model = _provider_model("openai", tier, "gpt-4o-mini", "gpt-4o")
    return ChatOpenAI(model=model, temperature=0)


def _build_anthropic(tier: str) -> Any:
    from langchain_anthropic import ChatAnthropic

    model = _provider_model(
        "anthropic",
        tier,
        "claude-haiku-4-5-20251001",
        "claude-sonnet-4-5-20250929",
    )
    return ChatAnthropic(model=model, temperature=0)


def _build_deepseek(tier: str) -> Any:
    from langchain_openai import ChatOpenAI

    model = _provider_model("deepseek", tier, "deepseek-chat", "deepseek-chat")
    return ChatOpenAI(
        model=model,
        api_key=config.get("deepseek_api_key"),
        base_url=config.get("deepseek_base_url", "https://api.deepseek.com"),
        temperature=0,
        timeout=float(config.get("deepseek_timeout", "60")),
        max_retries=int(config.get("deepseek_max_retries", "1")),
        max_tokens=int(config.get("deepseek_max_tokens", "2048")),
    )


PROVIDER_ADAPTERS = {
    "openai": ProviderAdapter("openai", _build_openai),
    "anthropic": ProviderAdapter("anthropic", _build_anthropic),
    "deepseek": ProviderAdapter("deepseek", _build_deepseek),
}


def get_provider_adapter(provider: str | None = None) -> ProviderAdapter:
    """Return the provider adapter selected by config or explicit name."""
    raw_provider = provider or config.get("provider", "openai") or "openai"
    normalized = raw_provider.strip().lower()
    try:
        return PROVIDER_ADAPTERS[normalized]
    except KeyError as exc:
        available = ", ".join(sorted(PROVIDER_ADAPTERS))
        raise ValueError(f"Unknown LLM provider: {raw_provider!r}. Available providers: {available}.") from exc


def get_llm(tier: str = "quick") -> Any:
    """Return a chat model. tier='quick' for analysts, 'deep' for synthesis."""
    config.export_to_env()
    return get_provider_adapter().build(normalize_tier(tier))
