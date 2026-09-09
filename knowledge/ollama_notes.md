# Ollama 基礎筆記

## 啟動本機服務

Ollama 負責在本機執行模型。開啟 Ollama App，或在終端機執行 `ollama serve` 啟動服務；若服務已經運行，不必重複啟動。本專案由 FastAPI 呼叫 `http://127.0.0.1:11434/api/generate`，網頁不會直接呼叫模型。

## 查看與下載模型

Ollama 指令 `ollama list` 可列出已安裝模型；若缺少模型，可用 `ollama pull gemma3:latest` 下載。本專案下拉選單提供 `gemma3:latest`、`gemma4:latest`、`qwen3:4b`；選擇某模型前，應先確認它已安裝。

## 單獨測試模型

Ollama 指令 `ollama run gemma3:latest "請用一句話介紹 Python"` 可以在終端機測試模型回答。這有助於區分問題是發生在模型服務，還是網頁與 FastAPI 的連線。

## 等待與錯誤

Ollama 首次載入模型可能較慢。本專案使用 `stream: false`，因此網頁會持續讀秒，等完整回答回來才顯示。若無法連線，確認 Ollama 已啟動；若找不到模型，用 `ollama list` 核對名稱；若逾時或記憶體不足，可縮短問題或選擇較小的模型。

參考：[Ollama 官方 CLI 說明](https://docs.ollama.com/cli)。
