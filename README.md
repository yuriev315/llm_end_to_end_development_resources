# AI Agent resources

An offline library for learning and building LLM agents: Chinese study guides, papers, official framework
documentation, pinned source snapshots, five runnable example projects and their offline Python wheels for
Linux and Windows, local inference runtimes, and a Windows minimum runtime.

This folder is distributed as the Release `ai-agent-20261106` of this repository. The Git tag holds the
small files (guides, project code, lock files, inventories, `.url` placeholders); the Release tars hold everything.
Download and extraction steps: [`download_restore_cn.md`](download_restore_cn.md). Offline start page: `index_cn.html`.

## Contents

| Path | What it is |
|---|---|
| `11_ai_agent/` | Chinese guides: learning path, paper guides, framework comparison, mechanisms, engineering/evaluation/safety, applications, licences, gaps |
| `11_ai_agent/docs_html/` | Offline mirrors of 6 official doc sites: OpenAI Agents SDK, LangGraph, AG2, CrewAI 1.15.33, MCP, Aider (plus `llms-full.txt` exports where the site provides them) |
| `11_ai_agent/implementations/` | 14 pinned source snapshots (LangGraph, AG2, AutoGen 0.2, OpenAI Agents SDK, MCP spec and Python SDK, smolagents, Aider, browser-use, SWE-bench, AgentBench, tau-bench, AgentDojo, Inspect AI); CrewAI source (191 MiB) is a `.url` |
| `11_ai_agent/experiments/` | Benchmark READMEs (SWE-bench, AgentBench, tau-bench); GAIA is gated, URL only |
| `_public/papers/agent/` | 54 papers: 29 PDFs under CC BY / CC BY-SA / CC0, 25 as `.url` (arXiv default licence or NC) |
| `agent_runtime_kits/` | Five projects (A01 tool use, A02 local RAG, A03 coding/files, A04 browser, A05 multi-agent), Linux wheelhouses for Python 3.10 and 3.12 (1063 wheels), llama.cpp b11998, Node.js v22.23.4, model tokenizers/configs and weight URLs |
| `windows/agent_runtime_kits/` | Windows x64 wheelhouses for the same projects (1062 wheels) |
| `deps/` | Windows minimum runtime: Python 3.10.11/3.12.10 installers, 1128 wheels for 17 environments resolved with Windows markers, llama.cpp CPU/Vulkan, a GGUF embedding model, `install_python.bat` |
| `inventories/` | Download records with sizes and sources |
| `scripts/` | The download scripts used to build the project wheelhouses |
| `url_placeholders_cn.csv` | Every `.url` placeholder with URL, size, SHA-256, licence and reason |

## Rules applied

- Files over 100 MiB and files without a redistribution licence are not included. Each has a `.url` file with
  the same name (Windows Internet Shortcut plus size, SHA-256, licence and reason): 41 in total,
  27 for licence reasons and 14 for size.
- Model weights (GGUF, safetensors) are URL-only by design; tokenizers and configs are included.
- Every wheel matches the SHA-256 recorded in its environment's `wheel_inventory_cn.csv`.

## What has been checked

- Every Linux wheelhouse was installed offline into a fresh CPython 3.10 / 3.12 venv, the main framework was
  imported, and each project's mock path was run: all pass (`inventories/runtime_test_results_cn.csv`). The optional
  Hugging Face backend was installed without torch (torch is a `.url`). Mock runs only exercise the loop, not a real model.
- Some original wheelhouses lacked conditional dependencies (`python_version < "3.11"` backports, Windows-only
  `colorama`/`pywin32`); these wheels were added and are listed in each environment's `wheel_additions_cn.csv`.
- The Windows CrewAI wheelhouses under `windows/` pair pydantic 2.12.5 with pydantic-core 2.50.2 and do not resolve;
  use `deps/wheels/A05_crewai` instead (see `KNOWN_ISSUE_cn.txt`).
- All 17 Windows minimum-runtime locks pass `pip install --dry-run --no-index --require-hashes` with
  `--platform win_amd64`.
- Nothing has been run on a real Windows machine, on a GPU, or against a cloud API.

Licences: each third-party file keeps its own licence (see `11_ai_agent/licenses_cn.md` and the placeholder list).
