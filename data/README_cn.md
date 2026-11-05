# data/ 模块索引（02 数据管线）

外层归档为本库命名（含 _en 语言后缀）；解包后内部保持上游原始路径。每个项目的中文入口说明见 project_cards/<编号>_cn.md。

## 存放于本目录的项目

| 编号 | 项目 | 版本 | 路线 | 角色 | 等级 | 归档 |
|---|---|---|---|---|---|---|
| P0201 | huggingface/datatrove | v0.10.1 | A,B | 单模块参考 | L1 | `P0201_huggingface_datatrove_v0.10.1_src_en.tar` |
| P0202 | docling-project/docling | v2.145.0 | B,C | 单模块参考 | L1 | `P0202_docling-project_docling_v2.145.0_src_en.tar` |
| P0203 | argilla-io/distilabel | 1.5.3 | B | 单模块参考 | L1 | `P0203_argilla-io_distilabel_1.5.3_src_en.tar` |
| P0204 | argilla-io/argilla | v2.8.0 | B,C | 完整工程 | L1 | `P0204_argilla-io_argilla_v2.8.0_src_en.tar` |
| P0205 | allenai/dolma | v1.2.1 | A | 单模块参考 | L1 | `P0205_allenai_dolma_v1.2.1_src_en.tar` |
| P0206 | HumanSignal/label-studio | 1.23.2 | B,C | 完整工程 | L1 | `P0206_HumanSignal_label-studio_1.23.2_src_en.tar` |
| P0207 | iterative/dvc | 3.67.1 | A,B | 单模块参考 | L1 | `P0207_iterative_dvc_3.67.1_src_en.tar` |
| P0208 | opendatalab/MinerU | mineru-4.1.2-released | B,C | 单模块参考 | L1 | `P0208_opendatalab_MinerU_mineru-4.1.2-released_src_en.tar` |

## 跨模块关联项目（只保存一份，存放在其主模块目录）

| 编号 | 项目 | 存放位置 | 用途 |
|---|---|---|---|
| P0102 | karpathy/minbpe | `foundations/P0102_karpathy_minbpe_master-1acefe8941_src_en.tar` | BPE 分词器最小实现（训练/编码/解码，含测试） |
| P1203 | pemistahl/lingua-py | `input_output_pipeline/P1203_pemistahl_lingua-py_v2.2.0_src_en.tar` | 语言识别（短文本、多语言置信度） |

## 本模块论文（18 篇，存放于 papers_books_courses/papers/<模块编号>/）

- Deduplicating Training Data Makes Language Models Better（arXiv 2107.06499v2；`papers_books_courses/papers/02/2021_Lee_DeduplicatingTrainingDataMakesLanguage_en.pdf`）
- What's In My Big Data?（arXiv 2310.20707v2；`papers_books_courses/papers/02/2023_Elazar_WhatSMyBigData_en.pdf`）
- A Survey on Data Selection for Language Models（arXiv 2402.16827v3；`papers_books_courses/papers/02/2024_Albalak_SurveyDataSelectionLanguageModels_en.pdf`）
- Docling Technical Report（arXiv 2408.09869v5；`papers_books_courses/papers/02/2024_Auer_DoclingTechnicalReport_en.pdf`）
- DataComp-LM: In search of the next generation of training sets for language models（arXiv 2406.11794v4；`papers_books_courses/papers/02/2024_Li_DatacompLmSearchNextGeneration_en.pdf`）
- Best Practices and Lessons Learned on Synthetic Data（arXiv 2404.07503v2；`papers_books_courses/papers/02/2024_Liu_BestPracticesLessonsLearnedSynthetic_en.pdf`）
- RegMix: Data Mixture as Regression for Language Model Pre-training（arXiv 2407.01492v2；`papers_books_courses/papers/02/2024_Liu_RegmixDataMixtureRegressionLanguage_en.pdf`）
- Rephrasing the Web: A Recipe for Compute and Data-Efficient Language Modeling（arXiv 2401.16380v1；`papers_books_courses/papers/02/2024_Maini_RephrasingWebRecipeComputeData_en.pdf`）
- The FineWeb Datasets: Decanting the Web for the Finest Text Data at Scale（arXiv 2406.17557v2；`papers_books_courses/papers/02/2024_Penedo_FinewebDatasetsDecantingWebFinest_en.pdf`）
- Dolma: an Open Corpus of Three Trillion Tokens for Language Model Pretraining Research（arXiv 2402.00159v2；`papers_books_courses/papers/02/2024_Soldaini_DolmaOpenCorpusThreeTrillion_en.pdf`）
- Nemotron-CC: Transforming Common Crawl into a Refined Long-Horizon Pretraining Dataset（arXiv 2412.02595v2；`papers_books_courses/papers/02/2024_Su_NemotronCcTransformingCommonCrawl_en.pdf`）
- Large Language Models for Data Annotation and Synthesis: A Survey（arXiv 2402.13446v3；`papers_books_courses/papers/02/2024_Tan_LargeLanguageModelsDataAnnotation_en.pdf`）
- MinerU: An Open-Source Solution for Precise Document Content Extraction（arXiv 2409.18839v1；`papers_books_courses/papers/02/2024_Wang_MineruOpenSourceSolutionPrecise_en.pdf`）
- Magpie: Alignment Data Synthesis from Scratch by Prompting Aligned LLMs with Nothing（arXiv 2406.08464v2；`papers_books_courses/papers/02/2024_Xu_MagpieAlignmentDataSynthesisScratch_en.pdf`）
- Data Mixing Laws: Optimizing Data Mixtures by Predicting Language Modeling Performance（arXiv 2403.16952v2；`papers_books_courses/papers/02/2024_Ye_DataMixingLawsOptimizingData_en.pdf`）
- DataDecide: How to Predict Best Pretraining Data with Small Experiments（arXiv 2504.11393v2；`papers_books_courses/papers/02/2025_Magnusson_DatadecideHowPredictBestPretraining_en.pdf`）
- FineWeb2: One Pipeline to Scale Them All -- Adapting Pre-Training Data Processing to Every Language（arXiv 2506.20920v1；`papers_books_courses/papers/02/2025_Penedo_Fineweb2OnePipelineScaleThem_en.pdf`）
- olmOCR: Unlocking Trillions of Tokens in PDFs with Vision Language Models（arXiv 2502.18443v3；`papers_books_courses/papers/02/2025_Poznanski_OlmocrUnlockingTrillionsTokensPdfs_en.pdf`）
