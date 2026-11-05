# 通用对话助手路线

> 标记说明：〔上游〕= 上游快照中的文件明确写明；〔建议〕= 本轮自行整理的建议；〔未验证〕= 命令、配置或兼容性未经运行验证。
> 本轮未安装依赖、未运行任何上游代码，所列项目最高为 L1；不构成生产就绪结论。环节级验收条件与入口文件见 `end_to_end_coverage_cn.csv`，跨仓库组合的证据见 `compatibility_matrix_cn.csv`，项目入口说明见 `project_cards/<编号>_cn.md`。

## 项目目标

多用户对话助手：模型接入、输入处理、上下文与记忆、生成、输出处理、前后端、认证隔离、部署、监控与反馈。

## 模块组合

vLLM（P0601）+ LiteLLM（P1003）+ LibreChat（P0901）+ Presidio/detect-secrets/NeMo Guardrails（P1201/P1202/P1204）+ mem0/Qdrant（P0809/P0705）+ instructor/nh3（P1217/P1222）+ Langfuse（P1004）。

## 资料和源码路径

applications/（09）、inference/、deployment_operations/、input_output_pipeline/；文档 D0901（LibreChat 文档站源）、D1001（Langfuse 文档站源）、D0601（OpenAI API 规范）。

## 环境

Docker/Compose；GPU 节点（vLLM）；Node（LibreChat 前后端）。

## 数据格式

OpenAI Chat Completions JSON；LibreChat 会话存 MongoDB（〔上游〕docker-compose.yml）；mem0 记忆条目按 user_id/agent_id/run_id 作用域。

## 配置

LibreChat `.env.example`、`librechat.example.yaml`；LiteLLM `litellm/proxy/proxy_config.yaml`；Langfuse `docker-compose.yml`。所有密钥仅保留占位符。

## 执行顺序

见 reference_stacks_cn.md 1.3：Langfuse → vLLM → LiteLLM → 输入/输出处理服务 → LibreChat。

## 测试方法

LibreChat `e2e/`；Presidio 测试；promptfoo 回归；GuideLLM 压测；越权与注入用例（AgentDojo、XSTest）。〔未验证〕

## 部署步骤

Compose 单机 → production-stack/KServe 集群；灰度与回滚见 production_deployment_ops_route_cn.md。

## 外部依赖

模型权重或托管 API；身份提供方；MongoDB/Meilisearch；spaCy 模型（Presidio）。

## 尚未解决的问题

输入/输出处理服务与 LibreChat 的接入层无上游参考（〔建议〕自写中间层或 LiteLLM hooks）；Open WebUI 许可含品牌条款；多语言过滤误报评测缺失。
