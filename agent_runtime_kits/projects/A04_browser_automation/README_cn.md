# A04 浏览器自动化

## 状态

- 云 API 必需：browser-use 的云浏览器/BU 模型路径是可选云服务，**本项目示例不依赖**  
- 可连接本地模型：Playwright 脚本本身可不接 LLM；若用 browser-use 则需模型  
- 离线资源已备齐：本地 `shop.html`、Playwright wheel、CFT Chromium zip 已写；**未解压未执行**  
- 已断网运行验证：**否**

## Python 版本

| 版本 | 内容 |
|---|---|
| 3.10 | Playwright + 自定义脚本。 **不上 browser-use**（上游 ≥3.11） |
| 3.12 | 上述 + browser-use 0.13.14 wheel |

mock 模式只读 HTML 字符串，**不是**浏览器自动化。

浏览器 zip 还要按 Playwright 的目录布局解压并设置 `PLAYWRIGHT_BROWSERS_PATH`。本轮未解压、未启动 Chromium。
