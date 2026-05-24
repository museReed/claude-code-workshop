---
name: KCL Claude Code Workshop
description: 3-hour workshop teaching tech management Master's students to direct AI agents
colors:
  bg: "#FBFBFD"
  bg-alt: "#F5F5F7"
  bg-card: "#FFFFFF"
  bg-warm: "#FAF8F3"
  ink: "#1D1D1F"
  ink-2: "#424245"
  ink-3: "#6E6E73"
  ink-4: "#86868B"
  ink-5: "#A1A1A6"
  navy: "#0E1A2F"
  navy-2: "#1F2C45"
  navy-deep: "#050B17"
  gold: "#B8902E"
  gold-bright: "#D4AD2B"
  gold-pale: "#F0DE9E"
  good: "#2E7D5B"
  warn: "#B6532A"
typography:
  hero:
    fontFamily: "-apple-system, BlinkMacSystemFont, 'SF Pro Display', 'PingFang TC', 'Noto Sans TC', sans-serif"
    fontSize: "clamp(48px, 8vw, 112px)"
    fontWeight: 800
    lineHeight: 1.02
    letterSpacing: "-0.04em"
  section-title:
    fontFamily: "-apple-system, BlinkMacSystemFont, 'SF Pro Display', 'PingFang TC', 'Noto Sans TC', sans-serif"
    fontSize: "clamp(32px, 4.5vw, 56px)"
    fontWeight: 700
    lineHeight: 1.08
    letterSpacing: "-0.028em"
  section-lede:
    fontFamily: "-apple-system, BlinkMacSystemFont, 'SF Pro Display', 'PingFang TC', 'Noto Sans TC', sans-serif"
    fontSize: "clamp(17px, 1.4vw, 21px)"
    fontWeight: 400
    lineHeight: 1.5
    letterSpacing: "-0.012em"
  body:
    fontFamily: "-apple-system, BlinkMacSystemFont, 'SF Pro Display', 'PingFang TC', 'Noto Sans TC', sans-serif"
    fontSize: "clamp(15px, 0.7vw + 13px, 17px)"
    fontWeight: 400
    lineHeight: 1.55
    letterSpacing: "-0.005em"
  code:
    fontFamily: "ui-monospace, 'SF Mono', Menlo, monospace"
    fontSize: "13px"
    fontWeight: 500
    lineHeight: 1.65
    letterSpacing: "normal"
rounded:
  sm: "8px"
  md: "12px"
  lg: "18px"
  xl: "24px"
  2xl: "28px"
  pill: "100px"
spacing:
  section-y: "clamp(72px, 11vh, 128px)"
  container-x: "clamp(20px, 4vw, 40px)"
  container-max: "1180px"
  text-max: "880px"
  lede-max: "720px"
components:
  card-light:
    backgroundColor: "{colors.bg-card}"
    textColor: "{colors.ink}"
    rounded: "{rounded.xl}"
    padding: "28px 28px 32px"
  card-dark:
    backgroundColor: "{colors.navy}"
    textColor: "#FFFFFF"
    rounded: "{rounded.xl}"
    padding: "28px 28px 32px"
  card-warm:
    backgroundColor: "{colors.bg-warm}"
    textColor: "{colors.ink-2}"
    rounded: "{rounded.md}"
    padding: "20px 28px"
  eyebrow-pill:
    backgroundColor: "{colors.gold-pale}"
    textColor: "{colors.gold}"
    rounded: "{rounded.pill}"
    padding: "5px 12px"
  phase-letter:
    backgroundColor: "{colors.gold-pale}"
    textColor: "{colors.gold}"
    rounded: "{rounded.pill}"
    size: "56px"
---

## Overview

KCL Claude Code Workshop 是一份 **brand-register** 的長 scroll 教學品，作為 3 小時 workshop 的單一教材。視覺路線：**Apple HIG 基底 + KCL navy/gold 學院色彩 + Arc Browser / Linear 風的當代手法**。

設計脈絡：講師（Wei）在現場投影、學員看著聽。少量決定性使用 glass、frosted surface 與 ambient motion，承擔「製作感 / 透明 / 補上現代」這組 personality。

繁中為主、技術名詞英文。font stack 優先吃 macOS 系統字（SF Pro + PingFang TC），web font 為 fallback。

## Colors

**雙世界 surface 系統。** 亮底（白 / 米色）與深底（KCL navy）交錯，**金色 (`gold` 系列)** 是唯一 accent — 點到為止，承擔強調 + 連結 + 標題重音三件事。

