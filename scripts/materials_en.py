"""Books / courses / official docs: copy-reuse from sibling libraries + direct official PDFs.

usage: python3 -I materials_en.py

Reuse rows are looked up in the sibling catalog by item id; title, version, licence and
completeness status are carried over (a sibling "部分资料" stays partial). Files are
copied, never moved. Direct rows are official PDFs verified with pypdf (parses, page
count >= min_pages, title words on first pages). State: state/materials/<id>.json.
"""
import csv
import re
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common_en import ACCESS_DATE, PYLIB, ROOT, STAGING, STATE, http, load_json, save_json  # noqa: E402

sys.path.insert(0, str(PYLIB))
import pypdf  # noqa: E402

PRL = "/root/programming_reference_literature"
AIUG = "/root/ai_undergraduate_graduate_curriculum_literature"
OUT = ROOT / "papers_books_courses"

# (our id, library, sibling id, kind -> subdir, modules)
REUSE = [
    ("B01", AIUG, "B10-01", "books", "01"), ("B02", AIUG, "B10-02", "books", "01"), ("B03", AIUG, "B09-01", "books", "01"),
    ("B04", AIUG, "B07-01", "books", "01"), ("B05", AIUG, "B07-02", "books", "01"), ("B06", AIUG, "B19-01", "books", "10"),
    ("B07", AIUG, "B19-02", "books", "03"), ("B08", PRL, "13B04", "books", "03"), ("B09", PRL, "04B04", "books", "10"),
    ("C01", AIUG, "A10-02", "courses", "01"), ("C02", AIUG, "D10-01", "courses", "01"), ("C03", AIUG, "D10-02", "courses", "03"),
    ("C04", AIUG, "A09-01", "courses", "01"), ("C05", AIUG, "A09-02", "courses", "01"), ("C06", AIUG, "A10-04", "courses", "09"),
    ("C07", PRL, "15C01", "courses", "08"), ("C08", PRL, "15C02", "courses", "08"), ("C09", PRL, "05C50", "courses", "04"),
    ("C10", PRL, "15C50", "courses", "08"), ("C11", AIUG, "A19-01", "courses", "10"), ("C12", AIUG, "A19-03", "courses", "10"),
    ("C13", PRL, "04C02", "courses", "10"), ("C14", PRL, "05X52", "courses", "01"),
    ("D01", PRL, "05D01", "official_docs", "03"), ("D02", PRL, "05D02", "official_docs", "03"), ("D03", PRL, "05D20", "official_docs", "04"),
    ("D04", PRL, "05D21", "official_docs", "02"), ("D05", PRL, "05D22", "official_docs", "01"), ("D06", PRL, "05D23", "official_docs", "03"),
    ("D07", PRL, "05D24", "official_docs", "04"), ("D08", PRL, "05D25", "official_docs", "04"), ("D09", PRL, "05D27", "official_docs", "05"),
    ("D10", PRL, "05D28", "official_docs", "04"), ("D11", PRL, "13D04", "official_docs", "03"), ("D12", PRL, "13D05", "official_docs", "03"),
    ("D13", PRL, "13D06", "official_docs", "03"), ("D14", PRL, "13D02", "official_docs", "06"), ("D15", PRL, "14D10", "official_docs", "10"),
    ("D16", PRL, "14D11", "official_docs", "10"), ("D17", PRL, "14D12", "official_docs", "10"), ("D18", PRL, "14D20", "official_docs", "10"),
    ("D19", PRL, "14D21", "official_docs", "10"), ("D20", PRL, "14D22", "official_docs", "10"), ("D21", PRL, "14D23", "official_docs", "10"),
    ("D22", PRL, "15D01", "official_docs", "07"), ("D23", PRL, "15D02", "official_docs", "07"), ("D24", PRL, "15D03", "official_docs", "08"),
    ("D25", PRL, "15D04", "official_docs", "07"), ("D26", PRL, "15D10", "official_docs", "08"), ("D27", PRL, "15D11", "official_docs", "08"),
    ("D28", PRL, "15D12", "official_docs", "08"), ("D29", PRL, "15D14", "official_docs", "08"), ("D30", PRL, "09D01", "official_docs", "09"),
    ("D31", PRL, "09D05", "official_docs", "09"), ("D32", PRL, "09D04", "official_docs", "09"), ("D33", PRL, "04D05", "official_docs", "04"),
    ("D34", PRL, "04D06", "official_docs", "02"), ("D35", PRL, "04D07", "official_docs", "03"), ("D36", PRL, "06D10", "official_docs", "10"),
    ("D37", PRL, "06D03", "official_docs", "08"), ("D38", PRL, "06D01", "official_docs", "05"), ("D39", PRL, "16D01", "official_docs", "12"),
    ("D40", PRL, "16D02", "official_docs", "12"), ("D41", PRL, "16D07", "official_docs", "08"), ("D42", PRL, "16D08", "official_docs", "08"),
    ("D43", PRL, "16D05", "official_docs", "09"), ("D44", PRL, "14D06", "official_docs", "06"), ("D45", PRL, "14D07", "official_docs", "06"),
    ("X01", PRL, "15X51", "courses", "12"), ("X02", PRL, "15X52", "courses", "12"), ("X03", PRL, "09X02", "courses", "09"),
    ("X04", PRL, "13X03", "courses", "03"),
]

