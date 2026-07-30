# claude2code Design System Template

這個目錄是可複用的靜態網站 design-system 模板，抽自 `setup-tutorial/`。

## 內容

```text
design-system/
├─ assets/css/design-system.css      # token + gallery ds-* 元件定義
├─ assets/css/design-system.json     # token 結構化參考
├─ docs/gallery.html                 # 元件展示頁
├─ docs/gallery.css                  # 展示頁 layout、wrapper 與操作樣式
├─ docs/UI-COMPONENT-CONTRACT.md     # 使用契約
├─ scripts/audit-ui-contract.py      # 稽核腳本
├─ scripts/verify_*.py               # gallery Playwright 驗證腳本
└─ templates/static-site/            # 最小可用靜態站模板
```

Gallery 現有 45 個元件（含 17 個動態變體）與 18 個服務圖示。

## 使用方式

1. 複製 `assets/css/design-system.css` 到你的專案，例如：

   ```text
   your-site/assets/css/design-system.css
   ```

2. 在 HTML 引入 Google Fonts 與 design-system：

   ```html
   <link rel="preconnect" href="https://fonts.googleapis.com">
   <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
   <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
   <link rel="stylesheet" href="assets/css/design-system.css">
   <link rel="stylesheet" href="assets/css/app.css">
   ```

3. 新專案的 `app.css` 只能做頁面 layout、wrapper、狀態；不要覆寫既有 `ds-*` 元件。

4. 執行稽核：

   ```bash
   python3 design-system/scripts/audit-ui-contract.py --project your-site --design-system design-system/assets/css/design-system.css
   ```

## 原則

- 既有 UI 先找 `docs/gallery.html` 中的 `ds-*` 元件。
- 自製元件只能在 design-system 語意無法滿足時新增。
- 自製元件也必須只使用 `design-system.css` 的 token：顏色、字體、字級、間距、圓角、陰影。
