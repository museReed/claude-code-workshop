# Handoff — jr_workshop_setup_env GitHub Pages publish

## 狀態摘要

- 已把原本 `antigravity-tutorial/` 本地資料夾改名為 `jr_workshop_setup_env/`；母 repo 目前顯示舊資料夾刪除 + 新資料夾 untracked，尚未 commit 這個 rename。
- 已在 `jr_workshop_setup_env/` 加 `.nojekyll`，供 GitHub Pages 靜態站使用。
- 已把 `jr_workshop_setup_env/` 複製到 `/tmp/jr_workshop_setup_env_publish/`，並在該目錄初始化獨立 git repo。
- `/tmp/jr_workshop_setup_env_publish/` 已有 commit `474a2bd Initial workshop setup site`，包含 10 個檔案。
- 嘗試用 `gh repo view museReed/jr_workshop_setup_env` 檢查/建立遠端時遇到 `error connecting to api.github.com`；需要重試網路操作。
- GitHub CLI auth 先前已確認有效：`museReed`，scopes 包含 `repo` 和 `workflow`。
- 本機檢查已通過：`node --check jr_workshop_setup_env/assets/js/app.js`、`node --check jr_workshop_setup_env/assets/js/steps.js`、UI contract audit。
- 使用者明確要求：不要叫 `antigravity-tutorial`，獨立 repo / 網站名稱使用 `jr_workshop_setup_env`。

## 必讀檔案

- `/Users/reed/Projects/claude-code-workshop/jr_workshop_setup_env/assets/js/steps.js` — 6 個 item 文案來源，已針對非工程師 TA 白話化。
- `/Users/reed/Projects/claude-code-workshop/jr_workshop_setup_env/assets/js/app.js` — SPA renderer、閱讀資料頁、FAQ、深色 terminal markdown renderer、copy/checklist/小鴨邏輯。
- `/Users/reed/Projects/claude-code-workshop/jr_workshop_setup_env/assets/css/app.css` — app-level wrapper 樣式；不可覆寫既有 `ds-*` 元件。
- `/Users/reed/Projects/claude-code-workshop/jr_workshop_setup_env/assets/css/design-system.css` — 發佈站內帶的 design-system CSS。
- `/tmp/jr_workshop_setup_env_publish/` — 已準備好的獨立 repo 工作目錄；commit `474a2bd` 可直接 push。

## 下一步

1. 重試 GitHub 網路操作（必要時用 escalated command）：
   ```bash
   cd /tmp/jr_workshop_setup_env_publish
   gh repo create museReed/jr_workshop_setup_env --public --source=. --remote=origin --push
   ```
   若 repo 已存在，改用：
   ```bash
   git remote add origin https://github.com/museReed/jr_workshop_setup_env.git 2>/dev/null || true
   git push -u origin main
   ```
2. 啟用 GitHub Pages，source 設為 `main` branch `/` root：
   ```bash
   gh api -X POST repos/museReed/jr_workshop_setup_env/pages -f source='{"branch":"main","path":"/"}'
   ```
   若已啟用，改查：
   ```bash
   gh api repos/museReed/jr_workshop_setup_env/pages
   ```
3. 回報 GitHub repo URL 與 Pages URL，預期 Pages URL 類似：
   `https://musereed.github.io/jr_workshop_setup_env/`。
4. 視需要再回母 repo：只 stage `jr_workshop_setup_env/` 與 `antigravity-tutorial/` delete 來記錄 rename；不要 stage unrelated modified/untracked 檔案。

## 已知問題

- 母 repo 工作樹是 mixed 狀態，包含多個 unrelated modified/untracked 檔案；不要使用 `git add -A`。
- `git mv antigravity-tutorial jr_workshop_setup_env` 曾因 `.git/index.lock` 權限失敗，已用一般 `mv` 完成資料夾 rename。
- 目前可能仍有本機 server 在 `8890`，但發佈任務不依賴它。
- GitHub API 網路曾失敗，不是 gh auth 問題；重試時若 sandbox 網路錯誤，需用 `require_escalated`。
