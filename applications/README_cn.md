# applications/ 模块索引（09 对话与业务产品、11 专业应用）

外层归档为本库命名（含 _en 语言后缀）；解包后内部保持上游原始路径。每个项目的中文入口说明见 project_cards/<编号>_cn.md。

## 存放于本目录的项目

| 编号 | 项目 | 版本 | 路线 | 角色 | 等级 | 归档 |
|---|---|---|---|---|---|---|
| P0901 | danny-avila/LibreChat | v0.8.8 | C | 完整工程 | L0 | `P0901_danny-avila_LibreChat_v0.8.8_src_en.tar` |
| P0902 | huggingface/chat-ui | v0.10.0 | C | 完整工程 | L1 | `P0902_huggingface_chat-ui_v0.10.0_src_en.tar` |
| P0903 | open-webui/open-webui | v0.12.5 | C | 完整工程 | L1 | `P0903_open-webui_open-webui_v0.12.5_src_en.tar` |
| P0904 | langgenius/dify | 1.18.0 | C | 完整工程 | L1 | `P0904_langgenius_dify_1.18.0_src_en.tar` |
| P1101 | Teddy-XiongGZ/MedRAG | main@7599a728a2 | C | 研究原型 | L0 | `P1101_Teddy-XiongGZ_MedRAG_main-7599a728a2_src_en.tar` |
| P1102 | Teddy-XiongGZ/MIRAGE | main@392943af99 | C | 评测基准 | L0 | `P1102_Teddy-XiongGZ_MIRAGE_main-392943af99_src_en.tar` |
| P1103 | Google-Health/medgemma | main@a60a66024f | B | 研究原型 | L0 | `P1103_Google-Health_medgemma_main-a60a66024f_src_en.tar` |
| P1105 | ncbi-nlp/MedCalc-Bench | main@20b10f9d66 | C | 评测基准 | L0 | `P1105_ncbi-nlp_MedCalc-Bench_main-20b10f9d66_src_en.tar` |
| P1106 | medspacy/medspacy | 1.3.1 | C | 单模块参考 | L1 | `P1106_medspacy_medspacy_1.3.1_src_en.tar` |
| P1107 | nazrulworld/fhir.resources | 8.3.0 | C | 工具库 | L1 | `P1107_nazrulworld_fhir.resources_8.3.0_src_en.tar` |
| P1108 | hgrecco/pint | 0.26.2 | C | 工具库 | L1 | `P1108_hgrecco_pint_0.26.2_src_en.tar` |
| P1109 | CadQuery/cadquery | v2.8.0 | C | 工具库 | L1 | `P1109_CadQuery_cadquery_v2.8.0_src_en.tar` |
| P1110 | gumyr/build123d | v0.13.0 | C | 工具库 | L1 | `P1110_gumyr_build123d_v0.13.0_src_en.tar` |
| P1111 | neka-nat/freecad-mcp | main@8babe9927c | C | 研究原型 | L1 | `P1111_neka-nat_freecad-mcp_main-8babe9927c_src_en.tar` |
| P1112 | SadilKhan/Text2CAD | main@669a81472e | B | 研究原型 | L1 | `P1112_SadilKhan_Text2CAD_main-669a81472e_src_en.tar` |
| P1113 | filapro/cad-recode | main@03e3262119 | B | 研究原型 | L0 | `P1113_filapro_cad-recode_main-03e3262119_src_en.tar` |
| P1114 | csml-rpi/Foam-Agent | main@ed8db9415e | C | 研究原型 | L1 | `P1114_csml-rpi_Foam-Agent_main-ed8db9415e_src_en.tar` |
| P1115 | midea-ai/SemaPLC | main@fea1b87a11 | C | 研究原型 | L1 | `P1115_midea-ai_SemaPLC_main-fea1b87a11_src_en.tar` |
| P1116 | YuchenXia/LLM4IAS | main@2029d581d4 | C | 研究原型 | L0 | `P1116_YuchenXia_LLM4IAS_main-2029d581d4_src_en.tar` |
| P1117 | SWE-bench/SWE-smith | v0.0.6 | B | 完整工程 | L1 | `P1117_SWE-bench_SWE-smith_v0.0.6_src_en.tar` |

