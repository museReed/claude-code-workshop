# Workshop Exercises

KCL Claude Code Workshop · Part 5（50 min）分組實作素材。

每組 3-4 人,從以下情境中**選一個**進行。每個場景都可以在 15-30 分鐘內走完一次完整的 prompt → 產出 → 檢視循環。

---

## 場景對照表

| 領域 | 子場景 | 難度 | 時間 | 核心技能 |
|------|--------|------|------|----------|
| **學術** | [academic/lit-review](./academic/lit-review/) | ⭐⭐⭐ | 20-25 min | 跨檔案抽取與比較 |
| **學術** | [academic/survey-analysis](./academic/survey-analysis/) | ⭐⭐⭐ | 25-30 min | 讓 AI 寫腳本處理結構化資料 |
| **學術** | [academic/references](./academic/references/) | ⭐⭐ | 15-20 min | 格式轉換與一致性檢查 |
| **學術** | [academic/dissertation](./academic/dissertation/) | ⭐⭐ | 20-25 min | 文件骨架生成與組織 |
| **協作** | [collaboration/meeting-tracker](./collaboration/meeting-tracker/) | ⭐ | 15-20 min | 從凌亂筆記抽出結構 |
| **生活** | [london-life/housing-search](./london-life/housing-search/) | ⭐⭐ | 20-25 min | 把雜訊資訊轉成決策矩陣 |
| **職涯** | [career/resume-tailoring](./career/resume-tailoring/) | ⭐⭐ | 20-25 min | 對標需求重寫文件 |

---

## 怎麼選

- **不確定怎麼用 AI?** → 從 `meeting-tracker` 或 `references` 開始,門檻最低。
- **對學術寫作最有感?** → `lit-review` 或 `dissertation`。
- **想看 AI 怎麼寫程式?** → `survey-analysis`(會生 Python 腳本)。
- **生活/職涯有實際需求?** → `housing-search` 或 `resume-tailoring`。

## 共通規則

1. **每組選一個場景,不要貪多。** 目標是走完一次完整循環,不是做完所有事。
2. **每個 prompt 都要寫下來。** 場景 README 內有建議 prompt,但鼓勵改寫成自己版本。
3. **Demo 時間 1 分鐘 / 組:** 展示你下了什麼 prompt、AI 回了什麼、你怎麼判斷要不要採納。
4. **Academic Integrity:** 每個學術場景都附說明,清楚標示「AI 可以幫到哪、哪些必須是你自己的」。

## 講師備註

- 所有素材皆為**合成範例**,不含真實學生或公司資料。
- Lit Review 的 `samples/` 用 `.md` 模擬論文摘要,讓場景立即可跑;正式教學前可換成真實 PDF。
- 場景設計刻意保留缺陷(凌亂格式、空白欄、模糊用詞),讓學員體會 AI 在「清理雜訊」這件事上的價值。
