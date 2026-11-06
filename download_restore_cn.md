# 下载与解压恢复说明（大语言模型端到端开发资源库，2026-10-29）

本资源库按“轻量 Git 分支 + Release 全文附件”的方式发布：

- **Git 分支 `release-lite-20261029`**：只包含以下内容，不含源码快照、官方文档镜像、论文、教材和课程全文：
  - 根目录的说明与登记表：`README_cn.md`、`resource_catalog_cn.csv`、`project_readiness_cn.csv`、`dependency_matrix_cn.csv`、`progress_cn.csv`、`download_failures_cn.csv`；
  - `guides/`（路线指南与覆盖矩阵）、`project_cards/`（项目中文入口说明）、各模块目录的 `README_cn.md` 及 `input_output_pipeline/` 的说明和验证矩阵；
  - 脚本 `scripts/` 和断点状态 `state/`；
  - 本说明、分包索引和改名明细。

  上传前仓库是空的，这个分支是独立的根提交。
- **Release `llm-e2e-full-20261029`**：10 个独立的不压缩 `.tar` 包，合起来就是完整的资源库。

Release 页面：https://github.com/yuriev315/llm_end_to_end_development_resources/releases/tag/llm-e2e-full-20261029

## 1. 包列表

包按路径顺序切分，内容范围如下（文件名前缀都是 `llm_end_to_end_development_resources_20261029_`，后缀都是 `_cn_en.tar`）：

| 包 | 内容范围（按路径顺序） |
|---|---|
| `batch001` | 根目录说明与登记表、`scripts/`、`state/`、`adaptation_alignment/`、`agents_coding/`、`applications/`，以及 `data/` 的前一部分（到 P0201 datatrove） |
| `batch002` | `data/` 其余部分（P0202 docling 起），`deployment_operations/` 的 P1001 |
| `batch003` | `deployment_operations/` 其余部分（P1002 kserve 起）、`evaluation/`、`foundations/`、`guides/`，以及 `inference/` 的 P0601 vLLM |
| `batch004` | `inference/` 其余部分（P0602 llama.cpp 起），`input_output_pipeline/` 到 P1224 |
| `batch005` | `input_output_pipeline/` 其余部分（P1225 起），`papers_books_courses/books/`，以及 `courses/` 的前几门课程 |
| `batch006` | `courses/` 中间部分：CMU 11-766 其余课件，到 karpathy《Neural Networks: Zero to Hero》 |
| `batch007` | `courses/` 其余部分（OpenAI Cookbook 起），`official_docs/` 到 Langfuse 文档 |
| `batch008` | `official_docs/` 中间部分（OWASP LLM Top 10 起，到 pytest 文档） |
| `batch009` | `official_docs/` 其余部分（PyTorch 2.15 文档起），`papers/` 到 06 模块的前一部分 |
| `batch010` | `papers/` 其余部分、`project_cards/`、`rag/`、`training/` |

每个文件属于哪个包，见 `archive_index_cn.csv`。它是 UTF-8 带 BOM 编码，可直接用 Excel 打开，共 1,787 行，每行一个文件。

- 每个包都可以**单独解压**，不需要拼接。
- 包之间**没有重复文件**，解压到同一目录时不会互相覆盖。
- 包没有压缩，所需磁盘空间约等于包的大小。全部解压约需 **12.5 GiB**。如果还要展开里面的源码快照和文档镜像（见第 4 节），建议预留 30 GiB。

## 2. Windows：浏览器下载

