# Windows Agent 运行套件

检索日 2026-10-30。项目源码与中文说明以 Linux 树 [`agent_runtime_kits/projects/`](../../agent_runtime_kits/projects/) 为准（通用源码共享）。本目录提供：

- `projects/*/environments/py310_windows` 与 `py312_windows` wheelhouse  
- [`runtimes/windows_x86_64/`](runtimes/windows_x86_64/) 下的 llama.cpp、Node、Playwright

模型 GGUF / bge 权重不在此树重复保存，使用共享模型增量包，解压到约定相对路径或设置环境变量。

本轮未在 Windows 上安装或运行。
