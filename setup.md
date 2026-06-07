# Workshop Setup Instructions

> **這份文件是給 Cursor AI 看的。** 學員只要把這份文件拖進 Cursor 的 Composer / Agent,跟它說「請依照這份文件幫我設定環境」,它會帶著學員一步步做完。
>
> 學員的角色:**看、確認、按 Allow、偶爾貼一段 key**。

---

## 給 Cursor AI 的核心規則

你正在幫一位**非 CS 背景的 Tech Management 碩士生**設定 Claude Code 環境。請嚴格遵守以下原則:

1. **用繁體中文跟學員溝通**,技術名詞英文。不要假設他懂 `npm`、`brew`、`export` 是什麼——每個動詞都先用一句話解釋。
2. **每個 Step 開始前,先告訴學員「我接下來要做什麼、為什麼」**,然後等學員說 OK 再開始。
3. **執行任何 sudo / 修改 shell config / 開外部網站前,務必先問學員確認。**
4. **跑完每個指令,看 output 確認成功,再進下一步。** 失敗就停下來解釋,不要硬往下。
5. **如果某步驟學員系統已經做好了,跳過。** 例如 `node -v` 顯示 v18+,就不用再裝 Node.js。
6. **不確定的時候,問學員,不要猜。**

---

## Step 1 · 偵測系統與現有環境

**告訴學員:**
> 「我先檢查你的系統現有狀態——看你已經有什麼、還缺什麼。這個步驟不會改任何東西。」

**執行以下檢查並把結果報給學員:**

```bash
# macOS / Linux
echo "===== OS ====="
uname -s

echo "===== Node.js ====="
node -v 2>/dev/null || echo "❌ NOT INSTALLED"

echo "===== npm ====="
npm -v 2>/dev/null || echo "❌ NOT INSTALLED"

echo "===== Claude Code ====="
claude --version 2>/dev/null || echo "❌ NOT INSTALLED"

echo "===== Homebrew (macOS) ====="
which brew 2>/dev/null || echo "❌ NOT INSTALLED (沒裝沒關係)"

echo "===== API key ====="
[ -n "$ANTHROPIC_API_KEY" ] && echo "✅ ANTHROPIC_API_KEY 已設定" || echo "❌ ANTHROPIC_API_KEY 未設定"
```

Windows PowerShell:
```powershell
Write-Host "===== OS ====="; (Get-CimInstance Win32_OperatingSystem).Caption
Write-Host "===== Node.js ====="; try { node -v } catch { "❌ NOT INSTALLED" }
Write-Host "===== npm ====="; try { npm -v } catch { "❌ NOT INSTALLED" }
Write-Host "===== Claude Code ====="; try { claude --version } catch { "❌ NOT INSTALLED" }
Write-Host "===== API key ====="; if ($env:ANTHROPIC_API_KEY) { "✅ 已設定" } else { "❌ 未設定" }
```

**根據結果,告訴學員接下來要做哪幾個 Step**(已裝好的跳過)。

---

## Step 2 · 安裝 Node.js v18+

> **跳過條件:** 如果 Step 1 看到 `node -v` 是 v18 或以上,直接跳到 Step 3。

**告訴學員:**
> 「Node.js 是 Claude Code 的基底——就像引擎裡的汽油,沒它跑不起來。我幫你裝。」

### 路徑 A:macOS + 已有 Homebrew

如果 `which brew` 有結果:
```bash
brew install node
```

### 路徑 B:macOS 沒有 Homebrew

**告訴學員:**
> 「你的 Mac 沒有 Homebrew(常用的套件管理工具)。我們直接去官網下載安裝檔。等下會打開瀏覽器,你下載 LTS(長期支援版),雙擊跑完安裝程式後告訴我。」

打開 https://nodejs.org/ ,等學員回報安裝完成。

### 路徑 C:Windows

**告訴學員:**
> 「我帶你去 Node.js 官網,你下載 Windows 的 .msi 安裝檔,雙擊一路按 Next 即可。完成後告訴我,**並請重新打開 terminal**(讓系統 reload PATH)。」

