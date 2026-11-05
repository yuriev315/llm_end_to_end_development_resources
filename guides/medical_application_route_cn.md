# 医疗应用参考路线（研究与教学用途）

> 标记说明：〔上游〕= 上游快照中的文件明确写明；〔建议〕= 本轮自行整理的建议；〔未验证〕= 命令、配置或兼容性未经运行验证。
> 本轮未安装依赖、未运行任何上游代码，所列项目最高为 L1；不构成生产就绪结论。环节级验收条件与入口文件见 `end_to_end_coverage_cn.csv`，跨仓库组合的证据见 `compatibility_matrix_cn.csv`，项目入口说明见 `project_cards/<编号>_cn.md`。

## 项目目标

医学文献/教材问答检索与评测原型。〔建议〕明确用途：研究、教学、内部文献检索辅助；**不用于诊断、治疗决策或患者直接使用**；没有任何条目经过临床验证或监管审批。

## 模块组合

MedRAG（P1101）+ MIRAGE（P1102）+ medspaCy（P1106）+ fhir.resources（P1107）+ pint（P1108）+ MedCalc-Bench 计算器（P1105）+ HealthBench（P0507）+ Argilla（P0204，专家评价）+ LangGraph 中断（P0806，人工接管）。适配训练参考：MedGemma 笔记本（P1103，权重另有条款）。

## 资料和源码路径

applications/（11）；指南 G05（WHO 大型多模态模型伦理与治理指南 2024）、G01（NIST AI 600-1）；论文 papers_books_courses/papers/11（Med-PaLM 2、MedRAG、MEDITRON、HealthBench、MedCalc-Bench、AMIE、AgentClinic、Med-HALT 等）。

## 环境

〔上游〕MedRAG 首次初始化时自动下载预计算嵌入（README.md:16），语料体积大；生成模型示例含 Mixtral、Llama-2、Meditron（需 GPU 或 API）。

## 数据格式

MIRAGE `benchmark.json`（题目、选项、答案）；MedCalc-Bench 样本（笔记、计算器、答案上下限，README.md:44–45）；FHIR 资源 JSON。

## 配置

MedRAG 初始化参数（检索器、语料、corpus_cache）；无独立配置文件（仓库无依赖声明，L0）。

## 执行顺序

〔建议〕1 用 MIRAGE 评测基线 → 2 接入 MedRAG 检索 → 3 计算类问题改为工具计算（pint + 计算器实现）→ 4 输出记录“工具计算值/模型文本/专家结论”三类来源 → 5 Argilla 专家评审 → 6 高风险转人工。

## 测试方法

MIRAGE 准确率；MedCalc-Bench 上下限判定；HealthBench 评分细则；Med-HALT 幻觉测试（论文）。〔未验证〕

## 部署步骤

仅限隔离研究环境；不建议面向患者部署。

## 外部依赖

UMLS/SNOMED CT/LOINC/RxNorm 术语库（需许可/注册，未下载）；医学语料；临床专家。

## 尚未解决的问题

FDA CDS 指南与 GMLP 原则下载 403 未收录；带版本号的临床指南库缺失；HuatuoGPT-II 因无许可证被排除；MedCalc-Bench 代码许可未单独声明。
