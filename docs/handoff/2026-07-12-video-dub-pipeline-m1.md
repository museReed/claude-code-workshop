# Handoff — video-dub-pipeline M1

## 狀態摘要
- 依 TDD §9 完成環境檢查、merge01、00 轉錄、人工潤飾、TTS、組裝、燒字幕，已停在 M1。
- `00/final.mp4` 已產出，尚未取得使用者試看確認，不能跑 01–06。
- `merge01` 已依使用者核准修正為 1920x1080：01-1 scale 1736x1080 後置中 pad，01-2 直入，統一 fps/pix_fmt 後 concat。
- Homebrew core ffmpeg 8.x 缺 libass；已安裝官方 `ffmpeg@7`，只有 render 階段使用 `/opt/homebrew/opt/ffmpeg@7/bin/ffmpeg`。
- 00 原本採逐句 ElevenLabs TTS；另已做段落式實驗版 `00/final_paragraph.mp4` 供比較。
- ElevenLabs key/voice 只從 Keychain 注入當次 env；不得寫入檔案或 log。

## 必讀檔案
- `/Users/reed/Projects/video-dub-pipeline/docs/PRD.md`：產品需求與 M1 停止點背景。
- `/Users/reed/Projects/video-dub-pipeline/docs/TDD.md`：TDD §0/§4/§7/§9 是本次 pipeline 規格與 runbook。
- `/Users/reed/Projects/video-dub-pipeline/pipeline.py`：目前 pipeline CLI 實作，含 `FFMPEG_SUBS_BIN` 與各階段命令。
- `/Volumes/Muse_AI_Core/video_dub_output/00/report.md`：00 正式逐句版輸出報告、TTS 壓縮/overrun 狀態、環境備註。
- `/Volumes/Muse_AI_Core/video_dub_output/00/report_paragraph.md`：段落式 TTS 實驗版分段、字數、timewarp 比例。
- `/Volumes/Muse_AI_Core/video_dub_output/00/polished.srt`：人工潤飾後字幕；時間軸沿用 `draft.srt` 未改。

## 下一步
1. 回覆使用者：段落式版本已產出 `/Volumes/Muse_AI_Core/video_dub_output/00/final_paragraph.mp4`，可與 `/Volumes/Muse_AI_Core/video_dub_output/00/final.mp4` 比較。
2. 說明 ElevenLabs 可調整的「情緒/表現」相關參數：`stability`、`style`、`similarity_boost`、`use_speaker_boost`、`speed`、以及 `previous_text`/`next_text` 對連貫性的幫助。
3. 等使用者試看 M1 與段落式版本後，再決定是否改 pipeline 為段落式；未經同意不得批次跑 01–06。
4. 若後續要繼續 TTS，先用同一個 escalated shell 從 Keychain 讀 key/voice 注入 env，不印值。

## 已知問題
- `/Users/reed/Projects/video-dub-pipeline` 目前不是 git repository；本 handoff commit 在 `/Users/reed/Projects/claude-code-workshop` 當前 branch。
- `gh pr list` 因網路受限連不上 `api.github.com`，未能取得 PR 狀態。
- 段落式版本為實驗輸出；其 paragraph audio 多數比目標時間短，透過 atempo 放慢約 0.80–0.89 倍貼齊原 SRT。