# (id, title, publisher, version, url, filename, min_pages, title words, modules, licence/terms)
DIRECT = [
    ("G01", "Artificial Intelligence Risk Management Framework: Generative Artificial Intelligence Profile (NIST AI 600-1)", "NIST", "July 2024",
     "https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf", "NIST_AI_600-1_GenAI_Profile_2024_en.pdf", 30, "Generative Artificial Intelligence Profile", "12", "美国政府作品（公有领域）"),
    ("G02", "Artificial Intelligence Risk Management Framework (AI RMF 1.0) (NIST AI 100-1)", "NIST", "January 2023",
     "https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf", "NIST_AI_100-1_AI_RMF_1.0_2023_en.pdf", 30, "Artificial Intelligence Risk Management Framework", "10", "美国政府作品（公有领域）"),
    ("G03", "Clinical Decision Support Software: Guidance for Industry and FDA Staff", "U.S. FDA", "September 2022 (final)",
     "https://www.fda.gov/media/109618/download", "FDA_ClinicalDecisionSupportSoftware_Guidance_2022_en.pdf", 15, "Clinical Decision Support Software", "11", "美国政府作品（公有领域）"),
    ("G04", "Good Machine Learning Practice for Medical Device Development: Guiding Principles", "U.S. FDA / Health Canada / MHRA", "October 2021",
     "https://www.fda.gov/media/153486/download", "FDA_GoodMachineLearningPractice_GuidingPrinciples_2021_en.pdf", 1, "Good Machine Learning Practice", "11", "美国政府作品（公有领域）"),
    ("G05", "Ethics and governance of artificial intelligence for health: Guidance on large multi-modal models", "WHO", "2024 (ISBN 9789240084759)",
     "https://iris.who.int/server/api/core/bitstreams/e9e62c65-6045-481e-bd04-20e206bc5039/content", "WHO_EthicsGovernanceAIHealth_LMM_Guidance_2024_en.pdf", 40, "large multi-modal models", "11", "CC BY-NC-SA 3.0 IGO"),
]


def find_row(lib, sid):
    for r in csv.DictReader(open(Path(lib) / "catalog_cn.csv", encoding="utf-8-sig")):
        if r.get("资料编号") == sid:
            return r
    return None


def copy_any(src, dest):
    if src.is_dir():
        if not dest.exists():
            shutil.copytree(src, dest, symlinks=True)
    elif not dest.exists():
        shutil.copy2(src, dest)


def size_mb(p):
    if p.is_file():
        return round(p.stat().st_size / 1e6, 1)
    return round(sum(f.stat().st_size for f in p.rglob("*") if f.is_file()) / 1e6, 1)


