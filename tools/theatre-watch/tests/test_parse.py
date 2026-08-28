#!/usr/bin/env python3
"""三層 parser + 去重 + diff 的回歸測試(不連網,純本機 fixture)。

跑法: python3 tests/test_parse.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from watch import Offer, dedupe, diff, parse_page, render_report  # noqa: E402

FIXTURES = Path(__file__).resolve().parent / "fixtures"
BASE = "https://example.com"
failures = []


def check(label, condition, detail=""):
    if condition:
        print(f"  PASS  {label}")
    else:
        print(f"  FAIL  {label} {detail}")
        failures.append(label)


def load(name):
    return (FIXTURES / name).read_text(encoding="utf-8")


print("layer 1 — JSON-LD")
offers = parse_page(load("jsonld.html"), "todaytix", BASE)
by_name = {o.show: o for o in offers}
check("抓到 3 齣", len(offers) == 3, f"got {len(offers)}")
check("The Mousetrap = £30", by_name.get("The Mousetrap") and by_name["The Mousetrap"].price == 30.0)
check("Wicked = £25", by_name.get("Wicked") and by_name["Wicked"].price == 25.0)
check("走的是 json-ld 這層", all(o.method == "json-ld" for o in offers))
check("URL 有帶到", by_name["Wicked"].url == "https://example.com/wicked")

print("layer 2 — 內嵌 JSON (__NEXT_DATA__)")
offers = parse_page(load("embedded.html"), "todaytix", BASE)
by_name = {o.show: o for o in offers}
check("Matilda = £24", by_name.get("Matilda The Musical") and by_name["Matilda The Musical"].price == 24.0)
check("小數價格 29.25 正確", by_name.get("Moulin Rouge!") and by_name["Moulin Rouge!"].price == 29.25)
check("走的是 embedded-json 這層", all(o.method == "embedded-json" for o in offers))

print("layer 3 — DOM 掃 £")
offers = parse_page(load("dom.html"), "todaytix", BASE)
by_name = {o.show: o for o in offers}
check("抓到 3 筆(不含 About us)", len(offers) == 3, f"got {len(offers)}: {list(by_name)}")
check("劇名去掉 'from £25'", "The Lion King" in by_name, f"got {list(by_name)}")
check("相對路徑補成絕對 URL",
      by_name.get("The Lion King") and by_name["The Lion King"].url.startswith("https://example.com/london/"))
check("絕對 URL 不被重複加前綴",
      by_name.get("The Book of Mormon") and by_name["The Book of Mormon"].url == "https://example.com/mormon")

print("dedupe — 同一齣戲留最便宜")
raw = [
    Offer("todaytix", "Wicked", 35.0, "GBP", BASE, "dom"),
    Offer("todaytix", "Wicked", 25.0, "GBP", BASE, "dom"),
    Offer("official-london-theatre", "Wicked", 30.0, "GBP", BASE, "dom"),
]
result = dedupe(raw)
check("兩個來源各留一筆", len(result) == 2, f"got {len(result)}")
check("todaytix 留 £25", next(o.price for o in result if o.source == "todaytix") == 25.0)
check("依價格排序", [o.price for o in result] == sorted(o.price for o in result))

print("diff — 新增 / 降價 / 消失")
current = [
    Offer("todaytix", "Wicked", 25.0, "GBP", BASE, "dom"),      # 從 30 降到 25
    Offer("todaytix", "The Mousetrap", 30.0, "GBP", BASE, "dom"),  # 新的
]
previous = [
    {"source": "todaytix", "show": "Wicked", "price": 30.0},
    {"source": "todaytix", "show": "Matilda", "price": 24.0},   # 不見了
]
changes = diff(current, previous)
check("1 筆新增", len(changes["new"]) == 1 and changes["new"][0]["show"] == "The Mousetrap")
check("1 筆降價,有記錄原價", len(changes["price_drops"]) == 1 and changes["price_drops"][0]["was"] == 30.0)
check("1 筆消失", len(changes["gone"]) == 1 and changes["gone"][0]["show"] == "Matilda")

print("render_report — 產得出 markdown")
report = render_report(current, changes, 30.0, "2026-08-28T12:00:00+00:00")
check("標題有日期", "2026-08-28" in report)
check("有新增區塊", "🆕 今天新出現" in report)
check("有降價區塊且顯示 £30.00 → £25.00", "£30.00 → **£25.00**" in report)
check("空清單不會爆炸", "今天沒有低於預算的票" in render_report([], {"new": [], "price_drops": [], "gone": []}, 30.0, "2026-08-28T12:00:00+00:00"))

print()
if failures:
    print(f"{len(failures)} 項失敗: {failures}")
    sys.exit(1)
print("全部通過 ✅")