## 跨模块关联项目（只保存一份，存放在其主模块目录）

| 编号 | 项目 | 存放位置 | 用途 |
|---|---|---|---|
| D0601 | openai/openai-openapi | `papers_books_courses/official_docs/D0601_openai_openai-openapi_main-089b14f36d_src_en.tar` | OpenAI API OpenAPI 规范（事实标准的 Chat Completions/Responses 接口，vLLM/LiteLLM 兼容目标） |
| P0104 | karpathy/nanochat | `foundations/P0104_karpathy_nanochat_master-92d63d4e8b_src_en.tar` | 小规模全流程：分词器→预训练→SFT→RL→评测→命令行对话（scripts/chat_cli.py） |
| P0206 | HumanSignal/label-studio | `data/P0206_HumanSignal_label-studio_1.23.2_src_en.tar` | 多模态人工标注平台（图纸/扫描件/文本标注、多人审核、Docker） |
| P0208 | opendatalab/MinerU | `data/P0208_opendatalab_MinerU_mineru-4.1.2-released_src_en.tar` | PDF 解析：表格、公式、扫描件 OCR 到 Markdown/JSON |
| P0506 | stanford-crfm/helm | `evaluation/P0506_stanford-crfm_helm_v0.5.16_src_en.tar` | 整体评测框架（含 MedHELM 医疗场景） |
| P0507 | openai/simple-evals | `evaluation/P0507_openai_simple-evals_main-652c89d0ca_src_en.tar` | 轻量评测实现（含 HealthBench 评分细则评测） |
| P0702 | infiniflow/ragflow | `rag/P0702_infiniflow_ragflow_v0.27.3_src_en.tar` | 完整 RAG 产品：深度文档解析、分块模板、引用、多租户、Docker Compose |
| P0807 | microsoft/multilspy | `agents_coding/P0807_microsoft_multilspy_v0.1.1_src_en.tar` | 面向智能体的语言服务器（LSP）客户端：定义/引用/补全 |
| P0808 | astral-sh/ruff | `agents_coding/P0808_astral-sh_ruff_0.17.3_src_en.tar` | Python 静态检查与格式化（规则集、配置） |
| P0809 | mem0ai/mem0 | `agents_coding/P0809_mem0ai_mem0_v2.2.1_src_en.tar` | 对话记忆层：记忆写入/更新/删除、按用户/会话隔离 |
| P1003 | BerriAI/litellm | `deployment_operations/P1003_BerriAI_litellm_v1.106.6_src_en.tar` | 模型网关：统一接口、密钥/预算/限速、回退、日志 |
| P1214 | openfga/openfga | `input_output_pipeline/P1214_openfga_openfga_v1.22.1_src_en.tar` | 细粒度授权（关系型访问控制，适用于用户/租户/文档权限过滤） |
| P1221 | cure53/DOMPurify | `input_output_pipeline/P1221_cure53_DOMPurify_3.4.17_src_en.tar` | 前端 HTML 净化（防 XSS 的模型输出呈现） |
| P1222 | messense/nh3 | `input_output_pipeline/P1222_messense_nh3_v0.3.7_src_en.tar` | Python 端 HTML 净化（ammonia 绑定） |

## 本模块论文（22 篇，存放于 papers_books_courses/papers/<模块编号>/）

