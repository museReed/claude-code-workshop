# Component-only MCP page builder handoff

## Handoff 類型

- `continuation`：目前完成架構分析，尚未開始 MCP server、PageSpec 或 Renderer 實作。
- Branch：`slides-playwright-mcp`
- Open PR：無。

## 狀態摘要

- `cinematic-video-hero/` 已是 Vite／React／TypeScript／Tailwind／Framer Motion 的互動能力工具庫。
- 工具庫目前有 5 個 preset tabs，包含 Cinematic、Creator、Fashion Archive、AI Image Product、Viktor Oddy Studio。
- 各 preset 已拆成可搜尋、可分類的能力卡，每張包含 Prompt、Script、驗證規則與 mini demo。
- Fashion Archive 已補 procedural masonry／waterfall demo；AI Image Product 已拆成 shell 與 3 個 feature-card components。
- Viktor Oddy Studio 已拆成 10 張 Brand、Motion、Interaction、Navigation 能力卡。
- 已確認 `npm run lint`、`npm run build` 通過，本地 Vite server 可回應 `HTTP 200`。
- 已規劃以 MCP 將這套 component catalog 變成自然語言 page builder。
- 核心原則：模型只產生經 schema 驗證的 PageSpec JSON，不允許直接產生 JSX、CSS、imports 或任意程式碼。
- `cinematic-video-hero/` 目前整個目錄仍是 untracked；不要在未確認 scope 前一次加入所有 repo 修改。

## 核心規劃

### 目標使用流程

1. User 用自然語言描述網站，例如「做一個 studio landing page，要 Hero、瀑布流、Pricing」。
2. Agent 呼叫 `search_components` 找出允許的元件。
3. Agent 呼叫 `get_component_schema` 取得 props、slots、children 與 token 限制。
4. Agent 呼叫 `compose_page` 或 `update_page`，只送出 PageSpec JSON。
5. MCP server 使用 Zod／JSON Schema 驗證；未知 component、額外 props、任意 className／HTML／JS 直接拒絕。
6. `PageRenderer` 將 component ID 映射到可信任 React components，產生 preview。
7. `validate_page` 必須通過後才允許儲存或 export。

### 建議 PageSpec

```ts
type PageSpec = {
  version: 1
  theme: 'cinematic' | 'creator' | 'archive' | 'image-product' | 'studio'
  sections: Array<{
    id: string
    component: ComponentId
    props: Record<string, unknown>
    slots?: Record<string, ComponentInstance[]>
  }>
}
```

PageSpec 禁止接受：

- JSX／HTML 字串
- `className`／任意 Tailwind classes
- 任意 CSS、JavaScript、event handler 或 imports
- 未登記的 component ID
- schema 未聲明的 props／children

### 建議 Component Registry

```ts
const componentRegistry = {
  'studio.hero': {
    component: StudioHero,
    propsSchema: StudioHeroPropsSchema,
    allowedChildren: [],
  },
  'studio.marquee': {
    component: InfiniteMarquee,
    propsSchema: MarqueePropsSchema,
    allowedChildren: [],
  },
  'studio.pricing': {
    component: PricingSection,
    propsSchema: PricingPropsSchema,
    allowedChildren: ['studio.pricing-card'],
  },
} as const
```

### 建議 MCP tools

| Tool | 責任 |
|---|---|
| `search_components` | 按意圖、preset、group 搜尋可用元件 |
| `get_component_schema` | 回傳 props、slots、children、tokens 與範例 |
| `list_design_tokens` | 回傳允許的色彩、字體、spacing、motion tokens |
| `compose_page` | 由合法 component instances 建立 PageSpec |
| `update_page` | 以結構化 operations 修改既有 PageSpec |
| `validate_page` | 驗證 schema、composition、accessibility 與 asset policy |
| `render_preview` | 由固定 PageRenderer 產生預覽，不接受任意程式碼 |
| `export_page` | Optional；只能輸出固定模板，不接受 raw code 注入 |

### 強制限制層級

- `AGENTS.md`、Skill、MCP `instructions` 只負責引導，不能當安全邊界。
- MCP tool schemas 能限制 MCP calls，但若 Agent 同時持有 shell／filesystem／patch tools，仍可能繞過。
- 真正的 hard boundary 是：模型只取得 MCP tools，MCP server 只接受 PageSpec，Renderer 只載入 registry components。
- 若直接在 Codex 使用，需另外用 project config、tool allowlist、sandbox 或 managed hooks 阻擋 raw code／filesystem 寫入；hook 應 fail closed。
- 若做給終端使用者，優先考慮 Apps SDK／Agents SDK app，讓模型執行環境只暴露這組 MCP tools。

