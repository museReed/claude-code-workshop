# Handoff — jr-student 安裝文件大改版 + 乾淨 VM 驗證

**類型**：continuation
**日期**：2026-07-10
**工作 repo**：`/Users/reed/Projects/claude-code-workshop-jr-student`（branch `main`，已 push，HEAD `729cde0`）

## 狀態摘要（做了什麼）

把 workshop 安裝文件從頭整頓並全部 push 上 GitHub：
- 資料夾重組 + **ASCII 化**：`agent-setup/`（AI 讀）、`student-guide/`（人讀）、`exercises/career/`。
- 安裝流程拆**兩階段**：`to_IDE_AI_Agent_setup.md`（給 Antigravity 裝 Node + Claude Code/Codex、提醒註冊 GitHub）→ `to_CLI_AI_Agent_setup.md`（給 claude/codex 做 GitHub + 面板）。
- IDE 由 **Cursor 改 Antigravity**；角色改「AI Agent」；支援 **Claude Code + Codex** 雙路。
- **安裝一律由 agent 指令直裝、不導官網**：Node（無 brew 抓官方 .pkg / winget）、gh（無 brew 抓官方 release zip 放進 npm 全域 bin）。
- `github-setup.md` 降為 to_CLI 的「細部參考」；狀態列面板改**網頁**帶學員操作（`musereed.github.io/jr_workshop_setup_env/#/item/status-panel`），刪除 panel-setup.md + 空 skill 資料夾。
- 開了一台**乾淨 macOS 26.3 VM**（UTM）準備實測，但尚未跑完驗證。

## 必讀檔案

- `claude-code-workshop-jr-student/agent-setup/to_IDE_AI_Agent_setup.md` — 第 1 階段安裝主文件，Node 直裝邏輯在 Step 2.5。
- `claude-code-workshop-jr-student/agent-setup/to_CLI_AI_Agent_setup.md` — 第 2 階段入口（GitHub + 面板）。
- `claude-code-workshop-jr-student/agent-setup/github-setup.md` — gh 免 brew 直裝 + 個人 repo 職責邊界（回應實測問題）。
- 記憶 `jr-student-i18n-plan` — 延後的繁/簡/英 i18n 計畫（注意：資料夾名這輪已改 ASCII，套用時要對齊 `agent-setup`/`student-guide`/`exercises`）。

## 下一步

1. **在乾淨 VM 裡實測 ASCII + 免 brew 版**：VM 已裝好在**內建** `~/Library/Containers/com.utmapp.UTM/Data/Documents/macOS.utm`（macOS 26.3，跟主機同版）。用先前給的兩段測試 prompt（IDE 階段餵 to_IDE、CLI 階段餵 to_CLI），重點看「無 Homebrew 直裝 gh」「repo 建在 ~/Desktop/my-claude-workshop 不誤 push 素材 repo」。
2. 收 agent 回報的「文件問題清單」→ 據此再修文件。

## 已知問題 / 待清理

- **VM 未搬到外接**：先前搬移中途誤按 play 導致外接半成品，已中止;VM 留在內建。外接殘留待清：`/Volumes/Muse_AI_Core/VMs/macOS.utm`（半成品）。IPSW 在 `/Volumes/Muse_AI_Core/UniversalMac_26.3_25D125_Restore.ipsw`。要搬外接的話：VM 關機 + UTM 結束後用 `cp` 複製、確認能開再刪內建（別再用 mv、別中途開）。
- **Antigravity 自身 bug**：會把含 `~` 的路徑包雙引號導致 `~` 不展開——repo 端改不了，ASCII 路徑已緩解。
- macOS guest 需主機版本 ≥ guest（本次踩過：UTM 預設抓最新 26.5.2 > 主機 26.3 裝不動，改用 26.3 IPSW 解決）。
