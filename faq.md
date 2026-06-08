# 課後 FAQ — Claude Code Workshop

> 整理自課堂上同學問過的問題。給上完課想再確認、或當天沒問到的人。

---

### Q1. 我不是工程師（PM / Data Scientist / 學生），需要用 GitHub 嗎？
需要、而且很值得。GitHub 是你成果的**雲端備份 + 版本歷史 + 分享連結**。連上 Claude Code 後，你可以用**自然語言**叫它幫你把檔案推上去、或從 GitHub 把東西抓下來，不必自己上網站點來點去。設定見 [`github-setup.md`](./github-setup.md)。

### Q2. 各家 LLM（Claude / GPT / Gemini / DeepSeek…）差在哪？只有 context window 不同嗎？
不只。它們在**推理能力、訓練資料、強項、速度、價格**上都有差別，context window（一次能記多少）只是其中一個維度。實務上的選法：難任務用最強的（Opus 級），日常用均衡的（Sonnet 級），大量簡單任務用最便宜的（Haiku 級）。

### Q3. CLAUDE.md 和 MEMORY.md 差在哪？
**兩個都是 Claude Code 官方原生功能，差別只在「誰寫」：**
- **CLAUDE.md**＝**你**寫的指令／規則（專案脈絡、規範、紅線）。
- **MEMORY.md（Auto memory）**＝**Claude 自己**根據你的更正與偏好寫的筆記（build 指令、除錯心得、你的習慣）。需 Claude Code `v2.1.59+`，存在 `~/.claude/projects/<project>/memory/`，每個 repo 一份、machine-local。

兩者**每個 session 開頭都會載入**。衝突時官方**沒有硬性優先級**（都只是 context，不是強制設定）；實務上 CLAUDE.md（你明確下的規則）應勝過 MEMORY.md（Claude 的筆記），要**強制**就用 hook。初學先會用 CLAUDE.md 就夠。

> 真正的第三方是 `claude-mem`（有自己的站 docs.claude-mem.ai），跟官方 Auto memory 無關。

### Q3b. 不同層級的 CLAUDE.md 衝突呢？（user vs project）
這個跟 Q3 不同——CLAUDE.md **各層級之間「有」明確優先順序**。載入由廣到細：**managed（企業/組織，不可被排除）→ user（`~/.claude/CLAUDE.md`）→ project（`./CLAUDE.md`）→ local**；愈靠近你工作目錄、愈晚載入的，優先級愈高。官方原話：「user-level rules 比 project rules 先載入，所以 **project 優先級較高**」。簡記：**企業 > 專案 > 個人**（企業層永遠套用）。

### Q4. 不同 session（對話）之間怎麼共享進度？
**不是靠某個檔案自動同步。** 常見做法是：在舊 session 叫 Claude「把目前進度寫成一份交接檔（handoff）」，新 session 再讀那份檔；或把重點寫進 CLAUDE.md。

### Q5. `/compact` 是什麼？有什麼代價？
當對話太長（context 用很多）時，`/compact` 會把對話**壓縮成摘要**，釋放空間。代價是**去脈絡化**——中間細節可能遺失。建議 context 到 ~70% 時做，或改用「寫交接檔 + 開新 session」。

### Q6. MCP 是什麼？是各工具自己做、還是 Claude Code 做？
MCP（Model Context Protocol）是 Anthropic 提出的**協定/標準**（像 AI 版的 USB-C），規定 AI 要怎麼接外部工具/資料。**各家（GitHub、Figma…）依這個標準做自己的 MCP server**。所以是「各工具自己做、大家遵守同一套規格」。

### Q7. 如果某個工具還沒有 MCP，就沒辦法用了嗎？
不會。Claude Code 還能用 **Playwright** 這類工具**直接開網頁、模擬點選**來操作沒有 MCP 的服務（只是比較慢、比較陽春）。

### Q8. 用中文還是英文跟 AI 溝通比較好？中文會比較耗 token 嗎？
中文 token 確實**略多**，但差距很小、不影響成本到要在意的程度。**重點是「你用哪種語言更能把問題講清楚」**——清楚表達 > 省 token。用中文完全 OK（連 skill 都可以用中文寫）。

### Q9. Skill 該做多大才合適？
Skill 是**高層的工作流程 SOP**（把步驟、規範、範例打包，可附腳本），不是單一小函式。判準：**會重複用、有固定步驟**的流程適合做成 skill；如果是一整個獨立系統，那就做成 project。不確定時，直接問 Claude「這個適合做成 skill 還是 project？」

### Q10. 中途換模型，會把前面的對話清掉嗎？
**不會**，對話內容還在。只是會讓**快取（cache）失效**，導致下一輪稍微變貴、變慢。真的要換模型，建議**開一個新 session** 比較乾淨。

### Q11. Cursor 登入時看到「Pro / $20」是不是會被收費？
那是付費方案。**今天用免費就夠，不要點 Pro / Upgrade。** 不小心點到（要你刷卡）就退回上一頁重選免費。

### Q12. 我裝環境一直卡關怎麼辦？
先看 [`onboarding.md`](./onboarding.md) 的操作小抄（90% 卡關是：視窗切換、複製帶到空格、Claude Code 只能用鍵盤、`@` 引用）。再不行，**直接用白話問 Claude 本人**，或記下卡在哪一步問講師。
