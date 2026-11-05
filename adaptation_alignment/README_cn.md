# adaptation_alignment/ 模块索引（04 适配与对齐）

外层归档为本库命名（含 _en 语言后缀）；解包后内部保持上游原始路径。每个项目的中文入口说明见 project_cards/<编号>_cn.md。

## 存放于本目录的项目

| 编号 | 项目 | 版本 | 路线 | 角色 | 等级 | 归档 |
|---|---|---|---|---|---|---|
| P0401 | huggingface/trl | v1.17.0 | B | 单模块参考 | L1 | `P0401_huggingface_trl_v1.17.0_src_en.tar` |
| P0402 | huggingface/peft | v0.21.2 | B | 单模块参考 | L1 | `P0402_huggingface_peft_v0.21.2_src_en.tar` |
| P0403 | hiyouga/LLaMA-Factory | v0.9.5 | B | 完整工程 | L1 | `P0403_hiyouga_LLaMA-Factory_v0.9.5_src_en.tar` |
| P0404 | volcengine/verl | v0.9.1 | B | 完整工程 | L1 | `P0404_volcengine_verl_v0.9.1_src_en.tar` |

## 跨模块关联项目（只保存一份，存放在其主模块目录）

| 编号 | 项目 | 存放位置 | 用途 |
|---|---|---|---|
| P0103 | rasbt/LLMs-from-scratch | `foundations/P0103_rasbt_LLMs-from-scratch_main-cdbd33e6d5_src_en.tar` | 从零实现 GPT：注意力、预训练、分类与指令微调、DPO（配套书籍代码） |
| P0104 | karpathy/nanochat | `foundations/P0104_karpathy_nanochat_master-92d63d4e8b_src_en.tar` | 小规模全流程：分词器→预训练→SFT→RL→评测→命令行对话（scripts/chat_cli.py） |
| P0203 | argilla-io/distilabel | `data/P0203_argilla-io_distilabel_1.5.3_src_en.tar` | 合成数据与 AI 反馈流水线（指令、偏好数据生成） |
| P0204 | argilla-io/argilla | `data/P0204_argilla-io_argilla_v2.8.0_src_en.tar` | 人工标注与专家审核平台（数据集版本、审核工作流、Docker 部署） |
| P0207 | iterative/dvc | `data/P0207_iterative_dvc_3.67.1_src_en.tar` | 数据与模型版本管理、流水线与实验追踪（数据—模型—配置关联） |
| P0302 | NVIDIA/Megatron-LM | `training/P0302_NVIDIA_Megatron-LM_core_v0.19.2_src_en.tar` | Megatron-Core 大规模分布式训练（张量/流水/专家并行、分布式检查点） |
| P0304 | Lightning-AI/litgpt | `training/P0304_Lightning-AI_litgpt_v0.5.13_src_en.tar` | 预训练/继续预训练/微调/LoRA/评测/服务一体化，YAML 配置 |
| P0501 | EleutherAI/lm-evaluation-harness | `evaluation/P0501_EleutherAI_lm-evaluation-harness_v0.4.13_src_en.tar` | 离线基准评测框架，YAML 自定义任务，去污染工具 |
| P0602 | ggml-org/llama.cpp | `inference/P0602_ggml-org_llama.cpp_b11986_src_en.tar` | CPU/GPU 本地推理、GGUF 转换与量化、HTTP 服务、语法约束输出 |
| P0606 | vllm-project/llm-compressor | `inference/P0606_vllm-project_llm-compressor_0.15.0_src_en.tar` | 训练后量化/稀疏化并导出 vLLM 可加载格式 |
| P0706 | FlagOpen/FlagEmbedding | `rag/P0706_FlagOpen_FlagEmbedding_v1.4.2_src_en.tar` | BGE 嵌入与重排序模型的推理、微调、评测代码 |
| P1103 | Google-Health/medgemma | `applications/P1103_Google-Health_medgemma_main-a60a66024f_src_en.tar` | MedGemma 官方笔记本：推理、微调示例（权重另有使用条款） |
| P1117 | SWE-bench/SWE-smith | `applications/P1117_SWE-bench_SWE-smith_v0.0.6_src_en.tar` | Coding 智能体训练数据合成（任务实例生成、轨迹） |

## 本模块论文（22 篇，存放于 papers_books_courses/papers/<模块编号>/）