打開 https://nodejs.org/ 。

### 驗證(共通)
```bash
node -v   # 應該看到 v18.x.x 或更新
npm -v    # 應該看到版本號
```

**任何一個失敗就停下來**,跟學員一起檢查,不要硬進 Step 3。

---

## Step 3 · 安裝 Claude Code

**告訴學員:**
> 「現在裝 workshop 的主角:Claude Code。它是個 terminal 裡跑的 AI 助手,跟 ChatGPT 不一樣,**它能讀檔、寫檔、跑命令**——所以我們今天才能拿它做事。」

**執行:**
```bash
npm install -g @anthropic-ai/claude-code
```

### 常見錯誤與處理

| 錯誤 | 處理方式 |
|------|---------|
| `EACCES: permission denied` (macOS) | 跟學員說明:「npm 需要管理員權限,等下會請你輸入 Mac 登入密碼」,然後跑 `sudo npm install -g @anthropic-ai/claude-code` |
| `EACCES`(學員不想用 sudo) | 改設定 npm 全域路徑:`mkdir -p ~/.npm-global && npm config set prefix '~/.npm-global'`,再加 `export PATH=~/.npm-global/bin:$PATH` 到 `~/.zshrc`,重 source 後重跑安裝 |
| `npm: command not found` | Step 2 沒做好,回去 Step 2 |
| Windows 「拒絕存取」 | 用「以系統管理員身分執行 PowerShell」重開,再跑安裝 |

### 驗證
```bash
claude --version
```
看到版本號(例如 `1.0.x`) = 成功。

---

## Step 4 · 設定 Anthropic API Key ⚠️ 最容易卡

**告訴學員:**
> 「最後一步,讓 Claude Code 能連上 AI 模型。有兩條路:」
>
> - **路徑 A:** 如果你有 **Claude Pro / Max subscription** → 用訂閱登入(免費,沒額外開銷)
> - **路徑 B:** 如果沒有訂閱 → 用 **API key**(需要信用卡 + 加值最少 $5)
>
> 你是哪一個?

### 路徑 A · Claude Subscription Login

```bash
claude
```

第一次跑 `claude` 會跳出登入流程:
- 跳出一段 URL
- 學員用瀏覽器打開
- 用 Anthropic 帳號(Claude.ai 那個)登入授權
- 回 terminal,看到歡迎訊息 = 成功

**告訴學員:** 「看到 Claude Code 的對話介面就是成功。輸入 `/exit` 先退出,我們繼續下一步。」

### 路徑 B · API Key

**步驟 1:取得 key**

帶學員到 https://console.anthropic.com:
1. 註冊帳號(用 Google 登入最快)
2. **加信用卡** + **加值 $5**(API 是用多少付多少,加 $5 跑 workshop 綽綽有餘)
3. 進「**API Keys**」頁面,點「Create Key」
4. **複製整段 key**(以 `sk-ant-` 開頭),不要關閉那個視窗

**等學員回報「我複製好了」再繼續。**

**步驟 2:設定環境變數**

⚠️ **重要:不要把學員的 key 真的存到任何檔案裡,只引導他自己貼。**

#### macOS / Linux(zsh,現代 Mac 預設)

跟學員說:「請把以下指令的 `<貼你的 key>` 換成你剛複製的 key,然後執行」:

```bash
# 寫進 shell config(下次開 terminal 也記得)
echo 'export ANTHROPIC_API_KEY="<貼你的 key>"' >> ~/.zshrc

# 立即在當前 terminal 生效
source ~/.zshrc
```

#### Windows PowerShell

```powershell
# 永久設定(下次開 terminal 也記得)
[Environment]::SetEnvironmentVariable("ANTHROPIC_API_KEY", "<貼你的 key>", "User")

# 當前 session 也設定(不用重開 terminal)
$env:ANTHROPIC_API_KEY = "<貼你的 key>"
```

**步驟 3:驗證**

```bash
# macOS / Linux
echo $ANTHROPIC_API_KEY | head -c 12   # 應該印出 sk-ant-xxx... 開頭

# Windows
$env:ANTHROPIC_API_KEY.Substring(0,12)
```

