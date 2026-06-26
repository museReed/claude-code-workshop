# Workshop Slides Build — Session Handoff

> 貼這行到新 session 即可：
> **「讀 docs/handoff/2026-06-26-workshop-slides-build.md 繼續工作，cd /Users/reed/Projects/claude-code-workshop 接續」**

---

## 工作環境

| 項目 | 值 |
|---|---|
| Repo | `/Users/reed/Projects/claude-code-workshop`（獨立 repo，非 muse-platform）|
| Branch | `main` |
| Worktree | 無 |
| Issue | 無 |
| 已 merge PR | 無 |
| 部署 URL | `https://musereed.github.io/claude-code-workshop/jr_workshop_slides/` |

## 目標

為 2026-06-27 的 6 小時 Claude Code workshop 建立一套可部署到 GitHub Pages 的互動式 HTML slide deck（TA：只用過 ChatGPT 的大學生/碩士生）。

## 已完成的工作

| Commit | 內容 |
|---|---|
| `8e52c72` | 補 commit assets 目錄（workshop.css、lottie、debug overlay）+ 同步 jr_workshop_slides |
| `de186d0` | 新增 `jr_workshop_slides/` 子路徑 + URL hash 定位（`#N`）|
| 各次 inline edit | S01–S08 全部 slides 建立完成 |

## 當前進度

- [x] 設計系統（CSS token、字型、Slide engine）
- [x] Debug overlay 安裝（🐞 圈選 → fix-list 工作流）
- [x] S01 Cover（hero-ambient Lottie 背景）
- [x] S02 ChatGPT vs Claude Code 兩欄比較
- [x] S03 2026 Why Now 垂直時間軸
- [x] S04 為什麼我（Q→A 節點流）
- [x] S05 為什麼這個 Workshop（問題 + 3 卡答案）
- [x] S06 講師 & 神隊友（Reed + Vivian + Darren 3 欄卡片）
- [x] S07 六小時地圖（暖白背景行列式議程，rows 3–5）
- [x] S08 今天的三個承諾（3 欄箭頭卡片）
- [x] URL hash 導航（`#N` 定位、refresh 保持頁面）
- [x] GitHub Pages 部署
- [ ] **S07 議程補上 rows 1–2** ← 接續點（用戶未確認內容）
- [ ] 後續 slides（T1–T6 理論、P1–P8 實戰內容頁）
- [ ] TA 卡片填入 Vivian / Darren 真實資訊
- [ ] Workshop 前最終驗收 + git push

## 關鍵決策

| 決策 | 結論 | 原因 |
|---|---|---|
| Slide 互動框架 | 自製 single-file HTML（非 Reveal.js） | 最輕量，可直接 GitHub Pages 部署 |
| 公司 logo 來源 | Google favicon API（sz=256）| simpleicons 只有 TikTok，clearbit/brandfetch 已關閉 |
| 字體縮放 | `zoom: 1.25` on `.slide-body` | 全局 +25% 一行搞定 |
| CSS reveal class | `.r` 元素按點擊順序顯示，全部顯示後才換頁 | 配合逐步揭露講解節奏 |
| Debug overlay | `document.body.classList.contains('dbg-active')` guard 保護所有 nav handler | 避免 debug 模式誤觸發 slide 切換 |
| 部署路徑 | `jr_workshop_slides/index.html`（slides.html 副本，路徑改 `../assets/`）| 原站保留，新站用子路徑隔離 |
| S07 背景 | `.slide-warm`（`#F7F3EE`）| 議程頁用暖白做視覺分區 |

## 必讀檔案

1. `slides.html` ← 主要工作檔，所有 slides 在這裡，HTML 改這裡
2. `jr_workshop_slides/index.html` ← 部署用副本，**每次改完 slides.html 要同步**（見注意事項）
3. `assets/css/workshop.css` ← CSS token 定義（`--navy-deep`、`--gold` 等）
4. `assets/js/debug-overlay.js` ← 🐞 debug 工作流說明

## 注意事項

- **同步副本**：每次改完 `slides.html`，必須重新同步 `jr_workshop_slides/index.html`：
  ```bash
  cp slides.html jr_workshop_slides/index.html
  sed -i '' 's|src="assets/|src="../assets/|g; s|href="assets/|href="../assets/|g; s|initLottie(.*, .assets/|initLottie(.*, ../assets/|g' jr_workshop_slides/index.html
  ```
  然後 `git add -A && git commit && git push`
- **CSS reveal class**：JS 用 `.revealed`（index/practice 用 `.visible`），CSS 接受兩者
- **S07 議程只有 rows 3–5**：rows 1–2 內容未確認，暫缺
- **TA 卡片（Vivian/Darren）**：內容是佔位符，上台前需填入真實資訊
- **`assets/` 首次 commit**：之前因 untracked 造成 GitHub Pages 白屏，已在 `8e52c72` 修復
- **`claude-design-prompt.md`**：已建立（未 commit），若需要在 Claude Design 重建 slides 可用

## 下一步（新 session 要做的事）

1. `cd /Users/reed/Projects/claude-code-workshop && open jr_workshop_slides/index.html` 確認目前 8 頁視覺正常
2. 確認 S07 議程 rows 1–2 的內容（向 Reed 詢問或從課程大綱推導）
3. 繼續往後建 slides（下一張應是 T1：Agent 概念介紹，或另一張過場 divider）
4. TA 資訊確定後用 🐞 overlay 更新 S06 Vivian / Darren 卡片
5. 所有 slides 完成後：`cp slides.html jr_workshop_slides/index.html && sed ... && git add -A && git commit -m "feat: complete workshop slides" && git push`

---

*Session 在 workshop 前一天（2026-06-26）產出此 handoff。*
