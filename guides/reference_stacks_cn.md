# 四条开发路线的参考组合（reference stacks）

> **阅读前须知**
> - 本文件基于本轮下载的上游源码快照做的**静态核对**。所有项目最高为 L1，没有运行、安装、训练或部署过任何上游代码。
> - “文档支持”表示使用方快照的代码或文档中确实提到被依赖方（证据文件见 `compatibility_matrix_cn.csv`），**不等于本轮验证过可以组合**。“待验证建议”是本轮整理的建议。
> - 来自不同仓库的组件，未经运行验证前都不能称为“可直接拼接”。
> - 每个环节的验收条件、入口文件和缺口见 `end_to_end_coverage_cn.csv`，补齐顺序见 `gap_backlog_cn.csv`。
> - 版本号均为本库快照版本（编号后括号内）。

---

## 路线 1：通用对话助手

### 1.1 建议组合

| 环节 | 首选（版本） | 备选 / 补充 |
|---|---|---|
| 模型接入/自托管 | vLLM（P0601 v0.32.0）提供 OpenAI 兼容 API；LiteLLM 网关（P1003 v1.106.6） | llama.cpp server（P0602 b11986，CPU 可用）；接口规范 D0601 |
| 输入处理 | Presidio（P1201 2.2.366）+ detect-secrets（P1202 v1.5.0）+ NeMo Guardrails（P1204 v0.24.1） | Llama Guard/Prompt Guard（P1206，权重需申请）、semantic-router（P1209） |
| 上下文与记忆 | mem0（P0809 v2.2.1，作用域 user_id/agent_id/run_id）+ Qdrant（P0705 v1.20.0） | LangGraph 检查点（P0806 1.2.18）、LLMLingua（P1216） |
| 生成 | vLLM，结构化输出后端 xgrammar（P0605 v0.2.8） | SGLang（P0603） |
| 输出处理 | instructor（P1217）/ jsonschema（P1219）+ nh3（P1222）或 DOMPurify（P1221） | Guardrails AI（P1205） |
| 前后端 | LibreChat（P0901 v0.8.8） | chat-ui（P0902）、Open WebUI（P0903，非标准开源许可） |
| 认证与隔离 | LibreChat 自带认证与中间件；网关层 LiteLLM 密钥/预算/限速 | OpenFGA（P1214）做资源级授权 |
| 部署 | Docker Compose（LibreChat `docker-compose.yml` / `deploy-compose.yml`）；GPU 侧 production-stack Helm（P1001） | KServe（P1002） |
| 监控与反馈 | Langfuse（P1004 v4.72.0） | Prometheus/OpenTelemetry 文档（D18/D19）、production-stack `observability/` |

### 1.2 模块接口（输入 → 输出）

```
浏览器 ──HTTPS──> LibreChat API（会话存 MongoDB）
   └─[本库建议] 输入处理服务：Presidio / detect-secrets / Guardrails 输入 rails
        └─ OpenAI Chat Completions 请求 ──> LiteLLM 网关（密钥、预算、回退、日志回调）
              └─ OpenAI 兼容 HTTP ──> vLLM（模型权重、xgrammar 结构化输出、tool_parsers）
        <─ 流式 SSE / JSON
   └─[本库建议] 输出处理：Schema 校验 → 风险检测 → nh3/DOMPurify 净化 → 渲染
追踪：LiteLLM 回调 → Langfuse（trace、score、dataset）
```

### 1.3 环境、配置与启动顺序（未执行）

1. 准备：Docker 与 Compose；GPU 节点（vLLM）；模型权重（按模型卡许可自行获取，本库未下载）。
2. 配置文件（均只保留占位符，切勿写入真实凭据）：LibreChat `.env.example` → `.env`，`librechat.example.yaml` → `librechat.yaml`（custom endpoints 指向 LiteLLM）；LiteLLM `litellm/proxy/proxy_config.yaml` 的 model_list 指向 vLLM 地址；Langfuse `docker-compose.yml` 中的密钥占位。
3. 启动顺序：Langfuse 依赖服务 → Langfuse → vLLM → LiteLLM → 输入/输出处理服务 → LibreChat。
4. 先只做配置校验：`docker compose -f <file> config`；`helm template`（production-stack）。

### 1.4 测试与部署步骤

- 单元：Presidio `presidio-analyzer/tests`、jsonschema、nh3 测试；LibreChat `e2e/`（Playwright）。
- 接口：用 promptfoo（P0504）对 LiteLLM 地址做回归；GuideLLM（P0607）压测 vLLM。
- 部署：Compose 单机 → production-stack Helm（GPU 集群）→ 灰度时用 KServe 的流量切分（P1002 文档）。

