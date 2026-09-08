# Tech Knowledge Base

個人技術知識庫，目前實作至 **v0.2 — Ollama Integration**。

## 目前功能與流程

網頁輸入問題 → JavaScript `POST /api/ask` → FastAPI → 本機 Ollama → 網頁顯示回答。

- Ollama endpoint：`POST http://127.0.0.1:11434/api/generate`。
- 傳送 `model`、`prompt`、繁體中文 system 提示與 `stream: false`，收到完整回答後顯示。
- 預設模型為本機已安裝的 `gemma3:latest`，可用 `OLLAMA_MODEL` 環境變數設定單一模型。
- 送出時顯示等待提示並停用表單，完成或失敗後恢復操作。
- 處理 Ollama 未啟動、連線中斷、模型不存在、模型執行失敗、逾時及無效回應。
- 回答以純文字顯示，保留換行，不將模型輸出當成 HTML 執行。
- 尚未讀取 `knowledge/`，沒有筆記搜尋、embeddings、資料庫或對話歷史。

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

若要改用另一個已安裝的模型，在啟動 FastAPI 前執行，例如：

```sh
export OLLAMA_MODEL=gemma4:latest
```

設定變更後需要重啟 FastAPI。`unset OLLAMA_MODEL` 可恢復預設值。

### 3. 開啟網頁

用瀏覽器開啟 <http://127.0.0.1:8000>，輸入問題並按「送出問題」。

測試問題：**請用繁體中文，簡短說明 Python 的 list 和 tuple 有什麼差別。**

預期先顯示 loading，再顯示本機模型的回答。首次模型載入可能較慢。
後端 HTTP 等待逾時為 120 秒，前端等待上限為 150 秒；
前端停止等待不保證 Ollama 立即停止運算。

若 8000 連接埠被占用，改用 `--port 8001` 並開啟對應網址。
按 `Control+C` 停止 FastAPI；執行 `deactivate` 離開虛擬環境。

## 錯誤排查

- 無法連線至 Ollama：確認 App 已開啟，或 `ollama serve` 正在運行。
- 找不到模型：用 `ollama list` 確認名稱，下載指定模型或修改 `OLLAMA_MODEL` 後重啟。
- 模型無法產生回答：檢查 Ollama 的錯誤紀錄與可用記憶體，必要時改用較小模型。
- 回答逾時：縮短問題或改用較小模型後重試。
- 無法連線至網頁後端：重新啟動 FastAPI。

## 檔案結構

```text
main.py                 首頁、問答 API 與 Ollama 呼叫
static/index.html       問題表單與回答區
static/style.css        樣式、loading 與錯誤顏色
static/app.js           API 呼叫、等待狀態與回答顯示
knowledge/.gitkeep      保留目錄，尚未使用
requirements.txt        FastAPI 與 Uvicorn
tests/test_api.py       後端整合邏輯與錯誤處理測試
```

只有 `static/` 提供靜態檔案，`knowledge/` 不會公開或讀取。

## 測試與 v0.2 驗收

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
