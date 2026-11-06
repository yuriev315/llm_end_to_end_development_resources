# A02 本地文档 RAG

## 状态

- 云 API 必需：否（可选）  
- 可连接本地模型：是（生成用 llama-server；嵌入地址见 `models/embeddings/*.url.txt`）  
- 离线资源已备齐：代码与示例文档已写；嵌入 **权重未入库，只记地址**  
- 已断网运行验证：**否**

## 嵌入后端

| 值 | 含义 | 是否语义检索 |
|---|---|---|
| `hash` | 词哈希向量 | 否，仅流水线 |
| `local` | llama-server `/v1/embeddings` | 取决于所加载的嵌入 GGUF |
| `hf` | sentence-transformers 加载 bge | 需 optional torch wheelhouse，本轮未执行 |

重排：配置 `AGENT_RERANK_PATH` 才启用，默认关闭。

引用字段：`doc_id, chunk, path, score, text`。知识更新需自行替换 [`fixtures/docs`](fixtures/docs/) 并重建切块；没有自动增量索引服务。

LangGraph 钉在独立 wheelhouse，不沿用 env 15 的安装状态。
