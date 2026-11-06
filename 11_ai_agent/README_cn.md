# AI Agent 独立专题

目录：`ai_agent/11_ai_agent/`。检索日 **2026-10-30**。这是离线资料库的**独立专题**，不是 `04_data_ai` 的子节，也不是 Hugging Face / LangChain wheel 的附赠说明。

本轮只下载与整理：**不安装** Python 包、**不启动** llama-server、**不跑** Agent、**不断网实测**。源码或 wheel 已落地 ≠ 可完全离线运行。

配套运行套件见 [`ai_agent/agent_runtime_kits/README_cn.md`](../agent_runtime_kits/README_cn.md)。

## 覆盖范围

| 子目录 | 内容 |
|---|---|
| [`theory/`](theory/) | 机制导读：工具调用、结构化输出、规划、记忆、反思、状态、工作流 |
| [`methods/`](methods/) | 方法说明：假设、适用、参数、局限 |
| [`implementations/`](implementations/) | 钉死版本的框架与评测仓库源码包 |
| [`docs_html/`](docs_html/) | 官方文档的有限额镜像 |
| [`experiments/`](experiments/) | 评测仓库说明；完整基准数据大多未下 |
| [`learning_path_cn.md`](learning_path_cn.md) | 中文学习路线 |
| [`paper_guides_cn.md`](paper_guides_cn.md) | 论文导读 |
| [`framework_compare_cn.md`](framework_compare_cn.md) | 框架对照 |
| [`licenses_cn.md`](licenses_cn.md) | 许可 |
| [`missing_cn.md`](missing_cn.md) | 缺失项 |

论文 PDF 在 [`../_public/papers/agent/`](../_public/papers/agent/)。清单以 `../inventories/agent_downloads_cn.csv` 为准，失败见 `agent_download_failures_cn.csv`。

## 钉死版本（检索日当时的维护状态）

| 组件 | 版本 | 依据 | 备注 |
|---|---|---|---|
| LangGraph | 1.2.18（2026-10-26） | GitHub / 已有 env 15 wheel | 与 `15_nlp_retrieval` 对齐，但 Agent 项目仍独立解析依赖 |
| AG2（AutoGen 后继） | v1.2.2（2026-10-27） | GitHub | 原 `microsoft/autogen` 已归档，另存历史 0.2.37 |
| CrewAI | 1.15.33（PyPI 2026-10-28） | PyPI | GitHub 标签可能滞后到 1.15.32，以实际 tarball 为准 |
| OpenAI Agents SDK | v0.24.0（2026-10-15） | GitHub | MIT；可接任意 OpenAI 兼容接口 |
| MCP 规范 | 2026-07-28 | 官方 GitHub Release | 无会话握手的新修订 |
| llama.cpp | b11998（2026-10-30，滚动发布） | GitHub | 当日预发布；CPU 必下，Vulkan/CUDA 作可选 GPU |
| Node.js | v22.23.4 | nodejs.org Maintenance LTS | 浏览器工具链备用 |
| aider-chat | 0.86.2 | PyPI | `<3.13,>=3.10` |
| browser-use | 0.13.14 | PyPI | **Python ≥ 3.11**，3.10 不强装 |

## 与原环境的关系

`environments/09_huggingface_llm_*` 与 `15_nlp_retrieval_*` **不能**自动满足本专题项目：缺少 Agents SDK / CrewAI / AG2 / Playwright / 本地推理后端，且 CrewAI 与 Agents SDK 的 `openai` 主版本冲突。每个代表项目都有自己的 wheelhouse。**模型权重只记官方地址，不随库分发。**
