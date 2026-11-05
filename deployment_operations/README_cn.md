# deployment_operations/ 模块索引（10 生产部署与维护）

外层归档为本库命名（含 _en 语言后缀）；解包后内部保持上游原始路径。每个项目的中文入口说明见 project_cards/<编号>_cn.md。

## 存放于本目录的项目

| 编号 | 项目 | 版本 | 路线 | 角色 | 等级 | 归档 |
|---|---|---|---|---|---|---|
| P1001 | vllm-project/production-stack | vllm-stack-0.1.13 | B,C | 完整工程 | L1 | `P1001_vllm-project_production-stack_vllm-stack-0.1.13_src_en.tar` |
| P1002 | kserve/kserve | v0.21.0 | B,C | 完整工程 | L1 | `P1002_kserve_kserve_v0.21.0_src_en.tar` |
| P1003 | BerriAI/litellm | v1.106.6 | C | 完整工程 | L1 | `P1003_BerriAI_litellm_v1.106.6_src_en.tar` |
| P1004 | langfuse/langfuse | v4.72.0 | C | 完整工程 | L1 | `P1004_langfuse_langfuse_v4.72.0_src_en.tar` |
| P1005 | NVIDIA/k8s-device-plugin | v0.20.1 | B,C | 单模块参考 | L1 | `P1005_NVIDIA_k8s-device-plugin_v0.20.1_src_en.tar` |
| P1006 | jd/tenacity | 9.2.1 | C | 工具库 | L0 | `P1006_jd_tenacity_9.2.1_src_en.tar` |
| P1007 | GokuMohandas/Made-With-ML（复用） | 快照日 2026-10-29 | C | 教学实现 | L1 | `P1007_MadeWithML_repo_en_src_en.tar` |
| P1008 | temporalio/sdk-python | 1.35.0 | C | 单模块参考 | L1 | `P1008_temporalio_sdk-python_1.35.0_src_en.tar` |

## 跨模块关联项目（只保存一份，存放在其主模块目录）

| 编号 | 项目 | 存放位置 | 用途 |
|---|---|---|---|
| P0207 | iterative/dvc | `data/P0207_iterative_dvc_3.67.1_src_en.tar` | 数据与模型版本管理、流水线与实验追踪（数据—模型—配置关联） |
| P0305 | stas00/ml-engineering | `training/P0305_stas00_ml-engineering_master-adab2fa873_src_en.tar` | 大模型训练与推理工程手册：硬件、网络、故障排查、调试、稳定性 |
| P0403 | hiyouga/LLaMA-Factory | `adaptation_alignment/P0403_hiyouga_LLaMA-Factory_v0.9.5_src_en.tar` | 统一微调框架：数据格式、SFT/DPO/KTO/PPO、导出合并、API 服务、Docker |
| P0601 | vllm-project/vllm | `inference/P0601_vllm-project_vllm_v0.32.0_src_en.tar` | 高吞吐推理服务：PagedAttention、连续批处理、量化、OpenAI 兼容 API、结构化输出、工具调用解析、基准脚本 |
| P0607 | vllm-project/guidellm | `inference/P0607_vllm-project_guidellm_v0.8.1_src_en.tar` | 推理服务负载测试：吞吐、延迟、并发扫描 |
| P0702 | infiniflow/ragflow | `rag/P0702_infiniflow_ragflow_v0.27.3_src_en.tar` | 完整 RAG 产品：深度文档解析、分块模板、引用、多租户、Docker Compose |
| P0803 | OpenHands/OpenHands | `agents_coding/P0803_OpenHands_OpenHands_v1.34.0_src_en.tar` | 软件开发智能体平台：沙箱运行时、权限、前后端、Docker |
| P0901 | danny-avila/LibreChat | `applications/P0901_danny-avila_LibreChat_v0.8.8_src_en.tar` | 多用户对话产品：认证、会话存储、文件上传、配额、多模型接入、Docker Compose |
| P0903 | open-webui/open-webui | `applications/P0903_open-webui_open-webui_v0.12.5_src_en.tar` | 自托管对话界面：RBAC、RAG、管道、Ollama/OpenAI 接入 |
| P0904 | langgenius/dify | `applications/P0904_langgenius_dify_1.18.0_src_en.tar` | LLM 应用平台：工作流、知识库、多租户、任务队列、Docker Compose |
