"""Download / reuse arXiv papers listed in seeds/papers_seed_en.txt and verify them.

usage: python3 -I papers_en.py [--retry-failed]

Reuse: if a sibling library already holds a verified PDF with the same arXiv id it is
copied (never moved) and marked 复用 with its source path. Otherwise: arXiv API metadata
(batched id_list) -> title check vs seed (fallback: title search) -> PDF download ->
pypdf check (parses, >=4 pages, title words found on first pages, has a references
section). State: state/papers/<arxiv_id>.json.
"""
import argparse
import csv
import re
import shutil
import sys
import time
import urllib.parse
import xml.etree.ElementTree as ET
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common_en import ACCESS_DATE, PYLIB, ROOT, SEEDS, STAGING, STATE, http, load_json, save_json  # noqa: E402

sys.path.insert(0, str(PYLIB))
import pypdf  # noqa: E402

NS = {"a": "http://www.w3.org/2005/Atom"}
OUT = ROOT / "papers_books_courses" / "papers"
WINDOW_START = "2023-10-29"
SIBLINGS = [
    ("/root/programming_reference_literature", "catalog_cn.csv", "版本", "本地路径", "完整性状态"),
    ("/root/ai_undergraduate_graduate_curriculum_literature", "catalog_cn.csv", "标识符", "本地路径", "完整性状态"),
]
STOP = set("a an the of for and in on with to via from by is are your our as at its".split())


def words(t):
    return [w for w in re.findall(r"[a-z0-9]+", t.lower()) if w not in STOP]


def sim(a, b):
    wa, wb = set(words(a)), set(words(b))
    return len(wa & wb) / max(1, len(wa | wb))


def reuse_map():
    m = {}
    for root, cat, idcol, pcol, scol in SIBLINGS:
        p = Path(root) / cat
        if not p.exists():
            continue
        for r in csv.DictReader(open(p, encoding="utf-8-sig")):
            ident = r.get(idcol) or ""
            mm = re.search(r"(\d{4}\.\d{4,5})(v\d+)?", ident) or re.search(r"arxiv\.org/(?:abs|pdf)/(\d{4}\.\d{4,5})(v\d+)?", r.get("下载地址") or r.get("官方来源") or "")
            if not mm or "完整" not in (r.get(scol) or "") or "部分" in (r.get(scol) or ""):
                continue
            f = Path(root) / (r.get(pcol) or "")
            if f.is_file() and f.suffix == ".pdf":
                m[mm.group(1)] = (str(f), (mm.group(2) or ""), r.get("标题") or "")
    return m


def parse_entries(body):
    out = {}
    root = ET.fromstring(body)
    for e in root.findall("a:entry", NS):
        idurl = e.findtext("a:id", "", NS)
        mm = re.search(r"abs/(\d{4}\.\d{4,5})(v\d+)?", idurl)
        if not mm:
            continue
        out[mm.group(1)] = {
            "title": re.sub(r"\s+", " ", e.findtext("a:title", "", NS)).strip(),
            "authors": [a.findtext("a:name", "", NS) for a in e.findall("a:author", NS)],
            "published": e.findtext("a:published", "", NS)[:10],
            "updated": e.findtext("a:updated", "", NS)[:10],
            "version": mm.group(2) or "",
        }
    return out


def meta_batch(ids):
    r = http("https://export.arxiv.org/api/query?" + urllib.parse.urlencode({"id_list": ",".join(ids), "max_results": len(ids)}), timeout=90)
    return parse_entries(r["body"]) if r.get("body") else {}


def search_title(title):
    q = 'ti:"' + re.sub(r"[^A-Za-z0-9 \-]", " ", title)[:200] + '"'
    r = http("https://export.arxiv.org/api/query?" + urllib.parse.urlencode({"search_query": q, "max_results": 5}), timeout=90)
    if not r.get("body"):
        return None, None
    best = max(parse_entries(r["body"]).items(), key=lambda kv: sim(kv[1]["title"], title), default=(None, None))
    return best


def fname(meta):
    year = meta["published"][:4]
    last = re.sub(r"[^A-Za-z]", "", (meta["authors"][0].split()[-1] if meta["authors"] else "Anon")) or "Anon"
    tw = [w.capitalize() for w in re.findall(r"[A-Za-z0-9]+", meta["title"]) if w.lower() not in STOP][:5]
    return f"{year}_{last}_{''.join(tw)}_en.pdf"


def page_text(rd, i):
    try:
        return rd.pages[i].extract_text() or ""
    except Exception:  # one odd font/page should not fail the whole check
        return ""


