# training/ 模块索引（03 预训练）

外层归档为本库命名（含 _en 语言后缀）；解包后内部保持上游原始路径。每个项目的中文入口说明见 project_cards/<编号>_cn.md。

## 存放于本目录的项目

| 编号 | 项目 | 版本 | 路线 | 角色 | 等级 | 归档 |
|---|---|---|---|---|---|---|
| P0301 | pytorch/torchtitan | v0.4.0 | A | 单模块参考 | L1 | `P0301_pytorch_torchtitan_v0.4.0_src_en.tar` |
| P0302 | NVIDIA/Megatron-LM | core_v0.19.2 | A,B | 完整工程 | L1 | `P0302_NVIDIA_Megatron-LM_core_v0.19.2_src_en.tar` |
| P0303 | allenai/OLMo-core | v3.0.0 | A | 完整工程 | L1 | `P0303_allenai_OLMo-core_v3.0.0_src_en.tar` |
| P0304 | Lightning-AI/litgpt | v0.5.13 | A,B | 完整工程 | L1 | `P0304_Lightning-AI_litgpt_v0.5.13_src_en.tar` |
| P0305 | stas00/ml-engineering | master@adab2fa873 | A,B | 运行手册 | L0 | `P0305_stas00_ml-engineering_master-adab2fa873_src_en.tar` |

## 跨模块关联项目（只保存一份，存放在其主模块目录）

| 编号 | 项目 | 存放位置 | 用途 |
|---|---|---|---|
| P0104 | karpathy/nanochat | `foundations/P0104_karpathy_nanochat_master-92d63d4e8b_src_en.tar` | 小规模全流程：分词器→预训练→SFT→RL→评测→命令行对话（scripts/chat_cli.py） |
| P0201 | huggingface/datatrove | `data/P0201_huggingface_datatrove_v0.10.1_src_en.tar` | 大规模文本处理：抽取、语言识别、质量过滤、MinHash 去重、分词统计 |
| P0205 | allenai/dolma | `data/P0205_allenai_dolma_v1.2.1_src_en.tar` | 预训练语料工具：打标、布隆过滤去重、混合配比 |
| P0501 | EleutherAI/lm-evaluation-harness | `evaluation/P0501_EleutherAI_lm-evaluation-harness_v0.4.13_src_en.tar` | 离线基准评测框架，YAML 自定义任务，去污染工具 |

## 本模块论文（21 篇，存放于 papers_books_courses/papers/<模块编号>/）

- Decoupled Weight Decay Regularization（arXiv 1711.05101v3；`papers_books_courses/papers/03/2017_Loshchilov_DecoupledWeightDecayRegularization_en.pdf`）
- Mixed Precision Training（arXiv 1710.03740v3；`papers_books_courses/papers/03/2017_Micikevicius_MixedPrecisionTraining_en.pdf`）
- ZeRO: Memory Optimizations Toward Training Trillion Parameter Models（arXiv 1910.02054v3；`papers_books_courses/papers/03/2019_Rajbhandari_ZeROMemoryOptimizationsTowardTraining_en.pdf`）
- Megatron-LM: Training Multi-Billion Parameter Language Models Using Model Parallelism（arXiv 1909.08053v4；`papers_books_courses/papers/03/2019_Shoeybi_MegatronLmTrainingMultiBillion_en.pdf`）
- Efficient Large-Scale Language Model Training on GPU Clusters Using Megatron-LM（arXiv 2104.04473v5；`papers_books_courses/papers/03/2021_Narayanan_EfficientLargeScaleLanguageModel_en.pdf`）
- FlashAttention-2: Faster Attention with Better Parallelism and Work Partitioning（arXiv 2307.08691v1；`papers_books_courses/papers/03/2023_Dao_FlashAttention2FasterAttentionBetter_en.pdf`）
- DeepSpeed Ulysses: System Optimizations for Enabling Training of Extreme Long Sequence Transformer Models（arXiv 2309.14509v2；`papers_books_courses/papers/03/2023_Jacobs_DeepspeedUlyssesSystemOptimizationsEnabling_en.pdf`）
- FP8-LM: Training FP8 Large Language Models（arXiv 2310.18313v2；`papers_books_courses/papers/03/2023_Peng_Fp8LmTrainingFp8Large_en.pdf`）
- Zero Bubble Pipeline Parallelism（arXiv 2401.10241v1；`papers_books_courses/papers/03/2023_Qi_ZeroBubblePipelineParallelism_en.pdf`）
- Spike No More: Stabilizing the Pre-training of Large Language Models（arXiv 2312.16903v4；`papers_books_courses/papers/03/2023_Takase_SpikeNoMoreStabilizingPre_en.pdf`）
- Small-scale proxies for large-scale Transformer training instabilities（arXiv 2309.14322v2；`papers_books_courses/papers/03/2023_Wortsman_SmallScaleProxiesLargeScale_en.pdf`）
- PyTorch FSDP: Experiences on Scaling Fully Sharded Data Parallel（arXiv 2304.11277v2；`papers_books_courses/papers/03/2023_Zhao_PyTorchFSDPExperiencesScalingFully_en.pdf`）
- Scaling FP8 training to trillion-token LLMs（arXiv 2409.12517v2；`papers_books_courses/papers/03/2024_Fishman_ScalingFp8TrainingTrillionToken_en.pdf`）
- Scaling Laws and Compute-Optimal Training Beyond Fixed Training Durations（arXiv 2405.18392v3；`papers_books_courses/papers/03/2024_Hgele_ScalingLawsComputeOptimalTraining_en.pdf`）
- MiniCPM: Unveiling the Potential of Small Language Models with Scalable Training Strategies（arXiv 2404.06395v3；`papers_books_courses/papers/03/2024_Hu_MinicpmUnveilingPotentialSmallLanguage_en.pdf`）
- MegaScale: Scaling Large Language Model Training to More Than 10,000 GPUs（arXiv 2402.15627v1；`papers_books_courses/papers/03/2024_Jiang_MegascaleScalingLargeLanguageModel_en.pdf`）
- Revisiting Reliability in Large-Scale Machine Learning Research Clusters（arXiv 2410.21680v2；`papers_books_courses/papers/03/2024_Kokolis_RevisitingReliabilityLargeScaleMachine_en.pdf`）
- TorchTitan: One-stop PyTorch native solution for production ready LLM pre-training（arXiv 2410.06511v3；`papers_books_courses/papers/03/2024_Liang_TorchTitanOneStopPyTorchNative_en.pdf`）
- FlashAttention-3: Fast and Accurate Attention with Asynchrony and Low-precision（arXiv 2407.08608v2；`papers_books_courses/papers/03/2024_Shah_FlashAttention3FastAccurateAttention_en.pdf`）
- ByteCheckpoint: A Unified Checkpointing System for Large Foundation Model Development（arXiv 2407.20143v4；`papers_books_courses/papers/03/2024_Wan_BytecheckpointUnifiedCheckpointingSystemLarge_en.pdf`）
- Muon is Scalable for LLM Training（arXiv 2502.16982v1；`papers_books_courses/papers/03/2025_Liu_MuonScalableLlmTraining_en.pdf`）
