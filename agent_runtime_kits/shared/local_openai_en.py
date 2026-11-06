"""OpenAI-compatible client helper for local llama-server or a cloud API.

This module does not load model weights. It only constructs a client from
environment variables. Tool-calling quality depends on the actual model and
is NOT implied by a successful HTTP handshake.
"""
from __future__ import annotations

import os
from typing import Any


def client_kwargs() -> dict[str, Any]:
    base = os.environ.get("AGENT_LLM_BASE_URL", "").strip()
    key = os.environ.get("AGENT_LLM_API_KEY", "").strip()
    mode = os.environ.get("AGENT_LLM_MODE", "local").strip().lower()
    if mode == "mock":
        return {"mode": "mock"}
    if mode == "cloud":
        if not key:
            raise RuntimeError("云 API 模式需要 AGENT_LLM_API_KEY")
        kwargs: dict[str, Any] = {"api_key": key}
        if base:
            kwargs["base_url"] = base
        return {"mode": "cloud", "openai_kwargs": kwargs}
    # local llama-server / vLLM / Ollama openai compat
    if not base:
        base = "http://127.0.0.1:8080/v1"
    return {
        "mode": "local",
        "openai_kwargs": {
            "api_key": key or "local-not-a-secret",
            "base_url": base,
        },
    }


def model_name() -> str:
    return os.environ.get("AGENT_LLM_MODEL", "qwen2.5-1.5b-instruct")


def describe() -> str:
    kw = client_kwargs()
    return f"mode={kw['mode']} model={model_name()} base={kw.get('openai_kwargs', {}).get('base_url', '')}"
