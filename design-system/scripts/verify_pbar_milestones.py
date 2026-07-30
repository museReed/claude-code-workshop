import re
from pathlib import Path

from playwright.sync_api import Page, sync_playwright


ROOT = Path(__file__).resolve().parent
HTML_PATH = ROOT.parent / "docs" / "gallery.html"
DESIGN_SYSTEM_CSS_PATH = ROOT.parent / "assets" / "css" / "design-system.css"
GALLERY_CSS_PATH = ROOT.parent / "docs" / "gallery.css"
SCREENSHOT_DIR = ROOT / "_screenshots"
SCREENSHOT_DIR.mkdir(exist_ok=True)
SCREENSHOT_PATH = SCREENSHOT_DIR / "gallery-pbar-sidecard.png"

TOLERANCE = 0.02
STATIONS = (0.25, 0.50, 0.75, 1.00)


def document_source() -> str:
    return (
        "<style>\n"
        + DESIGN_SYSTEM_CSS_PATH.read_text(encoding="utf-8")
        + "\n"
        + GALLERY_CSS_PATH.read_text(encoding="utf-8")
        + "\n</style>\n"
        + HTML_PATH.read_text(encoding="utf-8")
    )


class Verifier:
    def __init__(self) -> None:
        self.passed = 0
        self.errors: list[str] = []

    def check(self, condition: bool, message: str) -> None:
        if not condition:
            raise AssertionError(message)
        self.passed += 1

    def watch(self, page: Page) -> None:
        page.on("pageerror", lambda error: self.errors.append(f"pageerror: {error}"))
        page.on(
            "console",
            lambda message: (
                self.errors.append(f"console error: {message.text}")
                if message.type == "error"
                else None
            ),
        )


def open_content(page: Page) -> None:
    page.goto(HTML_PATH.as_uri(), wait_until="load")
    page.locator('.tab[data-tab="content"]').click()
    page.locator('.panel[data-panel="content"].active').wait_for(state="visible")


def ratio(locator, parent) -> float:
    box = locator.bounding_box()
    parent_box = parent.bounding_box()
    if box is None or parent_box is None:
        raise AssertionError("無法讀取進度條尺寸")
    return box["width"] / parent_box["width"]


def duck_ratio(duck, parent) -> float:
    box = duck.bounding_box()
    parent_box = parent.bounding_box()
    if box is None or parent_box is None:
        raise AssertionError("無法讀取鴨子位置")
    center = box["x"] + box["width"] / 2
    return (center - parent_box["x"]) / parent_box["width"]


def close_to(actual: float, expected: float) -> bool:
    return abs(actual - expected) <= TOLERANCE


def is_station(actual: float) -> bool:
    return any(close_to(actual, station) for station in STATIONS)


def card_style(card) -> dict[str, str]:
    return card.evaluate(
        """(node) => {
            const style = getComputedStyle(node);
            return {
                opacity: style.opacity,
                visibility: style.visibility,
                pointerEvents: style.pointerEvents,
                whiteSpace: style.whiteSpace,
            };
        }"""
    )


def intersection_area(first, second) -> float:
    first_box = first.bounding_box()
    second_box = second.bounding_box()
    if first_box is None or second_box is None:
        raise AssertionError("無法讀取矩形交集尺寸")
    overlap_width = max(
        0,
        min(first_box["x"] + first_box["width"], second_box["x"] + second_box["width"])
        - max(first_box["x"], second_box["x"]),
    )
    overlap_height = max(
        0,
        min(
            first_box["y"] + first_box["height"],
            second_box["y"] + second_box["height"],
        )
        - max(first_box["y"], second_box["y"]),
    )
    return overlap_width * overlap_height