### 1.5 兼容关系

| 组合 | 证据 | 判定 |
|---|---|---|
| LiteLLM → vLLM | LiteLLM 快照中检出 vLLM 提供方代码；无版本约束 | 文档支持（未验证） |
| LiteLLM → Langfuse | `pyproject.toml: langfuse>=4.7,<5.0`（Python SDK，非 Langfuse 服务版本） | 文档支持；服务端版本需另查 |
| LibreChat → LiteLLM/vLLM | LibreChat 快照检出相关文字；经 OpenAI 兼容接口 | 文档支持（未验证） |
| vLLM → xgrammar 0.2.8 | `requirements/common.txt: xgrammar == 0.2.8`，与本库 P0605 版本一致 | 版本层面一致 |
| mem0 → Qdrant | `qdrant-client>=1.12.0`（客户端）；服务端 v1.20.0 是否兼容未核对 | 待验证 |
| 输入/输出处理服务与 LibreChat 的接入方式 | 无上游参考 | **待验证建议**（需自写中间层或使用 LiteLLM hooks） |

### 1.6 尚需

模型权重与许可；GPU；LibreChat 依赖的 MongoDB/Meilisearch；Presidio 所需 spaCy 模型；Llama Guard 权重申请；OIDC 等身份提供方配置；生产域名与 TLS。

---

## 路线 2：专业知识 RAG

### 2.1 通用环节组合

| 环节 | 建议 | 说明 |
|---|---|---|
| 文档获取 | RAGFlow（P0702 v0.27.3）或 Dify（P0904 1.18.0）内置连接器；文档版本用 DVC（P0207） | 连接器未逐个核对 |
| 解析与来源定位 | Docling（P0202 v2.145.0，DoclingDocument 带页码/bbox）；MinerU（P0208，表格/公式/扫描件）；RAGFlow deepdoc | MinerU 为 Apache-2.0 加附加条款 |
| 清洗切分 | Haystack preprocessors（P0701 v3.4.1）或 RAGFlow 分块模板 `rag/app` | |
| 索引 | BGE 嵌入/重排序（P0706 v1.4.2）+ Qdrant（P0705）或 FAISS（P0704） | 嵌入与重排序权重未下载 |
| 权限过滤 | OpenFGA（P1214）计算可访问 doc_id → Qdrant payload 过滤 | **无上游参考实现，属本库建议，未验证（P0 缺口）** |
| 检索重排序 | Haystack retrievers/rankers | |
| 回答与引用 | RAGFlow 引用；评测用 Ragas（P0703）、FActScore（P1220） | “有证据支持”与“事实正确”分开评 |
| 更新维护 | DVC 数据版本 + Qdrant 快照 | 知识库版本与答案日志的关联需自建 |

接口（建议）：`原始文件 → DoclingDocument JSON（content, prov[page,bbox]） → chunks[{text, doc_id, version, page, acl}] → 向量 + payload → 检索候选[{doc_id, score}] → 重排序 → 回答 + citations[{doc_id, page, quote}]`。

启动顺序（RAGFlow 方案，未执行）：`docker/.env` 配置（占位符）→ `docker compose -f docker/docker-compose.yml config` 校验 → 依赖服务（检索引擎、MySQL、MinIO、Redis）→ RAGFlow 服务 → 在界面中配置模型提供方（指向路线 1 的 LiteLLM/vLLM）。

兼容关系：RAGFlow 快照检出 Docling、MinerU、vLLM 相关代码，**无版本约束**（文档支持，未验证）；Haystack 与 Qdrant 通过独立集成包 `qdrant-haystack`，该包不在本库（待验证）；Ragas 声明 `haystack-ai` 集成（可选依赖）。

### 2.2 医疗专用（用途与验证范围）

- **用途限定**：本库医疗条目仅用于研究与教学参考，例如医学问答检索评测、文献问答原型。**不是临床决策支持系统，没有任何条目经过临床验证或监管审批**。临床决策支持软件的监管边界请对照 FDA CDS 指南（本轮下载被 403 拒绝，未收录，见失败登记）与 WHO 大型多模态模型指南（G05，已收录）。
- 组件：MedRAG（P1101，检索器 + 语料，研究原型）+ MIRAGE（P1102，评测集已在快照中）；术语与数据结构：medspaCy（P1106）、fhir.resources（P1107）；单位与计算：pint（P1108）、MedCalc-Bench 计算器实现（P1105，数据 CC-BY-SA 4.0）；专家评价：HealthBench 评分细则（P0507）、Argilla（P0204）；人工接管：LangGraph 中断（P0806）。
- 缺失：UMLS/SNOMED CT/LOINC/RxNorm 术语库（需许可或注册，未下载）；带版本号的临床指南库；HuatuoGPT-II 因无许可证被排除。
- 规则【本库建议】：剂量/评分计算一律由工具完成，模型只负责抽取参数；输出同时记录“工具计算值”“模型生成文本”“专家确认结论”三种来源，分别标注可靠性，不合并。

