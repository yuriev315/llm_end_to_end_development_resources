"""Project seeds: one row per upstream project (stored once, in its primary module).

Fields: id, repo (github owner/name), mod (primary module), x (cross modules), routes,
role, tag (regex over tag names -> highest numeric match; "HEAD" -> default branch
commit), purpose (Chinese one-liner). Run: python3 -I projects_seed_en.py -> projects_en.json
"""
import json
from pathlib import Path

V = r"^v?(\d+)\.(\d+)\.(\d+)$"
V2 = r"^v?(\d+)\.(\d+)(?:\.(\d+))?$"

P = [
    # 01 foundations
    ("P0101", "karpathy/micrograd", "01", [], "A", "教学实现", "HEAD", "标量自动微分与小型神经网络（反向传播教学）"),
    ("P0102", "karpathy/minbpe", "01", ["02"], "A", "教学实现", "HEAD", "BPE 分词器最小实现（训练/编码/解码，含测试）"),
    ("P0103", "rasbt/LLMs-from-scratch", "01", ["04"], "A,B", "教学实现", "HEAD", "从零实现 GPT：注意力、预训练、分类与指令微调、DPO（配套书籍代码）"),
    ("P0104", "karpathy/nanochat", "01", ["03", "04", "05", "06", "09"], "A", "完整工程", "HEAD", "小规模全流程：分词器→预训练→SFT→RL→评测→命令行对话（scripts/chat_cli.py）"),
    # 02 data
    ("P0201", "huggingface/datatrove", "02", ["03"], "A,B", "单模块参考", V, "大规模文本处理：抽取、语言识别、质量过滤、MinHash 去重、分词统计"),
    ("P0202", "docling-project/docling", "02", ["07", "12"], "B,C", "单模块参考", V, "文档解析：PDF/Office/HTML、版面、表格、公式、OCR，输出带来源定位的结构"),
    ("P0203", "argilla-io/distilabel", "02", ["04"], "B", "单模块参考", V, "合成数据与 AI 反馈流水线（指令、偏好数据生成）"),
    ("P0204", "argilla-io/argilla", "02", ["04", "05"], "B,C", "完整工程", V, "人工标注与专家审核平台（数据集版本、审核工作流、Docker 部署）"),
    ("P0205", "allenai/dolma", "02", ["03"], "A", "单模块参考", V, "预训练语料工具：打标、布隆过滤去重、混合配比"),
    ("P0206", "HumanSignal/label-studio", "02", ["05", "11"], "B,C", "完整工程", V, "多模态人工标注平台（图纸/扫描件/文本标注、多人审核、Docker）"),
    ("P0207", "iterative/dvc", "02", ["04", "10"], "A,B", "单模块参考", V, "数据与模型版本管理、流水线与实验追踪（数据—模型—配置关联）"),
    ("P0208", "opendatalab/MinerU", "02", ["07", "11"], "B,C", "单模块参考", r"^(?:mineru-)?v?(\d+)\.(\d+)\.(\d+)(?:-released)?$", "PDF 解析：表格、公式、扫描件 OCR 到 Markdown/JSON"),
    # 03 training
    ("P0301", "pytorch/torchtitan", "03", [], "A", "单模块参考", V, "PyTorch 原生大模型预训练参考：FSDP2/TP/PP/CP、float8、检查点、TOML 配置"),
    ("P0302", "NVIDIA/Megatron-LM", "03", ["04"], "A,B", "完整工程", r"^core_v(\d+)\.(\d+)\.(\d+)$", "Megatron-Core 大规模分布式训练（张量/流水/专家并行、分布式检查点）"),
    ("P0303", "allenai/OLMo-core", "03", [], "A", "完整工程", V, "OLMo 开放预训练代码：模型、训练配置、数据混合、检查点与恢复"),
    ("P0304", "Lightning-AI/litgpt", "03", ["04", "06"], "A,B", "完整工程", V, "预训练/继续预训练/微调/LoRA/评测/服务一体化，YAML 配置"),
    ("P0305", "stas00/ml-engineering", "03", ["10"], "A,B", "运行手册", "HEAD", "大模型训练与推理工程手册：硬件、网络、故障排查、调试、稳定性"),
    # 04 adaptation & alignment
    ("P0401", "huggingface/trl", "04", [], "B", "单模块参考", V, "SFT/DPO/GRPO/奖励模型/GKD 蒸馏训练器"),
    ("P0402", "huggingface/peft", "04", [], "B", "单模块参考", V, "LoRA/QLoRA 等参数高效微调与适配器保存加载"),
    ("P0403", "hiyouga/LLaMA-Factory", "04", ["06", "10"], "B", "完整工程", V, "统一微调框架：数据格式、SFT/DPO/KTO/PPO、导出合并、API 服务、Docker"),
    ("P0404", "volcengine/verl", "04", [], "B", "完整工程", V, "大模型强化学习（PPO/GRPO 等）与 vLLM/SGLang rollout 集成"),
    # 05 evaluation
    ("P0501", "EleutherAI/lm-evaluation-harness", "05", ["03", "04"], "A,B", "完整工程", V, "离线基准评测框架，YAML 自定义任务，去污染工具"),
    ("P0502", "UKGovernmentBEIS/inspect_ai", "05", ["08", "12"], "B,C", "完整工程", V, "评测框架：自定义任务、工具调用、沙箱、打分器、日志查看"),
    ("P0503", "evalplus/evalplus", "05", ["08"], "B,C", "单模块参考", V, "代码生成执行评测（HumanEval+/MBPP+），含安全执行"),
    ("P0504", "promptfoo/promptfoo", "05", ["12"], "C", "完整工程", r"^(?:promptfoo-)?v?(\d+)\.(\d+)\.(\d+)$", "应用级提示/RAG/智能体回归测试与红队，CI 集成"),
    ("P0505", "SWE-bench/SWE-bench", "05", ["08"], "B,C", "评测基准", V, "仓库级补丁评测：Docker 构建、测试执行与判定"),
    ("P0506", "stanford-crfm/helm", "05", ["11"], "B,C", "完整工程", V, "整体评测框架（含 MedHELM 医疗场景）"),
    ("P0507", "openai/simple-evals", "05", ["11"], "C", "评测基准", "HEAD", "轻量评测实现（含 HealthBench 评分细则评测）"),
    # 06 inference
    ("P0601", "vllm-project/vllm", "06", ["10", "12"], "B,C", "完整工程", V, "高吞吐推理服务：PagedAttention、连续批处理、量化、OpenAI 兼容 API、结构化输出、工具调用解析、基准脚本"),
    ("P0602", "ggml-org/llama.cpp", "06", ["04"], "B,C", "完整工程", r"^b(\d+)$", "CPU/GPU 本地推理、GGUF 转换与量化、HTTP 服务、语法约束输出"),
    ("P0603", "sgl-project/sglang", "06", [], "B,C", "完整工程", V, "推理服务：RadixAttention 前缀缓存、结构化输出、调度"),
    ("P0604", "dottxt-ai/outlines", "06", ["12"], "C", "单模块参考", V, "受约束生成：JSON Schema/正则/语法"),
    ("P0605", "mlc-ai/xgrammar", "06", ["12"], "C", "单模块参考", V, "结构化生成语法引擎（vLLM/SGLang 后端）"),
    ("P0606", "vllm-project/llm-compressor", "06", ["04"], "B", "单模块参考", V, "训练后量化/稀疏化并导出 vLLM 可加载格式"),
    ("P0607", "vllm-project/guidellm", "06", ["10"], "B,C", "单模块参考", V, "推理服务负载测试：吞吐、延迟、并发扫描"),
    # 07 RAG
    ("P0701", "deepset-ai/haystack", "07", ["12"], "C", "完整工程", V, "RAG/智能体管线框架：组件、检索、重排序、评测"),
    ("P0702", "infiniflow/ragflow", "07", ["09", "10"], "C", "完整工程", V, "完整 RAG 产品：深度文档解析、分块模板、引用、多租户、Docker Compose"),
    ("P0703", "explodinggradients/ragas", "07", ["05"], "C", "单模块参考", V, "RAG 评测指标与测试集生成"),
    ("P0704", "facebookresearch/faiss", "07", [], "C", "单模块参考", V, "向量相似检索与索引库"),
    ("P0705", "qdrant/qdrant", "07", ["12"], "C", "完整工程", V, "向量数据库：载荷过滤（按用户/租户/文档权限过滤）、快照、分布式部署"),
    ("P0706", "FlagOpen/FlagEmbedding", "07", ["04"], "B,C", "单模块参考", V, "BGE 嵌入与重排序模型的推理、微调、评测代码"),
    # 08 agents & coding
    ("P0801", "modelcontextprotocol/python-sdk", "08", ["12"], "C", "单模块参考", V, "MCP 官方 Python SDK：工具/资源/提示接口，服务端与客户端"),
    ("P0802", "Aider-AI/aider", "08", [], "C", "完整工程", V, "终端结对编程：仓库地图、补丁编辑格式、lint/测试回路、git 集成"),
    ("P0803", "OpenHands/OpenHands", "08", ["10"], "C", "完整工程", V, "OpenHands Agent Canvas（本版本为自托管前端/控制台：会话、自动化、Helm/Docker；智能体运行时在 P0811）"),
    ("P0811", "OpenHands/software-agent-sdk", "08", ["12"], "C", "完整工程", V, "OpenHands 智能体 SDK 与 Agent Server：工具、沙箱工作区（Docker/远程）、安全分析与确认策略"),
    ("P0804", "continuedev/continue", "08", [], "C", "完整工程", r"^v(\d+)\.(\d+)\.(\d+)-vscode$", "IDE 集成（VS Code/JetBrains）代码助手与 CLI"),
    ("P0805", "SWE-agent/SWE-agent", "08", ["05"], "C", "完整工程", V, "仓库问题修复智能体：ACI 工具、配置、轨迹、批量评测"),
    ("P0806", "langchain-ai/langgraph", "08", ["12"], "C", "单模块参考", r"^(\d+)\.(\d+)\.(\d+)$", "有状态智能体编排：检查点、人工中断审批、重试、持久执行"),
    ("P0807", "microsoft/multilspy", "08", ["11"], "C", "单模块参考", V, "面向智能体的语言服务器（LSP）客户端：定义/引用/补全"),
    ("P0808", "astral-sh/ruff", "08", ["11"], "C", "单模块参考", r"^(\d+)\.(\d+)\.(\d+)$", "Python 静态检查与格式化（规则集、配置）"),
    ("P0809", "mem0ai/mem0", "08", ["09", "12"], "C", "单模块参考", V, "对话记忆层：记忆写入/更新/删除、按用户/会话隔离"),
    # 09 chat & product
    ("P0901", "danny-avila/LibreChat", "09", ["10"], "C", "完整工程", V, "多用户对话产品：认证、会话存储、文件上传、配额、多模型接入、Docker Compose"),
    ("P0902", "huggingface/chat-ui", "09", [], "C", "完整工程", V, "开源对话前后端（SvelteKit、MongoDB 会话、OpenAI 兼容后端）"),
    ("P0903", "open-webui/open-webui", "09", ["10"], "C", "完整工程", V, "自托管对话界面：RBAC、RAG、管道、Ollama/OpenAI 接入"),
    ("P0904", "langgenius/dify", "09", ["07", "10"], "C", "完整工程", r"^(\d+)\.(\d+)\.(\d+)$", "LLM 应用平台：工作流、知识库、多租户、任务队列、Docker Compose"),
    # 10 deployment & operations
    ("P1001", "vllm-project/production-stack", "10", ["06"], "B,C", "完整工程", r"^vllm-stack-(\d+)\.(\d+)\.(\d+)$", "vLLM 生产部署：Helm、路由、KV 缓存复用、Prometheus/Grafana 监控"),
    ("P1002", "kserve/kserve", "10", ["06"], "B,C", "完整工程", V, "Kubernetes 模型服务：InferenceService、灰度、扩缩容"),
    ("P1003", "BerriAI/litellm", "10", ["09", "12"], "C", "完整工程", r"^v(\d+)\.(\d+)\.(\d+)(?:-stable)?$", "模型网关：统一接口、密钥/预算/限速、回退、日志"),
    ("P1004", "langfuse/langfuse", "10", ["05", "12"], "C", "完整工程", V, "LLM 可观测性：追踪、评测、人工评分、提示版本、数据集回流"),
    ("P1005", "NVIDIA/k8s-device-plugin", "10", [], "B,C", "单模块参考", V, "Kubernetes GPU 设备插件（GPU 调度、时间切片、MIG）"),
    ("P1008", "temporalio/sdk-python", "10", ["12"], "C", "单模块参考", r"^(\d+)\.(\d+)\.(\d+)$", "持久执行：活动超时、重试策略、取消、幂等工作流（需 Temporal 服务）"),
    ("P1006", "jd/tenacity", "10", ["12"], "C", "工具库", r"^(\d+)\.(\d+)\.(\d+)$", "重试库：退避、停止条件、异步重试"),
    # 11 applications
    ("P1101", "Teddy-XiongGZ/MedRAG", "11", ["07"], "C", "研究原型", "HEAD", "医学 RAG 工具包（检索器、语料、MIRAGE 评测配套）"),
    ("P1102", "Teddy-XiongGZ/MIRAGE", "11", ["05"], "C", "评测基准", "HEAD", "医学 RAG 评测基准（MMLU-Med、MedQA 等 5 个数据集）"),
    ("P1103", "Google-Health/medgemma", "11", ["04"], "B", "研究原型", "HEAD", "MedGemma 官方笔记本：推理、微调示例（权重另有使用条款）"),
    ("P1104", "FreedomIntelligence/HuatuoGPT-II", "11", ["04"], "B", "研究原型", "HEAD", "中文医疗领域一阶段适配训练代码与评测"),
    ("P1105", "ncbi-nlp/MedCalc-Bench", "11", ["05"], "C", "评测基准", "HEAD", "医学计算器评测（公式与单位计算，含参考实现）"),
    ("P1106", "medspacy/medspacy", "11", ["12"], "C", "单模块参考", V, "临床文本处理：否定/上下文、段落、术语匹配"),
    ("P1107", "nazrulworld/fhir.resources", "11", [], "C", "工具库", V, "FHIR 资源 Python 模型（与医疗业务系统对接的数据结构校验）"),
    ("P1108", "hgrecco/pint", "11", ["12"], "C", "工具库", V2, "物理单位与量纲换算校验（医疗剂量单位、机械工程单位）"),
    ("P1109", "CadQuery/cadquery", "11", [], "C", "工具库", V, "参数化 CAD 脚本库（LLM 生成 CAD 代码的执行目标）"),
    ("P1110", "gumyr/build123d", "11", [], "C", "工具库", V, "参数化 CAD（基于 OCCT），导出 STEP/STL"),
    ("P1111", "neka-nat/freecad-mcp", "11", ["08"], "C", "研究原型", "HEAD", "FreeCAD 的 MCP 服务器（设计辅助，需本地 FreeCAD）"),
    ("P1112", "SadilKhan/Text2CAD", "11", [], "B", "研究原型", "HEAD", "文本到 CAD 序列生成（研究代码）"),
    ("P1113", "filapro/cad-recode", "11", [], "B", "研究原型", "HEAD", "点云到 CadQuery 代码逆向（研究代码）"),
    ("P1114", "csml-rpi/Foam-Agent", "11", ["08"], "C", "研究原型", "HEAD", "OpenFOAM 仿真智能体：前处理、运行、错误修复（仿真辅助）"),
    ("P1115", "midea-ai/SemaPLC", "11", ["08"], "C", "研究原型", "HEAD", "PLC 结构化文本生成与验证门控（控制代码研究，不可直接下发设备）"),
    ("P1116", "YuchenXia/LLM4IAS", "11", ["08"], "C", "研究原型", "HEAD", "工业自动化系统 LLM 智能体（仿真/实验环境控制研究）"),
    ("P1117", "SWE-bench/SWE-smith", "11", ["04", "08"], "B", "完整工程", V, "Coding 智能体训练数据合成（任务实例生成、轨迹）"),
    # 12 input/output pipeline
    ("P1201", "microsoft/presidio", "12", [], "C", "完整工程", r"^(\d+)\.(\d+)\.(\d+)$", "PII 识别与脱敏（分析器/匿名器、自定义识别器、Docker）"),
    ("P1202", "Yelp/detect-secrets", "12", [], "C", "单模块参考", V, "凭据/密钥检测（插件、基线、审计）"),
    ("P1203", "pemistahl/lingua-py", "12", ["02"], "C", "工具库", V, "语言识别（短文本、多语言置信度）"),
    ("P1204", "NVIDIA-NeMo/Guardrails", "12", [], "C", "完整工程", V, "运行时护栏：输入/输出/检索/执行 rails、对话流程、配置"),
    ("P1205", "guardrails-ai/guardrails", "12", [], "C", "单模块参考", V, "输出校验器框架：结构、类型、重问修复"),
    ("P1206", "meta-llama/PurpleLlama", "12", ["05"], "B,C", "评测基准", "HEAD", "Llama Guard/Prompt Guard 安全分类与 CyberSecEval 评测"),
    ("P1207", "protectai/llm-guard", "12", [], "C", "单模块参考", V, "输入/输出扫描器：提示注入、PII、毒性、代码、URL"),
    ("P1208", "lm-sys/RouteLLM", "12", [], "C", "研究原型", "HEAD", "强弱模型路由（成本-质量权衡）"),
    ("P1209", "aurelio-labs/semantic-router", "12", [], "C", "单模块参考", V, "基于嵌入的意图/路由判定"),
    ("P1210", "google-research/camel-prompt-injection", "12", ["08"], "C", "研究原型", "HEAD", "CaMeL：控制流/数据流隔离防提示注入（研究实现）"),
    ("P1211", "ethz-spylab/agentdojo", "12", ["05", "08"], "C", "评测基准", V, "智能体提示注入攻防评测环境"),
    ("P1212", "NVIDIA/garak", "12", ["05"], "C", "完整工程", V, "LLM 漏洞扫描（探针/检测器/报告）"),
    ("P1213", "microsoft/PyRIT", "12", ["05"], "C", "完整工程", V, "生成式 AI 风险识别与红队自动化框架"),
    ("P1214", "openfga/openfga", "12", ["07", "09"], "C", "完整工程", V, "细粒度授权（关系型访问控制，适用于用户/租户/文档权限过滤）"),
    ("P1215", "openai/model_spec", "12", [], "C", "规范文档", "HEAD", "模型行为规范（指令层级：平台/开发者/用户）"),
    ("P1216", "microsoft/LLMLingua", "12", [], "C", "研究原型", V, "提示/上下文压缩"),
    ("P1217", "567-labs/instructor", "12", [], "C", "单模块参考", V, "Pydantic 结构化输出、校验失败重试"),
    ("P1218", "pydantic/pydantic", "12", [], "C", "工具库", V, "请求/响应数据模型与类型校验"),
    ("P1219", "python-jsonschema/jsonschema", "12", [], "C", "工具库", V, "JSON Schema 校验"),
    ("P1220", "shmsw25/FActScore", "12", ["05"], "C", "研究原型", V, "长文本事实性逐条原子事实打分"),
    ("P1221", "cure53/DOMPurify", "12", ["09"], "C", "工具库", r"^(\d+)\.(\d+)\.(\d+)$", "前端 HTML 净化（防 XSS 的模型输出呈现）"),
    ("P1222", "messense/nh3", "12", ["09"], "C", "工具库", V, "Python 端 HTML 净化（ammonia 绑定）"),
    ("P1223", "microsoft/BIPIA", "12", ["05"], "C", "评测基准", "HEAD", "间接提示注入基准（外部内容嵌入指令）"),
    ("P1224", "uiuc-kang-lab/InjecAgent", "12", ["05"], "C", "评测基准", "HEAD", "工具集成智能体间接提示注入基准"),
    ("P1225", "centerforaisafety/HarmBench", "12", ["05"], "B,C", "评测基准", "HEAD", "红队与拒答鲁棒性标准化评测"),
    ("P1226", "JailbreakBench/jailbreakbench", "12", ["05"], "C", "评测基准", V, "越狱攻击/防御基准与评测器"),
    ("P1227", "allenai/wildguard", "12", ["05"], "B,C", "评测基准", "HEAD", "安全分类器与评测（有害提示/回复/拒答）"),
    ("P1228", "ShishirPatil/gorilla", "12", ["05", "08"], "C", "评测基准", V2, "含 BFCL 函数调用评测（名称/参数/多轮）"),
    ("P1229", "paul-rottger/xstest", "12", ["05"], "C", "评测基准", "HEAD", "过度拒答（误报）测试集"),
]

