# 生产部署与运维路线

> 标记说明：〔上游〕= 上游快照中的文件明确写明；〔建议〕= 本轮自行整理的建议；〔未验证〕= 命令、配置或兼容性未经运行验证。
> 本轮未安装依赖、未运行任何上游代码，所列项目最高为 L1；不构成生产就绪结论。环节级验收条件与入口文件见 `end_to_end_coverage_cn.csv`，跨仓库组合的证据见 `compatibility_matrix_cn.csv`，项目入口说明见 `project_cards/<编号>_cn.md`。

## 项目目标

容器、编排、GPU 调度、配置与秘密管理、CI/CD、监控、日志、告警、扩缩容、灰度、回滚、备份恢复。

## 模块组合

production-stack（P1001）、KServe（P1002）、NVIDIA k8s-device-plugin（P1005）、LiteLLM（P1003）、Langfuse（P1004）、GuideLLM（P0607）、Temporal（P1008）、Made With ML（P1007，复用，MLOps 课程代码）。

## 资料和源码路径

deployment_operations/；文档 Docker（D15，部分）、Kubernetes（D16）、Dockerfile 参考（D17）、Prometheus（D18）、OpenTelemetry（D19）、Helm（D20）、KServe 文档站（D21）、GitHub Actions（D36）、NIST AI RMF（G02）；手册 ml-engineering（P0305）、ML Systems（B06/B07）。

## 环境

Kubernetes + NVIDIA GPU + 设备插件；Helm；镜像仓库。

## 数据格式

Helm values.yaml；KServe InferenceService YAML；Prometheus 指标；OpenTelemetry trace。

## 配置

〔上游〕production-stack `helm/values.yaml` 默认引擎镜像 `lmcache/vllm-openai:latest`（第 45–47 行）——〔建议〕必须固定标签；秘密使用 Kubernetes Secret 或外部秘密管理，清单中只放占位符。

## 执行顺序

〔建议〕helm template 渲染并审阅 → 预发环境部署 → GuideLLM 基线（吞吐/延迟/并发）→ promptfoo 质量回归 → 灰度（KServe 流量切分）→ 全量 → 保留上一版本以便回滚。

## 测试方法

production-stack tests/；KServe test/；k8s-device-plugin 测试；演练回滚与备份恢复。〔未验证〕

## 部署步骤

参照 production-stack `tutorials/` 与 KServe 文档；监控按 `observability/` 与 Prometheus 文档。

## 外部依赖

集群与 GPU；对象存储；身份与秘密管理；告警通道。

## 尚未解决的问题

无执行证据（L1）；镜像默认 latest；成本测量需结合 LiteLLM 成本记录自建；备份恢复只有通用文档。
