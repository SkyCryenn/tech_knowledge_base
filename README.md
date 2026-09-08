# Tech Knowledge Base

個人技術知識庫，目前實作至 **v0.3 — Local Knowledge**。

## 目前功能與流程

網頁輸入問題 → JavaScript `POST /api/ask` → FastAPI 搜尋本地筆記 → 本機 Ollama → 網頁顯示回答。

- Ollama endpoint：`POST http://127.0.0.1:11434/api/generate`。
- 傳送 `model`、`prompt`、繁體中文 system 提示與 `stream: false`，收到完整回答後顯示。
- 下拉選單提供 `gemma3:latest`、`gemma4:latest`、`qwen3:4b`，清楚顯示目前選擇與回答使用的模型。
- 每次請求傳送 `question` 與 `model`；未傳、null、空字串或空白模型名稱皆使用 `gemma3:latest`。
- 成功與錯誤都顯示從送出至回應處理完成的秒數（包含網路與模型等待，非 Ollama 純推論時間）。
- 送出時顯示等待提示並停用表單，完成或失敗後恢復操作。
- 處理 Ollama 未啟動、連線中斷、模型不存在、模型執行失敗、逾時及無效回應。
- 回答以純文字顯示，保留換行，不將模型輸出當成 HTML 執行。
- 使用關鍵字搜尋 `knowledge/` 的 Markdown，將相關文字傳給 Ollama；沒有匹配時維持一般問答。
- 沒有來源顯示、embeddings、資料庫或對話歷史。

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

若清單沒有 `gemma3:latest`，先下載（本機此次已安裝，無須重複下載）：

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
main.py                 首頁、問答 API 與 Ollama 呼叫
static/index.html       問題表單與回答區
static/style.css        樣式、loading 與錯誤顏色
static/app.js           API 呼叫、等待狀態與回答顯示
knowledge_search.py    Markdown 讀取與關鍵字搜尋
knowledge/python_notes.md  範例技術筆記
knowledge/.gitkeep      保留目錄
requirements.txt        FastAPI 與 Uvicorn
tests/test_api.py       後端整合邏輯與錯誤處理測試
```

只有 `static/` 提供靜態檔案，`knowledge/` 僅由後端讀取，不提供下載路由。

## 測試與 v0.3 驗收

不需要啟動 Ollama 即可執行模擬回應的後端測試：

```sh
.venv/bin/python -m unittest discover -s tests -v
```

這些測試驗證請求內容、回答處理、空白問題、連線失敗、逾時、缺少模型與無效回應。
真實端到端驗收需啟動 Ollama 和 FastAPI，並在瀏覽器逐項確認：

1. 使用者可輸入問題。
2. 本機 Ollama 實際產生回答。
3. 回答出現在瀏覽器。

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
不會回傳來源檔名或新增來源顯示區；這留給 v0.4。

### v0.3 手動驗收

使用 `gemma3:latest` 分別提問：

- 筆記內有答案：「範例專案 Maple 的開發伺服器使用哪個連接埠？如何啟動？」
  預期包含筆記特有的 `8765` 與 `python -m http.server 8765`。
- 筆記內無答案：「DNS 是什麼？請簡短回答。」
  預期仍能收到一般回答，不發生搜尋錯誤。

兩種情況都應保留模型選擇、loading、即時讀秒、最終耗時與錯誤提示。
