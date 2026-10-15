# itwilldo-wiki-demo

一個給 [Claude Code](https://claude.com/claude-code) 使用的個人知識庫骨架。

內含三個部分：目錄契約、五份物件規格、四支工作流 skill。

**機制是完整的，內容是空的**——你拿到的不是別人的筆記，是一套讓 AI 幫你把資料整理成知識庫的規則。

AI 每個 session 會自動讀取 `CLAUDE.md`，所以你不需要每次告訴它規則是什麼。

這套機制怎麼設計出來的、為什麼這樣分層，記錄在 [iThome 鐵人賽系列](https://ithelp.ithome.com.tw/users/20160279/ironman/9459)。

## 需要什麼

|                                               | 必要性 | 用途                                          |
| --------------------------------------------- | --- | ------------------------------------------- |
| [Claude Code](https://claude.com/claude-code) | 必要  | 整套知識庫由它驅動                                   |
| Git                                           | 必要  | commit 與推上遠端，也是你的備份與版本紀錄                    |
| [Obsidian](https://obsidian.md/)              | 建議  | 頁面之間用 Wikilink 互連，Obsidian 能直接跳轉、看反向連結與關係圖譜 |

## 開始使用

### 1. 取得你自己的 repo

點擊 GitHub repo 頁面上的綠色 **Use this template** 按鈕，選 **Create a new repository**（不是 Open in a codespace），產生一份屬於你的新 repo——沒有這裡的 commit 歷史，remote 直接指向你自己。知識庫放的是個人內容，建議設成 **Private**。

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

第一次是空的，所以它會開新主題，接著把收錄計畫告訴你、等你確認之後才寫入。寫完你會拿到三樣東西——`1-raw/` 裡的原始來源、`2-wiki/` 裡整理過的頁面，以及 `2-wiki/index.md` 裡的第一筆索引。

## 日常怎麼用

| 想做什麼 | 怎麼說 | 會發生什麼 |
| --- | --- | --- |
| 收錄新來源 | 「把這個收進知識庫」＋內容、連結或檔案路徑 | 先給收錄計畫，你確認後才寫入 |
| 把 `0-capture/` 的內容收進 wiki | 「把 capture 裡的 X 收進 wiki」 | 同上；收完會從 `0-capture/` 移除，原文留在 `1-raw/` |
| 查東西 | 直接問，或用 `/wiki-query` | 回答並附上查過哪些頁面；查不到會說查了哪裡 |
| 存檔 | 「commit」 | 先檢查結構，列出要 commit 的檔案讓你確認，再 commit 並推上遠端 |
| 檢查結構 | 「檢查知識庫」 | 檢查連結、索引、頁面格式，回報結果 |

`0-capture/` 是你自己的發想區，想到什麼直接寫進去就好，不需要叫 AI。

## 目錄怎麼分

```text
0-capture/     還在發想、還沒定型的暫存工作區
1-raw/         原始來源，保留原貌不改寫
2-wiki/        整理後的正式知識
specs/         各類檔案的規格，AI 執行時會讀
```

三者的界線是**內容處於什麼狀態**，不是內容的主題：還在想 → `0-capture/`；已經定型但還沒整理 → `1-raw/`；整理完可以直接查用 → `2-wiki/`。

完整的結構、行為邊界與各情境對應的 skill，見 [`CLAUDE.md`](CLAUDE.md)；單一類型檔案的詳細規格見 [`specs/`](specs/)。這份 README 不重複那些內容，以免兩邊各說各話。

## 維護與擴充

這一節寫給你，也寫給 AI：要改這個知識庫的結構、規則或 skill 時，先看這裡知道要動哪些地方。

### 改動對照表

| 想做什麼 | 要動哪裡 | 連帶影響 |
| --- | --- | --- |
| 調整某個主題收什麼、不收什麼 | `2-wiki/index.md` 該主題的範圍宣告 | AI 收錄時以範圍宣告判斷歸屬，寫得越準，歸類越不會歪 |
| 頁面加一個 frontmatter 欄位 | `specs/wiki-page.md` | skill 執行時才讀 specs，lint 下次就會檢查新欄位，不用改 skill |
| 改頂層資料夾名稱 | `CLAUDE.md`、`specs/` 各份、`.claude/skills/` 各支、本 README | 請 AI 改完後 grep 舊名稱，確認沒有殘留 |
| 加一支 skill | 新增 `.claude/skills/<名稱>/SKILL.md`，並在 `CLAUDE.md` routing 表加一列 | 沒列進 routing 表，AI 不知道什麼時候該用 |
| 拿掉一支 skill 或一個功能 | 刪掉 skill 資料夾和 routing 表那一列 | grep skill 名稱，其他 skill 或 specs 可能還引用著 |
| 加一份規格 | 新增 `specs/<物件>.md` | **一定要有人引用它**——從 `CLAUDE.md` 或會用到它的 skill 裡引用；沒有人引用的規格等於不存在 |
| 改規則本身的寫法 | 先讀 `specs/claude-authoring.md` | 它管的是規則該怎麼寫，包含 `CLAUDE.md` 自己；這是作者的偏好，你有自己的偏好可以自由調整 |

### 規則從失敗長出來

不要預先想像「以後可能需要」的規則。同一件事 AI 做錯第二次，再把它寫成規則，放進對應的 spec 或 `CLAUDE.md`。規則越少，AI 越不會在規則之間打架。

### 知識庫變大之後

連結檢查目前由 AI 每次讀過全部頁面來做。頁面多到 lint 開始漏掉死連結，或每次跑都很慢時，可以請 AI 把連結檢查寫成腳本，再讓 `wiki-lint` 改成呼叫它。

### 改完怎麼確認

1. grep 改掉的舊名稱或舊路徑，確認沒有殘留。
2. 說「檢查知識庫」跑一次 lint。

## 回饋與聯絡

用起來哪裡卡、哪裡順，或是看了之後決定不用，都很想知道：

- GitHub Issues：<https://github.com/troublord/itwilldo-wiki-demo/issues>
- 部落格：[Rambling Quest](https://ramblingquest.com)
- Email：yeelm1487@gmail.com
- LINE ID：scarbelly897
