# Handoff — design-system + Antigravity tutorial

## 狀態摘要

- 已建立可複用 `design-system/` 模板，含 token CSS、gallery、contract、audit script、static-site starter。
- 已建立 `setup-tutorial/` Claude Code 安裝教學站，仍可作為設計系統用法參考。
- 已建立 `antigravity-tutorial/` 學生自學站：6 個 item、素材瀏覽器、checklist、小鴨進度、無錄影模式。
- 已從 `https://github.com/museReed/claude-code-workshop-jr-student.git` clone 生成 `antigravity-tutorial/assets/js/materials.js`。
- 已新增正式 design-system 元件 `ds-step-block`，並同步到 repo 內所有 design-system.css 複本。
- 已更新小鴨元件：走路速度慢 2 倍，抵達後使用 `dance`，不再新增 `sit` 狀態。
- 已同步 `ds-step-block` 到 scratchpad 的 `gallery.html` 和 `design-system.css`，對應使用者指定的 `file:///private/tmp/.../scratchpad/gallery.html#`。
- 最近稽核：`setup-tutorial`、`antigravity-tutorial`、`design-system/templates/static-site` 都通過 `audit-ui-contract.py`。

## 必讀檔案

- `/Users/reed/Projects/claude-code-workshop/design-system/HANDOFF-FOR-NEXT-SESSION.md` — 新 session 使用 design token 的前置規則。
- `/Users/reed/Projects/claude-code-workshop/design-system/docs/UI-COMPONENT-CONTRACT.md` — UI 元件契約，規定何時用既有 `ds-*`、何時可自製。
- `/Users/reed/Projects/claude-code-workshop/design-system/docs/gallery.html` — repo 內 gallery，已含 `ds-step-block` 展示。
- `/private/tmp/claude-501/-Users-reed-Projects-claude-code-workshop/336eb592-4de8-4231-8498-07f742f1fca2/scratchpad/gallery.html` — 使用者指定的 scratchpad gallery，也已同步 `ds-step-block`。
- `/Users/reed/Projects/claude-code-workshop/antigravity-tutorial/assets/js/steps.js` — Antigravity 6 個 item 的內容來源。
- `/Users/reed/Projects/claude-code-workshop/antigravity-tutorial/assets/js/materials.js` — 學生素材 repo 的檔案樹與內容來源。
- `/Users/reed/Projects/claude-code-workshop/antigravity-tutorial/assets/js/app.js` — Antigravity SPA、素材瀏覽器、Markdown renderer、copy、progress 邏輯。

## 下一步

1. 若要把 Antigravity 站的非終端機步驟改成正式 `ds-step-block`，先更新 `antigravity-tutorial/assets/js/app.js` 的 `renderCommand()`：`lang:"text"` 應改渲染 step block，`lang:"bash"/"slash"` 才使用 `ds-term`。
2. 改完後執行：
   ```bash
   node --check antigravity-tutorial/assets/js/app.js
   python3 design-system/scripts/audit-ui-contract.py --project antigravity-tutorial --design-system design-system/assets/css/design-system.css
   ```
3. 視覺驗證：開 `http://127.0.0.1:8789/`（若 server 不在，於 `antigravity-tutorial/` 跑 `python3 -m http.server 8789`）。
4. 若要檢查 scratchpad gallery，開：`file:///private/tmp/claude-501/-Users-reed-Projects-claude-code-workshop/336eb592-4de8-4231-8498-07f742f1fca2/scratchpad/gallery.html#`。

## 已知問題

- Git status 顯示 repo 原本已有多個 unrelated modified/untracked 檔案；本 handoff commit 只會加入交接文件，不會整理其他工作檔。
- `antigravity-tutorial` 尚未把 `lang:"text"` 指令全面改用 `ds-step-block`，目前只是 design-system 已具備正式元件。
- Scratchpad 路徑是暫存區，雖已同步但可能被系統清除；repo 內 `design-system/docs/gallery.html` 才是持久版本。
