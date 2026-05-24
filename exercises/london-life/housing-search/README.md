# Scenario: 倫敦找房決策矩陣

**難度** ⭐⭐ · **時間** 20-25 min

## 情境

你下個月要搬到倫敦讀書。SpareRoom / Rightmove / Facebook 群組看了**爆炸多**房源,腦袋已經糊掉:

- 哪間離學校近?走路還是 zone 1 tube?
- 哪間 council tax 包不包?bills 包不包?
- 哪間室友看起來正常、哪間像在描述 horror film?
- 哪間有「**hidden cost**」(deposit 高得不合理、押 6 個月、guarantor 要求英國人)?

你今天要做的:把雜亂的房源清單轉成一張**可以拿給家人解釋為什麼選 X 的決策矩陣**。

## 輸入

- `criteria.md` — 你的條件(預算、通勤、室友偏好、deal-breaker)
- `listings.md` — 8 筆從不同平台複製貼上的房源(格式不一、有些含內心 OS)

## 預期產出

1. `comparison.csv` — 對齊欄位的比較表(月租、地點、zone、通勤時間、bills、deposit、deal-breakers 命中、隱藏成本)
2. `shortlist.md` — 排名前 3 的選擇,每個附:
   - 為什麼推薦
   - 還需要確認的問題(寫信給房東/房仲時要問什麼)
   - 風險點
3. `red_flags.md` — 全部 8 個裡的紅旗清單(deposit 超標、不合法條款、可疑措辭)

## 建議流程

```
Step 1  Claude 讀 criteria.md,複述「它認為的 deal-breaker」(避免它誤判)
Step 2  讀 listings.md,把每筆轉成結構化資料 → comparison.csv
Step 3  ★ 計算通勤時間時:告訴 Claude 你的學校位置(KCL Strand),不要讓它瞎猜
Step 4  比對 criteria,生 shortlist
Step 5  獨立做 red flag 偵測(這是 AI 最有價值的地方:它知道什麼是不合理條款)
```

## 建議 Prompts

**理解條件:**
```
Read criteria.md. Summarise in your own words:
- My absolute non-negotiables (deal-breakers)
- My "would be nice" items
- My budget ceiling
Confirm before doing anything else.
```

**結構化:**
```
Read listings.md. For each of the 8 listings, extract into comparison.csv:
listing_id, monthly_rent_gbp, location, tube_zone, walk_to_kcl_strand_min,
bills_included (Y/N/partial), council_tax_included (Y/N), deposit_weeks,
deal_breakers_hit (list from criteria.md), one-line summary.

For commute time, assume King's College London Strand campus.
Where info is missing, write UNKNOWN — do not guess.
```

**篩選 + 風險:**
```
Based on comparison.csv and criteria.md, produce shortlist.md with the top 3.
For each: 3 reasons to consider, 3 questions to email the landlord/agent,
and 1 risk to watch for.

Then produce red_flags.md scanning ALL 8 listings for:
- Deposits exceeding 5 weeks rent (illegal under Tenant Fees Act 2019)
- "No DSS / no students / no foreigners" or similar discriminatory wording
- Guarantor requirements that effectively exclude international students
- Suspiciously low rent for the area
- Vague or evasive descriptions of the property
- Pressure tactics ("must decide today", "lots of interest")
```

## Academic Integrity

不適用——這不是學術任務。但有兩個重要注意:

1. **AI 對 UK 租屋法律的知識**可能過時或錯誤,red flag 清單要當作**提醒**,不是法律意見。實際要去 [Shelter](https://england.shelter.org.uk/) 或 KCL Student Advice 查證。
2. **不要把房東/房仲的真實 email 丟給 AI**——這是別人的個資。範例素材已經改寫過。

## 進階(時間夠的話)

讓 Claude 幫你寫一封**英文 inquiry email** 給你的 top 1 房源,語氣要 polite-but-firm,並列出你要問的 3-5 個問題。
