# A03 编码与文件操作

## 状态

- 云 API 必需：否（可选）。aider 默认文档大量写云模型，但可改 `OPENAI_API_BASE`  
- 可连接本地模型：是  
- 离线资源已备齐：沙箱代码已写；aider wheel 见 inventories  
- 已断网运行验证：**否**

## 两层（必须拆环境）

1. **本仓库沙箱脚本** [`src/file_agent.py`](src/file_agent.py)：只读写 [`fixtures/workspace`](fixtures/workspace/)，无 shell。wheelhouse：`environments/py3xx_<platform>/`（openai-agents 0.24.0，openai 3.x）。  
2. **aider-chat 0.86.2**：社区编码 Agent。wheelhouse：`environments/A03_aider_py3xx_<platform>/`。它钉死 `openai==2.20.0`，与 Agents SDK 冲突，不能混装。不要对沙箱外的真实仓库启用任意命令。

Python：aider 声明 `>=3.10,<3.13`，3.10 与 3.12 都解析；本轮 `--only-binary :all:`，不编译 sdist。
