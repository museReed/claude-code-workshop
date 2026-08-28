#!/usr/bin/env python3
"""theatre-watch — 每天抓倫敦劇院便宜票,低於預算就報給你。

設計原則:
  1. 先看 robots.txt,被禁的網址直接跳過(不繞過任何反爬機制)
  2. 每個請求之間 sleep,不打人家伺服器
  3. 解析採「三層 fallback」:JSON-LD → 頁面內嵌 JSON → DOM 掃 £ 價格
     網站改版時通常只會壞掉一層,不會整個掛掉

用法:
    python3 watch.py                          # 正常跑一次
    python3 watch.py --max-price 25           # 覆寫預算
    python3 watch.py --from-file page.html --source todaytix   # 離線測解析器
    python3 watch.py --dump-html debug/       # 把抓到的 HTML 存下來,方便修 selector
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
import urllib.robotparser
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

HERE = Path(__file__).resolve().parent

# 用真實的 UA + 說明用途。不要偽裝成別的東西。
USER_AGENT = (
    "theatre-watch/1.0 (personal price watcher; "
    "+https://github.com/musereed/claude-code-workshop)"
)

PRICE_RE = re.compile(r"£\s?(\d{1,4}(?:\.\d{2})?)")

# JSON 裡可能放「劇名」和「價格」的 key(各網站命名不同,全部都試)
NAME_KEYS = ("name", "title", "showName", "productName", "displayName", "eventName")
PRICE_KEYS = ("price", "lowPrice", "minPrice", "fromPrice", "lowestPrice", "priceFrom")


# --------------------------------------------------------------------------
# 資料結構
# --------------------------------------------------------------------------

@dataclass(frozen=True)
class Offer:
    source: str          # todaytix / official-london-theatre
    show: str
    price: float
    currency: str
    url: str
    method: str          # 是被哪一層 parser 抓到的,debug 用

    def key(self) -> str:
        return f"{self.source}::{self.show.lower().strip()}"


# --------------------------------------------------------------------------
# 抓取
# --------------------------------------------------------------------------

class Fetcher:
    """帶 robots.txt 檢查 + 禮貌延遲的 HTTP client。"""

    def __init__(self, delay: float = 3.0, timeout: int = 30, retries: int = 3):
        self.delay = delay
        self.timeout = timeout
        self.retries = retries
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": USER_AGENT,
            "Accept": "text/html,application/xhtml+xml",
            "Accept-Language": "en-GB,en;q=0.9",
        })
        self._robots: dict[str, urllib.robotparser.RobotFileParser | None] = {}
        self._last_request = 0.0

    def allowed(self, url: str) -> bool:
        """robots.txt 說不行就是不行。讀不到 robots.txt 時保守放行。"""
        origin = "{0.scheme}://{0.netloc}".format(urlparse(url))
        if origin not in self._robots:
            rp = urllib.robotparser.RobotFileParser()
            rp.set_url(origin + "/robots.txt")
            try:
                resp = self.session.get(origin + "/robots.txt", timeout=self.timeout)
                if resp.status_code == 200:
                    rp.parse(resp.text.splitlines())
                else:
                    rp = None
            except requests.RequestException:
                rp = None
            self._robots[origin] = rp
        rp = self._robots[origin]
        return True if rp is None else rp.can_fetch(USER_AGENT, url)

    def get(self, url: str) -> str | None:
        if not self.allowed(url):
            print(f"  [skip] robots.txt 不允許抓這個網址: {url}", file=sys.stderr)
            return None

        for attempt in range(1, self.retries + 1):
            gap = self.delay - (time.monotonic() - self._last_request)
            if gap > 0:
                time.sleep(gap)
            try:
                resp = self.session.get(url, timeout=self.timeout)
                self._last_request = time.monotonic()
                if resp.status_code == 200:
                    return resp.text
                # 429 / 5xx 才值得重試,4xx 重試也沒用
                if resp.status_code not in (429, 500, 502, 503, 504):
                    print(f"  [fail] HTTP {resp.status_code}: {url}", file=sys.stderr)
                    return None
                print(f"  [retry {attempt}/{self.retries}] HTTP {resp.status_code}", file=sys.stderr)
            except requests.RequestException as exc:
                self._last_request = time.monotonic()
                print(f"  [retry {attempt}/{self.retries}] {type(exc).__name__}: {exc}", file=sys.stderr)
            time.sleep(2 ** attempt)  # 2s, 4s, 8s
        return None


# --------------------------------------------------------------------------
# 解析:三層 fallback
# --------------------------------------------------------------------------

def _to_price(value) -> float | None:
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return float(value) if value > 0 else None
    if isinstance(value, str):
        m = PRICE_RE.search(value) or re.search(r"(\d{1,4}(?:\.\d{2})?)", value)
        if m:
            price = float(m.group(1))
            return price if price > 0 else None
    return None


def _clean(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def parse_jsonld(soup: BeautifulSoup, source: str, base_url: str) -> list[Offer]:
    """第 1 層:JSON-LD 結構化資料(最可靠,網站給搜尋引擎看的官方欄位)。"""
    offers: list[Offer] = []
    for tag in soup.find_all("script", type="application/ld+json"):
        try:
            data = json.loads(tag.string or "")
        except (json.JSONDecodeError, TypeError):
            continue
        for node in _walk(data):
            if not isinstance(node, dict):
                continue
            name = next((node[k] for k in NAME_KEYS if isinstance(node.get(k), str)), None)
            offer_node = node.get("offers") or node
            price = currency = None
            for cand in _walk(offer_node):
                if isinstance(cand, dict):
                    price = next((_to_price(cand[k]) for k in PRICE_KEYS if k in cand), None)
                    if price:
                        currency = cand.get("priceCurrency") or "GBP"
                        break
            if name and price:
                offers.append(Offer(source, _clean(name), price, currency or "GBP",
                                    node.get("url") or base_url, "json-ld"))
    return offers


def parse_embedded_json(soup: BeautifulSoup, source: str, base_url: str) -> list[Offer]:
    """第 2 層:頁面內嵌的 JSON(Next.js __NEXT_DATA__、Nuxt、Redux state...)。

    不假設任何特定結構,直接遞迴走整棵樹,找「同時有劇名和價格」的 dict。
    """
    offers: list[Offer] = []
    for tag in soup.find_all("script"):
        raw = tag.string or ""
        if len(raw) < 200 or "{" not in raw:
            continue
        for blob in _json_blobs(raw):
            for node in _walk(blob):
                if not isinstance(node, dict):
                    continue
                name = next((node[k] for k in NAME_KEYS
                             if isinstance(node.get(k), str) and 1 < len(node[k]) < 120), None)
                price = next((_to_price(node[k]) for k in PRICE_KEYS if k in node), None)
                if name and price:
                    offers.append(Offer(source, _clean(name), price, "GBP",
                                        node.get("url") or base_url, "embedded-json"))
    return offers


def parse_dom(soup: BeautifulSoup, source: str, base_url: str) -> list[Offer]:
    """第 3 層:硬掃 DOM。找內文含 £NN 的連結,連結文字當劇名。

    最不精準,但網站怎麼改版都還有得抓 —— 當保險絲用。
    """
    offers: list[Offer] = []
    for link in soup.find_all("a", href=True):
        text = _clean(link.get_text(" "))
        m = PRICE_RE.search(text)
        if not m:
            continue
        price = float(m.group(1))
        # 把價格字串從劇名裡拿掉,剩下的當名字
        name = _clean(PRICE_RE.sub("", text))
        name = re.sub(r"\b(from|tickets?|book now|£)\b", "", name, flags=re.I).strip(" ·-–|")
        if not name or len(name) > 120 or price <= 0:
            continue
        href = link["href"]
        url = href if href.startswith("http") else base_url.rstrip("/") + "/" + href.lstrip("/")
        offers.append(Offer(source, name, price, "GBP", url, "dom"))
    return offers


def _walk(node):
    """遞迴吐出巢狀 dict/list 裡的每一個節點。"""
    yield node
    if isinstance(node, dict):
        for value in node.values():
            yield from _walk(value)
    elif isinstance(node, list):
        for item in node:
            yield from _walk(item)


def _json_blobs(raw: str):
    """從 <script> 內文裡把 JSON 物件挖出來(可能前後包著 JS 賦值語句)。"""
    text = raw.strip()
    try:
        yield json.loads(text)
        return
    except json.JSONDecodeError:
        pass
    # 找第一個 { 到最後一個 },用 raw_decode 逐段吃
    decoder = json.JSONDecoder()
    idx = 0
    found = 0
    while idx < len(text) and found < 5:
        start = text.find("{", idx)
        if start == -1:
            return
        try:
            obj, end = decoder.raw_decode(text, start)
            yield obj
            found += 1
            idx = end
        except json.JSONDecodeError:
            idx = start + 1


def parse_page(html: str, source: str, base_url: str) -> list[Offer]:
    """三層依序試,第一層有結果就不往下掉。"""
    soup = BeautifulSoup(html, "html.parser")
    for parser in (parse_jsonld, parse_embedded_json, parse_dom):
        offers = parser(soup, source, base_url)
        if offers:
            return offers
    return []


# --------------------------------------------------------------------------
# 整理 / 比對 / 輸出
# --------------------------------------------------------------------------

def dedupe(offers: list[Offer]) -> list[Offer]:
    """同一齣戲只留最便宜那筆。"""
    best: dict[str, Offer] = {}
    for offer in offers:
        prev = best.get(offer.key())
        if prev is None or offer.price < prev.price:
            best[offer.key()] = offer
    return sorted(best.values(), key=lambda o: (o.price, o.show))


def diff(current: list[Offer], previous: list[dict]) -> dict[str, list]:
    """跟昨天的快照比:新出現的 / 降價的 / 消失的。"""
    prev_by_key = {f"{p['source']}::{p['show'].lower().strip()}": p for p in previous}
    cur_keys = {o.key() for o in current}

    new, dropped, gone = [], [], []
    for offer in current:
        prev = prev_by_key.get(offer.key())
        if prev is None:
            new.append(asdict(offer))
        elif offer.price < prev["price"]:
            dropped.append({**asdict(offer), "was": prev["price"]})
    for key, prev in prev_by_key.items():
        if key not in cur_keys:
            gone.append(prev)
    return {"new": new, "price_drops": dropped, "gone": gone}


def render_report(offers: list[Offer], changes: dict, max_price: float, ran_at: str) -> str:
    lines = [
        f"# 倫敦劇院便宜票 · {ran_at[:10]}",
        "",
        f"預算上限 **£{max_price:.0f}** · 命中 **{len(offers)}** 筆",
        "",
    ]

    if changes["new"]:
        lines += ["## 🆕 今天新出現", ""]
        for o in changes["new"]:
            lines.append(f"- **{o['show']}** — £{o['price']:.2f} · [{o['source']}]({o['url']})")
        lines.append("")

    if changes["price_drops"]:
        lines += ["## 📉 降價了", ""]
        for o in changes["price_drops"]:
            lines.append(
                f"- **{o['show']}** — £{o['was']:.2f} → **£{o['price']:.2f}** · [{o['source']}]({o['url']})"
            )
        lines.append("")

    lines += ["## 全部命中", "", "| 價格 | 劇名 | 來源 |", "|---|---|---|"]
    for o in offers:
        lines.append(f"| £{o.price:.2f} | [{o.show}]({o.url}) | {o.source} |")
    if not offers:
        lines.append("| — | _今天沒有低於預算的票_ | — |")

    if changes["gone"]:
        lines += ["", "## ⚠️ 不見了(可能賣完或下架)", ""]
        for o in changes["gone"]:
            lines.append(f"- {o['show']} (£{o['price']:.2f}, {o['source']})")

    lines += ["", "---", "", f"_抓取時間 {ran_at} · 價格以官網結帳頁為準,含手續費前的顯示價_"]
    return "\n".join(lines) + "\n"


# --------------------------------------------------------------------------
# main
# --------------------------------------------------------------------------

def main() -> int:
    ap = argparse.ArgumentParser(description="抓倫敦劇院便宜票")
    ap.add_argument("--config", default=str(HERE / "config.json"))
    ap.add_argument("--out", default=str(HERE / "data"))
    ap.add_argument("--max-price", type=float, default=None, help="覆寫 config 裡的預算")
    ap.add_argument("--from-file", help="離線模式:解析本機 HTML 檔而不連網")
    ap.add_argument("--source", default="local", help="搭配 --from-file 用的來源名稱")
    ap.add_argument("--dump-html", help="把抓到的 HTML 存到這個資料夾(修 parser 用)")
    args = ap.parse_args()

    config = json.loads(Path(args.config).read_text(encoding="utf-8"))
    max_price = args.max_price if args.max_price is not None else config.get("max_price", 30)
    ran_at = datetime.now(timezone.utc).isoformat(timespec="seconds")

    raw: list[Offer] = []

    if args.from_file:
        html = Path(args.from_file).read_text(encoding="utf-8")
        raw = parse_page(html, args.source, config.get("base_url", "https://example.com"))
        print(f"離線解析 {args.from_file}: {len(raw)} 筆")
    else:
        fetcher = Fetcher(delay=config.get("delay_seconds", 3.0))
        for target in config["targets"]:
            print(f"抓取 {target['name']} — {target['url']}")
            html = fetcher.get(target["url"])
            if html is None:
                continue
            if args.dump_html:
                dump = Path(args.dump_html)
                dump.mkdir(parents=True, exist_ok=True)
                (dump / f"{target['name']}.html").write_text(html, encoding="utf-8")
            found = parse_page(html, target["source"], target["url"])
            methods = {o.method for o in found}
            print(f"  → {len(found)} 筆 (parser: {', '.join(methods) or 'none'})")
            raw.extend(found)

    offers = [o for o in dedupe(raw) if o.price <= max_price]

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    latest_path = out_dir / "latest.json"
    previous = []
    if latest_path.exists():
        try:
            previous = json.loads(latest_path.read_text(encoding="utf-8"))["offers"]
        except (json.JSONDecodeError, KeyError):
            pass

    changes = diff(offers, previous)
    snapshot = {
        "ran_at": ran_at,
        "max_price": max_price,
        "offers": [asdict(o) for o in offers],
        "changes": changes,
    }

    latest_path.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2), encoding="utf-8")
    (out_dir / f"{ran_at[:10]}.json").write_text(
        json.dumps(snapshot, ensure_ascii=False, indent=2), encoding="utf-8")
    report = render_report(offers, changes, max_price, ran_at)
    (HERE / "REPORT.md").write_text(report, encoding="utf-8")

    print(f"\n命中 {len(offers)} 筆 ≤ £{max_price:.0f} "
          f"(新 {len(changes['new'])} · 降價 {len(changes['price_drops'])})")
    print(f"報告: {HERE / 'REPORT.md'}")

    # 完全沒抓到東西 → 用 exit code 讓排程器知道要看一下(可能是網站改版)
    if not args.from_file and not raw:
        print("\n⚠️  一筆都沒抓到,parser 可能該修了(試試 --dump-html)", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
