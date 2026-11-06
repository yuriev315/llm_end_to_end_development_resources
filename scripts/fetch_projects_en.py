"""Snapshot upstream projects and run a read-only static check.

usage: python3 -I fetch_projects_en.py [--only P0101,P0102] [--redo]

Per project: choose version (tag regex / default-branch HEAD) with git ls-remote,
shallow clone (GIT_LFS_SKIP_SMUDGE=1, no submodules), record commit + dates, scan files
(licence, tests, CI, Docker/Compose/Helm, dependency/lock files, entry points, configs,
LFS pointers, submodules), then tar the working tree (without .git) into the module dir
as <id>_<owner>_<name>_<ver>_src_en.tar. Nothing from the clone is executed or imported.
State: state/projects/<id>.json (resume: done items are skipped unless --redo).
"""
import argparse
import configparser
import json
import os
import re
import shutil
import subprocess
import sys
import time
import tomllib
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common_en import ACCESS_DATE, CLONES, MODULES, ROOT, SEEDS, STATE, http, load_json, save_json  # noqa: E402

ENV = dict(os.environ, GIT_LFS_SKIP_SMUDGE="1", GIT_TERMINAL_PROMPT="0")
SKIP_DIRS = {".git", "node_modules", "__pycache__"}
DEP_FILES = ("pyproject.toml", "setup.py", "setup.cfg", "requirements.txt", "package.json", "go.mod",
             "Cargo.toml", "CMakeLists.txt", "environment.yml", "environment.yaml", "Gemfile", "pom.xml", "build.gradle")
LOCK_FILES = ("uv.lock", "poetry.lock", "pdm.lock", "Pipfile.lock", "package-lock.json", "pnpm-lock.yaml",
              "yarn.lock", "bun.lock", "bun.lockb", "Cargo.lock", "go.sum", "conda-lock.yml", "requirements.lock")
CMD_RE = re.compile(r"^\s*(?:\$\s*)?((?:pip|pip3|uv|python|python3|docker|docker-compose|make|npm|pnpm|yarn|bash|sh|"
                    r"torchrun|accelerate|deepspeed|vllm|sglang|llamafactory-cli|lm_eval|inspect|helm|kubectl|cmake|"
                    r"cargo|go|litgpt|aider|openhands|sweagent|promptfoo|garak|git clone|conda|poetry|tox|pytest)\b.*)$")


def run(cmd, cwd=None, timeout=1800):
    p = subprocess.run(cmd, cwd=cwd, env=ENV, capture_output=True, text=True, timeout=timeout)
    return p.returncode, p.stdout, p.stderr


def numkey(m):
    return tuple(int(g) if g is not None else -1 for g in m.groups())


def choose_version(repo, tag_rule):
    url = f"https://github.com/{repo}"
    rc, out, err = run(["git", "ls-remote", "--symref", url, "HEAD"], timeout=120)
    if rc != 0:
        return None, f"ls-remote 失败：{err.strip()[:200]}"
    branch = re.search(r"ref: refs/heads/(\S+)\s+HEAD", out)
    head_sha = re.search(r"^([0-9a-f]{40})\s+HEAD", out, re.M)
    info = {"default_branch": branch.group(1) if branch else "", "head_commit": head_sha.group(1) if head_sha else ""}
    if tag_rule == "HEAD":
        info.update(ref=info["default_branch"], version=f"{info['default_branch']}@{info['head_commit'][:10]}", kind="分支快照")
        return info, ""
    rc, out, err = run(["git", "ls-remote", "--tags", "--refs", url], timeout=300)
    rx = re.compile(tag_rule)
    best = None
    for line in out.splitlines():
        name = line.split("refs/tags/", 1)[-1]
        m = rx.match(name)
        if m and (best is None or numkey(m) > best[0]):
            best = (numkey(m), name)
    if not best:
        info.update(ref=info["default_branch"], version=f"{info['default_branch']}@{info['head_commit'][:10]}",
                    kind="分支快照（无匹配发布标签）")
        return info, ""
    info.update(ref=best[1], version=best[1], kind="发布标签")
    return info, ""


def maintenance(repo, branch):
    """Latest default-branch commit date via the public Atom feed; archived flag via repo page (no API quota)."""
    res = {"head_commit_date": "", "archived": ""}
    r = http(f"https://github.com/{repo}/commits/{branch}.atom", timeout=60, tries=2)
    if r.get("body"):
        m = re.search(rb"<updated>([^<]+)</updated>", r["body"])
        res["head_commit_date"] = m.group(1).decode()[:10] if m else ""
    r = http(f"https://github.com/{repo}", timeout=60, tries=2)
    if r.get("body"):
        res["archived"] = "是" if b"This repository was archived by the owner" in r["body"] else "否"
    return res


