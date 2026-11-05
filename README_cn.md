# 大语言模型端到端开发资源库（llm_end_to_end_development_resources）

建库日期：2026-10-29。本库收集**实际开发所需**的参考源码、配置、测试、部署文件、官方文档、运行手册，以及配套教材、课程与论文，覆盖通用助手、医疗、机械制造和 Coding 应用。

> **重要声明**
> - 本轮只做了下载、静态核对和运行准备：**没有安装依赖、没有运行任何上游代码、没有训练、没有部署**。所有项目的可运行性等级最高为 L1，**没有任何 L2/L3 结论，也没有任何“生产就绪”结论**。
> - 未下载模型权重、大型数据集、依赖缓存和构建产物；所需外部资源登记在 `dependency_matrix_cn.csv` 与 `project_cards/`。
> - 配置中只保留占位符，本库不含真实凭据。
> - 教学示例不得视为可直接投入生产；医疗条目仅限研究与教学用途；机械“实际控制”类条目仅为研究原型，不得连接真实设备。
> - **版权受限资料**（NC 许可、版权保留、未见许可证、仅个人保存等）已改为 `*.url.md` 占位文件，仅保留官方来源 URL；原件备份在本机 `D:/copyright_files/`（不上传）。明细见 `copyright_placeholder_report_cn.md`。

## 1. 三条开发路线

| 路线 | 含义 | 本库主要条目 |
|---|---|---|
| A 从头训练 | 从分词器、模型定义到预训练 | P0101–P0105、P0201/P0205、P0301–P0305 |
| B 适配开放权重模型 | 持续预训练、SFT、PEFT、偏好优化、RL、蒸馏 | P0401–P0404、P0606、P0706、P1103、P1117 |
| C 使用模型服务开发应用 | 对话、RAG、智能体、专业应用、输入输出处理链 | 07–12 模块大部分条目 |

每个项目在 `resource_catalog_cn.csv` 的“开发路线”列标明所属路线；API 应用示例不被当作模型训练代码。

## 2. 目录

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
| guides/ | 路线指南与覆盖矩阵（见第 4 节） |
| project_cards/ | 每个源码/文档项目的中文入口说明 `<编号>_cn.md` |
| scripts/ | 下载、核对、登记脚本（可断点续跑）；`scripts/seeds/` 为人工整理的种子与矩阵数据 |
| state/ | 每个条目的下载与核对状态 JSON |

每个模块目录有 `README_cn.md` 索引：列出存放在本目录的项目，以及只保存一份、存放在其他模块目录的跨模块项目。

**归档规则**：上游项目以 `<编号>_<owner>_<repo>_<版本>_src_en.tar` 保存（外层名称带语言后缀）；解包后顶层目录为 `<repo>-<版本>`，内部保持上游原始文件名与路径。快照为工作树（不含 .git），**子模块和 Git LFS 对象未随快照下载**，均已在 `project_readiness_cn.csv` 中注明。

## 3. 登记表（根目录）

| 文件 | 说明 |
|---|---|
| resource_catalog_cn.csv | 全部已收录条目（源码项目、官方文档、论文、教材、课程/实践），含版本、提交号、许可证、来源方式（新下载/复用）、完整性 |
| project_readiness_cn.csv | 每个项目的可运行性等级、证据、入口、配置、测试、CI、部署文件、LFS/子模块、下一步验证命令（未执行） |
| dependency_matrix_cn.csv | Python/torch/Node 要求、依赖与锁文件、README 中硬件与 HF 资源的原文摘录、外部资源与访问条件 |
| progress_cn.csv | 各模块数量统计 |
| download_failures_cn.csv | 下载失败与按规则排除的条目 |

可运行性等级：L0 源码已下载、未完成静态核对要求；L1 已核对入口、依赖和配置说明（本轮为自动扫描 + 部分人工核对）；L2/L3 需在记录环境中实际运行，本轮均无。文档/规范类条目标“不适用”。

## 4. 指南（guides/）

- `reference_stacks_cn.md`：四条路线（通用对话助手、专业知识 RAG、Coding 智能体、模型微调与发布）的建议组合、模块接口、启动顺序、测试与部署步骤、兼容关系与待补资源。
- `end_to_end_coverage_cn.csv`：路线 × 环节覆盖矩阵（目标、验收条件、参考项目/版本/提交号/路径、入口文件——已核对存在于快照中、依赖、测试与部署文件、许可证、维护状态、下载状态、等级、缺失项、优先级）。
- `gap_backlog_cn.csv`：按 P0/P1/P2 排序的缺口清单。
- `compatibility_matrix_cn.csv`：跨仓库组合的证据（使用方快照中的引用文件、版本约束原文、自动版本比对结论）。
- `completion_report_cn.md`：本轮完成情况报告。
- 八条路线指南：`from_scratch_training_route_cn.md`、`open_weight_adaptation_route_cn.md`、`general_assistant_route_cn.md`、`domain_rag_route_cn.md`、`medical_application_route_cn.md`、`mechanical_manufacturing_route_cn.md`、`coding_agent_route_cn.md`、`production_deployment_ops_route_cn.md`。

## 5. 复用来源

复制自同机已有资料库，原件未移动或删除，来源路径记录在目录表“备注”列：
- `/root/programming_reference_literature`（官方文档、课程、实践项目、部分论文）
- `/root/ai_undergraduate_graduate_curriculum_literature`（教材与课程）

此前的大模型多模态、ML/DL、小语种资料库目录在本机已不存在，未能复用。

## 6. 续跑与重建

```bash
cd /root/llm_end_to_end_development_resources/scripts
python3 -I seeds/projects_seed_en.py        # 由种子生成 projects_en.json
python3 -I fetch_projects_en.py              # 源码快照（已完成的跳过；--only ID --redo 重做）
python3 -I reuse_projects_en.py              # 复用的项目快照
python3 -I papers_en.py [--retry-failed]     # 论文（arXiv，共享限速锁 /tmp/lmm_ratelimit）
python3 -I materials_en.py                   # 教材/课程/官方文档复用与官方 PDF
python3 -I build_catalog_en.py               # 根目录登记表、模块索引、项目卡片
python3 -I build_guides_en.py                # 覆盖矩阵、缺口、兼容矩阵、验证矩阵
python3 -I build_route_guides_en.py          # 路线指南 + 引用核对
```

缓存（克隆工作区、暂存文件、被排除的归档）位于 `/root/.cache/lede_lit/`。

## 7. 注意

- 本库根目录下出现的 `.git`（约 5.8 GB，单个提交 “first commit”，远端指向 GitHub）**不是本轮流程创建的**，内容是建库中途的部分状态。本轮未对其做任何操作，是否保留或推送由用户决定。
