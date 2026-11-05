# Coding 智能体路线

> 标记说明：〔上游〕= 上游快照中的文件明确写明；〔建议〕= 本轮自行整理的建议；〔未验证〕= 命令、配置或兼容性未经运行验证。
> 本轮未安装依赖、未运行任何上游代码，所列项目最高为 L1；不构成生产就绪结论。环节级验收条件与入口文件见 `end_to_end_coverage_cn.csv`，跨仓库组合的证据见 `compatibility_matrix_cn.csv`，项目入口说明见 `project_cards/<编号>_cn.md`。

## 项目目标

仓库索引 → 需求与上下文 → 计划与工具调用 → 补丁编辑 → 隔离执行 → 构建测试与静态分析 → 结果反馈 → 用户审核 → IDE/终端集成。

## 模块组合

见 reference_stacks_cn.md 路线 3：aider（P0802）、multilspy（P0807）、OpenHands SDK（P0811）、SWE-agent（P0805）、mini-SWE-agent（P0810）、MCP SDK（P0801）、SWE-bench（P0505）、Ruff（P0808）、Continue（P0804）。

## 资料和源码路径

agents_coding/、evaluation/；文档 MCP 规范（D26 复用、D0801 新快照）、LSP 规范（D27）、VS Code 扩展 API（D28）、Pyright（D37）、Bandit（D42）、gVisor（D41）；论文 papers_books_courses/papers/08。

## 环境

〔上游〕SWE-bench 建议 x86_64、≥120GB 磁盘、16GB 内存、8 核（README.md:112）；需 Docker。

## 数据格式

SWE-bench 实例（repo、base_commit、FAIL_TO_PASS、PASS_TO_PASS）；aider SEARCH/REPLACE 块；MCP tools/call JSON。

## 配置

SWE-agent `config/default.yaml`；Continue config；OpenHands SDK `examples/`。

## 执行顺序

〔建议〕mini-SWE-agent 在 SWE-bench Lite 单实例 → SWE-agent 批量 → OpenHands SDK + Docker 工作区 → IDE 集成（Continue）。

## 测试方法

SWE-bench harness 判定；各项目 tests/；Ruff 规则检查。〔未验证〕

## 部署步骤

OpenHands Agent Canvas（P0803，Helm/Docker）+ Agent Server（P0811）；隔离运行时与网络策略由部署方配置。

## 外部依赖

模型 API 或自托管代码模型；SWE-bench 数据与镜像；语言服务器二进制。

## 尚未解决的问题

OpenHands SDK 固定 litellm==1.93.0；Agent Canvas 与 SDK 版本对应未核对；通用依赖解析器源码未收录。
