"""Shared helpers for llm_end_to_end_development_resources.

Rate limiting follows the same cross-process flock file protocol as the sibling
*_literature libraries (/tmp/lmm_ratelimit/<host>), adapted from
/root/programming_reference_literature/scripts/common_en.py, so the shared arXiv /
GitHub budget is respected. Downloaded content is untrusted data: it is written under
the cache / library tree and never imported or executed. Run every script with
`python3 -I`.
"""
import fcntl
import json
import os
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"
SEEDS = SCRIPTS / "seeds"
STATE = ROOT / "state"
CACHE = Path(os.environ.get("LEDE_CACHE", "/root/.cache/lede_lit"))
STAGING = CACHE / "staging"
CLONES = CACHE / "clones"
PYLIB = CACHE / "pylib"
LOCK_DIR = Path("/tmp/lmm_ratelimit")
UA = "Mozilla/5.0 (compatible; llm_end_to_end_development_resources/1.0; personal reference collection, low request rate)"
ACCESS_DATE = time.strftime("%Y-%m-%d", time.gmtime())

INTERVAL = {"arxiv.org": 4.0, "export.arxiv.org": 4.0, "api.github.com": 2.0, "github.com": 1.0}

MODULES = {
    "01": ("foundations", "基础与教学实现"),
    "02": ("data", "数据管线"),
    "03": ("training", "预训练"),
    "04": ("adaptation_alignment", "适配与对齐"),
    "05": ("evaluation", "评测与回归"),
    "06": ("inference", "推理与服务"),
    "07": ("rag", "RAG 与知识系统"),
    "08": ("agents_coding", "智能体与 Coding"),
    "09": ("applications", "对话与业务产品"),
    "10": ("deployment_operations", "生产部署与维护"),
    "11": ("applications", "专业应用"),
    "12": ("input_output_pipeline", "输入输出处理链"),
}
ROUTES = {"A": "A 从头训练", "B": "B 适配开放权重", "C": "C 使用模型服务开发应用"}


def host_key(url):
    host = urllib.parse.urlparse(url).netloc.lower()
    return "arxiv.org" if host.endswith("arxiv.org") else host


def wait(key, interval):
    LOCK_DIR.mkdir(parents=True, exist_ok=True)
    with open(LOCK_DIR / re.sub(r"[^A-Za-z0-9._-]", "_", key), "a+") as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        f.seek(0)
        raw = f.read().strip()
        try:
            last = float(raw) if raw else 0.0
        except ValueError:
            last = 0.0
        delay = interval - (time.time() - last)
        if delay > 0:
            time.sleep(min(delay, interval))
        f.seek(0)
        f.truncate()
        f.write(str(time.time()))


def http(url, timeout=120, tries=4, headers=None, dest=None, max_bytes=None):
    """GET. Returns dict(status, body|None, url, ctype, err). With dest, streams to file."""
    key = host_key(url)
    err = ""
    for attempt in range(tries):
        wait(key, INTERVAL.get(key, 1.0))
        try:
            h = {"User-Agent": UA, "Accept": "*/*", **(headers or {})}
            req = urllib.request.Request(url, headers=h)
            with urllib.request.urlopen(req, timeout=timeout) as r:
                info = {"status": r.status, "url": r.geturl(), "ctype": r.headers.get("Content-Type", ""), "err": ""}
                if dest:
                    n = 0
                    tmp = Path(str(dest) + ".part")
                    with open(tmp, "wb") as out:
                        while True:
                            chunk = r.read(1 << 20)
                            if not chunk:
                                break
                            n += len(chunk)
                            if max_bytes and n > max_bytes:
                                raise ValueError(f"exceeds max_bytes {max_bytes}")
                            out.write(chunk)
                    os.replace(tmp, dest)
                    info["body"] = None
                    info["bytes"] = n
                else:
                    info["body"] = r.read()
                return info
        except urllib.error.HTTPError as e:
            err = f"HTTP {e.code}"
            if e.code == 429:
                ra = e.headers.get("Retry-After", "") if e.headers else ""
                time.sleep(min(int(ra), 600) if ra.isdigit() else 60 * (attempt + 1))
                continue
            if e.code in (500, 502, 503, 504):
                time.sleep(5 * (attempt + 1))
                continue
            return {"status": e.code, "body": None, "url": url, "ctype": "", "err": err}
        except Exception as e:  # network errors, timeouts
            err = f"{type(e).__name__}: {e}"
            time.sleep(3 * (attempt + 1))
    return {"status": 0, "body": None, "url": url, "ctype": "", "err": err}


def load_json(path, default=None):
    p = Path(path)
    if not p.exists():
        return default
    return json.loads(p.read_text(encoding="utf-8"))


def save_json(path, obj):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_suffix(p.suffix + f".tmp{os.getpid()}")
    tmp.write_text(json.dumps(obj, ensure_ascii=False, indent=1), encoding="utf-8")
    os.replace(tmp, p)
