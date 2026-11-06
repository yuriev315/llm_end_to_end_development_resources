# AI Agent 专题：下载与解压说明

本专题以 Release `ai-agent-20261106` 发布，共 6 个不压缩 tar 包，外加文件索引和校验文件。资料检索日：项目 wheel、源码快照、论文与运行时按 2026-10-30 的钉死版本获取，文档镜像为 2026-11-06 的页面。

## 1. 需要下载哪些包

| 包 | 大小 | 文件数 | 内容 | 什么时候需要 |
|---|---:|---:|---|---|
| `ai_agent_20261106_01_docs_papers_code_cn_en.tar` | 1.13 GiB | 4006 | 说明、指南、文档镜像、论文、源码快照、项目代码、模型分词器、清单、.url 占位 | **必下**（只想阅读，下这一个就够） |
| `ai_agent_20261106_02_linux_wheels_cn_en.tar` | 1.30 GiB | 1063 | Linux x86-64 项目 wheelhouse（Python 3.10 / 3.12） | 在 Linux 上离线安装项目 |
| `ai_agent_20261106_03_windows_wheels_cn_en.tar` | 1.18 GiB | 1062 | Windows x64 项目 wheelhouse（Python 3.10 / 3.12） | 在 Windows 上用项目自带 wheelhouse |
| `ai_agent_20261106_04_linux_runtimes_cn_en.tar` | 0.08 GiB | 3 | Linux 版 llama.cpp（CPU、Vulkan）、Node.js | 在 Linux 上运行本地模型 |
| `ai_agent_20261106_05_windows_runtimes_cn_en.tar` | 0.09 GiB | 3 | Windows 版 llama.cpp（CPU、Vulkan）、Node.js | 在 Windows 上运行本地模型 |
| `ai_agent_20261106_06_windows_minimum_runtime_cn_en.tar` | 1.24 GiB | 1200 | Windows 最小运行环境：Python 安装包、17 个环境的 wheel、llama.cpp、嵌入模型、安装脚本 | 在 Windows 上一键建环境（推荐） |

- 每个包都可以单独解压，不分先后；包与包之间没有重复文件。
- 所有包的顶层目录都是 `ai_agent/`，**解压到同一个目录**后，链接才能互相跳转。
- `ai_agent_20261106_archive_index_cn.csv` 列出每个包里的每个文件（相对路径、字节数、SHA-256）。

## 2. Windows 上解压

1. 建一个路径很短的目录，例如 `D:\aia\`（包内最长相对路径：Windows 部分 186 个字符，Linux wheel 224 个字符，目录太深会超过 260 字符限制）。
2. 把 tar 包放进去，在该目录打开命令提示符或 PowerShell，对每个包执行：

   ```
   tar -xf ai_agent_20261106_01_docs_papers_code_cn_en.tar
   ```

   也可以用 7-Zip 解压到当前目录。
3. 用浏览器打开 `ai_agent\index_cn.html`。
4. 建 Python 环境见 `ai_agent\deps\README_cn.md`。

## 3. Linux 上解压

```bash
mkdir -p ~/aia && cd ~/aia
for f in ai_agent_20261106_0*_cn_en.tar; do tar -xf "$f"; done
sha256sum -c ai_agent_20261106_SHA256SUMS.txt
```

项目的离线安装方法见各项目目录 `agent_runtime_kits/projects/<项目>/README_cn.md`。

## 4. 不在包内的文件（`.url` 占位）

共 41 个 `.url` 文件，与原文件同名、同位置：

- 27 个因许可不允许再分发：25 篇论文（arXiv 默认许可或 NC 许可）、2 个 FFmpeg 构建（LGPL）。
- 14 个超过 100 MiB：torch CPU wheel、CrewAI 源码快照、llama.cpp CUDA 包、Chrome for Testing 浏览器包。

每个 `.url` 是 Windows Internet 快捷方式，双击打开官方地址；文件里还写了原文件名、字节数、SHA-256（已知时）、许可和原因。完整清单：`ai_agent/url_placeholders_cn.csv`。

模型权重（Qwen2.5 GGUF、bge safetensors 等）按本专题的约定只记录地址（`*.url.txt`），分词器和配置文件在包内。

## 5. 校验值（SHA-256）

```
62b1ab97e3e7dbe2029d6e7510779a752065dc87e1c77007416dffc101e45c0d  ai_agent_20261106_01_docs_papers_code_cn_en.tar
c76925f64eac6a7f6a5ec8ccbf2eea93b0e0bbd8dad3c13bbb09429f785194cc  ai_agent_20261106_02_linux_wheels_cn_en.tar
16d4852dbca0fad5b7380a9fce27da6ff8f11b0f61e8c6d40d7739dfeca64f7e  ai_agent_20261106_03_windows_wheels_cn_en.tar
6965ae107cd6fd31e92427b9045bbbdb9483ccd8be3ab27e07807b762353d352  ai_agent_20261106_04_linux_runtimes_cn_en.tar
cd66b722004cc71e38a525e86e788355918fdbe192a9edc7996d4ea31a12d252  ai_agent_20261106_05_windows_runtimes_cn_en.tar
f1d9663f1666546fb5942417e6e864b57f31e8dd2ca2badfc8c6cf24ec247a64  ai_agent_20261106_06_windows_minimum_runtime_cn_en.tar
```
