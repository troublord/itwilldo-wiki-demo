---
name: wiki-pull
description: 從 Git 遠端同步最新內容。
---

# Wiki Pull

## 步驟

1. **確認工作目錄**

   執行 `git status --porcelain`。

   - 工作目錄乾淨：繼續。
   - 有未 commit 的異動：停止並列出異動，讓使用者決定如何處理後再繼續。
   - 使用者選擇暫存異動時，使用 `git stash push -u`，並記錄本次有建立 stash。

2. **記錄同步前狀態**

   執行 `git rev-parse HEAD`，保存同步前的 HEAD。

3. **同步遠端**

   執行 `git pull --ff-only`。

   - 成功：繼續。
   - 無法快轉或發生其他錯誤：停止並回報，不自行 merge、rebase 或覆蓋內容。

4. **還原 stash**

   若步驟 1 有建立 stash，執行 `git stash pop`。發生衝突時停止並回報衝突檔案，不自行解決。

5. **摘要同步結果**

   以同步前 HEAD 與目前 HEAD 執行：

   - `git log <舊HEAD>..HEAD --oneline`
   - `git diff <舊HEAD> HEAD --stat`

   簡短回報這次新增的 commit 與受影響範圍。
