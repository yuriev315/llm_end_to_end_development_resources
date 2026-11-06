#!/usr/bin/env python3
"""Download CrewAI Windows wheels with win32 markers (host is Linux).

Does not install. Skips uvloop. Weights are never fetched.
"""
from __future__ import annotations

import csv
import hashlib
import os
import subprocess
import sys
import zipfile
from collections import deque
from pathlib import Path

from packaging.markers import default_environment
from packaging.requirements import Requirement
from packaging.utils import canonicalize_name

PIP_PYZ = Path("tools/pip.pyz")
CACHE = Path("ai_agent/state/pip_cache")
LOG = Path("ai_agent/state/logs/agent_topic")
OKCSV = Path("ai_agent/inventories/agent_downloads_cn.csv")
FAIL = Path("ai_agent/inventories/agent_download_failures_cn.csv")
RETRIEVED = "2026-10-30"
SKIP_NAMES = {"uvloop"}  # POSIX-only; pip on Linux would otherwise pull it


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def record(kind: str, name: str, status: str, path: str, source: str, note: str, size: int = 0) -> None:
    new = not OKCSV.exists()
    with OKCSV.open("a", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        if new:
            w.writerow(["kind", "name", "status", "path", "source", "bytes", "retrieved", "note"])
        w.writerow([kind, name, status, path, source, size, RETRIEVED, note])


def fail(kind: str, name: str, source: str, reason: str) -> None:
    new = not FAIL.exists()
    with FAIL.open("a", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        if new:
            w.writerow(["kind", "name", "source", "reason", "retrieved"])
        w.writerow([kind, name, source, reason, RETRIEVED])
    print(f"FAIL {kind} {name}: {reason}", flush=True)


def win_env(py: str) -> dict:
    env = default_environment()
    env.update(
        {
            "os_name": "nt",
            "sys_platform": "win32",
            "platform_machine": "AMD64",
            "platform_system": "Windows",
            "platform_release": "10",
            "platform_version": "10",
            "python_version": py,
            "python_full_version": f"{py}.12",
            "implementation_name": "cpython",
            "implementation_version": f"{py}.12",
            "extra": "",
        }
    )
    return env


def requires_from_wheel(whl: Path, env: dict) -> list[str]:
    reqs = []
    with zipfile.ZipFile(whl) as z:
        names = [n for n in z.namelist() if n.endswith("METADATA") and ".dist-info/" in n]
        if not names:
            return []
        meta = z.read(names[0]).decode("utf-8", "replace")
    for line in meta.splitlines():
        if not line.startswith("Requires-Dist:"):
            continue
        spec = line.split(":", 1)[1].strip()
        try:
            r = Requirement(spec)
        except Exception:
            continue
        if canonicalize_name(r.name) in SKIP_NAMES:
            continue
        if r.marker is not None:
            try:
                if not r.marker.evaluate(env):
                    continue
            except Exception:
                if "extra ==" in spec:
                    continue
        reqs.append(spec)
    return reqs


def pip_download_one(dest: Path, py: str, req: str, logf: Path) -> int:
    tag = py.replace(".", "")
    cmd = [
        sys.executable, str(PIP_PYZ), "download",
        "--dest", str(dest),
        "--python-version", py,
        "--implementation", "cp",
        "--abi", f"cp{tag}",
        "--abi", "abi3",
        "--abi", "none",
        "--platform", "win_amd64",
        "--platform", "any",
        "--only-binary", ":all:",
        "--no-deps",
        "--cache-dir", str(CACHE),
        "--disable-pip-version-check",
        "--timeout", "120",
        "--retries", "3",
        req,
    ]
    with logf.open("a", encoding="utf-8") as fh:
        fh.write("$ " + " ".join(cmd) + "\n")
        fh.flush()
        proc = subprocess.run(cmd, stdout=fh, stderr=subprocess.STDOUT, text=True)
        fh.write(f"[exit {proc.returncode}] {req}\n")
    return proc.returncode


def existing_dist_names(dest: Path) -> set[str]:
    names = set()
    for p in dest.glob("*.whl"):
        # name-ver-...
        n = p.name.split("-")[0].replace("_", "-")
        names.add(canonicalize_name(n))
    return names


def fill(py: str) -> None:
    dest = Path(
        f"ai_agent/windows/agent_runtime_kits/projects/"
        f"A05_multi_agent/environments/A05_multi_agent_crewai_py{py.replace('.','')}_windows/wheelhouse"
    )
    dest.mkdir(parents=True, exist_ok=True)
    linux_src = Path(
        f"ai_agent/agent_runtime_kits/projects/"
        f"A05_multi_agent/environments/A05_multi_agent_crewai_py{py.replace('.','')}_linux/wheelhouse"
    )
    # copy portable wheels
    if linux_src.is_dir():
        for p in linux_src.glob("*.whl"):
            if "manylinux" in p.name or "linux_" in p.name or "musllinux" in p.name:
                continue
            if "uvloop" in p.name.lower():
                continue
            t = dest / p.name
            if not t.exists():
                try:
                    os.link(p, t)
                except OSError:
                    import shutil
                    shutil.copy2(p, t)
    env = win_env(py)
    logf = LOG / f"retry_crewai_win_markers_{py}.log"
    LOG.mkdir(parents=True, exist_ok=True)
    CACHE.mkdir(parents=True, exist_ok=True)
    q = deque(["crewai==1.15.33", "python-dotenv>=1.0"])
    seen = set()
    failed = []
    while q:
        spec = q.popleft()
        try:
            r = Requirement(spec)
        except Exception:
            failed.append(spec)
            continue
        key = canonicalize_name(r.name)
        if key in SKIP_NAMES or key in seen:
            continue
        seen.add(key)
        def parse_existing() -> None:
            stem = r.name.replace("-", "_")
            matches = [p for p in dest.glob("*.whl") if canonicalize_name(p.name.split("-")[0]) == key]
            for whl in matches:
                for nxt in requires_from_wheel(whl, env):
                    q.append(nxt)

        have = key in existing_dist_names(dest)
        if have:
            parse_existing()
            continue
        before = {p.name for p in dest.glob("*.whl")}
        rc = pip_download_one(dest, py, spec, logf)
        after = {p.name for p in dest.glob("*.whl")}
        new = after - before
        if rc != 0 and not new:
            failed.append(spec)
            continue
        parse_existing()
    wheels = sorted(dest.glob("*.whl"))
    envroot = dest.parent
    (envroot / "requirements_lock_en.txt").write_text("\n".join(p.name for p in wheels) + "\n", encoding="utf-8")
    inv = envroot / "wheel_inventory_cn.csv"
    with inv.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["filename", "bytes", "sha256"])
        for p in wheels:
            w.writerow([p.name, p.stat().st_size, sha256(p)])
    note = f"n={len(wheels)} failed={len(failed)}"
    print(f"py{py} {note} dest={dest}", flush=True)
    if failed:
        (envroot / "WINDOWS_MARKER_GAPS_cn.txt").write_text(
            "pip on Linux cannot always resolve Windows markers. Remaining:\n" + "\n".join(failed) + "\n",
            encoding="utf-8",
        )
        fail("wheels", f"A05_multi_agent_crewai/{py}/windows", "pypi", note + " see " + str(logf))
    if len(wheels) >= 20:
        record("wheels", f"A05_multi_agent_crewai/{py}/windows", "ok", str(dest), "pypi win32-markers", note, sum(p.stat().st_size for p in wheels))
    elif wheels:
        record("wheels", f"A05_multi_agent_crewai/{py}/windows", "partial", str(dest), "pypi win32-markers", note, sum(p.stat().st_size for p in wheels))


def main() -> None:
    for py in ("3.10", "3.12"):
        fill(py)


if __name__ == "__main__":
    main()
