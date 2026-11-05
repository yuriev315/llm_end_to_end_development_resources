# 训练层面的模型对齐 与 请求时的运行时控制：区别与登记

> 两类资料分开登记。提示模板、关键词过滤、规则引擎、护栏配置都属于**运行时控制**，不能称为“已完成模型对齐”。反过来，做过对齐训练的模型也仍然需要运行时控制。本文件只做静态整理，所列项目均未运行。

## 1. 定义

| | A. 请求时的指令组织与运行时控制 | B. 模型训练层面的对齐 |
|---|---|---|
| 作用对象 | 单次请求的输入、上下文与输出 | 模型参数 |
| 生效方式 | 改变模型看到的内容，或拦截/修正模型输出 | 改变模型在任意输入下的行为倾向 |
| 典型手段 | 系统/开发者/用户指令分层、提示模板、上下文预算与压缩、检索内容边界、工具 Schema、约束解码、输入/输出分类器、规则引擎、权限检查、人工审核 | 指令微调（SFT）、偏好数据、奖励模型、DPO/KTO/SimPO 等偏好优化、PPO/GRPO 等强化学习、蒸馏、针对指令层级或注入的对抗训练 |
| 变更成本 | 低，可热更新，需回归 | 高，需训练、评测、发布与回滚 |
| 失效方式 | 被绕过（注入、越狱、编码混淆）；规则误报或漏报 | 泛化不足、奖励被钻空子、能力退化、过度拒答 |
| 证明有效的方式 | 针对该控制点的测试集（误报/漏报、注入成功率）与端到端回归 | 训练前后在有用性、准确性、安全性、领域行为评测上的对比（含置信区间） |

## 2. A 类资料（运行时控制）

| 主题 | 本库条目 |
|---|---|
| 指令层级与行为规范 | P1215 openai/model_spec；OWASP LLM Top 10（D1201）；NIST AI 600-1（G01） |
| 护栏框架 | P1204 NeMo Guardrails、P1205 Guardrails AI、P1207 llm-guard（上游已归档） |
| 输入/输出分类器（作为运行时组件使用） | P1206 Llama Guard / Prompt Guard / LlamaFirewall、P1227 WildGuard |
| 注入防护的系统设计 | P1210 CaMeL；论文 2403.14720 Spotlighting、2503.18813 Defeating Prompt Injections by Design |
| 上下文组织与压缩 | P1216 LLMLingua、P0811 OpenHands SDK context |
| 结构化输出与校验 | P0605 xgrammar、P0604 Outlines、P1217 instructor、P1218 pydantic、P1219 jsonschema |
| 路由 | P1209 semantic-router、P1208 RouteLLM |
| 权限 | P1214 OpenFGA |

注意：Llama Guard、WildGuard 本身是经过训练的模型，但**部署成过滤器时**属于运行时控制；它们的存在不代表被保护的主模型已经对齐。

## 3. B 类资料（训练对齐）

| 主题 | 本库条目 |
|---|---|
| 训练框架 | P0401 TRL（SFT/DPO/奖励模型/GRPO，GKD 在 `trl/experimental/gkd`）、P0402 PEFT、P0403 LLaMA-Factory、P0404 verl、P0304 litgpt、P0103 LLMs-from-scratch（教学，含 DPO） |
| 偏好/合成数据与标注 | P0203 distilabel、P0204 Argilla、P0206 Label Studio |
| 奖励模型评测 | 论文 2403.13787 RewardBench；2406.08673 HelpSteer2 |
| 方法论文 | 2203.02155 InstructGPT、2305.18290 DPO、2402.01306 KTO、2405.14734 SimPO、2402.03300 GRPO、2501.12948 DeepSeek-R1、2411.15124 Tülu 3、2306.13649 GKD |
| 面向安全行为的训练 | 论文 2404.13208 Instruction Hierarchy、2402.06363 StruQ、2410.05451 SecAlign、2406.18510 WildTeaming |
| 对齐效果评测 | 有用性/指令遵循：2311.07911 IFEval、2404.04475 AlpacaEval LC；准确性：lm-eval（P0501）、HELM（P0506）；安全性：HarmBench（P1225）、XSTest（P1229）、JailbreakBench（P1226）；领域：HealthBench（P0507）、MedHELM（P0506）、MIRAGE（P1102） |

## 4. 登记规则（本库执行）

1. `validation_matrix_cn.csv` 中每个检查项都标明“通过时能证明的层级”；凡属 A 类的条目，结论只写“该运行时控制通过某测试”，不写“模型已对齐”。
2. 声称模型对齐改进时，必须同时给出：训练数据版本、基座版本与许可、训练配置、评测集版本、对比基线及统计误差（参见论文 2411.00640）。本轮没有进行任何训练，因此**本库目前没有任何“已完成对齐”的结论**。
3. 两类手段叠加时（例如对齐模型 + 输出分类器），评测需要分别报告单独效果与叠加效果，避免把护栏的拦截率算成模型本身的安全性。
