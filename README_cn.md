# 大语言模型端到端开发资源库（llm_end_to_end_development_resources）

本库收集**实际开发所需**的参考源码、配置、测试、部署文件、官方文档、运行手册，以及配套教材、课程与论文，覆盖通用助手、医疗、机械制造和 Coding 应用。

> **重要声明**
> - 本库只做了下载、静态核对和运行准备：**没有运行任何上游代码、没有训练、没有部署**。所有项目的可运行性等级最高为 L1，**没有任何 L2/L3 结论，也没有任何“生产就绪”结论**。
> - 大模型权重和完整数据集没有收录。Release 里只有项目用到的最小模型和样例数据，其余的下载地址见同名 `.url` 文件。
> - 配置中只保留占位符，本库不含真实凭据。
> - 教学示例不得视为可直接投入生产；医疗条目仅限研究与教学用途；机械“实际控制”类条目仅为研究原型，不得连接真实设备。
> - **版权受限资料**（非商业许可、版权保留、未见许可证、仅个人保存等）在本库中是同名 `.url` 占位文件，不含原文件。

## 1. 内容在哪里

| 位置 | 内容 |
|---|---|
| Git 分支 | 登记表、指南、项目卡片、模块索引、清单和 `.url` 占位文件 |
| Release `llm-e2e-full-20261029` | 源码快照、官方文档、论文、教材、课程、依赖 wheel、最小模型和样例数据 |

下载和解压方法见 [`download_restore_cn.md`](download_restore_cn.md)，离线安装见 [`windows/README_offline_install_cn.md`](windows/README_offline_install_cn.md)。

`.url` 文件可以双击打开原始来源，里面还记录了大小、SHA-256、版本和许可证。出现 `.url` 的原因有三种：

| 状态 | 含义 |
|---|---|
| `PLACEHOLDER_RESTRICTED` | 版权受限，或没有找到明确的再分发许可 |
| `PLACEHOLDER_OVERSIZE` | 单个文件超过 100 MiB |
| `PLACEHOLDER_NOT_OBTAINED` | 来源拒绝自动下载，需要用浏览器打开 |

全部占位文件见 [`manifests/url_placeholders.csv`](manifests/url_placeholders.csv)，每个文件的状态见 [`manifests/file_status.csv`](manifests/file_status.csv)，公开文件的许可证见 [`manifests/public_file_licenses.csv`](manifests/public_file_licenses.csv)。

## 2. 三条开发路线

| 路线 | 含义 | 本库主要条目 |
|---|---|---|
| A 从头训练 | 从分词器、模型定义到预训练 | P0101–P0105、P0201/P0205、P0301–P0305 |
| B 适配开放权重模型 | 持续预训练、SFT、PEFT、偏好优化、RL、蒸馏 | P0401–P0404、P0606、P0706、P1103、P1117 |
| C 使用模型服务开发应用 | 对话、RAG、智能体、专业应用、输入输出处理链 | 07–12 模块大部分条目 |

每个项目在 `resource_catalog_cn.csv` 的“开发路线”列标明所属路线；API 应用示例不被当作模型训练代码。

## 3. 目录

| 目录 | 内容 |
|---|---|
| foundations/ | 01 基础与教学实现 |
| data/ | 02 数据管线（解析、OCR、去重、合成、标注、版本） |
| training/ | 03 预训练 |
| adaptation_alignment/ | 04 适配与对齐 |
| evaluation/ | 05 评测与回归 |
| inference/ | 06 推理与服务 |
| rag/ | 07 RAG 与知识系统 |
| agents_coding/ | 08 智能体与 Coding |
| applications/ | 09 对话与业务产品 + 11 专业应用（医疗、机械制造、Coding 训练数据） |
| deployment_operations/ | 10 生产部署与维护 |
| input_output_pipeline/ | 12 输入前处理 → 指令组织 → 生成 → 输出后处理 → 工具执行；含 `input_output_pipeline_cn.md`、`alignment_vs_runtime_controls_cn.md`、`validation_matrix_cn.csv` |
| papers_books_courses/ | papers/<模块编号>/（论文）、books/、courses/、official_docs/ |
| guides/ | 路线指南与覆盖矩阵（见第 5 节） |
| project_cards/ | 每个源码/文档项目的中文入口说明 `<编号>_cn.md` |
| windows/、ubuntu/、run_data/ | 依赖 wheel、最小模型和样例数据中超过 100 MiB 或版权受限文件的 `.url` |
| manifests/ | 文件状态、占位文件、许可证和依赖清单 |
| state/ | 部分项目的下载与核对状态 JSON |

每个模块目录有 `README_cn.md` 索引：列出存放在本目录的项目，以及只保存一份、存放在其他模块目录的跨模块项目。

**归档规则**：上游项目以 `<编号>_<owner>_<repo>_<版本>_src_en.tar.gz` 保存，内容是对应提交的工作树（不含 .git），**子模块和 Git LFS 对象不在快照内**。登记表和模块索引里写的 `.tar` 路径，在 Release 中是同名的 `.tar.gz`。

## 4. 登记表（根目录）

| 文件 | 说明 |
|---|---|
| resource_catalog_cn.csv | 全部条目（源码项目、官方文档、论文、教材、课程/实践），含版本、提交号、许可证、完整性 |
| project_readiness_cn.csv | 每个项目的可运行性等级、版本、提交号和核验说明 |
| dependency_matrix_cn.csv | Python/torch/Node 要求、依赖与锁文件、README 中硬件与 HF 资源的原文摘录、外部资源与访问条件 |
| progress_cn.csv | 各模块数量统计 |
| download_failures_cn.csv | 下载失败与按规则排除的条目 |
| archive_index_cn.csv | Release 中每个包的文件清单 |

可运行性等级：L0 源码已下载、未完成静态核对要求；L1 已核对入口、依赖和配置说明；L2/L3 需在记录环境中实际运行，目前均无。文档/规范类条目标“不适用”。

## 5. 指南（guides/）

- `reference_stacks_cn.md`：四条路线（通用对话助手、专业知识 RAG、Coding 智能体、模型微调与发布）的建议组合、模块接口、启动顺序、测试与部署步骤、兼容关系与待补资源。
- `end_to_end_coverage_cn.csv`：路线 × 环节覆盖矩阵（目标、验收条件、参考项目/版本/提交号/路径、入口文件、依赖、测试与部署文件、许可证、维护状态、下载状态、等级、缺失项、优先级）。
- `gap_backlog_cn.csv`：按 P0/P1/P2 排序的缺口清单。
- `compatibility_matrix_cn.csv`：跨仓库组合的证据（使用方快照中的引用文件、版本约束原文、自动版本比对结论）。
- `completion_report_cn.md`：完成情况报告。
- 八条路线指南：`from_scratch_training_route_cn.md`、`open_weight_adaptation_route_cn.md`、`general_assistant_route_cn.md`、`domain_rag_route_cn.md`、`medical_application_route_cn.md`、`mechanical_manufacturing_route_cn.md`、`coding_agent_route_cn.md`、`production_deployment_ops_route_cn.md`。

## 6. 许可

本仓库没有统一的许可证。每份资料保留其原有许可，并由原作者或出版方持有版权，逐文件的许可证见 `manifests/public_file_licenses.csv`。

如果你是权利人，并认为某个文件不应放在这里，请开一个 issue，我会尽快处理。
