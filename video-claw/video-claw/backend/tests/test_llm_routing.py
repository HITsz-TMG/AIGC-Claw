"""Routing tests for the LLM dispatcher in llm_client.py."""

import os
import sys

BACKEND_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)


class _StubClient:
    def __init__(self):
        self.calls = []

    def query(self, prompt, image_urls=None, model="", web_search=False):
        self.calls.append(model)
        return f"stub-response from {model}"


def _make_llm_with_stubs():
    from models.llm_client import LLM

    llm = LLM()
    minimax_stub = _StubClient()
    deepseek_stub = _StubClient()
    # Inject stubs so we exercise routing without hitting any network/API.
    llm._minimax_client = minimax_stub
    llm._deepseek_client = deepseek_stub
    return llm, minimax_stub, deepseek_stub


def test_minimax_model_routes_to_minimax_client():
    llm, minimax_stub, deepseek_stub = _make_llm_with_stubs()
    result = llm.query("hello", model="MiniMax-M3", safe_content=False)
    assert minimax_stub.calls == ["MiniMax-M3"]
    assert deepseek_stub.calls == []
    assert "stub-response" in result


def test_minimax_m27_routes_to_minimax_client():
    llm, minimax_stub, _ = _make_llm_with_stubs()
    llm.query("hi", model="MiniMax-M2.7", safe_content=False)
    assert minimax_stub.calls == ["MiniMax-M2.7"]


def test_deepseek_model_does_not_route_to_minimax():
    llm, minimax_stub, deepseek_stub = _make_llm_with_stubs()
    llm.query("hi", model="deepseek-chat", safe_content=False)
    assert minimax_stub.calls == []
    assert deepseek_stub.calls == ["deepseek-chat"]
