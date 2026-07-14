# Handoff — Design Token 主題化架構討論(參考 shadcn/ui)

Type: investigation / discussion
Date: 2026-07-14
Branch: slides-playwright-mcp

## 狀態摘要

一場架構討論,沒有動任何程式碼。用戶想搞清楚:**如何讓一批已定義好的特效 / UI 元件,靠切換 design token 來替換文字大小、顏色、字體、圖案/背景色階。**

結論:
- 用戶要的不是「純 token 轉換器」(Style Dictionary),而是「token + 元件的完整方案」。
- 標準工程解法 = **token 合約 + CSS 變數注入層**:元件只讀 `var(--x)` 語意名,從不寫死 hex;換主題 = 換根節點一組變數值(`data-theme` / `.dark`)。
- 這正是用戶自己在 `cinematic-video-hero`(branch `spike/design-tokens`)已經做了大半的架構:`THEME_TOKENS` + `claude2code.design-tokens.json` + resolver + PageRenderer inline 注入。
- 研究了 shadcn/ui 的做法作為參考標竿:三層鏈 `:root 變數` → `@theme inline` 短名映射 → 元件用 `bg-primary` class。

## shadcn/ui 三層鏈(參考重點)

```
① :root { --primary: oklch(...) } / .dark 覆蓋同名變數   ← token 值收一處
② @theme inline { --color-primary: var(--primary) }      ← Tailwind 短名映射
③ <button className="bg-primary text-primary-foreground"> ← 元件只用語意名
```

兩個值得抄的設計決策:
1. **成對命名**:`--primary` 一定配 `--primary-foreground`(底色+其上字色),保證對比度。
2. **語意名而非色名**:叫 `--primary`/`--card`/`--muted`,不叫 `--blue-500`;暗色只是重新指向。

用戶結論:**不需要引入 Tailwind `@theme` 那層**,直接寫 `var(--x)` 已達同效,只是 class 名長一點。

## 用戶現況 vs shadcn 對照

| 環節 | shadcn | 用戶現況(cinematic-video-hero) |
|---|---|---|
| Token 值放一處 | `globals.css` `:root` | ✅ `THEME_TOKENS` / `claude2code.design-tokens.json` |
| 元件讀語意名 | Tailwind `bg-primary` | ⚠️ 部分讀 `var()`,還有 3 個 hex 寫死在 `Pricing.tsx` |
| 換主題機制 | 切 `.dark`/`data-theme` | ✅ PageRenderer 換 `data-theme` 注入 |
| 短名映射層 | `@theme inline` | ❌ 沒有,也不打算加 |

## 未解 / 待深入的問題

1. **「特效」(漸層/陰影/動畫)如何 token 化** — shadcn 只示範顏色,這塊比純顏色麻煩,尚未討論。
2. **圖案 / 背景圖替換** — CSS 變數可塞 `url()`,但若要換 `<img>` 的 src,需走 token → renderer → src(用戶 renderer 已在做,待確認)。
3. **命名重構** — 是否把 `THEME_TOKENS` 改成 shadcn 式「語意名 + `-foreground` 成對」。
4. **W3C DTCG 格式對齊** — 是否把 token JSON 改成標準格式,之後能吃 Style Dictionary / Figma 同步。
5. **落地清理** — `Pricing.tsx` 剩的 3 個寫死 hex 要換成 `var()`,否則那幾處換主題不會變。

## 必讀檔案 / 資源

- `docs/handoff/2026-07-14-component-only-mcp-page-builder.md` — 用戶 component-only MCP page builder 的架構背景,本討論的上游脈絡。
- `cinematic-video-hero/` repo(branch `spike/design-tokens`) — 用戶實際在做的 token 系統:`THEME_TOKENS`(tokens.ts)、`claude2code.design-tokens.json`(兩層 primitive→semantic)、resolver、PageRenderer。**要接續實作前先看這裡。**
- shadcn 官方 Theming 文件 https://ui.shadcn.com/docs/theming — 整頁就在講上面那三層鏈。
- 最快驗證:`npx shadcn@latest init` 開空專案,看它生成的 `globals.css`(`:root` 20 幾行變數 + `.dark` 覆蓋)。

## 下一步(接手時可直接做的)

這是討論,沒有進行中的實作。接手時視用戶意圖選一條:

- 若用戶要**繼續討論** → 從上面「未解問題」挑一項展開(特效 token 化 / 圖案替換 / 命名重構)。
- 若用戶要**動手實作** → 進 `cinematic-video-hero` branch `spike/design-tokens`,先清 `Pricing.tsx` 3 個寫死 hex,再依 shadcn「語意名 + `-foreground` 成對」規矩檢查 `THEME_TOKENS` 命名。
