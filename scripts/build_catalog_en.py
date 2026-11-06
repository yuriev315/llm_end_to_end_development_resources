"""Build root registers and per-project Chinese entry cards from state/*.json.

usage: python3 -I build_catalog_en.py

Outputs (root): resource_catalog_cn.csv, project_readiness_cn.csv, dependency_matrix_cn.csv,
progress_cn.csv, download_failures_cn.csv; project_cards/<id>_cn.md.
README excerpts are read from the cached clones as data (quoted, never executed).
"""
import csv
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common_en import CLONES, MODULES, ROOT, ROUTES, SEEDS, STATE, load_json  # noqa: E402

WINDOW = "2023-10-29"
HW_RE = re.compile(r"\b(\d+\s*(?:x|×)\s*(?:H100|A100|H200|B200|GPU)s?|H100|A100|H200|B200|VRAM|GPU memory|\d+\s*GB\b|CUDA\s*\d+|ROCm|CPU[- ]only|Apple Silicon|8xH100|node)", re.I)
HF_RE = re.compile(r"huggingface\.co/(datasets/)?([A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+)")
MANUAL = load_json(SEEDS / "manual_notes_cn.json", {})  # optional hand-checked notes per project id


def w(path, header, rows):
    with open(ROOT / path, "w", encoding="utf-8-sig", newline="") as f:
        cw = csv.writer(f)
        cw.writerow(header)
        cw.writerows(rows)


def clone_root(pid):
    d = CLONES / pid
    if not d.exists():
        return None
    kids = [k for k in d.iterdir() if k.is_dir() and k.name != ".git"]
    if not (d / "README.md").exists() and len(kids) == 1 and not any(d.glob("README*")):
        return kids[0]
    return d


def readme_excerpts(pid, st):
    d = clone_root(pid)
    hw, hf = [], []
    if not d:
        return hw, hf
    for rd in (st.get("static", {}).get("readme") or [])[:1]:
        p = d / rd
        if not p.exists():
            continue
        for i, line in enumerate(p.read_text(errors="replace").splitlines(), 1):
            t = line.strip()
            if len(hw) < 6 and HW_RE.search(t) and 15 < len(t) < 300 and not t.startswith(("<img", "![", "[![")):
                hw.append(f"{rd}:{i}: {t[:220]}")
            for m in HF_RE.finditer(t):
                ident = ("数据集 " if m.group(1) else "模型/空间 ") + m.group(2).rstrip(".)")
                if ident not in hf and len(hf) < 10:
                    hf.append(ident)
    return hw, hf


def mods_of(seed):
    return [seed.get("mod", "")] + [x for x in seed.get("x", []) if x]


def route_names(r):
    return "；".join(ROUTES[x] for x in (r or "").split(",") if x in ROUTES)


def verify_cmds(s):
    st = s.get("static", {})
    cmds = []
    if any(f.endswith("uv.lock") for f in st.get("lock_files", [])):
        cmds.append("uv sync --frozen  # 隔离虚拟环境，按锁文件安装")
    elif st.get("requires_python") or "pyproject.toml" in st.get("dep_files", []):
        cmds.append("python -m venv .venv && . .venv/bin/activate && pip install -e .  # 按 pyproject 安装")
    elif st.get("req_files"):
        cmds.append(f"python -m venv .venv && . .venv/bin/activate && pip install -r {st['req_files'][0]}")
    if st.get("npm_scripts"):
        lock = "pnpm install --frozen-lockfile" if any("pnpm-lock" in x for x in st.get("lock_files", [])) else "npm ci"
        cmds.append(lock)
    if st.get("tests"):
        if st.get("npm_scripts") and "test" in st.get("npm_scripts", []):
            cmds.append("npm test")
        else:
            cmds.append(f"pytest -x -q {st['tests'][0]}  # 先挑 CPU 可跑的单元测试子集")
    if st.get("compose"):
        cmds.append(f"docker compose -f {st['compose'][0]} config  # 仅校验编排文件，不启动")
    return cmds


