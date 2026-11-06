# Agent 本地运行套件

检索日 **2026-10-30**。与论文专题同步准备。每个代表项目**独立解析依赖**，不复用 `09_huggingface_llm` / `15_nlp_retrieval` 的 venv 声明。

本轮：**下载与配置**。未安装、未执行、未断网验证。

## 五个代表项目

| ID | 覆盖 | 主代码 | 主框架 wheel | 3.10 | 3.12 |
|---|---|---|---|---|---|
| A01 | 工具调用与多步任务 | [`projects/A01_tool_multistep`](projects/A01_tool_multistep/) | openai-agents 0.24.0 | 是 | 是 |
| A02 | 本地文档 RAG | [`projects/A02_local_doc_rag`](projects/A02_local_doc_rag/) | LangGraph 1.2.18 + LangChain 1.4.7 | 是 | 是 |
| A03 | 编码与文件操作 | [`projects/A03_coding_files`](projects/A03_coding_files/) | aider-chat 0.86.2 + Agents SDK | 是 | 是 |
| A04 | 浏览器自动化 | [`projects/A04_browser_automation`](projects/A04_browser_automation/) | Playwright；browser-use 仅 3.12 | **无 browser-use** | 是 |
| A05 | 多 Agent 协作 | [`projects/A05_multi_agent`](projects/A05_multi_agent/) | AG2 与 CrewAI **两个 wheelhouse** | 是 | 是 |

Windows 对应 wheel 在 `ai_agent/windows/agent_runtime_kits/projects/*/environments/`。

## 运行时与模型（共享归档）

| 路径 | 内容 |
|---|---|
| [`runtimes/linux_x86_64/llama_cpp/`](runtimes/linux_x86_64/llama_cpp/) | llama.cpp CPU 官方包 |
| [`runtimes/linux_x86_64/llama_cpp_gpu/`](runtimes/linux_x86_64/llama_cpp_gpu/) | Vulkan/CUDA 可选 |
| [`runtimes/windows_x86_64/`](runtimes/windows_x86_64/) | 同名 Windows 包（亦硬链接到 Windows 库） |
| `runtimes/*/nodejs/` | Node.js v22.23.4 官方包 |
| `runtimes/*/playwright_browsers/` | Playwright 1.64 Chromium = Chrome for Testing 156.0.8078.4 zip（未执行） |
| [`models/cpu_baseline/`](models/cpu_baseline/) | Qwen2.5 0.5B/1.5B/3B Q4_K_M **地址文件**（不存 GGUF） |
| [`models/gpu_optional/`](models/gpu_optional/) | Qwen2.5 7B Q4_K_M **分片地址**（不存 GGUF） |
| [`models/embeddings/`](models/embeddings/) | bge-small-en/zh 与可选 GGUF 的 **地址**；保留 tokenizer/config |
| [`models/rerankers/`](models/rerankers/) | bge-reranker-base **权重地址**；保留 tokenizer/config |
| [`models/tokenizers/`](models/tokenizers/) | Qwen 分词器与模板（不是权重） |

## 模型分档（工具调用未验证）

| 档 | 模型 | 许可 | 硬件（估计，未测） | 工具调用 |
|---|---|---|---|---|
| CPU 冒烟 | Qwen2.5-0.5B Q4_K_M | Apache-2.0 | RAM 1–2 GiB | 预期经常失败 |
| CPU 基线 | Qwen2.5-1.5B Q4_K_M | Apache-2.0 | RAM 3–4 GiB | 未验证 |
| CPU 增强 | Qwen2.5-3B Q4_K_M | Apache-2.0 | RAM 5–8 GiB | 未验证 |
| GPU 可选 | Qwen2.5-7B Q4_K_M | Apache-2.0 | 建议 VRAM ≥ 8 GiB 或 RAM ≥ 12 GiB | 未验证；不能当保证 |
| 嵌入 | bge-small-en/zh | MIT | CPU | 嵌入 ≠ 生成工具调用 |
| 重排 | bge-reranker-base | MIT | CPU 慢 | 需 optional torch 环境才方便加载 safetensors |

OpenAI 兼容接口可连上，**不能**据此认定模型会工具调用。

## 状态标签约定（每个项目 README 重复）

四选多，必须据实：

1. **云 API 必需** — 该路径没有本地后端配置或上游只接云。  
2. **可连接本地模型** — 已提供 `base_url` 模板与 llama.cpp 后端；GGUF **需按 `models/*.url.txt` 自行获取**。  
3. **离线资源已备齐** — 该项目声明的代码、wheel、浏览器已落盘（以 inventories 为准）。**模型权重按约定只记地址，不算已备齐权重。**  
4. **已断网运行验证** — 本轮 **一律不使用**。

mock 路径用于学习循环结构，不使用模型，也不得标第 4 项。

## 增量包切分

1. 文档 + 源码 + 项目代码 + Linux wheel  
2. 模型权重地址清单（不打包 GGUF/safetensors）  
3. 可选 GPU 权重 + GPU 版 llama.cpp  
4. Linux 运行时（llama CPU、Node、浏览器）  
5. Windows wheel + Windows 运行时  

原 01–33 Release 不动。许可不允许公开的不进公开 tar。