DOCS = [
    # official documentation repositories (counted as 官方文档 per version/commit)
    ("D0901", "LibreChat-AI/librechat.ai", "09", [], "C", "官方文档", "HEAD", "LibreChat 官方文档站源（配置 librechat.yaml、认证、部署）"),
    ("D0902", "open-webui/docs", "09", [], "C", "官方文档", "HEAD", "Open WebUI 官方文档站源（部署、RBAC、管道）"),
    ("D0903", "langgenius/dify-docs", "09", [], "C", "官方文档", "HEAD", "Dify 官方文档源（自托管、环境变量、知识库）"),
    ("D1001", "langfuse/langfuse-docs", "10", [], "C", "官方文档", "HEAD", "Langfuse 官方文档站源（自托管、追踪、评测、提示管理）"),
    ("D0601", "openai/openai-openapi", "06", ["09"], "C", "接口规范", "HEAD", "OpenAI API OpenAPI 规范（事实标准的 Chat Completions/Responses 接口，vLLM/LiteLLM 兼容目标）"),
    ("D1201", "OWASP/www-project-top-10-for-large-language-model-applications", "12", [], "C", "安全规范", "HEAD", "OWASP LLM 应用十大风险（2025 版源文件、多语言译本）"),
    ("D0801", "modelcontextprotocol/modelcontextprotocol", "08", ["12"], "C", "接口规范", "HEAD", "MCP 规范与文档（本轮最新提交；另有复用的较早快照）"),
]

