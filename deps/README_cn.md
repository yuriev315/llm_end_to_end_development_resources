# Windows 最小运行环境（deps/）

本目录是 AI Agent 专题五个项目和八个参考框架在 **Windows x64** 上的最小离线运行环境：Python 安装包、按 Windows 平台标记解析的 wheel、llama.cpp 运行时和一个嵌入模型。

## 内容

| 路径 | 内容 |
|---|---|
| `runtimes/python/` | CPython 3.10.11 与 3.12.10 官方 64 位安装包（附官方 `.sigstore` 签名包） |
| `runtimes/llama_cpp/` | llama.cpp b11998 Windows CPU 包与 Vulkan 包 |
| `models/embeddings/bge-small-en-v1.5-q8_0.gguf` | 嵌入模型（MIT，35 MiB），可直接给 `llama-server --embedding` 用 |
| `wheels/<环境>/` | 每个环境一套完整 wheel（含 Windows 专用依赖，如 colorama、pywin32） |
| `locks/<环境>.lock.txt` | 带 SHA-256 的锁文件（`pip install --require-hashes` 可用） |
| `locks/<环境>.requirements_direct.txt` | 该环境的直接依赖 |
| `windows/install_python.bat` | 按环境名建 venv 并离线安装 |
| `windows/pins/<环境>.txt` | 安装用的版本清单 |
| `manifests/minimum_runtime_dependencies.csv` | 每个环境的每个包与版本 |

## 环境

| 环境 | Python | 用途 | 包数 | wheel 大小 |
|---|---|---|--:|--:|
| `A01` | 3.10 | 工具调用与多步任务 | 43 | 19.6 MiB |
| `A02` | 3.10 | 本地文档 RAG | 63 | 30.4 MiB |
| `A02_hf` | 3.10 | RAG 的 Hugging Face 嵌入后端（可选；torch 为 .url 占位） | 44 | 109.2 MiB |
| `A03` | 3.10 | 沙箱文件 Agent | 41 | 19.4 MiB |
| `A03_aider` | 3.10 | aider-chat 0.86.2 | 111 | 112.9 MiB |
| `A04` | 3.10 | Playwright（Python 3.10） | 44 | 56.8 MiB |
| `A04_browser_use` | 3.12 | browser-use 0.13.14（Python 3.12） | 111 | 94.6 MiB |
| `A05_ag2` | 3.10 | AG2 1.2.2 | 22 | 7.3 MiB |
| `A05_crewai` | 3.10 | CrewAI 1.15.33（按 Windows 标记重新解析，pydantic 与 pydantic-core 版本配套） | 147 | 240.5 MiB |
| `REF_inspect_ai` | 3.12 | Inspect AI 0.3.286（要求 Python ≥3.11） | 80 | 77.5 MiB |
| `REF_agentdojo` | 3.10 | AgentDojo 0.1.15 | 95 | 55.5 MiB |
| `REF_smolagents` | 3.10 | smolagents 1.22.0 | 31 | 15.2 MiB |
| `REF_autogen` | 3.10 | AutoGen 0.2.37（autogen-agentchat） | 30 | 30.1 MiB |
| `REF_swebench` | 3.10 | SWE-bench 2.1.0 工具包（评测需 Docker） | 69 | 75.7 MiB |
| `REF_tau_bench` | 3.10 | tau-bench 依赖（源码包在 11_ai_agent/implementations/） | 93 | 113.7 MiB |
| `REF_agentbench` | 3.10 | AgentBench 客户端依赖（任务环境需 Docker） | 78 | 48.9 MiB |
| `REF_mcp_sdk` | 3.10 | MCP Python SDK 1.16.0（pydantic<2.13） | 27 | 10.6 MiB |

- 以 CPython 3.10 为主；`A04_browser_use` 与 `REF_inspect_ai` 的上游要求 Python ≥ 3.11，用 3.12。
- 环境之间有版本冲突（例如 CrewAI 需要 `openai` 2.x，Agents SDK 与 AG2 需要 3.x），必须分开建 venv。
- `windows/agent_runtime_kits/.../wheelhouse/` 里是各项目自带的 wheelhouse；本目录的 wheel 另按 Windows 平台标记解析，补齐了 Windows 专用依赖，安装时优先用本目录。
- `A02_hf` 需要的 torch 2.14.1+cpu（118 MiB）超过 100 MiB，只有 `.url` 占位。先按占位文件里的地址下载到 `wheels\A02_hf\`，核对 SHA-256 后再安装。

## 安装

在包根目录（同时含 `deps\` 和 `windows\` 的目录）执行：

```bat
deps\runtimes\python\python-3.10.11-amd64.exe /quiet PrependPath=1 Include_launcher=1
deps\runtimes\python\python-3.12.10-amd64.exe /quiet Include_launcher=1
deps\windows\install_python.bat A01
set PYTHONUTF8=1
venvs\A01\Scripts\python agent_runtime_kits\projects\A01_tool_multistep\src\agent_loop.py --mode mock
```

A02 真实嵌入：先解压 `deps\runtimes\llama_cpp\llama-b11998-bin-win-cpu-x64.zip`，再运行

```bat
llama-server -m deps\models\embeddings\bge-small-en-v1.5-q8_0.gguf --embedding --pooling mean --port 8080
```

生成模型（Qwen2.5 GGUF）不随包分发，地址在 `agent_runtime_kits/models/`。

## 核对情况

- 每个锁文件都用 `pip install --dry-run --no-index --require-hashes` 对本目录的 wheel 做过离线核对，全部通过。
- **没有在真实 Windows 上运行过**；`install_python.bat` 也没有在 Windows 上执行过。
- 云 API、真实大模型、GPU、Docker（SWE-bench、AgentBench）相关路径没有实测。
