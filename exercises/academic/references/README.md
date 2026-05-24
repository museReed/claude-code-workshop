# Scenario: Reference 管理與格式轉換

**難度** ⭐⭐ · **時間** 15-20 min

## 情境

你的 dissertation 已經寫了 5,000 字,引用列表卻是**地獄**——有 APA、有 Harvard、有從網頁複製的純 URL、有從 EndNote 出來的格式錯誤、還有兩筆**疑似重複**。

Supervisor 下週要看,你不想花一整天用 Word 一條條改。

## 輸入

- `refs_messy.txt` — 18 筆混合格式的引用清單,包含:
  - 至少 4 種不同的引用格式
  - 1-2 筆重複(但寫法不同)
  - 1 筆缺欄位(例如沒有年份)
  - 1-2 筆只有純 URL

## 預期產出

1. `references_harvard.md` — 統一為 KCL Harvard 格式的清單(依字母排序)
2. `citation_audit.md` — 審查報告,包含:
   - 找到的重複(舊筆 → 新筆對照)
   - 缺欄位的引用(哪幾筆,缺什麼)
   - 純 URL 補完成完整引用的清單(誰寫的、什麼時候)

## 建議流程

```
Step 1  Claude 先把每筆現有格式辨識出來,列在表上(讓你檢查)
Step 2  統一轉換成 Harvard,排序
Step 3  獨立做 audit:重複、缺漏、補完
Step 4  ★ 自己抽查 3 筆原始 vs Harvard,確認轉換正確
```

## 建議 Prompts

**識別階段:**
```
Read refs_messy.txt. For each entry, report:
- Index (1-based)
- Detected format (APA / Harvard / Chicago / URL only / unclear)
- One short note if anything looks wrong or missing
Output as a markdown table. Do NOT convert yet — I want to verify first.
```

**轉換階段:**
```
Convert all entries to KCL Harvard style (Author, Year. Title. Journal, vol(issue), pp.).
For URL-only entries, fetch metadata if you can; if not, flag them.
Sort alphabetically by first author surname.
Save as references_harvard.md.
```

**Audit 階段:**
```
Re-read refs_messy.txt and produce citation_audit.md with three sections:
1. Duplicates — list pairs of entries that refer to the same work
2. Missing fields — list entries that lack year, journal, or DOI
3. URL-only — list entries that are just a URL, and what you found when resolving them
```

## Academic Integrity

| 可以 ✅ | 不可以 ❌ |
|---------|-----------|
| 用 AI 統一格式 | 用 AI **編造** 你沒讀過的論文的 metadata |
| 用 AI 偵測重複與缺欄 | 把 AI 標的「URL 解析結果」未驗證就放進論文 |
| 把這當成 Zotero 替代品 | 引用你只看過 abstract 的 paper 卻假裝讀過全文 |

**驗證步驟:** AI 補的 URL metadata(作者、年份、期刊)**必須上原始網頁核對**——這是 hallucination 的高風險區。
