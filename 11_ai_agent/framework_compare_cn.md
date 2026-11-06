# 框架对照（钉死版本，2026-10-30）

对照依据：官方文档镜像、源码 tarball 与 PyPI 元数据。本轮**没有**import 或跑通示例。

## 总表

| | LangGraph 1.2.18 | AG2 1.2.2 | CrewAI 1.15.33 | OpenAI Agents SDK 0.24.0 |
|---|---|---|---|---|
| 定位 | 有向图状态机 + checkpoint | 对话式多智能体（AutoGen 后继） | 角色/任务/Crew 编排 | 轻量 Agent + 工具 + 交接 |
| 许可证 | MIT | 见仓库（含 CC-BY-4.0 文档与 Apache 代码，以 tarball 内文件为准） | MIT | MIT |
| Python | ≥3.10 | ≥3.10（随依赖变） | ≥3.10,<3.14 | ≥3.10 |
| 状态 | 图、channel、thread、interrupt | agent chat、tool timeout | Flow / Crew / memory 后端 | RunState、handoff、MCP 注解 |
| 本地模型 | 经 LangChain 聊天模型或 OpenAI 兼容 | `base_url` + OpenAI 3.x 客户端 | 官方仍偏云厂商；可用 OpenAI 兼容但客户端是 **openai 2.x** | 文档写明 provider-agnostic，`base_url` 即可 |
| MCP | extra / 生态 | 有 MCP 事件相关改动 | 依赖 `mcp` 包 | 0.24.0 暴露 MCP annotations |
| 追踪 | LangSmith 云（未打包） | 自有 telemetry 选项 | OpenTelemetry 依赖在树中 | 内置 tracing，可关 |
| 与本套件项目 | A02 主框架 | A05 独立 wheelhouse | A05 另一独立 wheelhouse | A01/A03/A04 |

## 不能混装的依赖

CrewAI 1.15.33 声明 `openai>=2.30,<3`。  
OpenAI Agents SDK 0.24.0 与 AG2 1.2.2 需要 `openai` 3.x。  
所以 **CrewAI 必须单独 venv**。这不是风格问题，是解析冲突。

历史 `microsoft/autogen` v0.2.37 仅作文献对照，新项目不要拿它当默认。

## 工程能力对照（文档层面，未实测）

| 能力 | LangGraph | AG2 | CrewAI | Agents SDK |
|---|---|---|---|---|
| 超时 | 图节点/ retry 策略需自配 | 1.2.2 起工具 `timeout=` | 任务级超时配置（见发行说明） | Runner 超时 |
| 重试 | 有 retry 政策节点 | 客户端重试 + 工具错回模型 | 失败策略字段 | 工具异常格式化（0.24） |
| 持久化 | checkpoint SQLite/Postgres | 需自接 | Flow 状态 / 存储后端 | session / RunState |
| 人工介入 | `interrupt` | human-in-the-loop 模式 | 发行说明含 human feedback | approvals（0.24 修了 pending approval） |
| 多 Agent 交接 | 子图 / supervisor 自搭 | 群聊、发言权 | 角色与委派 | handoff |
| 成本 | 自计 token | token 统计在 1.2.2 加强 | eval 可记成本时间 | 用量对象 |

## 其他纳入但不作为五个项目主框架的库

| 库 | 版本意图 | 用途 |
|---|---|---|
| smolagents | 探测最新 tag | 少依赖的工具调用对照 |
| MCP Python SDK | 探测 tag | 协议实现，不是 Agent 运行时 |
| aider-chat 0.86.2 | PyPI | A03 编码 Agent 代表；可接本地接口 |
| browser-use 0.13.14 | PyPI | A04 的 3.12 附加；**3.10 不支持** |
| llama.cpp b11998 | 二进制 | 本地推理后端，不是 Agent 框架 |

## 选型建议（仍须实测）

- 要**可恢复的工作流** → LangGraph。  
- 要**角色说明书式协作** → CrewAI（独立环境）。  
- 要**少抽象、贴近 OpenAI 工具协议** → Agents SDK。  
- 要从 AutoGen 论文复现对话模式 → AG2，不要旧 `autogen` 0.2。
