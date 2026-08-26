import os
import sys

models_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.dirname(models_dir)
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

import logging

try:
    from models.config_model import get_model_config
    from models.llm_gpt import GPT
    from models.llm_gemini import Gemini
    from models.llm_deepseek import DeepSeek
    from models.llm_dashscope import QwenLLM
    from models.vlm_dashscope import QwenVLClient
except ImportError:
    from config_model import get_model_config
    from llm_gpt import GPT
    from llm_gemini import Gemini
    from llm_deepseek import DeepSeek
    from llm_dashscope import QwenLLM
    from vlm_dashscope import QwenVLClient

from config import Config

logger = logging.getLogger(__name__)

class LLM:
    def __init__(self, gemini_base_url="", gemini_api_key="", gpt_base_url="", gpt_api_key="", deepseek_base_url="", deepseek_api_key="", dashscope_api_key="", atlascloud_base_url="", atlascloud_api_key=""):
        self._gemini_base_url = gemini_base_url or Config.GOOGLE_GEMINI_BASE_URL
        self._gemini_api_key = gemini_api_key or Config.GEMINI_API_KEY
        self._gpt_base_url = gpt_base_url or Config.OPENAI_BASE_URL
        self._gpt_api_key = gpt_api_key or Config.OPENAI_API_KEY
        self._deepseek_base_url = deepseek_base_url or Config.DEEPSEEK_BASE_URL
        self._deepseek_api_key = deepseek_api_key or Config.DEEPSEEK_API_KEY
        self._dashscope_api_key = dashscope_api_key or Config.DASHSCOPE_API_KEY
        self._atlascloud_base_url = atlascloud_base_url or Config.ATLASCLOUD_BASE_URL
        self._atlascloud_api_key = atlascloud_api_key or Config.ATLASCLOUD_API_KEY

        self._gemini_client = None
        self._gpt_client = None
        self._deepseek_client = None
        self._dashscope_client = None
        self._dashscope_vl_client = None
        self._atlascloud_client = None

    @property
    def gemini_client(self):
        if self._gemini_client is None:
            self._gemini_client = Gemini(
                base_url=self._gemini_base_url,
                api_key=self._gemini_api_key,
            )
        return self._gemini_client

    @property
    def gpt_client(self):
        if self._gpt_client is None:
            self._gpt_client = GPT(
                base_url=self._gpt_base_url,
                api_key=self._gpt_api_key,
                proxy=Config.provider_proxy("openai"),
            )
        return self._gpt_client

    @property
    def deepseek_client(self):
        if self._deepseek_client is None:
            self._deepseek_client = DeepSeek(
                base_url=self._deepseek_base_url,
                api_key=self._deepseek_api_key,
            )
        return self._deepseek_client

    @property
    def dashscope_client(self):
        if self._dashscope_client is None:
            self._dashscope_client = QwenLLM(api_key=self._dashscope_api_key)
        return self._dashscope_client

    @property
    def dashscope_vl_client(self):
        if self._dashscope_vl_client is None:
            self._dashscope_vl_client = QwenVLClient(api_key=self._dashscope_api_key)
        return self._dashscope_vl_client

    @property
    def atlascloud_client(self):
        if self._atlascloud_client is None:
            self._atlascloud_client = GPT(
                base_url=self._atlascloud_base_url,
                api_key=self._atlascloud_api_key,
                proxy=Config.provider_proxy("atlascloud"),
            )
        return self._atlascloud_client

    def full_to_half(self, text):
        if not isinstance(text, str):
            return text
        
        translation_table = {0x3000: 0x0020}
        for i in range(65281, 65375):
            translation_table[i] = i - 65248
            
        return text.translate(translation_table)

    def query(self, prompt, image_urls=[], model="qwen3.6-max-preview", safe_content=True, task_id=None, web_search=False):
        """
        Query the LLM with a prompt and optional image URLs.
        Selects the backend (GPT or Gemini) based on the model name.

        :param web_search: Enable web search for supported providers
        """
        if safe_content:
            prompt = self.full_to_half(prompt)

        if not model:
            model = "qwen3.6-max-preview"
            
        if Config.PRINT_MODEL_INPUT:
            lines = [
                "---- LLM QUERY REQUEST ----",
                f"Model: {model}",
            ]
            if task_id:
                lines.append(f"Task ID: {task_id}")
            if image_urls:
                lines.append(f"Images: {len(image_urls)}")
                lines.extend(f"  - {u}" for u in image_urls)
            lines.extend([
                f"Web Search: {web_search}",
                f"Prompt: {prompt[:200]}{'...' if len(prompt) > 200 else ''}",
                "-" * 30,
            ])
            logger.info("\n%s", "\n".join(lines))
            
        result = ""
        model_lower = model.lower()
        provider = get_model_config(model).get("provider")
        if provider == "atlascloud":
            result = self.atlascloud_client.query(prompt, image_urls=image_urls, model=model, web_search=False)
        elif model_lower.startswith("gemini"):
            result = self.gemini_client.query(prompt, image_urls=image_urls, model=model)
        elif "gpt" in model_lower:
            # OpenAI series models
            result = self.gpt_client.query(prompt, image_urls=image_urls, model=model, web_search=web_search)
        elif "kimi" in model_lower or "qwen3.6-plus" in model_lower or "qwen3.6-flash" in model_lower or "vl" in model_lower:
            # DashScope VLM models (using MultiModalConversation API)
            result = self.dashscope_vl_client.chat(text=prompt, images=image_urls, model=model, stream=False)
        elif "deepseek-v3.2" in model_lower:
            # DeepSeek v3.2 (通过 DashScope Generation API)
            result = self.dashscope_client.query(prompt, image_urls=image_urls, model=model, web_search=web_search)
        elif model_lower.startswith("deepseek") and "v3.2" not in model_lower:
            # Original DeepSeek provider
            result = self.deepseek_client.query(prompt, image_urls=image_urls, model=model, web_search=web_search)
        else:
            # Default to Qwen models / deepseek-v3.2 via DashScope Generation API
            result = self.dashscope_client.query(prompt, image_urls=image_urls, model=model, web_search=web_search)

        if safe_content:
            result = self.full_to_half(result)
        
        # Remove empty lines
        return '\n'.join([line for line in result.split('\n') if line.strip() != ''])
