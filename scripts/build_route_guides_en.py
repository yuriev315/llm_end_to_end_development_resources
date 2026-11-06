"""Render guides/*_route_cn.md from seeds/route_guides_cn.py, then lint every self-written
Markdown guide: each cited item id (P/D/G/B/C/X + digits) and arXiv id must be a registered,
successfully collected item.

usage: python3 -I build_route_guides_en.py
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent / "seeds"))
from common_en import ROOT, STATE, load_json  # noqa: E402
from route_guides_cn import FIELDS, GUIDES  # noqa: E402

HEAD = ("> 标记说明：〔上游〕= 上游快照中的文件明确写明；〔建议〕= 本轮自行整理的建议；〔未验证〕= 命令、配置或兼容性未经运行验证。\n"
        "> 本轮未安装依赖、未运行任何上游代码，所列项目最高为 L1；不构成生产就绪结论。环节级验收条件与入口文件见 `end_to_end_coverage_cn.csv`，"
        "跨仓库组合的证据见 `compatibility_matrix_cn.csv`，项目入口说明见 `project_cards/<编号>_cn.md`。\n")


def render():
    for fn, (title, body) in GUIDES.items():
        assert list(body) == FIELDS, fn
        lines = [f"# {title}", "", HEAD]
        for k in FIELDS:
            lines += [f"## {k}", "", body[k], ""]
        (ROOT / "guides" / fn).write_text("\n".join(lines), encoding="utf-8")
    print("rendered", len(GUIDES))


def lint():
    ok_items = set()
    for p in (STATE / "projects").glob("*.json"):
        s = load_json(p)
        if s.get("status") == "done":
            ok_items.add(s["id"])
    for p in (STATE / "materials").glob("*.json"):
        s = load_json(p)
        if s.get("status") == "done":
            ok_items.add(s["id"])
    ok_arxiv = set()
    for p in (STATE / "papers").glob("*.json"):
        s = load_json(p)
        if s.get("status") == "done":
            ok_arxiv.add(s.get("arxiv_id"))
    bad = 0
    docs = list((ROOT / "guides").glob("*.md")) + list((ROOT / "input_output_pipeline").glob("*.md")) + [ROOT / "README_cn.md"]
    for d in docs:
        if not d.exists():
            continue
        t = d.read_text(encoding="utf-8")
        for m in sorted(set(re.findall(r"(?<![A-Za-z0-9_/.-])((?:P\d{4}|D\d{4}|D\d{2}|G\d{2}|B\d{2}|C\d{2}|X\d{2}))(?![0-9])", t))):
            if m not in ok_items:
                print(f"{d.name}: 未登记或未完成条目 {m}")
                bad += 1
        for m in sorted(set(re.findall(r"(?<![\d.])(\d{4}\.\d{4,5})(?![\d])", t))):
            failed_ok = d.name == "completion_report_cn.md" and load_json(STATE / "papers" / f"{m}.json", {}).get("status") == "failed"
            if m not in ok_arxiv and not failed_ok:
                print(f"{d.name}: 论文 {m} 未在已核验论文中")
                bad += 1
    print("lint problems:", bad)


if __name__ == "__main__":
    render()
    lint()
