# 下载与解压说明（大语言模型端到端开发资源库）

全部包都在 Release `llm-e2e-full-20261029`，每个约 1.5 GB，可以单独解压，解压到同一个目录即可，包之间没有重复文件。

| 资产 | 内容 |
|---|---|
| `llm_end_to_end_development_resources_20261029_batch*_cn_en.tar` | 源码快照、官方文档、论文、教材、课程 |
| `llm_e2e_incremental_20261104_pack_windows_min_*` | Windows CPU 基础依赖 |
| `llm_e2e_incremental_20261104_pack_windows_rest_*` | 其余 Windows wheel |
| `llm_e2e_incremental_20261104_pack_ubuntu_wheels_*` | Ubuntu wheel |
| `llm_e2e_incremental_20261104_pack_models_datasets_*` | 最小模型和样例数据 |
| `llm_e2e_incremental_20261104_min_install_*` | 依赖的锁文件和安装脚本 |
| `llm_e2e_incremental_20261104_final_docs_*` | 安装说明、依赖清单和生成它们的工具 |
| `archive_index_cn.csv` | 每个包的文件清单 |
| `SHA256SUMS.txt` | 每个包的 SHA-256 |

## 下载

```bash
gh release download llm-e2e-full-20261029 --repo yuriev315/llm_end_to_end_development_resources --dir ./dl --pattern "*batch*"
```

也可以在 Release 页面用浏览器逐个下载。

## 解压

Linux：

```bash
mkdir -p llm_e2e && for f in dl/*.tar; do tar -xf "$f" -C llm_e2e; done
```

Windows：在 WinRAR 中选中所有 `.tar` 文件，右键选择“解压文件”，目标路径填一个短路径，例如 `D:\llm_e2e\`，不要勾选“解压到单独的文件夹”。

源码快照是 `.tar.gz`，解压后还是单个文件，需要时再解开。

## 校验

```bash
sha256sum -c SHA256SUMS.txt --ignore-missing
```

## `.url` 文件

仓库里的 `.url` 文件和被替换的文件同名，只多一个后缀。双击可以打开原始来源，文本编辑器可以看到大小和 SHA-256，下载后可以核对。
