# 机械制造应用参考路线

> 标记说明：〔上游〕= 上游快照中的文件明确写明；〔建议〕= 本轮自行整理的建议；〔未验证〕= 命令、配置或兼容性未经运行验证。
> 本轮未安装依赖、未运行任何上游代码，所列项目最高为 L1；不构成生产就绪结论。环节级验收条件与入口文件见 `end_to_end_coverage_cn.csv`，跨仓库组合的证据见 `compatibility_matrix_cn.csv`，项目入口说明见 `project_cards/<编号>_cn.md`。

## 项目目标

分四类，不得混用：① 问答（标准、工艺、维护知识检索）；② 设计辅助（生成/修改参数化 CAD）；③ 仿真辅助（生成与修复 CFD 算例）；④ 实际控制（PLC 代码）——仅研究，不得直接下发设备。

## 模块组合

① 通用 RAG 组合 + pint（P1108）；② CadQuery（P1109）、build123d（P1110）、freecad-mcp（P1111）、Text2CAD（P1112）、CAD-Recode（P1113）；③ Foam-Agent（P1114）；④ SemaPLC（P1115）、LLM4IAS（P1116）。审核：Label Studio（P0206）。

## 资料和源码路径

applications/（11）；论文 papers_books_courses/papers/11（Text2CAD、CAD-Recode、CADCodeVerify、CAD-Assistant、BlenderLLM、Foam-Agent、LLM4PLC、Agents4PLC、LLM 设计与制造评估）。

## 环境

〔上游〕Foam-Agent 容器预装 OpenFOAM v10（README.md:35）；freecad-mcp 需本地 FreeCAD 与 addon（README.md:40）；SemaPLC 用 Docker 运行 OpenPLC Runtime v4 + matiec（README.md:49）并需 LLM API 密钥（README.md:109）。

## 数据格式

CadQuery/build123d Python 脚本 → STEP/STL；OpenFOAM 算例目录；IEC 61131-3 结构化文本。

## 配置

Foam-Agent 环境变量（README 示例 FOAMAGENT_MODEL_VERSION）；SemaPLC 模型提供方配置；所有 API 密钥仅占位。

## 执行顺序

〔建议〕② 设计辅助：模型生成 CadQuery 脚本 → 在隔离环境执行重建几何 → 自动检查（尺寸、体积、单位）→ 工程师审核；③ 仿真：生成算例 → 求解 → 独立检查收敛/网格/边界条件 → 工程师签核；④ 控制：仅在软 PLC 仿真中验证。

## 测试方法

cadquery/build123d `tests/`；几何重建成功率；仿真残差与网格质量检查（〔建议〕自建）。〔未验证〕

## 部署步骤

①② 可作为内部工具原型；③ 仅研究；④ 不部署到任何真实设备。

## 外部依赖

ISO 公差标准、材料数据库（付费/授权，未下载）；FreeCAD、OpenFOAM、OpenPLC；Text2CAD/CAD-Recode 权重（非商业许可）。

## 尚未解决的问题

公差与材料数据缺失；仿真结果独立校验无参考实现；Foam-Agent 57 个 LFS 指针未取回；工程图纸解析缺失；研究原型许可多为非商业。
