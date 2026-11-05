# inference/ 模块索引（06 推理与服务）

外层归档为本库命名（含 _en 语言后缀）；解包后内部保持上游原始路径。每个项目的中文入口说明见 project_cards/<编号>_cn.md。

## 存放于本目录的项目

| 编号 | 项目 | 版本 | 路线 | 角色 | 等级 | 归档 |
|---|---|---|---|---|---|---|
| P0601 | vllm-project/vllm | v0.32.0 | B,C | 完整工程 | L1 | `P0601_vllm-project_vllm_v0.32.0_src_en.tar` |
| P0602 | ggml-org/llama.cpp | b11986 | B,C | 完整工程 | L1 | `P0602_ggml-org_llama.cpp_b11986_src_en.tar` |
| P0603 | sgl-project/sglang | v0.5.22 | B,C | 完整工程 | L1 | `P0603_sgl-project_sglang_v0.5.22_src_en.tar` |
| P0604 | dottxt-ai/outlines | 1.3.3 | C | 单模块参考 | L1 | `P0604_dottxt-ai_outlines_1.3.3_src_en.tar` |
| P0605 | mlc-ai/xgrammar | v0.2.8 | C | 单模块参考 | L1 | `P0605_mlc-ai_xgrammar_v0.2.8_src_en.tar` |
| P0606 | vllm-project/llm-compressor | 0.15.0 | B | 单模块参考 | L1 | `P0606_vllm-project_llm-compressor_0.15.0_src_en.tar` |
| P0607 | vllm-project/guidellm | v0.8.1 | B,C | 单模块参考 | L1 | `P0607_vllm-project_guidellm_v0.8.1_src_en.tar` |

## 跨模块关联项目（只保存一份，存放在其主模块目录）

| 编号 | 项目 | 存放位置 | 用途 |
|---|---|---|---|
| P0104 | karpathy/nanochat | `foundations/P0104_karpathy_nanochat_master-92d63d4e8b_src_en.tar` | 小规模全流程：分词器→预训练→SFT→RL→评测→命令行对话（scripts/chat_cli.py） |
| P0304 | Lightning-AI/litgpt | `training/P0304_Lightning-AI_litgpt_v0.5.13_src_en.tar` | 预训练/继续预训练/微调/LoRA/评测/服务一体化，YAML 配置 |
| P0403 | hiyouga/LLaMA-Factory | `adaptation_alignment/P0403_hiyouga_LLaMA-Factory_v0.9.5_src_en.tar` | 统一微调框架：数据格式、SFT/DPO/KTO/PPO、导出合并、API 服务、Docker |
| P1001 | vllm-project/production-stack | `deployment_operations/P1001_vllm-project_production-stack_vllm-stack-0.1.13_src_en.tar` | vLLM 生产部署：Helm、路由、KV 缓存复用、Prometheus/Grafana 监控 |
| P1002 | kserve/kserve | `deployment_operations/P1002_kserve_kserve_v0.21.0_src_en.tar` | Kubernetes 模型服务：InferenceService、灰度、扩缩容 |

## 本模块论文（20 篇，存放于 papers_books_courses/papers/<模块编号>/）

