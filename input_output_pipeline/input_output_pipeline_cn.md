# 输入输出处理链：各环节职责与参考实现

> 状态说明：本文件是本轮整理的设计参考。表中“参考实现”均为已下载的上游源码快照（版本见 `project_readiness_cn.csv`），**全部只做了静态核对（最高 L1），没有运行任何上游代码**。标注【本库建议】的内容是本轮自行整理的建议，不是上游已有功能，也没有经过验证。

处理链：**用户输入前处理 → 指令与上下文组织 → 模型生成 → 输出后处理 → 工具或业务执行 → 记录、反馈与回归**

逐项检查与证据见 `validation_matrix_cn.csv`；训练对齐与运行时控制的区别见 `alignment_vs_runtime_controls_cn.md`。

## 0. 贯穿全链的三条规则

1. **原始输入不可丢失**【本库建议】：每个请求保存 `raw_input`（原文及附件哈希）、`processed_input`（规范化/脱敏后文本）以及 `transform_log`（规则名称、版本、改动位置、是否可逆）。凡是会改变用户原意的改写（摘要、翻译、意图改写）都不算“清洗”，必须单独记录为“改写”，并保留原文供模型或人工对照。
2. **只有系统通道能授予指令权限**：检索文档、用户上传的文件、网页、工具返回内容一律是**数据**，不获得系统/开发者指令权限。可参考：OpenAI Model Spec（P1215，指令层级：平台 > 开发者 > 用户 > 工具/内容）、CaMeL（P1210，控制流与数据流分离的研究实现）、NeMo Guardrails 的检索 rails 与执行 rails（P1204）。
3. **四类“通过”分开记录**：格式正确 ≠ 规则通过 ≠ 有证据支持 ≠ 事实正确。模型自检（让同一模型判断自己的输出）不能替代独立验证；见论文 2310.01798 与 2406.01297（papers_books_courses/papers/12/）。

## 1. 用户输入前处理

| 子环节 | 责任方 | 输出 | 参考实现（编号） | 失败时 |
|---|---|---|---|---|
| 请求结构、字段类型、长度、编码、文件格式校验 | 平台网关 | 结构化请求对象或拒绝码 | Pydantic（P1218）、jsonschema（P1219）；网关限额：LiteLLM（P1003，`litellm/proxy/hooks`） | 返回明确错误码，不进入模型 |
| 文本规范化、语言识别 | 平台 | `processed_input` + 语言标签 | lingua-py（P1203，实现在 Rust crate lingua-rs，快照中未包含） | 记录置信度，低于阈值时标为“未知语言” |
| OCR 与文档解析 | 平台 | 带页码/坐标的结构化文档 | Docling（P0202）、MinerU（P0208）、RAGFlow deepdoc（P0702） | 解析失败的页列入报告，不静默丢弃 |
| 隐私与敏感信息识别、脱敏、凭据保护 | 平台 + 安全 | 脱敏文本 + 加密的可逆映射（如需要） | Presidio（P1201）、detect-secrets（P1202） | 命中凭据时阻断，并提示用户撤销已泄露的凭据 |
| 内容分类、业务范围判断、风险分级 | 业务 + 安全 | 风险等级（低/中/高/拒绝） | Llama Guard / Prompt Guard（P1206，权重需申请）、WildGuard（P1227）、NeMo Guardrails 输入 rails（P1204） | 高风险转人工或拒绝；误报样本进入回归集 |
| 意图、任务类型识别与模型/工具路由 | 业务 | 路由决策 + 理由 | semantic-router（P1209）、RouteLLM（P1208，研究原型） | 低置信度时走澄清或默认路由 |
| 歧义识别、澄清、多轮指代 | 业务 + 模型 | 澄清问题或补全后的请求 | 无专门开源组件；LangGraph 人工中断（P0806 `libs/langgraph/langgraph/types.py`）可实现“暂停—澄清—继续” | 【本库建议】澄清最多 1–2 轮，超过即转人工 |
| 提示注入、越权请求、不可信附件 | 安全 | 风险标签；附件以“数据”身份封装 | Prompt Guard / LlamaFirewall（P1206）、NeMo Guardrails（P1204）、CaMeL（P1210） | 检测器只能降低风险，必须配合第 2 节的权限边界 |
| 用户、租户、角色、资源权限 | 平台 | 允许访问的资源集合 | OpenFGA（P1214）、Open WebUI 访问控制（P0903 `backend/open_webui/utils/access_control`）、LibreChat 中间件（P0901 `api/server/middleware`） | 默认拒绝 |

