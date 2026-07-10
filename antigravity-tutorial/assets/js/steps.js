/* Antigravity 環境建置教學網站內容資料
   所有 item 文字集中在這裡；render 程式不得寫死 item 文案。 */
window.SETUP_STEPS = [
  {
    id: "install-antigravity",
    num: "01",
    title: "安裝 Antigravity + 下載素材",
    badge: null,
    mac_win: "macOS 為主",
    goal: "裝好並登入 Antigravity，把上課素材 clone 到本機。",
    intro: "環境設定很麻煩——裝 Node、設 PATH、打一堆指令。所以我們不自己裝：先裝一個 AI（Antigravity），再讓它幫我們裝別的 AI。你手動只做兩件事：下載並登入 Antigravity、註冊 GitHub。",
    analogy: "Antigravity 長得像程式編輯器，但裡面住著一個 AI Agent——你用講的，它動手。今天它是我們的「裝機工人」。",
    kind: "steps",
    commands: [
      { label: "① 下載並登入", lang: "text", code: "https://antigravity.google", note: "選你的作業系統下載 → 安裝 → 開啟 → 用 Google 帳號登入（免費、免信用卡）。看到編輯器 + 右側 Agent 面板 = 成功。" },
      { label: "② Clone 上課素材", lang: "bash", code: `cd ~/Desktop
git clone https://github.com/museReed/claude-code-workshop-jr-student.git
cd claude-code-workshop-jr-student && ls exercises/`, note: "git clone = 把 GitHub 上的資料夾複製一份到你電腦。看到 academic、career、collaboration、london-life 四個資料夾 = 素材到手。" },
      { label: "Windows 附註", lang: "text", code: "開 PowerShell（不是 Terminal）；先裝 Git for Windows（連結見課程頁）。", note: null, collapsible: true },
      { label: "macOS 附註", lang: "text", code: "第一次跑 git 可能跳出裝 Xcode Command Line Tools——按同意，等 5–10 分鐘。", note: null, collapsible: true }
    ],
    checklist: ["Antigravity 開得起來且已登入", "看到右側 Agent 面板", "ls 看到 academic / career / collaboration / london-life 四個資料夾"]
  },
  {
    id: "explore-materials",
    num: "02",
    title: "認識上課素材",
    badge: null,
    mac_win: "macOS 為主",
    goal: "搞懂 clone 下來的 repo 裡有什麼、四大類練習各是什麼。",
    intro: "這個資料夾就是今天的教材。下面點任一個檔案，右邊會顯示它的內容——<code>.md</code> 會自動排版。先逛一圈，對素材有個全貌。",
    analogy: null,
    kind: "materials",
    commands: [],
    checklist: ["我知道 exercises/ 底下有四大類練習", "我至少打開看過一個練習的 README"]
  },
  {
    id: "install-agent",
    num: "03",
    title: "Antigravity 初始環境安裝",
    badge: "Claude Code 為主",
    mac_win: "macOS 為主",
    goal: "讓 Antigravity 幫你裝好 Claude Code（Codex 路徑相同）。你的角色從「動手」變「監工」。",
    intro: "<code>setup.md</code> 是一份寫給 AI 看的安裝說明書。你把它交給 Antigravity，它照著幫你裝，你只要看、按 Allow。",
    analogy: "注意那個一直跳出來的 <b>Allow?</b>——AI 每次要動你的電腦都會先問，你按它才跑，不按它就停。這就是 AI Agent 跟網頁版 ChatGPT 最大的差別。",
    kind: "steps",
    commands: [
      { label: "① 打開資料夾", lang: "text", code: "Antigravity → Open Folder → 選桌面的 claude-code-workshop-jr-student → 打開右側 Agent 面板。", note: null },
      { label: "② 把 setup.md 交給它", lang: "text", code: "把 setup.md 拖進 Agent 對話框（或用 @setup.md），輸入下面這句 ↓", note: null },
      { label: "指令（貼進 Agent 對話框）", lang: "prompt", code: "請依照這份 setup.md 幫我設定環境。文件裡寫「Cursor」的地方，就是指你。", note: "這份說明書原本寫給 Cursor，補這句它就懂交接。" },
      { label: "③ 監工 AI 四個動作", lang: "text", code: "AI 會依序：問你有哪家訂閱 → 體檢電腦（===== Node.js ===== 那排）→ 跑 npm install -g @anthropic-ai/claude-code → 請你登入（terminal 跳 URL → 瀏覽器授權 → 回來看到歡迎訊息）。每次 Allow 前看清楚再按。", note: null },
      { label: "Codex 使用者看這裡", lang: "bash", code: "有 ChatGPT Plus 就回答「Codex」，AI 改跑 npm install -g @openai/codex，其餘流程一模一樣。", note: null, collapsible: true }
    ],
    checklist: ["AI 完成環境偵測", "Claude Code（或 Codex）安裝完成", "登入成功、看到歡迎訊息"]
  },
  {
    id: "first-chat",
    num: "04",
    title: "第一次對話",
    badge: null,
    mac_win: "macOS 為主",
    goal: "親手跟 Claude Code 講第一句話，體驗它「能看你的資料夾」。",
    intro: "換主角登場。先 <code>cd</code> 進 workshop 資料夾<b>再</b>啟動 <code>claude</code>——要先走進資料夾它才看得到裡面的檔案，這個順序很重要。",
    analogy: "它真的去看了你的資料夾再回答——這就是 AI Agent 跟網頁版 ChatGPT 最大的不同：它有手有腳，能碰你的檔案。",
    kind: "steps",
    commands: [
      { label: "啟動", lang: "bash", code: `cd ~/Desktop/claude-code-workshop-jr-student
claude`, note: null },
      { label: "第一句話（打進 Claude Code）", lang: "prompt", code: "你好，我現在在哪個資料夾？裡面有什麼東西？", note: null }
    ],
    checklist: ["claude 成功啟動", "它正確講出資料夾裡有哪些東西"]
  },
  {
    id: "status-panel",
    num: "05",
    title: "裝狀態列面板",
    badge: "Claude Code 專屬・選配",
    mac_win: "macOS 為主",
    goal: "（僅 Claude Code）在畫面底部加一條即時狀態列，看得到 AI 用了多少資源。",
    intro: "<code>claude-hud</code> 是 <b>Claude Code 專屬</b>的外掛（Codex 沒有，用 Codex 的同學跳過這步）。這三行是 slash 指令，<b>貼進 Claude Code 的輸入框、一次一行</b>，不是終端機。",
    analogy: null,
    kind: "steps",
    commands: [
      { label: "第 1 行 · 加入 marketplace", lang: "slash", code: "/plugin marketplace add jarrodwatts/claude-hud", note: null },
      { label: "第 2 行 · 安裝外掛", lang: "slash", code: "/plugin install claude-hud", note: null },
      { label: "第 3 行 · 啟用", lang: "slash", code: "/claude-hud:setup", note: "跑完面板立刻出現在底部，不用重啟。" }
    ],
    checklist: ["畫面底部出現狀態列（模型 / context% / 用量）"]
  },
  {
    id: "github-push",
    num: "06",
    title: "AI Agent 幫你上 GitHub",
    badge: null,
    mac_win: "macOS 為主",
    goal: "註冊 GitHub，讓 Claude Code 自己把你的成果 push 上雲端。",
    intro: "GitHub 是你作品的雲端家。唯一要你動手的是註冊帳號，其餘交給 AI。",
    analogy: "GitHub 像工程師的 Instagram——你的作品有個可分享的網址。",
    kind: "steps",
    commands: [
      { label: "① 註冊帳號", lang: "text", code: "https://github.com/signup", note: "填 email、設密碼、選一個好記的英文 username（會出現在你作品網址裡）。已有帳號跳過。" },
      { label: "② 交給 Claude Code", lang: "text", code: "回到 claude，說「請依照 github-setup.md 幫我設定 GitHub」。AI 會跑 gh auth login：terminal 跳一個 one-time code + 開瀏覽器 → 你貼 code、按 Authorize → AI 自己建 repo、push。", note: null },
      { label: "③ 驗證", lang: "bash", code: "gh repo view --web", note: "瀏覽器打開你的新 repo，看到檔案 = 成功。" }
    ],
    checklist: ["看到 ✓ Logged in as <username>", "GitHub 出現新 repo 且裡面有檔案"]
  }
];
