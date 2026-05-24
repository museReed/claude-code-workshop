# Scenario: Group Project 會議追蹤

**難度** ⭐ · **時間** 15-20 min

## 情境

你是 group project 的事實上的「co-ordinator」(不一定願意,但事情會自動找上你)。每週開會大家七嘴八舌,你用 Google Docs 記了**生肉版** notes,但:

- 三週後沒人記得「誰要做什麼」
- Action items 散落在會議記錄各處
- 隊友會說「上週我們不是決定要…?」然後找不到證據

讓 Claude Code 幫你把生肉變成**可追蹤的結構**。

## 輸入

- `raw_notes.txt` — 三週的會議生肉,有時序、有口語、有錯字、有離題對話。

## 預期產出

1. `meetings/week1.md`、`week2.md`、`week3.md` — 每週一個結構化檔案,包含:
   - 出席
   - 決議
   - Action items(誰、做什麼、什麼時候 due)
2. `tracker.md` — 總覽追蹤表,合併三週所有 action items,標記:
   - ⏳ 進行中
   - ✅ 已完成(從後續會議推斷)
   - ⚠️ 卡住或無下文

## 建議流程

```
Step 1  Claude 先複述「它從 raw_notes 看到幾次會議、誰常出現」(確認沒漏)
Step 2  生成 weekN.md 三個檔案
Step 3  獨立做 tracker.md,從跨週脈絡推斷狀態
Step 4  ★ 你比對:有沒有重要決議被當成閒聊忽略?
```

## 建議 Prompts

**理解階段:**
```
Read raw_notes.txt. Report:
- How many meetings you can identify
- Who appears as regular attendees
- Anything that looks like notes from outside the meetings (chat, off-topic)
Do not extract anything yet — just confirm what you see.
```

**結構化階段:**
```
Split raw_notes.txt into one .md file per week, saved under meetings/.
Each file must include:
- # Week N Meeting — [date if you can infer]
- ## Attendees
- ## Decisions (numbered)
- ## Action items (table: Owner | Task | Due | Status)
- ## Parked / unresolved
Use exact wording where the original notes are clear; paraphrase where they're chaotic but flag with [paraphrased].
```

**追蹤階段:**
```
Generate tracker.md combining all action items across week1-3.
For each item, infer current status from later meetings:
- ✅ Completed (mentioned as done in later week)
- ⏳ In progress (referenced but not closed)
- ⚠️ Stalled (mentioned once and never again)
Sort by owner. Add a one-line note for ⚠️ items suggesting what to ask about next meeting.
```

## Academic Integrity

這個場景**完全 OK**——它就是個 productivity tool,等同於用 Notion 或 Otter.ai 整理會議。

你沒有用 AI 寫任何學術內容,只是讓它幫你整理你**自己手寫的** 筆記。
