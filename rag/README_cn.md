# rag/ 模块索引（07 RAG 与知识系统）

外层归档为本库命名（含 _en 语言后缀）；解包后内部保持上游原始路径。每个项目的中文入口说明见 project_cards/<编号>_cn.md。

## 存放于本目录的项目

| 编号 | 项目 | 版本 | 路线 | 角色 | 等级 | 归档 |
|---|---|---|---|---|---|---|
| P0701 | deepset-ai/haystack | v3.4.1 | C | 完整工程 | L1 | `P0701_deepset-ai_haystack_v3.4.1_src_en.tar` |
| P0702 | infiniflow/ragflow | v0.27.3 | C | 完整工程 | L1 | `P0702_infiniflow_ragflow_v0.27.3_src_en.tar` |
| P0703 | explodinggradients/ragas | v0.4.3 | C | 单模块参考 | L1 | `P0703_explodinggradients_ragas_v0.4.3_src_en.tar` |
| P0704 | facebookresearch/faiss | v1.15.1 | C | 单模块参考 | L1 | `P0704_facebookresearch_faiss_v1.15.1_src_en.tar` |
| P0705 | qdrant/qdrant | v1.20.0 | C | 完整工程 | L1 | `P0705_qdrant_qdrant_v1.20.0_src_en.tar` |
| P0706 | FlagOpen/FlagEmbedding | v1.4.2 | B,C | 单模块参考 | L1 | `P0706_FlagOpen_FlagEmbedding_v1.4.2_src_en.tar` |

## 跨模块关联项目（只保存一份，存放在其主模块目录）

| 编号 | 项目 | 存放位置 | 用途 |
|---|---|---|---|
| P0202 | docling-project/docling | `data/P0202_docling-project_docling_v2.145.0_src_en.tar` | 文档解析：PDF/Office/HTML、版面、表格、公式、OCR，输出带来源定位的结构 |
| P0208 | opendatalab/MinerU | `data/P0208_opendatalab_MinerU_mineru-4.1.2-released_src_en.tar` | PDF 解析：表格、公式、扫描件 OCR 到 Markdown/JSON |
| P0904 | langgenius/dify | `applications/P0904_langgenius_dify_1.18.0_src_en.tar` | LLM 应用平台：工作流、知识库、多租户、任务队列、Docker Compose |
| P1101 | Teddy-XiongGZ/MedRAG | `applications/P1101_Teddy-XiongGZ_MedRAG_main-7599a728a2_src_en.tar` | 医学 RAG 工具包（检索器、语料、MIRAGE 评测配套） |
| P1214 | openfga/openfga | `input_output_pipeline/P1214_openfga_openfga_v1.22.1_src_en.tar` | 细粒度授权（关系型访问控制，适用于用户/租户/文档权限过滤） |

## 本模块论文（24 篇，存放于 papers_books_courses/papers/<模块编号>/）

