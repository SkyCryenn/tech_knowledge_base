# Tech Knowledge Base

個人技術知識庫，已完成本地問答、知識檢索與來源顯示，並完成 **v0.5 — Demo Polish** 的展示整理。

目前首頁與 API 版本標示仍為 v0.4；本次收尾僅更新文件。

## 目前功能與流程

網頁輸入問題 → JavaScript `POST /api/ask` → FastAPI 搜尋本地筆記 → 本機 Ollama → 網頁顯示回答、內容來源與處理時間。

- Ollama endpoint：`POST http://127.0.0.1:11434/api/generate`。
- 傳送 `model`、`prompt`、繁體中文 system 提示與 `stream: false`，收到完整回答後顯示。
- 下拉選單提供 `gemma3:latest`、`gemma4:latest`、`qwen3:4b`，清楚顯示目前選擇與回答使用的模型。
- 每次請求傳送 `question` 與 `model`；未傳、null、空字串或空白模型名稱皆使用 `gemma3:latest`。
- 送出後立即開始讀秒，每 0.1 秒更新；成功或錯誤時停止並保留最終耗時（包含網路與模型等待，非 Ollama 純推論時間）。
- 送出時顯示等待提示並停用表單，完成或失敗後恢復操作。
- 處理 Ollama 未啟動、連線中斷、模型不存在、模型執行失敗、逾時及無效回應。
- 回答以純文字顯示，保留換行，不將模型輸出當成 HTML 執行。
- 使用關鍵字搜尋 `knowledge/` 的 Markdown，將相關文字傳給 Ollama；沒有匹配時維持一般問答。
- 回答下方有固定的「內容來源」區塊：單一來源顯示檔名，多個來源去重後逐行列出，沒有匹配時顯示「無本地筆記」。
- 沒有 embeddings、資料庫或對話歷史。

Python 相依套件仍只有 FastAPI 與 Uvicorn。HTTP 呼叫使用標準函式庫 `urllib`，
資料驗證使用 FastAPI 已相依的 Pydantic，無須新增套件。

## 在 macOS 啟動

