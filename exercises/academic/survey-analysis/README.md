# Scenario: 問卷數據快速分析

**難度** ⭐⭐⭐ · **時間** 25-30 min

## 情境

你做了一份小型問卷(100 份回應),要在三天內交出 preliminary findings。你**不會寫 Python**,但你會描述你想要的分析。讓 Claude Code 幫你寫腳本、跑統計、畫圖,然後**你**負責判斷哪些 finding 值得寫進論文。

## 輸入

- `survey.csv` — 100 列合成資料,主題「postgraduate 學生對 AI 工具的使用態度與行為」。

### 欄位說明

| 欄位 | 型別 | 說明 |
|------|------|------|
| `respondent_id` | int | 流水號 |
| `program` | str | 學程(Tech Mgmt / Business / Engineering / Other) |
| `year_of_study` | int | 1 或 2(碩士第幾年) |
| `age_bracket` | str | 22-25 / 26-30 / 31-35 / 36+ |
| `freq_use_ai` | int | 1-5 Likert(1=從不,5=每天) |
| `trust_ai_output` | int | 1-5 Likert |
| `concern_integrity` | int | 1-5 Likert(對學術誠信的擔憂) |
| `tools_used` | str | 多選,用 `;` 分隔(ChatGPT;Claude;Gemini;Copilot;None) |
| `monthly_spend_gbp` | float | 每月花在 AI 訂閱的金額 |
| `open_response` | str | 開放問題:「你在使用 AI 工具時最大的困擾?」 |

## 預期產出

1. `analysis.py` — Claude Code 生成的分析腳本(可重跑)
2. `charts/` — 至少 3 張圖(分布、交叉、開放問題詞頻)
3. `findings_draft.md` — 300-500 字 preliminary findings 草稿

## 建議流程

```
Step 1  讓 Claude 讀進 survey.csv,先回報「資料長什麼樣」(避免它瞎猜)
Step 2  請它跑敘述性統計與缺失值檢查
Step 3  指定要看的交叉(例如:program × freq_use_ai)
Step 4  ★ 開放問題用 LLM 自己做主題抽取(這就是 AI 比傳統工具強的地方)
Step 5  自己審查 findings,標出哪些可信、哪些需要補資料
```

## 建議 Prompts

**先了解資料:**
```
Read survey.csv. Report: number of rows, columns and types, any missing values,
and a quick summary stat for each numeric column. Do NOT do analysis yet.
```

**敘述性 + 交叉:**
```
Write analysis.py that:
1. Outputs descriptive stats for all Likert columns by program
2. Creates a chart showing freq_use_ai distribution by year_of_study
3. Creates a heatmap of correlations between the three Likert columns
Save all charts to charts/. Use only pandas + matplotlib, no extra deps.
```

**開放問題主題抽取:**
```
Read the open_response column. Identify 4-6 recurring themes.
For each theme: name it, give the % of responses it appears in,
and quote 2 representative responses. Save to findings_draft.md.
```

## Academic Integrity

| 可以 ✅ | 不可以 ❌ |
|---------|-----------|
| 用 AI 寫分析腳本 | 把 AI 的 findings 草稿一字不改交出 |
| 用 LLM 做主題抽取(再人工驗證) | 用 AI 編造不存在的受訪者引述 |
| 用 AI 解釋它跑出來的統計 | 用 AI 「補」你資料裡沒問到的問題答案 |

**驗證步驟:** 開放問題的主題抽取,**人工抽 10 筆**對比 AI 的歸類是否合理。
