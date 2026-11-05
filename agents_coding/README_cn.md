# agents_coding/ 模块索引（08 智能体与 Coding）

外层归档为本库命名（含 _en 语言后缀）；解包后内部保持上游原始路径。每个项目的中文入口说明见 project_cards/<编号>_cn.md。

## 存放于本目录的项目

| 编号 | 项目 | 版本 | 路线 | 角色 | 等级 | 归档 |
|---|---|---|---|---|---|---|
| P0801 | modelcontextprotocol/python-sdk | v2.3.0 | C | 单模块参考 | L1 | `P0801_modelcontextprotocol_python-sdk_v2.3.0_src_en.tar` |
| P0802 | Aider-AI/aider | v0.86.2 | C | 完整工程 | L1 | `P0802_Aider-AI_aider_v0.86.2_src_en.tar` |
| P0803 | OpenHands/OpenHands | v1.34.0 | C | 完整工程 | L1 | `P0803_OpenHands_OpenHands_v1.34.0_src_en.tar` |
| P0804 | continuedev/continue | v2.1.0-vscode | C | 完整工程 | L0 | `P0804_continuedev_continue_v2.1.0-vscode_src_en.tar` |
| P0805 | SWE-agent/SWE-agent | v1.1.0 | C | 完整工程 | L1 | `P0805_SWE-agent_SWE-agent_v1.1.0_src_en.tar` |
| P0806 | langchain-ai/langgraph | 1.2.18 | C | 单模块参考 | L1 | `P0806_langchain-ai_langgraph_1.2.18_src_en.tar` |
| P0807 | microsoft/multilspy | v0.1.1 | C | 单模块参考 | L1 | `P0807_microsoft_multilspy_v0.1.1_src_en.tar` |
| P0808 | astral-sh/ruff | 0.17.3 | C | 单模块参考 | L1 | `P0808_astral-sh_ruff_0.17.3_src_en.tar` |
| P0809 | mem0ai/mem0 | v2.2.1 | C | 单模块参考 | L1 | `P0809_mem0ai_mem0_v2.2.1_src_en.tar` |
| P0810 | SWE-agent/mini-swe-agent（复用） | main 提交 | C | 教学实现 | L1 | `P0810_mini_swe_agent_main_en.tar` |
| P0811 | OpenHands/software-agent-sdk | v1.59.0 | C | 完整工程 | L1 | `P0811_OpenHands_software-agent-sdk_v1.59.0_src_en.tar` |

## 跨模块关联项目（只保存一份，存放在其主模块目录）

| 编号 | 项目 | 存放位置 | 用途 |
|---|---|---|---|
| P0502 | UKGovernmentBEIS/inspect_ai | `evaluation/P0502_UKGovernmentBEIS_inspect_ai_0.3.286_src_en.tar` | 评测框架：自定义任务、工具调用、沙箱、打分器、日志查看 |
| P0503 | evalplus/evalplus | `evaluation/P0503_evalplus_evalplus_v0.3.1_src_en.tar` | 代码生成执行评测（HumanEval+/MBPP+），含安全执行 |
| P0505 | SWE-bench/SWE-bench | `evaluation/P0505_SWE-bench_SWE-bench_v5.0.1_src_en.tar` | 仓库级补丁评测：Docker 构建、测试执行与判定 |
| P1111 | neka-nat/freecad-mcp | `applications/P1111_neka-nat_freecad-mcp_main-8babe9927c_src_en.tar` | FreeCAD 的 MCP 服务器（设计辅助，需本地 FreeCAD） |
| P1114 | csml-rpi/Foam-Agent | `applications/P1114_csml-rpi_Foam-Agent_main-ed8db9415e_src_en.tar` | OpenFOAM 仿真智能体：前处理、运行、错误修复（仿真辅助） |
| P1115 | midea-ai/SemaPLC | `applications/P1115_midea-ai_SemaPLC_main-fea1b87a11_src_en.tar` | PLC 结构化文本生成与验证门控（控制代码研究，不可直接下发设备） |
| P1116 | YuchenXia/LLM4IAS | `applications/P1116_YuchenXia_LLM4IAS_main-2029d581d4_src_en.tar` | 工业自动化系统 LLM 智能体（仿真/实验环境控制研究） |
| P1117 | SWE-bench/SWE-smith | `applications/P1117_SWE-bench_SWE-smith_v0.0.6_src_en.tar` | Coding 智能体训练数据合成（任务实例生成、轨迹） |
| P1210 | google-research/camel-prompt-injection | `input_output_pipeline/P1210_google-research_camel-prompt-injection_main-f083b6b396_src_en.tar` | CaMeL：控制流/数据流隔离防提示注入（研究实现） |
| P1211 | ethz-spylab/agentdojo | `input_output_pipeline/P1211_ethz-spylab_agentdojo_v0.1.35_src_en.tar` | 智能体提示注入攻防评测环境 |
| P1228 | ShishirPatil/gorilla | `input_output_pipeline/P1228_ShishirPatil_gorilla_v1.3_src_en.tar` | 含 BFCL 函数调用评测（名称/参数/多轮） |

## 本模块论文（25 篇，存放于 papers_books_courses/papers/<模块编号>/）

