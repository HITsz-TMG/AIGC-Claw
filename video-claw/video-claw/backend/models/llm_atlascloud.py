"""Atlas Cloud OpenAI-compatible LLM client."""

import os
import sys

models_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.dirname(models_dir)
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from config import Config  # noqa: E402
from models.llm_gpt import GPT  # noqa: E402


class AtlasCloud(GPT):
    """Atlas Cloud text generation client using the OpenAI-compatible chat API."""

    def __init__(self, base_url: str = "", api_key: str = "", timeout: int = 300):
        super().__init__(
            base_url=base_url or Config.ATLASCLOUD_BASE_URL,
            api_key=api_key or Config.ATLASCLOUD_API_KEY,
            proxy=Config.provider_proxy("atlascloud"),
            timeout=timeout,
        )

    def query(self, prompt, image_urls=None, model="qwen/qwen3.5-flash", web_search=False):
        if image_urls:
            raise ValueError("Atlas Cloud LLM models registered here are text-only.")
        if web_search:
            raise ValueError("Atlas Cloud provider does not support Video-Claw web_search mode.")
        model = model or "qwen/qwen3.5-flash"
        model_lower = model.lower()
        for prefix in ("atlascloud/", "atlas-cloud/", "atlas/"):
            if model_lower.startswith(prefix):
                model = model[len(prefix):]
                break
        return super().query(prompt, image_urls=[], model=model or "qwen/qwen3.5-flash")
