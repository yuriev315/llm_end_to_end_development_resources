"""Copy-reuse project snapshots already held by sibling libraries (never moved) and run the
same read-only static scan as fetch_projects_en.py on an extracted copy in the cache.

usage: python3 -I reuse_projects_en.py
"""
import csv
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common_en import ACCESS_DATE, CLONES, MODULES, ROOT, SEEDS, STATE, load_json, save_json  # noqa: E402
from fetch_projects_en import level, scan  # noqa: E402

SIB_CATALOGS = ["/root/programming_reference_literature/catalog_cn.csv",
                "/root/ai_undergraduate_graduate_curriculum_literature/catalog_cn.csv"]


def sibling_row(src):
    for cat in SIB_CATALOGS:
        lib = Path(cat).parent
        for r in csv.DictReader(open(cat, encoding="utf-8-sig")):
            if r.get("本地路径") and (lib / r["本地路径"]) == Path(src):
                return r
    return {}


def main():
    for s in load_json(SEEDS / "projects_reuse_en.json"):
        stp = STATE / "projects" / f"{s['id']}.json"
        if load_json(stp, {}).get("status") == "done":
            continue
        src = Path(s["src"])
        if not src.exists():
            save_json(stp, dict(id=s["id"], status="failed", error=f"复用源不存在：{src}", seed=s))
            continue
        mdir = MODULES[s["mod"]][0]
        name = src.name if src.suffix == ".tar" else src.name + "_src_en.tar"
        dest = ROOT / mdir / f"{s['id']}_{name}"
        work = CLONES / s["id"]
        if work.exists():
            shutil.rmtree(work)
        work.mkdir(parents=True)
        if src.suffix == ".tar":
            shutil.copy2(src, dest)
            subprocess.run(["tar", "-xf", str(src), "-C", str(work), "--no-same-owner"], check=True)
            inner = [p for p in work.iterdir()]
            root = inner[0] if len(inner) == 1 and inner[0].is_dir() else work
        else:
            subprocess.run(["tar", "--exclude=.git", "--sort=name", "--owner=0", "--group=0", "-cf", str(dest), "-C", str(src.parent), src.name], check=True)
            shutil.copytree(src, work / src.name, symlinks=True, ignore=shutil.ignore_patterns(".git"))
            root = work / src.name
        st = scan(root)
        lv, miss = level(st)
        r = sibling_row(src)
        save_json(stp, dict(
            id=s["id"], repo=s["title"], upstream=r.get("官方来源") or r.get("原始来源") or "", seed=dict(s, x=[], tag="复用"),
            status="done", source="复用", reuse_from=str(src), version=r.get("版本") or r.get("学期或版本") or "",
            commit=r.get("源码提交号") or "", commit_date=r.get("提交日期") or "", kind="复用快照", static=st, level=lv, level_missing=miss,
            archive=str(dest.relative_to(ROOT)), archive_mb=round(dest.stat().st_size / 1e6, 1), access_date=ACCESS_DATE,
            sibling_verify=r.get("核验结果") or r.get("核验说明") or "", head_commit_date="", archived=""))
        print(s["id"], "reused", lv, miss)


if __name__ == "__main__":
    main()
