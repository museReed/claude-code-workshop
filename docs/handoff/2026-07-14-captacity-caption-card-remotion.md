# Handoff — captacity 字幕 + Remotion 字卡 component

**日期**：2026-07-14  **類型**：continuation
**工作目錄**：`/Users/reed/Projects/video-dub-pipeline/remotion-cards`（**非 git**）+ 素材在外接碟 `/Volumes/Muse_AI_Core/video_dub_output/00`

## 狀態摘要（已完成）

1. **`<Caption>` 逐字高亮字幕 component**（`remotion-cards/src/Caption.tsx`）：三種 style 全做完並視覺驗證——`clean`（換白提亮）/ `karaoke`（accent 底線隨唸讀刷過）/ `pop`（逐字彈入 + scale 彈跳）。每 style 有預設高亮色，`accent` prop 可覆寫。
2. **`Card` 右上角資訊卡四項升級**（`remotion-cards/src/Card.tsx`）：退場動畫（`durationInFrames` prop）、進場 stagger（色條→標題→內文）、位置(`POSITION_PRESETS`)+尺寸(sm/md/lg)、5 種類型 + 單色 glyph（term ℹ藍 / emphasis ★琥珀 / warning ⚠紅 / tip ✓綠 / quote ❝紫）。既有卡相容。
3. **00 影片疊新卡**：Remotion CardsOverlay 渲染成透明 ProRes 4444（alpha）→ ffmpeg 疊到底片。已產出 `/Volumes/Muse_AI_Core/video_dub_output/00/final_with_cards_remotion.mp4`（含配音）。
4. **類型重分類 + 去音軌**：`cards-data.json` cue10 trouble shooting→warning、cue51 重點→quote。**進行中**：正在 composite 靜音版 `final_with_cards_remotion_muted.mp4`（background task `bef3jna8f`，用 `-an`，供用戶之後重錄配音）。

## 必讀檔案

- `remotion-cards/src/Card.tsx` — 升級後的卡片 component（改動最大，看 5 類型 + 退場 + stagger 邏輯）
- `remotion-cards/src/Caption.tsx` — 逐字字幕 component（三 style switch 分支）
- `remotion-cards/src/Root.tsx` — 6 個 Composition：CardsOverlay(正式) / CaptionDemo / KaraokeDemo / PopDemo / CardShowcase
- `remotion-cards/src/cards-data.json` — 00 的 8 張卡資料（已改 cue10/cue51 類型）
- `tools/burn_cards.py` — **舊的** ffmpeg ASS 燒卡流程（要被取代的對象）
- `remotion-cards/AGENTS.md` — 已改成 Remotion/TS 版（無 unit test 要求），派 codex 前確認

## 關鍵指令（可重跑）

```
# 渲染透明卡片層（alpha 必須這樣才有）
cd /Users/reed/Projects/video-dub-pipeline/remotion-cards
npx remotion render src/index.ts CardsOverlay out/overlay-00.mov \
  --codec=prores --prores-profile=4444 --pixel-format=yuva444p10le

# 疊到底片（含配音）
cd /Volumes/Muse_AI_Core/video_dub_output/00
/opt/homebrew/opt/ffmpeg@7/bin/ffmpeg -y \
  -i final_tempo_paragraph_anchor_subtitle_plain.mp4 \
  -i /Users/reed/Projects/video-dub-pipeline/remotion-cards/out/overlay-00.mov \
  -filter_complex "[0:v][1:v]overlay=format=auto" \
  -map 0:a -c:a copy -c:v libx264 -crf 18 -preset medium -pix_fmt yuv420p \
  -movflags +faststart final_with_cards_remotion.mp4
# 靜音版把 `-map 0:a -c:a copy` 換成 `-an`
```

## 下一步

1. **確認靜音版產出**：check `final_with_cards_remotion_muted.mp4`，抽 t=30s（warning 紅）、t=163s（quote 紫）確認新類型顏色對。
2. **task 2：把上面流程包成腳本取代 `burn_cards.py`**（用戶已要求）。派 codex，spec 要點：
   - 新工具 `tools/burn_cards_remotion.py <id> [--mute] [--base FILE]`
   - 讀 `video_dub_output/<id>/cards.json`（含 cue）+ srt 算 start/end（參考 burn_cards.py 的 `card_events`）→ 生成 `remotion-cards/src/cards-data.json`
   - 跑 remotion render（上面指令）→ ffmpeg 疊卡（`--mute` 時用 `-an`）
   - **不要移除舊 `burn_cards.py`**，並存供對照
   - 驗收會跑 remotion render，**勿與其他 render 並行**（撞 out/overlay-00.mov）
   - 非 git 目標，走 codex-agent skill 非 git 模式（`CODEX_SNAPSHOT_GLOBS`）

## 已知問題 / 注意

- `remotion.config.ts` 只設 `setVideoImageFormat('png')`；alpha **必須** CLI 明給 `--pixel-format=yuva444p10le`，否則出 ProRes 422 無 alpha（踩過）。
- 底片 `final_tempo_...plain.mp4` 是 60fps，overlay 30fps，ffmpeg overlay 依秒對齊 OK。
- CODEX_SNAPSHOT_GLOBS 逗號多 glob 只吃第一個（工具限制），review 時另一檔直接讀新檔。
- Caption chunk 之間有時間空隙會 render null（字幕短暫消失），連續語音無妨。

## 追加進度（session 後段）

- **01 影片完成**：8 張卡從逐字稿新編（Antigravity / Review-driven / 必須勾選(warning) / 安全性(quote) / 兩種 Yes / Markdown 預覽等），已產出靜音版 `video_dub_output/01/final_with_cards_remotion_muted.mp4`。⚠️ 只做結構驗證（檔在 + 音軌=0），**未逐幀視覺確認**——抽 t=131s(warning紅)、t=205s(quote紫) 確認。
- 01 用 1920x1080（00 是 1736x1080）；`cards-data.json` 加了 `duration` 欄位、Root.tsx `DURATION` 改成資料驅動。
- **互動 flowchart**：`remotion-cards/flow.html`（codex + frontend-skill 產，自包含，節點可展開），涵蓋整條 flow。
- **注意：`cards-data.json` 現在是 01 的內容**（覆寫了 00 的）。要重跑 00 需還原 00 版資料（8 卡見上表 / git 無、可從 00 cards.json 重建）。

## 🔴 下一步第一優先：字幕 vs 畫面動作 時間軸錯位（用戶回報）

- **現象**：燒在影片上的字幕跟螢幕上的操作對不上（用戶用 `字幕 vs 畫面動作` 明確指認，非「卡 vs 字幕」也非潤飾問題）。
- **已排除**：draft.srt / polished.srt / render_plain srt 三條**首尾時間戳完全相同**（0–3.92s 起、6:50.7–6:52.64 止）→ 潤飾步驟沒動時間軸。卡片騎在字幕時間軸，非根因。
- **懷疑點**：`pipeline.py` 的 tempo / paragraph-anchor 調速步驟（產出 `final_tempo_paragraph_anchor_subtitle_plain.mp4`）——把段落調速對齊配音時，字幕或畫面其一沒同步位移。
- **下一步**：讀 `pipeline.py` 找 tempo/anchor 邏輯，比對「調速後的畫面時間軸」與「字幕 srt 時間軸」是否同源；先在 01 抓一個明顯錯位的時間點量偏移量。字幕修對後，卡片時間軸要一起重算 + 重渲染。
