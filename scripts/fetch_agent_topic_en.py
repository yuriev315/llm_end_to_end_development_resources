#!/usr/bin/env python3
"""Download AI Agent literature, pinned sources, docs, runtimes, and wheels.

Model weights (GGUF / safetensors / bin / pt) are URL-only: write ``*.url.txt``
and never download the blobs. Tokenizer/config sidecars may still be fetched.
Collection only: no install, no model load, no agent execution.
Resume-safe. Retrieval date: 2026-10-30.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request
import zipfile
from pathlib import Path

DEST = Path("ai_agent")
KNOW = DEST
WIN = DEST / "windows"
PIP_PYZ = Path("tools/pip.pyz")
CACHE = Path("ai_agent/state/pip_cache")
LOG = Path("ai_agent/state/logs/agent_topic")
UA = "offline-library-agent-topic/2026-10-30"
RETRIEVED = "2026-10-30"

PAPERS = KNOW / "_public" / "papers" / "agent"
SRC = KNOW / "11_ai_agent" / "implementations"
DOCS = KNOW / "11_ai_agent" / "docs_html"
EVALS = KNOW / "11_ai_agent" / "experiments"
KITS = KNOW / "agent_runtime_kits"
WIN_KITS = WIN / "agent_runtime_kits"
FAIL = KNOW / "inventories" / "agent_download_failures_cn.csv"
OKCSV = KNOW / "inventories" / "agent_downloads_cn.csv"

LINUX_PLATS = [
    "manylinux2014_x86_64",
    "manylinux_2_17_x86_64",
    "manylinux_2_24_x86_64",
    "manylinux_2_27_x86_64",
    "manylinux_2_28_x86_64",
    "manylinux_2_31_x86_64",
    "manylinux_2_34_x86_64",
    "manylinux_2_35_x86_64",
    "linux_x86_64",
    "any",
]

PAPER_SEED = [
    # id, title_words, topic, note
    ("2201.11903", "Chain Thought", "mechanisms", "CoT"),
    ("2210.03629", "ReAct", "literature", "ReAct"),
    ("2205.00445", "MRKL", "mechanisms", "MRKL systems"),
    ("2302.04761", "Toolformer", "literature", "Toolformer"),
    ("2303.11366", "Reflexion", "literature", "Reflexion"),
    ("2304.03442", "Generative Agents", "literature", "Generative Agents"),
    ("2305.10601", "Tree Thoughts", "mechanisms", "Tree of Thoughts"),
    ("2303.17651", "Self-Refine", "mechanisms", "Self-Refine"),
    ("2305.18323", "ReWOO", "mechanisms", "ReWOO"),
    ("2309.02427", "Cognitive Architectures", "mechanisms", "CoALA"),
    ("2401.05566", "Executable Code Actions", "mechanisms", "CodeAct"),
    ("2310.08560", "MemGPT", "rag_memory", "MemGPT"),
    ("2305.15334", "Gorilla", "mechanisms", "Gorilla"),
    ("2307.16789", "ToolLLM", "mechanisms", "ToolLLM"),
    ("2303.17580", "HuggingGPT", "applications", "HuggingGPT"),
    ("2305.16291", "Voyager", "applications", "Voyager"),
    ("2303.17760", "CAMEL", "multi_agent", "CAMEL"),
    ("2308.08155", "AutoGen", "multi_agent", "AutoGen"),
    ("2308.00352", "MetaGPT", "multi_agent", "MetaGPT"),
    ("2311.10709", "ChatDev", "multi_agent", "ChatDev"),
    ("2309.07864", "Rise Potential", "literature", "Xi et al. survey"),
    ("2402.01680", "Survey LLM-based Autonomous", "literature", "Wang et al. survey"),
    ("2406.05804", "Prominent Paradigms", "literature", "tool/plan/feedback survey"),
    ("2503.23037", "Agentic Large Language", "literature", "2025 agentic LLM survey"),
    ("2005.11401", "Retrieval-Augmented Generation", "rag_memory", "Lewis RAG"),
    ("2004.04906", "Dense Passage Retrieval", "rag_memory", "DPR"),
    ("2212.10496", "Hypothetical Document", "rag_memory", "HyDE"),
    ("2310.11511", "Self-RAG", "rag_memory", "Self-RAG"),
    ("2312.10997", "Retrieval-Augmented Generation", "rag_memory", "Gao RAG survey"),
    ("2401.15884", "RAPTOR", "rag_memory", "RAPTOR"),
    ("2402.19473", "Corrective Retrieval", "rag_memory", "CRAG"),
    ("2404.16130", "Local Global Graph", "rag_memory", "GraphRAG"),
    ("2308.03688", "AgentBench", "eval_safety", "AgentBench"),
    ("2311.12983", "GAIA", "eval_safety", "GAIA"),
    ("2310.06770", "SWE-bench", "eval_safety", "SWE-bench"),
    ("2405.15793", "SWE-agent", "applications", "SWE-agent"),
    ("2406.12045", "tau-bench", "eval_safety", "tau-bench"),
    ("2306.05685", "Judging LLM-as-a-Judge", "eval_safety", "LLM-as-a-Judge"),
    ("2307.13854", "WebArena", "eval_safety", "WebArena"),
    ("2402.05930", "OSWorld", "eval_safety", "OSWorld"),
    ("2211.09527", "Ignore This Title", "eval_safety", "Ignore Previous Prompt"),
    ("2302.12173", "Not What You've Signed", "eval_safety", "Greshake prompt injection"),
    ("2406.13352", "AgentDojo", "eval_safety", "AgentDojo"),
    ("2410.09024", "AgentHarm", "eval_safety", "AgentHarm"),
    ("2403.02691", "InjecAgent", "eval_safety", "InjecAgent"),
    ("2402.01030", "OpenDevin", "applications", "OpenHands/OpenDevin"),
    ("2310.03714", "DSPy", "engineering", "DSPy"),
    ("2401.14069", "AgentScope", "multi_agent", "AgentScope"),
    ("2402.01817", "Understanding planning", "mechanisms", "LLM agent planning"),
    ("2408.02666", "TheAgentCompany", "eval_safety", "TheAgentCompany"),
    ("2407.01532", "AgentBoard", "eval_safety", "AgentBoard"),
    ("2406.04692", "Multi-Agent Collaboration", "multi_agent", "multi-agent survey"),
    ("2404.06474", "ToolSandbox", "eval_safety", "ToolSandbox"),
    ("2402.07712", "State of LLM Agents", "literature", "optional follow-on"),
]

SOURCE_SEED = [
    ("langchain-ai/langgraph", "1.2.18", "MIT", "LangGraph pinned to env-15 wheel"),
    ("ag2ai/ag2", "v1.2.2", "CC-BY-4.0 / Apache-2.0 see repo", "AutoGen successor AG2"),
    ("microsoft/autogen", "v0.2.37", "MIT", "historical AutoGen 0.2; upstream archived"),
    ("crewAIInc/crewAI", "1.15.33", "MIT", "CrewAI; fallback 1.15.32"),
    ("openai/openai-agents-python", "v0.24.0", "MIT", "OpenAI Agents SDK"),
    ("modelcontextprotocol/modelcontextprotocol", "2026-07-28", "MIT", "MCP spec"),
    ("modelcontextprotocol/python-sdk", "v1.16.0", "MIT", "MCP Python SDK; tag probed"),
    ("huggingface/smolagents", "v1.22.0", "Apache-2.0", "HF smolagents; tag probed"),
    ("Aider-AI/aider", "v0.86.2", "Apache-2.0", "aider coding agent"),
    ("browser-use/browser-use", "0.13.14", "MIT", "browser-use; py>=3.11"),
    ("princeton-nlp/SWE-bench", "v2.1.0", "MIT", "SWE-bench code; full dataset NOT downloaded"),
    ("THUDM/AgentBench", "v0.1", "Apache-2.0", "AgentBench; tag probed"),
    ("sierra-research/tau-bench", "main", "MIT", "tau-bench snapshot; main if untagged"),
    ("ethz-spylab/agentdojo", "v0.1.15", "Apache-2.0", "AgentDojo eval; tag probed"),
    ("UKGovernmentBEIS/inspect_ai", "v0.3.100", "MIT", "Inspect AI; tag probed"),
    ("gaia-benchmark/GAIA", "main", "research", "GAIA metadata if public; files may fail"),
]

DOC_MIRRORS = [
    ("openai_agents_python", "https://openai.github.io/openai-agents-python/", 80),
    ("langgraph", "https://docs.langchain.com/oss/python/langgraph/", 80),
    ("ag2", "https://docs.ag2.ai/", 80),
    ("crewai", "https://docs.crewai.com/", 80),
    ("mcp", "https://modelcontextprotocol.io/", 80),
    ("aider", "https://aider.chat/docs/", 40),
]

# Direct requirements per project. Closures resolved by pip download.
PROJECTS = {
    "A01_tool_multistep": {
        "title": "基础工具调用与多步任务",
        "py": ["3.10", "3.12"],
        "req": [
            "openai-agents==0.24.0",
            "openai>=3.20.0,<4",
            "pydantic>=2.7,<3",
            "httpx>=0.27",
            "python-dotenv>=1.0",
            "mcp>=1.12.0",
        ],
    },
    "A02_local_doc_rag": {
        "title": "本地文档 RAG",
        "py": ["3.10", "3.12"],
        "req": [
            "langgraph==1.2.18",
            "langchain==1.4.7",
            "langchain-core==1.7.3",
            "langchain-text-splitters==1.1.3",
            "langchain-community==0.4.2",
            "pypdf>=5.0",
            "numpy>=1.26",
            "httpx>=0.27",
            "python-dotenv>=1.0",
            "openai>=3.20.0,<4",
            "tiktoken>=0.7",
        ],
    },
    "A02_optional_hf_embed": {
        "title": "可选 Hugging Face 嵌入/重排（需 torch）",
        "py": ["3.10", "3.12"],
        "req": [
            "sentence-transformers>=3.0",
            "transformers>=4.44",
            "faiss-cpu>=1.8",
            "torch",
        ],
        "extra_index": "https://download.pytorch.org/whl/cpu",
        "optional": True,
        "parent": "A02_local_doc_rag",
    },
    "A03_coding_files": {
        "title": "编码与文件操作",
        "py": ["3.10", "3.12"],
        "req": [
            "aider-chat==0.86.2",
            "openai-agents==0.24.0",
            "openai>=3.20.0,<4",
            "python-dotenv>=1.0",
        ],
    },
    "A04_browser_automation": {
        "title": "浏览器自动化",
        "py": ["3.10", "3.12"],
        "req_by_py": {
            "3.10": [
                "playwright>=1.48",
                "openai-agents==0.24.0",
                "openai>=3.20.0,<4",
                "python-dotenv>=1.0",
            ],
            "3.12": [
                "playwright>=1.48",
                "browser-use==0.13.14",
                "openai-agents==0.24.0",
                "openai>=3.20.0,<4",
                "python-dotenv>=1.0",
            ],
        },
        "skip_note_310": "browser-use 要求 Python>=3.11，3.10 仅准备 Playwright + Agents SDK 自定义项目",
    },
    "A05_multi_agent_ag2": {
        "title": "多 Agent 协作（AG2）",
        "py": ["3.10", "3.12"],
        "req": ["ag2==1.2.2", "openai>=3.37.0,<4", "python-dotenv>=1.0"],
        "parent": "A05_multi_agent",
    },
    "A05_multi_agent_crewai": {
        "title": "多 Agent 协作（CrewAI，独立环境）",
        "py": ["3.10", "3.12"],
        "req": ["crewai==1.15.33", "python-dotenv>=1.0"],
        "parent": "A05_multi_agent",
        "note": "CrewAI 1.15.33 声明 openai>=2.30,<3，与 Agents SDK / AG2 的 openai 3.x 冲突，必须独立 wheelhouse",
    },
}

MODELS = [
    {
        "id": "qwen25_05b_q4km",
        "tier": "cpu_smoke",
        "repo": "Qwen/Qwen2.5-0.5B-Instruct-GGUF",
        "file": "qwen2.5-0.5b-instruct-q4_k_m.gguf",
        "license": "Apache-2.0",
        "hw": "CPU RAM 约 1–2 GiB；不作为可用工具调用模型",
        "tool_call": "未验证；参数量过小，预期工具调用/结构化输出经常失败",
        "dest": "cpu_baseline",
        "public": True,
    },
    {
        "id": "qwen25_15b_q4km",
        "tier": "cpu_baseline",
        "repo": "Qwen/Qwen2.5-1.5B-Instruct-GGUF",
        "file": "qwen2.5-1.5b-instruct-q4_k_m.gguf",
        "license": "Apache-2.0",
        "hw": "CPU RAM 约 3–4 GiB，x86-64 AVX2 更佳",
        "tool_call": "未验证；接口可接 OpenAI 兼容服务，不代表能稳定工具调用",
        "dest": "cpu_baseline",
        "public": True,
    },
    {
        "id": "qwen25_3b_q4km",
        "tier": "cpu_better",
        "repo": "Qwen/Qwen2.5-3B-Instruct-GGUF",
        "file": "qwen2.5-3b-instruct-q4_k_m.gguf",
        "license": "Apache-2.0",
        "hw": "CPU RAM 约 5–8 GiB",
        "tool_call": "未验证；相对 0.5B/1.5B 更有机会，仍不能标为已验证",
        "dest": "cpu_baseline",
        "public": True,
    },
    {
        "id": "qwen25_7b_q4km",
        "tier": "gpu_optional",
        "repo": "Qwen/Qwen2.5-7B-Instruct-GGUF",
        "file": "qwen2.5-7b-instruct-q4_k_m.gguf",
        "license": "Apache-2.0",
        "hw": "建议 GPU VRAM ≥ 8 GiB 或 CPU RAM ≥ 12 GiB；本机未测",
        "tool_call": "未验证；常见社区经验认为 7B 级更接近可用工具调用，不是保证",
        "dest": "gpu_optional",
        "public": True,
        "shards": [
            "qwen2.5-7b-instruct-q4_k_m-00001-of-00002.gguf",
            "qwen2.5-7b-instruct-q4_k_m-00002-of-00002.gguf",
        ],
    },
]

HF_SMALL = [
    # embeddings / rerank / tokenizer sidecars
    {
        "repo": "BAAI/bge-small-en-v1.5",
        "files": [
            "model.safetensors",
            "config.json",
            "tokenizer.json",
            "tokenizer_config.json",
            "special_tokens_map.json",
            "vocab.txt",
            "sentence_bert_config.json",
            "modules.json",
            "1_Pooling/config.json",
            "README.md",
        ],
        "dest": "embeddings/bge-small-en-v1.5",
        "license": "MIT",
        "hw": "CPU 即可，约 130 MiB 权重",
    },
    {
        "repo": "BAAI/bge-small-zh-v1.5",
        "files": [
            "model.safetensors",
            "config.json",
            "tokenizer.json",
            "tokenizer_config.json",
            "special_tokens_map.json",
            "vocab.txt",
            "sentence_bert_config.json",
            "modules.json",
            "1_Pooling/config.json",
            "README.md",
        ],
        "dest": "embeddings/bge-small-zh-v1.5",
        "license": "MIT",
        "hw": "CPU 即可，约 95 MiB 权重",
    },
    {
        "repo": "BAAI/bge-reranker-base",
        "files": [
            "model.safetensors",
            "pytorch_model.bin",
            "config.json",
            "tokenizer.json",
            "tokenizer_config.json",
            "special_tokens_map.json",
            "vocab.txt",
            "README.md",
        ],
        "dest": "rerankers/bge-reranker-base",
        "license": "MIT",
        "hw": "CPU 可用但慢；建议 4+ GiB RAM。权重只记地址，不下载",
        "pick_first": ["model.safetensors", "pytorch_model.bin"],
    },
    {
        "repo": "Qwen/Qwen2.5-1.5B-Instruct",
        "files": ["tokenizer.json", "tokenizer_config.json", "vocab.json", "merges.txt", "LICENSE", "README.md"],
        "dest": "tokenizers/Qwen2.5-1.5B-Instruct",
        "license": "Apache-2.0",
        "hw": "仅分词器/模板，不是权重",
    },
]

GGUF_EMBED = [
    {
        "repo": "CompendiumLabs/bge-small-en-v1.5-gguf",
        "file": "bge-small-en-v1.5-q8_0.gguf",
        "alts": [
            ("ggml-org/bge-small-en-v1.5-GGUF", "bge-small-en-v1.5-q8_0.gguf"),
            ("gpustack/bge-small-en-v1.5-GGUF", "bge-small-en-v1.5-Q8_0.gguf"),
        ],
        "dest": "embeddings",
        "license": "MIT (original BGE) + GGUF conversion",
    }
]


def log(msg: str) -> None:
    LOG.mkdir(parents=True, exist_ok=True)
    line = f"{time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())} {msg}"
    print(line, flush=True)
    (LOG / "fetch_en.log").open("a", encoding="utf-8").write(line + "\n")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def record(kind: str, name: str, status: str, path: str, source: str, note: str, size: int = 0) -> None:
    OKCSV.parent.mkdir(parents=True, exist_ok=True)
    new = not OKCSV.exists()
    with OKCSV.open("a", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        if new:
            w.writerow(["kind", "name", "status", "path", "source", "bytes", "retrieved", "note"])
        w.writerow([kind, name, status, path, source, size, RETRIEVED, note])


def fail(kind: str, name: str, source: str, reason: str) -> None:
    FAIL.parent.mkdir(parents=True, exist_ok=True)
    new = not FAIL.exists()
    with FAIL.open("a", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        if new:
            w.writerow(["kind", "name", "source", "reason", "retrieved"])
        w.writerow([kind, name, source, reason, RETRIEVED])
    log(f"FAIL {kind} {name}: {reason}")


def request(url: str, dest: Path, timeout: int = 120) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    part = dest.with_suffix(dest.suffix + ".part")
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "*/*"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        with part.open("wb") as out:
            while True:
                chunk = resp.read(1024 * 1024)
                if not chunk:
                    break
                out.write(chunk)
    part.replace(dest)


def download(url: str, dest: Path, min_bytes: int = 64, timeout: int = 180, retries: int = 4) -> bool:
    if dest.exists() and dest.stat().st_size >= min_bytes:
        return True
    last = ""
    for i in range(retries):
        try:
            request(url, dest, timeout=timeout)
            if dest.exists() and dest.stat().st_size >= min_bytes:
                return True
            last = f"too small {dest.stat().st_size if dest.exists() else 0}"
        except Exception as e:
            last = str(e)
            time.sleep(2 + i * 3)
    return False


def gh_api(path: str) -> dict | list | None:
    url = "https://api.github.com" + path
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/vnd.github+json"})
        with urllib.request.urlopen(req, timeout=60) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        log(f"github api fail {path}: {e}")
        return None


def fetch_papers() -> None:
    PAPERS.mkdir(parents=True, exist_ok=True)
    for arid, words, topic, note in PAPER_SEED:
        dest = PAPERS / f"{arid.replace('.', '_')}_{note.replace(' ', '_')}.pdf"
        urls = [
            f"https://arxiv.org/pdf/{arid}.pdf",
            f"https://export.arxiv.org/pdf/{arid}.pdf",
            f"https://arxiv.org/pdf/{arid}v1.pdf",
        ]
        ok = False
        used = ""
        for u in urls:
            if download(u, dest, min_bytes=20_000, timeout=120):
                head = dest.read_bytes()[:8]
                if head.startswith(b"%PDF"):
                    ok = True
                    used = u
                    break
                dest.unlink(missing_ok=True)
        if ok:
            record("paper", arid, "ok", str(dest), used, f"{note}; topic={topic}; words={words}", dest.stat().st_size)
            log(f"paper ok {arid} {dest.stat().st_size}")
        else:
            fail("paper", arid, urls[0], "download or PDF header failed")
        time.sleep(1.2)


def try_github_tarball(repo: str, ref: str, dest: Path) -> str | None:
    urls = [
        f"https://github.com/{repo}/archive/refs/tags/{ref}.tar.gz",
        f"https://codeload.github.com/{repo}/tar.gz/refs/tags/{ref}",
        f"https://github.com/{repo}/archive/{ref}.tar.gz",
        f"https://codeload.github.com/{repo}/tar.gz/{ref}",
    ]
    for u in urls:
        if download(u, dest, min_bytes=2000, timeout=180):
            # github sometimes returns HTML
            head = dest.read_bytes()[:4]
            if head.startswith(b"\x1f\x8b") or head.startswith(b"PK"):
                return u
            dest.unlink(missing_ok=True)
    return None


def fetch_sources() -> None:
    SRC.mkdir(parents=True, exist_ok=True)
    for repo, tag, lic, note in SOURCE_SEED:
        slug = repo.replace("/", "__") + f"_{tag}"
        dest = SRC / f"{slug}.tar.gz"
        used = try_github_tarball(repo, tag, dest)
        if not used and tag != "main":
            # probe latest release tag
            data = gh_api(f"/repos/{repo}/releases/latest")
            if isinstance(data, dict) and data.get("tag_name"):
                alt = data["tag_name"]
                dest = SRC / f"{repo.replace('/', '__')}_{alt}.tar.gz"
                used = try_github_tarball(repo, alt, dest)
                note = note + f"; used latest {alt}"
        if not used:
            used = try_github_tarball(repo, "main", SRC / f"{repo.replace('/', '__')}_main.tar.gz")
            dest = SRC / f"{repo.replace('/', '__')}_main.tar.gz"
            note = note + "; fell back to main snapshot"
        if used and dest.exists():
            record("source", repo, "ok", str(dest), used, f"{lic}; {note}", dest.stat().st_size)
            log(f"source ok {repo} {dest.name} {dest.stat().st_size}")
        else:
            fail("source", repo, f"github:{tag}", note)


def fetch_docs() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    for name, url, quota_mb in DOC_MIRRORS:
        out = DOCS / name
        out.mkdir(parents=True, exist_ok=True)
        marker = out / "_MIRROR_en.txt"
        if marker.exists() and any(out.glob("**/*.html")):
            record("docs", name, "ok_cached", str(out), url, "existing mirror", 0)
            continue
        cmd = [
            "wget", "-q", "-r", "-l", "3", "-np", "-nH", "--cut-dirs=0",
            "-p", "-k", "-E",
            f"--quota={quota_mb}m",
            "--timeout=20", "--tries=2",
            "-R", "woff,woff2,ttf,mp4,webm,zip,tar,gz",
            "-U", UA,
            "-P", str(out),
            url,
        ]
        log("docs wget " + name)
        try:
            subprocess.run(cmd, check=False, timeout=300)
        except Exception as e:
            fail("docs", name, url, str(e))
            continue
        htmls = list(out.glob("**/*.html"))
        marker.write_text(f"url={url}\nretrieved={RETRIEVED}\nhtml_files={len(htmls)}\nquota_mb={quota_mb}\n", encoding="utf-8")
        if htmls:
            record("docs", name, "ok", str(out), url, f"html={len(htmls)} quota={quota_mb}m", sum(p.stat().st_size for p in htmls))
        else:
            fail("docs", name, url, "no html files")


def fetch_llama_cpp() -> None:
    tag = "b11998"
    data = gh_api(f"/repos/ggml-org/llama.cpp/releases/tags/{tag}")
    assets = []
    if isinstance(data, dict):
        assets = [a.get("name") for a in data.get("assets", []) if a.get("name")]
        if data.get("tag_name"):
            tag = data["tag_name"]
    want_sub = [
        "ubuntu-x64.tar.gz",
        "win-cpu-x64.zip",
        "ubuntu-vulkan-x64.tar.gz",
        "win-vulkan-x64.zip",
        "ubuntu-cuda-12",
        "win-cuda-12",
        "cudart-llama-bin-win-cuda-12",
    ]
    dest_linux = KITS / "runtimes" / "linux_x86_64" / "llama_cpp"
    dest_win = KITS / "runtimes" / "windows_x86_64" / "llama_cpp"
    dest_linux.mkdir(parents=True, exist_ok=True)
    dest_win.mkdir(parents=True, exist_ok=True)
    (WIN_KITS / "runtimes" / "windows_x86_64" / "llama_cpp").mkdir(parents=True, exist_ok=True)
    names = assets or [
        f"llama-{tag}-bin-ubuntu-x64.tar.gz",
        f"llama-{tag}-bin-win-cpu-x64.zip",
        f"llama-{tag}-bin-ubuntu-vulkan-x64.tar.gz",
        f"llama-{tag}-bin-win-vulkan-x64.zip",
    ]
    picked = []
    for name in names:
        if not any(s in name for s in want_sub):
            continue
        url = f"https://github.com/ggml-org/llama.cpp/releases/download/{tag}/{name}"
        if "win-" in name or name.endswith(".zip"):
            dest = dest_win / name
        else:
            dest = dest_linux / name
        gpu = "cuda" in name.lower() or "vulkan" in name.lower()
        if gpu:
            dest = (KITS / "runtimes" / ("windows_x86_64" if "win-" in name else "linux_x86_64") / "llama_cpp_gpu" / name)
        if download(url, dest, min_bytes=100_000, timeout=300):
            record("runtime", name, "ok", str(dest), url, f"llama.cpp {tag}", dest.stat().st_size)
            picked.append(name)
            if "win-" in name:
                wdest = WIN_KITS / "runtimes" / "windows_x86_64" / ("llama_cpp_gpu" if gpu else "llama_cpp") / name
                wdest.parent.mkdir(parents=True, exist_ok=True)
                if not wdest.exists():
                    try:
                        os.link(dest, wdest)
                    except OSError:
                        import shutil
                        shutil.copy2(dest, wdest)
        else:
            fail("runtime", name, url, "llama.cpp asset")
    (dest_linux / "SNAPSHOT_en.txt").write_text(
        f"tag={tag}\nretrieved={RETRIEVED}\nassets={picked}\nnote=binaries only; not executed this round\n",
        encoding="utf-8",
    )


def fetch_nodejs() -> None:
    ver = "v22.23.4"
    files = [
        (f"https://nodejs.org/dist/{ver}/node-{ver}-linux-x64.tar.xz",
         KITS / "runtimes" / "linux_x86_64" / "nodejs" / f"node-{ver}-linux-x64.tar.xz"),
        (f"https://nodejs.org/dist/{ver}/node-{ver}-win-x64.zip",
         KITS / "runtimes" / "windows_x86_64" / "nodejs" / f"node-{ver}-win-x64.zip"),
        (f"https://nodejs.org/dist/{ver}/SHASUMS256.txt",
         KITS / "runtimes" / "linux_x86_64" / "nodejs" / "SHASUMS256.txt"),
    ]
    for url, dest in files:
        if download(url, dest, min_bytes=200, timeout=180):
            record("runtime", dest.name, "ok", str(dest), url, f"Node.js {ver} official", dest.stat().st_size)
            if "win-x64" in dest.name:
                wdest = WIN_KITS / "runtimes" / "windows_x86_64" / "nodejs" / dest.name
                wdest.parent.mkdir(parents=True, exist_ok=True)
                if not wdest.exists():
                    try:
                        os.link(dest, wdest)
                    except OSError:
                        import shutil
                        shutil.copy2(dest, wdest)
        else:
            fail("runtime", dest.name, url, "nodejs")


def hf_url(repo: str, file: str) -> str:
    return f"https://huggingface.co/{repo}/resolve/main/{file}?download=true"


WEIGHT_SUFFIXES = {".gguf", ".safetensors", ".bin", ".pt", ".pth", ".onnx", ".ckpt"}


def write_url_file(dest: Path, url: str, extra: dict | None = None) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(url.rstrip() + "\n", encoding="utf-8")
    meta = {
        "url": url,
        "retrieved": RETRIEVED,
        "downloaded": False,
        "policy": "url_only_no_weight_file",
    }
    if extra:
        meta.update(extra)
    dest.with_suffix(dest.suffix + ".json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def _unlink_weight(path: Path) -> None:
    if path.exists() and path.is_file():
        path.unlink()
        log(f"removed weight {path}")


def fetch_models() -> None:
    """Record weight URLs only. Do not download GGUF/safetensors/bin/pt."""
    catalog = []
    for m in MODELS:
        extra = {k: v for k, v in m.items() if k != "alts"}
        extra["alts"] = [
            {"repo": r, "file": f, "url": hf_url(r, f)} for r, f in m.get("alts", [])
        ]
        files = list(m.get("shards") or [m["file"]])
        urls = []
        dest0 = None
        for fn in files:
            url = hf_url(m["repo"], fn)
            dest = KITS / "models" / m["dest"] / (fn + ".url.txt")
            write_url_file(dest, url, {**extra, "file": fn})
            record("model_url", f"{m['id']}/{fn}" if m.get("shards") else m["id"], "url_only", str(dest), url, m["tool_call"], 0)
            _unlink_weight(KITS / "models" / m["dest"] / fn)
            old_src = KITS / "models" / m["dest"] / (fn + ".source.json")
            if old_src.exists():
                old_src.unlink()
            urls.append({"file": fn, "url": url, "path": str(dest)})
            dest0 = dest0 or dest
        if m.get("shards"):
            logical = KITS / "models" / m["dest"] / (m["file"] + ".url.txt")
            note = (
                "Official Q4_K_M is split shards; single-file URL 404s. "
                "Merge after download: llama-gguf-split --merge "
                f"{m['shards'][0]} {m['file']}\n"
            )
            logical.write_text(note + "\n".join(u["url"] for u in urls) + "\n", encoding="utf-8")
            (logical.with_suffix(logical.suffix + ".json")).write_text(
                json.dumps(
                    {
                        "url": urls[0]["url"],
                        "retrieved": RETRIEVED,
                        "downloaded": False,
                        "policy": "url_only_no_weight_file",
                        "shard_urls": urls,
                        **extra,
                    },
                    ensure_ascii=False,
                    indent=2,
                ),
                encoding="utf-8",
            )
            dest0 = logical
        catalog.append({"id": m["id"], "url": urls[0]["url"] if urls else hf_url(m["repo"], m["file"]), "path": str(dest0), "shard_urls": urls, **extra})
        log(f"model url only {m['id']}")
        _unlink_weight(KITS / "models" / m["dest"] / m["file"])
    for spec in HF_SMALL:
        base = KITS / "models" / spec["dest"]
        any_ok = False
        weight_urls = []
        for fn in spec["files"]:
            dest = base / fn
            url = hf_url(spec["repo"], fn)
            if Path(fn).suffix.lower() in WEIGHT_SUFFIXES:
                write_url_file(Path(str(dest) + ".url.txt"), url, {"repo": spec["repo"], "file": fn, "license": spec["license"]})
                record("model_url", f"{spec['repo']}/{fn}", "url_only", str(dest) + ".url.txt", url, spec["license"], 0)
                _unlink_weight(dest)
                weight_urls.append({"file": fn, "url": url})
                continue
            if dest.exists() and dest.stat().st_size >= 20:
                any_ok = True
                record("model", f"{spec['repo']}/{fn}", "ok", str(dest), url, spec["license"], dest.stat().st_size)
                continue
            if download(url, dest, min_bytes=20, timeout=180):
                any_ok = True
                record("model", f"{spec['repo']}/{fn}", "ok", str(dest), url, spec["license"], dest.stat().st_size)
            else:
                fail("model", f"{spec['repo']}/{fn}", url, "hf sidecar")
        payload = {
            **spec,
            "retrieved": RETRIEVED,
            "sidecar_ok": any_ok,
            "downloaded_weights": False,
            "weight_urls": weight_urls,
        }
        (base / "SOURCE_en.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    for spec in GGUF_EMBED:
        candidates = [(spec["repo"], spec["file"])] + spec.get("alts", [])
        dest = KITS / "models" / spec["dest"] / (spec["file"] + ".url.txt")
        extra = {k: v for k, v in spec.items() if k != "alts"}
        extra["alts"] = [{"repo": r, "file": f, "url": hf_url(r, f)} for r, f in spec.get("alts", [])]
        write_url_file(dest, hf_url(spec["repo"], spec["file"]), extra)
        record("model_url", spec["file"], "url_only", str(dest), hf_url(spec["repo"], spec["file"]), spec["license"], 0)
        catalog.append({"id": spec["file"], "url": hf_url(spec["repo"], spec["file"]), "path": str(dest), **extra})
        for repo, fn in candidates:
            _unlink_weight(KITS / "models" / spec["dest"] / fn)
        log(f"model url only {spec['file']}")
    cat_path = KITS / "models" / "WEIGHTS_url_only.json"
    cat_path.write_text(
        json.dumps({"retrieved": RETRIEVED, "downloaded": False, "models": catalog}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    (KITS / "models" / "DO_NOT_DOWNLOAD_WEIGHTS.txt").write_text(
        "This topic records official/HF URLs for weights and does not store GGUF or safetensors.\n"
        f"retrieved={RETRIEVED}\n",
        encoding="utf-8",
    )


def pip_cmd(dest: Path, py: str, platform: str) -> list[str]:
    tag = py.replace(".", "")
    cmd = [
        sys.executable, str(PIP_PYZ), "download",
        "--dest", str(dest),
        "--python-version", py,
        "--implementation", "cp",
        "--abi", f"cp{tag}",
        "--abi", "abi3",
        "--abi", "none",
        "--only-binary", ":all:",
        "--cache-dir", str(CACHE),
        "--disable-pip-version-check",
        "--timeout", "120",
        "--retries", "4",
    ]
    if platform == "linux":
        for plat in LINUX_PLATS:
            cmd.extend(["--platform", plat])
    else:
        cmd.extend(["--platform", "win_amd64", "--platform", "any"])
    return cmd


def fetch_wheels() -> None:
    CACHE.mkdir(parents=True, exist_ok=True)
    LOG.mkdir(parents=True, exist_ok=True)
    for key, spec in PROJECTS.items():
        parent = spec.get("parent", key)
        for py in spec["py"]:
            reqs = spec.get("req_by_py", {}).get(py, spec.get("req", []))
            if spec.get("req_by_py") and py not in spec.get("req_by_py", {}):
                continue
            for platform, envroot in (
                ("linux", KITS / "projects" / parent / "environments" / f"py{py.replace('.', '')}_{'linux'}"),
                ("windows", WIN_KITS / "projects" / parent / "environments" / f"py{py.replace('.', '')}_windows"),
            ):
                if key.startswith("A02_optional") or key.startswith("A05_"):
                    envroot = envroot.parent / f"{key}_py{py.replace('.', '')}_{platform if platform=='linux' else 'windows'}"
                envroot.mkdir(parents=True, exist_ok=True)
                dest = envroot / "wheelhouse"
                dest.mkdir(parents=True, exist_ok=True)
                reqfile = envroot / "requirements_direct_en.txt"
                reqfile.write_text("\n".join(reqs) + "\n", encoding="utf-8")
                (envroot / "SNAPSHOT_en.txt").write_text(
                    f"project={key}\npython={py}\nplatform={platform}\nretrieved={RETRIEVED}\noptional={spec.get('optional', False)}\nnote={spec.get('note', spec.get('skip_note_310', ''))}\n",
                    encoding="utf-8",
                )
                cmd = pip_cmd(dest, py, platform)
                extra = spec.get("extra_index")
                if extra:
                    cmd.extend(["--extra-index-url", extra])
                cmd.extend(["-r", str(reqfile)])
                logf = LOG / f"wheels_{key}_{py}_{platform}.log"
                log(" ".join(cmd))
                with logf.open("w", encoding="utf-8") as fh:
                    fh.write("$ " + " ".join(cmd) + "\n")
                    fh.flush()
                    proc = subprocess.run(cmd, stdout=fh, stderr=subprocess.STDOUT, text=True)
                    fh.write(f"\n[exit {proc.returncode}]\n")
                wheels = sorted(dest.glob("*.whl"))
                lock = envroot / "requirements_lock_en.txt"
                # lock from filenames is not a pip freeze; record wheel names
                lock.write_text("\n".join(p.name for p in wheels) + "\n", encoding="utf-8")
                inv = envroot / "wheel_inventory_cn.csv"
                with inv.open("w", encoding="utf-8", newline="") as f:
                    w = csv.writer(f)
                    w.writerow(["filename", "bytes", "sha256"])
                    for p in wheels:
                        w.writerow([p.name, p.stat().st_size, sha256(p)])
                if proc.returncode == 0 and wheels:
                    record("wheels", f"{key}/{py}/{platform}", "ok", str(dest), "pypi", f"n={len(wheels)}", sum(p.stat().st_size for p in wheels))
                else:
                    fail("wheels", f"{key}/{py}/{platform}", "pypi", f"exit={proc.returncode} wheels={len(wheels)} see {logf}")


def fetch_playwright_browsers() -> None:
    """Locate chromium revision from a downloaded playwright wheel without executing it."""
    wheels = list((KITS / "projects" / "A04_browser_automation").glob("environments/*/wheelhouse/playwright-*.whl"))
    wheels += list((WIN_KITS / "projects" / "A04_browser_automation").glob("environments/*/wheelhouse/playwright-*.whl"))
    rev = None
    for whl in wheels:
        try:
            with zipfile.ZipFile(whl) as z:
                names = [n for n in z.namelist() if n.endswith("browsers.json") or n.endswith("driver/package/browsers.json")]
                if not names:
                    names = [n for n in z.namelist() if n.endswith("browsers.json")]
                if not names:
                    continue
                data = json.loads(z.read(names[0]))
                for b in data if isinstance(data, list) else data.get("browsers", []):
                    if b.get("name") == "chromium":
                        rev = str(b.get("revision") or b.get("browserVersion") or "")
                        if rev.isdigit():
                            break
                if rev and rev.isdigit():
                    break
        except Exception as e:
            log(f"playwright wheel parse {whl}: {e}")
    if not rev:
        # known recent fallback; recorded as unverified revision
        rev = "1181"
        log("playwright revision fallback 1181")
    ver = None
    for whl in wheels:
        try:
            with zipfile.ZipFile(whl) as z:
                names = [n for n in z.namelist() if n.endswith("browsers.json")]
                if not names:
                    continue
                data = json.loads(z.read(names[0]))
                for b in data if isinstance(data, list) else data.get("browsers", []):
                    if b.get("name") == "chromium" and b.get("browserVersion"):
                        ver = str(b["browserVersion"])
                        break
            if ver:
                break
        except Exception:
            pass
    # Playwright 1.64+ Chromium is Chrome for Testing, not chromium-{rev}.zip
    artifacts = []
    if ver:
        artifacts = [
            ("linux", f"https://storage.googleapis.com/chrome-for-testing-public/{ver}/linux64/chrome-linux64.zip",
             KITS / "runtimes" / "linux_x86_64" / "playwright_browsers" / f"chrome-linux64-{ver}.zip"),
            ("linux", f"https://storage.googleapis.com/chrome-for-testing-public/{ver}/linux64/chrome-headless-shell-linux64.zip",
             KITS / "runtimes" / "linux_x86_64" / "playwright_browsers" / f"chrome-headless-shell-linux64-{ver}.zip"),
            ("win", f"https://storage.googleapis.com/chrome-for-testing-public/{ver}/win64/chrome-win64.zip",
             KITS / "runtimes" / "windows_x86_64" / "playwright_browsers" / f"chrome-win64-{ver}.zip"),
            ("win", f"https://storage.googleapis.com/chrome-for-testing-public/{ver}/win64/chrome-headless-shell-win64.zip",
             KITS / "runtimes" / "windows_x86_64" / "playwright_browsers" / f"chrome-headless-shell-win64-{ver}.zip"),
        ]
    ffmpeg = {
        "linux": (f"https://cdn.playwright.dev/dbazure/download/playwright/builds/ffmpeg/1013/ffmpeg-linux.zip",
                  KITS / "runtimes" / "linux_x86_64" / "playwright_browsers" / "ffmpeg-1013-linux.zip"),
        "win": (f"https://cdn.playwright.dev/dbazure/download/playwright/builds/ffmpeg/1013/ffmpeg-win64.zip",
                KITS / "runtimes" / "windows_x86_64" / "playwright_browsers" / "ffmpeg-1013-win64.zip"),
    }
    for plat, url, dest in artifacts:
        ok = download(url, dest, min_bytes=5_000_000, timeout=600, retries=5)
        if ok:
            record("runtime", dest.name, "ok", str(dest), url, f"playwright CFT chromium rev={rev} ver={ver} NOT executed", dest.stat().st_size)
            if plat == "win":
                wdest = WIN_KITS / "runtimes" / "windows_x86_64" / "playwright_browsers" / dest.name
                wdest.parent.mkdir(parents=True, exist_ok=True)
                if not wdest.exists():
                    try:
                        os.link(dest, wdest)
                    except OSError:
                        import shutil
                        shutil.copy2(dest, wdest)
        else:
            fail("runtime", dest.name, url, "playwright CFT chromium")
        note = dest.parent / "REVISION_en.txt"
        note.write_text(
            f"chromium_revision={rev}\nbrowserVersion={ver}\nkind=chrome-for-testing\nretrieved={RETRIEVED}\nexecuted=no\n",
            encoding="utf-8",
        )
    for plat, (url, dest) in ffmpeg.items():
        if download(url, dest, min_bytes=100_000, timeout=180):
            record("runtime", dest.name, "ok", str(dest), url, "playwright ffmpeg NOT executed", dest.stat().st_size)
            if plat == "win":
                wdest = WIN_KITS / "runtimes" / "windows_x86_64" / "playwright_browsers" / dest.name
                wdest.parent.mkdir(parents=True, exist_ok=True)
                if not wdest.exists():
                    try:
                        os.link(dest, wdest)
                    except OSError:
                        import shutil
                        shutil.copy2(dest, wdest)
        else:
            fail("runtime", dest.name, url, "playwright ffmpeg")


def fetch_eval_small() -> None:
    EVALS.mkdir(parents=True, exist_ok=True)
    samples = [
        ("https://raw.githubusercontent.com/gaia-benchmark/GAIA/main/README.md", EVALS / "GAIA_README.md"),
        ("https://raw.githubusercontent.com/princeton-nlp/SWE-bench/main/README.md", EVALS / "SWE_bench_README.md"),
        ("https://raw.githubusercontent.com/THUDM/AgentBench/main/README.md", EVALS / "AgentBench_README.md"),
        ("https://raw.githubusercontent.com/sierra-research/tau-bench/main/README.md", EVALS / "tau_bench_README.md"),
    ]
    for url, dest in samples:
        if download(url, dest, min_bytes=80, timeout=60):
            record("eval_doc", dest.name, "ok", str(dest), url, "readme only; datasets not claimed complete", dest.stat().st_size)
        else:
            fail("eval_doc", dest.name, url, "readme")


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("stage", nargs="?", default="all",
                   choices=["all", "papers", "sources", "docs", "runtimes", "models", "wheels", "browsers", "eval"])
    args = p.parse_args()
    LOG.mkdir(parents=True, exist_ok=True)
    stage = args.stage
    if stage in ("all", "papers"):
        fetch_papers()
    if stage in ("all", "sources"):
        fetch_sources()
    if stage in ("all", "docs"):
        fetch_docs()
    if stage in ("all", "eval"):
        fetch_eval_small()
    if stage in ("all", "runtimes"):
        fetch_llama_cpp()
        fetch_nodejs()
    if stage in ("all", "models"):
        fetch_models()
    if stage in ("all", "wheels"):
        fetch_wheels()
    if stage in ("all", "browsers"):
        fetch_playwright_browsers()
    log(f"done stage={stage}")


if __name__ == "__main__":
    main()
