---
name: wiki-promote
description: 將 0-capture/ 中已成熟的內容整理進正式知識庫。
---

# Wiki Promote

將 `0-capture/` 中已經完成發想、值得保留的內容正式整理進知識庫。

## 步驟

1. **確認 Promote 範圍**

   確認本次要處理的 capture 檔案或內容範圍。

   若同一份檔案中只有部分內容已成熟，只處理指定部分，不連帶整理其他仍在發想中的內容。

2. **執行 Ingest**

   對本次確定 Promote 的內容，完整依照以下流程處理：

   ```text
   .claude/skills/wiki-ingest/SKILL.md
   ```

3. **清理 Capture**

   確認本次 Promote 的內容已完整保存後，才進行。

   讀取：

   ```text
   .claude/specs/capture.md
   ```

   依規格清理本次已完成處理的內容，可以：

   - 從持續使用的 capture 檔案中移除已處理段落；
   - 刪除已完成用途、且內容已妥善保存的暫存檔案；
   - 保留尚未整理完成的部分。

   執行刪除前，先向使用者說明預計移除的內容並取得確認。