1. 打开上面的 Release 页面，展开 **Assets**。
2. 依次点击 10 个 `.tar` 文件，以及 `archive_index_cn.csv`、`windows_rename_map_cn.csv`、`download_restore_cn.md`、`upload_report_cn.md`，全部保存到**同一个下载文件夹**，例如 `D:\下载\llm_e2e\`。
3. 单个包最大约 1.5 GB。浏览器提示“是否保留”时选择保留。下载中断时，可以在浏览器的下载列表里点“恢复”，或重新下载。
4. 对照 `upload_report_cn.md` 中的字节数，核对每个包的大小。在文件属性窗口里看“大小”一项的字节数，不要看“占用空间”。

## 3. Windows：WinRAR 解压（全部解压到同一个目标目录）

请使用 **WinRAR 6 或更新版本**，目标目录用短路径，例如 `D:\llm_e2e\`。

1. 在下载文件夹中，按住 Ctrl 选中 10 个 `.tar` 文件。
2. 右键 → **WinRAR → 解压文件…**（Extract files…）。
3. “目标路径”填 `D:\llm_e2e\`。
4. **不要**勾选“解压到单独的文件夹 / 在子文件夹中解压”（Extract archives to subfolders）。
5. 点确定。

也可以逐个解压：每个包都右键 → WinRAR → **解压文件…**，目标路径都填同一个 `D:\llm_e2e\`。不要用“解压到 llm_end_to_end_development_resources_20261029_batch0XX_cn_en\”这个菜单项，它会给每个包各建一个子文件夹，目录结构就被拆散了。

解压后的目录结构：

```
D:\llm_e2e\
├─ README_cn.md、resource_catalog_cn.csv、project_readiness_cn.csv、dependency_matrix_cn.csv …
├─ foundations\ data\ training\ adaptation_alignment\ evaluation\ inference\
├─ rag\ agents_coding\ applications\ deployment_operations\ input_output_pipeline\
├─ papers_books_courses\（papers\、books\、courses\、official_docs\）
├─ guides\ project_cards\
├─ scripts\
└─ state\
```

### Windows 兼容处理

发布包里的文件名都已经处理过，在 Windows 下解压发布包不会因为文件名报错。第一层最长相对路径 165 个字符。资源库的本地原件没有改动，每一处改动都逐条记在 `windows_rename_map_cn.csv` 里。

- **Stanford CS336 讲义的图片缓存**（`papers_books_courses/courses/Stanford_CS336_2025Spring_Lectures_en/var/files/`）：
  - 这个目录里的图片按“原网址”命名，最长的相对路径达 293 个字符，超过 Windows 资源管理器的 260 字符限制。
  - 其中 218 个路径超过 165 个字符的文件已截短文件名，并在末尾加上原文件名的 8 位哈希，例如 `image-f6740f86942b62021ef254624d82476e-https_upload_wikimedia_org_wikipedia_com_453ae1a5`。
  - 讲义轨迹文件 `var/traces/lecture_*.json` 中引用这些图片的 52 处路径已同步改写（8 个文件），配套查看器仍能找到图片。其余 171 个被改名的图片没有被任何文件引用，是缓存残留。
  - 如果在 Linux 上重新运行讲义代码，代码会按原网址名重新下载缓存图片，不影响使用。
- **44 个内层 `.tar` 已在发布包中重新打包**，其余内容不变：
  - **文件名带 Windows 不允许的字符（119 个）**：NVIDIA Nsight、NCCL、DeepSpeed、Sentence Transformers 文档镜像，Faiss Wiki，以及 Kästner《Machine Learning in Production》网页版。名字里的 `?` 等字符改成 `_`，网页中的对应链接同步改写。
  - **同一目录下只差大小写的文件（6 个）**：PyTorch 教程镜像中的 5 张图片（例如 `profiler_overview1.PNG` 与 `profiler_overview1.png`），以及 argilla 源码中的 1 个测试文件。在 Windows 下它们会互相覆盖，因此后一个加了 `_case2` 后缀，PyTorch 教程网页中的引用同步改写。
  - **符号链接（110 个）**：Windows 普通用户无法创建符号链接，WinRAR 会报错“需要管理员权限”。其中 31 个指向包内普通文件的链接，改成了目标文件的副本；另外 79 个本来就是失效链接（目标不在包内）或指向目录，已去掉，原链接目标逐条记在改名明细里。
  - 因此这 44 个文件的字节数与资源库原件不同，这是正常的。
- 其余 116 个 `.tar` 和 10 个 `.zip` 已逐个检查，没有上述问题，没有改动。

## 4. 内层归档（.tar / .zip）

资源库本身就把大部分资料整包保存。解压发布包之后，它们仍是单个文件，需要时再单独解开：

- **源码快照**：各模块目录下的 `<编号>_<owner>_<repo>_<版本>_src_en.tar`，共 97 个。解开后顶层目录是 `<repo>-<版本>`，是上游项目的工作树（不含 `.git`，子模块和 Git LFS 对象未随快照下载）。
- **官方文档镜像与课程包**：在 `papers_books_courses/official_docs/` 和 `courses/` 下。HTML 镜像解开后，用浏览器打开其中的 `index.html`。

解开方法：右键该文件 → WinRAR → **解压到 “文件名\”**。

**长路径提示**：有 5 个源码快照的包内路径超过 200 个字符，这是上游项目自身的目录结构，没有改动：Langfuse（最长 408）、OWASP LLM Top 10（234）、Ruff（224）、KServe（218）、SGLang（211）。WinRAR 可以正常解出这类长路径，但资源管理器可能无法打开最深的文件。建议把这几个包解到很短的目录（例如 `D:\L\`）。如需在资源管理器或其他工具中处理，可在 Windows 10/11 中开启长路径支持：注册表 `HKLM\SYSTEM\CurrentControlSet\Control\FileSystem` 下的 `LongPathsEnabled` 设为 1。

## 5. Linux / macOS

```bash
mkdir -p ~/llm_e2e
for f in llm_end_to_end_development_resources_20261029_batch*_cn_en.tar; do tar -xf "$f" -C ~/llm_e2e || echo "FAILED: $f"; done
```

## 6. 资料状态说明（来自资源库自身的登记表，与打包无关）

- 收录条目见 `resource_catalog_cn.csv`，各模块数量见 `progress_cn.csv`：
  - 源码项目 110 个，官方文档 54 份，论文 217 篇（只计已核验全文），教材 9 本，课程和实践包 18 个。
- 可运行性等级最高为 L1（已核对入口、依赖和配置说明）。资源库**没有安装依赖、没有运行任何上游代码**，也没有任何 L2/L3 或“生产就绪”结论。详见 `project_readiness_cn.csv`。
- 失败和按规则排除的条目记录在 `download_failures_cn.csv`，不计入，也没有对应文件。例如 2 个无许可证的仓库（HuatuoGPT-II、open-webui/docs）按规则排除。
- 模型权重、大型数据集和依赖缓存都没有下载，所需外部资源登记在 `dependency_matrix_cn.csv` 和 `project_cards/`。
- **快照时间**：本次按 2026-10-29 21:32（中欧时间）的资源库内容打包。打包前先把整个资源库复制成一份快照，打包用的就是这份快照。资源库最后一次写入是在 21:23。

## 7. 完整性说明

- 本次发布只登记了上传状态：GitHub API 显示附件为 `uploaded`，且远端大小等于本地大小。**没有**做下载回验和哈希校验。
- 资源库本身没有整库的 SHA-256 清单。
- 资源库中的资料文件都已打包，没有遗漏。只排除了资源库根目录下的本地 `.git/`（约 5.8 GB，单个提交 “first commit”，不是资料内容，也没有推送到远端）。
- CS336 两个作业仓库中的 2 个 `uv.lock` 是依赖锁文件，属于资料内容，已打包。

## 补充：版权受限文件和依赖包

- 版权受限的文件不在上面的包里。它们在 Git 分支中是同名的 `.url` 文件，`archive_index_cn.csv` 中对应行的“包文件名”为空，备注说明了原因。因此全部解压后，这些位置只有 `.url`。
- `batch011` 放的是项目运行用到的少量 Git LFS 对象。
- 依赖 wheel、安装脚本、最小模型和样例数据在以 `llm_e2e_incremental_20261104_` 开头的包里，用法见 `windows/README_offline_install_cn.md`。
- 每个包的 SHA-256 见 Release 中的 `SHA256SUMS.txt`，下载后可以用 `sha256sum -c SHA256SUMS.txt --ignore-missing` 核对。
- Release 中的 `archive_index_all_packs_cn.csv` 列出所有包（含依赖包）里的每个文件。
