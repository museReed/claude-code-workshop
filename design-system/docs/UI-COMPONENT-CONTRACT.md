# UI Component Contract

本網站的 UI 必須以 `assets/css/design-system.css` 與 scratchpad `gallery.html` 展示的 `ds-*` 元件為準。`app.css` 只能做版面排列、資料狀態與必要的新語意元件；不得改既有 `ds-*` 元件內部配色、字體、字級、padding、border 或陰影。

## 既有 gallery 元件對應

| 網站場景 | 必須使用的 gallery 結構 | 可加的 app wrapper |
|---|---|---|
| 全站容器 | `ds-container` / `ds-container-narrow` | `app-shell`、layout class |
| 頂部導覽 | `ds-nav` | `app-nav`、`nav-inner`、`nav-actions` |
| 按鈕 | `ds-btn` + `ds-btn-primary` / `ds-btn-ghost` / `ds-btn-sm` | 只可作為 flex item，不改內部樣式 |
| 卡片 | `ds-card` / `ds-card-flat` | `step-card` 只做 clickable layout / hover transform |
| 標籤 | `ds-pill` / `ds-pill-accent` / `ds-pill-success` | 不覆寫 |
| 內文提示 | `ds-callout` | 成功 / 警告是必要語意變體，仍只用 token |
| 步驟說明 | `ds-step-block` / `ds-step-num` / `ds-step-title` / `ds-step-body` / `ds-step-note` | 用於非終端機操作步驟，不要用 `ds-term` 假裝 |
| 側欄 | `ds-side-item` + `current` | 不覆寫 |
| 進度條與小鴨 | `ds-pbar` / `ds-pbar-fill` / `ds-duck` 原結構 | JS 只改 `width` / `left` 與 `walk/dance/left` 狀態 |
| 終端機 / 指令區塊 | `ds-term` / `ds-term-chrome` / `ds-term-dot` / `ds-term-body` | `cmd-wrap` 加 copy 與 collapsible，不改 terminal 內部 token |

## 允許自製的必要語意元件

| 自製元件 | 為何 gallery 不足 | token 規則 |
|---|---|---|
| `ds-callout--success` | gallery 只有 accent callout，預期結果需要 success 語意 | 只用 `--color-success-*` |
| `ds-callout--warn` | gallery 沒有 warning callout，pitfalls 需要 warning 語意 | 只用 `--amber-*` / `--color-*` |
| `ds-check` | gallery 沒有 checklist checkbox row | 只用 `--color-border-*`、`--color-bg-*`、`--color-success-*`、`--fs-*` |
| `ds-teleprompter` | gallery 沒有錄影提詞面板 | 只用 `--neutral-*`、`--color-accent-*`、`--color-border`、`--font-sans`、`--fs-*` |
| `ds-shot` | gallery 沒有截圖占位槽 | 只用 `--color-border`、`--neutral-*`、`--color-text-*`、`--fs-*` |

## 投影片遷移元件 (Tier A+B)

由 `slides.html` 盤點抽出、gallery 原本沒有的語意元件。已定義於 `design-system.css`（token + class），故 audit 自動放行；使用時只補 layout wrapper，不覆寫內部。

| 新元件 | 角色 | 為何 gallery 不足 | token 規則 |
|---|---|---|---|
| `ds-slide` / `ds-slide--dark/deep/warm` + `ds-hero`(`-eyebrow`/`-title`/`-lede`) | 滿版投影片外框 + hero 標題區 | gallery 無 full-bleed / hero 概念 | `--slide-bg-*`、`--slide-ink`、`--slide-eyebrow`、`--fs-*` |
| `ds-compare`(`-dot--ok/warn/bad`) | 多欄比較表（Claude Code vs Codex 等） | gallery 無表格元件 | `--compare-*`（狀態點接 `--color-success/warn/danger`）；外層自包 `overflow-x:auto` |
| `ds-chat` + `ds-bubble--before/--after` | 痛點 before/after 對話泡泡 | gallery 無 chat bubble | `--bubble-*`（before→danger、after→success） |
| `ds-transform`(`-side--before/--after`,`-arrow`) | 改造前→箭頭→改造後對比塊 | gallery 無 before/after 塊 | `--transform-arrow`、`--color-danger-bg`/`--color-success-bg` |
| `ds-modal-overlay` / `-panel` / `-close` | 點卡片彈出的說明/預覽視窗 | gallery 無 modal | `--modal-overlay`、`--modal-panel-bg` |
| `ds-agenda`(row/num/time/title,`.is-break`) | 有時序的地圖 agenda 表 | gallery 無 agenda | `--color-accent`、`--color-text-faint`、`--fs-*` |
| `ds-timeline`(item/dot/time/title) | 垂直圓點時間軸 | gallery 無 timeline | `--timeline-line`、`--timeline-dot` |
| `ds-flow` + `ds-flow-arrow` | 步驟卡串接（item 復用 `ds-card`/`ds-step-block`） | gallery 無連接式流程 | `--flow-connector` |
| `ds-browser`(bar/dot/url/body) | 瀏覽器 chrome 框 + 內嵌成品 | gallery 無 browser 框 | `--browser-chrome`、`--browser-body-bg` |
| `ds-lightbox` | 截圖點擊放大（複用 modal 遮罩） | gallery 無 lightbox | `--modal-overlay` |

> 這些一律走 `design-system.css` 的 token，無硬色碼；改配色只動 `:root` 上層 token，不動元件。
> 刻意不做的（Tier C，一次性插圖）：放射狀 diagram、漏斗、對比視覺舞台、iframe 流程圖、Lottie 背景、QR code——用 primitives 拼，不抽 token。

## 禁止規則

- 不得在 `app.css` 硬寫 hex / rgb / hsl 顏色。
- 不得在 `app.css` 使用非 token 字級；只能用 `var(--fs-*)` 或 `clamp(var(...))`。
- 不得在 `app.css` 直接覆寫既有 gallery 元件 selector，例如 `.ds-card`、`.ds-btn`、`.ds-pill`、`.ds-term`、`.ds-side-item`、`.ds-pbar`、`.ds-duck`。
- 不得新增自製 `ds-*` 元件，除非先在本文件「允許自製」表格中登記原因與 token 規則。
- 指令 copy 必須複製 `steps.js` 原始 `code`，不能複製高亮後的 HTML。
