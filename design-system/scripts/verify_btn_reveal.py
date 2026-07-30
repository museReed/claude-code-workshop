import re
from pathlib import Path

from playwright.sync_api import Page, sync_playwright


ROOT = Path(__file__).resolve().parent
HTML_PATH = ROOT.parent / "docs" / "gallery.html"
DESIGN_SYSTEM_CSS_PATH = ROOT.parent / "assets" / "css" / "design-system.css"
GALLERY_CSS_PATH = ROOT.parent / "docs" / "gallery.css"
SCREENSHOT_DIR = ROOT / "_screenshots"
SCREENSHOT_DIR.mkdir(exist_ok=True)
SCREENSHOT_PATH = SCREENSHOT_DIR / "gallery-btn-reveal.png"

CSS_START = "/* Hover reveal button */"
CSS_END = "/* End hover reveal button */"


def document_source() -> str:
    return (
        "<style>\n"
        + DESIGN_SYSTEM_CSS_PATH.read_text(encoding="utf-8")
        + "\n"
        + GALLERY_CSS_PATH.read_text(encoding="utf-8")
        + "\n</style>\n"
        + HTML_PATH.read_text(encoding="utf-8")
    )


def computed_opacity(locator) -> str:
    return locator.evaluate("element => getComputedStyle(element).opacity")


def open_content_tab(page: Page) -> None:
    page.goto(HTML_PATH.as_uri(), wait_until="load")
    page.locator('button.tab[data-tab="content"]').click()


def main() -> None:
    passed: list[str] = []

    def check(condition: bool, label: str) -> None:
        assert condition, label
        passed.append(label)

    html = document_source()
    check("ds-btn-reveal" in html, "component class is present")
    # 計數每加一個元件就會變，別寫死數字——只確認那行還在、格式沒壞
    check(
        re.search(r"\d+ 元件（含 \d+ 個動態變體）", html) is not None,
        "header component count line is present",
    )

    css_start = html.index(CSS_START)
    css_end = html.index(CSS_END, css_start) + len(CSS_END)
    reveal_css = html[css_start:css_end]
    check(
        re.search(r"#[0-9a-fA-F]{3,8}", reveal_css) is None,
        "component CSS contains no raw hex colors",
    )
    check(
        re.search(r"""(?:src|href)\s*=\s*["'](?:https?:|//)""", html) is None
        and re.search(r"""url\(\s*["']?(?:https?:|//)""", html) is None
        and re.search(r"@import\s", html) is None,
        "HTML has no external resource references",
    )

    page_errors: list[str] = []
    console_errors: list[str] = []

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1280, "height": 900})
        page = context.new_page()
        page.on("pageerror", lambda error: page_errors.append(str(error)))
        page.on(
            "console",
            lambda message: (
                console_errors.append(message.text) if message.type == "error" else None
            ),
        )
        open_content_tab(page)

        button = page.locator(".ds-btn-reveal")
        check(button.count() == 1, "one reveal button exists")
        box = button.bounding_box()
        check(box is not None, "reveal button is visible")
        assert box is not None
        check(box["width"] >= 100, "reveal button width is at least 100px")
        check(box["height"] >= 30, "reveal button height is at least 30px")

        label = button.locator(".ds-btn-reveal__label")
        icons = button.locator(".ds-btn-reveal__icons svg")
        check(computed_opacity(label) == "1", "label starts at opacity 1")
        check(icons.count() == 3, "reveal button has three icons")
        check(
            all(computed_opacity(icons.nth(index)) == "0" for index in range(3)),
            "all icons start at opacity 0",
        )
        delays = [
            icons.nth(index).evaluate(
                "element => getComputedStyle(element).transitionDelay"
            )
            for index in range(3)
        ]
        check(
            delays == ["0.65s", "0.8s", "0.5s"],
            "icon transition delays preserve the reference timing",
        )

        use_hrefs = button.locator("use").evaluate_all(
            "elements => elements.map(element => element.getAttribute('href'))"
        )
        check(
            all(
                href and href.startswith("#") and f'<symbol id="{href[1:]}"' in html
                for href in use_hrefs
            ),
            "every sprite use resolves to an in-file symbol",
        )

        button.hover()
        # label 的 transition 就是 1.2s，等剛好 1200ms 是踩在邊界上——
        # 頁面變重（鴨子常駐踏步動畫）後就會晚幾毫秒到位而假紅。留 300ms 餘裕。
        page.wait_for_timeout(1500)
        check(computed_opacity(label) == "0", "hover hides the label")
        check(
            all(computed_opacity(icons.nth(index)) == "1" for index in range(3)),
            "hover reveals all icons",
        )
        button.scroll_into_view_if_needed()
        page.screenshot(path=str(SCREENSHOT_PATH))
        context.close()

        reduced_context = browser.new_context(
            viewport={"width": 1280, "height": 900},
            reduced_motion="reduce",
        )
        reduced_page = reduced_context.new_page()
        reduced_page.on("pageerror", lambda error: page_errors.append(str(error)))
        reduced_page.on(
            "console",
            lambda message: (
                console_errors.append(message.text) if message.type == "error" else None
            ),
        )
        open_content_tab(reduced_page)
        reduced_button = reduced_page.locator(".ds-btn-reveal")
        reduced_button.hover()
        reduced_icons = reduced_button.locator(".ds-btn-reveal__icons svg")
        reduced_state = reduced_button.evaluate(
            """button => ({
                transform: getComputedStyle(button).transform,
                labelOpacity: getComputedStyle(
                    button.querySelector(".ds-btn-reveal__label")
                ).opacity,
            })"""
        )
        check(
            reduced_state == {"transform": "none", "labelOpacity": "0"},
            "reduced motion removes scale and switches the label directly",
        )
        check(
            all(
                computed_opacity(reduced_icons.nth(index)) == "1" for index in range(3)
            ),
            "reduced motion reveals icons directly",
        )
        check(
            all(
                reduced_icons.nth(index).evaluate(
                    "element => getComputedStyle(element).transitionDelay"
                )
                == "0s"
                for index in range(3)
            ),
            "reduced motion removes icon delays",
        )
        reduced_context.close()
        browser.close()

    check(not page_errors, f"page errors: {page_errors}")
    check(not console_errors, f"console errors: {console_errors}")
    check(
        SCREENSHOT_PATH.exists() and SCREENSHOT_PATH.stat().st_size > 0,
        "gallery screenshot is saved",
    )

    print(f"PASS: {len(passed)} assertions")


if __name__ == "__main__":
    main()
