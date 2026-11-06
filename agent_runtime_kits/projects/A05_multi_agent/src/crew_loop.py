#!/usr/bin/env python3
"""Role-based multi-agent loop with shared state, cost accounting, and failure policy.

Default backend is a scripted mock. AG2 and CrewAI live in separate wheelhouses
because they pin different openai major versions. This file does not import them
so the mock path has no extra deps.
"""
from __future__ import annotations

import argparse
import json
import os
import time
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Budget:
    max_steps: int = 8
    max_tokens_est: int = 2000
    used_tokens_est: int = 0
    usd_per_1k: float = 0.0

    def charge(self, tokens: int) -> None:
        self.used_tokens_est += tokens
        if self.used_tokens_est > self.max_tokens_est:
            raise RuntimeError("budget_exceeded")

    def cost_usd(self) -> float:
        return self.used_tokens_est / 1000.0 * self.usd_per_1k


@dataclass
class SharedState:
    topic: str
    notes: list[str] = field(default_factory=list)
    draft: str = ""
    critique: str = ""
    errors: list[str] = field(default_factory=list)


def researcher(state: SharedState) -> None:
    src = Path(__file__).resolve().parents[1] / "fixtures" / "brief_cn.md"
    text = src.read_text(encoding="utf-8")
    state.notes.append(text.strip().splitlines()[0])
    state.notes.append("来源: fixtures/brief_cn.md")


def writer(state: SharedState) -> None:
    if not state.notes:
        raise RuntimeError("no_research")
    state.draft = "摘要：" + "；".join(state.notes)


def critic(state: SharedState) -> None:
    if "来源" not in state.draft:
        state.critique = "缺引用来源，需要重写。"
        raise RuntimeError("missing_citation")
    state.critique = "有来源标注，通过。"


def run_mock(topic: str) -> dict:
    budget = Budget()
    state = SharedState(topic=topic)
    t0 = time.time()
    roles = [("researcher", researcher), ("writer", writer), ("critic", critic)]
    log = []
    for name, fn in roles:
        try:
            budget.charge(120)
            fn(state)
            log.append({"role": name, "ok": True})
        except Exception as e:
            state.errors.append(f"{name}:{e}")
            log.append({"role": name, "ok": False, "error": str(e)})
            if name == "writer":
                break
    return {
        "ok": not state.errors,
        "backend": "mock",
        "shared_state": {
            "notes": state.notes,
            "draft": state.draft,
            "critique": state.critique,
            "errors": state.errors,
        },
        "cost": {"est_tokens": budget.used_tokens_est, "usd": budget.cost_usd()},
        "latency_s": round(time.time() - t0, 3),
        "log": log,
        "verified": False,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--task-file", default=str(Path(__file__).resolve().parents[1] / "examples" / "task_brief.json"))
    parser.add_argument("--mode", default=os.environ.get("AGENT_LLM_MODE", "mock"))
    args = parser.parse_args()
    task = json.loads(Path(args.task_file).read_text(encoding="utf-8"))
    if args.mode != "mock":
        print(json.dumps({
            "ok": False,
            "error": "non-mock backends are wired via AG2/CrewAI extra scripts; not executed this round",
            "hint": "see scripts/ag2_notes_cn.md and scripts/crewai_notes_cn.md",
        }, ensure_ascii=False, indent=2))
        return
    print(json.dumps(run_mock(task["topic"]), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
