# theatre-watch — 倫敦劇院便宜票監控

每天自動去 TodayTix 和 Official London Theatre 抓票價,低於你設定的預算就整理成一份報告,
還會跟昨天比對「今天新出現什麼 / 什麼降價了」。

---

## ⚠️ 先讀這段(重要)

**1. 這支程式在 Claude Code 的雲端 session 裡跑不動。**
這個環境的網路 proxy 把 `todaytix.com` 和 `officiallondontheatre.com` 擋掉了(CONNECT 回 403)。
程式會禮貌地重試三次然後以 exit code 2 收工 —— 它沒壞,是網路政策的關係。
**要真的抓到資料,得在你自己的電腦或 GitHub Actions 上跑**(見下面的排程章節)。

**2. Parser 的 selector 還沒對過真實頁面。**
我沒辦法從這個環境連上那兩個網站,所以三層 parser 是照一般網站結構寫的、用 fixture 測過,
但**第一次在能連網的地方跑時,你很可能要微調**。做法:

```bash
python3 watch.py --dump-html debug/     # 把真實 HTML 存下來
# 打開 debug/*.html 看實際結構,再回頭調 watch.py 裡的 NAME_KEYS / PRICE_KEYS
```

**3. 抓取前請自己確認網站的 Terms of Service。**
本程式只做「個人用途、每天幾次、低頻率」的抓取,並且:
- 開抓前先讀 `robots.txt`,被禁的網址直接跳過
- 每個請求之間 sleep 3 秒
- 用真實的 User-Agent 標明用途,**不繞過任何反爬機制**

如果哪天網站的 ToS 明確禁止,或它出了官方 API,就別再用這個抓 —— 改用官方管道。

---

## 快速開始

```bash
pip install -r requirements.txt

python3 tests/test_parse.py        # 先跑測試,確認 parser 正常
python3 watch.py                   # 抓一次
python3 watch.py --max-price 25    # 改預算
```

產出:

| 檔案 | 內容 |
|------|------|
| `REPORT.md` | 人看的報告(新出現 / 降價 / 全部命中) |
| `data/latest.json` | 最新快照,下次跑拿來做 diff |
| `data/YYYY-MM-DD.json` | 每日歷史,想看價格趨勢時用 |

## 設定

改 `config.json`:

```json
{
  "max_price": 30,          // 預算上限(英鎊)
  "delay_seconds": 3.0,     // 每個請求之間隔幾秒,別調太低
  "targets": [ ... ]        // 要抓的頁面,可自己增減
}
```

想加別的來源(例如 Off-West End 劇院自己的網站),往 `targets` 裡加一筆就好,
parser 是通用的,不用改程式。

## 它怎麼解析頁面(三層 fallback)

網站改版是常態,所以不押寶在單一 selector 上:

| 層 | 方法 | 可靠度 |
|----|------|--------|
| 1 | **JSON-LD** — 網站給 Google 看的 `<script type="application/ld+json">` | 最高,欄位是標準的 |
| 2 | **內嵌 JSON** — Next.js `__NEXT_DATA__` 之類的 state,遞迴找「同時有劇名和價格」的物件 | 中,改版時 key 可能換名 |
| 3 | **DOM 掃描** — 找內文含 `£NN` 的 `<a>`,連結文字當劇名 | 最低,但最耐改版 —— 當保險絲 |

第一層有結果就不往下掉。跑完會印出實際用了哪一層,可以當健康檢查:
如果原本走 json-ld 的來源突然掉到 dom,代表網站結構變了。

## 排程

### 方法 A:GitHub Actions(推薦 —— 不用開電腦)

Repo 裡已經放好 `.github/workflows/theatre-watch.yml`,push 上去就會自己跑:

- 每天兩次:**00:15**(Official London Theatre 上架當日票)、**10:15**(TodayTix Rush 開賣)
- 報告直接顯示在 Actions 的 **job summary** 頁面
- 快照存成 artifact(保留 30 天),用 cache 保留上次資料才比得出 diff
- **抓到 0 筆會讓 workflow 變紅** → GitHub 寄 email 通知你去修 parser

要接收通知:GitHub → Settings → Notifications → Actions → 勾 email。

> cron 走 UTC,英國夏令(BST)和冬令(GMT)差一小時,所以冬天會早一小時跑。
> 在意的話就多排一個時段。

### 方法 B:你自己的 Mac(cron)

```bash
crontab -e
```

加一行(路徑換成你的):

```cron
15 0,10 * * * cd ~/claude-code-workshop/tools/theatre-watch && /usr/bin/python3 watch.py >> watch.log 2>&1
```

想抓到便宜票時直接跳通知,把這段接在後面:

```cron
15 0,10 * * * cd ~/claude-code-workshop/tools/theatre-watch && /usr/bin/python3 watch.py >> watch.log 2>&1 && /usr/bin/osascript -e 'display notification "有新的便宜票" with title "theatre-watch"'
```

> macOS 的 cron 可能需要在「系統設定 → 隱私權與安全性 → 完全取硬碟取用權」把 `cron` 加進去。
> 想要更原生的做法就改用 `launchd`(`~/Library/LaunchAgents/`),睡眠喚醒後會補跑。

### 方法 C:Claude Code Routine

Claude Code 可以建定時任務,每天叫一個 session 起來跑這支程式並讀報告給你。
但**它跑在同一個被擋網路的雲端環境裡**,所以除非那個環境的 network policy 放行這兩個網域,
不然結果會跟現在一樣是 0 筆。要用這條路,得先去環境設定裡把網域加進允許清單。

## 開發

```bash
python3 tests/test_parse.py     # 22 項檢查,不連網
```

`tests/fixtures/` 裡三份 HTML 分別對應三層 parser。改 parser 前先確認測試是綠的,
改完再跑一次;要支援新網站就加一份 fixture。

## 已知限制

- **抓不到 Rush / Lottery 的即時價**:那些只在 TodayTix 手機 App 裡,網頁看不到,而且是 10:00 秒殺。
  這支程式能幫你的是「哪些戲今天有便宜票、值得 10:00 去搶」,不是代搶。
- **價格是「from 價」**:網頁顯示的最低票價,通常是視野最差的位子,而且**不含手續費**。
  實際結帳金額請以官網為準(Official London Theatre 折扣票手續費 £3、全價票 £1)。
- **沒有 JS 渲染**:目前用 `requests` 直抓 HTML。如果某個頁面的價格是純前端 JS 塞進去的,
  三層都會撈不到 —— 那就得換 Playwright,但也會慢很多、更容易被擋。先用 `--dump-html` 確認再決定。
