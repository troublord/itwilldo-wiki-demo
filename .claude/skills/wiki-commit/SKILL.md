---
name: wiki-commit
description: 把目前的異動 commit 並推上遠端。
---

# Wiki Commit

1. 呼叫 `wiki-lint`。沒有通過就停下來回報，不 commit。
2. 重新看一次 `git status`（lint 可能改過檔案），以這時的全部異動為範圍，向使用者列出檔案清單與 commit message，取得一次確認。
3. commit，然後 `git push`。
