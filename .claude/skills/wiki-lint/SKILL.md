---
name: wiki-lint
description: 由 wiki-commit 呼叫，在 commit 前檢查知識庫結構一致性。
---

# Wiki Lint

檢查對象為目前尚未 commit 的異動（`git status` + `git diff HEAD`），不使用歷史 checkpoint。

## 步驟

1. **決定本次要跑哪些檢查**

   執行：

   ```text
   git -c core.quotepath=false status --porcelain=v1 -uall
   ```

   依本次異動涉及的頂層目錄決定後續步驟：

   - 有 `1-raw/` 異動 → 執行步驟 2。
   - 有 `2-wiki/` 異動 → 執行步驟 3、4、5。
   - 兩者都沒有異動（例如只動 `0-capture/` 或 `.claude/`）→ 回報「本次無 `1-raw/`、`2-wiki/` 異動，無需結構健檢」後結束。

   被略過的檢查一律明講略過原因，不靜默跳過。

2. **`1-raw/` 不變性**

   讀取：

   ```text
   .claude/specs/raw-lifecycle.md
   ```

   依其中「不變性」規則檢查本次異動；不符合即為異常。

3. **連結與索引結構**

   執行：

   ```text
   python .claude/scripts/wiki_link_check.py
   ```

   依 exit code 處理：

   - 0：通過。
   - 1：讀取 stdout 的 JSON，回報其中的 `deadlink_forward`（連到不存在的頁面）、`deadlink_reverse`（本次刪除或改名的頁面仍被其他頁面連著）、`ambiguous`（連結同時命中多個頁面）、`unindexed`（新頁面沒有被 `2-wiki/index.md` 或所屬 `_index.md` 收錄）異常。
   - 2：script 本身執行失敗，停止並回報 stderr。
   - 找不到 Python 直譯器（未安裝或不在 PATH）：**不中斷**，回報「連結與索引檢查未執行，本次 commit 未涵蓋這項檢查」，其餘檢查照常進行。

4. **Frontmatter schema**

   讀取：

   ```text
   .claude/specs/wiki-page.md
   ```

   依其中目前定義的 schema 檢查這次有異動的 `2-wiki/**/*.md`。不符合即為異常。

   步驟 2 至 4 任一出現異常即停止並回報，不自行修改異常內容，不繼續 commit。

5. **確認 `index.md` 內容跟上**

   讀取：

   ```text
   .claude/specs/wiki-index.md
   ```

   步驟 3 只機械確認新頁面「有沒有被索引層連到」，這一步處理需要語意判斷的部分：範圍宣告是否仍然準確、既有摘要是否因本次異動而過時、區塊是否已超過門檻而該拆出 `_index.md`。不足的部分直接補上。
