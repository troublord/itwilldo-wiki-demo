---
name: wiki-commit
description: 建立 Git commit。
---

# Wiki Commit

## 步驟

1. **掃描異動**

   執行：

   ```text
   git -c core.quotepath=false status --porcelain=v1 -uall
   ```

   列出這次準備 commit 的所有異動（工作目錄狀態，不比對歷史 checkpoint）。

2. **健檢**

   用 Skill 工具呼叫：

   ```text
   .claude/skills/wiki-lint/SKILL.md
   ```

   無條件呼叫即可，本次異動需要跑哪些檢查由 wiki-lint 自己判斷。lint 未通過則停止 commit 並回報。

3. **確認 commit 範圍與訊息**

   1. 重新掃描 `git -c core.quotepath=false status --porcelain=v1 -uall`，取得目前完整異動——步驟 2 可能已經動過檔案（例如 lint 補上的 `2-wiki/index.md`）。
   2. 從中辨識本次任務直接產生、或使用者明確要求納入的異動；其餘不列入這次 commit。
   3. 向使用者顯示這次的 commit scope（檔案清單）與草擬的 commit message。
   4. 取得使用者一次確認。
   5. 只 `git add` 已確認的檔案。
   6. 建立 commit。
