"""Unit tests for the MiniMax LLM provider integration."""

import os
import sys

BACKEND_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)


def test_minimax_provider_in_config_defaults():
    """MiniMax should be registered as an api_provider with the overseas base URL."""
    from config import Config

    config = Config.as_dict()
    providers = config["api_providers"]
    assert "minimax" in providers
    assert providers["minimax"]["base_url"] == "https://api.minimax.io/v1"
    assert "api_key" in providers["minimax"]
    assert providers["minimax"]["enable_proxy"] is False


def test_minimax_models_registered():
    """MiniMax-M3 (new default) and MiniMax-M2.7 (compat) should be llm models."""
    from models.config_model import get_model_config, get_models_by_type

    llm_ids = {model["id"] for model in get_models_by_type("llm")}
    assert "MiniMax-M3" in llm_ids
    assert "MiniMax-M2.7" in llm_ids

    m3 = get_model_config("MiniMax-M3")
    assert m3["provider"] == "minimax"
    assert "llm" in m3["type"]


def test_minimax_client_default_base_url():
    """Client should fall back to the overseas base URL and default model M3."""
    from models.llm_minimax import DEFAULT_MINIMAX_BASE_URL, MiniMax

    client = MiniMax(api_key="test-key", base_url="")
    assert client.base_url == DEFAULT_MINIMAX_BASE_URL
    assert client.base_url.endswith("/v1")


def test_minimax_client_custom_base_url():
    from models.llm_minimax import MiniMax

    client = MiniMax(api_key="test-key", base_url="https://example.com/v1")
    assert client.base_url == "https://example.com/v1"


def test_minimax_client_uses_openai_sdk():
    """The provider should be implemented on top of the OpenAI-compatible SDK."""
    from models.llm_minimax import MiniMax

    client = MiniMax(api_key="test-key")
    # OpenAI client exposes chat.completions.create
    assert hasattr(client.client, "chat")
    assert hasattr(client.client.chat, "completions")
