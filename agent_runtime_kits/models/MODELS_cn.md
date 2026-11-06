# 权重地址（不下载文件）

检索日 **2026-10-30**。本专题 **只记录地址，不保存 GGUF / safetensors 等权重**。  
分词器与 `config.json` 可以保留。未加载、未推理。估算均为卡面/经验，本机未测。

完整 JSON：[`WEIGHTS_url_only.json`](WEIGHTS_url_only.json)。每个代表权重有 `{文件名}.url.txt`（一行 URL）。

| ID | 许可 | 格式 | 量化 | 硬件估算（未测） | 地址文件 |
|---|---|---|---|---|---|
| Qwen2.5-0.5B-Instruct | Apache-2.0 | GGUF | Q4_K_M | CPU RAM 约 1–2 GiB | [`cpu_baseline/qwen2.5-0.5b-instruct-q4_k_m.gguf.url.txt`](cpu_baseline/qwen2.5-0.5b-instruct-q4_k_m.gguf.url.txt) |
| Qwen2.5-1.5B-Instruct | Apache-2.0 | GGUF | Q4_K_M | 约 3–4 GiB | [`cpu_baseline/qwen2.5-1.5b-instruct-q4_k_m.gguf.url.txt`](cpu_baseline/qwen2.5-1.5b-instruct-q4_k_m.gguf.url.txt) |
| Qwen2.5-3B-Instruct | Apache-2.0 | GGUF | Q4_K_M | 约 5–8 GiB | [`cpu_baseline/qwen2.5-3b-instruct-q4_k_m.gguf.url.txt`](cpu_baseline/qwen2.5-3b-instruct-q4_k_m.gguf.url.txt) |
| Qwen2.5-7B-Instruct | Apache-2.0 | GGUF 分片 | Q4_K_M | 建议 VRAM ≥ 8 GiB 或 RAM ≥ 12 GiB | `gpu_optional/*.gguf.url.txt`（官方为两片，单文件 404） |
| bge-small-en-v1.5 | MIT | safetensors | 原精度 | CPU，约 130 MiB | [`embeddings/bge-small-en-v1.5/model.safetensors.url.txt`](embeddings/bge-small-en-v1.5/model.safetensors.url.txt) |
| bge-small-zh-v1.5 | MIT | safetensors | 原精度 | CPU，约 95 MiB | [`embeddings/bge-small-zh-v1.5/model.safetensors.url.txt`](embeddings/bge-small-zh-v1.5/model.safetensors.url.txt) |
| bge-small-en-v1.5 GGUF | MIT + 转换 | GGUF | Q8_0 | CPU | [`embeddings/bge-small-en-v1.5-q8_0.gguf.url.txt`](embeddings/bge-small-en-v1.5-q8_0.gguf.url.txt) |
| bge-reranker-base | MIT | safetensors 或 bin | 原精度 | CPU 慢 | [`rerankers/bge-reranker-base/model.safetensors.url.txt`](rerankers/bge-reranker-base/model.safetensors.url.txt) |
| Qwen2.5-1.5B tokenizer | Apache-2.0 | tokenizer | — | 很小 | [`tokenizers/Qwen2.5-1.5B-Instruct/`](tokenizers/Qwen2.5-1.5B-Instruct/)（已保存配置，不是权重） |

脚本 [`scripts/fetch_agent_topic_en.py`](../../scripts/fetch_agent_topic_en.py) 的 `models` 阶段只写地址文件，不会再拉权重。
