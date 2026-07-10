/* Antigravity 環境建置教學網站內容資料
   所有 item 文字集中在這裡；render 程式不得寫死 item 文案。 */
window.SETUP_STEPS = [
  {
    id: "install-antigravity",
    num: "01",
    title: "安裝 Antigravity + 下載素材",
    badge: null,
    mac_win: "macOS 為主",
    goal: "裝好並登入 Antigravity，把上課教材資料夾複製到桌面。",
    intro: "一開始最麻煩的是準備電腦：下載工具、登入帳號、把教材放到正確位置。這一頁只做兩件事：先打開 Antigravity，再把上課教材資料夾複製到桌面。",
    analogy: "Antigravity 看起來像一個寫作工作區，旁邊有一位會幫你操作電腦的 AI 助手。今天它的角色是「幫大家準備電腦的人」。",
    kind: "steps",
    commands: [
      { label: "① 下載並登入", lang: "text", code: "https://antigravity.google", note: "選你的作業系統下載 → 安裝 → 開啟 → 用 Google 帳號登入（免費、免信用卡）。看到編輯器 + 右側 AI 助手面板 = 成功。" },
      { label: "② 下載教材資料夾", lang: "bash", code: `cd ~/Desktop
git clone https://github.com/museReed/claude-code-workshop-jr-student.git
cd claude-code-workshop-jr-student && ls exercises/`, agentPrompt: "請幫我把上課教材下載到桌面。請先確認 git 可以使用，然後從 https://github.com/museReed/claude-code-workshop-jr-student.git 下載教材到我的 ~/Desktop。完成後請進入 claude-code-workshop-jr-student 資料夾，列出 exercises/ 內容，確認教材已經下載成功。過程中請用繁體中文說明每一步；如果遇到錯誤，請先停下來告訴我原因與下一步。", note: "這段指令會把 GitHub 上的教材資料夾下載到桌面。最後看到練習資料夾名稱，就代表教材已經到手。" },
      { label: "Windows 附註", lang: "text", code: "開 PowerShell（Windows 的文字指令視窗，不是一般設定頁）；如果電腦還不能下載教材，先安裝 Git for Windows（連結見課程頁）。", note: null, collapsible: true },
      { label: "macOS 附註", lang: "text", code: "第一次下載教材時，macOS 可能會跳出一個工具安裝視窗。按同意，等 5–10 分鐘，再回來繼續。", note: null, collapsible: true }
    ],
    checklist: ["Antigravity 開得起來且已登入", "看到右側 AI 助手面板", "桌面上已經有上課教材資料夾"]
  },
  {
    id: "explore-materials",
    num: "02",
    title: "認識上課素材",
    badge: null,
    mac_win: "macOS 為主",
    goal: "搞懂下載下來的教材資料夾裡有什麼、今天會用到哪些練習。",
    intro: "這個資料夾就是今天的教材。下面點任一個檔案，右邊會顯示內容；<code>.md</code> 是一種會自動排版的文字檔。先逛一圈，知道教材大概放在哪裡。",
    analogy: null,
    kind: "materials",
    commands: [],
    checklist: ["我知道教材裡有哪些練習資料", "我至少打開看過一份入口說明檔"]
  },
  {
    id: "install-agent",
    num: "03",
    title: "Antigravity 初始環境安裝",
    badge: "Claude Code 為主",
    mac_win: "macOS 為主",
    goal: "讓 Antigravity 幫你把主要 AI 工具裝好。你的角色從「自己動手」變成「看著 AI 做、確認每一步」。",
    intro: "<code>setup.md</code> 是一份給 AI 看的安裝說明書。你把它交給 Antigravity，它會照著幫你準備電腦；你只要看清楚它要做什麼，再按允許。",
    analogy: "注意那個一直跳出來的 <b>Allow?</b>——AI 每次要動你的電腦前都會先問你。你按允許，它才會繼續；你不按，它就會停下來。",
    kind: "steps",
    commands: [
      { label: "① 打開資料夾", lang: "text", code: "Antigravity → Open Folder → 選桌面的 claude-code-workshop-jr-student → 打開右側 AI 助手面板。", note: null },
      { label: "② 把 setup.md 交給它", lang: "text", code: "把 setup.md 拖進 AI 助手的對話框（或輸入 @setup.md 選它），再貼下面這句話。", note: null },
      { label: "這句話（貼進 AI 助手對話框）", lang: "prompt", code: "請依照這份 setup.md 幫我把上課需要的工具準備好。文件裡寫「Cursor」的地方，就是指你。", note: "這份說明書原本寫給另一個 AI 工具；補這句話，是告訴 Antigravity：現在由你來做。" },
      { label: "③ 監工 AI 四個動作", lang: "text", code: "AI 會依序：問你使用哪個帳號 → 檢查電腦缺什麼 → 幫你安裝需要的工具 → 帶你登入。每次看到 Allow，先看清楚它要做什麼，再按允許。", note: null },
      { label: "Codex 使用者看這裡", lang: "bash", code: "如果你是用 ChatGPT Plus，就回答「Codex」。AI 會改裝 OpenAI 的工具，其餘流程一樣：檢查、安裝、登入。", note: null, collapsible: true }
    ],
    checklist: ["AI 已檢查電腦狀態", "Claude Code（或 Codex）已安裝完成", "登入成功、看到歡迎訊息"]
  },
  {
    id: "first-chat",
    num: "04",
    title: "第一次對話",
    badge: null,
    mac_win: "macOS 為主",
    goal: "親手跟 Claude Code 講第一句話，確認它看得到你的教材資料夾。",
    intro: "換 Claude Code 登場。先進到教材資料夾，再打開 Claude Code；這樣它才知道今天要看哪一份教材。",
    analogy: "它不是只靠你貼文字回答，而是真的會看你打開的資料夾。這就是這類 AI 助手跟一般聊天網頁最大的不同。",
    kind: "steps",
    commands: [
      { label: "進到教材資料夾並打開 Claude Code", lang: "bash", code: `cd ~/Desktop/claude-code-workshop-jr-student
claude`, note: null },
      { label: "第一句話（貼進 Claude Code）", lang: "prompt", code: "你好，我現在在哪個資料夾？裡面有什麼東西？", note: null }
    ],
    checklist: ["Claude Code 成功打開", "它能說出教材資料夾裡有哪些東西"]
  },
  {
    id: "status-panel",
    num: "05",
    title: "裝狀態列面板",
    badge: "Claude Code 專屬・選配",
    mac_win: "macOS 為主",
    goal: "（僅 Claude Code）在畫面底部加一條狀態列，讓你看得懂 AI 目前用量。",
    intro: "這一步是 <b>Claude Code 專屬</b>，用 Codex 的同學可以跳過。你只要把下面三行設定，一行一行貼進 Claude Code 的輸入框；不要貼到電腦的一般文字指令視窗。",
    analogy: null,
    kind: "steps",
    commands: [
      { label: "第 1 行 · 加入面板來源", lang: "slash", code: "/plugin marketplace add jarrodwatts/claude-hud", note: null },
      { label: "第 2 行 · 安裝面板", lang: "slash", code: "/plugin install claude-hud", note: null },
      { label: "第 3 行 · 打開面板", lang: "slash", code: "/claude-hud:setup", note: "跑完後，畫面底部會出現狀態列，不用重新打開 Claude Code。" }
    ],
    checklist: ["畫面底部出現狀態列（目前使用的 AI、剩餘記憶空間、用量）"]
  },
  {
    id: "github-push",
    num: "06",
    title: "AI 助手幫你上 GitHub",
    badge: null,
    mac_win: "macOS 為主",
    goal: "註冊 GitHub，讓 Claude Code 幫你把成果放到雲端。",
    intro: "GitHub 可以想成作品的雲端資料夾。你只需要註冊帳號，後面讓 Claude Code 幫你把成果放上去。",
    analogy: "GitHub 像作品集的雲端相簿：放上去之後，你會有一個可以分享的網址。",
    kind: "steps",
    commands: [
      { label: "① 註冊帳號", lang: "text", code: "https://github.com/signup", note: "填 email、設密碼、選一個好記的英文 username（它會出現在你的作品網址裡）。已有帳號就跳過。" },
      { label: "② 交給 Claude Code", lang: "text", code: "回到 Claude Code，說「請依照 github-setup.md 幫我設定 GitHub」。接著它會顯示一組一次性代碼，並打開瀏覽器；你把代碼貼上、按授權，剩下交給 AI。", note: null },
      { label: "③ 驗證", lang: "bash", code: "gh repo view --web", note: "瀏覽器會打開你的 GitHub 雲端資料夾。看到檔案，就代表成果已經放上去了。" }
    ],
    checklist: ["看到登入成功訊息", "GitHub 出現新的雲端資料夾，而且裡面有檔案"]
  }
];
