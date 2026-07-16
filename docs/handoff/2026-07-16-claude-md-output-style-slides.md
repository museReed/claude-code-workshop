# Session handoff: CLAUDE.md and Output style slides

## 狀態摘要

- Branch: `agent/publish-claude-md-slides`
- 將原本混合的 CLAUDE.md／Output style 教材拆解並重新編排。
- 新增兩張 Output style 投影片：回答規格說明與主管摘要格式範例。
- 刪除舊的 CLAUDE.md 範例與兩張重複概念頁，改回下半場地圖。
- 修正 `slide-legacy` 未隱藏造成舊內容疊在每張投影片頂端的問題。
- 修正 Skill 頁官方 Skill 清單與右側卡片的垂直對齊。
- 本機預覽已啟動：`http://127.0.0.1:4173/slides.html`。
- 所有上述變更都已提交，但尚未 push 或發布到 GitHub Pages。

## 必讀檔案

- `slides.html`：所有投影片、樣式與導覽邏輯都在此檔；第六章改動集中在約第 2100 行後。
- `PRODUCT.md`：投影課程的受眾、教材目的與設計原則。
- `DESIGN.md`：KCL navy/gold、字體、投影片版面與無障礙規則。

## 下一步

1. 在本機預覽上繼續依使用者留言調整 `slides.html`；每次變更後重新整理瀏覽器。
2. 完成視覺確認後，執行 `git diff --check` 並建立提交。
3. 準備發布時，從使用者自己的 Terminal 推送：
   `git -C /Users/wangwei/Documents/Codex/2026-07-15/new-chat/work/claude-code-workshop-publish push origin HEAD:main`
4. GitHub Pages 部署完成後，驗證 `https://musereed.github.io/claude-code-workshop/slides.html`。

## 已知問題

- Codex 執行環境可連 GitHub 網路，但無法使用 macOS Keychain 的 GitHub 憑證，無法自行 push。
- GitHub CLI 在此環境無法連線 API，因此沒有確認是否有開啟中的 PR。
- 本機 HTTP server 是暫時程序；若停止，從工作區執行 `python3 -m http.server 4173 --bind 127.0.0.1` 即可重新啟動。
