"""Build guides/end_to_end_coverage_cn.csv, guides/gap_backlog_cn.csv, guides/compatibility_matrix_cn.csv.

usage: python3 -I build_guides_en.py

Coverage rows come from seeds/coverage_rows_cn.py; every cited upstream path is checked for
existence inside the cached snapshot. Compatibility evidence is a read-only grep of the
consumer project's snapshot; a pair with no hit is labelled 待验证建议. Nothing is executed.
"""
import csv
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent / "seeds"))
from common_en import CLONES, ROOT, STATE, load_json  # noqa: E402
from coverage_rows_cn import ROWS  # noqa: E402
from validation_rows_cn import ROWS as VROWS  # noqa: E402

G = ROOT / "guides"

# (consumer, provider, grep regex, interface description, dependency-name regex for version pins)
# (consumer, provider, grep regex, interface description, pinned package name, same package as provider?)
COMPAT = [
    ("P0404", "P0601", r"vllm", "verl rollout 使用 vLLM 推理引擎", "vllm", True),
    ("P0404", "P0603", r"sglang", "verl rollout 使用 SGLang", "sglang", True),
    ("P0404", "P0302", r"[Mm]egatron", "verl 训练后端可选 Megatron-Core", "megatron-core", True),
    ("P0403", "P0601", r"vllm", "LLaMA-Factory 推理/评测脚本调用 vLLM", "vllm", True),
    ("P0403", "P0401", r"\btrl\b", "LLaMA-Factory 依赖 TRL 训练器", "trl", True),
    ("P0403", "P0402", r"\bpeft\b", "LLaMA-Factory 依赖 PEFT", "peft", True),
    ("P0401", "P0402", r"\bpeft\b", "TRL 与 PEFT 适配器训练", "peft", True),
    ("P0401", "P0601", r"vllm", "TRL GRPO 等在线生成可用 vLLM", "vllm", True),
    ("P0606", "P0601", r"vllm|compressed.tensors", "llm-compressor 输出 compressed-tensors 供 vLLM 加载", "compressed-tensors", False),
    ("P1003", "P0601", r"hosted_vllm|vllm", "LiteLLM 代理转发至 vLLM OpenAI 兼容服务", "vllm", True),
    ("P1003", "P1004", r"langfuse", "LiteLLM 回调写入 Langfuse 追踪", "langfuse", False),
    ("P0901", "P1003", r"litellm|LiteLLM", "LibreChat 自定义端点指向 LiteLLM/OpenAI 兼容服务", "litellm", True),
    ("P0901", "P0601", r"vllm|vLLM", "LibreChat 自定义端点指向 vLLM", "vllm", True),
    ("P0903", "P0601", r"vllm|vLLM|OPENAI_API_BASE_URL", "Open WebUI 通过 OpenAI 兼容接口接入 vLLM", "vllm", True),
    ("P0902", "P0601", r"vllm|vLLM|OPENAI_BASE_URL", "chat-ui 通过 OpenAI 兼容接口接入后端", "vllm", True),
    ("P1001", "P0601", r"vllm/vllm-openai|vllm", "production-stack 部署 vLLM 引擎镜像", "vllm", True),
    ("P1002", "P0601", r"vllm|vLLM", "KServe Hugging Face 运行时使用 vLLM 后端", "vllm", True),
    ("P0501", "P0601", r"vllm", "lm-eval vLLM 模型后端", "vllm", True),
    ("P0502", "P0601", r"vllm", "inspect_ai vLLM 模型提供方", "vllm", True),
    ("P0504", "P0601", r"vllm|vLLM", "promptfoo 对 OpenAI 兼容/vLLM 端点做回归", "vllm", True),
    ("P0607", "P0601", r"vllm|vLLM", "GuideLLM 对 vLLM 服务压测", "vllm", True),
    ("P0805", "P0505", r"swebench|SWE-bench", "SWE-agent 批量运行并用 SWE-bench 评测", "swebench", True),
    ("P0810", "P0505", r"swebench|SWE-bench", "mini-SWE-agent 评测 SWE-bench", "swebench", True),
    ("P0811", "P1003", r"litellm", "OpenHands SDK 经 LiteLLM 调用模型", "litellm", True),
    ("P0809", "P0705", r"qdrant", "mem0 向量存储使用 Qdrant（依赖 qdrant-client，服务端版本另计）", "qdrant-client", False),
    ("P0702", "P0601", r"vllm|VLLM", "RAGFlow 模型提供方含 vLLM/OpenAI 兼容", "vllm", True),
    ("P0702", "P0202", r"docling", "RAGFlow 解析器可用 Docling", "docling", True),
    ("P0702", "P0208", r"mineru|MinerU", "RAGFlow 解析器可用 MinerU", "mineru", True),
    ("P0904", "P0601", r"vllm|vLLM", "Dify 模型供应商接入 vLLM", "vllm", True),
    ("P0701", "P0705", r"qdrant|Qdrant", "Haystack 文档存储集成 Qdrant（独立集成包）", "qdrant-haystack", False),
    ("P0703", "P0701", r"haystack", "Ragas 与 Haystack 集成", "haystack-ai", True),
    ("P1204", "P1201", r"presidio", "NeMo Guardrails 敏感数据检测使用 Presidio", "presidio-analyzer", True),
    ("P1217", "P1218", r"pydantic", "instructor 基于 Pydantic 校验", "pydantic", True),
    ("P0601", "P0605", r"xgrammar", "vLLM 结构化输出后端 xgrammar", "xgrammar", True),
    ("P0601", "P0604", r"outlines", "vLLM 结构化输出依赖 outlines_core（非 outlines 主包）", "outlines_core", False),
    ("P0603", "P0605", r"xgrammar", "SGLang 结构化输出后端 xgrammar", "xgrammar", True),
    ("P1101", "P1102", r"MIRAGE", "MedRAG 在 MIRAGE 上评测", "mirage", False),
    ("P1111", "P0801", r"\bmcp\b|FastMCP", "freecad-mcp 基于 MCP Python SDK", "mcp", True),
    ("P1212", "P1003", r"litellm", "garak 通过 LiteLLM 调用目标模型", "litellm", True),
    ("P1211", "P0801", r"\bmcp\b", "AgentDojo 与 MCP", "mcp", True),
    ("P0304", "P0401", r"\btrl\b", "litgpt 与 TRL", "trl", True),
]
DEP_GLOBS = ["pyproject.toml", "setup.py", "setup.cfg", "requirements*.txt", "requirements/*.txt", "package.json", "go.mod", "helm/*/values.yaml"]


