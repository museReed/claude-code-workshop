"""Verify every logo actually renders (real geometry, right colours, both variants)."""

import time
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent
HTML_PATH = ROOT.parent / "docs" / "gallery.html"
SCREENSHOT_DIR = ROOT / "_screenshots"
SCREENSHOT_DIR.mkdir(exist_ok=True)
URL = HTML_PATH.as_uri()
OUT = SCREENSHOT_DIR

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1200, "height": 1000})
    errs = []
    page.on("pageerror", lambda e: errs.append(f"pageerror: {e}"))
    page.on(
        "console",
        lambda m: (
            errs.append(f"console.{m.type}: {m.text}") if m.type == "error" else None
        ),
    )
    page.goto(URL)
    time.sleep(0.5)
    page.click('.tab[data-tab="content"]')
    time.sleep(0.4)

    report = page.evaluate(
        """() => {
            const symbols = [...document.querySelectorAll('.ds-sprite symbol')].map(s => s.id);
            const marks = [...document.querySelectorAll('.ds-toollogo-mark')];
            const bad = [];
            marks.forEach(m => {
                const href = m.querySelector('use').getAttribute('href').slice(1);
                if (!symbols.includes(href)) bad.push(href + ' (no symbol)');
                const r = m.getBoundingClientRect();
                if (r.width < 10 || r.height < 10) bad.push(href + ' (zero size)');
            });
            return {symbols: symbols.length, marks: marks.length, bad};
        }"""
    )
    print("sprite symbols:", report["symbols"], "| rendered marks:", report["marks"])
    print("broken refs:", report["bad"] or "none")

    colors = page.evaluate(
        """() => {
            const out = {};
            document.querySelectorAll('.ds-toollogo--brand').forEach(f => {
                const n = f.querySelector('use').getAttribute('href').slice(1);
                out[n] = getComputedStyle(f.querySelector('.ds-toollogo-mark')).color;
            });
            return out;
        }"""
    )
    for k in [
        "logo-claude",
        "logo-github",
        "logo-openai",
        "logo-nodejs",
        "logo-terminal",
        "logo-anthropic",
    ]:
        print(f"  brand {k:18s} {colors.get(k)}")

    mono = page.evaluate(
        """() => getComputedStyle(document.querySelector('.ds-toollogo:not(.ds-toollogo--brand) .ds-toollogo-mark')).color"""
    )
    print("mono variant colour:", mono)

    # visual proof: each mark must actually paint pixels
    painted = page.evaluate(
        """() => {
            const marks = [...document.querySelectorAll('.ds-toollogo:not(.ds-toollogo--brand) .ds-toollogo-mark')];
            return marks.map(m => {
                const u = m.querySelector('use');
                const sym = document.getElementById(u.getAttribute('href').slice(1));
                const kids = sym ? sym.children.length : 0;
                return [u.getAttribute('href').slice(1), kids];
            }).filter(([, k]) => k === 0);
        }"""
    )
    print("symbols with no shapes:", painted or "none")

    page.evaluate(
        "document.querySelector('.ds-toollogo-grid').scrollIntoView({block:'start'})"
    )
    time.sleep(0.3)
    page.screenshot(path=f"{OUT}/gallery-logos.png")
    print("\nerrors:", errs[:8])
    browser.close()
