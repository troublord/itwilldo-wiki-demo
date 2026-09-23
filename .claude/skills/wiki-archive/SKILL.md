---
name: wiki-archive
description: 將進行中的專案移至 archive。
---

# Wiki Archive

## 步驟

1. **觸發**

   收到明確的歸檔要求後直接執行，不需要再次確認。

2. **搬移 wiki**

   將該專案在 `2-wiki/projects/` 下的目錄以 `git mv` 由 `active/` 移至 `archive/`。

   不搬動 `1-raw/` 對應內容。

3. **修正連結**

   搜尋 `2-wiki/` 中指向舊完整路徑的 Wikilink，改成新路徑；短名連結不需處理。

4. **更新索引**

   讀取：

   ```text
   .claude/specs/wiki-index.md
   ```

   依規格將該專案條目移至 `2-wiki/index.md` 的 Archived Projects 區塊；步驟 3 掃到的相關頁面一併同步。