def rel(p, base):
    return str(p.relative_to(base))


def scan(d):
    files = []
    for root, dirs, fs in os.walk(d):
        dirs[:] = [x for x in dirs if x not in SKIP_DIRS]
        for f in fs:
            files.append(Path(root) / f)
    s = {"file_count": len(files), "size_mb": round(sum(f.stat().st_size for f in files if f.is_file() and not f.is_symlink()) / 1e6, 1)}
    names = [rel(f, d) for f in files]
    low = [n.lower() for n in names]
    top = [n for n in names if "/" not in n]
    s["license_files"] = [n for n in names if re.match(r"^(licen[cs]e|copying|notice)([._-].*)?$", n.lower())][:6]
    s["license_guess"] = ""
    for lf in s["license_files"]:
        try:
            head = (d / lf).read_text(errors="replace")[:3000]
        except OSError:
            continue
        for pat, name in [(r"Apache License\s+Version 2\.0", "Apache-2.0"), (r"MIT License|Permission is hereby granted, free of charge", "MIT"),
                          (r"BSD 3-Clause|Redistribution and use in source and binary forms", "BSD 类"), (r"GNU AFFERO GENERAL PUBLIC LICENSE", "AGPL-3.0"),
                          (r"GNU LESSER GENERAL PUBLIC LICENSE", "LGPL"), (r"GNU GENERAL PUBLIC LICENSE", "GPL"), (r"Mozilla Public License", "MPL-2.0"),
                          (r"Creative Commons Attribution-ShareAlike|CC BY-SA", "CC-BY-SA"), (r"Creative Commons", "CC 类"),
                          (r"Elastic License", "Elastic-2.0"), (r"Open WebUI License", "Open WebUI License（BSD-3 加品牌条款）"),
                          (r"LLAMA \d|Llama \d(\.\d)? Community License", "Llama 社区许可"), (r"CC0", "CC0")]:
            if re.search(pat, head):
                s["license_guess"] = name if not s["license_guess"] else s["license_guess"]
                if "Apache" in name and re.search(r"additional conditions|multi-tenant", head, re.I):
                    s["license_guess"] = "Apache-2.0 附加条件（见 LICENSE）"
                break
    s["tests"] = sorted({n.split("/")[0] if n.split("/")[0] in ("tests", "test") else "/".join(n.split("/")[:2])
                         for n in names if re.search(r"(^|/)(tests?|__tests__|e2e)(/|$)", n) or re.search(r"(^|/)test_[^/]+\.py$|_test\.(py|go)$|\.(test|spec)\.(ts|js)$", n)})[:12]
    s["test_file_count"] = sum(1 for n in names if re.search(r"(^|/)test_[^/]+\.py$|_test\.(py|go)$|\.(test|spec)\.(ts|tsx|js)$", n))
    s["ci"] = [n for n in names if n.startswith(".github/workflows/") or n in (".gitlab-ci.yml", ".travis.yml", "azure-pipelines.yml", "Jenkinsfile") or n.startswith(".circleci/") or n.startswith(".buildkite/")]
    s["docker"] = [n for n in names if re.search(r"(^|/)(Dockerfile[^/]*|[^/]*\.Dockerfile|containerfile)$", n, re.I)][:15]
    s["compose"] = [n for n in names if re.search(r"(^|/)(docker-)?compose[^/]*\.ya?ml$", n, re.I)][:10]
    s["helm_k8s"] = [n for n in names if re.search(r"(^|/)(Chart\.yaml|kustomization\.ya?ml|values\.yaml)$", n)][:10]
    s["dep_files"] = [n for n in names if Path(n).name in DEP_FILES and n.count("/") <= 2][:12]
    s["req_files"] = [n for n in names if re.search(r"(^|/)requirements[^/]*\.(txt|in)$", n) and n.count("/") <= 2][:10]
    s["lock_files"] = [n for n in names if Path(n).name in LOCK_FILES and n.count("/") <= 2][:10]
    s["docs_files"] = sum(1 for n in low if n.startswith(("docs/", "doc/", "documentation/", "website/docs")))
    s["config_files"] = sum(1 for n in low if re.search(r"(^|/)(configs?|recipes?|examples?)/.*\.(ya?ml|toml|json)$", n))
    s["config_dirs"] = sorted({n.split("/")[0] + ("/" + n.split("/")[1] if n.count("/") > 1 else "") for n in names
                              if re.search(r"(^|/)(configs?|recipes?)/", n)})[:8]
    s["examples_dirs"] = sorted({n.split("/")[0] for n in names if re.match(r"(examples?|samples?|cookbook|notebooks?|tutorials?)/", n.lower())})
    s["sample_data"] = [n for n in names if re.search(r"(^|/)(data|datasets?|samples?|fixtures)/[^/]+\.(jsonl|json|csv|parquet|txt)$", n, re.I) and (d / n).is_file() and (d / n).stat().st_size < 5_000_000][:8]
    s["readme"] = [n for n in top if n.lower().startswith("readme")]
    s["changelog"] = [n for n in top if re.match(r"(changelog|changes|history|release)", n.lower())]
    s["makefile"] = [n for n in names if Path(n).name in ("Makefile", "justfile", "Taskfile.yml", "noxfile.py", "tox.ini") and n.count("/") <= 1]
    # LFS
    ga = d / ".gitattributes"
    s["lfs_patterns"] = re.findall(r"^(\S+).*filter=lfs", ga.read_text(errors="replace"), re.M)[:10] if ga.exists() else []
    lfs_ptr = []
    for f in files:
        try:
            if f.is_file() and f.stat().st_size < 300 and f.read_bytes().startswith(b"version https://git-lfs"):
                lfs_ptr.append(rel(f, d))
        except OSError:
            pass
    s["lfs_pointer_files"] = len(lfs_ptr)
    s["lfs_pointer_examples"] = lfs_ptr[:5]
    # submodules
    subs = []
    gm = d / ".gitmodules"
    if gm.exists():
        cp = configparser.ConfigParser()
        try:
            cp.read_string(gm.read_text(errors="replace"))
            for sec in cp.sections():
                path = cp[sec].get("path", "")
                _, out, _ = run(["git", "ls-tree", "HEAD", path], cwd=d)
                sha = out.split()[2] if out.split() else ""
                subs.append({"path": path, "url": cp[sec].get("url", ""), "commit": sha})
        except configparser.Error:
            subs.append({"path": "?", "url": ".gitmodules 解析失败", "commit": ""})
    s["submodules"] = subs
    # python / node requirements and entry points
    s["requires_python"], s["py_scripts"], s["torch_spec"] = "", [], ""
    pp = d / "pyproject.toml"
    if pp.exists():
        try:
            t = tomllib.loads(pp.read_text(errors="replace"))
            proj = t.get("project", {})
            s["requires_python"] = proj.get("requires-python", "")
            s["py_scripts"] = list((proj.get("scripts") or {}).keys())[:10] or list((t.get("tool", {}).get("poetry", {}).get("scripts") or {}).keys())[:10]
            deps = proj.get("dependencies", []) or []
            s["torch_spec"] = ", ".join(x for x in deps if re.match(r"torch\b", x))[:80]
            s["dep_count"] = len(deps)
            s["optional_groups"] = list((proj.get("optional-dependencies") or {}).keys())[:12]
        except Exception as e:  # malformed toml
            s["pyproject_error"] = str(e)[:120]
    if not s["torch_spec"]:
        for rf in s["req_files"][:4]:
            m = re.search(r"^torch\s*[=<>~!].*$", (d / rf).read_text(errors="replace"), re.M)
            if m:
                s["torch_spec"] = f"{rf}: {m.group(0).strip()}"[:80]
                break
    pj = d / "package.json"
    if pj.exists():
        try:
            j = json.loads(pj.read_text(errors="replace"))
            s["node_engines"] = j.get("engines", {})
            s["npm_scripts"] = list((j.get("scripts") or {}).keys())[:15]
        except Exception:
            pass
    s["entry_files"] = [n for n in names if n.count("/") <= 1 and re.search(r"(^|/)(main|train|run|serve|server|app|cli|finetune|pretrain|evaluate|eval)[^/]*\.(py|sh|ts|js)$", n)][:10]
    # README commands (documentation only; never run)
    cmds = []
    for rd in s["readme"][:1]:
        in_code = False
        for line in (d / rd).read_text(errors="replace").splitlines():
            if line.strip().startswith("```"):
                in_code = not in_code
                continue
            if in_code:
                m = CMD_RE.match(line)
                if m and len(cmds) < 15:
                    cmds.append(m.group(1).strip()[:200])
        txt = (d / rd).read_text(errors="replace").lower()
        s["readme_has_install"] = bool(re.search(r"install|安装|quick ?start|getting started", txt))
        s["readme_mentions_gpu"] = bool(re.search(r"\bcuda\b|\bgpu\b|nvidia", txt))
    s["readme_commands"] = cmds
    return s


