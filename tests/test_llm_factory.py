import pytest

from openbusiness.llm_clients.factory import get_provider_adapter, normalize_tier


def test_normalize_tier() -> None:
    assert normalize_tier(" Quick ") == "quick"

    with pytest.raises(ValueError, match="Unsupported LLM tier"):
        normalize_tier("slow")


def test_get_provider_adapter_validates_provider_without_building_client() -> None:
    assert get_provider_adapter("deepseek").name == "deepseek"

    with pytest.raises(ValueError, match="Unknown LLM provider"):
        get_provider_adapter("unknown")
