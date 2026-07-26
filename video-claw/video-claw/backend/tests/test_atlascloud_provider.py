import sys
from pathlib import Path
from unittest.mock import Mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from config import DEFAULT_CONFIG
from models.config_model import get_model_config
from models.llm_client import LLM


def test_atlascloud_provider_defaults():
    provider = DEFAULT_CONFIG["api_providers"]["atlascloud"]

    assert provider == {
        "api_key": "",
        "base_url": "https://api.atlascloud.ai/v1",
        "enable_proxy": False,
    }
    assert get_model_config("deepseek-ai/deepseek-v4-pro")["provider"] == "atlascloud"


def test_atlascloud_model_uses_openai_compatible_client():
    llm = LLM(atlascloud_api_key="test-key")
    client = Mock()
    client.query.return_value = "Atlas response"
    llm._atlascloud_client = client

    result = llm.query("Hello", model="deepseek-ai/deepseek-v4-pro", web_search=True)

    assert result == "Atlas response"
    client.query.assert_called_once_with(
        "Hello",
        image_urls=[],
        model="deepseek-ai/deepseek-v4-pro",
        web_search=False,
    )
