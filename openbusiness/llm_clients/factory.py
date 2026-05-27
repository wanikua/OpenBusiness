"""LLM client factory — reads provider/model from config module."""

from __future__ import annotations

from openbusiness.llm_clients import config


def get_llm(tier: str = "quick"):
    """Return a chat model. tier='quick' for analysts, 'deep' for synthesis."""
    config.export_to_env()
    provider = config.get("provider", "openai")

    if provider == "anthropic":
        from langchain_anthropic import ChatAnthropic

        model = (
            config.get("anthropic_quick_model", "claude-haiku-4-5-20251001")
            if tier == "quick"
            else config.get("anthropic_deep_model", "claude-sonnet-4-5-20250929")
        )
        return ChatAnthropic(model=model, temperature=0)

    from langchain_openai import ChatOpenAI

    if provider == "deepseek":
        model = (
            config.get("deepseek_quick_model", "deepseek-chat")
            if tier == "quick"
            else config.get("deepseek_deep_model", "deepseek-chat")
        )
        return ChatOpenAI(
            model=model,
            api_key=config.get("deepseek_api_key"),
            base_url=config.get("deepseek_base_url", "https://api.deepseek.com"),
            temperature=0,
            timeout=float(config.get("deepseek_timeout", "60")),
            max_retries=int(config.get("deepseek_max_retries", "1")),
            max_tokens=int(config.get("deepseek_max_tokens", "2048")),
        )

    model = (
        config.get("openai_quick_model", "gpt-4o-mini")
        if tier == "quick"
        else config.get("openai_deep_model", "gpt-4o")
    )
    return ChatOpenAI(model=model, temperature=0)
