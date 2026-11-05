# 完成报告：大语言模型端到端开发资源库（2026-10-29）

目录：`/root/llm_end_to_end_development_resources/`（约 13 GB 资料；另有一个非本流程创建的 `.git`，约 5.8 GB，见第 8 节）

## 1. 现状核对

- 开始时目标目录**不存在**，本库全部在本轮建立。此前的大模型多模态、ML/DL、小语种资料库在本机已不存在，无法复用；复用来源只有 `programming_reference_literature` 与 `ai_undergraduate_graduate_curriculum_literature`。
- 计数口径：只计入下载成功且通过核验的条目。只有链接、残缺、失败和按规则排除的条目单列在 `download_failures_cn.csv`，不计入。
- 本轮**没有**安装依赖、运行外部代码、训练、部署、上传或删除资料。

## 2. 数量

| 类别 | 已核验收录 | 其中新下载 | 其中复用 | 说明 |
|---|---|---|---|---|
| 独立源码项目（按项目 + 版本计） | 110 | 107 | 3 | 每个项目只保存一份，跨模块通过索引关联 |
| 官方文档 / 规范（按版本计） | 54 | 9 | 45 | 新下载 = 6 个文档/规范仓库快照 + 3 份官方指南 PDF（NIST AI 600-1、NIST AI RMF 1.0、WHO 大型多模态模型指南）；复用中 10 份为“部分资料”（范围见目录备注） |
| 论文 | 217 | 185 | 32 | 各研究模块 17–29 篇；158 篇首发于近三年；29 篇为注明理由的经典例外；另 30 篇早于窗口（2022–2023 年 10 月前），目录中标“早于窗口” |
| 教材 | 9 | 0 | 9 | SLP3、UDL、D2L、Foundations of LLMs、大语言模型（LLMBook，中文）、ML Systems 上下卷、How to Scale Your Model、ML in Production |
| 课程 / 实践包 | 18 | 0 | 18 | CS336（讲义 + 作业 1/2）、CS224N、CMU 11-711、CMU 11-766、Berkeley LLM Agents ×2、HF LLM/Agents 课程、CS329S、FSDL、CMU 17-645、Zero to Hero、Claude/OpenAI Cookbook、FastAPI 全栈模板、DeepSpeedExamples |
| 失败 / 排除 | 5 | — | — | 见第 7 节 |

论文目标（每个研究模块约 30–50 篇）**未达到**：本轮按补充要求优先补齐代码、配置、测试和文档，没有扩大论文配额。各模块：01=17、02=18、03=21、04=22、05=19、06=20、07=24、08=25、11=22、12=29。

## 3. 可运行性等级与证据

| 等级 | 数量 | 证据 |
|---|---|---|
| L3 / L2 | 0 | 本轮未执行任何上游代码，无执行记录 |
| L1 | 95 | 只读静态扫描：许可证文件、依赖声明、入口（pyproject scripts / Makefile / 入口文件 / README 命令）、安装说明齐备；LibreChat 为人工核对（安装文档在独立文档站 D0901） |
| L0 | 13 | 缺依赖声明、明确入口或安装说明：nanoGPT（复用）、simple-evals、Continue（README 无安装段）、tenacity（库，无入口）、MedRAG、MIRAGE、MedGemma 笔记本、MedCalc-Bench（无 LICENSE 文件）、CAD-Recode、LLM4IAS、PurpleLlama（多组件）、FActScore、XSTest（数据集） |
| 不适用 | 8 | 文档/规范/手册类（OpenAI API 规范、MCP 规范、LibreChat/Dify/Langfuse 文档站源、OWASP LLM Top 10、Model Spec、ml-engineering 手册） |

每个项目的证据、入口、配置、测试、CI、部署文件和“下一步验证命令（未执行）”见 `project_readiness_cn.csv` 与 `project_cards/<编号>_cn.md`。

快照不完整之处（已逐项标注）：7 个项目含未下载的子模块（P0103、P0404、P0502、P0605×3、P0809、P1008、P1206）；Foam-Agent 有 57 个 Git LFS 指针文件、Qdrant 有 1 个未取回；lingua-py 2.x 快照不含 Rust 实现（lingua-rs）。