记录要求【本库建议】：`request_id`、`tenant_id`、`user_id`、`raw_input_ref`、`processed_input`、`transform_log[]`、`risk_level`、`route`，并写入追踪系统（Langfuse P1004 或 OpenTelemetry，文档 D19）。

## 2. 指令与上下文组织（请求时）

| 子环节 | 做法 | 参考 |
|---|---|---|
| 系统/开发者/用户指令组织与冲突处理 | 分层放置，冲突时以更高层级为准，并在日志中记录冲突 | P1215 Model Spec；论文 2404.13208（Instruction Hierarchy） |
| 提示模板 | 模板带版本号，与模型版本、适配器版本一起记录 | Langfuse 提示管理（P1004）；promptfoo 回归（P0504） |
| 上下文预算与历史压缩 | 固定预算：系统 > 当前请求 > 检索证据 > 历史摘要；压缩结果可回溯 | LLMLingua（P1216）、OpenHands SDK context（P0811 `openhands-sdk/openhands/sdk/context`） |
| 检索内容与工具结果的可信边界 | 以明确分隔符和“数据”角色注入，不拼接进系统指令 | 论文 2403.14720（Spotlighting）、2402.06363（StruQ）、2410.05451（SecAlign） |
| 工具定义与结构化输出约束 | 工具参数用 JSON Schema 描述，生成端用约束解码 | MCP 规范（D26/D0801）、MCP Python SDK（P0801）；xgrammar（P0605）、Outlines（P0604）、vLLM 结构化输出（P0601 `docs/features/structured_outputs.md`） |

## 3. 模型生成

- 服务端：vLLM（P0601）、SGLang（P0603）、llama.cpp（P0602）。流式输出为 SSE，工具调用解析器在 `vllm/tool_parsers`。
- 停止条件、最大长度、超时由调用方显式设置；客户端取消须传到服务端（vLLM 支持中止请求，端到端行为需自测，未验证）。

## 4. 输出后处理

| 子环节 | 检查层级 | 参考实现 |
|---|---|---|
| 流式解析、停止、截断、中断 | 格式正确 | vLLM `vllm/entrypoints/openai/api_server.py` 与 `tests/entrypoints` |
| JSON/Schema/字段类型/业务约束 | 格式正确 → 规则通过 | instructor（P1217，校验失败重问）、Guardrails AI（P1205）、jsonschema（P1219） |
| 工具调用名称、参数、权限、执行前校验 | 权限正确 | MCP SDK（P0801）、OpenHands SDK security（P0811 `openhands-sdk/openhands/sdk/security`）；评测 BFCL（P1228） |
| 引用来源、检索证据、事实支持 | 有证据支持 | Ragas（P0703）、FActScore（P1220）；论文 2305.14627（ALCE） |
| 事实正确性 | 事实正确 | 只能依赖独立来源与人工抽检；FActScore 需外部知识源 |
| 敏感信息泄露、内容风险、越权内容 | 安全评测 | Presidio（P1201）、garak（P1212）、PyRIT（P1213） |
| 医疗/机械/Coding 领域校验 | 规则通过 | 医疗：pint（P1108）、MedCalc-Bench 计算器（P1105）、medspaCy（P1106）；机械：pint、CadQuery 几何重建（P1109）；Coding：SWE-bench harness（P0505）、Ruff（P0808） |
| Markdown/HTML/链接/文件安全呈现 | 规则通过 | DOMPurify（P1221，前端）、nh3（P1222，Python 端）；OWASP Cheat Sheet（D39） |
| 格式修复、有限重试、模型回退、人工审核 | 规则通过 | LiteLLM 回退（P1003 `litellm/router.py`）、LangGraph 中断审批（P0806）、Argilla 审核（P0204） |
| 输出、文件、工具结果关联记录 | 审计 | Langfuse trace/observation（P1004） |

