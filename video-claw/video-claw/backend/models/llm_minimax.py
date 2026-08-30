import os
import sys

models_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.dirname(models_dir)
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

import time
import logging
from openai import OpenAI
from config import Config

logger = logging.getLogger(__name__)

DEFAULT_MINIMAX_BASE_URL = "https://api.minimax.io/v1"
DEFAULT_MINIMAX_TIMEOUT = 300
DEFAULT_MINIMAX_MAX_ATTEMPTS = 5
DEFAULT_MINIMAX_MAX_TOKENS = 8000


class MiniMax:
    """
    MiniMax LLM 客户端（OpenAI 兼容接口）

    MiniMax-M3: 最新旗舰模型，1M 上下文，最大输出 128K，支持图片输入
    MiniMax-M2.7: 上一代模型，作为兼容选项保留

    注意：
    - Base URL 使用海外版 https://api.minimax.io/v1
    - temperature 取值范围为 (0.0, 1.0]，默认 1.0，不能传 0
    """
    def __init__(self, base_url="", api_key="", timeout=None, max_attempts=None):
        import httpx
        self.base_url = base_url or Config.MINIMAX_BASE_URL or DEFAULT_MINIMAX_BASE_URL
        self.api_key = api_key or Config.MINIMAX_API_KEY
        self.timeout = self._as_int(timeout, DEFAULT_MINIMAX_TIMEOUT)
        self.max_attempts = self._as_int(max_attempts, DEFAULT_MINIMAX_MAX_ATTEMPTS)

        if not self.api_key:
            logger.warning("MINIMAX_API_KEY is not set")

        kwargs = {"api_key": self.api_key, "base_url": self.base_url, "timeout": self.timeout}
        proxy = Config.provider_proxy("minimax")
        if proxy:
            kwargs["http_client"] = httpx.Client(proxy=proxy, timeout=self.timeout)
        self.client = OpenAI(**kwargs)
        self.max_tokens = DEFAULT_MINIMAX_MAX_TOKENS

    @staticmethod
    def _as_int(value, default: int) -> int:
        try:
            return int(value)
        except (TypeError, ValueError):
            return default

    def query(self, prompt, image_urls=[], model="MiniMax-M3", web_search=False):
        """
        Query MiniMax model via the OpenAI-compatible Chat Completions API.

        :param prompt: Text prompt
        :param image_urls: Optional image URLs for multimodal input
        :param model: Model name (e.g., MiniMax-M3, MiniMax-M2.7)
        :param web_search: Unused for MiniMax, kept for interface consistency
        """
        if not model:
            model = "MiniMax-M3"

        messages = [{"role": "system", "content": "You are a helpful assistant."}]
        content = [{"type": "text", "text": prompt}]
        if image_urls:
            content.extend([{"type": "image_url", "image_url": {"url": url}} for url in image_urls])
        messages.append({"role": "user", "content": content})

        attempts = 0
        while attempts < self.max_attempts:
            try:
                response = self.client.chat.completions.create(
                    model=model,
                    messages=messages,
                    max_tokens=self.max_tokens,
                    temperature=1.0,  # MiniMax requires temperature in (0.0, 1.0]
                )

                if response.choices and response.choices[0].message.content:
                    return response.choices[0].message.content
                logger.warning("MiniMax returned an empty response; retrying")
                time.sleep(2)
            except Exception as e:
                logger.warning(
                    "MiniMax request failed; retrying. model=%s attempt=%s/%s timeout=%ss error=%s",
                    model,
                    attempts + 1,
                    self.max_attempts,
                    self.timeout,
                    e,
                )
                time.sleep(5)
            attempts += 1

        raise Exception("Max attempts reached, failed to get a response from MiniMax.")


if __name__ == "__main__":
    import sys
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from config import Config

    # 支持的模型列表
    MODELS = ["MiniMax-M3", "MiniMax-M2.7"]

    print("=== MiniMax 文本生成可用性测试 ===")
    api_key = Config.MINIMAX_API_KEY
    base_url = Config.MINIMAX_BASE_URL
    if not api_key:
        print("✗ MINIMAX_API_KEY 未设置，跳过")
        sys.exit(1)
    print(f"  API Key: {api_key[:6]}***{api_key[-4:]}")
    if base_url:
        print(f"  Base URL: {base_url}")

    client = MiniMax(api_key=api_key, base_url=base_url)
    prompt = "用一句话介绍你自己。"
    print(f"  Prompt: {prompt}")

    for model in MODELS:
        print(f"\n--- 测试模型: {model} ---")
        t0 = time.time()
        try:
            resp = client.query(prompt, model=model)
            elapsed = time.time() - t0
            print(f"✓ 响应 ({elapsed:.1f}s): {resp.strip()[:200]}")
        except Exception as e:
            print(f"✗ 失败: {e}")
