# Product

## Register

brand

## Users

King's College London Technology Management 碩士生（主修）— 非 CS 背景，多數從未使用過 terminal / CLI。年齡 22-30，英語授課，但這份教材以**繁體中文為主、技術名詞保留英文**。

使用情境分兩種，**主要是第一種**：
1. **講師（Wei）現場投影 / 導覽** — 3 小時 workshop 期間在大螢幕上跑，講師人在現場、學員看著聽。
2. **學員課前 / 課後自己看** — 拿到 link 自己捲、自己展開 scenario 卡、回頭查 Part 6 在哪。

Job to be done：讓非 CS 背景的學員相信「我可以指揮 AI agent 做事」，並親手跑過一次「下指令 → 看輸出 → 判斷」的完整循環。

## Product Purpose

這份網頁**取代傳統 slide**，作為 3 小時 workshop 的單一教材 + 講師 console + 課後資源。它不是宣傳品，不是 SaaS landing page，也不是 PowerPoint 的網頁版。

成功的定義：
- 投影時學員不會打瞌睡 — 視覺有層次、有 ambient motion、概念有恰當的視覺承載
- 學員看完知道「Claude Code 跟 ChatGPT 不一樣」、「CCC 框架是什麼」、「Academic Integrity 紅線在哪」
- 講師可以在 3 小時內順著網頁一路講下去，不需要切回 slide / 切回 Notion / 切回任何其他工具

## Brand Personality

**製作感 / 透明 / 補上現代**

三個詞拆解：
- **製作感**：學員看了會覺得「這份是某個有設計意識的人精心做的，不是隨便交差」— KCL 講師親手做，不是模板拼裝
- **透明**：視覺上允許 layered glass、frosted card、半透明 panel；tone 上對學員誠實（包含告訴他們「AI 不能做什麼」「為什麼這比知道它能做什麼更重要」）
- **補上現代**：基底是 KCL navy + gold 的學院色彩，但用 Arc Browser / Linear 的當代手法執行 — 不是把 Apple HIG 套上 KCL logo，是真的長得像 2026 的東西

視覺路線參考：**Arc Browser**（glass card + 亮邊 + 漸層）、**Linear**（深底 + 質感筆觸 + 設計感產品）。Glass effect 允許但必須 deliberate — 1-3 處決定性使用，不要到處灑。

## Anti-references

**明確不要像**：
1. **SaaS landing page**（Stripe / Vercel / Linear marketing 頁那種「hero stat + 3-up feature card + testimonial + CTA」模板） — 不要 hero-metric template、不要重複 3-up card grid、不要 mono eyebrow chip 出現在每個 section
2. **PowerPoint / Google Slides** — 不要項目符號 bullet list、不要 clipart icon、不要「標題頁 → 內容頁 → 結語頁」的 slide 思維
3. **MOOC 平台**（Coursera / edX） — 不要「Enroll」按鈕的 LMS 感
4. **AI-generated dev tool landing** — 不要 navy + neon + matrix background + "Built with AI" badge 的訓練料 cliché

**檔案內已經有的問題**（critique 揪出來的）：
- 6 處 `border-left: 3px solid gold` 的 side-stripe — impeccable absolute ban
- 5 處以上 3-up grid 反覆出現 — identical card grid 反射
- 10+ 個 section 的 `.eyebrow` mono uppercase tracked — section grammar AI scaffolding
- hero-stats 4 格 — hero-metric template

## Design Principles

1. **Show, don't decorate** — 動畫 / glass / motion 必須承擔功能（解釋概念 / 引導視線 / 標示當前位置），不能是裝飾。"沒有就少一點理解" 的才留。

2. **講師時間是 1st-class** — 任何設計決策，先問「投影時這個讓講師更好講、還是更難講」。Eyebrow 過多 = 講師每段都要重新建立 context，是負擔。Schedule 表格 clickable = 講師可以跳轉，是支援。

3. **Glass is rare, ambient is everywhere** — Glass effect 全頁限制在 1-3 處決定性使用（nav 已用 1 處）。但 ambient motion（hero gradient 飄移、blinking cursor、stagger reveal）可以鋪滿，因為它服務「製作感」這個 personality。

4. **CJK + Latin 混排必須對齊** — 繁中為主、英文 inline 出現是常態。字級、行高、字重的選擇必須同時讓兩種腳本看起來體面。砍掉沒用的 web font（Inter 在 system stack 已有 SF Pro，多餘）。

5. **教學紅線是品牌的一部分** — Academic Integrity 不是 footer 的法律免責文，是設計表現的一部分。各 scenario 的紅線文字、CLAUDE.md 範例裡的 Don't 段、closing 的「你不需要會寫 code，但你需要會指揮 AI 寫 code」— 都需要 typographic 上的存在感。

## Accessibility & Inclusion

- **WCAG 2.1 AA 為基線** — KCL 公立大學標準。所有文字對比 ≥4.5:1（normal text），≥3:1（large text）
- **鍵盤可用** — scenario 卡的展開 / nav anchor / 任何 interactive 元素都要有 keyboard 操作 + focus state
- **`prefers-reduced-motion` 完整支援** — 包括 hero ambient drift、blinking cursor、stagger reveal、scenario fadein animation 都要尊重系統設定
- **CJK 字體 fallback chain 健康** — Noto Sans TC 必要時可用，但 macOS / iOS 學員應優先吃到 PingFang TC（已在 stack 內）
- **無 colour-only meaning** — ✅/⏳/⚠️ 等狀態 icon 不能單靠顏色傳達；目前用 emoji 是 OK 的（emoji 本身有 shape difference）