def level(s):
    miss = []
    if not s["license_files"]:
        miss.append("许可证文件")
    if not (s["dep_files"] or s["req_files"]):
        miss.append("依赖声明")
    if not (s["py_scripts"] or s.get("npm_scripts") or s["makefile"] or s["entry_files"] or s["readme_commands"]):
        miss.append("明确入口")
    if not s.get("readme_has_install"):
        miss.append("安装/运行说明")
    return ("L1" if not miss else "L0"), miss


def safe(v):
    return re.sub(r"[^A-Za-z0-9._-]+", "-", v).strip("-")


def process(seed, redo=False):
    sid, repo = seed["id"], seed["repo"]
    st_path = STATE / "projects" / f"{sid}.json"
    st = load_json(st_path, {})
    if st.get("status") == "done" and not redo and Path(ROOT / st["archive"]).exists():
        return st
    if st.get("status") == "excluded" and not redo:
        return st
    st = {"id": sid, "repo": repo, "upstream": f"https://github.com/{repo}", "seed": seed, "access_date": ACCESS_DATE, "status": "started"}
    info, err = choose_version(repo, seed["tag"])
    if not info:
        st.update(status="failed", error=err)
        save_json(st_path, st)
        return st
    st.update(info)
    dest = CLONES / sid
    if dest.exists():
        shutil.rmtree(dest)
    rc, out, err = run(["git", "clone", "--depth", "1", "--single-branch", "--no-tags", "--branch", info["ref"],
                        f"https://github.com/{repo}", str(dest)], timeout=3600)
    if rc != 0:
        st.update(status="failed", error=f"clone 失败：{err.strip()[-300:]}")
        save_json(st_path, st)
        return st
    _, out, _ = run(["git", "log", "-1", "--format=%H|%cI|%s"], cwd=dest)
    sha, cdate, subj = (out.strip().split("|", 2) + ["", ""])[:3]
    st.update(commit=sha, commit_date=cdate[:10], commit_subject=subj[:120])
    st["static"] = scan(dest)
    st["level"], st["level_missing"] = level(st["static"])
    st.update(maintenance(repo, info["default_branch"]))
    mdir = seed.get("dir") or MODULES[seed["mod"]][0]
    owner, name = repo.split("/")
    arch = Path(mdir) / f"{sid}_{safe(owner)}_{safe(name)}_{safe(info['version'])}_src_en.tar"
    prefix = f"{name}-{safe(info['version'])}"
    tmp = ROOT / (str(arch) + ".part")
    tmp.parent.mkdir(parents=True, exist_ok=True)
    rc, out, err = run(["tar", "--exclude=.git", "--sort=name", "--owner=0", "--group=0", "--numeric-owner",
                        f"--mtime={cdate or '1970-01-01'}", "--transform", f"s,^\\.,{prefix},", "-cf", str(tmp), "."], cwd=dest)
    if rc != 0:
        st.update(status="failed", error=f"tar 失败：{err[-300:]}")
        save_json(st_path, st)
        return st
    os.replace(tmp, ROOT / arch)
    st.update(archive=str(arch), archive_mb=round((ROOT / arch).stat().st_size / 1e6, 1), archive_prefix=prefix, status="done",
              finished=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
    save_json(st_path, st)
    return st


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default="")
    ap.add_argument("--redo", action="store_true")
    a = ap.parse_args()
    seeds = load_json(SEEDS / "projects_en.json")
    only = set(filter(None, a.only.split(",")))
    for s in seeds:
        if only and s["id"] not in only:
            continue
        t0 = time.time()
        try:
            st = process(s, a.redo)
        except Exception as e:  # keep going; record failure
            st = {"id": s["id"], "repo": s["repo"], "status": "failed", "error": f"{type(e).__name__}: {e}"[:300], "seed": s}
            save_json(STATE / "projects" / f"{s['id']}.json", st)
        print(f"{s['id']} {s['repo']} {st.get('status')} {st.get('version','')} {st.get('level','')} {st.get('archive_mb','')}MB "
              f"{int(time.time()-t0)}s {st.get('error','')[:120]}", flush=True)


if __name__ == "__main__":
    main()
