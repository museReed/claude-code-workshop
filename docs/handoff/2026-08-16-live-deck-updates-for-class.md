# 交接：把上課用的 slides.html 補到今天要教的內容

- **類型**：continuation
- **分支**：`slides-2026-08-16`（worktree，從 `origin/main` 開的；**所有 commit 都已 push 到 main**）
- **線上**：https://musereed.github.io/claude-code-workshop/slides.html（72 頁，已部署）
- **前一份**：`docs/handoff/2026-08-15-slides-rebuild-and-feedback-fixes.md`（在 jr-setup-ui repo）

## 狀態摘要

1. **今天上課用的是現行 `slides.html`**（Reed 8/16 凌晨拍板）——新網站 `jr-workshop-slides`
   來不及，改成直接補現行 deck。60 → 72 頁，22 個 commit 全部推上 main 並確認線上生效。
2. **新增八頁**：常用指令 ×2（Claude/Codex）、Obsidian ×2、Remote Control ×3、
   AI CLI + Obsidian、AI App、jr-setup-ui 安裝、活動素材下載。
3. **權限段重新定位**：Auto／Accept Edits 是一般人的預設、白名單降為進階，
   並講明嚮導已幫學生裝好 acceptEdits 白名單。
4. **課程地圖重做**：不分上下半場，改用 `jr-workshop-slides` 的段落順序與名稱，一頁 6 列共兩頁。
5. **修掉 deck 本身的換頁重影**（兩張同時半透明），並把全文 12 處「不是⋯⋯」改成正面表述。
6. **jr-setup-ui 也推了一版**（`fd11d5a`，另一個 repo）：Typeless 選用列 + 新的 `optional` 燈號。

## 必讀檔案

| 檔案 | 為什麼要讀 |
|---|---|
| `slides.html` | 本體。新加的頁都用 `id="s13b/s13c/s13d/s13e/s22a/s-cmd*/s-obs*/s-remote*"` 找得到 |
| `docs/handoff/2026-08-16-live-deck-updates-for-class.md` | 本檔 |
| `~/Projects/jr-workshop-slides/docs/migration-map.md` | 舊 deck 50 頁 → 新網站的對照表，含七處「被壓掉的 prompt / 對照表」清單 |
| `~/Projects/jr-workshop-slides/src/model.js` | 新網站的 13 段結構——課程地圖的順序與段名就是照這份 |

## 下一步

1. **Reed 還沒決定的三件事**（都不擋上課）：
   - AI IDE 那個彈窗要不要也改成優缺點（GUI／CLI 已改，IDE 還是舊的「適合誰」）
   - 後面那張「下半場地圖」（`id="s68-agenda"`）跟新課程地圖重複，刪掉還是改標題
   - 課程地圖各段的時間分配是估的，要不要調數字
2. **兩處我沒現場驗過的操作**，Reed 按一次比較準：
   - Claude 的 `Esc Esc`（我寫「叫出前面的訊息，挑一則跳回去重講」）
   - Codex 的 `Esc` 打斷、`Shift + Tab` 的 Plan／Default 循環
3. **課後**：新網站 `~/Projects/jr-workshop-slides`（63 頁）還沒 `git init`，
   要接著做就照 `docs/migration-map.md` 把舊內容搬完。

## 已知問題

- **本機 4175 的 server 是從這個 worktree 開的**，session 結束後 worktree 會失效；
  之後要在本機看，從自己的 repo `git pull` main 再開 server。
- `~/Projects/claude-code-workshop` 的工作樹**在 `slides-playwright-mcp` 分支且有 53 個未提交變更**
  （含整個目錄被刪除）。今天全程沒碰它——要合併 main 前先確認那些變更。
- `claude2code-design-system` 有一個未提交的修正：時間軸動畫 `--i` 延遲改成不寫死項次
  （原本只寫到第三項，第四項以後不會依序長）。要不要 commit 由 Reed 決定。
- 新網站那邊 `assets/css/design-system.css` 是設計系統的副本，公開前要確認可不可以公開。
