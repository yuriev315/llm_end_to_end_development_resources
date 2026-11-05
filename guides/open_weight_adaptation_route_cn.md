# 开放权重模型适配路线（路线 B）

> 标记说明：〔上游〕= 上游快照中的文件明确写明；〔建议〕= 本轮自行整理的建议；〔未验证〕= 命令、配置或兼容性未经运行验证。
> 本轮未安装依赖、未运行任何上游代码，所列项目最高为 L1；不构成生产就绪结论。环节级验收条件与入口文件见 `end_to_end_coverage_cn.csv`，跨仓库组合的证据见 `compatibility_matrix_cn.csv`，项目入口说明见 `project_cards/<编号>_cn.md`。

## 项目目标

在开放权重基座上做持续预训练、SFT、参数高效微调、偏好优化/强化学习或蒸馏，并完成评测、量化与发布。

## 模块组合

组合 A：TRL v1.17.0（P0401）+ PEFT v0.21.2（P0402）+ vLLM v0.32.0（P0601）+ lm-eval v0.4.13（P0501）。组合 B：LLaMA-Factory v0.9.5（P0403，需其自身旧版本依赖）。RL：verl v0.9.1（P0404，独立环境）。数据：Argilla、Label Studio、distilabel、datatrove；量化：llm-compressor（P0606）、llama.cpp（P0602）。

## 资料和源码路径

adaptation_alignment/、data/、evaluation/、inference/；文档 TRL/PEFT/Transformers/Accelerate（D03、D06–D08）；论文 papers_books_courses/papers/04；详细组合见 reference_stacks_cn.md 路线 4。

## 环境

〔上游〕TRL 要求 Python ≥3.11、torch>=2.6.0；LLaMA-Factory 要求 Python ≥3.11、torch>=2.4.0；verl 要求 Python >=3.10,<3.13（各自 pyproject.toml）。〔建议〕两套组合分别建独立虚拟环境或容器。

## 数据格式

〔上游〕LLaMA-Factory `data/dataset_info.json` 注册数据集，示例 `alpaca_en_demo.json`（指令）、`dpo_en_demo.json`（偏好）、`glaive_toolcall_en_demo.json`（工具调用）、`kto_en_demo.json`；TRL 使用 messages / prompt-completion / chosen-rejected 格式。

## 配置

LLaMA-Factory `examples/train_lora/`、`examples/train_qlora/`、`examples/merge_lora/`；TRL 配置类；verl `examples/`。

## 执行顺序

数据采集与标注 → 去重与去污染 → 基座与许可登记（含 revision）→ 训练配置 → 小样本试训 → 正式训练与检查点 → 评测（通用 + 安全 + 领域）→ 合并/量化 → vLLM 部署 → 回归与灰度。

## 测试方法

trl/peft/LLaMA-Factory `tests/`；lm-eval 任务与去污染；HarmBench/XSTest 安全回归；量化前后精度对比。〔未验证〕

## 部署步骤

vLLM 加载合并模型或 LoRA 适配器；production-stack Helm（默认引擎镜像 tag 为 latest，需固定）；KServe 灰度。

## 外部依赖

基座权重与许可（未下载）；GPU 显存（LLaMA-Factory README.md:490 起有显存表，上游原文）；评测数据集。

## 尚未解决的问题

LLaMA-Factory 与本库 TRL/PEFT/vLLM 版本约束冲突；verl 固定 vllm==0.24.0；数据—模型—分词器—提示—适配器版本关联无一体化参考。