- ReAct: Synergizing Reasoning and Acting in Language Models（arXiv 2210.03629v3；`papers_books_courses/papers/08/2022_Yao_ReActSynergizingReasoningActingLanguage_en.pdf`）
- SWE-bench: Can Language Models Resolve Real-World GitHub Issues?（arXiv 2310.06770v3；`papers_books_courses/papers/08/2023_Jimenez_SWEBenchLanguageModelsResolve_en.pdf`）
- MemGPT: Towards LLMs as Operating Systems（arXiv 2310.08560v2；`papers_books_courses/papers/08/2023_Packer_MemGPTTowardsLLMsAsOperating_en.pdf`）
- Gorilla: Large Language Model Connected with Massive APIs（arXiv 2305.15334v1；`papers_books_courses/papers/08/2023_Patil_GorillaLargeLanguageModelConnected_en.pdf`）
- Identifying the Risks of LM Agents with an LM-Emulated Sandbox（arXiv 2309.15817v2；`papers_books_courses/papers/08/2023_Ruan_IdentifyingRisksLmAgentsLm_en.pdf`）
- Toolformer: Language Models Can Teach Themselves to Use Tools（arXiv 2302.04761v1；`papers_books_courses/papers/08/2023_Schick_ToolformerLanguageModelsTeachThemselves_en.pdf`）
- Reflexion: Language Agents with Verbal Reinforcement Learning（arXiv 2303.11366v4；`papers_books_courses/papers/08/2023_Shinn_ReflexionLanguageAgentsVerbalReinforcement_en.pdf`）
- AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation（arXiv 2308.08155v2；`papers_books_courses/papers/08/2023_Wu_AutogenEnablingNextGenLlm_en.pdf`）
- RepoCoder: Repository-Level Code Completion Through Iterative Retrieval and Generation（arXiv 2303.12570v3；`papers_books_courses/papers/08/2023_Zhang_RepocoderRepositoryLevelCodeCompletion_en.pdf`）
- Qwen2.5-Coder Technical Report（arXiv 2409.12186v3；`papers_books_courses/papers/08/2024_Hui_Qwen25CoderTechnicalReport_en.pdf`）
- Large Language Model-Based Agents for Software Engineering: A Survey（arXiv 2409.02977v2；`papers_books_courses/papers/08/2024_Liu_LargeLanguageModelBasedAgents_en.pdf`）
- StarCoder 2 and The Stack v2: The Next Generation（arXiv 2402.19173v1；`papers_books_courses/papers/08/2024_Lozhkov_Starcoder2StackV2Next_en.pdf`）
- Training Software Engineering Agents and Verifiers with SWE-Gym（arXiv 2412.21139v2；`papers_books_courses/papers/08/2024_Pan_TrainingSoftwareEngineeringAgentsVerifiers_en.pdf`）
- AppWorld: A Controllable World of Apps and People for Benchmarking Interactive Coding Agents（arXiv 2407.18901v1；`papers_books_courses/papers/08/2024_Trivedi_AppworldControllableWorldAppsPeople_en.pdf`）
- Agent Workflow Memory（arXiv 2409.07429v1；`papers_books_courses/papers/08/2024_Wang_AgentWorkflowMemory_en.pdf`）
- Executable Code Actions Elicit Better LLM Agents（arXiv 2402.01030v4；`papers_books_courses/papers/08/2024_Wang_ExecutableCodeActionsElicitBetter_en.pdf`）
- OpenHands: An Open Platform for AI Software Developers as Generalist Agents（arXiv 2407.16741v3；`papers_books_courses/papers/08/2024_Wang_OpenHandsOpenPlatformAISoftware_en.pdf`）
- Agentless: Demystifying LLM-based Software Engineering Agents（arXiv 2407.01489v2；`papers_books_courses/papers/08/2024_Xia_AgentlessDemystifyingLLMBasedSoftware_en.pdf`）
- OSWorld: Benchmarking Multimodal Agents for Open-Ended Tasks in Real Computer Environments（arXiv 2404.07972v2；`papers_books_courses/papers/08/2024_Xie_OsworldBenchmarkingMultimodalAgentsOpen_en.pdf`）
- SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering（arXiv 2405.15793v3；`papers_books_courses/papers/08/2024_Yang_SWEAgentAgentComputerInterfaces_en.pdf`）
- AutoCodeRover: Autonomous Program Improvement（arXiv 2404.05427v3；`papers_books_courses/papers/08/2024_Zhang_AutocoderoverAutonomousProgramImprovement_en.pdf`）
- Model Context Protocol (MCP): Landscape, Security Threats, and Future Research Directions（arXiv 2503.23278v3；`papers_books_courses/papers/08/2025_Hou_ModelContextProtocolMcpLandscape_en.pdf`）
- SWE-Lancer: Can Frontier LLMs Earn $1 Million from Real-World Freelance Software Engineering?（arXiv 2502.12115v4；`papers_books_courses/papers/08/2025_Miserendino_SweLancerCanFrontierLlms_en.pdf`）
- SWE-RL: Advancing LLM Reasoning via Reinforcement Learning on Open Software Evolution（arXiv 2502.18449v2；`papers_books_courses/papers/08/2025_Wei_SweRlAdvancingLlmReasoning_en.pdf`）
- SWE-smith: Scaling Data for Software Engineering Agents（arXiv 2504.21798v2；`papers_books_courses/papers/08/2025_Yang_SweSmithScalingDataSoftware_en.pdf`）
