import re
from pathlib import Path

from playwright.sync_api import Locator, Page, sync_playwright


ROOT = Path(__file__).resolve().parent
HTML_PATH = ROOT.parent / "docs" / "gallery.html"
DESIGN_SYSTEM_CSS_PATH = ROOT.parent / "assets" / "css" / "design-system.css"
GALLERY_CSS_PATH = ROOT.parent / "docs" / "gallery.css"
SCREENSHOT_DIR = ROOT / "_screenshots"
SCREENSHOT_DIR.mkdir(exist_ok=True)
SCREENSHOT_PATH = SCREENSHOT_DIR / "gallery-btn-fill-brand.png"

BRAND_CSS_START = "/* Hover fill brand variant */"
BRAND_CSS_END = "/* End hover fill brand variant */"
EXPECTED_BRANDS = (
    ("Claude", "#logo-claude", "#D97757"),
    ("Anthropic", "#logo-anthropic", "#F0ECE4"),
    ("OpenAI", "#logo-openai", "#F0ECE4"),
    ("DeepSeek", "#logo-deepseek", "#5786FE"),
    ("Gemini", "#logo-gemini", "#B79BE0"),
)


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


def resolved_custom_color(locator: Locator, property_name: str) -> str:
    return locator.evaluate(
        """(element, propertyName) => {
            const probe = document.createElement("span");
            probe.style.color = `var(${propertyName})`;
            element.append(probe);
            const color = getComputedStyle(probe).color;
            probe.remove();
            return color;
        }""",
        property_name,
    )


def resolved_token_color(page: Page, token: str) -> str:
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


def rgb_tuple(css_color: str) -> tuple[float, float, float]:
    if css_color.startswith("#"):
        hex_color = css_color.removeprefix("#")
        if len(hex_color) == 3:
            hex_color = "".join(channel * 2 for channel in hex_color)
        return tuple(
            float(int(hex_color[index : index + 2], 16)) for index in (0, 2, 4)
        )

    channels = re.search(r"rgba?\(\s*([\d.]+)[,\s]+([\d.]+)[,\s]+([\d.]+)", css_color)
    assert channels is not None, f"could not parse color: {css_color}"
    return tuple(float(channel) for channel in channels.groups())


def relative_luminance(css_color: str) -> float:
    channels = []
    for channel in rgb_tuple(css_color):
        normalized = channel / 255
        channels.append(
            normalized / 12.92
            if normalized <= 0.04045
            else ((normalized + 0.055) / 1.055) ** 2.4
        )
    return 0.2126 * channels[0] + 0.7152 * channels[1] + 0.0722 * channels[2]


def contrast_ratio(first: str, second: str) -> float:
    lighter, darker = sorted(
        (relative_luminance(first), relative_luminance(second)), reverse=True
    )
    return (lighter + 0.05) / (darker + 0.05)


def open_content_tab(page: Page) -> None:
    page.goto(HTML_PATH.as_uri(), wait_until="load")
    page.locator('button.tab[data-tab="content"]').click()