def clone_root(pid):
    d = CLONES / pid
    if not d.exists():
        return None
    kids = [k for k in d.iterdir() if k.is_dir()]
    if not any(d.glob("README*")) and len(kids) == 1:
        return kids[0]
    return d


def ref_info(rid):
    if rid.startswith(("P", "D")) and (STATE / "projects" / f"{rid}.json").exists():
        s = load_json(STATE / "projects" / f"{rid}.json")
        if s.get("status") != "done":
            return None, s
        return "project", s
    m = load_json(STATE / "materials" / f"{rid}.json")
    return ("material", m) if m and m.get("status") == "done" else (None, m or {})


def grep_hits(pid, rx, limit=3):
    d = clone_root(pid)
    if not d:
        return []
    p = subprocess.run(["grep", "-rIlE", "--exclude-dir=.git", "--exclude-dir=node_modules", "--exclude=*.lock", "--exclude=*lock.json",
                        "--exclude=*.svg", "--exclude=*.ipynb", rx, "."], cwd=d, capture_output=True, text=True, timeout=600)
    files = [f[2:] for f in p.stdout.splitlines()]
    files.sort(key=lambda f: (0 if re.search(r"(^|/)(docs?|README|examples?)", f, re.I) else 1 if f.endswith((".py", ".ts", ".go")) else 2, len(f)))
    return files[:limit]


def dep_pins(pid, pkg):
    rx = r"(?<![\w.-])" + re.escape(pkg) + r"\s*(\[[^\]]*\])?\s*\(?\s*(>=|<=|==|~=|!=|<|>|\^)"
    d = clone_root(pid)
    out = []
    if not d:
        return out
    for g in DEP_GLOBS:
        for f in d.glob(g):
            if not f.is_file() or f.stat().st_size > 2_000_000:
                continue
            for line in f.read_text(errors="replace").splitlines():
                t = line.strip().strip(",")
                if re.search(rx, t, re.I) and len(t) < 200:
                    out.append(f"{f.relative_to(d)}: {t}")
                    if len(out) >= 3:
                        return out
    return out


def vtuple(v):
    m = re.search(r"(\d+)(?:\.(\d+))?(?:\.(\d+))?", v or "")
    return tuple(int(x or 0) for x in m.groups()) if m else None