### 2.3 机械制造专用（问答 / 设计辅助 / 仿真 / 实际控制分开）

| 类别 | 条目 | 状态 |
|---|---|---|
| 问答 | 通用 RAG 组合 + pint 单位换算 | 公差标准（ISO 286 等）与材料数据库需付费或授权，**缺失** |
| 设计辅助 | CadQuery（P1109 v2.8.0）、build123d（P1110 v0.13.0）作为代码执行目标；freecad-mcp（P1111，需本地 FreeCAD）；Text2CAD（P1112，CC BY-NC-SA）、CAD-Recode（P1113，CC BY-NC）为研究代码 | 几何可重建 ≠ 满足设计要求，需工程师审核 |
| 仿真辅助 | Foam-Agent（P1114，OpenFOAM v10 容器）| 57 个 LFS 指针文件未取回；结果独立校验参考**缺失** |
| 实际控制 | SemaPLC（P1115）、LLM4IAS（P1116）仅为研究原型 | **任何生成的控制代码不得直接下发真实设备**；SemaPLC 上游流程会部署到 OpenPLC 软 PLC，只能在隔离仿真环境中研究 |

---

## 路线 3：Coding 智能体

### 3.1 建议组合

| 环节 | 建议（版本） |
|---|---|
| 仓库索引 | aider repomap（P0802 v0.86.2 `aider/repomap.py`）；multilspy（P0807 v0.1.1）+ LSP 规范（D27） |
| 需求与上下文 | OpenHands SDK context（P0811 v1.59.0）；SWE-agent 配置（P0805 v1.1.0 `config/default.yaml`） |
| 计划与工具调用 | MCP 规范（D26/D0801）+ MCP Python SDK（P0801 v2.3.0）；OpenHands tools（terminal、file_editor、apply_patch） |
| 补丁编辑 | aider editblock（SEARCH/REPLACE）；OpenHands apply_patch |
| 隔离执行 | OpenHands workspace（docker / remote_api）；SWE-bench 容器；gVisor 文档（D41） |
| 构建测试与静态分析 | SWE-bench harness（P0505 v5.0.1）；Ruff（P0808 0.17.3）；Pyright 文档（D37）；Bandit 文档（D42） |
| 结果反馈 | SWE-agent 环境观察；mini-SWE-agent（P0810，教学参考） |
| 用户审核 | Continue diff 视图（P0804 `core/edit`）；aider git 提交 |
| IDE/终端 | Continue（VS Code/JetBrains/CLI）；aider CLI；VS Code 扩展 API 文档（D28） |
| 训练数据（可选，路线 B） | SWE-smith（P1117）、论文 SWE-Gym / SWE-RL |

### 3.2 接口与顺序（未执行）

`问题描述 + 仓库 → 仓库地图/LSP 符号 → 计划 → 工具调用（MCP 或 SDK 工具，JSON Schema 参数）→ 补丁（diff）→ 容器内构建与测试 → 测试日志解析（SWE-bench log_parsers）→ 反馈模型 → 用户在 IDE 审阅 diff → git 提交`。

最小验证顺序：先用 mini-SWE-agent 或 SWE-agent 在 SWE-bench Lite 的 1 个实例上跑通（需 Docker、模型 API、上游建议 ≥120GB 磁盘/16GB 内存/8 核），再替换为 OpenHands SDK。

### 3.3 兼容关系

- SWE-agent / mini-SWE-agent → SWE-bench：快照中检出 swebench 引用，无版本约束（文档支持，未验证）。
- **OpenHands SDK 固定 `litellm==1.93.0`，本库 LiteLLM 快照为 1.106.6：版本不一致，不能共用同一环境**。
- OpenHands/OpenHands v1.34.0 现为 Agent Canvas 前端/控制台，智能体运行时在 software-agent-sdk（P0811），二者版本对应关系需查上游发布说明（未核对）。

### 3.4 尚需

模型 API 或自托管代码模型；Docker；SWE-bench 数据集与镜像；各语言服务器二进制（multilspy 运行时下载）；通用依赖解析器（如 uv）源码未收录。

---

## 路线 4：模型微调与发布

### 4.1 建议组合（按依赖约束分成两套，不能混装）