def main() -> None:
    passed: list[str] = []
    contrast_results: list[tuple[str, str, str, float]] = []

    def check(condition: bool, label: str) -> None:
        assert condition, label
        passed.append(label)

    html = document_source()
    # 計數每加一個元件就會變，別寫死數字——只確認那行還在、格式沒壞
    check(
        re.search(r"\d+ 元件（含 \d+ 個動態變體）", html) is not None,
        "header component count line is present",
    )

    brand_css_start = html.index(BRAND_CSS_START)
    brand_css_end = html.index(BRAND_CSS_END, brand_css_start) + len(BRAND_CSS_END)
    brand_css = html[brand_css_start:brand_css_end]
    check(
        re.search(r"#[0-9a-fA-F]{3,8}", brand_css) is None,
        "brand variant CSS contains no raw hex colors",
    )
    check(
        "var(--fill-ink,var(--slide-bg-deep))" in html,
        "fill hover ink uses the deep token fallback",
    )

    reduced_motion_start = html.index("@media(prefers-reduced-motion:reduce)")
    reduced_motion_end = html.index("</style>", reduced_motion_start)
    reduced_motion_css = html[reduced_motion_start:reduced_motion_end]
    check(
        ".ds-btn-fill--brand::before{transition:none}" in reduced_motion_css,
        "brand fill reduced-motion rule is merged into the existing media query",
    )
    check(
        re.search(r"""(?:src|href)\s*=\s*["']https?://""", html) is None
        and re.search(r"@import\s", html) is None,
        "HTML remains self-contained",
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

        brand_buttons = page.locator(".ds-btn-fill--brand")
        check(brand_buttons.count() == 5, "exactly five brand fill buttons exist")

        actual_fill_colors: list[str] = []
        for index, (name, symbol, expected_hex) in enumerate(EXPECTED_BRANDS):
            button = brand_buttons.nth(index)
            box = button.bounding_box()
            check(
                box is not None and box["width"] >= 80 and box["height"] >= 28,
                f"{name} button is at least 80x28px",
            )

            actual_symbol = button.locator("use").get_attribute("href")
            check(actual_symbol == symbol, f"{name} uses {symbol}")
            check(
                f'<symbol id="{symbol.removeprefix("#")}"' in html,
                f"{name} symbol resolves in the sprite",
            )

            fill_color = computed(button, "--fill-color").strip().upper()
            actual_fill_colors.append(fill_color)
            check(
                fill_color == expected_hex.upper(),
                f"{name} fill color matches {expected_hex}",
            )
            check(
                rgb_tuple(computed(button, "color")) == rgb_tuple(fill_color),
                f"{name} text starts at its fill color",
            )

        check(
            len(set(actual_fill_colors)) == 4,
            "five brand buttons resolve to four unique fill colors",
        )

        all_buttons = page.locator(".ds-btn-fill")
        check(all_buttons.count() == 7, "exactly seven fill buttons exist")
        legacy_buttons = page.locator(".ds-btn-fill:not(.ds-btn-fill--brand)")
        check(
            legacy_buttons.count() == 2, "accent and success fill buttons still exist"
        )

        deep_ink = resolved_token_color(page, "--slide-bg-deep")
        button_specs = (
            ("accent", legacy_buttons.nth(0)),
            ("success", legacy_buttons.nth(1)),
            *(
                (name, brand_buttons.nth(index))
                for index, (name, _, _) in enumerate(EXPECTED_BRANDS)
            ),
        )

        for name, button in button_specs:
            fill_color = resolved_custom_color(button, "--fill-color")
            button.hover()
            page.wait_for_timeout(800)
            hover_ink = computed(button, "color")
            shadow = computed(button, "box-shadow", "::before")
            spread_values = [
                float(value) for value in re.findall(r"(-?\d+(?:\.\d+)?)px", shadow)
            ]
            ratio = contrast_ratio(hover_ink, fill_color)
            contrast_results.append((name, fill_color, hover_ink, ratio))

            check(
                rgb_tuple(hover_ink) == rgb_tuple(deep_ink),
                f"{name} hover ink resolves to the deep token",
            )
            check("inset" in shadow, f"{name} hover fill shadow is inset")
            check(
                any(value > 0 for value in spread_values),
                f"{name} hover fill spread is positive",
            )
            check(ratio >= 4.5, f"{name} hover contrast is at least 4.5:1")

        brand_card = brand_buttons.first.locator(
            "xpath=ancestor::div[contains(@class, 'ds-card')]"
        )
        check(
            "var(--slide-bg-deep)" in (brand_card.get_attribute("style") or ""),
            "brand buttons are shown on the required dark card",
        )
        brand_card.screenshot(path=str(SCREENSHOT_PATH))
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
        reduced_brand = reduced_page.locator(".ds-btn-fill--brand").first
        check(
            computed(reduced_brand, "transition-duration", "::before") == "0s",
            "reduced motion disables brand fill transition",
        )
        reduced_brand.hover()
        check(
            "inset" in computed(reduced_brand, "box-shadow", "::before"),
            "reduced motion switches directly to the filled hover state",
        )
        reduced_context.close()
        browser.close()

    check(not page_errors, f"page errors: {page_errors}")
    check(not console_errors, f"console errors: {console_errors}")
    check(
        SCREENSHOT_PATH.exists() and SCREENSHOT_PATH.stat().st_size > 0,
        "brand gallery screenshot is saved",
    )

    for name, fill_color, hover_ink, ratio in contrast_results:
        print(f"{name}: fill={fill_color} ink={hover_ink} contrast={ratio:.2f}:1")
    print(f"PASS: {len(passed)} assertions")


if __name__ == "__main__":
    main()
