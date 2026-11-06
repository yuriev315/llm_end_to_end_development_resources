"""Input/output pipeline validation matrix rows (input_output_pipeline/validation_matrix_cn.csv).

Each row: stage, check item, what a pass proves (one of 格式正确 / 规则通过 / 有证据支持 / 事实正确 /
权限正确 / 安全评测), implementations [(project id, [paths])], upstream test evidence
[(project id, [test paths])], public eval sets, limits. Paths are checked by build_guides_en.py.
"""

PROVES = ("格式正确", "规则通过", "有证据支持", "事实正确", "权限正确", "安全评测")

ROWS = [
    ("输入前处理", "请求结构、字段类型、长度、编码校验", "格式正确", [("P1218", ["pydantic"]), ("P1219", ["jsonschema"])], [("P1218", ["tests"])], "", "只证明结构合法，不证明内容安全或意图正确"),
    ("输入前处理", "文件格式与文档解析（PDF/Office/扫描件/表格/公式）", "格式正确", [("P0202", ["docling/cli/main.py"]), ("P0208", ["mineru"])], [("P0202", ["tests/data"])], "docling tests/data 期望输出", "解析正确率需按业务文档另建标注集；工程图纸无专门解析"),
    ("输入前处理", "语言识别", "规则通过", [("P1203", ["language-testdata", "accuracy-reports"])], [("P1203", ["accuracy-reports"])], "lingua accuracy-reports（上游报告）", "实现位于 lingua-rs，未在快照中；短文本与混合语言误判需自测"),
    ("输入前处理", "PII 识别与脱敏（保留原始/脱敏映射）", "规则通过", [("P1201", ["presidio-analyzer", "presidio-anonymizer"])], [("P1201", ["presidio-analyzer/tests"])], "", "识别依赖 NER 模型与规则，多语言漏报率需自测；可逆脱敏映射须加密存储"),
    ("输入前处理", "凭据/密钥检测", "规则通过", [("P1202", ["detect_secrets"])], [("P1202", ["tests"])], "", "基于规则/熵，存在误报与漏报"),
    ("输入前处理", "内容分类与风险分级", "安全评测", [("P1206", ["Llama-Guard3"]), ("P1227", ["README.md"]), ("P1207", ["README.md"])], [("P1229", ["xstest_prompts.csv"])], "XSTest（过度拒答）、WildGuard 评测", "分类器输出是概率判断；llm-guard 上游已归档"),
    ("输入前处理", "意图识别与模型/工具路由", "规则通过", [("P1209", ["semantic_router"]), ("P1208", ["routellm"])], [("P1209", ["tests"])], "", "路由准确率需业务意图集；RouteLLM 为研究原型"),
    ("输入前处理", "提示注入检测（直接/间接、附件内容）", "安全评测", [("P1206", ["Prompt-Guard", "LlamaFirewall"]), ("P1204", ["nemoguardrails/library"])],
     [("P1211", ["src/agentdojo"]), ("P1223", ["README.md"]), ("P1224", ["README.md"])], "AgentDojo、BIPIA、InjecAgent", "检测器可被绕过；必须配合权限隔离，不能作为唯一防线"),
    ("输入前处理", "用户/租户/角色/资源访问权限", "权限正确", [("P1214", ["docs"]), ("P0903", ["backend/open_webui/utils/access_control"])], [("P1214", ["assets/tests"])], "", "授权判定正确不代表检索层已执行过滤，需端到端越权测试"),
    ("指令组织", "指令层级（平台/开发者/用户）与冲突处理", "规则通过", [("P1215", ["README.md"]), ("P1204", ["examples/configs"])], [], "", "模型规范是行为目标文档，不是可执行检查；冲突处理效果需评测"),
    ("指令组织", "上下文预算与历史压缩", "规则通过", [("P1216", ["llmlingua"]), ("P0811", ["openhands-sdk/openhands/sdk/context"])], [], "", "压缩可能丢失关键信息，需回归评测"),
    ("指令组织", "检索内容与工具结果的可信边界（数据≠指令）", "安全评测", [("P1210", ["README.md"]), ("P1204", ["nemoguardrails/rails"])], [("P1211", ["src/agentdojo"])], "AgentDojo", "CaMeL 为研究实现；边界标记降低风险但不消除"),
    ("生成", "结构化输出约束（JSON Schema/语法）", "格式正确", [("P0605", ["python"]), ("P0604", ["src"]), ("P0601", ["docs/features/structured_outputs.md"])], [("P0605", ["tests"]), ("P0604", ["tests"])], "", "约束解码保证语法，不保证字段语义正确"),
    ("输出后处理", "流式解析、停止条件、截断与中断", "格式正确", [("P0601", ["vllm/entrypoints/openai/api_server.py", "vllm/tool_parsers"])], [("P0601", ["tests/entrypoints"])], "", "流式与非流式一致性、客户端取消需自建测试"),
    ("输出后处理", "JSON/Schema/业务约束校验与有限重试", "格式正确", [("P1217", ["instructor"]), ("P1205", ["guardrails"])], [("P1217", ["tests"]), ("P1205", ["tests"])], "", "重试次数与回退策略需显式上限；重试成本需记录"),
    ("输出后处理", "工具调用名称、参数、权限及执行前校验", "权限正确", [("P0801", ["src/mcp/server"]), ("P0811", ["openhands-sdk/openhands/sdk/security"])], [("P1228", ["berkeley-function-call-leaderboard"])], "BFCL", "参数格式正确≠调用合适；高影响操作须人工确认"),
    ("输出后处理", "引用来源与检索证据支持检查", "有证据支持", [("P0703", ["src"]), ("P1220", ["factscore"])], [("P0703", ["tests"])], "ALCE（论文）、RAGAS 指标", "裁判模型自身可能出错；有证据支持≠事实正确"),
    ("输出后处理", "事实正确性（独立来源核对）", "事实正确", [("P1220", ["factscore"])], [], "FActScore、SimpleQA 类（论文）", "需要独立知识源与人工抽检；模型自检不能替代"),
    ("输出后处理", "敏感信息泄露、内容风险与越权内容检测", "安全评测", [("P1201", ["presidio-analyzer"]), ("P1212", ["garak/probes", "garak/detectors"])], [("P1212", ["tests"]), ("P1225", ["configs"])], "HarmBench、JailbreakBench、garak 探针", "红队覆盖有限，需持续回归"),
    ("输出后处理", "医疗专用校验（单位、剂量计算、术语编码）", "规则通过", [("P1108", ["pint"]), ("P1105", ["calculator_implementations"]), ("P1106", ["medspacy"])], [("P1106", ["tests"])], "MedCalc-Bench、HealthBench", "研究代码，未经临床验证；高风险输出必须人工审核"),
    ("输出后处理", "机械专用校验（单位、几何可重建性）", "规则通过", [("P1108", ["pint"]), ("P1109", ["cadquery"])], [("P1109", ["tests"])], "", "公差/材料标准数据缺失；几何可重建≠满足设计要求"),
    ("输出后处理", "Coding 专用校验（编译、测试、静态分析）", "规则通过", [("P0505", ["swebench/harness/run_evaluation.py"]), ("P0808", ["crates"]), ("P0802", ["aider/linter.py"])], [("P0505", ["tests"])], "SWE-bench", "测试通过≠需求正确；需人工审阅 diff"),
    ("输出后处理", "Markdown/HTML/链接安全呈现", "规则通过", [("P1221", ["src"]), ("P1222", ["src"])], [("P1221", ["test"]), ("P1222", ["tests"])], "", "净化配置需与前端渲染器一致"),
    ("输出后处理", "格式修复、模型回退与人工审核", "规则通过", [("P1003", ["litellm/router.py"]), ("P0806", ["libs/langgraph/langgraph/types.py"]), ("P0204", ["argilla-server"])], [], "", "回退带来延迟与成本，需在追踪中记录"),
    ("工具执行", "建议与执行分离、执行隔离、超时与资源限制", "权限正确", [("P0811", ["openhands-workspace/openhands/workspace/docker"]), ("P0505", ["swebench/harness/docker_utils.py"])], [("P0811", ["tests"])], "", "容器隔离强度取决于运行时配置（参见 gVisor 文档 D41）"),
    ("工具执行", "高影响操作确认、幂等、重试与失败恢复", "规则通过", [("P1008", ["temporalio"]), ("P1006", ["tenacity"]), ("P0806", ["libs/checkpoint"])], [("P1008", ["tests"])], "", "幂等键设计属于业务实现，上游只提供机制"),
    ("工具执行", "执行结果检查后再反馈模型；日志、审计与回归", "有证据支持", [("P1004", ["worker"]), ("P0504", ["examples"])], [("P0504", ["examples"])], "promptfoo 回归配置", "审计日志需不可篡改存储，上游未提供"),
]