**组合 A（版本层面一致）**：TRL v1.17.0（P0401）+ PEFT v0.21.2（P0402）+ vLLM v0.32.0（P0601）+ lm-eval v0.4.13（P0501）
- 依据：TRL `pyproject.toml` 声明 `vllm>=0.22.0,<0.33.0`、`peft>=0.17.0`；lm-eval 声明 `vllm>=0.18`。均为版本号层面一致，未运行验证。

**组合 B（LLaMA-Factory v0.9.5 一体化）**：必须使用其自身约束 `trl>=0.18.0,<=0.24.0`、`peft>=0.18.0,<=0.18.1`、`vllm>=0.4.3,<=0.11.0`（来自其 `pyproject.toml` 与 `requirements/vllm.txt`）。这些版本**不在本库**，需按需另行获取；不能与组合 A 的版本放在同一环境。

**强化学习（可选）**：verl v0.9.1 固定 `vllm==0.24.0`、`sglang==0.5.12`，同样与本库快照版本不同，需独立环境。

| 环节 | 组件 |
|---|---|
| 数据与标注 | Argilla（P0204）/ Label Studio（P0206）人工与专家审核；distilabel（P0203）合成 |
| 质量检查与切分 | datatrove（P0201）去重过滤；lm-eval `lm_eval/decontamination` 去污染 |
| 基座与许可 | HF 模型卡（D10 huggingface_hub 文档）；记录 repo_id + revision（提交号）+ 分词器版本 |
| 训练配置 | LLaMA-Factory `examples/train_lora/*.yaml`、`data/dataset_info.json`（组合 B）；TRL 配置类（组合 A） |
| 微调 | SFT / LoRA / QLoRA / DPO / GRPO；蒸馏：TRL `trl/experimental/gkd` |
| 检查点与恢复 | Trainer 断点恢复（transformers 文档 D03）；大规模时 torchtitan checkpointer（P0301）或 Megatron dist_checkpointing（P0302） |
| 评测 | lm-eval 自定义任务（`docs/new_task_guide.md`）；inspect_ai；安全 HarmBench/XSTest |
| 导出与量化 | LoRA 合并（LLaMA-Factory `examples/merge_lora`）；llm-compressor W4A16（P0606，输出 compressed-tensors）；llama.cpp `convert_hf_to_gguf.py` + `tools/quantize` |
| 服务部署 | vLLM（含 LoRA 适配器服务）；production-stack Helm |
| 回归、灰度、回滚 | promptfoo 回归；KServe 流量切分；Langfuse 数据集；GuideLLM 性能回归 |

### 4.2 版本关联（建议）

每次发布登记：`data_version`（DVC 提交）→ `base_model@revision` → `tokenizer@revision` → `train_config` 哈希 → `adapter` 版本 → `eval_report`（评测集版本）→ `prompt_template` 版本（Langfuse）→ `serving_image` 标签。上游没有一体化实现，需组合 DVC（P0207）、MLflow 文档（D33）、Langfuse（P1004）。

### 4.3 兼容关系小结

| 组合 | 判定 |
|---|---|
| TRL 1.17 ↔ vLLM 0.32 / PEFT 0.21.2 | 版本声明范围内（未验证） |
| LLaMA-Factory 0.9.5 ↔ 本库 TRL/PEFT/vLLM | **约束外，不能直接组合** |
| verl 0.9.1 ↔ 本库 vLLM/SGLang | **约束外** |
| llm-compressor 0.15.0 → vLLM | 依赖 `compressed-tensors==0.20.1`；vLLM 端对该格式版本的支持需核对（待验证） |
| production-stack 路由 ↔ vLLM | 路由包固定 `vllm==0.13.0`（`pyproject.toml`）；引擎默认镜像为 `helm/values.yaml` 第 45–47 行的 `lmcache/vllm-openai:latest`，**未固定版本**，部署前必须改为明确标签并核对与模型/适配器的兼容性 |

### 4.4 尚需

基座权重与许可审查；GPU（LLaMA-Factory README 第 490 行起给出各方法显存表，属上游原文，未核实）；训练数据；评测数据集（运行时下载）；Kubernetes 集群（灰度/回滚）。

---

## 附：从头训练（路线 A）参考

教学链：micrograd（P0101）→ minbpe（P0102）→ LLMs-from-scratch（P0103）→ nanoGPT（P0105）→ nanochat（P0104，全流程至命令行对话 `scripts/chat_cli.py`，`runs/runcpu.sh` 为 CPU 缩小示例）。工程级：torchtitan（P0301）、Megatron-LM（P0302 core_v0.19.2）、OLMo-core（P0303）、litgpt（P0304）；数据：datatrove、dolma；故障排查手册：ml-engineering（P0305）。详见 `from_scratch_training_route_cn.md`。
