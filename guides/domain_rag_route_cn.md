# 专业知识 RAG 路线

> 标记说明：〔上游〕= 上游快照中的文件明确写明；〔建议〕= 本轮自行整理的建议；〔未验证〕= 命令、配置或兼容性未经运行验证。
> 本轮未安装依赖、未运行任何上游代码，所列项目最高为 L1；不构成生产就绪结论。环节级验收条件与入口文件见 `end_to_end_coverage_cn.csv`，跨仓库组合的证据见 `compatibility_matrix_cn.csv`，项目入口说明见 `project_cards/<编号>_cn.md`。

## 项目目标

文档获取 → 解析与来源定位 → 清洗切分 → 索引 → 权限过滤 → 检索重排序 → 回答与引用 → 领域校验 → 更新维护。

## 模块组合

Docling/MinerU（P0202/P0208）+ Haystack 或 RAGFlow（P0701/P0702）+ FlagEmbedding（P0706）+ Qdrant/FAISS（P0705/P0704）+ OpenFGA（P1214）+ Ragas/FActScore（P0703/P1220）+ DVC（P0207）。

## 资料和源码路径

rag/、data/、input_output_pipeline/；文档 LlamaIndex（D25，部分）、LangChain（D24，部分）、FAISS Wiki（D23）、Sentence Transformers（D22）；论文 papers_books_courses/papers/07。

## 环境

CPU 可完成解析与小规模索引（〔上游〕MinerU README_zh-CN.md:444 起列出 CPU/GPU 模式与内存需求）；RAGFlow 需 Docker Compose 多个依赖服务。

## 数据格式

DoclingDocument JSON（prov 含页码与 bbox）；chunk 元数据 {doc_id, version, page, acl}（〔建议〕）；引用 {doc_id, page, quote}。

## 配置

RAGFlow `docker/.env`、`conf/service_conf.yaml`；Qdrant `config/config.yaml`。

## 执行顺序

见 reference_stacks_cn.md 2.1。〔建议〕先用 docling `tests/data` 中的样例文档做离线解析回归，再接索引。

## 测试方法

docling tests/data 期望输出；haystack test/；qdrant tests；Ragas 指标与人工抽检；越权检索测试（〔建议〕自建）。〔未验证〕

## 部署步骤

RAGFlow Compose 或 Helm（`helm/`）；Qdrant 快照用于回滚。

## 外部依赖

嵌入/重排序/解析模型权重；业务系统连接器凭据（占位）；领域语料。

## 尚未解决的问题

权限过滤（OpenFGA→向量库 payload）无上游参考（P0）；知识库版本与答案日志关联需自建；工程图纸解析缺失。
