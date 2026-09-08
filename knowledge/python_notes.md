# Python 技術筆記

## 範例專案 Maple 的本地開發設定

Maple 是本筆記虛構的 Python 範例專案。Maple 開發伺服器使用連接埠 8765，啟動指令是 `python -m http.server 8765`。這是 Maple 的練習設定，不是 Tech Knowledge Base 的啟動設定。

## Python list 與 tuple

Python 的 list（列表）可以新增、刪除或替換元素；tuple（元組）建立後不能新增、刪除或替換其中的元素。需要修改內容時使用 list，例如 `tasks = ["閱讀", "練習"]`；固定組合可使用 tuple，例如 `position = (10, 20)`。tuple 若包含可變物件，該物件本身仍然可以修改。

## Python 虛擬環境

Python 虛擬環境用來隔離不同專案的套件。在 macOS 可用 `python3 -m venv .venv` 建立，再用 `source .venv/bin/activate` 啟用，最後用 `deactivate` 離開。