需要 Python 3.10 或更新版本，以及 [Ollama](https://ollama.com/download/mac)。

### 1. 啟動 Ollama

開啟 Ollama App，或在終端機執行並保持運行：

```sh
ollama serve
```

若服務已運行，不必再執行 `ollama serve`。在另一個終端機檢查模型：

```sh
ollama list
```

若清單沒有 `gemma3:latest`，先下載：

```sh
ollama pull gemma3:latest
```

### 2. 啟動 FastAPI

```sh
cd /Users/hughessmacbook/Projects/tech_knowledge_base
```

首次安裝時執行；若已有 `.venv`，可略過建立步驟：

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

每次啟動：

```sh
source .venv/bin/activate
python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

在網頁下拉選單切換模型即可，不需要重啟 FastAPI。
本版改為每次請求選擇模型，不讀取或修改 `OLLAMA_MODEL` 環境變數。

### 3. 開啟網頁

用瀏覽器開啟 <http://127.0.0.1:8000>，輸入問題並按「送出問題」。

請透過上述 FastAPI 網址使用網頁，不要直接雙擊 `static/index.html`。
直接開啟 HTML 檔案時，`/static/` 資源與 `/api/ask` 無法連到本地服務。
若頁面只有文字、沒有樣式，先確認網址，再按 `Command+Shift+R` 強制重新整理。
可開啟 <http://127.0.0.1:8000/static/style.css> 確認樣式檔可讀取。

測試問題：**請用繁體中文，簡短說明 Python 的 list 和 tuple 有什麼差別。**

預期先顯示 loading，再顯示本機模型的回答。首次模型載入可能較慢。
後端 HTTP 等待逾時為 120 秒，前端等待上限為 150 秒；
前端停止等待不保證 Ollama 立即停止運算。

若 8000 連接埠被占用，改用 `--port 8001` 並開啟對應網址。
按 `Control+C` 停止 FastAPI；執行 `deactivate` 離開虛擬環境。

## 錯誤排查

- 無法連線至 Ollama：確認 App 已開啟，或 `ollama serve` 正在運行。
- 找不到模型：用 `ollama list` 確認名稱，下載指定模型或在網頁切換至已安裝的模型。
- 模型無法產生回答：檢查 Ollama 的錯誤紀錄與可用記憶體，必要時改用較小模型。
- 回答逾時：縮短問題或改用較小模型後重試。
- 無法連線至網頁後端：重新啟動 FastAPI。

## 檔案結構

```text
main.py                 首頁、問答 API、Ollama 呼叫與頁面快取設定
knowledge_search.py     Markdown 讀取、關鍵字搜尋與來源追蹤
static/index.html       問題表單、模型選單、回答與來源區塊
static/style.css        頁面與來源區塊樣式
static/app.js           API 呼叫、loading、即時讀秒與來源顯示
knowledge/              本地 Markdown 筆記（清單如下）
requirements.txt        FastAPI 與 Uvicorn
tests/test_api.py        API 與錯誤處理測試
tests/test_knowledge.py  搜尋、context 與來源去重測試
```

只有 `static/` 提供靜態檔案，`knowledge/` 僅由後端讀取，不提供下載路由。
首頁與靜態檔案停用快取，避免更新後混用新舊 HTML、JavaScript 與 CSS。

## 目前的示範筆記

| 檔案 | 內容 |
| --- | --- |
| [python_notes.md](knowledge/python_notes.md) | Python list／tuple、虛擬環境，以及虛構 Maple 專案的連接埠練習設定 |
| [git_notes.md](knowledge/git_notes.md) | 查看修改、暫存與提交、版本歷史及 `.gitignore` |
| [ollama_notes.md](knowledge/ollama_notes.md) | 啟動 Ollama、模型清單與下載、終端機問答及常見錯誤 |
| [macos_python_notes.md](knowledge/macos_python_notes.md) | macOS 專案目錄、虛擬環境、安裝套件與啟動 FastAPI |
| [test1.md](knowledge/test1.md) | 個人旅遊安排，用於驗證自訂筆記檢索 |
| [test2.md](knowledge/test2.md) | 個人小說閱讀紀錄，用於驗證自訂筆記檢索 |

`knowledge/.gitkeep` 僅用來保留目錄，不是知識筆記。Maple 的練習設定與本專案的啟動設定不同。

## 測試與展示驗收

不需要啟動 Ollama 即可執行模擬回應的後端測試：

```sh
.venv/bin/python -m unittest discover -s tests -v
```

這些測試涵蓋請求內容、模型選擇、錯誤處理、Markdown 搜尋、context 傳遞與來源去重。
真實端到端驗收需啟動 Ollama 和 FastAPI，並在瀏覽器逐項確認：

1. 使用者可輸入問題。
2. 本機 Ollama 實際產生回答。
3. 回答出現在瀏覽器，下方顯示來源區塊。
4. 等待時秒數持續更新，完成或錯誤時保留最終時間。

API 另會拒絕缺少問題、非字串或超過 10,000 字元的問題。

### 三個模型的手動測試

依序選擇 `gemma3:latest`、`gemma4:latest`、`qwen3:4b`，每次輸入：
「請用繁體中文一句話說明 Python 的 list 和 tuple 的差別。」

每個模型都確認：

1. 目前模型名稱隨下拉選單更新。
2. 送出後顯示 loading，模型與問題欄位暫時停用。
3. 回答完成後顯示該次模型名稱、回答與「處理時間：X.X 秒」。
4. 切換下一個模型時，上一則回答仍保留原本模型標記；新請求會清除舊回答與計時。
5. FastAPI 停止後再次送出，應顯示連線錯誤及本次耗時，表單恢復可操作。

若模型尚未安裝，分別執行 `ollama pull gemma3:latest`、
`ollama pull gemma4:latest` 或 `ollama pull qwen3:4b`。

### 新增自己的 Markdown 技術筆記

把 UTF-8 編碼的 `.md` 檔放入 `knowledge/` 或其子目錄，例如 `knowledge/git.md`。
使用清楚的標題、技術名詞與空行分隔段落，將主題名稱和相關說明放在同一段。
每次提問都會重新讀取，新增或修改筆記後不需要重啟伺服器。

搜尋流程：

1. 英文轉小寫並以單字比對；中文拆成相鄰兩字，排除少數常見問句詞。
2. 每段筆記計算與問題重疊的不同關鍵字數，依分數排序。
3. 最多取三段，每段最多 2,000 字元；很長的段落會先切段。
4. 只將筆記文字與問題分開放入 prompt，要求模型優先參考筆記。
5. 沒有匹配、目錄不存在或沒有可讀筆記時，直接使用一般問答。無法讀取的檔案會略過並記錄警告。

這是簡單的字面搜尋，不理解同義詞或語意；中文單字查詢不支援，兩字重疊也可能誤判。
API 回傳 `answer`、`model` 與 `sources`（檔名字串陣列）。
來源來自實際傳給 Ollama 的段落，依搜尋排序去重；子目錄保留相對路徑。
這些是提供給模型的參考筆記，不代表回答的每一句都取自筆記。

### 本地知識檢索測試

使用 `gemma3:latest` 分別提問：

- 筆記內有答案：「範例專案 Maple 的開發伺服器使用哪個連接埠？如何啟動？」
  預期包含筆記特有的 `8765` 與 `python -m http.server 8765`。
- 筆記內無答案：「DNS 是什麼？請簡短回答。」
  預期仍能收到一般回答，不發生搜尋錯誤。

兩種情況都應保留模型選擇、loading、即時讀秒、最終耗時與錯誤提示。

### 來源顯示測試

1. 問「Maple 開發伺服器的連接埠？」：回答下方的「內容來源」區塊應包含 `python_notes.md`；其他匹配來源也可能列出。
2. 問「DNS 是什麼？請簡短回答。」：如果筆記沒有 DNS 內容，「內容來源」區塊應顯示「無本地筆記」。
3. 測試多來源時，在 `knowledge/` 新增兩份 Markdown，以相同的獨特關鍵字寫段落，
   其中一份寫兩段。用該關鍵字提問；若三段都命中，應列出兩個檔名，每個僅一次。
4. 再次送出或遇到錯誤時，舊的回答和來源不應殘留在畫面上。

來源仍受既有「最多三段」限制，僅列出選入 context 的檔案，不列出其他匹配檔案。

### 技術筆記展示問題

- 「Git 如何查看尚未暫存的修改？」
- 「Ollama 如何下載模型？」
- 「macOS 如何啟動本專案的 FastAPI？」

觀察回答是否符合筆記，且來源區塊包含相關檔案。新增筆記會影響關鍵字排序，
同一問題可能命中多份檔案；來源以當次實際送入模型的內容為準。
