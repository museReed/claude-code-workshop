import re
from io import BytesIO
from pathlib import Path

from PIL import Image
from playwright.sync_api import Locator, Page, sync_playwright


ROOT = Path(__file__).resolve().parent
HTML_PATH = ROOT.parent / "docs" / "gallery.html"
DESIGN_SYSTEM_CSS_PATH = ROOT.parent / "assets" / "css" / "design-system.css"
GALLERY_CSS_PATH = ROOT.parent / "docs" / "gallery.css"
SCREENSHOT_DIR = ROOT / "_screenshots"
SCREENSHOT_DIR.mkdir(exist_ok=True)
SCREENSHOT_PATH = SCREENSHOT_DIR / "gallery-btn-fill.png"

CSS_START = "/* Hover fill button */"
CSS_END = "/* End hover fill button */"


def document_source() -> str:
    return (
        "<style>\n"
        + DESIGN_SYSTEM_CSS_PATH.read_text(encoding="utf-8")
        + "\n"
        + GALLERY_CSS_PATH.read_text(encoding="utf-8")
        + "\n</style>\n"
        + HTML_PATH.read_text(encoding="utf-8")
    )


def computed(locator: Locator, property_name: str, pseudo: str | None = None) -> str:
    return locator.evaluate(
        """(element, args) =>
            getComputedStyle(element, args.pseudo).getPropertyValue(args.property)""",
        {"property": property_name, "pseudo": pseudo},
    )


def open_content_tab(page: Page) -> None:
    page.goto(HTML_PATH.as_uri(), wait_until="load")
    page.locator('button.tab[data-tab="content"]').click()


def resolve_token_color(page: Page, token: str) -> str:
    return page.evaluate(
        """token => {
            const probe = document.createElement("span");
            probe.style.color = `var(${token})`;
            document.body.append(probe);
            const color = getComputedStyle(probe).color;
            probe.remove();
            return color;
        }""",
        token,
    )


def rgb_tuple(css_color: str) -> tuple[int, int, int]:
    channels = re.search(r"rgba?\((\d+),\s*(\d+),\s*(\d+)", css_color)
    assert channels is not None, f"could not parse color: {css_color}"
    return tuple(int(channel) for channel in channels.groups())


def center_region_differs_from_card(button: Locator) -> bool:
    card_color = rgb_tuple(
        button.evaluate(
            "element => getComputedStyle(element.closest('.ds-card')).backgroundColor"
        )
    )
    image = Image.open(BytesIO(button.screenshot())).convert("RGB")
    center_x = image.width // 2
    center_y = image.height // 2
    pixels = [
        image.getpixel((x, y))
        for x in range(center_x - 3, center_x + 4)
        for y in range(center_y - 3, center_y + 4)
    ]
    return sum(pixel != card_color for pixel in pixels) > len(pixels) // 2


