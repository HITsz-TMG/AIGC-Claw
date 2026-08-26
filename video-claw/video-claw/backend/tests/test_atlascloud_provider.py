import importlib
import sys
import types
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parents[1]
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))


def test_atlascloud_models_are_registered_as_llm():
    from models.config_model import get_model_config, get_models_by_type, model_type_capabilities

    llm_ids = {model["id"] for model in get_models_by_type("llm")}
    assert "qwen/qwen3.5-flash" in llm_ids
    assert "deepseek-ai/deepseek-v4-pro" in llm_ids

    qwen = get_model_config("qwen/qwen3.5-flash")
    assert qwen["provider"] == "atlascloud"
    assert qwen["family"] == "qwen"
    assert model_type_capabilities("llm", qwen)["api_contract_verified"] is True


def test_atlascloud_config_defaults_and_environment_fallback(monkeypatch):
    monkeypatch.setenv("ATLASCLOUD_API_KEY", "atlas-test-key")

    import config as config_module

    config_module = importlib.reload(config_module)
    Config = config_module.Config

    assert Config.ATLASCLOUD_API_KEY == "atlas-test-key"
    assert Config.ATLASCLOUD_BASE_URL == "https://api.atlascloud.ai/v1"
    assert Config.provider_proxy("atlascloud") == ""


def test_llm_routes_registered_atlascloud_model(monkeypatch):
    fake_openai = types.ModuleType("openai")
    fake_openai.OpenAI = object
    monkeypatch.setitem(sys.modules, "openai", fake_openai)

    fake_dashscope = types.ModuleType("dashscope")
    fake_dashscope.Generation = object
    fake_dashscope.MultiModalConversation = object
    monkeypatch.setitem(sys.modules, "dashscope", fake_dashscope)

    from models.llm_client import LLM

    class FakeAtlasCloud:
        def query(self, prompt, image_urls=None, model="", web_search=False):
            return f"{model}:{prompt}:{bool(image_urls)}:{web_search}"

    client = LLM(atlascloud_api_key="atlas-test-key")
    monkeypatch.setattr(client, "_atlascloud_client", FakeAtlasCloud())

    assert client.query("hello", model="qwen/qwen3.5-flash") == (
        "qwen/qwen3.5-flash:hello:False:False"
    )
