# A01 基础工具调用与多步任务

## 状态

- 云 API 必需：否（可选路径）  
- 可连接本地模型：是（llama-server OpenAI 兼容）  
- 离线资源已备齐：代码、配置与 wheel 已写；**GGUF 只记地址，权重未入库**  
- 已断网运行验证：**否**

## 这是什么

一个最小 ReAct 式循环：计算器、便笺、时间。mock 策略覆盖 [`examples/task_multistep.json`](examples/task_multistep.json)。真实模型路径使用 JSON object 输出，失败会记入结果，不伪装成功。

依赖：`openai-agents==0.24.0` 及闭包（独立 wheelhouse）。主脚本目前只用 `openai` 客户端，避免把 SDK 当唯一入口；SDK 源码在 [`11_ai_agent/implementations/`](../../../11_ai_agent/implementations/)。

## 启动（本轮未执行）

Linux：

```bash
# 1. 解压 llama.cpp CPU 包，确认 llama-server 可执行文件
# 2. bash scripts/start_llama_server_linux.sh
# 3. 用对应 Python 3.10 或 3.12 建 venv，pip install --no-index --find-links environments/py312_linux/wheelhouse -r environments/py312_linux/requirements_direct_en.txt
# 4. AGENT_LLM_MODE=local python src/agent_loop.py
```

mock（仍属“未验证真实 Agent”）：

```bash
AGENT_LLM_MODE=mock python src/agent_loop.py
```

Windows 用 `environments/py3xx_windows` 与 [`scripts/start_llama_server_windows.ps1`](scripts/start_llama_server_windows.ps1)。