def main() -> None:
    passed: list[str] = []

    def check(condition: bool, label: str) -> None:
        assert condition, label
        passed.append(label)

    html = document_source()
    check("ds-btn-fill" in html, "fill component class is present")
    # 計數每加一個元件就會變，別寫死數字——只確認那行還在、格式沒壞
    check(
        re.search(r"\d+ 元件（含 \d+ 個動態變體）", html) is not None,
        "header component count line is present",
    )
    check(
        html.index("<code>.ds-btn-reveal</code>")
        < html.index("<code>.ds-btn-fill</code>"),
        "fill section follows the reveal section",
    )

    css_start = html.index(CSS_START)
    css_end = html.index(CSS_END, css_start) + len(CSS_END)
    fill_css = html[css_start:css_end]
    check(
        re.search(r"#[0-9a-fA-F]{3,8}", fill_css) is None,
        "fill component CSS contains no raw hex colors",
    )
    check(
        "--fill-color:var(--color-accent)" in fill_css
        and "--fill-color:var(--color-success)" in fill_css,
        "both fill colors use one shared CSS variable",
    )
    check(
        re.search(r"""(?:src|href)\s*=\s*["']https?://""", html) is None
        and re.search(r"@import\s", html) is None,
        "HTML has no external resources",
    )
    check("M962.267429" not in html, "old inline Twitter path is removed")
    check(
        '<symbol id="logo-twitter" viewBox="0 0 16 16">' in html,
        "Twitter sprite symbol is present",
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

        # 品牌變體另有自己的驗證腳本，這裡只看非品牌的那兩顆
        buttons = page.locator(".ds-btn-fill:not(.ds-btn-fill--brand)")
        check(buttons.count() == 2, "default and success fill buttons exist")
        default_button = buttons.nth(0)
        success_button = buttons.nth(1)
        for label, button in (
            ("default", default_button),
            ("success", success_button),
        ):
            box = button.bounding_box()
            check(box is not None, f"{label} fill button is visible")
            assert box is not None
            check(box["width"] >= 80, f"{label} fill button width is at least 80px")
            check(box["height"] >= 28, f"{label} fill button height is at least 28px")

        accent_color = resolve_token_color(page, "--color-accent")
        success_color = resolve_token_color(page, "--color-success")
        # hover 文字改成深墨（原本的淺墨對比只有 2.71:1，不到 WCAG 4.5:1）
        hover_ink = resolve_token_color(page, "--slide-bg-deep")
        check(
            computed(default_button, "color") == accent_color,
            "default text starts at the accent token color",
        )
        check(
            computed(success_button, "color") == success_color,
            "success text starts at the success token color",
        )
        check(
            computed(default_button, "box-shadow", "::before") == "none",
            "default pseudo-element starts without a fill shadow",
        )

        fill_uses = buttons.locator("use").evaluate_all(
            "elements => elements.map(element => element.getAttribute('href'))"
        )
        check(
            fill_uses == ["#logo-twitter", "#logo-twitter"],
            "both fill buttons reuse the Twitter sprite",
        )

        default_button.hover()
        page.wait_for_timeout(800)
        default_shadow = computed(default_button, "box-shadow", "::before")
        spread_values = [
            float(value) for value in re.findall(r"(-?\d+(?:\.\d+)?)px", default_shadow)
        ]
        check(
            computed(default_button, "color") == hover_ink,
            "default hover text uses the dark ink token color",
        )
        check("inset" in default_shadow, "default hover uses an inset fill shadow")
        check(
            any(value > 0 for value in spread_values),
            "default hover fill has a positive expansion radius",
        )
        check(
            center_region_differs_from_card(default_button),
            "hover fill is visibly painted over the card background",
        )

        success_button.hover()
        page.wait_for_timeout(800)
        success_shadow = computed(success_button, "box-shadow", "::before")
        check("inset" in success_shadow, "success hover uses an inset fill shadow")
        check(
            success_shadow != default_shadow,
            "success and default hover fills resolve to different colors",
        )

        reveal = page.locator(".ds-btn-reveal")
        reveal_uses = reveal.locator("use").evaluate_all(
            "elements => elements.map(element => element.getAttribute('href'))"
        )
        check(
            all(
                href and href.startswith("#") and f'<symbol id="{href[1:]}"' in html
                for href in reveal_uses
            ),
            "every reveal sprite use resolves to an in-file symbol",
        )
        reveal_icons = reveal.locator(".ds-btn-reveal__icons svg")
        check(reveal_icons.count() == 3, "reveal button still has three icons")
        check(
            all(
                computed(reveal_icons.nth(index), "opacity") == "0"
                for index in range(3)
            ),
            "all reveal icons still start at opacity 0",
        )
        reveal.hover()
        page.wait_for_timeout(1200)
        check(
            all(
                computed(reveal_icons.nth(index), "opacity") == "1"
                for index in range(3)
            ),
            "reveal hover still shows all three icons",
        )

        default_button.hover()
        page.wait_for_timeout(800)
        default_button.scroll_into_view_if_needed()
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
        reduced_button = reduced_page.locator(
            ".ds-btn-fill:not(.ds-btn-fill--brand)"
        ).first
        check(
            computed(reduced_button, "transition-duration", "::before") == "0s",
            "reduced motion disables the fill expansion transition",
        )
        reduced_button.hover()
        check(
            computed(reduced_button, "color")
            == resolve_token_color(reduced_page, "--slide-bg-deep")
            and "inset" in computed(reduced_button, "box-shadow", "::before"),
            "reduced motion switches directly to the filled hover state",
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
