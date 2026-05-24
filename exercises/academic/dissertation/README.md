# Scenario: Dissertation 結構化寫作助手

**難度** ⭐⭐ · **時間** 20-25 min

## 情境

你已經跟 supervisor 確認過 dissertation 的大方向,寫了一份 `outline.md`(章節 + bullet points)。但接下來:

- 不知道每章該寫多少字
- 不知道哪些章節彼此的論證會打架
- 不知道空了一段的「Methodology」要怎麼開始寫

你**不要**讓 AI 直接寫論文。你要讓 AI 把 outline **變成可操作的資料夾結構** + **supervisor 視角的回饋**,讓你寫得起來。

## 輸入

- `outline.md` — 一份大致完成、但細節空泛的 dissertation 大綱。

## 預期產出

1. 一個 `dissertation/` 資料夾結構,每章一個 `.md`,每個檔案內含:
   - 章節核心問題
   - 字數目標
   - 建議引用來源(從你既有的 reading list)
   - 與前/後章節的連接點
2. `review_feedback.md` — Supervisor 角度的回饋,標出:
   - 哪些章節主張可能彼此衝突
   - 哪些章節缺乏 empirical 支撐
   - 建議的研究問題收斂方向

## 建議流程

```
Step 1  Claude 讀 outline.md,先「複述」它理解的核心 RQ(避免它搞錯方向)
Step 2  生成資料夾結構,你看完滿不滿意再改
Step 3  獨立做 review,角色設定為 critical supervisor
Step 4  ★ 不要直接用 review 的話,當成 prompt 跟自己對話
```

## 建議 Prompts

**理解階段:**
```
Read outline.md. In your own words, state:
1. What you think the research question is
2. What you think the main argument is
3. What you think the contribution is
Do not propose changes yet — I just want to see if you understood it correctly.
```

**結構生成:**
```
Based on outline.md, create a folder structure: one .md file per chapter under
dissertation/. Each file must contain (template):
- # Chapter X: [Title]
- ## Core question
- ## Target word count
- ## Suggested sources (from outline.md reading list)
- ## Connection to previous chapter
- ## Connection to next chapter
- ## Open questions / unresolved
```

**Review 階段:**
```
Adopt the role of a sceptical supervisor at KCL. Review outline.md and produce
review_feedback.md with:
- 3 internal contradictions (where chapter X's claim conflicts with chapter Y's)
- 3 weak spots needing empirical evidence
- 1 suggested narrowing of the research question, with reasoning
Be critical but constructive. Do NOT rewrite the dissertation.
```

## Academic Integrity

| 可以 ✅ | 不可以 ❌ |
|---------|-----------|
| 用 AI 把 outline 轉成結構 | 用 AI **寫** 任何一章的 argument |
| 用 AI 模擬 supervisor 給 critical feedback | 把 review_feedback 當成自己的反思 |
| 用 AI 整理你既有的閱讀資源 | 用 AI 編造你沒讀過的文獻當作 source |

**驗證步驟:** AI 提出的「contradictions」要回到 outline 自己對照,確認**它沒有過度詮釋**你的話。
