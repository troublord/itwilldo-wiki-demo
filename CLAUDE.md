這是一個由 LLM維護的知識庫。

## 核心架構

```text
itwilldo-wiki-demo/
├── CLAUDE.md
├── README.md
├── 0-capture/              ← 發想與暫存工作區
├── 1-raw/                  ← 原始來源
│   ├── assets/             ← 附件（圖片、Word、PDF 等）
│   ├── sources/
│   └── 雜記/
└── 2-wiki/                 ← 整理後的正式知識內容
    ├── topics/             ← 沒有明確終點、持續累積修訂
    └── projects/           ← 有明確終點的工作
        ├── active/
        └── archive/        ← 工作結束後歸檔至此
```

## 語言慣例

使用繁體中文進行對話與內容撰寫，除非來源本身是英文且逐字引用/專有名詞更適合保留原文（例如論文標題、人名）。

