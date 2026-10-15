# Object spec：wiki 頁面

Object: `2-wiki/` 底下的一般內容頁面。

適用範圍：定義單一 wiki 頁面的 frontmatter、命名與交叉引用規則。`index.md`、`_index.md` 等路由頁面可沿用本規格，但其路由角色由檔名與所在位置判定，不額外使用 frontmatter 標記。

## Frontmatter

每個 wiki 頁面使用 YAML frontmatter：

```yaml
---
tags: [tag1, tag2]
created: 2026-09-22
updated: 2026-09-22
---
```

- `tags`：描述頁面可跨主題使用的標籤。
- `created`：頁面建立日期，格式為 `YYYY-MM-DD`。
- `updated`：頁面最後更新日期，格式為 `YYYY-MM-DD`。


## 命名

頁面名稱應能清楚辨識內容，避免使用過度寬泛、容易與其他頁面混淆的名稱。

例如：

```text
LLM Wiki 與 RAG 的差異.md
```

能直接辨識頁面內容。

這項規則只適用於頁面檔名，不限制 `topics/<topic-name>/` 或 `projects/<project-name>/` 等目錄名稱。

## 交叉引用

wiki 頁面之間使用 Obsidian Wikilink：

```text
[[頁面名稱]]
```

**頁面名稱**應盡量唯一且具體，避免使用 `[[研究]]` 這類泛稱。

若已有與目前內容語意相關的 wiki 頁面，應建立必要的交叉引用。

交叉引用以實際內容關聯為準，不為了增加連結數量而建立無意義連結。

新建立的頁面若目前沒有適合的既有頁面可連結，可以暫時不建立交叉引用。

## 驗證

可機械檢查：

- frontmatter 是否包含 `tags`、`created`、`updated`。
- `tags` 格式是否合法。
- `created`、`updated` 是否符合 `YYYY-MM-DD`。
- Wikilink 是否指向存在的頁面。

需要語意判斷：

- 頁面名稱是否清楚且足以辨識。
- tags 是否與頁面內容相關。
- 交叉引用是否具有實際內容關聯。