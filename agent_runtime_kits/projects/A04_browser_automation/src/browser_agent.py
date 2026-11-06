#!/usr/bin/env python3
"""Playwright agent against a local HTML fixture.

Requires a Playwright browser build. This round downloaded the browser zip
where possible but did not install or launch it. browser-use is Python 3.12
only and is not imported here.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

FIXTURE = Path(__file__).resolve().parents[1] / "fixtures" / "shop.html"


def mock_run() -> dict:
    html = FIXTURE.read_text(encoding="utf-8")
    has_btn = "购买螺丝" in html
    return {
        "ok": True,
        "backend": "mock_no_browser",
        "answer": "未启动浏览器。静态检查到购买按钮。" if has_btn else "页面缺少按钮",
        "fixture": str(FIXTURE),
        "note": "mock 不是浏览器自动化结果",
    }


def playwright_run() -> dict:
    from playwright.sync_api import sync_playwright

    url = FIXTURE.resolve().as_uri()
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)
        page.click("#buy-a")
        status = page.inner_text("#status")
        browser.close()
    return {
        "ok": True,
        "backend": "playwright",
        "answer": status,
        "verified": False,
        "note": "若本函数被运行，仍需单独确认浏览器二进制来自本套件而非系统下载",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", default=os.environ.get("AGENT_BROWSER_MODE", "mock"))
    args = parser.parse_args()
    if args.mode == "playwright":
        print(json.dumps(playwright_run(), ensure_ascii=False, indent=2))
    else:
        print(json.dumps(mock_run(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
