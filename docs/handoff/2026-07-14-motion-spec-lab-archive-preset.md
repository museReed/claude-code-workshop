# Motion Spec Lab — Fashion Archive preset handoff

## 狀態摘要

- 在 `cinematic-video-hero/` 建立 Vite／React／Tailwind／Framer Motion 的互動能力工具庫。
- 已完成 Cinematic Hero 與 Creator Portfolio 兩套 preset，卡片可播放效果並查看 Prompt、Script、驗證規則。
- 已加入 Depth Role Carousel、Microsoft Fluent 3D PNG 素材及 Mouse-Scrub Gaze 卡片。
- Mouse-Scrub Gaze detail 已包含素材製作流程與 Runway、Higgsfield、Veo、MetaHuman 連結。
- 目前正在新增第三套 `Fashion Archive` preset；已加入 `archive` 型別、雙影片 URL 與 8 個 preview kind，但卡片資料與 demo 尚未完成。
- 專案最後一次完整驗證是在 Archive preset 開始前，當時 `npm run lint && npm run build` 通過。
- 本地 Vite server 先前運行於 `http://127.0.0.1:5173/`，接手時需確認是否仍在運行。
- Repo 另有大量與本任務無關的既有修改，請只操作 `cinematic-video-hero/` 與本 handoff。

## 必讀檔案

- `cinematic-video-hero/src/App.tsx`：功能資料模型、所有卡片 Prompt／Script、可播放 demo 與 inspector UI 都集中於此；Archive preset 正在此檔案中途實作。
- `cinematic-video-hero/src/index.css`：Liquid Glass、Gradient Display 與工具庫 scrollbar 等共用樣式。
- `cinematic-video-hero/package.json`：目前依賴 React 18、Tailwind 3、Framer Motion 12、Lucide；Archive demo 可先沿用 Motion，不必立即加入 GSAP。
- `docs/handoff/2026-07-14-motion-spec-lab-archive-preset.md`：本次未完成工作的範圍與接手步驟。

## 下一步

1. 在 `features` 陣列加入 `preset: 'archive'` 的 8 張卡：`Dual Video Scrub`、`Dead Zone Switcher`、`Scroll Phase Director`、`Procedural Archive Grid`、`Viewport Scale Cards`、`Exclusion UI`、`Custom Cursor`、`Scroll Outro`。
2. 為每張卡補齊 `prompt`、`script`、`validations`，並將已分析出的衝突寫進強約束：單一 transform owner、seek queue、resize 重算、footer z-index、touch/reduced-motion fallback。
3. 新增 8 個可播放 mini demo；`Dual Video Scrub` 使用 `ARCHIVE_VIDEOS`，其餘可用 Framer Motion 模擬，避免在工具庫本身引入 GSAP。
4. 更新 preset tab 陣列與 `presetMeta`，加入 `Fashion Archive` 及 `Archive` icon。
5. 執行 `cd cinematic-video-hero && npm run lint && npm run build`，修正型別與 hooks 問題。
6. 確認 `http://127.0.0.1:5173/` 可存取；若 server 不在，執行 `npm run dev -- --host 127.0.0.1`。

## 已知問題

- `App.tsx` 已把 `PresetId` 擴充為 `archive`，但 UI tab 尚只列出 cinematic／creator，Archive preset 暫時不可見。
- `PreviewKind` 已加入 8 個 Archive kind，但 `EffectPreview` 尚無對應 render 分支。
- 來源 Prompt 同時要求 GSAP 與 RAF 控制黑色 panel transform；能力卡必須明確規定只能有一個 transform owner。
- 來源 Prompt 的 dead-zone 文案與行為互相矛盾；建議卡片採「中央保持最後 active side、回到起始幀」並把策略做成可設定項。