若印出空白:
- macOS:跑 `source ~/.zshrc` 再試
- Windows:**完全關閉並重開 PowerShell**(`SetEnvironmentVariable` 對新開的 session 才生效)

**最終測試:**
```bash
claude --version
```
看到版本號 = 成功(此時 Claude Code 還沒被叫起來,只是確認 binary 可用)。

---

## Step 5 · 核心環境完成 + 交棒

**告訴學員:**
> 「✅ 核心環境(Node.js + Claude Code + API key)設定完成。
>
> **檢查清單:**
> - Node.js: [印當前版本]
> - Claude Code: [印當前版本]
> - API key / 登入: 已設定 ✅
>
> 接下來請**離開 Cursor**,回到 terminal,跟講師一起做下一步——`git clone` 拿 workshop 素材,然後在 workshop 資料夾啟動 `claude`。
>
> 啟動 `claude` 之後,還有兩個小設定要做(Step 6、Step 7),這次換 **Claude Code** 帶你做。」

---

## Step 6 · 狀態列面板（在 Claude Code 裡做）

> **接力給 Claude Code。** 學員啟動 `claude` 後,把 `panel-setup.md` 餵給 Claude Code（或說「請依照 panel-setup.md 幫我裝狀態列面板」）。
>
> 內容:安裝 `claude-hud` 外掛,在畫面底部加一條即時狀態列（模型 / context / 用量）。完整步驟見同資料夾的 **[`panel-setup.md`](./panel-setup.md)**。
>
> 完成標準:Claude Code 畫面最底下出現狀態列。

---

## Step 7 · GitHub（在 Claude Code 裡做）

> **接力給 Claude Code。** 把 `github-setup.md` 餵給 Claude Code（或說「請依照 github-setup.md 幫我設定 GitHub」）。
>
> 內容:帶學員註冊 GitHub 帳號,然後 Claude Code 自己 `gh auth login`、`gh repo create`、`git push`,把成果推上雲端。完整步驟見同資料夾的 **[`github-setup.md`](./github-setup.md)**。
>
> 完成標準:學員的 GitHub 上出現一個新 repo,裡面有檔案。

---

> ✅ **全部完成 = Step 1–7 都做完。** 跑完這份 `setup.md`、再依序完成 `panel-setup.md`（Step 6）與 `github-setup.md`（Step 7）,環境才算真正就緒。

---

## 失敗模式速查表(給 Cursor AI 與講師)

| 症狀 | 可能原因 | 解法 |
|------|---------|------|
| `npm: command not found` | Node.js 沒裝好 / PATH 沒重 load | 重開 terminal;若還是不行回 Step 2 |
| `EACCES` 安裝 Claude Code | 全域 npm 權限不足 | `sudo` 或改 `--prefix=~/.npm-global` |
| `claude: command not found`(裝完之後) | npm 全域路徑不在 PATH | `which npm`,找出 npm prefix,把 `<prefix>/bin` 加到 `~/.zshrc` 的 PATH |
| API key 設了 `echo` 卻是空 | shell config 沒重 load / Windows 沒重開 terminal | macOS `source ~/.zshrc`;Windows 完全關閉 PowerShell 重開 |
| Console.anthropic.com 沒辦法刷卡 | 國際信用卡限制(常見於部分卡別) | 換另一張卡;或讓學員暫用講師備用 key |
| Cursor AI 自己卡住或亂答 | 網路 / Cursor 服務問題 | 講師接手,改用手動 setup(備用文件) |

---

## 講師救援包(若 Phase B 整體失敗)

1. **講師備用 API key:** 預先建一把,寫在實體紙片上,需要時直接給卡關的學員
2. **預設環境 zip:** 一份已經設定好的環境參考(僅供示意),AirDrop 給極端卡關者
3. **跳過策略:** 學員卡超過 8 分鐘,**先讓他用講師 key 頂著,workshop 後再個別處理**——不要 30 個人陪 1 個人等
