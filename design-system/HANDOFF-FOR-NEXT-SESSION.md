# Handoff — 使用 claude2code Design System 的前置作業

> 給新的 Codex / Claude session：如果你要在本 repo 或新專案中使用這套 UI，請先讀完本文件，再開始改頁面。核心原則是：**先用 design-system 既有 token 與 `ds-*` 元件；只有既有語意無法滿足時，才新增自製元件，而且自製元件也必須只用 token。**

---

## 1. 你要先知道的檔案

```text
design-system/
├─ assets/css/design-system.css          # 唯一權威：design token + gallery ds-* 元件
├─ assets/css/design-system.json         # token 結構化參考
├─ docs/gallery.html                     # 元件長相與結構範例
├─ docs/UI-COMPONENT-CONTRACT.md         # 元件使用契約 / 禁止事項
├─ scripts/audit-ui-contract.py          # 自動稽核腳本
└─ templates/static-site/                # 可複製的新專案模板
```

如果是在現有教學網站中開發，主要看：

```text
setup-tutorial/
├─ index.html
├─ assets/css/design-system.css          # 目前與 design-system 主檔一致
├─ assets/css/app.css                    # 只放頁面 layout / wrapper / 必要自製元件
├─ assets/js/app.js
└─ assets/js/steps.js
```

---

## 2. 開始任何 UI 工作前，必做順序

1. 先讀 `design-system/docs/UI-COMPONENT-CONTRACT.md`。
2. 打開或搜尋 `design-system/docs/gallery.html`，確認 gallery 已有什麼 `ds-*` 元件。
3. 需要新頁面時，優先從 `design-system/templates/static-site/` 複製 starter。
4. 寫 UI 時，先用 `design-system/assets/css/design-system.css` 的 token 與元件，不要自己發明顏色、字體、字級。
5. 改完後一定跑稽核腳本。

---

## 3. 元件使用規則

| 場景 | 優先使用 | 注意事項 |
|---|---|---|
| 容器 | `ds-container` / `ds-container-narrow` | 不要覆寫 padding / max-width |
| 導覽 | `ds-nav` | app class 只做排列，不改內部色彩 |
| 按鈕 | `ds-btn` + `ds-btn-primary` / `ds-btn-ghost` / `ds-btn-sm` | 不覆寫按鈕 padding / 顏色 / 字級 |
| 卡片 | `ds-card` / `ds-card-flat` | app class 可做 grid / hover transform，但不要改 card 內部 token |
| Pill | `ds-pill` / `ds-pill-accent` / `ds-pill-success` | 狀態顯示優先用 pill，不要改 card 背景 |
| Callout | `ds-callout` | 成功 / 警告變體已登記為必要自製語意 |
| 步驟說明 | `ds-step-block` / `ds-step-num` / `ds-step-title` / `ds-step-body` / `ds-step-note` | 非終端機操作步驟用這個，不要用 `ds-term` 假裝 |
| 側欄 | `ds-side-item` + `.current` | 不覆寫內部樣式 |
| 進度條 / 小鴨 | `ds-pbar` / `ds-pbar-fill` / `ds-duck` | JS 只改 `width`、`left`、`walk/dance/left` 狀態 |
| 終端機 | `ds-term` / `ds-term-chrome` / `ds-term-dot` / `ds-term-body` | 指令區塊必須包這個，不要自製 `ds-cmd` |

---

## 4. 自製元件規則

目前允許的自製 `ds-*` 元件只有：

```text
ds-callout--success
ds-callout--warn
ds-check
ds-check-label
ds-teleprompter
ds-shot
```

新增任何自製 `ds-*` 前，必須先更新：

1. `design-system/docs/UI-COMPONENT-CONTRACT.md`：寫清楚為什麼 gallery 不足、使用哪些 token。
2. `design-system/scripts/audit-ui-contract.py`：把新 class 加進 allowlist。

不要新增 `ds-cmd`。指令區塊必須用 gallery 的 `ds-term` 結構，copy button 只能當 wrapper 補在 terminal chrome 的右側。

---

## 5. 嚴格禁止

- 禁止在 `app.css` 寫硬色碼：`#...`、`rgb()`、`rgba()`、`hsl()`、`hsla()`。
- 禁止在 `app.css` 寫非 token 字級；只能用 `var(--fs-*)` 或 `clamp(var(...))`。
- 禁止直接覆寫既有 gallery 元件，例如：
  - `.ds-card`
  - `.ds-btn`
  - `.ds-pill`
  - `.ds-term`
  - `.ds-side-item`
  - `.ds-pbar`
  - `.ds-duck`
  - `.ds-container`
- 禁止為了單頁效果改 `design-system.css`；除非任務明確是更新 design system 本身。
- 禁止讓 copy button 複製高亮後的 HTML；copy 必須複製原始純文字。

---

## 6. 稽核指令

檢查現有 `setup-tutorial`：

```bash
python3 design-system/scripts/audit-ui-contract.py \
  --project setup-tutorial \
  --design-system design-system/assets/css/design-system.css
```

檢查 starter template：

```bash
python3 design-system/scripts/audit-ui-contract.py \
  --project design-system/templates/static-site \
  --design-system design-system/assets/css/design-system.css
```

如果你複製 starter 到 `my-new-site/`：

```bash
python3 design-system/scripts/audit-ui-contract.py \
  --project my-new-site \
  --design-system design-system/assets/css/design-system.css
```

---

## 7. 本 repo 目前狀態

- `design-system/` 已抽成可複用模板。
- `setup-tutorial/` 目前仍是原教學網站，可作參考，但不要把它的 `app.css` 當通用 design system。
- `design-system/assets/css/design-system.css`、`setup-tutorial/assets/css/design-system.css`、`design-system/templates/static-site/assets/css/design-system.css` 目前內容一致。
- 最近一次稽核已通過：
  - `setup-tutorial`
  - `design-system/templates/static-site`

---

## 8. 新 session 建議提示詞

如果要開新 session，建議先貼這段：

```text
請先讀 design-system/HANDOFF-FOR-NEXT-SESSION.md、design-system/docs/UI-COMPONENT-CONTRACT.md，以及 design-system/docs/gallery.html。後續 UI 實作必須優先使用 design-system/assets/css/design-system.css 的 token 與 gallery ds-* 元件；app.css 只能做 layout / wrapper / 狀態。若需要自製元件，先更新 contract 與 audit allowlist，且只用 design token。改完請跑 audit-ui-contract.py。
```
