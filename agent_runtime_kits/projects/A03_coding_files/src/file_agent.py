#!/usr/bin/env python3
"""Sandboxed file tools + optional coding-agent notes for aider.

All file operations stay inside fixtures/workspace. No shell, no git, no
network. aider-chat is provided as a separate pinned environment; this script
does not invoke aider.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "shared"))
from local_openai_en import client_kwargs, model_name  # noqa: E402

WORKSPACE = Path(__file__).resolve().parents[1] / "fixtures" / "workspace"


def resolve(rel: str) -> Path:
    p = (WORKSPACE / rel).resolve()
    if WORKSPACE.resolve() not in p.parents and p != WORKSPACE.resolve():
        raise ValueError(f"path escapes sandbox: {rel}")
    return p


def tool_list(prefix: str = ".") -> dict:
    base = resolve(prefix)
    items = []
    for p in sorted(base.rglob("*")):
        if p.is_file():
            items.append(str(p.relative_to(WORKSPACE)))
    return {"files": items}


def tool_read(path: str) -> dict:
    p = resolve(path)
    text = p.read_text(encoding="utf-8")
    return {"path": path, "text": text, "nchars": len(text)}


def tool_write(path: str, text: str) -> dict:
    p = resolve(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")
    return {"path": path, "nchars": len(text), "written": True}


def tool_search(pattern: str) -> dict:
    rx = re.compile(pattern)
    hits = []
    for p in WORKSPACE.rglob("*"):
        if not p.is_file():
            continue
        try:
            lines = p.read_text(encoding="utf-8").splitlines()
        except UnicodeDecodeError:
            continue
        for i, line in enumerate(lines, 1):
            if rx.search(line):
                hits.append({"path": str(p.relative_to(WORKSPACE)), "line": i, "text": line[:200]})
    return {"hits": hits[:50]}


TOOLS = {
    "list_files": lambda **kw: tool_list(kw.get("prefix", ".")),
    "read_file": lambda **kw: tool_read(kw["path"]),
    "write_file": lambda **kw: tool_write(kw["path"], kw.get("text", "")),
    "search": lambda **kw: tool_search(kw["pattern"]),
}


def mock_run(task: str) -> dict:
    steps = []
    steps.append({"action": "list_files", "obs": tool_list(".")})
    if "add" in task.lower() or "add(" in task or "两数相加" in task:
        src = tool_read("calc.py")
        steps.append({"action": "read_file", "obs": {"nchars": src["nchars"]}})
        new = src["text"].replace(
            "def add(a, b):\n    return None",
            "def add(a, b):\n    return a + b",
        )
        steps.append({"action": "write_file", "obs": tool_write("calc.py", new)})
        return {"ok": True, "backend": "mock", "answer": "已在沙箱内把 add 改为返回 a+b", "steps": steps}
    return {"ok": True, "backend": "mock", "answer": "已列出沙箱文件", "steps": steps}


def openai_run(task: str) -> dict:
    from openai import OpenAI

    info = client_kwargs()
    client = OpenAI(**info["openai_kwargs"])
    messages = [
        {
            "role": "system",
            "content": (
                "你只能在沙箱内用 JSON 调用 list_files/read_file/write_file/search 或 finish。"
                "禁止提出 shell 或访问沙箱外路径。"
            ),
        },
        {"role": "user", "content": task},
    ]
    steps = []
    for _ in range(8):
        resp = client.chat.completions.create(
            model=model_name(),
            messages=messages,
            temperature=0,
            response_format={"type": "json_object"},
        )
        raw = resp.choices[0].message.content or "{}"
        decision = json.loads(raw)
        act = decision.get("action")
        if act == "finish":
            return {"ok": True, "backend": info["mode"], "answer": decision.get("answer", ""), "steps": steps, "verified": False}
        if act not in TOOLS:
            obs = {"error": "unknown_action"}
        else:
            try:
                obs = TOOLS[act](**(decision.get("args") or {}))
            except Exception as e:
                obs = {"error": str(e)}
        steps.append({"decision": decision, "observation": obs})
        messages.append({"role": "assistant", "content": raw})
        messages.append({"role": "user", "content": json.dumps(obs, ensure_ascii=False)})
    return {"ok": False, "error": "max_steps", "steps": steps, "verified": False}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--task-file", default=str(Path(__file__).resolve().parents[1] / "examples" / "task_fix_add.json"))
    parser.add_argument("--mode", default=os.environ.get("AGENT_LLM_MODE", "mock"))
    args = parser.parse_args()
    os.environ["AGENT_LLM_MODE"] = args.mode
    WORKSPACE.mkdir(parents=True, exist_ok=True)
    task = json.loads(Path(args.task_file).read_text(encoding="utf-8"))["task"]
    out = mock_run(task) if args.mode == "mock" else openai_run(task)
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
