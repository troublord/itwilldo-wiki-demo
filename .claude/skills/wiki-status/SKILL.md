---
name: wiki-status
description: 用來快速掌握目前的 git 修改狀況
disable-model-invocation: true
allowed-tools: Bash
---

# Wiki 狀態報告

回答「現在 git 上到底有什麼還沒 commit」。除了 `git fetch` 更新遠端追蹤資訊外，不異動任何檔案。

## 步驟

1. **更新遠端資訊**：執行 `git fetch`。失敗（例如離線）時不中斷，在回報中註明 ahead/behind 以上次 fetch 為準。

2. **取得分支與完整異動**：執行 `git -c core.quotepath=false status --porcelain=v1 -b -uall`。
   - 第一行 `## <分支>...<upstream> [ahead N, behind M]` 取得分支與領先／落後數；沒有 upstream 時只有分支名稱。
   - 其餘各行為異動檔案。

3. **整理異動**：
   - 將 Git 狀態轉成白話的「新增、修改、刪除、搬移／改名」。
   - 依檔案的頂層目錄分組；repo 根目錄檔案另列為「根目錄」。
   - 每組列出實際異動檔案。

4. **檢查 1-raw/ 異動**：若本次有 `1-raw/` 異動，讀取 `.claude/specs/raw-lifecycle.md`，依其中目前規則判斷是否異常。異常只回報，不自行修復。

5. **回報**：
   - 先摘要目前分支、ahead/behind 狀態與異動總數。
   - 再按分類列出異動檔案。
   - 若有 `1-raw/` 異常或本地落後遠端，放在摘要最前面提醒。