REUSE = [
    # (id, title, source library path, mod, routes, role, purpose)
    ("P0105", "karpathy/nanoGPT（复用）", "/root/programming_reference_literature/practice/karpathy_nanoGPT_master_en.tar", "01", "A", "教学实现", "最小 GPT 训练/微调代码"),
    ("P0810", "SWE-agent/mini-swe-agent（复用）", "/root/programming_reference_literature/practice/mini_swe_agent_main_en.tar", "08", "C", "教学实现", "约百行的参考代码智能体"),
    ("P1007", "GokuMohandas/Made-With-ML（复用）", "/root/ai_undergraduate_graduate_curriculum_literature/practice/MadeWithML_repo_en", "10", "C", "教学实现", "MLOps 端到端课程代码（测试、CI/CD、部署）"),
]

if __name__ == "__main__":
    out = [dict(id=i, repo=r, mod=m, x=x, routes=ro, role=role, tag=t, purpose=p) for i, r, m, x, ro, role, t, p in P]
    out += [dict(id=i, repo=r, mod=m, x=x, routes=ro, role=role, tag=t, purpose=p, dir="papers_books_courses/official_docs")
            for i, r, m, x, ro, role, t, p in DOCS]
    ids = [o["id"] for o in out] + [r[0] for r in REUSE]
    assert len(ids) == len(set(ids)), "duplicate ids"
    Path(__file__).with_name("projects_en.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    Path(__file__).with_name("projects_reuse_en.json").write_text(json.dumps(
        [dict(id=i, title=t, src=s, mod=m, routes=ro, role=role, purpose=p) for i, t, s, m, ro, role, p in REUSE],
        ensure_ascii=False, indent=1), encoding="utf-8")
    print(len(out), "projects,", len(REUSE), "reuse")