def judge(pins, prov_version):
    """Compare simple PEP 440-style bounds in the pin lines with the provider version we hold."""
    pv = vtuple(prov_version)
    if not pv:
        return "无法判断（本库为分支快照，无版本号）"
    verdicts = []
    for line in pins:
        spec = line.split(":", 1)[-1].split(";")[0].split("#")[0]
        conds = re.findall(r"(>=|<=|==|~=|!=|<|>)\s*v?(\d+(?:\.\d+){0,2})", spec)
        if not conds:
            continue
        ok = True
        for op, v in conds:
            t = vtuple(v)
            if op == "~=":
                ok &= pv >= t and pv[:1] == t[:1]
            else:
                ok &= {">=": pv >= t, "<=": pv <= t, "==": pv == t, "!=": pv != t, "<": pv < t, ">": pv > t}[op]
        verdicts.append((line.split(":", 1)[0], "约束内" if ok else "约束外"))
    if not verdicts:
        return "无版本约束可比对"
    per = "；".join(f"{f}→{v}" for f, v in verdicts)
    if all(v == "约束内" for _, v in verdicts):
        return f"全部约束内（仅版本号层面）：{per}"
    if all(v == "约束外" for _, v in verdicts):
        return f"约束外（不能直接组合）：{per}"
    return f"声明范围与固定版本不一致：{per}"


