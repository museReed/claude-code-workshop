# Scenario: Literature Review 加速器

**難度** ⭐⭐⭐ · **時間** 20-25 min

## 情境

你正在寫一份 literature review,手邊有 3-5 篇 paper,但**沒時間一篇一篇細讀**。你想快速建立一張比較矩陣,看哪些研究在什麼問題上有共識、哪些有分歧、有沒有 research gap 可以切入。

## 輸入

- `samples/` 內 3 篇模擬論文摘要(`.md`)。
- 正式 workshop 時可替換為 PDF;Claude Code 能直接讀 PDF 文字。

## 預期產出

1. `literature_matrix.csv` — 比較矩陣:每篇一列,欄位包含 **Author / Year / Research Question / Method / Sample Size / Key Finding / Limitation**。
2. `gap_analysis.md` — 300-500 字的 gap 分析,列出 3 個可能的 research gap。

## 建議流程

```
Step 1  讀進所有 sample,確認 AI 抓到的是正確內容
Step 2  生成 literature_matrix.csv
Step 3  根據矩陣,生成 gap_analysis.md(草稿)
Step 4  ★ 你自己判斷:gap 是否合理?有沒有 AI 編造?
```

## 建議 Prompts

**抽取階段:**
```
Read all .md files in samples/. For each paper, extract:
author, year, research question, method, sample size, key finding,
and one stated limitation. Output as a markdown table first so I can verify,
then save as literature_matrix.csv.
```

**Gap 分析階段:**
```
Based on literature_matrix.csv, identify 3 research gaps. For each gap:
- State the gap in one sentence
- Cite which papers (by author/year) failed to address it
- Suggest a research question that would close the gap
Save to gap_analysis.md. Do NOT invent findings not in the matrix.
```

## Academic Integrity

| 可以 ✅ | 不可以 ❌ |
|---------|-----------|
| 用 AI 整理、抽取論文資訊 | 把 AI 寫的 gap analysis 一字不改放進 dissertation |
| 用矩陣加速你自己的閱讀 | 用 AI 來「假裝讀過」其實沒讀的論文 |
| 讓 AI 列出潛在的論點供你選擇 | 引用 AI 編造的不存在文獻 |

**驗證步驟:** 矩陣產出後,**逐欄抽查 1-2 篇**,確認 AI 沒有編造數據或誤讀。