- Distilling the Knowledge in a Neural Network（arXiv 1503.02531v1；`papers_books_courses/papers/04/2015_Hinton_DistillingKnowledgeNeuralNetwork_en.pdf`）
- LoRA: Low-Rank Adaptation of Large Language Models（arXiv 2106.09685v2；`papers_books_courses/papers/04/2021_Hu_LoraLowRankAdaptationLarge_en.pdf`）
- Training language models to follow instructions with human feedback（arXiv 2203.02155v1；`papers_books_courses/papers/04/2022_Ouyang_TrainingLanguageModelsFollowInstructions_en.pdf`）
- On-Policy Distillation of Language Models: Learning from Self-Generated Mistakes（arXiv 2306.13649v3；`papers_books_courses/papers/04/2023_Agarwal_PolicyDistillationLanguageModelsLearning_en.pdf`）
- QLoRA: Efficient Finetuning of Quantized LLMs（arXiv 2305.14314v1；`papers_books_courses/papers/04/2023_Dettmers_QloraEfficientFinetuningQuantizedLlms_en.pdf`）
- Direct Preference Optimization: Your Language Model is Secretly a Reward Model（arXiv 2305.18290v3；`papers_books_courses/papers/04/2023_Rafailov_DirectPreferenceOptimizationLanguageModel_en.pdf`）
- Back to Basics: Revisiting REINFORCE Style Optimization for Learning from Human Feedback in LLMs（arXiv 2402.14740v2；`papers_books_courses/papers/04/2024_Ahmadian_BackBasicsRevisitingReinforceStyle_en.pdf`）
- LoRA Learns Less and Forgets Less（arXiv 2405.09673v2；`papers_books_courses/papers/04/2024_Biderman_LoraLearnsLessForgetsLess_en.pdf`）
- KTO: Model Alignment as Prospect Theoretic Optimization（arXiv 2402.01306v5；`papers_books_courses/papers/04/2024_Ethayarajh_KtoModelAlignmentProspectTheoretic_en.pdf`）
- Simple and Scalable Strategies to Continually Pre-train Large Language Models（arXiv 2403.08763v4；`papers_books_courses/papers/04/2024_Ibrahim_SimpleScalableStrategiesContinuallyPre_en.pdf`）
- RewardBench: Evaluating Reward Models for Language Modeling（arXiv 2403.13787v2；`papers_books_courses/papers/04/2024_Lambert_RewardbenchEvaluatingRewardModelsLanguage_en.pdf`）
- Tulu 3: Pushing Frontiers in Open Language Model Post-Training（arXiv 2411.15124v5；`papers_books_courses/papers/04/2024_Lambert_Tulu3PushingFrontiersOpen_en.pdf`）
- DoRA: Weight-Decomposed Low-Rank Adaptation（arXiv 2402.09353v6；`papers_books_courses/papers/04/2024_Liu_DoraWeightDecomposedLowRank_en.pdf`）
- SimPO: Simple Preference Optimization with a Reference-Free Reward（arXiv 2405.14734v3；`papers_books_courses/papers/04/2024_Meng_SimpoSimplePreferenceOptimizationReference_en.pdf`）
- Compact Language Models via Pruning and Knowledge Distillation（arXiv 2407.14679v2；`papers_books_courses/papers/04/2024_Muralidharan_CompactLanguageModelsPruningKnowledge_en.pdf`）
- DeepSeekMath: Pushing the Limits of Mathematical Reasoning in Open Language Models（arXiv 2402.03300v3；`papers_books_courses/papers/04/2024_Shao_DeepseekmathPushingLimitsMathematicalReasoning_en.pdf`）
- HybridFlow: A Flexible and Efficient RLHF Framework（arXiv 2409.19256v2；`papers_books_courses/papers/04/2024_Sheng_HybridflowFlexibleEfficientRlhfFramework_en.pdf`）
- HelpSteer2: Open-source dataset for training top-performing reward models（arXiv 2406.08673v1；`papers_books_courses/papers/04/2024_Wang_Helpsteer2OpenSourceDatasetTraining_en.pdf`）
- A Survey on Knowledge Distillation of Large Language Models（arXiv 2402.13116v4；`papers_books_courses/papers/04/2024_Xu_SurveyKnowledgeDistillationLargeLanguage_en.pdf`）
- LlamaFactory: Unified Efficient Fine-Tuning of 100+ Language Models（arXiv 2403.13372v4；`papers_books_courses/papers/04/2024_Zheng_LlamafactoryUnifiedEfficientFineTuning_en.pdf`）
- DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning（arXiv 2501.12948v2；`papers_books_courses/papers/04/2025_DeepSeekAI_DeepseekR1IncentivizingReasoningCapability_en.pdf`）
- DAPO: An Open-Source LLM Reinforcement Learning System at Scale（arXiv 2503.14476v2；`papers_books_courses/papers/04/2025_Yu_DapoOpenSourceLlmReinforcement_en.pdf`）