def main():
    cov, gaps = [], []
    for route, no, stage, goal, acc, refs, fmt, deps, tests, coverage, missing, prio in ROWS:
        names, vers, commits, paths, lic, maint, dl, lv, chk = [], [], [], [], [], [], [], [], []
        for rid, ups in refs:
            kind, s = ref_info(rid)
            if kind == "project":
                names.append(f"{rid} {s.get('repo')}")
                vers.append(s.get("version", ""))
                commits.append((s.get("commit") or "")[:12])
                paths.append(s.get("archive", ""))
                lic.append(s.get("static", {}).get("license_guess") or "见 LICENSE")
                maint.append(f"{rid}: 最新提交 {s.get('head_commit_date') or '?'}{'，已归档' if s.get('archived') == '是' else ''}")
                dl.append(f"{rid} 已下载")
                lv.append(f"{rid}:{s.get('level')}")
                root = clone_root(rid)
                for u in ups:
                    ok = root is not None and (root / u).exists()
                    chk.append(f"{rid}/{u}{'' if ok else '（未找到！）'}")
            elif kind == "material":
                names.append(f"{rid} {s.get('title','')[:50]}")
                vers.append(s.get("version", ""))
                commits.append("")
                paths.append(s.get("path", ""))
                lic.append(s.get("license", ""))
                dl.append(f"{rid} {'已下载' if s.get('source')=='新下载' else '复用'}{'（部分资料）' if not s.get('complete', True) else ''}")
                lv.append(f"{rid}:文档")
            else:
                names.append(f"{rid}（未收录：{(s or {}).get('error') or (s or {}).get('reason') or '无记录'}）")
                dl.append(f"{rid} 未收录")
        bad = [c for c in chk if "未找到" in c]
        cov.append([route, no, stage, goal, acc, "；".join(names), "；".join(vers), "；".join(commits), "；".join(paths),
                    "；".join(chk), fmt, deps, tests, "；".join(lic), "；".join(maint), "见 compatibility_matrix_cn.csv",
                    "；".join(dl), "；".join(lv) + "（本轮未执行，最高 L1）", missing, prio, coverage, "全部存在" if not bad else f"{len(bad)} 处未找到"])
        if coverage != "已覆盖" or missing:
            gaps.append([route, stage, coverage, missing or "—", prio,
                         {"P0": "阻塞：缺少后无法连接流程", "P1": "测试/权限/隔离/回归/恢复/部署不足", "P2": "优化参考"}[prio],
                         "；".join(n.split(" ")[0] for n in names), "见 reference_stacks_cn.md 对应路线“待补”"])
    hdr = ["路线", "环节序号", "环节", "目标功能", "验收条件", "参考项目", "版本", "提交号", "本地路径", "入口文件/配置（上游相对路径，已核对存在性）",
           "数据格式与小型示例", "模型/数据/软件/硬件依赖", "测试、部署文件及运行手册", "许可证", "维护状态", "兼容条件", "下载状态", "验证等级",
           "缺失项", "补齐优先级", "覆盖判定", "路径核对"]
    with open(G / "end_to_end_coverage_cn.csv", "w", encoding="utf-8-sig", newline="") as f:
        csv.writer(f).writerows([hdr] + cov)
    # global gaps not tied to a single row
    for fpath in ["download_failures_cn.csv"]:
        for r in csv.DictReader(open(ROOT / fpath, encoding="utf-8-sig")):
            if r["类型"] in ("论文",):
                continue
            gaps.append(["全局", f"资料获取：{r['名称']}", "缺失", r["失败原因"], "P1" if r["类型"] != "资料" else "P2", "资料缺口", r["编号"], r["下一步"]])
    with open(G / "gap_backlog_cn.csv", "w", encoding="utf-8-sig", newline="") as f:
        csv.writer(f).writerows([["路线", "环节/资料", "覆盖判定", "缺口说明", "优先级", "优先级含义", "相关条目", "建议处理"]] +
                                sorted(gaps, key=lambda g: (g[4], g[0])))
    comp = []
    for a, b, rx, desc, pkg, same in COMPAT:
        sa, sb = load_json(STATE / "projects" / f"{a}.json", {}), load_json(STATE / "projects" / f"{b}.json", {})
        hits = grep_hits(a, rx)
        pins = dep_pins(a, pkg)
        status = "上游文档/代码提及（未验证）" if hits else "待验证建议（快照中未检出）"
        verdict = (judge(pins, sb.get("version", "")) if same else f"约束针对 {pkg}，与收录项目不是同一包，不做自动比对") if pins else "无显式约束"
        comp.append([f"{a} {sa.get('repo','')}", sa.get("version", ""), f"{b} {sb.get('repo','')}", sb.get("version", ""), desc, status,
                     "；".join(hits) or "无", "；".join(pins) or "依赖文件未声明版本约束", verdict,
                     "自动比对仅看版本号；包名不同（如 qdrant-client 与 qdrant 服务、outlines_core 与 outlines）时须人工判断" if pins else
                     "无显式约束：通常经 OpenAI 兼容 HTTP 接口或可选插件对接，协议细节仍需验证", "否"])
        print(a, b, status, verdict, pins[:1])
    with open(G / "compatibility_matrix_cn.csv", "w", encoding="utf-8-sig", newline="") as f:
        csv.writer(f).writerows([["使用方", "使用方版本", "被依赖方", "本库收录版本", "接口/集成方式", "兼容性证据等级", "证据文件（使用方快照内）",
                                  "版本约束原文", "版本比对（自动）", "说明", "是否经运行验证"]] + comp)
    vm = []
    for stage, item, proves, impl, tests, evalsets, limits in VROWS:
        def fmt(refs):
            out, bad = [], 0
            for rid, ups in refs:
                st = load_json(STATE / "projects" / f"{rid}.json", {})
                root = clone_root(rid)
                for u in ups:
                    ok = root is not None and (root / u).exists()
                    bad += not ok
                    out.append(f"{rid} {st.get('repo','')}@{st.get('version','')}:{u}{'' if ok else '（未找到！）'}")
            return "；".join(out), bad
        i_txt, b1 = fmt(impl)
        t_txt, b2 = fmt(tests)
        lv = "；".join(f"{rid}:{load_json(STATE / 'projects' / f'{rid}.json', {}).get('level','')}" for rid, _ in impl)
        vm.append([stage, item, proves, i_txt, t_txt or "上游未见对应测试", evalsets or "—", lv + "（未执行）",
                   "否：本轮仅静态核对，未运行任何测试", limits, "全部存在" if not (b1 or b2) else f"{b1 + b2} 处未找到"])
    (ROOT / "input_output_pipeline").mkdir(exist_ok=True)
    with open(ROOT / "input_output_pipeline" / "validation_matrix_cn.csv", "w", encoding="utf-8-sig", newline="") as f:
        csv.writer(f).writerows([["环节", "检查项", "通过时能证明的层级", "实现项目（版本:上游路径）", "上游测试证据（路径）", "公开评测集/方法",
                                  "可运行性等级", "本库测试执行证据", "限制", "路径核对"]] + vm)
    print("coverage", len(cov), "gaps", len(gaps), "compat", len(comp), "validation", len(vm))
    for r in vm:
        if r[-1] != "全部存在":
            print("VALIDATION PATH MISSING:", r[1], r[3], r[4])
    for r in cov:
        if r[-1] != "全部存在":
            print("PATH MISSING:", r[0], r[2], [c for c in r[9].split("；") if "未找到" in c])


if __name__ == "__main__":
    main()
