# 狀態列面板安裝指南（claude-hud）

> **這份文件是給 Claude Code 看的。** 學員只要把這份文件餵給 Claude Code（拖進來，或說「請依照 panel-setup.md 幫我裝狀態列面板」），它會帶著學員把面板裝好。
>
> 目標：**以人為的互動越少越好**。學員只需要在被提示時，把三行指令貼進 Claude Code 的輸入框、按 Enter。

---

## 這個面板是什麼

`claude-hud` 是一個 Claude Code 外掛，會在畫面底部加一條**即時狀態列**，隨時顯示：

- 現在用的是哪個模型（例如 Opus / Sonnet）
- context window 用掉多少 %
- 這段時間花了多少 token / 用量
- 載入了幾個 CLAUDE.md、MCP、hook
- 剛剛做了幾次 Edit / Bash / Read

對學員的價值：**看得到「AI 正在用多少資源、花多少錢」**，呼應第 1.1 章的模型成本概念。

來源（Source of Truth）：<https://github.com/jarrodwatts/claude-hud>

---

## 給 Claude Code 的核心規則

你正在幫一位**非 CS 背景的 Tech Management 碩士生**安裝 claude-hud。請遵守：

1. **用繁體中文溝通**，技術名詞英文。
2. **這三個是 slash 指令，必須由學員親自貼進 Claude Code 的輸入框**（不是終端機 / 不是 Bash）。你（Claude Code）無法替自己執行 slash 指令，所以你的工作是：清楚地把指令給學員、解釋、等他貼完回報、再驗證。
3. **一次給一行，等學員回報成功再給下一行**，不要三行一起丟。
4. 出錯就停下來看錯誤訊息，對照下方「常見錯誤」處理。

---

## 安裝步驟（學員在 Claude Code 輸入框依序貼上）

**告訴學員：** 「接下來請把我給你的指令，一行一行貼到這個 Claude Code 的輸入框，按 Enter。第一行是加入外掛市集。」

### 第 1 行 · 加入 marketplace
```
/plugin marketplace add jarrodwatts/claude-hud
```
看到「marketplace added」之類的成功訊息 → 進下一行。

### 第 2 行 · 安裝外掛
```
/plugin install claude-hud
```
看到安裝成功 → 進下一行。

> ⚠️ **Linux 學員若失敗**（`EXDEV: cross-device link not permitted`）：請學員先離開、在終端機跑 `mkdir -p ~/.cache/tmp && TMPDIR=~/.cache/tmp claude` 重開 Claude Code，再貼一次第 2 行。macOS / Windows 通常不會遇到。

### 第 3 行 · 啟用狀態列
```
/claude-hud:setup
```
跑完面板會**立刻出現在畫面底部，不用重啟**。

---

## 驗證

**告訴學員：** 「看畫面最底下，是不是多了一條狀態列，上面有模型名稱、context %、用量？有 = 裝好了。」

如果沒出現：
- 確認第 2 行的安裝有成功（再貼一次 `/plugin install claude-hud`）
- 再跑一次 `/claude-hud:setup`
- 仍然沒有 → 完全關閉並重開 Claude Code，狀態列會在新 session 出現

---

## 常見錯誤

| 症狀 | 處理 |
|------|------|
| 貼指令沒反應 | 確認是貼到 **Claude Code 輸入框**，不是終端機；slash 指令開頭一定是 `/` |
| `marketplace not found` | 檢查有沒有打錯 `jarrodwatts/claude-hud`，重貼第 1 行 |
| Linux `EXDEV` | 用 `TMPDIR=~/.cache/tmp claude` 重開再裝（見上方） |
| 裝完面板沒出現 | 重跑 `/claude-hud:setup`；再不行就重開 Claude Code |

---

## 完成

面板出現後，這份文件的任務就完成了。請告訴學員：「狀態列裝好了，之後你隨時都看得到 AI 用了多少資源。」