## 4. 四条路线的覆盖情况（详见 `end_to_end_coverage_cn.csv`）

| 路线 | 已覆盖 | 部分覆盖 | 缺失 |
|---|---|---|---|
| 1 通用对话助手（9 个环节） | 模型接入、生成、前后端、部署、监控反馈 | 输入处理、上下文与记忆、输出处理、认证与隔离 | — |
| 2 专业知识 RAG 通用环节（8 个） | 解析与来源定位、清洗切分、索引、检索重排序 | 文档获取、**权限过滤（P0）**、回答与引用、更新维护 | — |
| 2 医疗专用（4 项） | — | 医学检索与评测、**术语与编码（P0）**、单位与计算、**指南版本/证据追踪/专家评价/人工接管（P0）** | — |
| 2 机械制造专用（4 项） | — | CAD/CAE 接口、**实际控制（仅研究，P0）** | **单位/公差/材料数据（P0）**、**仿真结果检查与工程师审核（P0）** |
| 3 Coding 智能体（9 个） | 全部 9 个环节均有参考实现 | — | — |
| 4 模型微调与发布（10 个） | 数据标注、质量切分、训练配置、微调、检查点恢复、评测、导出量化、服务部署 | **基座和许可证（P0，未下载任何权重）**、回归/灰度/回滚 | — |

覆盖矩阵中引用的全部上游入口文件与目录都已核对确实存在于快照中。“已覆盖”只表示有对应的参考代码与文档，不表示已验证可运行。

### 参考链完整程度

| 路线 | 参考链 | 主要缺少 |
|---|---|---|
| 1 通用助手 | 有完整参考链（vLLM → LiteLLM → LibreChat，Langfuse 监控） | 模型权重/API、GPU、身份提供方；输入/输出处理服务与 LibreChat 之间的接入层无上游参考；未验证 |
| 2 RAG（通用） | 有完整参考链（Docling/MinerU → Haystack 或 RAGFlow → BGE → Qdrant → Ragas） | 嵌入/解析模型权重；**权限过滤拼接无上游参考**；未验证 |
| 2 医疗 | 只有研究级参考链（MedRAG + MIRAGE + 计算器） | 术语库许可（UMLS/SNOMED/LOINC）、医学语料与嵌入（体积大未下载）、指南版本库、临床验证 |
| 2 机械制造 | 不完整 | 公差标准、材料数据（付费/授权）；仿真结果独立校验；研究原型多为非商业许可 |
| 3 Coding | 有完整参考链（aider/multilspy → OpenHands SDK 或 SWE-agent → SWE-bench → Continue） | 模型、Docker、SWE-bench 数据与镜像（上游建议 ≥120GB 磁盘）；未验证 |
| 4 微调发布 | 有完整参考链，但**版本冲突**（见第 5 节） | 基座权重与许可、GPU、旧版本依赖、集群；未验证 |

## 5. 兼容性核对结果（`compatibility_matrix_cn.csv`，41 组）

39 组在使用方快照中检出对被依赖方的引用（文档/代码提及，未验证），2 组未检出（列为待验证建议）。按依赖文件中的版本约束自动比对：

- **约束外，不能直接组合**：LLaMA-Factory v0.9.5 要求 `trl<=0.24.0`、`peft<=0.18.1`、`vllm<=0.11.0`（本库为 TRL 1.17.0 / PEFT 0.21.2 / vLLM 0.32.0）；verl v0.9.1 固定 `vllm==0.24.0`、`sglang==0.5.12`；OpenHands SDK 固定 `litellm==1.93.0`（本库 1.106.6）；production-stack 路由包固定 `vllm==0.13.0`。
- **版本范围内（仅版本号层面）**：TRL 1.17 ↔ vLLM 0.32 / PEFT 0.21.2；lm-eval ↔ vLLM；vLLM ↔ xgrammar 0.2.8；NeMo Guardrails ↔ Presidio；freecad-mcp ↔ MCP SDK；garak ↔ LiteLLM。
- **声明与固定不一致**：instructor 的 `pyproject.toml` 允许 pydantic 2.14.2，但其 `requirements.txt` 固定 2.13.4。
- 其他：production-stack Helm 默认引擎镜像为 `lmcache/vllm-openai:latest`（未固定版本）；22 组没有显式版本约束，靠 OpenAI 兼容 HTTP 接口或可选插件对接，协议细节待验证。

