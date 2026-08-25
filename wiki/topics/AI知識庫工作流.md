# AI 知識庫工作流

收集「別人怎麼設計、操作 AI 輔助的筆記/知識庫系統」的方法與技巧，作為以後優化咱們自己這個知識庫時的參考靈感，不是咱們自己實際做的決定（咱們自己實際的架構變動記在 [[建設歷程]]）。

## 心心：用 Obsidian + Claude Code 打造第二大腦

**來源**：YouTube 保姆級教程，逐字稿存在 `raw/links/用ObsidianAI搭建第二大腦-保姆級教程.md`，原影片 https://www.youtube.com/watch?v=RZEb6FLZSHE

講者從 Milanote 換到 Obsidian，因為 Obsidian 本質是管理本地 Markdown 檔案，AI 可以直接讀寫操作；Milanote 存雲端、結構層層嵌套，AI 難以系統性讀取。做法重點：

- **給 AI 用的兩層導航**：根目錄放 `CLAUDE.md` 當總入口（自我介紹 + 資料夾地圖，告訴 AI 什麼情況要讀哪個資料夾）；每個資料夾裡再放一個 `instructions.md`，寫這個資料夾的結構、命名規則、操作方式。AI 進資料夾前一定先讀 instructions.md，只讀當下需要的那一層，不用整庫掃過，省 token 也變快。
- **Daily Notes 當 session 之間的記憶橋樑**：每天開新的 Claude Code session，結束前請 AI 把當天做了什麼、卡在哪裡、還要跟進什麼寫進當天的 Daily Notes。下次開新 session 不用重讀整庫，只讀最近幾天的 Daily Notes 就能接續脈絡。
- **自動化輸入管道**：Obsidian Web Clipper 一鍵存網頁/推文/YouTube 字幕（含時間戳，可跳轉影片片段）；Apple Books 劃線內容一鍵匯入；iPhone Action Button + Shortcuts 設定語音記錄，走路開車時也能把一閃而過的想法記進 Daily Notes。
- **Canvas 畫思維導圖**：Obsidian 的 Canvas 本質是本地 JSON 檔案，可以直接截圖給 Claude，讓它幫忙生成/修改思維導圖，取代原本用 Milanote 畫圖的需求。
- **把 Claude Skills 放進筆記庫資料夾**：這樣 Skill 的參考文件可以跟著筆記庫的內容一起持續更新，不會脫節。
- 其他省 token 技巧：用 Obsidian 官方 CLI 操作筆記，比讓 AI 直接讀寫檔案省 token。

**跟咱們現在的差異，可以參考的點**：
- 咱們目前只有根目錄的 `CLAUDE.md`，還沒有各資料夾各自的 `instructions.md`——這篇是具體案例，以後資料夾/資料變多、`CLAUDE.md` 開始塞不下細節時可以參考這個分層做法。
- 咱們還沒有 Daily Notes 機制。使用者提到以後可能想加「待辦清單」之類的功能，這篇的「AI 每天結束寫日誌、下次接續脈絡」做法，是一個現成的參考方向——待辦清單可以是 Daily Notes 的其中一種用途（追蹤「還要跟進什麼」）。
