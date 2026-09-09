# macOS Python 開發筆記

## 進入專案目錄

在 macOS 終端機執行 `cd ~/Projects/tech_knowledge_base` 進入本專案，再以 `pwd` 確認目前位置。`python3 --version` 可確認 Python 是否能使用及其版本。

## 建立與啟用虛擬環境

macOS 上可用 `python3 -m venv .venv` 建立 Python 虛擬環境，隔離本專案的套件；已有 `.venv` 時不用重建。每次開啟新的終端機工作階段，先在專案目錄執行 `source .venv/bin/activate`；完成工作後用 `deactivate` 離開。

## 安裝專案套件

啟用 Python 虛擬環境後，執行 `python -m pip install -r requirements.txt` 安裝本專案的 FastAPI 與 Uvicorn。`python -m pip` 使用目前 Python 對應的套件管理工具，避免套件裝到另一個 Python 環境。

## 啟動與停止網頁

在 macOS 的專案目錄啟用虛擬環境後，執行 `python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000` 啟動 FastAPI，接著用瀏覽器開啟 `http://127.0.0.1:8000`。`--reload` 讓程式修改後自動重新載入；按 `Control+C` 停止伺服器。若 8000 已被占用，可改為 `--port 8001`，並使用對應網址。

參考：[Python 官方 venv 說明](https://docs.python.org/3/library/venv.html)。
