# AG2 连接说明（未执行）

源码快照：`knowledge/11_ai_agent/implementations/` 中 `ag2ai__ag2_v1.2.2`（若标签下载失败则见实际文件名）。

独立 wheelhouse：[`environments/A05_multi_agent_ag2_py310_linux`](../environments/A05_multi_agent_ag2_py310_linux/) 与对应 3.12 / Windows 目录。

本地模型：

```text
config_list = [{
  "model": "qwen2.5-1.5b-instruct",
  "base_url": "http://127.0.0.1:8080/v1",
  "api_key": "local-not-a-secret",
  "price": [0, 0],
}]
```

AG2 声明 `openai>=3.37,<4`。与 CrewAI 的 openai 2.x 冲突。本轮未 import `autogen`/`ag2`，不能写“已跑通群聊”。