def verify(pdf, title):
    try:
        rd = pypdf.PdfReader(str(pdf))
        n = len(rd.pages)
        first = " ".join(page_text(rd, i) for i in range(min(2, n)))
        tail = " ".join(page_text(rd, i) for i in range(2, min(n, 150)))
    except Exception as e:
        return False, f"pypdf 解析失败：{type(e).__name__}"
    tw = set(words(title))
    hit = len(tw & set(words(first))) / max(1, len(tw))
    refs = bool(re.search(r"references|bibliography|reference\s*list", (tail + " " + first).lower()))
    ok = n >= 4 and hit >= 0.6 and refs
    return ok, f"pypdf 可解析 {n} 页；首两页标题词匹配 {hit:.2f}；参考文献节{'存在' if refs else '缺失'}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--retry-failed", action="store_true")
    a = ap.parse_args()
    seeds = []
    for line in (SEEDS / "papers_seed_en.txt").read_text(encoding="utf-8").splitlines():
        if line.strip() and not line.startswith("#"):
            mod, aid, title, classic = (line.split("|") + [""])[:4]
            seeds.append(dict(mod=mod, aid=aid, title=title, classic=classic))
    rmap = reuse_map()
    todo = []
    for s in seeds:
        st = load_json(STATE / "papers" / f"{s['aid']}.json", {})
        if st.get("status") == "done" or (st.get("status") == "failed" and not a.retry_failed):
            continue
        todo.append(s)
    print(len(seeds), "seeds;", len(todo), "to process;", len(rmap), "reusable ids in siblings", flush=True)
    metas = {}
    need = [s["aid"] for s in todo if s["aid"] not in rmap]
    for i in range(0, len(need), 40):
        metas.update(meta_batch(need[i:i + 40]))
    for s in todo:
        aid, stp = s["aid"], STATE / "papers" / f"{s['aid']}.json"
        st = dict(seed=s, access_date=ACCESS_DATE)
        try:
            if aid in rmap:
                src, ver, rtitle = rmap[aid]
                ok, note = verify(src, s["title"])
                if ok:
                    dest = OUT / s["mod"] / Path(src).name
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    if not dest.exists():
                        shutil.copy2(src, dest)
                    st.update(status="done", source="复用", reuse_from=src, arxiv_id=aid, version=ver, title=rtitle or s["title"],
                              path=str(dest.relative_to(ROOT)), verify=note, published="")
                    save_json(stp, st)
                    print(aid, "reused", flush=True)
                    continue
            meta = metas.get(aid)
            if not meta or sim(meta["title"], s["title"]) < 0.5:
                got_id, got = search_title(s["title"])
                if got and sim(got["title"], s["title"]) >= 0.6:
                    st["id_corrected_from"] = aid
                    aid, meta = got_id, got
                else:
                    st.update(status="failed", reason=f"元数据不符：种子编号 {s['aid']} 对应 '{(meta or {}).get('title','无')}'，标题检索未命中")
                    save_json(stp, st)
                    print(s["aid"], "FAILED meta", flush=True)
                    continue
            dest = OUT / s["mod"] / fname(meta)
            dest.parent.mkdir(parents=True, exist_ok=True)
            tmp = STAGING / f"{aid}{meta['version']}.pdf"
            r = {"status": 200} if tmp.exists() and tmp.stat().st_size > 10000 else \
                http(f"https://arxiv.org/pdf/{aid}{meta['version']}", dest=tmp, timeout=180, max_bytes=80_000_000)
            if r.get("status") != 200 or not tmp.exists():
                st.update(status="failed", reason=f"下载失败 {r.get('err') or r.get('status')}", arxiv_id=aid)
                save_json(stp, st)
                print(aid, "FAILED download", flush=True)
                continue
            ok, note = verify(tmp, meta["title"])
            st.update(arxiv_id=aid, version=meta["version"], title=meta["title"], authors=meta["authors"][:8],
                      author_count=len(meta["authors"]), published=meta["published"], updated=meta["updated"], verify=note,
                      url=f"https://arxiv.org/abs/{aid}{meta['version']}")
            if ok:
                shutil.move(tmp, dest)
                st.update(status="done", source="新下载", path=str(dest.relative_to(ROOT)))
            else:
                st.update(status="failed", reason="核验未通过：" + note)
            save_json(stp, st)
            print(aid, st["status"], note, flush=True)
        except Exception as e:
            st.update(status="failed", reason=f"{type(e).__name__}: {e}"[:300])
            save_json(stp, st)
            print(aid, "ERROR", e, flush=True)


if __name__ == "__main__":
    main()
