# Tech Knowledge Base

個人技術知識庫，目前完成 **v0.1 — Project Foundation**。

## 目前功能

- FastAPI 提供首頁與靜態檔案。
- 原生 HTML、CSS、JavaScript 提供問題輸入欄位及送出按鈕。
- 送出時顯示版本提示；問題不會傳送或儲存，也不會產生回答。
- `knowledge/` 保留供後續版本使用，目前不會讀取筆記。

尚未整合 Ollama。後續版本範圍請參閱 `ROADMAP.md`。

## 在 macOS 本地執行

先確認已安裝 Python 3.10 或更新版本，並可執行 `python3 --version`。
本次實際驗證使用 Python 3.14.7。

在終端機進入專案目錄：

```sh
cd /Users/hughessmacbook/Projects/tech_knowledge_base
```

第一次設定時建立虛擬環境並安裝套件（若已有 `.venv`，可略過建立步驟）：

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

每次啟動時，在專案目錄執行：

```sh
source .venv/bin/activate
python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

用瀏覽器開啟 <http://127.0.0.1:8000>。
若 8000 連接埠已被占用，可改為 `--port 8001`，並開啟對應網址。

按 `Control+C` 停止伺服器；執行 `deactivate` 離開虛擬環境。

## 檔案結構

```text
main.py              FastAPI 首頁路由與靜態檔案設定
static/index.html    首頁與問題表單
static/style.css     基本樣式
static/app.js        表單互動
knowledge/.gitkeep   保留空的知識目錄
requirements.txt     FastAPI 與 Uvicorn 直接相依套件
.gitignore           排除虛擬環境、快取與本地敏感設定
```

靜態檔案路徑以 `main.py` 所在位置為基準。只有 `static/` 對外提供檔案，
`knowledge/` 不會公開。

## v0.1 驗收方式

1. 執行啟動指令，確認出現 `Application startup complete`。
2. 在瀏覽器開啟首頁，確認標題、問題欄位與送出按鈕正常顯示。
3. 輸入問題並送出，確認文字保留且顯示 v0.1 尚未提供回答功能的提示。

不需要安裝 Ollama、Node.js、資料庫或前端建置工具。
