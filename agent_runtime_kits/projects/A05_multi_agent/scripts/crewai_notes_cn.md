# CrewAI 连接说明（未执行）

钉住 1.15.33。GitHub 标签若只有 1.15.32，以实际下载的 tag/tarball 为准，并在 SNAPSHOT 中记录。

独立 wheelhouse：[`environments/A05_multi_agent_crewai_py310_linux`](../environments/A05_multi_agent_crewai_py310_linux/) 等。

CrewAI 1.15.33 依赖 `openai>=2.30,<3`，不能与 OpenAI Agents SDK 0.24 / AG2 1.2.2 共用一个 venv。

本地 OpenAI 兼容服务仍可通过 `OPENAI_API_BASE` 指向 llama-server。接口兼容不等于角色协作、工具调用或结构化输出已经可用。本轮未执行 `crew.kickoff()`。
