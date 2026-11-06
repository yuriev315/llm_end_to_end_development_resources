# 缺失与未验证（写清单时以 inventories 为准）

## 明确不做或未完成

- 未安装任何包，未启动 llama-server，未断网跑 Agent。  
- 未下载 SWE-bench 实例 blob、GAIA 附件、WebArena 站点、OSWorld 虚拟机。GAIA 仓库/HF 数据集当前 404/401，只记地址：[`experiments/GAIA_SOURCE.url.txt`](experiments/GAIA_SOURCE.url.txt)。  
- 模型权重（GGUF / safetensors）**只记录官方地址，不下载**；已下过的已删除并换成 `*.url.txt`。
- 未下载 14B/32B/70B 级权重。  
- 未打包 vLLM、Ollama 模型库、闭源 API 客户端密钥。  
- 未验证任何本地模型的工具调用或结构化输出成功率。  
- browser-use 在 Python 3.10 不可用（上游 `>=3.11`）。  
- 原 `01_math`–`10_quant_finance` 知识领域仍为骨架，不属于本增量完成范围。  
- Windows 套件不复制权重；两边共用 `models/*.url.txt` 地址。  
- LangSmith / 云追踪账号类服务无法离线化。  
- 部分 GitHub tag 可能 404，脚本会退回 latest 或 main，以 implementations 目录实文件为准。

## 硬件

目标默认为 **Linux x86-64 glibc** 与 **Windows 10/11 x86-64 CPU**。  
GPU 套件（llama.cpp CUDA/Vulkan + Qwen2.5-7B Q4）是可选增量，**不**声称能在任意电脑运行。未收集本机 GPU 型号。
