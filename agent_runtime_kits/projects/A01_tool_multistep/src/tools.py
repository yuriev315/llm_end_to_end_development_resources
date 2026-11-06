"""Deterministic tools for the multi-step demo. No network, no shell."""
from __future__ import annotations

import ast
import operator
import time
from typing import Any

OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.USub: operator.neg,
    ast.Pow: operator.pow,
}


def _eval(node: ast.AST) -> float:
    if isinstance(node, ast.Expression):
        return _eval(node.body)
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return float(node.value)
    if isinstance(node, ast.BinOp) and type(node.op) in OPS:
        return OPS[type(node.op)](_eval(node.left), _eval(node.right))
    if isinstance(node, ast.UnaryOp) and type(node.op) in OPS:
        return OPS[type(node.op)](_eval(node.operand))
    raise ValueError("只允许 + - * / ** 与数字")


def calculator(expr: str) -> dict[str, Any]:
    tree = ast.parse(expr, mode="eval")
    value = _eval(tree)
    return {"expr": expr, "value": value}


def now_iso() -> dict[str, Any]:
    return {"utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}


class Scratchpad:
    def __init__(self) -> None:
        self.notes: list[str] = []

    def add(self, text: str) -> dict[str, Any]:
        self.notes.append(text)
        return {"n": len(self.notes), "last": text}

    def list_notes(self) -> dict[str, Any]:
        return {"notes": list(self.notes)}


TOOLS = {
    "calculator": {
        "description": "计算只含数字与 + - * / ** 的表达式",
        "fn": lambda pad, expr: calculator(expr),
    },
    "now_iso": {
        "description": "返回当前 UTC 时间",
        "fn": lambda pad: now_iso(),
    },
    "note_add": {
        "description": "把一条短备注写入便笺",
        "fn": lambda pad, text: pad.add(text),
    },
    "note_list": {
        "description": "列出便笺",
        "fn": lambda pad: pad.list_notes(),
    },
}
