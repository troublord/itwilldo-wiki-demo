# 個人知識庫

這是一個由 LLM 協助維護的個人知識庫。

使用者負責閱讀、思考、提供來源與做最終判斷；LLM 負責整理、歸類、建立交叉引用，以及維護知識庫結構。

## 核心架構

```text
./
├── CLAUDE.md
├── README.md
├── .claude/
│   ├── scripts/            ← 檢查用腳本，由 skill 呼叫
│   ├── skills/
│   └── specs/
├── 0-capture/              ← 發想與暫存工作區
├── 1-raw/                  ← 原始來源
│   ├── assets/             ← 圖片、PDF、Word 等附件
│   ├── sources/            ← 正式知識來源
│   └── 雜記/               ← 保留但暫不整理的內容
└── 2-wiki/                 ← 整理後的正式知識
    ├── index.md
    ├── topics/             ← 沒有明確終點、持續累積修訂
    └── projects/           ← 有明確終點的工作
        ├── active/
        └── archive/
```

三個主要區域的角色：

- `0-capture/`：工作中的暫存內容，可自由修改與整理。
- `1-raw/`：保留原貌的來源資料，不因整理而改寫。
- `2-wiki/`：經過整理後，可直接查詢與使用的正式知識。

各類物件的詳細規格位於 `.claude/specs/`。

## 行為邊界

### 保留原始來源

`1-raw/` 中已保存的來源應維持原貌。

不得因摘要、整理、格式修正或建立 wiki 頁面而直接改寫或刪除既有來源。

詳細規則見：

```text
.claude/specs/raw-lifecycle.md
```

### Capture 是工作區

`0-capture/` 用於尚未整理完成的內容。

其中內容可以新增、修改、重組或移除，但在刪除前應確認仍有價值的資訊已經保存到適當位置。

詳細規則見：

```text
.claude/specs/capture.md
```

### Wiki 是整理後的知識

`2-wiki/` 中的頁面應遵守統一的頁面格式、命名與交叉引用規則。

詳細規則見：

```text
.claude/specs/wiki-page.md
```

### 不擅自改變來源意思

整理使用者提供的內容時，可以重新組織資訊、摘要與整合，但不得捏造來源沒有表達的事實、立場或結論。

若整理需要加入推論或分析，應清楚區分來源內容與新增判斷。

### 修改規則本身

新增或修改 `CLAUDE.md` 與 `.claude/skills/*/SKILL.md` 時，規則的寫法本身也有規格。

詳細規則見：

```text
.claude/specs/claude-authoring.md
```

## Routing

遇到多步驟工作時，依情境使用對應 skill。

| 情境                             | 使用                                     |
| ------------------------------ | -------------------------------------- |
| 將新的來源整理並收錄進知識庫                 | `.claude/skills/wiki-ingest/SKILL.md`  |
| 查詢 `2-wiki/` 中的知識              | `.claude/skills/wiki-query/SKILL.md`   |
| 將 `0-capture/` 中已成熟的內容整理進正式知識庫 | `.claude/skills/wiki-promote/SKILL.md` |
| 將進行中的專案移至 archive              | `.claude/skills/wiki-archive/SKILL.md` |
| 在 commit 前檢查知識庫結構              | `.claude/skills/wiki-lint/SKILL.md`    |
| 建立 Git commit                  | `.claude/skills/wiki-commit/SKILL.md`  |
| 從 Git 遠端同步最新內容                 | `.claude/skills/wiki-pull/SKILL.md`    |
| 查看目前 Git 工作目錄狀態                | `.claude/skills/wiki-status/SKILL.md`  |

只需要確認某類檔案應遵守的規格時，直接讀取 `.claude/specs/`，不需要啟動完整 workflow。
