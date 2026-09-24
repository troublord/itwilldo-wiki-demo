# itwilldo-wiki-demo

一個給 [Claude Code](https://claude.com/claude-code) 使用的個人知識庫骨架。

它由三個部分組成：目錄契約、五份物件規格、八支工作流 skill。

**機制是完整的，內容是空的**——你拿到的不是別人的筆記，是一套讓 AI 幫你把資料整理成知識庫的規則。

AI 每個 session 會自動讀取 `CLAUDE.md`，所以你不需要每次告訴它規則是什麼。

這套機制怎麼設計出來的、為什麼這樣分層，記錄在 [iThome 鐵人賽系列](https://ithelp.ithome.com.tw/users/20160279/ironman/9459)。

## 需要什麼

|                                               | 必要性 | 用途                                          |
| --------------------------------------------- | --- | ------------------------------------------- |
| [Claude Code](https://claude.com/claude-code) | 必要  | 整套知識庫由它驅動                                   |
| Git                                           | 必要  | 多支 skill 直接操作 Git（commit、pull、狀態檢查）         |
| Python 3                                      | 選配  | 解鎖連結與索引的自動檢查，只用標準函式庫，不需要 `pip install`      |
| [Obsidian](https://obsidian.md/)              | 建議  | 頁面之間用 Wikilink 互連，Obsidian 能直接跳轉、看反向連結與關係圖譜 |

沒有 Python 也能正常使用：`wiki-lint` 會回報「連結與索引檢查未執行」，其餘檢查照跑，不會擋住你 commit。

## 開始使用

### 1. 取得你自己的 repo

點擊 Github repo 頁面上的綠色 **Use this template** 按鈕，選 **Create a new repository**（不是 Open in a codespace），產生一份屬於你的新 repo——沒有這裡的 commit 歷史，remote 直接指向你自己。知識庫放的是個人內容，建議設成 **Private**。

接著把它 clone 到本機。

### 2. 啟動

- **Windows**：雙擊 `launch.cmd`；想做成桌面捷徑可以參考 [iThome 鐵人賽系列](https://ithelp.ithome.com.tw/users/20160279/ironman/9459)第八篇
- **macOS / Linux**：`./launch.sh`

兩支腳本做的事一樣：切到知識庫目錄，然後啟動 `claude`。你也可以自己 `cd` 進目錄直接跑 `claude`。

### 3. 丟第一份東西進去

直接告訴它你要收錄什麼，例如：

```text
把這篇文章收進知識庫：<貼上內容或檔案路徑>
```

它會走 `wiki-ingest` 流程，第一次是空的，所以會開新主題，接著把收錄計畫告訴你、等你確認之後才寫入。寫完你會拿到三樣東西——`1-raw/` 裡的原始來源、`2-wiki/` 裡整理過的頁面，以及 `2-wiki/index.md` 裡的第一筆索引。

目前的觸發方式是語意觸發，若要改成明確觸發(例如:呼叫/wiki-ingest才觸發)就直接跟AI說。

之後想查東西就直接問，它會走 `wiki-query`；要 commit 就說要 commit，它會先跑結構健檢再問你確認範圍。

## 目錄怎麼分

```text
0-capture/     還在發想、還沒定型的暫存工作區
1-raw/         原始來源，保留原貌不改寫
2-wiki/        整理後的正式知識
```

三者的界線是**內容處於什麼狀態**，不是內容的主題：還在想 → `0-capture/`；已經定型但還沒整理 → `1-raw/`；整理完可以直接查用 → `2-wiki/`。

完整的結構、行為邊界與各情境對應的 skill，見 [`CLAUDE.md`](CLAUDE.md)；單一類型檔案的詳細規格見 [`.claude/specs/`](.claude/specs/)。這份 README 不重複那些內容，以免兩邊各說各話。

## 可以調整什麼

### 內容——本來就是你的

`0-capture/`、`1-raw/`、`2-wiki/` 出廠就是空的。你放什麼、長成什麼樣子，跟這份模板原本的樣子沒有關係。

### 設定——預期你會動

- **`2-wiki/index.md` 的範圍宣告**：這是 AI 判斷新內容該歸到哪裡的主要依據。主題長出來之後要把「收什麼、不收什麼」寫清楚，寫得越準，之後歸類越不會歪
- **`tags` 慣例**：`wiki-page.md` 有紀錄相關規則，目前只要求有這個欄位，怎麼用是你的事
- **要不要用 `1-raw/雜記/`**：想留著但不打算整理進 wiki 的東西放這裡；用不到就讓它空著或是刪掉

### 機制——能改，但要知道連帶影響

**改規格等於改行為。** skill 是在執行當下才去讀 `.claude/specs/`，不是把規則寫死在自己身上。舉例來說，你在 `wiki-page.md` 的 frontmatter schema 加一個欄位，`wiki-lint` 下次跑就會檢查那個欄位，不需要改 skill。

**改頂層目錄名稱**要動的地方是固定的幾處：`CLAUDE.md`、`.claude/specs/` 各份、`.claude/skills/` 各支，以及 `.claude/scripts/wiki_link_check.py` 頂端的 `WIKI_DIR` 與 `RAW_DIR` 兩個常數（腳本裡的路徑全部走這兩個常數，所以只改這裡就夠）。

具體可以請 AI 掃過之後再次確認。
## 擴充方法

### 加一支 skill

1. 建立 `.claude/skills/<名稱>/SKILL.md`，開頭用 YAML frontmatter 寫 `name` 與 `description`
2. 在 `CLAUDE.md` 的 routing 表加一列：什麼情境 → 用哪支
3. 寫法本身依 [`.claude/specs/claude-authoring.md`](.claude/specs/claude-authoring.md)：觸發條件要能明確判斷、只寫行為不寫理由、條件分支要互斥且完整

### 加一份物件規格

1. 建立 `.claude/specs/<物件>.md`
2. **一定要有人引用它**——例如從 `CLAUDE.md` 的行為邊界進入，或從會用到它的 skill 裡引用。沒有人引用的規格等於不存在，AI 不會憑空想到要去讀它

### 改規則本身的寫法

`claude-authoring.md` 管的就是「規則該怎麼寫」，包含 `CLAUDE.md` 自己。要動規則之前先讀它。

這個規則是作者的偏好，如果你有自己的偏好可以自由調整。
## 自動檢查做了什麼

`wiki-lint` 會在 commit 前跑，它自己判斷這次異動需要跑哪幾項：

| 檢查 | 觸發條件 | 內容 |
| --- | --- | --- |
| 來源不變性 | `1-raw/` 有異動 | 既有來源有沒有被改寫或刪除 |
| 連結與索引 | `2-wiki/` 有異動 | 連到不存在的頁面、刪掉的頁面還被連著、一個連結同時命中多頁、新頁面沒被索引收錄 |
| Frontmatter | `2-wiki/` 有異動 | 欄位是否齊全、格式是否正確 |

只動 `0-capture/` 的 commit 不會觸發任何一項。

其中「連結與索引」由 `.claude/scripts/wiki_link_check.py` 執行，也可以自己跑：

```bash
python .claude/scripts/wiki_link_check.py
```

輸出是一份 JSON，四個欄位都空的就代表沒問題。

這需要你安裝 python ，一樣可以請 AI 做，不安裝不影響功能運行(只是檢查會少一部份)

其他想到再更新上來，有任何想讓作者知道的 feel free to hit me up。

## 聯絡作者

- 部落格：[Rambling Quest](https://ramblingquest.com)
- Email：yeelm1487@gmail.com
- LINE ID：scarbelly897


