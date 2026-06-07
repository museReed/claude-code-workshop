# GitHub 設定指南（註冊 → 建 repo → push）

> **這份文件是給 Claude Code 看的。** 學員把這份文件餵給 Claude Code（拖進來，或說「請依照 github-setup.md 幫我設定 GitHub」），它會帶學員把帳號接好、建立一個個人 repo、並把成果 push 上去。
>
> 目標：**以人為的互動越少越好**。學員只需要做兩件事：(1) 在瀏覽器註冊 GitHub 帳號、(2) 在 `gh auth login` 時於瀏覽器按授權。其餘全部由 Claude Code 自主執行。

---

## 為什麼要做這步

GitHub 是程式碼與文字檔的**雲端倉庫**：把今天的成果 push 上去，就有了**雲端備份、版本歷史、可分享的連結**。這是你成果的「歸宿」之一（另一個是 Obsidian）。

---

## 給 Claude Code 的核心規則

你正在幫一位**非 CS 背景的 Tech Management 碩士生**設定 GitHub。請嚴格遵守：

1. **用繁體中文溝通**，技術名詞英文；每個動作先一句話說明「我要做什麼、為什麼」。
2. **執行任何指令前先說明，跑完看 output 確認成功再進下一步**，失敗就停下來解釋。
3. **只有兩個動作需要學員親自做**：瀏覽器註冊、`gh auth login` 的瀏覽器授權。其餘你自己跑。
4. **不要把任何 token / 密碼寫進檔案**。`gh auth login` 會安全地保管憑證。
5. 不確定就問學員，不要猜。

---

## Step 1 · 註冊 GitHub 帳號（學員手動，瀏覽器）

**告訴學員：**
> 「先註冊一個免費 GitHub 帳號。我幫你開註冊頁，你填 email、設密碼、選一個 username（之後會出現在你的作品網址裡，建議用好記的英文名）。驗證完 email 後回來告訴我，並把你的 **username** 給我。」

開啟 <https://github.com/signup>，等學員回報「註冊好了」+ 提供 username。

> 已經有 GitHub 帳號的學員：直接跳到 Step 2。

---

## Step 2 · 安裝 GitHub CLI（`gh`）

> **跳過條件：** 先跑 `gh --version`，有版本號就跳到 Step 3。

**告訴學員：** 「我裝一個叫 `gh` 的小工具，它讓我可以直接幫你操作 GitHub，不用你一直點網頁。」

```bash
# macOS（有 Homebrew）
brew install gh

# macOS（沒有 Homebrew）→ 改用官方安裝頁
#   開 https://cli.github.com/ 下載安裝，裝完請學員重開 terminal

# Windows
winget install --id GitHub.cli
```

驗證：
```bash
gh --version
```

---

## Step 3 · 登入 GitHub（`gh auth login`，學員瀏覽器按授權）

**告訴學員：** 「現在把這台電腦跟你的 GitHub 帳號連起來。我跑登入指令，會跳出一個一次性代碼，你在瀏覽器貼上、按授權就好。」

執行（用這組非互動參數，盡量減少提問）：
```bash
gh auth login --hostname github.com --git-protocol https --web
```

- 終端機會顯示一段 **one-time code**，並開啟瀏覽器。
- 請學員把 code 貼到瀏覽器、按 **Authorize**。
- 回到終端機看到 `✓ Logged in as <username>` = 成功。

驗證：
```bash
gh auth status
```

設定 git 身分（若尚未設定，用 GitHub 帳號資訊）：
```bash
git config --global user.name  "$(gh api user --jq .login)"
git config --global user.email "$(gh api user --jq '.id')+$(gh api user --jq .login)@users.noreply.github.com"
```

---

## Step 4 · 建立 repo 並 push（Claude Code 自主執行）

**告訴學員：** 「接下來我自己來：幫你開一個新的 repo，放一個起始檔案，推上 GitHub。你看著就好。」

在學員目前的工作資料夾執行（若資料夾還沒有 git，就初始化）：

```bash
# 1. 準備一個起始檔案（若資料夾是空的，給它一個 README）
[ -f README.md ] || printf '# %s\n\n我的 Claude Code Workshop 成果。\n' "$(basename "$PWD")" > README.md

# 2. 初始化 git（若尚未初始化）
git rev-parse --is-inside-work-tree >/dev/null 2>&1 || git init -b main

# 3. 第一次 commit
git add -A
git commit -m "First commit from Claude Code Workshop" || echo "（沒有新變更可 commit，繼續）"

# 4. 建立 GitHub repo 並一次 push（repo 名用資料夾名，私人 repo）
gh repo create "$(basename "$PWD")" --private --source=. --remote=origin --push
```

> 若 `gh repo create` 說 repo 已存在：改用 `git push -u origin main`。

**告訴學員：** 「好了，我幫你開了一個 GitHub repo 並把檔案推上去。」打開來看：
```bash
gh repo view --web
```

---

## 驗證

```bash
gh repo view --web   # 瀏覽器打開你的新 repo
```
在 GitHub 頁面看到剛剛的 `README.md`（或你的檔案）= **成功**。

---

## 之後怎麼用（一句話）

以後每次想備份成果，在資料夾裡跑這三行（或直接叫 Claude Code「幫我 push 上 GitHub」）：
```bash
git add -A && git commit -m "update" && git push
```

---

## 常見錯誤

| 症狀 | 處理 |
|------|------|
| `gh: command not found` | Step 2 沒裝好 / 沒重開 terminal；重做 Step 2 |
| `gh auth login` 卡住 | 確認瀏覽器有貼 one-time code 並按 Authorize；可重跑指令 |
| `repository already exists` | 改跑 `git push -u origin main` |
| push 被拒（non-fast-forward） | 先 `git pull --rebase origin main` 再 `git push` |
| 學員沒有 Homebrew 也裝不了 gh | 改用官方安裝頁 <https://cli.github.com/>，或先跳過、workshop 後補做 |
