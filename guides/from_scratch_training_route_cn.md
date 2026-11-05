# 从头训练路线（路线 A）

> 标记说明：〔上游〕= 上游快照中的文件明确写明；〔建议〕= 本轮自行整理的建议；〔未验证〕= 命令、配置或兼容性未经运行验证。
> 本轮未安装依赖、未运行任何上游代码，所列项目最高为 L1；不构成生产就绪结论。环节级验收条件与入口文件见 `end_to_end_coverage_cn.csv`，跨仓库组合的证据见 `compatibility_matrix_cn.csv`，项目入口说明见 `project_cards/<编号>_cn.md`。

## 项目目标

理解并复现从分词器到预训练、后训练、评测、对话服务的完整流程；先在 CPU/单卡上跑缩小版，再迁移到多卡工程框架。〔建议〕教学示例不得作为生产模型训练方案。

## 模块组合

01 基础：micrograd（P0101）→ minbpe（P0102）→ LLMs-from-scratch（P0103）→ nanoGPT（P0105，复用）→ nanochat（P0104，全流程）；02 数据：datatrove（P0201）、dolma（P0205）；03 预训练：torchtitan（P0301）、Megatron-LM（P0302）、OLMo-core（P0303）、litgpt（P0304）；05 评测：lm-eval（P0501）；排障：ml-engineering（P0305）。

## 资料和源码路径

foundations/、data/、training/ 下的 *_src_en.tar；课程 CS336 讲义与作业（papers_books_courses/courses/，复用 C01–C03）、CS224N、SLP3、Foundations of LLMs、How to Scale Your Model（B08）；论文 papers_books_courses/papers/01、02、03。

## 环境

〔上游〕nanochat：`uv sync --extra cpu` 或 `--extra gpu`（README.md:35–36），README.md:81 提到 8XA100 节点可运行但更慢；torchtitan 需 PyTorch nightly 与 Python 3.11+（README.md:60）。〔建议〕先用 nanochat `runs/runcpu.sh` 做 CPU 缩小验证。

## 数据格式

〔上游〕nanochat 预训练数据为 parquet 分片，`nanochat/dataset.py` 中 BASE_URL 指向 HF 数据集 karpathy/climbmix-400b-shuffle，运行时按需下载；datatrove 处理 JSONL/parquet 文档。

## 配置

nanochat 的 `runs/*.sh`（speedrun.sh、runcpu.sh、scaling_laws.sh）；torchtitan `torchtitan/config`；Megatron-Core 命令行参数；OLMo-core 训练脚本配置。

## 执行顺序

〔建议〕1 读 CS336 讲义并完成 minbpe/micrograd 测试 → 2 LLMs-from-scratch 章节代码 → 3 nanochat CPU 示例 → 4 datatrove 小样本去重过滤 → 5 torchtitan 单机调试配置 → 6 多机前阅读 ml-engineering 的故障排查章节。

## 测试方法

minbpe `pytest -v .`（README 命令）；nanochat `tests/`；torchtitan `tests/`；训练产物用 lm-eval 自定义任务评测。〔未验证〕

## 部署步骤

〔上游〕nanochat 本快照提供命令行对话脚本 scripts/chat_cli.py 与推理基准 scripts/infer_bench.py（未见网页对话脚本），仅用于演示；正式服务转入路线 4 的 vLLM 部署。

## 外部依赖

预训练语料（HF，体积大，未下载）；GPU；共享存储与高速网络（多机）。

## 尚未解决的问题

所有项目均为 L1/L0，未运行；预训练语料与算力未准备；数据配比与训练—评测隔离需按 02 模块自行实施。