- Dense Passage Retrieval for Open-Domain Question Answering（arXiv 2004.04906v3；`papers_books_courses/papers/07/2020_Karpukhin_DensePassageRetrievalOpenDomain_en.pdf`）
- Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks（arXiv 2005.11401v4；`papers_books_courses/papers/07/2020_Lewis_RetrievalAugmentedGenerationKnowledgeIntensive_en.pdf`）
- ColBERTv2: Effective and Efficient Retrieval via Lightweight Late Interaction（arXiv 2112.01488v3；`papers_books_courses/papers/07/2021_Santhanam_Colbertv2EffectiveEfficientRetrievalLightweight_en.pdf`）
- Self-RAG: Learning to Retrieve, Generate, and Critique through Self-Reflection（arXiv 2310.11511v1；`papers_books_courses/papers/07/2023_Asai_SelfRAGLearningRetrieveGenerate_en.pdf`）
- Ragas: Automated Evaluation of Retrieval Augmented Generation（arXiv 2309.15217v2；`papers_books_courses/papers/07/2023_Es_RagasAutomatedEvaluationRetrievalAugmented_en.pdf`）
- Enabling Large Language Models to Generate Text with Citations（arXiv 2305.14627v2；`papers_books_courses/papers/07/2023_Gao_EnablingLargeLanguageModelsGenerate_en.pdf`）
- Retrieval-Augmented Generation for Large Language Models: A Survey（arXiv 2312.10997v5；`papers_books_courses/papers/07/2023_Gao_RetrievalAugmentedGenerationLargeLanguage_en.pdf`）
- Lost in the Middle: How Language Models Use Long Contexts（arXiv 2307.03172v3；`papers_books_courses/papers/07/2023_Liu_LostMiddleHowLanguageModels_en.pdf`）
- RankZephyr: Effective and Robust Zero-Shot Listwise Reranking is a Breeze!（arXiv 2312.02724v1；`papers_books_courses/papers/07/2023_Pradeep_RankzephyrEffectiveRobustZeroShot_en.pdf`）
- ARES: An Automated Evaluation Framework for Retrieval-Augmented Generation Systems（arXiv 2311.09476v2；`papers_books_courses/papers/07/2023_SaadFalcon_AresAutomatedEvaluationFrameworkRetrieval_en.pdf`）
- Improving Text Embeddings with Large Language Models（arXiv 2401.00368v3；`papers_books_courses/papers/07/2023_Wang_ImprovingTextEmbeddingsLargeLanguage_en.pdf`）
- Seven Failure Points When Engineering a Retrieval Augmented Generation System（arXiv 2401.05856v1；`papers_books_courses/papers/07/2024_Barnett_SevenFailurePointsWhenEngineering_en.pdf`）
- M3-Embedding: Multi-Linguality, Multi-Functionality, Multi-Granularity Text Embeddings Through Self-Knowledge Distillation（arXiv 2402.03216v5；`papers_books_courses/papers/07/2024_Chen_M3EmbeddingMultiLingualityMulti_en.pdf`）
- The Faiss library（arXiv 2401.08281v4；`papers_books_courses/papers/07/2024_Douze_FaissLibrary_en.pdf`）
- From Local to Global: A Graph RAG Approach to Query-Focused Summarization（arXiv 2404.16130v2；`papers_books_courses/papers/07/2024_Edge_LocalGlobalGraphRagApproach_en.pdf`）
- ColPali: Efficient Document Retrieval with Vision Language Models（arXiv 2407.01449v6；`papers_books_courses/papers/07/2024_Faysse_ColpaliEfficientDocumentRetrievalVision_en.pdf`）
- Late Chunking: Contextual Chunk Embeddings Using Long-Context Embedding Models（arXiv 2409.04701v3；`papers_books_courses/papers/07/2024_Gnther_LateChunkingContextualChunkEmbeddings_en.pdf`）
- HippoRAG: Neurobiologically Inspired Long-Term Memory for Large Language Models（arXiv 2405.14831v3；`papers_books_courses/papers/07/2024_Gutirrez_HipporagNeurobiologicallyInspiredLongTerm_en.pdf`）
- RAPTOR: Recursive Abstractive Processing for Tree-Organized Retrieval（arXiv 2401.18059v1；`papers_books_courses/papers/07/2024_Sarthi_RaptorRecursiveAbstractiveProcessingTree_en.pdf`）
- Corrective Retrieval Augmented Generation（arXiv 2401.15884v3；`papers_books_courses/papers/07/2024_Yan_CorrectiveRetrievalAugmentedGeneration_en.pdf`）
- CRAG -- Comprehensive RAG Benchmark（arXiv 2406.04744v2；`papers_books_courses/papers/07/2024_Yang_CragComprehensiveRagBenchmark_en.pdf`）
- PoisonedRAG: Knowledge Corruption Attacks to Retrieval-Augmented Generation of Large Language Models（arXiv 2402.07867v3；`papers_books_courses/papers/07/2024_Zou_PoisonedragKnowledgeCorruptionAttacksRetrieval_en.pdf`）
- MMTEB: Massive Multilingual Text Embedding Benchmark（arXiv 2502.13595v4；`papers_books_courses/papers/07/2025_Enevoldsen_MmtebMassiveMultilingualTextEmbedding_en.pdf`）
- Agentic Retrieval-Augmented Generation: A Survey on Agentic RAG（arXiv 2501.09136v4；`papers_books_courses/papers/07/2025_Singh_AgenticRetrievalAugmentedGenerationSurvey_en.pdf`）
