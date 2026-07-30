# Static Site Starter

這是一個最小可用靜態網站模板。

## 開啟

```bash
python3 -m http.server 8790
```

然後開：`http://127.0.0.1:8790/`

## 稽核

從 repo 根目錄執行：

```bash
python3 design-system/scripts/audit-ui-contract.py \
  --project design-system/templates/static-site \
  --design-system design-system/assets/css/design-system.css
```
