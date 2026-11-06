#!/usr/bin/env python3
"""Local-document RAG with citations.

Embedding backends:
  hash  — deterministic token hashing (pipeline demo only, NOT semantic)
  local — llama-server /v1/embeddings
  hf    — sentence-transformers (optional extra wheelhouse + weights)

This round did not execute any backend.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "shared"))
from local_openai_en import client_kwargs, model_name  # noqa: E402


@dataclass
class Chunk:
    doc_id: str
    path: str
    i: int
    text: str
    vec: list[float]


def chunk_text(text: str, size: int = 400, overlap: int = 60) -> list[str]:
    text = re.sub(r"\s+", " ", text).strip()
    out = []
    i = 0
    while i < len(text):
        out.append(text[i : i + size])
        i += max(1, size - overlap)
    return out or [""]


def hash_embed(text: str, dim: int = 64) -> list[float]:
    vec = [0.0] * dim
    for tok in re.findall(r"[\w\u4e00-\u9fff]+", text.lower()):
        h = int(hashlib.sha256(tok.encode("utf-8")).hexdigest(), 16)
        vec[h % dim] += 1.0
        vec[(h // dim) % dim] -= 0.25
    n = math.sqrt(sum(x * x for x in vec)) or 1.0
    return [x / n for x in vec]


def cosine(a: list[float], b: list[float]) -> float:
    return sum(x * y for x, y in zip(a, b)) / (
        (math.sqrt(sum(x * x for x in a)) or 1.0) * (math.sqrt(sum(y * y for y in b)) or 1.0)
    )


def local_embed(texts: list[str]) -> list[list[float]]:
    from openai import OpenAI

    info = client_kwargs()
    client = OpenAI(**info["openai_kwargs"])
    model = os.environ.get("AGENT_EMBED_MODEL", "bge-small-en-v1.5")
    resp = client.embeddings.create(model=model, input=texts)
    return [d.embedding for d in resp.data]


def hf_embed(texts: list[str]) -> list[list[float]]:
    from sentence_transformers import SentenceTransformer

    path = os.environ.get(
        "AGENT_EMBED_PATH",
        str(ROOT / "models" / "embeddings" / "bge-small-en-v1.5"),
    )
    model = SentenceTransformer(path)
    arr = model.encode(texts, normalize_embeddings=True)
    return [v.tolist() for v in arr]


def load_docs(folder: Path) -> list[Chunk]:
    chunks: list[Chunk] = []
    for p in sorted(folder.glob("**/*")):
        if p.suffix.lower() not in {".txt", ".md"}:
            continue
        text = p.read_text(encoding="utf-8")
        for i, c in enumerate(chunk_text(text)):
            chunks.append(Chunk(doc_id=p.stem, path=str(p), i=i, text=c, vec=[]))
    return chunks


def embed_chunks(chunks: list[Chunk], backend: str) -> None:
    texts = [c.text for c in chunks]
    if backend == "hash":
        vecs = [hash_embed(t) for t in texts]
    elif backend == "local":
        vecs = local_embed(texts)
    elif backend == "hf":
        vecs = hf_embed(texts)
    else:
        raise SystemExit(f"unknown backend {backend}")
    for c, v in zip(chunks, vecs):
        c.vec = v


def retrieve(chunks: list[Chunk], query: str, backend: str, k: int = 3) -> list[tuple[float, Chunk]]:
    qv = {"hash": hash_embed, "local": lambda t: local_embed([t])[0], "hf": lambda t: hf_embed([t])[0]}[backend](query)
    scored = sorted(((cosine(qv, c.vec), c) for c in chunks), key=lambda x: x[0], reverse=True)
    return scored[:k]


def maybe_rerank(query: str, hits: list[tuple[float, Chunk]]) -> list[tuple[float, Chunk]]:
    path = os.environ.get("AGENT_RERANK_PATH", "")
    if not path:
        return hits
    # Optional CrossEncoder; not executed this round.
    from sentence_transformers import CrossEncoder

    ce = CrossEncoder(path)
    pairs = [(query, h[1].text) for h in hits]
    scores = ce.predict(pairs)
    ranked = sorted(zip(scores, [h[1] for h in hits]), key=lambda x: float(x[0]), reverse=True)
    return [(float(s), c) for s, c in ranked]


def answer(query: str, hits: list[tuple[float, Chunk]], backend: str) -> dict:
    cites = [
        {"doc_id": c.doc_id, "chunk": c.i, "path": c.path, "score": round(s, 4), "text": c.text[:240]}
        for s, c in hits
    ]
    context = "\n\n".join(f"[{i}] {c['text']}" for i, c in enumerate(cites))
    if backend == "hash" or os.environ.get("AGENT_LLM_MODE", "mock") == "mock":
        return {
            "answer": "示意回答：请根据引用片段自行阅读。hash 嵌入不是语义检索。",
            "citations": cites,
            "backend": backend,
            "llm": "mock",
        }
    from openai import OpenAI

    info = client_kwargs()
    client = OpenAI(**info["openai_kwargs"])
    prompt = (
        "只根据下列片段回答，并在句末用 [n] 引用。片段不足时说不知道。\n"
        f"{context}\n\n问题：{query}"
    )
    resp = client.chat.completions.create(model=model_name(), messages=[{"role": "user", "content": prompt}], temperature=0)
    return {"answer": resp.choices[0].message.content, "citations": cites, "backend": backend, "llm": info["mode"], "verified": False}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--docs", default=str(Path(__file__).resolve().parents[1] / "fixtures" / "docs"))
    parser.add_argument("--query-file", default=str(Path(__file__).resolve().parents[1] / "examples" / "queries.json"))
    parser.add_argument("--backend", default=os.environ.get("AGENT_EMBED_BACKEND", "hash"), choices=["hash", "local", "hf"])
    args = parser.parse_args()
    chunks = load_docs(Path(args.docs))
    embed_chunks(chunks, args.backend)
    queries = json.loads(Path(args.query_file).read_text(encoding="utf-8"))["queries"]
    out = []
    for q in queries:
        hits = retrieve(chunks, q, args.backend)
        hits = maybe_rerank(q, hits)
        out.append({"query": q, **answer(q, hits, args.backend)})
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