- GPTQ: Accurate Post-Training Quantization for Generative Pre-trained Transformers（arXiv 2210.17323v2；`papers_books_courses/papers/06/2022_Frantar_GptqAccuratePostTrainingQuantization_en.pdf`）
- Fast Inference from Transformers via Speculative Decoding（arXiv 2211.17192v2；`papers_books_courses/papers/06/2022_Leviathan_FastInferenceFromTransformersSpeculative_en.pdf`）
- Efficient Memory Management for Large Language Model Serving with PagedAttention（arXiv 2309.06180v1；`papers_books_courses/papers/06/2023_Kwon_EfficientMemoryManagementLargeLanguage_en.pdf`）
- AWQ: Activation-aware Weight Quantization for LLM Compression and Acceleration（arXiv 2306.00978v6；`papers_books_courses/papers/06/2023_Lin_AwqActivationAwareWeightQuantization_en.pdf`）
- Fairness in Serving Large Language Models（arXiv 2401.00588v2；`papers_books_courses/papers/06/2023_Sheng_FairnessServingLargeLanguageModels_en.pdf`）
- S-LoRA: Serving Thousands of Concurrent LoRA Adapters（arXiv 2311.03285v3；`papers_books_courses/papers/06/2023_Sheng_SLoraServingThousandsConcurrent_en.pdf`）
- Efficient Guided Generation for Large Language Models（arXiv 2307.09702v4；`papers_books_courses/papers/06/2023_Willard_EfficientGuidedGenerationLargeLanguage_en.pdf`）
- Efficient Streaming Language Models with Attention Sinks（arXiv 2309.17453v4；`papers_books_courses/papers/06/2023_Xiao_EfficientStreamingLanguageModelsAttention_en.pdf`）
- SGLang: Efficient Execution of Structured Language Model Programs（arXiv 2312.07104v2；`papers_books_courses/papers/06/2023_Zheng_SGLangEfficientExecutionStructuredLanguage_en.pdf`）
- Taming Throughput-Latency Tradeoff in LLM Inference with Sarathi-Serve（arXiv 2403.02310v3；`papers_books_courses/papers/06/2024_Agrawal_TamingThroughputLatencyTradeoffLLM_en.pdf`）
- Vidur: A Large-Scale Simulation Framework For LLM Inference（arXiv 2405.05465v2；`papers_books_courses/papers/06/2024_Agrawal_VidurLargeScaleSimulationFramework_en.pdf`）
- QuaRot: Outlier-Free 4-Bit Inference in Rotated LLMs（arXiv 2404.00456v2；`papers_books_courses/papers/06/2024_Ashkboos_QuarotOutlierFree4Bit_en.pdf`）
- Medusa: Simple LLM Inference Acceleration Framework with Multiple Decoding Heads（arXiv 2401.10774v3；`papers_books_courses/papers/06/2024_Cai_MedusaSimpleLlmInferenceAcceleration_en.pdf`）
- XGrammar: Flexible and Efficient Structured Generation Engine for Large Language Models（arXiv 2411.15100v3；`papers_books_courses/papers/06/2024_Dong_XgrammarFlexibleEfficientStructuredGeneration_en.pdf`）
- EAGLE: Speculative Sampling Requires Rethinking Feature Uncertainty（arXiv 2401.15077v3；`papers_books_courses/papers/06/2024_Li_EagleSpeculativeSamplingRequiresRethinking_en.pdf`）
- KIVI: A Tuning-Free Asymmetric 2bit Quantization for KV Cache（arXiv 2402.02750v2；`papers_books_courses/papers/06/2024_Liu_KiviTuningFreeAsymmetric2bit_en.pdf`）
- Mooncake: A KVCache-centric Disaggregated Architecture for LLM Serving（arXiv 2407.00079v5；`papers_books_courses/papers/06/2024_Qin_MooncakeKVCacheCentricDisaggregatedArchitecture_en.pdf`）
- DistServe: Disaggregating Prefill and Decoding for Goodput-optimized Large Language Model Serving（arXiv 2401.09670v3；`papers_books_courses/papers/06/2024_Zhong_DistServeDisaggregatingPrefillDecodingGoodput_en.pdf`）
- A Survey on Efficient Inference for Large Language Models（arXiv 2404.14294v3；`papers_books_courses/papers/06/2024_Zhou_SurveyEfficientInferenceLargeLanguage_en.pdf`）
- FlashInfer: Efficient and Customizable Attention Engine for LLM Inference Serving（arXiv 2501.01005v2；`papers_books_courses/papers/06/2025_Ye_FlashinferEfficientCustomizableAttentionEngine_en.pdf`）
