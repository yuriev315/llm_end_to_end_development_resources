# Qwen2.5-7B Q4_K_M 分片地址

官方仓库把该量化拆成两个 GGUF。本专题 **不下载分片**，只记地址。单文件 `qwen2.5-7b-instruct-q4_k_m.gguf` 的官方 URL 为 404。

地址：

- [`qwen2.5-7b-instruct-q4_k_m-00001-of-00002.gguf.url.txt`](qwen2.5-7b-instruct-q4_k_m-00001-of-00002.gguf.url.txt)
- [`qwen2.5-7b-instruct-q4_k_m-00002-of-00002.gguf.url.txt`](qwen2.5-7b-instruct-q4_k_m-00002-of-00002.gguf.url.txt)
- [`qwen2.5-7b-instruct-q4_k_m.gguf.url.txt`](qwen2.5-7b-instruct-q4_k_m.gguf.url.txt)（两片 URL 汇总）

若自行下载后合并（本库未执行）：

```
llama-gguf-split --merge qwen2.5-7b-instruct-q4_k_m-00001-of-00002.gguf qwen2.5-7b-instruct-q4_k_m.gguf
```