def main() -> None:
    verifier = Verifier()
    card_measurements: dict[str, tuple[float, float, float, float]] = {}
    station_positions: list[float] = []
    duck_intersections: dict[str, float] = {}
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1440, "height": 1000})
        page = context.new_page()
        verifier.watch(page)
        open_content(page)

        bar = page.locator(".ds-pbar--milestones")
        verifier.check(bar.count() == 1, "里程碑進度條應剛好有一個")
        dots = bar.locator(".ds-milestone")
        verifier.check(dots.count() == 4, "里程碑圓點應剛好有四個")
        verifier.check(
            dots.evaluate_all("(nodes) => nodes.map((node) => node.dataset.value)")
            == ["25", "50", "75", "100"],
            "data-value 順序應為 25/50/75/100",
        )
        verifier.check(
            dots.evaluate_all(
                "(nodes) => nodes.map((node) => node.style.getPropertyValue('--at'))"
            )
            == ["25%", "50%", "75%", "100%"],
            "四個圓點應用 --at 百分比定位",
        )
        verifier.check(
            dots.evaluate_all(
                """(nodes) => nodes.map((node) => [
                    node.classList.contains("ds-milestone--edge-start"),
                    node.classList.contains("ds-milestone--edge-end"),
                ])"""
            )
            == [[True, False], [True, False], [False, True], [False, True]],
            "25%/50% 應向右開，75%/100% 應向左開",
        )
        # 圓點只做展示，不可點也不進 tab 序（用戶指定）
        verifier.check(
            dots.evaluate_all(
                "(nodes) => nodes.every((node) => node.tagName === 'SPAN')"
            ),
            "圓點必須是 span，不得是可點擊元素",
        )
        verifier.check(
            dots.evaluate_all(
                """(nodes) => nodes.every((node) =>
                    node.getAttribute("aria-hidden") === "true"
                    && node.tabIndex < 0
                    && !node.matches("button, a, [role=button], [tabindex]:not([tabindex='-1'])")
                )"""
            ),
            "圓點不得可聚焦、應對輔助技術隱藏",
        )

        cards = dots.locator(".ds-milestone-card")
        verifier.check(cards.count() == 4, "四顆圓點都應包含資訊小卡")
        verifier.check(
            cards.evaluate_all(
                """(nodes) => nodes.every((node) => {
                    const style = getComputedStyle(node);
                    return style.opacity === "0" || style.visibility === "hidden";
                })"""
            ),
            "未 hover 時四張小卡都應隱藏",
        )
        verifier.check(
            cards.evaluate_all(
                """(nodes) => nodes.every(
                    (node) => getComputedStyle(node).pointerEvents === "none"
                )"""
            ),
            "四張小卡都應設定 pointer-events:none",
        )
        verifier.check(
            cards.evaluate_all(
                """(nodes) => nodes.every((node) =>
                    getComputedStyle(node).whiteSpace !== "nowrap"
                    && node.getBoundingClientRect().width <= 260
                )"""
            ),
            "小卡應允許換行且寬度不超過 260px",
        )

        fill = bar.locator(".ds-pbar-fill")
        duck = bar.locator(".ds-duck")
        verifier.check(
            bar.get_attribute("role") is None
            and fill.get_attribute("role") == "progressbar",
            "progressbar 語意應位於 fill",
        )
        verifier.check(bar.get_attribute("data-base") == "50", "data-base 應為 50")
        verifier.check(close_to(ratio(fill, bar), 0.50), "初始 fill 應為 50%")
        initial_duck = duck_ratio(duck, bar)
        station_positions.append(initial_duck)
        verifier.check(close_to(initial_duck, 0.50), "初始鴨子應在 50%")
        verifier.check(
            duck.evaluate("(node) => node.classList.contains('walk')"),
            "初始鴨子應帶 walk class",
        )
        controls = page.locator(".ds-pbar-stations")
        prev_button = controls.locator("[data-station-prev]")
        next_button = controls.locator("[data-station-next]")
        status = controls.locator(".ds-pbar-station-status")
        verifier.check(controls.count() == 1, "進度軸下方應有一列站點控制")
        verifier.check(
            prev_button.inner_text() == "← 上一站"
            and next_button.inner_text() == "下一站 →",
            "站點按鈕文字應為上一站與下一站",
        )
        verifier.check(
            prev_button.get_attribute("class") == "ds-btn ds-btn-ghost ds-btn-sm"
            and next_button.get_attribute("class") == "ds-btn ds-btn-ghost ds-btn-sm",
            "站點按鈕應沿用 ds-btn ghost small 樣式",
        )
        verifier.check(
            status.inner_text() == "第 2 / 4 站 · 跑出第一個成品",
            "初始狀態應顯示第 2 / 4 站與 50% 站名",
        )
        verifier.check(
            not prev_button.is_disabled() and not next_button.is_disabled(),
            "初始第二站的前後按鈕都應可用",
        )

        static_bar = page.locator(
            '.panel[data-panel="content"] '
            ".ds-pbar:not(.ds-pbar--milestones):not(.ds-pbar--indeterminate)"
        ).first
        verifier.check(
            close_to(ratio(static_bar.locator(".ds-pbar-fill"), static_bar), 0.52),
            "既有靜態進度條應維持 52%",
        )
        verifier.check(
            static_bar.locator(".ds-milestone").count() == 0,
            "既有靜態進度條不應有里程碑圓點",
        )

        expected_cards = [
            ("25", "環境裝好"),
            ("50", "跑出第一個成品"),
            ("75", "部署上線"),
            ("100", "完課"),
        ]
        demo_card = page.locator(".ds-card:has(.ds-pbar--milestones)")
        if demo_card.bounding_box() is None:
            raise AssertionError("無法讀取里程碑 demo 卡尺寸")
        padding_top = float(
            demo_card.evaluate(
                "(node) => parseFloat(getComputedStyle(node).paddingTop)"
            )
        )
        side_gap = float(
            page.locator(":root").evaluate(
                "(node) => parseFloat(getComputedStyle(node).getPropertyValue('--space-6'))"
            )
        )
        verifier.check(
            padding_top < 100,
            f"里程碑 demo 卡 padding-top 應小於 100px，實際為 {padding_top:.1f}px",
        )
        for index, (value, name) in enumerate(expected_cards):
            dots.nth(index).hover()
            page.wait_for_timeout(500)
            card = cards.nth(index)
            demo_box = demo_card.bounding_box()
            if demo_box is None:
                raise AssertionError("無法讀取里程碑 demo 卡尺寸")
            style = card_style(card)
            verifier.check(
                style["opacity"] != "0" and style["visibility"] != "hidden",
                f"hover {value}% 時對應小卡應可見",
            )
            text = card.inner_text()
            verifier.check(
                name in text and f"{value}%" in text,
                f"hover {value}% 時小卡應同時包含名稱與百分比",
            )
            card_box = card.bounding_box()
            if card_box is None:
                raise AssertionError(f"無法讀取 {value}% 小卡尺寸")
            card_left = card_box["x"]
            card_right = card_left + card_box["width"]
            card_top = card_box["y"]
            card_bottom = card_top + card_box["height"]
            demo_left = demo_box["x"]
            demo_right = demo_left + demo_box["width"]
            demo_top = demo_box["y"]
            demo_bottom = demo_top + demo_box["height"]
            card_measurements[value] = (
                card_left,
                card_right,
                demo_left,
                demo_right,
            )
            verifier.check(
                card_left >= demo_left - 1
                and card_right <= demo_right + 1
                and card_top >= demo_top - 1
                and card_bottom <= demo_bottom + 1,
                f"{value}% 小卡應完整落在 demo 卡內："
                f"{card_left:.1f}..{card_right:.1f} × "
                f"{card_top:.1f}..{card_bottom:.1f}",
            )
            dot_box = dots.nth(index).bounding_box()
            if dot_box is None:
                raise AssertionError(f"無法讀取 {value}% 圓點尺寸")
            dot_center = dot_box["x"] + dot_box["width"] / 2
            horizontal_gap = (
                card_left - dot_center if index < 2 else dot_center - card_right
            )
            verifier.check(
                horizontal_gap >= side_gap - 1,
                f"{value}% 小卡應從圓點的{'右側' if index < 2 else '左側'}"
                f"保留至少 {side_gap:.0f}px，實際為 {horizontal_gap:.1f}px",
            )

        dots.nth(2).hover()
        page.wait_for_timeout(800)
        verifier.check(close_to(ratio(fill, bar), 0.75), "hover 75% 後 fill 應為 75%")
        verifier.check(
            close_to(duck_ratio(duck, bar), 0.50),
            "hover 75% 時鴨子仍應留在目前的 50% 站",
        )
        verifier.check(
            duck.evaluate(
                "(node) => node.classList.contains('walk')"
                " && !node.classList.contains('left')"
            ),
            "hover 不應改變鴨子的持續踏步或方向",
        )
        active_card = bar.locator(".ds-milestone.is-active .ds-milestone-card")
        verifier.check(active_card.is_visible(), "hover 75% 時資訊小卡應可見")
        verifier.check("75" in active_card.inner_text(), "資訊小卡應顯示 75")

        page.mouse.move(0, 0)
        page.wait_for_timeout(800)
        verifier.check(
            close_to(ratio(fill, bar), 0.50),
            "尚未推進時 mouseleave 應回目前的 50% 站",
        )

        next_button.click()
        page.wait_for_timeout(200)
        verifier.check(
            duck.evaluate("(node) => node.classList.contains('is-running')"),
            "按下一站 200ms 後鴨子應帶 is-running",
        )
        verifier.check(
            prev_button.is_disabled() and next_button.is_disabled(),
            "抵達序列進行中兩顆推進按鈕都應 disabled",
        )
        verifier.check(
            bar.locator(".ds-firework").count() == 0,
            "跑步 200ms 時尚未抵達，不應出現煙花",
        )
        verifier.check(
            not duck.evaluate("(node) => node.classList.contains('left')"),
            "下一站移動中途的鴨子方向應朝右",
        )

        page.wait_for_timeout(400)
        running_position = duck_ratio(duck, bar)
        verifier.check(
            0.50 < running_position < 0.75,
            "位移 600ms 時鴨子中心應介於前後兩站之間",
        )

        page.wait_for_timeout(1150)
        verifier.check(
            bar.locator(".ds-firework").count() == 1,
            "抵達並完成跳躍後應出現一組煙花",
        )
        verifier.check(
            duck.evaluate(
                "(node) => !node.classList.contains('is-running')"
                " && node.classList.contains('walk')"
            ),
            "煙花出現時 is-running 應移除且 walk 應保留",
        )

        page.wait_for_timeout(1100)
        target_dot = dots.nth(2)
        target_card = target_dot.locator(".ds-milestone-card")
        target_close = target_card.locator(".ds-milestone-card-close")
        landed_position = duck_ratio(duck, bar)
        station_positions.append(landed_position)
        verifier.check(
            bar.locator(".ds-firework").count() == 0,
            "完整序列結束後煙花節點應從 DOM 移除",
        )
        verifier.check(
            is_station(landed_position) and close_to(landed_position, 0.75),
            "下一站完成後鴨子應落在 75% 站",
        )
        verifier.check(
            close_to(ratio(fill, bar), 0.75),
            "下一站完成後 fill 應與鴨子同步到 75%",
        )
        target_style = card_style(target_card)
        verifier.check(
            target_card.evaluate("(node) => node.classList.contains('is-pinned')")
            and target_style["opacity"] != "0"
            and target_style["visibility"] != "hidden",
            "完整序列後目標站小卡應釘住且可見",
        )
        verifier.check(
            target_style["pointerEvents"] == "auto",
            "釘住的小卡 computed pointer-events 應為 auto",
        )
        verifier.check(
            target_dot.get_attribute("aria-hidden") is None,
            "釘住期間目標圓點應移除 aria-hidden",
        )
        verifier.check(
            target_close.count() == 1
            and target_close.is_visible()
            and target_close.evaluate("(node) => node.tabIndex >= 0"),
            "釘住態關閉鈕應存在、可見且可聚焦",
        )
        verifier.check(
            not prev_button.is_disabled() and not next_button.is_disabled(),
            "抵達 75% 後兩顆按鈕都應依站點規則恢復",
        )
        duck_intersections["pinned"] = intersection_area(target_card, duck)
        verifier.check(
            duck_intersections["pinned"] == 0,
            "75% 釘住態小卡不得與同站鴨子相交",
        )
        demo_card.screenshot(path=str(SCREENSHOT_PATH))

        # 只預覽「還沒到」的站：hover 已走過的 25% 不得讓進度條倒退
        dots.nth(0).hover()
        page.wait_for_timeout(800)
        verifier.check(
            close_to(ratio(fill, bar), 0.75),
            "hover 已走過的 25% 時 fill 應維持在目前的 75% 站",
        )
        verifier.check(
            target_card.is_visible(),
            "hover 其他圓點時釘住的小卡不得消失",
        )
        page.mouse.move(0, 0)
        page.wait_for_timeout(800)
        verifier.check(
            close_to(ratio(fill, bar), 0.75),
            "釘住期間 mouseleave 後 fill 應回目前的 75% 站",
        )
        verifier.check(target_card.is_visible(), "mouseleave 後釘住的小卡仍應可見")

        target_close.click()
        page.wait_for_timeout(500)
        closed_style = card_style(target_card)
        verifier.check(
            not target_card.evaluate("(node) => node.classList.contains('is-pinned')")
            and (
                closed_style["opacity"] == "0" or closed_style["visibility"] == "hidden"
            ),
            "點關閉鈕後小卡應解除釘住並隱藏",
        )
        verifier.check(
            target_dot.get_attribute("aria-hidden") == "true",
            "關閉小卡後目標圓點應補回 aria-hidden=true",
        )
        target_dot.hover()
        page.wait_for_timeout(500)
        duck_intersections["hover"] = intersection_area(target_card, duck)
        verifier.check(
            target_card.is_visible() and duck_intersections["hover"] == 0,
            "hover 75% 時側向小卡應可見且不得與同站鴨子相交",
        )
        page.mouse.move(0, 0)
        page.wait_for_timeout(800)

        next_button.click()
        page.wait_for_timeout(200)
        next_button.dispatch_event("click")
        page.wait_for_timeout(2600)
        guarded_position = duck_ratio(duck, bar)
        station_positions.append(guarded_position)
        verifier.check(
            close_to(guarded_position, 1.00) and is_station(guarded_position),
            "序列中再次 dispatch click 後仍應只前進一站並停在站值",
        )
        verifier.check(
            next_button.is_disabled() and not prev_button.is_disabled(),
            "最後一站時下一站應 disabled、上一站應可用",
        )

        prev_button.click()
        page.wait_for_timeout(400)
        verifier.check(
            duck.evaluate("(node) => node.classList.contains('left')"),
            "上一站移動 400ms 時鴨子應帶 left",
        )
        verifier.check(
            duck.locator(".ds-duck-hop").count() == 1
            and duck.locator("svg").evaluate(
                "(node) => new DOMMatrix(getComputedStyle(node).transform).a < 0"
            ),
            "跳躍 wrapper 不得影響往回跑時 svg 的水平翻轉",
        )
        page.wait_for_timeout(2200)
        backward_position = duck_ratio(duck, bar)
        station_positions.append(backward_position)
        verifier.check(
            close_to(backward_position, 0.75) and is_station(backward_position),
            "上一站完成後鴨子應落在 75% 站",
        )
        verifier.check(
            bar.locator(".ds-firework").count() == 0,
            "連續完成三次推進後不得堆積煙花節點",
        )

        for expected in (0.50, 0.25):
            prev_button.click()
            page.wait_for_timeout(2600)
            actual = duck_ratio(duck, bar)
            station_positions.append(actual)
            verifier.check(
                is_station(actual) and close_to(actual, expected),
                f"上一站完成後鴨子應落在 {expected:.0%} 站",
            )
            verifier.check(
                close_to(ratio(fill, bar), expected),
                f"上一站完成後 fill 應同步到 {expected:.0%}",
            )

        verifier.check(
            prev_button.is_disabled() and not next_button.is_disabled(),
            "第一站時上一站應 disabled、下一站應可用",
        )
        verifier.check(
            status.inner_text() == "第 1 / 4 站 · 環境裝好",
            "到達第一站後狀態文字應更新",
        )
        verifier.check(
            duck.evaluate("(node) => node.classList.contains('walk')"),
            "移動完成並靜止後鴨子仍應帶 walk class",
        )
        verifier.check(
            duck.locator(".ds-leg").evaluate(
                "(node) => getComputedStyle(node).animationName !== 'none'"
            ),
            "靜止站點上的鴨腳仍應持續播放踏步動畫",
        )

        for expected in (0.50, 0.75):
            next_button.click()
            page.wait_for_timeout(2600)
            actual = duck_ratio(duck, bar)
            station_positions.append(actual)
            verifier.check(
                is_station(actual) and close_to(actual, expected),
                f"下一站完成後鴨子應落在 {expected:.0%} 站",
            )
        status_at_75 = status.inner_text()
        verifier.check(
            status_at_75 == "第 3 / 4 站 · 部署上線",
            "75% 站狀態應讀取該圓點的小卡站名",
        )
        dots.nth(0).hover()
        page.wait_for_timeout(800)
        verifier.check(
            close_to(ratio(fill, bar), 0.75),
            "hover 已走過的 25% 時 fill 不得倒退，應維持 75%",
        )
        verifier.check(
            close_to(duck_ratio(duck, bar), 0.75),
            "hover 25% 時鴨子仍應留在目前的 75% 站",
        )
        verifier.check(
            status.inner_text() == status_at_75,
            "hover 預覽不應改變目前站的狀態文字",
        )
        verifier.check(
            bar.locator(".ds-milestone.is-active .ds-milestone-card").is_visible(),
            "hover 25% 時資訊小卡應可見",
        )

        page.mouse.move(0, 0)
        page.wait_for_timeout(800)
        verifier.check(
            close_to(ratio(fill, bar), 0.75),
            "從 25% 預覽 mouseleave 後 fill 應回目前的 75% 站",
        )

        next_button.click()
        page.wait_for_timeout(2600)
        verifier.check(
            next_button.is_disabled() and not prev_button.is_disabled(),
            "最後一站時下一站應 disabled、上一站應可用",
        )

        reduced_context = browser.new_context(
            viewport={"width": 1440, "height": 1000}, reduced_motion="reduce"
        )
        reduced_page = reduced_context.new_page()
        verifier.watch(reduced_page)
        open_content(reduced_page)
        reduced_bar = reduced_page.locator(".ds-pbar--milestones")
        reduced_duck = reduced_bar.locator(".ds-duck")
        reduced_status = reduced_page.locator(".ds-pbar-station-status")
        reduced_page.locator("[data-station-next]").click()
        reduced_page.wait_for_timeout(300)
        verifier.check(
            close_to(duck_ratio(reduced_duck, reduced_bar), 0.75),
            "reduced-motion 下按下一站後鴨子應立即到 75%",
        )
        verifier.check(
            close_to(ratio(reduced_bar.locator(".ds-pbar-fill"), reduced_bar), 0.75),
            "reduced-motion 下按下一站後 fill 應立即到 75%",
        )
        verifier.check(
            reduced_status.inner_text() == "第 3 / 4 站 · 部署上線",
            "reduced-motion 下按下一站後狀態應立即更新",
        )
        verifier.check(
            reduced_duck.locator(".ds-leg").evaluate(
                "(node) => getComputedStyle(node).animationName === 'none'"
            ),
            "reduced-motion 下應關掉踏步動畫",
        )
        reduced_target = reduced_page.locator(".ds-milestone").nth(2)
        verifier.check(
            reduced_bar.locator(".ds-firework").count() == 0
            and reduced_target.locator(".ds-milestone-card").evaluate(
                "(node) => node.classList.contains('is-pinned')"
            ),
            "reduced-motion 下 300ms 內應無煙花且目標小卡已釘住",
        )
        verifier.check(
            reduced_target.get_attribute("aria-hidden") is None,
            "reduced-motion 下釘住的目標圓點也應移除 aria-hidden",
        )
        reduced_dot = reduced_page.locator(".ds-milestone").nth(3)
        reduced_dot.hover()
        verifier.check(
            close_to(ratio(reduced_bar.locator(".ds-pbar-fill"), reduced_bar), 1.0),
            "reduced-motion 下 hover 100% 應立即完成",
        )
        reduced_card_style = card_style(reduced_dot.locator(".ds-milestone-card"))
        verifier.check(
            reduced_card_style["opacity"] != "0"
            and reduced_card_style["visibility"] != "hidden",
            "reduced-motion 下 hover 後小卡應立即可見",
        )
        verifier.check(
            reduced_target.locator(".ds-milestone-card").is_visible(),
            "reduced-motion 下 hover 其他圓點不得隱藏釘住卡",
        )
        reduced_context.close()

        html = document_source()
        milestone_css = html.split("/* 進度 · 里程碑變體 */", 1)[1].split(
            "/* Loader · 局部等待（新元件） */", 1
        )[0]
        verifier.check(
            re.search(r"#[0-9a-fA-F]{3,8}", milestone_css) is None,
            "里程碑 CSS 不得含 raw hex",
        )
        verifier.check(
            re.search(
                r"\.ds-pbar--milestones \.ds-pbar-fill"
                r"\{transition:width \.45s ease\}",
                milestone_css,
            )
            is not None
            and re.search(
                r"\.ds-pbar--milestones \.ds-duck"
                r"\{[^}]*transition:left 1s ease\}",
                milestone_css,
            )
            is not None,
            "里程碑 fill 應維持 0.45s，鴨子位移 transition 應為 1s",
        )
        verifier.check(
            re.search(
                r"\.ds-pbar--milestones \.ds-duck\.is-arriving "
                r"\.ds-duck-hop\{animation:ds-duck-hop",
                milestone_css,
            )
            is not None
            and re.search(
                r"\.ds-pbar--milestones \.ds-duck\.is-arriving "
                r"(?:svg|\.ds-duck)\{",
                milestone_css,
            )
            is None,
            "跳躍動畫只能掛在專用 ds-duck-hop wrapper",
        )
        verifier.check(
            re.search(
                r"\.ds-firework\{[^}]*pointer-events:none[^}]*"
                r"animation:ds-firework-life \.8s",
                milestone_css,
            )
            is not None,
            "煙花應為 0.8s、pointer-events:none 的里程碑限定樣式",
        )
        verifier.check(
            re.search(r"\.ds-duck\{[^}]*transition:left 1\.2s ease\}", html)
            is not None,
            "全域 ds-duck 的 1.2s transition 應維持不變",
        )
        verifier.check(
            re.search(r'(?:src|href)\s*=\s*["\']https?://', html, re.I) is None
            and re.search(r"@import", html, re.I) is None,
            "HTML 應維持單一自足",
        )
        verifier.check(not verifier.errors, f"瀏覽器錯誤：{verifier.errors}")

        context.close()
        browser.close()

    print(f"PASS: {verifier.passed} assertions")
    print(
        "Edges: "
        + "; ".join(
            f"{value}% {bounds[0]:.1f}..{bounds[1]:.1f} "
            f"within {bounds[2]:.1f}..{bounds[3]:.1f}"
            for value, bounds in card_measurements.items()
        )
    )
    print(
        "Stations: " + " → ".join(f"{position:.2f}" for position in station_positions)
    )
    print(f"Padding-top: {padding_top:.1f}px")
    print(
        "Duck intersections: "
        + "; ".join(
            f"{state} {area:.1f}px²" for state, area in duck_intersections.items()
        )
    )
    print(f"Screenshot: {SCREENSHOT_PATH.name}")


if __name__ == "__main__":
    main()