- What Disease does this Patient Have? A Large-scale Open Domain Question Answering Dataset from Medical Exams（arXiv 2009.13081v1；`papers_books_courses/papers/11/2020_Jin_WhatDiseaseDoesThisPatient_en.pdf`）
- HuatuoGPT-II, One-stage Training for Medical Adaption of LLMs（arXiv 2311.09774v2；`papers_books_courses/papers/11/2023_Chen_HuatuogptIiOneStageTraining_en.pdf`）
- MEDITRON-70B: Scaling Medical Pretraining for Large Language Models（arXiv 2311.16079v1；`papers_books_courses/papers/11/2023_Chen_Meditron70bScalingMedicalPretraining_en.pdf`）
- Llama Guard: LLM-based Input-Output Safeguard for Human-AI Conversations（arXiv 2312.06674v1；`papers_books_courses/papers/11/2023_Inan_LlamaGuardLlmBasedInput_en.pdf`）
- How Can Large Language Models Help Humans in Design and Manufacturing?（arXiv 2307.14377v1；`papers_books_courses/papers/11/2023_Makatura_HowCanLargeLanguageModels_en.pdf`）
- Can Generalist Foundation Models Outcompete Special-Purpose Tuning? Case Study in Medicine（arXiv 2311.16452v1；`papers_books_courses/papers/11/2023_Nori_CanGeneralistFoundationModelsOutcompete_en.pdf`）
- Med-HALT: Medical Domain Hallucination Test for Large Language Models（arXiv 2307.15343v2；`papers_books_courses/papers/11/2023_Pal_MedHaltMedicalDomainHallucination_en.pdf`）
- Towards Expert-Level Medical Question Answering with Large Language Models（arXiv 2305.09617v1；`papers_books_courses/papers/11/2023_Singhal_TowardsExpertLevelMedicalQuestion_en.pdf`）
- Generating CAD Code with Vision-Language Models for 3D Designs（arXiv 2410.05340v2；`papers_books_courses/papers/11/2024_Alrashedy_GeneratingCadCodeVisionLanguage_en.pdf`）
- BlenderLLM: Training Large Language Models for Computer-Aided Design with Self-improvement（arXiv 2412.14203v1；`papers_books_courses/papers/11/2024_Du_BlenderllmTrainingLargeLanguageModels_en.pdf`）
- LLM4PLC: Harnessing Large Language Models for Verifiable Programming of PLCs in Industrial Control Systems（arXiv 2401.05443v1；`papers_books_courses/papers/11/2024_Fakih_Llm4plcHarnessingLargeLanguageModels_en.pdf`）
- Text2CAD: Generating Sequential CAD Models from Beginner-to-Expert Level Text Prompts（arXiv 2409.17106v1；`papers_books_courses/papers/11/2024_Khan_Text2cadGeneratingSequentialCadModels_en.pdf`）
- MedCalc-Bench: Evaluating Large Language Models for Medical Calculations（arXiv 2406.12036v4；`papers_books_courses/papers/11/2024_Khandekar_MedcalcBenchEvaluatingLargeLanguage_en.pdf`）
- Agents4PLC: Automating Closed-loop PLC Code Generation and Verification in Industrial Control Systems using LLM-based Agents（arXiv 2410.14209v2；`papers_books_courses/papers/11/2024_Liu_Agents4plcAutomatingClosedLoopPlc_en.pdf`）
- CAD-Assistant: Tool-Augmented VLLMs as Generic CAD Task Solvers（arXiv 2412.13810v3；`papers_books_courses/papers/11/2024_Mallis_CadAssistantToolAugmentedVllms_en.pdf`）
- CAD-Recode: Reverse Engineering CAD Code from Point Clouds（arXiv 2412.14042v2；`papers_books_courses/papers/11/2024_Rukhovich_CadRecodeReverseEngineeringCad_en.pdf`）
- AgentClinic: a multimodal agent benchmark to evaluate AI in simulated clinical environments（arXiv 2405.07960v5；`papers_books_courses/papers/11/2024_Schmidgall_AgentclinicMultimodalAgentBenchmarkEvaluate_en.pdf`）
- Towards Conversational Diagnostic AI（arXiv 2401.05654v1；`papers_books_courses/papers/11/2024_Tu_TowardsConversationalDiagnosticAi_en.pdf`）
- Benchmarking Retrieval-Augmented Generation for Medicine（arXiv 2402.13178v2；`papers_books_courses/papers/11/2024_Xiong_BenchmarkingRetrievalAugmentedGenerationMedicine_en.pdf`）
- HealthBench: Evaluating Large Language Models Towards Improved Human Health（arXiv 2505.08775v1；`papers_books_courses/papers/11/2025_Arora_HealthbenchEvaluatingLargeLanguageModels_en.pdf`）
- MedGemma Technical Report（arXiv 2507.05201v4；`papers_books_courses/papers/11/2025_Sellergren_MedgemmaTechnicalReport_en.pdf`）
- Foam-Agent: A Large Language Model-Based Multi-Agent Framework for Automating Computational Fluid Dynamics Workflows（arXiv 2505.04997v3；`papers_books_courses/papers/11/2025_Yue_FoamAgentLargeLanguageModel_en.pdf`）