def resolve_path(lib, rel):
    """Catalog paths may point at the first file of a multi-file pack (…/01_x_en.pdf): copy the pack dir."""
    p = Path(lib) / rel
    if p.is_file() and re.match(r"^\d\d_", p.name) and p.parent != Path(lib):
        return p.parent
    return p


def main():
    for mid, lib, sid, sub, mods in REUSE:
        stp = STATE / "materials" / f"{mid}.json"
        if load_json(stp, {}).get("status") == "done":
            continue
        r = find_row(lib, sid)
        if not r:
            save_json(stp, dict(id=mid, status="failed", reason=f"源库目录中未找到 {sid}", lib=lib))
            print(mid, "missing row")
            continue
        src = resolve_path(lib, r["本地路径"])
        status = r.get("完整性状态") or r.get("下载及完整性状态") or ""
        if not src.exists() or "完整" not in status and "部分" not in status:
            save_json(stp, dict(id=mid, status="failed", reason=f"源文件不存在或源库状态为 {status}", src=str(src)))
            print(mid, "src missing", src)
            continue
        dest = OUT / sub / src.name
        copy_any(src, dest)
        typ = r.get("资料类型") or r.get("类型") or ""
        save_json(stp, dict(
            id=mid, status="done", source="复用", reuse_from=str(src), sibling_id=sid, kind=sub, mods=mods,
            title=r.get("标题", ""), author=r.get("作者或机构") or r.get("作者或教师") or "", school=r.get("学校") or r.get("学校或出版社") or "",
            version=r.get("版本") or r.get("学期或版本") or r.get("版本或修订日期") or "", year=r.get("年份") or r.get("原著/首次公开日期") or "",
            license=r.get("许可证") or r.get("许可或使用条件") or "", sibling_status=status, sibling_verify=r.get("核验结果") or r.get("核验说明") or "",
            scope=r.get("范围说明") or r.get("覆盖范围说明") or "", type=typ, path=str(dest.relative_to(ROOT)), size_mb=size_mb(dest),
            complete="部分" not in status, access_date=ACCESS_DATE))
        print(mid, "reused", sid, size_mb(dest), "MB", status[:12])
    for gid, title, pub, ver, url, fn, minp, tw, mods, lic in DIRECT:
        stp = STATE / "materials" / f"{gid}.json"
        if load_json(stp, {}).get("status") == "done":
            continue
        tmp = STAGING / fn
        r = http(url, dest=tmp, timeout=180, max_bytes=150_000_000)
        st = dict(id=gid, title=title, author=pub, version=ver, url=url, kind="official_docs", mods=mods, license=lic,
                  source="新下载", access_date=ACCESS_DATE, type="官方指南/规范")
        if r.get("status") != 200 or not tmp.exists():
            st.update(status="failed", reason=f"下载失败 {r.get('err') or r.get('status')}")
        else:
            try:
                rd = pypdf.PdfReader(str(tmp))
                n = len(rd.pages)
                txt = " ".join((rd.pages[i].extract_text() or "") for i in range(min(4, n))).lower()
                words = [w for w in re.findall(r"[a-z]+", tw.lower()) if len(w) > 2]
                hit = sum(w in txt for w in words) / max(1, len(words))
                ok = n >= minp and hit >= 0.75
                st["verify"] = f"pypdf 可解析 {n} 页；前 4 页标题词匹配 {hit:.2f}"
            except Exception as e:
                ok, st["verify"] = False, f"pypdf 解析失败：{type(e).__name__}"
            if ok:
                dest = OUT / "official_docs" / fn
                shutil.move(tmp, dest)
                st.update(status="done", path=str(dest.relative_to(ROOT)), size_mb=size_mb(dest), complete=True)
            else:
                st.update(status="failed", reason="核验未通过：" + st["verify"])
        save_json(stp, st)
        print(gid, st["status"], st.get("verify", st.get("reason", "")))


if __name__ == "__main__":
    main()