def main():
    projects = [load_json(p) for p in sorted((STATE / "projects").glob("*.json"))]
    papers = [load_json(p) for p in sorted((STATE / "papers").glob("*.json"))]
    mats = [load_json(p) for p in sorted((STATE / "materials").glob("*.json"))]
    cat, ready, deps, fails = [], [], [], []
    cards = ROOT / "project_cards"
    cards.mkdir(exist_ok=True)
    for s in projects:
        seed = s.get("seed", {})
        st = s.get("static", {})
        kind = "官方文档" if seed.get("dir", "").endswith("official_docs") else "源码项目"
        if s.get("status") != "done":
            excl = s.get("status") == "excluded"
            fails.append([s["id"], kind, s.get("repo", ""), f"https://github.com/{s.get('repo','')}", s.get("error", ""),
                          "已下载但按规则排除，不计入" if excl else "下载失败", "待上游补充许可证后重新收录" if excl else "重试或换源"])
            continue
        mods = mods_of(seed)
        lic = st.get("license_guess") or ("、".join(st.get("license_files", [])) or "未见许可证文件")
        lfs = f"LFS 指针 {st.get('lfs_pointer_files',0)} 个" if st.get("lfs_pointer_files") else ("声明 LFS 规则但快照无指针" if st.get("lfs_patterns") else "无")
        subs = "；".join(f"{x['path']}→{x['url']}@{x['commit'][:10]}" for x in st.get("submodules", [])) or "无"
        missing_comp = []
        for key, label in [("tests", "测试"), ("ci", "CI 配置"), ("docker", "Dockerfile"), ("compose", "Compose"), ("lock_files", "依赖锁文件")]:
            if not st.get(key):
                missing_comp.append(label)
        note = f"组件缺失：{'、'.join(missing_comp) or '无'}；子模块未随快照下载：{subs if subs!='无' else '无'}；LFS：{lfs}"
        cat.append([s["id"], kind, " ".join(MODULES[m][1] for m in mods if m in MODULES), seed.get("mod"), "、".join(mods[1:]),
                    route_names(seed.get("routes")), seed.get("role", ""), s.get("repo", ""), seed.get("purpose", ""), s.get("upstream", ""),
                    s.get("version", ""), s.get("kind", ""), s.get("commit", ""), s.get("commit_date", ""), s.get("archive", ""),
                    s.get("archive_mb", ""), lic, s.get("source", "新下载"), "完整快照（工作树，不含 .git）",
                    f"文件 {st.get('file_count','')} 个；{s.get('level','')}", s.get("access_date", ""), note])
        hw, hf = readme_excerpts(s["id"], s)
        man = MANUAL.get(s["id"], {})
        ev = []
        if st.get("license_files"):
            ev.append("许可证 " + "、".join(st["license_files"][:2]))
        if st.get("dep_files") or st.get("req_files"):
            ev.append("依赖 " + "、".join((st.get("dep_files") or st.get("req_files"))[:3]))
        entries = st.get("py_scripts") or st.get("entry_files") or st.get("makefile") or []
        if entries:
            ev.append("入口 " + "、".join(entries[:4]))
        if st.get("readme_commands"):
            ev.append(f"README 命令 {len(st['readme_commands'])} 条")
        lvl = man.get("level") or s.get("level", "L0")
        if kind == "官方文档" or seed.get("role") in ("规范文档", "运行手册", "接口规范", "安全规范"):
            lvl, man = "不适用（文档/规范）", dict(man, level_note="文档或规范类资料，不评定可运行性")
        lvl_note = man.get("level_note") or ("静态核对（自动）：许可证/依赖声明/入口/安装说明齐备" if lvl == "L1" else "缺：" + "、".join(s.get("level_missing", [])))
        cmds = man.get("verify_cmds") or verify_cmds(s)
        ready.append([s["id"], s.get("repo", ""), s.get("version", ""), s.get("commit", "")[:12], lvl, lvl_note, "；".join(ev),
                      "、".join(entries[:6]), "、".join(st.get("config_dirs", [])[:5]) + (f"（配置类文件 {st.get('config_files',0)} 个）" if st.get("config_files") else ""),
                      f"{st.get('test_file_count',0)} 个测试文件；目录 " + "、".join(st.get("tests", [])[:4]) if st.get("tests") else "未见",
                      "、".join(Path(x).name for x in st.get("ci", [])[:6]) + (f" 等 {len(st['ci'])} 个" if len(st.get("ci", [])) > 6 else "") or "未见",
                      "；".join(filter(None, ["Docker: " + "、".join(st.get("docker", [])[:3]) if st.get("docker") else "",
                                               "Compose: " + "、".join(st.get("compose", [])[:3]) if st.get("compose") else "",
                                               "Helm/K8s: " + "、".join(st.get("helm_k8s", [])[:3]) if st.get("helm_k8s") else ""])) or "未见",
                      lfs, subs, man.get("blockers", "见依赖矩阵外部资源列；未逐项核对" if not hf else "需外部模型/数据（见依赖矩阵）"),
                      " && ".join(cmds) or "需人工确定", man.get("conditions", "隔离环境（容器或虚拟机），默认 CPU；仅在确认外部资源与许可后运行"),
                      "否（本轮未执行任何上游代码）"])
        deps.append([s["id"], s.get("repo", ""), s.get("version", ""), st.get("requires_python", ""), st.get("torch_spec", ""),
                     "、".join(st.get("dep_files", [])[:5]), "、".join(st.get("lock_files", [])[:4]) or "无锁文件",
                     str(st.get("node_engines", "")) if st.get("node_engines") else "", "、".join(st.get("optional_groups", [])[:8]),
                     "是（README 提及 GPU/CUDA）" if st.get("readme_mentions_gpu") else "README 未提及",
                     " | ".join(hw) or "README 未见硬件说明", "；".join(hf) or "README 未见 Hugging Face 资源链接",
                     man.get("external", ""), man.get("access", ""), s.get("head_commit_date", ""), s.get("archived", ""),
                     lic])
        card = [f"# {s['id']} {s.get('repo','')}（中文入口说明）", "",
                f"- 用途：{seed.get('purpose','')}",
                f"- 路线：{route_names(seed.get('routes'))}；角色：{seed.get('role','')}；主模块：{MODULES.get(seed.get('mod'),('',''))[1]}；关联模块：{'、'.join(MODULES[m][1] for m in mods[1:] if m in MODULES) or '无'}",
                f"- 上游：{s.get('upstream','')}；版本：{s.get('version','')}（{s.get('kind','')}）；提交：{s.get('commit','')}（{s.get('commit_date','')}）",
                f"- 默认分支最新提交日期（Atom 订阅，{s.get('access_date','')} 访问）：{s.get('head_commit_date','') or '未取得'}；归档状态：{s.get('archived','') or '未取得'}",
                f"- 本地归档：`{s.get('archive','')}`（{s.get('archive_mb','')} MB，解包后顶层目录 `{s.get('archive_prefix','')}`，内部保留上游原始路径）",
                f"- 来源方式：{s.get('source','新下载')}{('；复用自 ' + s['reuse_from']) if s.get('reuse_from') else ''}",
                f"- 许可证：{lic}（以上游 LICENSE 原文为准）", "",
                "## 静态核对（只读，未执行）", "",
                f"- 可运行性等级：**{lvl}**（{lvl_note}）",
                f"- 依赖声明：{'、'.join(st.get('dep_files', [])[:6]) or '未见'}；锁文件：{'、'.join(st.get('lock_files', [])) or '无'}；Python 要求：{st.get('requires_python') or '未声明'}；torch：{st.get('torch_spec') or '未声明'}",
                f"- 入口：{'、'.join(entries[:8]) or '未见'}；npm scripts：{'、'.join(st.get('npm_scripts', [])[:8]) or '无'}",
                f"- 配置：{'、'.join(st.get('config_dirs', [])) or '未见配置目录'}；示例目录：{'、'.join(st.get('examples_dirs', [])) or '无'}；小型示例数据：{'、'.join(st.get('sample_data', [])[:5]) or '未见'}",
                f"- 测试：{st.get('test_file_count',0)} 个测试文件；CI：{len(st.get('ci', []))} 个配置；Docker：{len(st.get('docker', []))}；Compose：{len(st.get('compose', []))}；Helm/K8s：{len(st.get('helm_k8s', []))}",
                f"- 文档：docs 类文件 {st.get('docs_files',0)} 个；变更记录：{'、'.join(st.get('changelog', [])) or '未见'}",
                f"- LFS：{lfs}；子模块：{subs}", "",
                "## 上游 README 中的硬件/资源原文摘录（引用，不代表已核实）", ""]
        card += [f"- {x}" for x in hw] or ["- 未检出相关行"]
        card += ["", "## 上游 README 提及的 Hugging Face 资源（需另行获取，未下载）", ""]
        card += [f"- {x}" for x in hf] or ["- 未检出"]
        if man:
            card += ["", "## 人工核对补充（本轮整理）", ""] + [f"- {k}：{v}" for k, v in man.items() if k not in ("level",)]
        card += ["", "## 后续最小验证（未执行，需在隔离环境中进行）", ""] + [f"- `{c}`" for c in cmds]
        card += ["", "> 本卡片由 scripts/build_catalog_en.py 依据只读静态扫描生成；未运行上游代码，不构成 L2/L3 证据，也不代表生产就绪。"]
        (cards / f"{s['id']}_cn.md").write_text("\n".join(card) + "\n", encoding="utf-8")
    pap_ok = 0
    for p in papers:
        seed = p.get("seed", {})
        if p.get("status") != "done":
            fails.append([seed.get("aid"), "论文", seed.get("title"), f"https://arxiv.org/abs/{seed.get('aid')}", p.get("reason", ""), "未计入", "人工核对或换版本"])
            continue
        pap_ok += 1
        pub = p.get("published", "")
        if not pub:
            mm = re.match(r"(\d{2})(\d{2})\.", p.get("arxiv_id", ""))
            pub = f"20{mm.group(1)}-{mm.group(2)}" if mm else ""
        recent = pub >= WINDOW[:len(pub)] if pub else False
        cat.append([f"A{p.get('arxiv_id')}", "论文", MODULES.get(seed.get("mod"), ("", ""))[1], seed.get("mod"), "", "", "研究论文",
                    p.get("title", seed.get("title")), "", p.get("url") or f"https://arxiv.org/abs/{p.get('arxiv_id')}", f"arXiv {p.get('arxiv_id')}{p.get('version','')}",
                    "首发 " + pub, "", "", p.get("path", ""), "", "arXiv 许可（见论文页）", p.get("source", ""), "完整（已核验）",
                    p.get("verify", ""), p.get("access_date", ""),
                    ("近三年" if recent else f"经典例外：{seed.get('classic') or '早于窗口'}") + (f"；复用自 {p['reuse_from']}" if p.get("reuse_from") else "")])
    for m in mats:
        if m.get("status") != "done":
            fails.append([m.get("id"), "资料", m.get("title", ""), m.get("url", m.get("src", "")), m.get("reason", ""), "未计入", "人工下载或换源"])
            continue
        kind = {"books": "教材", "courses": "课程/实践", "official_docs": "官方文档"}.get(m.get("kind"), m.get("kind"))
        comp = "完整（已核验）" if m.get("complete") else "部分资料（已核验，范围见说明）"
        cat.append([m["id"], kind, MODULES.get(m.get("mods"), ("", ""))[1], m.get("mods"), "", "", m.get("type", ""), m.get("title", ""), "",
                    m.get("url", ""), m.get("version", ""), "", "", "", m.get("path", ""), m.get("size_mb", ""), m.get("license", ""),
                    m.get("source", ""), comp, (m.get("verify") or m.get("sibling_verify", ""))[:200], m.get("access_date", ""),
                    (f"复用自 {m['reuse_from']}（源编号 {m.get('sibling_id')}）" if m.get("reuse_from") else "") + (("；范围：" + m["scope"][:150]) if m.get("scope") else "")])
    w("resource_catalog_cn.csv", ["编号", "资源类型", "模块", "主模块编号", "关联模块编号", "开发路线", "角色", "名称/上游仓库", "用途", "上游地址",
                                  "版本", "版本类型/首发", "提交号", "提交日期", "本地路径", "大小MB", "许可证", "来源方式", "完整性状态", "核验说明",
                                  "访问日期", "备注"], cat)
    w("project_readiness_cn.csv", ["编号", "项目", "版本", "提交号", "可运行性等级", "等级依据", "静态核对证据", "入口", "配置",
                                   "测试", "CI", "部署文件", "LFS", "子模块（未下载）", "运行阻塞", "下一步验证命令（未执行）", "验证条件", "是否执行过"], ready)
    w("dependency_matrix_cn.csv", ["编号", "项目", "版本", "Python 要求", "torch 规格", "依赖声明文件", "锁文件", "Node engines", "可选依赖组",
                                   "GPU 提及", "README 硬件原文摘录", "README 提及的 HF 模型/数据", "外部资源（人工核对）", "访问条件（人工核对）",
                                   "默认分支最新提交", "上游已归档", "许可证"], deps)
    w("download_failures_cn.csv", ["编号", "类型", "名称", "地址", "失败原因", "处理", "下一步"], fails)
    cnt = defaultdict(Counter)
    for r in cat:
        cnt[r[3]][r[1]] += 1
        cnt[r[3]][r[17]] += 1
    rows = []
    for m in sorted(MODULES):
        c = cnt.get(m, Counter())
        rows.append([m, MODULES[m][1], c["源码项目"], c["官方文档"], c["论文"], c["教材"], c["课程/实践"], c["新下载"], c["复用"],
                     "30–50（研究模块）" if m in ("01", "02", "03", "04", "05", "06", "07", "08", "11", "12") else "不强制"])
    w("progress_cn.csv", ["模块编号", "模块", "源码项目", "官方文档", "论文（已核验）", "教材", "课程/实践", "新下载条目", "复用条目", "论文目标"], rows)
    # module index files: projects stored here + cross-module projects (stored once elsewhere) + papers
    by_dir = defaultdict(list)
    for m, (d, name) in MODULES.items():
        by_dir[d].append((m, name))
    for d, mods in by_dir.items():
        codes = {m for m, _ in mods}
        lines = [f"# {d}/ 模块索引（{'、'.join(f'{m} {n}' for m, n in mods)}）", "",
                 "外层归档为本库命名（含 _en 语言后缀）；解包后内部保持上游原始路径。每个项目的中文入口说明见 project_cards/<编号>_cn.md。", "",
                 "## 存放于本目录的项目", "", "| 编号 | 项目 | 版本 | 路线 | 角色 | 等级 | 归档 |", "|---|---|---|---|---|---|---|"]
        for s2 in projects:
            sd = s2.get("seed", {})
            if s2.get("status") == "done" and sd.get("mod") in codes and not sd.get("dir"):
                lines.append(f"| {s2['id']} | {s2.get('repo')} | {s2.get('version')} | {sd.get('routes')} | {sd.get('role')} | {s2.get('level')} | `{Path(s2['archive']).name}` |")
        lines += ["", "## 跨模块关联项目（只保存一份，存放在其主模块目录）", "", "| 编号 | 项目 | 存放位置 | 用途 |", "|---|---|---|---|"]
        for s2 in projects:
            sd = s2.get("seed", {})
            if s2.get("status") == "done" and codes & set(sd.get("x", [])) and (sd.get("mod") not in codes or sd.get("dir")):
                lines.append(f"| {s2['id']} | {s2.get('repo')} | `{s2['archive']}` | {sd.get('purpose')} |")
        pp = [p for p in papers if p.get("status") == "done" and p["seed"]["mod"] in codes]
        if pp:
            lines += ["", f"## 本模块论文（{len(pp)} 篇，存放于 papers_books_courses/papers/<模块编号>/）", ""]
            lines += [f"- {p.get('title')}（arXiv {p.get('arxiv_id')}{p.get('version','')}；`{p.get('path')}`）" for p in sorted(pp, key=lambda x: x.get("path", ""))]
        (ROOT / d).mkdir(exist_ok=True)
        (ROOT / d / "README_cn.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"catalog {len(cat)}; projects {len(ready)}; papers ok {pap_ok}; materials ok {sum(1 for m in mats if m.get('status')=='done')}; failures {len(fails)}")


if __name__ == "__main__":
    main()