### 建議目錄

```text
cinematic-video-hero/
├── src/component-library/
│   ├── registry.ts
│   ├── schemas.ts
│   ├── tokens.ts
│   └── components/
├── src/page-builder/
│   ├── PageRenderer.tsx
│   ├── PageSpec.ts
│   └── validatePageSpec.ts
├── mcp/
│   ├── server.ts
│   └── tools/
├── generated-pages/
│   └── *.json
└── .codex/config.toml
```

## 必讀檔案

- `cinematic-video-hero/src/App.tsx`：目前 5 個 presets、feature registry、Prompt／Script／validations 與所有 mini demos 都集中在這裡；重構來源。
- `cinematic-video-hero/src/index.css`：現有共用視覺 tokens、Liquid Glass、scrollbar 與字體 imports。
- `cinematic-video-hero/package.json`：確認 React、TypeScript、Vite、Tailwind、Framer Motion 與 Lucide 版本；MCP／schema dependencies 尚未加入。
- `docs/handoff/2026-07-14-motion-spec-lab-archive-preset.md`：Fashion Archive 的來源需求與原始 constraints。
- `.codex/config.toml`：若採 Codex local MCP，需要在 trusted project scope 設定 server、required 與 enabled tools；目前需先確認是否存在／是否可修改。

## 下一步

1. 先與 Claude 決定產品 surface：`Codex local MCP`、`ChatGPT Apps SDK`，或獨立 `Agents SDK` page-builder app。
2. 決定 hard-enforcement 邊界：是否完全移除模型的 shell／filesystem tools；若不能，定義 managed hook／sandbox 策略。
3. 從 `App.tsx` 抽出 `ComponentId`、registry、props schemas 與 design tokens；先選 5 個代表性元件做 spike。
4. 建立 `PageSpec` Zod schema，加入 unknown-key rejection、allowed-children、asset allowlist 與 token enums。
5. 建立只讀 tools：`search_components`、`get_component_schema`、`list_design_tokens`。
6. 建立寫入 tools：`compose_page`、`update_page`、`validate_page`，輸出只存到 `generated-pages/*.json`。
7. 建立 `PageRenderer` 與 `render_preview`；加入 invalid component、extra props、nested child、raw HTML／className injection tests。
8. 完成 spike 後再決定是否把 MCP server 包成 Codex plugin 或 ChatGPT plugin／app。
9. 每個階段執行 `cd cinematic-video-hero && npm run lint && npm run build`。

## 待討論決策

- PageSpec 是否只允許 section-level components，還是也允許 nested primitives。
- 文字、圖片 URL 與 links 是否可自由輸入，或必須套 asset／domain allowlist。
- 是否允許 theme tokens 覆寫；如果允許，覆寫範圍要限制到 enum，而非任意 CSS。
- 頁面儲存先用 repo JSON，還是多使用者情境直接用 Supabase。
- Export 是否要輸出 React source；若需要，必須由固定 templates 產生，而不是讓模型自由寫 code。
- Codex 開發模式與終端 user 模式是否需要兩套不同權限設定。

## 已知問題

- `cinematic-video-hero/src/App.tsx` 已非常大型；在 MCP 實作前最好先抽 registry 與 demo components。
- Repo 有大量與本任務無關的既有修改；commit 時只能加入明確檔案。
- `cinematic-video-hero/` 仍是 untracked，後續需先確認是否正式納入 repo。
- `PPMondwest-Regular.woff2` 尚未存在於 `public/`，Viktor Oddy mini demos 使用 `Instrument Serif` fallback。
- 部分 demo 依賴 motionsites.ai、Higgs、CloudFront 等外部 assets，需要 domain allowlist、timeout 與 fallback 策略。
- 原始 Viktor Oddy prompt 混有 Viktor Oddy、Vortex Studio、Halaska Studio、Chris Halaska 等品牌資料，產品化前需統一。
- MCP instructions 與 Prompt 不是 hard security boundary；只要模型仍有 raw filesystem／shell 工具，就不能保證「只用 registry components」。

## 官方參考

- OpenAI Apps SDK：<https://developers.openai.com/apps-sdk>
- Build an MCP server：<https://developers.openai.com/apps-sdk/build/mcp-server>
- Codex MCP：<https://learn.chatgpt.com/docs/extend/mcp.md>
- Codex Hooks：<https://learn.chatgpt.com/docs/hooks.md>
