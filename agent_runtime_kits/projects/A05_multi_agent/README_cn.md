# A05 多 Agent 协作

## 状态

- 云 API 必需：否（可选）。CrewAI 文档默认云厂商  
- 可连接本地模型：是（两个框架都走 OpenAI 兼容，但 **openai 主版本不同**）  
- 离线资源已备齐：mock 协作代码、AG2/CrewAI Linux 与 Windows wheel 已写；**未执行**  
- 已断网运行验证：**否**

## 为什么拆两个环境

CrewAI 1.15.33 → `openai` 2.x  
AG2 1.2.2 → `openai` 3.x  

混装会解析失败。mock 脚本不导入二者，用标准库即可阅读角色 / 共享状态 / 预算 / 失败处理。

角色：researcher → writer → critic。共享状态在内存 dataclass。成本按估算 token。写作者失败则停止。

Windows 上 CrewAI 的 `uvicorn[standard]` 依赖 `uvloop`（仅 POSIX）。在 Linux 主机上用 `pip download --platform win_amd64` 时，标记按**主机**求值，会错误地去拉 uvloop 并失败。Linux wheelhouse 已备齐；Windows CrewAI 若重试仍空，只能在 Windows 本机再解析，或安装不带 `[standard]` 的 uvicorn。AG2 的 Windows wheelhouse 不受此影响。