### Light surfaces
- `bg` (#FBFBFD) — 全頁底色，Apple 慣用偏冷的「幾乎是白」
- `bg-alt` (#F5F5F7) — section 變化、hover state
- `bg-card` (#FFFFFF) — card 用，跟 bg 拉開層次
- `bg-warm` (#FAF8F3) — 暖底 callout、休息區段（pure neutral 之外的呼吸）

### Dark surfaces
- `navy` (#0E1A2F) — section-dark 主底，KCL 學院色
- `navy-2` (#1F2C45) — navy gradient 終點 / 較亮 dark card
- `navy-deep` (#050B17) — integrity / footer 最深層、金字塔頂

### Ink (text)
- `ink` (#1D1D1F) — h1-h5 主標題
- `ink-2` (#424245) — body text、section-lede
- `ink-3` (#6E6E73) — meta、caption、time label
- `ink-4` / `ink-5` — disabled / 微弱輔助

### Accent: Gold
- `gold` (#B8902E) — eyebrow pill 文字、accent link、`.accent` 重音
- `gold-bright` (#D4AD2B) — dark section 上的 gold（提亮以維持對比）
- `gold-pale` (#F0DE9E) — dark code block 文字、低調金（避免在亮底用、會糊）

### Semantic
- `good` (#2E7D5B) — Demo good-prompt 區、scenario yes-list
- `warn` (#B6532A) — Demo bad-prompt 區、Phase 警示、scenario no-list

**OKLCH 注意**：目前 frontmatter 用 hex 是為了 Stitch 相容。所有顏色都是已校過 contrast 的工程值，未來如轉 OKLCH，亮度跟 chroma 都要保持，不可單純色彩空間轉換。

## Typography

**單一 sans family，weight + size 變化做層次。** 不混 serif、不引入 display font。Hero / section-title / lede / body / code 五層階梯，比例 ≥ 1.25。

### Font stack
- **Sans**：`-apple-system, BlinkMacSystemFont, "SF Pro Display", "SF Pro Text", "Inter", "PingFang TC", "Noto Sans TC"` — Mac/iOS 直接吃 SF Pro + PingFang，Linux/Windows fallback Inter + Noto Sans TC
- **Mono**：`ui-monospace, "SF Mono", "JetBrains Mono", Menlo, Monaco` — 同樣優先吃系統 mono

### Hierarchy (fluid `clamp()`)
- **Hero h1**: 48 → 112px / weight 800 / letter-spacing -0.04em — 開場「Claude Code 工作坊。」level
- **Section title**: 32 → 56px / weight 700 / -0.028em — 各章節大標
- **Section lede**: 17 → 21px / weight 400 / -0.012em — 章節下方的引文
- **Body**: 15 → 17px / weight 400 / -0.005em — 段落內文
- **Meta / caption**: 12-14px / weight 500 / +0.04em tracking — eyebrow、time、tag

### CJK + Latin 混排規則
- 中文不加 letter-spacing（會破壞字距）；letter-spacing 只用在 Latin 字串
- 同段中英混排時，inline 英文（如 `Claude Code`、`CCC`）字級與中文一致，不另外放大
- `<code>` inline 為 mono、`background: gold-tint`、`padding: 2px 7px`、`rounded: 4px`

### Mono 使用紀律
**Mono 只用於：** 真實 code、command、檔名、time stamp（`5–8 min`、`25–35 min`）、版本號（`v 2.1`）

**Mono 不用於：** 章節編號、tag 標籤、eyebrow chip、stat label、card title — 這些之前濫用 mono 製造「技術感」，是 anti-pattern。改用 sans + weight + tracking。

## Elevation

**幾乎 flat。** Apple 學派的克制設計：陰影只在 hover 出現、用來確認互動，不用來區分層級。Layering 主要靠 surface color 變化（`bg` / `bg-card` / `bg-alt`）。

### Shadow ladder
- **Rest**: 0 — 所有 card 預設沒影
- **Hover (subtle)**: `0 12px 32px rgba(0, 0, 0, 0.06)` — cap-card / ccc-card hover、transform: translateY(-3px) 配套
- **Hover (mid)**: `0 12px 32px rgba(0, 0, 0, 0.08)` — phase card / 重要 affordance hover

### Border ladder
- `--line` (rgba 0/0.08) — 預設 hairline，每張 card、每個 section divider
- `--line-2` (rgba 0/0.14) — dashed separator、tool-how 上的虛線
- `--line-dark` (rgba 255/0.12) — dark section 上的 hairline

### Glass / backdrop-filter（罕用、決定性）
- **Nav** (`backdrop-filter: saturate(180%) blur(24px)` over `rgba(251,251,253,0.72)`) — sticky 玻璃 nav，Apple-style 標準作法 ✓ 保留
- **未來新增的 glass 使用** — 必須 deliberate，限制在 floating panel / floating callout / 浮動 indicator 等真正需要「半透明 + 模糊背景」表達層次的場合。**禁止：** 不要在每個 card 上加 backdrop-filter；不要在 dark section 整面 glass

## Components

### Cards
- **`.cap-card` / `.ccc-card`** — light card，padding 28px，rounded `xl`，hover lift + soft shadow
- **`.phase`** — light card 加強版，3-column grid（letter badge / body / meta），rounded `xl`，padding 32px
- **`.scn`** — dark card（rgba 白 0.04 over navy），accordion 行為，open 狀態加金色 tint
- **`.tier`** — gradient card，3 種 variant：tier-agent（gold gradient）/ tier-product（navy-2）/ tier-model（navy-deep with gold-pale text）
- **`.demo`** — 二分欄 card：bad（warn-tint）/ good（good-tint）

### Eyebrow pill
`.eyebrow` — 章節 chip，`gold-pale` 底 + `gold` 文字 + 小圓點 + rounded `pill`。**注意：目前過量使用，distill 後應只剩 3-5 處最關鍵章節保留。**

### Phase letter badge
`.phase-letter` — 56px 圓形，gold-pale 底 + gold 文字 + 1px gold border，內裝大寫字母 A-E。`warn` variant 改 warn-tint。

### Code blocks
- **Inline `<code>`** — mono / gold-tint bg / rounded 4px / 2px 7px padding
- **`<pre>` (terminal style)** — navy bg / gold-pale text / mono 13px / rounded `md` / 16-20px padding / 結尾閃爍 `▋` cursor（已加，承擔「terminal 是活的」訊號）

### Flow diagram
`.flow` — 橫向 flex 排列的 node + arrow，`.you` class 標當前位置（gold bg）。Stagger reveal on scroll（已加）。

### Ambient motion
- **Hero gradient drift** — 22 秒 ease-out alternate，translate + scale，z-index: 0 pseudo-element（已加）
- **Reveal-on-scroll** — `.r` class + IntersectionObserver，transform translateY(20px) → 0 / opacity 0 → 1 over 0.7s，stagger via `.r-d1` / `.r-d2` ...
- **All animation** — 必須在 `prefers-reduced-motion: reduce` 下停用（已加）

## Do's and Don'ts

### Do
- **Surface 對比拉層次** — light → light-alt → light-card 三層，dark → dark-2 → dark-deep 三層。一個 section 之內可以混
- **Gold accent 點到為止** — 每段最多出現 1-2 次（章節 eyebrow、`.accent` 重音字、CTA link）。Gold 不能拿來當大面積 surface（除了 `.tier-agent` 那一張刻意的 hero card）
- **Eyebrow chip 留給「真的需要章節 framing」的場合** — Part 0 開場、Part 3 安裝、Part 5 實作、Part 7.1 deep dive 之類的關鍵 framing 點。一般 section title 直接開講
- **Glass / blur 限定決定性場合** — nav（已用）+ 未來 floating panel + indicator。每張 card 都 glass = 違反 absolute ban
- **CJK + 英文 inline 字級對齊** — 不要為了「強調英文 term」放大英文
- **Animation 服務功能** — hero drift（生命感）、`▋` cursor（terminal 活著的訊號）、flow stagger（引導視線）、scenario fadein（展開回饋）

### Don't
- **❌ Side-stripe borders** — `border-left / border-right: 3px solid <accent>` 一律禁用，這是 impeccable absolute ban。如要強調 callout，改用 full border / background tint / leading icon
- **❌ Hero-metric template** — big number + small label 的 4-up stats 是 SaaS landing 反射。如要呈現數字，挑 1-2 個最重要的、用 typographic 重量處理
- **❌ Identical 3-up card grid 反覆出現** — 同一頁出現超過 2 次 3-up grid 就要打散。改 asymmetric / 1-row scroll / vertical stack
- **❌ Mono 當裝飾** — 章節編號、tag、eyebrow 用 mono 是「技術感」反射。Mono 留給 code / command / file / timestamp
- **❌ 全部 card 加 backdrop-filter** — glass 是 spice，不是 base
- **❌ 載入沒用的 web font** — Inter 在 system stack 已被 SF Pro 取代，CJK 已被 PingFang 取代，Noto Sans TC 為 Linux fallback。`@import` 三個 family 14 個 weight 是浪費
- **❌ 動畫不檢查 `prefers-reduced-motion`** — 任何新加的動效都要有 media query 護欄
- **❌ Color-only state signal** — ✅/⏳/⚠️ 等狀態必須有 emoji / icon / 文字輔助，不能只靠顏色
- **❌ Em dash `—` 在英文段落** — 中文段落用 `——` OK（標準標點），英文段落改 colon / semicolon / period
