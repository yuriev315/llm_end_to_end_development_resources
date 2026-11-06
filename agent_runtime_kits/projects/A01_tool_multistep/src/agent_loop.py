#!/usr/bin/env python3
"""Minimal tool-calling loop: mock, local OpenAI-compatible server, or cloud API.

Not executed in this collection round. A successful client constructor does not
mean the model can call tools or emit valid JSON.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
import traceback
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "shared"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from local_openai_en import client_kwargs, describe, model_name  # noqa: E402
from tools import Scratchpad, TOOLS  # noqa: E402


SCHEMA = {
    "type": "object",
    "properties": {
        "thought": {"type": "string"},
        "action": {"type": "string", "enum": list(TOOLS) + ["finish"]},
        "args": {"type": "object"},
        "answer": {"type": "string"},
    },
    "required": ["action"],
}


def mock_policy(task: str, history: list[dict]) -> dict:
    """Scripted policy for the bundled example. Not an LLM."""
    n = len(history)
    if "37*19" in task.replace(" ", "") or "37 × 19" in task or "37*19" in task:
        if n == 0:
            return {"thought": "先算 37*19", "action": "calculator", "args": {"expr": "37*19"}}
        if n == 1:
            val = history[-1]["observation"].get("value")
            return {"thought": "记下中间结果", "action": "note_add", "args": {"text": f"37*19={val}"}}
        if n == 2:
            return {"thought": "取当前时间", "action": "now_iso", "args": {}}
        return {
            "thought": "汇总",
            "action": "finish",
            "answer": f"37*19={history[0]['observation']['value']}; time={history[2]['observation']['utc']}",
        }
    return {"thought": "示例策略不覆盖该任务", "action": "finish", "answer": "mock_unhandled"}


def dispatch(pad: Scratchpad, action: str, args: dict) -> dict:
    spec = TOOLS[action]
    fn = spec["fn"]
    if action in ("calculator",):
        return fn(pad, args.get("expr", ""))
    if action in ("note_add",):
        return fn(pad, args.get("text", ""))
    return fn(pad)


def run_mock(task: str, max_steps: int = 6) -> dict:
    pad = Scratchpad()
    history: list[dict] = []
    t0 = time.time()
    for step in range(max_steps):
        decision = mock_policy(task, history)
        if decision.get("action") == "finish":
            return {
                "ok": True,
                "backend": "mock",
                "answer": decision.get("answer", ""),
                "steps": history,
                "latency_s": round(time.time() - t0, 3),
                "tool_calls_ok": all("error" not in h["observation"] for h in history),
            }
        try:
            obs = dispatch(pad, decision["action"], decision.get("args") or {})
        except Exception as e:
            obs = {"error": str(e)}
        history.append({"decision": decision, "observation": obs})
    return {"ok": False, "backend": "mock", "error": "max_steps", "steps": history}


def run_openai(task: str, max_steps: int = 8, timeout_s: float = 60.0) -> dict:
    from openai import OpenAI

    info = client_kwargs()
    client = OpenAI(**info["openai_kwargs"], timeout=timeout_s)
    pad = Scratchpad()
    messages = [
        {
            "role": "system",
            "content": (
                "你是工具调用代理。每次只输出 JSON，字段 thought, action, args, answer。"
                f"action 只能是 {list(TOOLS)+['finish']}。不要编造工具结果。"
            ),
        },
        {"role": "user", "content": task},
    ]
    history: list[dict] = []
    t0 = time.time()
    for _ in range(max_steps):
        try:
            resp = client.chat.completions.create(
                model=model_name(),
                messages=messages,
                temperature=0,
                response_format={"type": "json_object"},
            )
            raw = resp.choices[0].message.content or "{}"
            decision = json.loads(raw)
        except Exception as e:
            return {
                "ok": False,
                "backend": info["mode"],
                "error": f"model_or_json: {e}",
                "trace": traceback.format_exc()[-1500:],
                "steps": history,
                "note": "接口通了也不等于工具调用能力已验证",
            }
        action = decision.get("action")
        if action == "finish":
            return {
                "ok": True,
                "backend": info["mode"],
                "answer": decision.get("answer", ""),
                "steps": history,
                "latency_s": round(time.time() - t0, 3),
                "verified": False,
            }
        if action not in TOOLS:
            history.append({"decision": decision, "observation": {"error": "unknown_action"}})
            messages.append({"role": "assistant", "content": raw})
            messages.append({"role": "user", "content": json.dumps({"error": "unknown_action"}, ensure_ascii=False)})
            continue
        try:
            obs = dispatch(pad, action, decision.get("args") or {})
        except Exception as e:
            obs = {"error": str(e)}
        history.append({"decision": decision, "observation": obs})
        messages.append({"role": "assistant", "content": raw})
        messages.append({"role": "user", "content": json.dumps(obs, ensure_ascii=False)})
    return {"ok": False, "backend": info["mode"], "error": "max_steps", "steps": history, "verified": False}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--task-file", default=str(Path(__file__).resolve().parents[1] / "examples" / "task_multistep.json"))
    parser.add_argument("--mode", default=os.environ.get("AGENT_LLM_MODE", "mock"))
    args = parser.parse_args()
    os.environ["AGENT_LLM_MODE"] = args.mode
    task = json.loads(Path(args.task_file).read_text(encoding="utf-8"))["task"]
    print(describe())
    if args.mode == "mock":
        out = run_mock(task)
    else:
        out = run_openai(task)
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
