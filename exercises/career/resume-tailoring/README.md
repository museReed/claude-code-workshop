# Scenario: 履歷對標職缺 (Resume Tailoring)

**難度** ⭐⭐ · **時間** 20-25 min

## 情境

你看到一份**很想申請的 job description**,但你的 CV 是**通用版**——三年前寫的、塞滿大學社團、行文像高中老師寫的推薦信。

你不要讓 AI 「重寫一份漂亮履歷」(這會變成所有人都長一樣)。你要讓 AI 做**三件事**:

1. **解構 JD** —— 把職缺需求翻成清單(必要 / 加分 / 隱含)
2. **盤點你的 CV** —— 對標清單,找出 ✅ 你有但沒寫好、⚠️ 你有但藏起來、❌ 你真的沒有
3. **改寫 bullet points** —— 針對命中的項目,把弱動詞、空泛描述、無量化的句子改強

最後 **你** 決定要採納哪些改寫,不要把 AI 草稿一字不改丟出去。

## 輸入

- `cv_draft.md` — 你目前的凌亂 CV(動詞弱、缺數字、有矛盾、太冗長)
- `job_description.md` — 目標職缺(Product Manager — Graduate Programme,某 fintech)

## 預期產出

1. `jd_breakdown.md` — JD 解構,分成三層需求清單
2. `gap_analysis.md` — 對標 cv_draft,標出 ✅/⚠️/❌
3. `cv_tailored.md` — 重寫後的 CV(只改命中項目的 bullet,不亂塞東西)
4. `cover_letter_draft.md`(選做) — 400 字 cover letter 草稿

## 建議流程

```
Step 1  Claude 讀 JD,先複述「這份工作真正在找的是什麼樣的人」
Step 2  獨立讀 cv_draft,做 gap analysis(此時還不要改 CV)
Step 3  ★ 你看 gap analysis,刪掉你不認同的判斷(AI 會誤判)
Step 4  Claude 根據確認過的 gap,改寫 bullet points
Step 5  你逐句檢查:這句話是真的嗎?還是 AI 幫我吹牛?
```

## 建議 Prompts

**JD 解構:**
```
Read job_description.md. Break it into three lists:
1. Required (explicit must-haves)
2. Preferred (nice-to-haves)
3. Implicit (signals beneath the surface — what the JD really wants)
Save to jd_breakdown.md.
```

**Gap 分析:**
```
Read cv_draft.md and jd_breakdown.md. For each item from jd_breakdown,
mark one of:
✅ Have it AND it's already well-presented on the CV
⚠️ Have it but it's hidden / under-sold / not quantified
❌ Don't have it (be honest — don't invent)
Save to gap_analysis.md as a table. One row per JD item.
```

**Bullet 改寫:**
```
For every ⚠️ in gap_analysis.md, rewrite the relevant bullet on cv_draft.md
to make the strength visible. Rules:
- Use strong verbs (led, shipped, reduced, grew — not "responsible for", "helped with")
- Quantify wherever possible — even rough numbers (~50 users, ~10% improvement)
- DO NOT invent numbers I didn't provide
- If a bullet can't be improved truthfully, leave it and flag with [needs data]
Save full tailored CV to cv_tailored.md.
```

**Cover letter(選做):**
```
Write a 400-word cover letter draft based on cv_tailored.md and job_description.md.
Structure: hook (why this company specifically), match (3 strongest fits), close
(what I want next). Tone: confident, not desperate. Plain English, no buzzwords.
```

## Academic Integrity / Career Integrity

| 可以 ✅ | 不可以 ❌ |
|---------|-----------|
| 用 AI 解構 JD、找盲點 | 用 AI **編造** 你沒做過的經驗 |
| 用 AI 改寫弱動詞、加結構 | 用 AI 加你查無實證的量化數字 |
| 用 AI 起草 cover letter | 用 AI 整篇生成、自己一字不改交出 |

**核心原則:** AI 改寫後的每一句,**你要能在面試裡用自己的話展開講 2 分鐘**。如果展不開,那句話就不該留。

## 進階(時間夠的話)

- 拿 `cv_tailored.md` 給 AI 模擬面試官:「Based on this CV, what are the 5 toughest questions you'd ask in interview?」
- 自己練習回答,再回頭看 CV 哪裡需要再修。
