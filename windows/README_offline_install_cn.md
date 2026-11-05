# 离线安装说明（Windows 10/11 x64，Ubuntu）

Release 资产都以 `llm_e2e_incremental_20261104_` 开头。按需下载后解压到同一个目录，例如 `D:\llm_e2e`。

| 用途 | 需要的资产 |
|---|---|
| Windows 基础依赖（每个项目一组） | `pack_windows_min_*`、`min_install_*` |
| Windows 全部依赖分组 | 再加 `pack_windows_rest_*` |
| Ubuntu | `pack_ubuntu_wheels_*`、`min_install_*` |
| 最小模型和样例数据 | `pack_models_datasets_*` |

```bat
mkdir D:\llm_e2e\dl
gh release download llm-e2e-full-20261029 --repo yuriev315/llm_end_to_end_development_resources --dir D:\llm_e2e\dl --pattern "llm_e2e_incremental_20261104_pack_windows_min_*" --pattern "llm_e2e_incremental_20261104_min_install_*"
cd /d D:\llm_e2e
for %f in (dl\*.tar dl\*.tar.gz) do tar -xf "%f"
```

项目源码不在增量里，要从原有的 `batch` 包获取，见仓库的 `download_restore_cn.md`。

## Windows：基础依赖

安装 64 位 Python，勾选 py launcher。大多数项目用 3.10，其他版本写在 `.bat` 的第一行注释里。虚拟环境建在当前目录：

```bat
mkdir D:\work\P0103 & cd /d D:\work\P0103
D:\llm_e2e\windows\min_projects\P0103\install_base.bat
.venv_P0103\Scripts\activate.bat
```

缺 wheel 时，`.bat` 会停止并给出下载命令，例如：

```bat
powershell -ExecutionPolicy Bypass -File D:\llm_e2e\windows\download_missing_wheels.ps1 -Project P0103
```

## Windows：其他依赖分组

脚本在 `windows\all_projects\<项目ID>\`，每个分组一个 `install_<分组>.bat`。缺 wheel 时用 `windows\download_wheels_all.ps1 -Project <项目ID>`。

GPU：`windows\projects\<项目ID>\install_*_gpu_*.bat`。CUDA 版 `torch` 单个 2.4 GB 以上，先从 `windows\wheelhouse\gpu\` 下的 `.url` 下载。

## Ubuntu

```bash
mkdir -p ~/work/P0102 && cd ~/work/P0102
bash /path/to/ubuntu/projects/P0102/install_base.sh
. .venv_P0102/bin/activate
```

缺 wheel 时运行 `bash /path/to/ubuntu/download_wheels_all.sh P0102`。需要 glibc 2.35 或更新版本，以及脚本要求的 Python 版本。Ubuntu 只覆盖根依赖。

## 模型和数据

文件在 `run_data/`。超过 100 MiB 的只有 `.url`，放在 `run_install_*` 里。`manifests/run_resources.csv` 列出每个仓库覆盖了什么。

这些模型是项目引用过的最小可用模型，**不一定是项目默认用的模型**。数据集大多只是样例，不是完整数据。

## 验证情况

- Windows：1,409 组依赖做过离线解析，1,229 组只靠归档内的 wheel 就能通过，其余 180 组要先下载超过 100 MiB 的 wheel。`.bat` 和 `.ps1` 没有在真实 Windows 上运行过。
- Ubuntu：4 个小项目做过真实离线安装。
- 项目本身没有运行过。