【本库建议】每次输出保存 `checks = {format_ok, rules_ok, evidence_supported, fact_checked_by, human_reviewed_by}`，各字段独立取值，禁止用一个“通过”布尔值代替。

## 5. 工具或业务执行与闭环

1. **建议与执行分离**：模型只产出“执行计划/工具调用请求”，由执行器在权限检查后执行。参考 OpenHands SDK 的确认策略与安全分析（P0811），SWE-agent 的工具接口（P0805）。
2. **隔离与资源限制**：Docker/远程工作区（P0811 `openhands-workspace/.../docker`、`remote_api`）、SWE-bench 容器（P0505）；更强隔离参考 gVisor 文档（D41）。超时、CPU/内存/网络限制由部署方配置。
3. **高影响操作确认、幂等、重试与恢复**：Temporal（P1008，活动重试与超时、工作流可恢复）、tenacity（P1006）、LangGraph 检查点（P0806 `libs/checkpoint`）。幂等键属于业务设计。
4. **结果检查后再反馈模型**：工具结果先做格式与安全检查、截断，再以“数据”身份回传。
5. **日志、审计、反馈与回归**：Langfuse（P1004）记录 trace、评分、数据集；promptfoo（P0504）把失败样本固化为回归用例。

## 6. 端到端评测（本库已收录的公开测试集与方法）

| 关注点 | 已收录 | 缺口 |
|---|---|---|
| 意图识别与任务完成率 | τ-bench（论文 2406.12045）、AppWorld（论文 2407.18901）、inspect_ai 自定义任务（P0502） | 业务意图集需自建 |
| 过滤误报/漏报及多语言差异 | XSTest（P1229）、OR-Bench（论文 2405.20947）、WildGuard（P1227）、HarmBench（P1225） | 中文及其他语言的误报评测缺失 |
| 提示注入与权限绕过 | AgentDojo（P1211）、BIPIA（P1223，上游已归档）、InjecAgent（P1224）、garak（P1212）、PyRIT（P1213） | 多租户越权端到端用例需自建 |
| 输出结构、引用、工具参数 | BFCL（P1228）、Ragas（P0703）、JSONSchemaBench（论文 2501.10868） | — |
| 流式与非流式差异 | vLLM tests/entrypoints（单元级） | 端到端对比测试缺失 |
| 重试、回退的延迟与成本 | GuideLLM（P0607）、LiteLLM 成本记录（P1003） | 成本—质量联合评测需自建 |
| 规则/提示/模型/知识库更新后的回归 | promptfoo（P0504）、lm-eval（P0501）、Langfuse 数据集（P1004） | 版本关联（数据—模型—提示—知识库）需组合 DVC/MLflow/Langfuse，无一体化参考 |

## 7. 下一步最小验证（未执行）

在无网络隔离容器中（CPU 即可）：
1. `presidio-analyzer` 单元测试与 `detect-secrets` 测试：验证 PII/凭据规则（需下载 spaCy 模型，需联网一次）。
2. `jsonschema`、`instructor` 测试（instructor 的 LLM 相关测试需替换为本地 mock）。
3. `nh3` 与 DOMPurify 测试：验证 HTML 净化。
4. AgentDojo 自带的确定性环境（不调用外部模型时只能跑框架自检）。
通过后才能把对应项目提升为 L2，并在 `project_readiness_cn.csv` 记录环境与命令输出。