## 6. 缺口清单摘要（`gap_backlog_cn.csv`：P0 7 项、P1 20 项、P2 7 项）

P0（不补就连不成流程）：RAG 权限过滤拼接；医疗术语与编码库；医疗指南版本/证据追踪/人工接管；机械公差与材料数据；仿真结果独立检查与工程师审核；PLC 实际控制只能停留在研究；微调基座权重与许可登记。

P1 示例：输入处理的多语言误报评测；记忆删除与租户隔离测试；LLaMA-Factory/verl 所需的旧版本依赖；数据—模型—分词器—提示—适配器版本关联；FDA 指南获取；Foam-Agent LFS 对象；镜像版本固定。

## 7. 失败与排除

| 条目 | 原因 | 处理 |
|---|---|---|
| FDA《Clinical Decision Support Software》指南、FDA/加拿大卫生部/MHRA《GMLP 指导原则》 | HTTP 403（站点拒绝自动下载） | 未绕过；需人工从 fda.gov 下载 |
| SentencePiece 论文（arXiv 1808.06226） | PDF 文本无法抽取，标题核验不通过 | 未计入；需人工核对 |
| HuatuoGPT-II 源码、Open WebUI 文档仓库 | 上游无 LICENSE 文件、README 也无许可声明 | 下载后按无许可证不收录规则排除，归档移至 `/root/.cache/lede_lit/excluded/`（未删除） |

另：Azure/PyRIT 已于 2026-03-27 归档，改为从新地址 microsoft/PyRIT 的 v1.1.0 收录，旧快照移至缓存 excluded/。llm-guard 与 BIPIA 上游已归档，保留并注明。

## 8. 需要你决定的事项

- 库根目录的 `.git`（约 5.8 GB，2026-10-29 20:12Z 创建，单个提交 “first commit”，远端为 `github.com/yuriev315/llm_end_to_end_development_resources`）**不是本流程创建的**，内容是建库中途的部分状态。本轮未读写、未推送。如需上传，应在本轮资料定稿后重新提交，并注意 GitHub 单文件 100 MiB 限制（多个源码归档超过该大小）。
- 是否人工下载两份 FDA 文件并补登记。

## 9. 下一步最小运行验证方案（均未执行）

前提：隔离容器或虚拟机，默认 CPU、无 GPU；只读挂载归档；不使用真实凭据。

1. **L2 冒烟（CPU，约 1–2 小时）**：解包 minbpe、micrograd、jsonschema、nh3、presidio、detect-secrets、pint、cadquery 快照，在各自虚拟环境安装后运行上游测试子集（命令见 `project_readiness_cn.csv`），记录环境、命令与输出，再把这些项目改登为 L2。
2. **路线 1 最小链**：llama.cpp（CPU）加载一个小型开放权重 GGUF 模型 → LiteLLM 指向它 → promptfoo 跑 5 条回归用例；全程只用 `docker compose config` 与本地进程，验证 OpenAI 兼容接口能否打通。
3. **路线 2 最小链**：用 docling `tests/data` 的样例 PDF 解析 → FAISS 建索引 → 检索 → Ragas 指标（裁判模型用第 2 步的本地模型）。
4. **路线 3 最小链**：mini-SWE-agent + SWE-bench Lite 单实例（需 Docker 与约 120GB 磁盘）。
5. **路线 4 最小链**：TRL 1.17 + PEFT 0.21.2，用 LLaMA-Factory 自带的 `alpaca_en_demo.json` 格式数据在极小模型上做 LoRA SFT 几步 → lm-eval 跑 1 个任务；需 GPU 时另行申请资源。

只有在记录环境中通过上述测试，才能把对应项目或路线标为 L2/L3。
