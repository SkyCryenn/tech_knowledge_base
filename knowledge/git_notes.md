# Git 基礎筆記

## 查看修改

Git 用來記錄檔案的版本。在專案目錄執行 `git status`，可以查看新增、修改及已暫存的檔案；`git diff` 查看尚未暫存的修改，`git diff --staged` 查看準備提交的修改。

## 暫存與提交

Git 的暫存區用來挑選本次要記錄的修改。例如 `git add knowledge/git_notes.md` 只暫存這份筆記；確認內容後，`git commit -m "Add Git notes"` 才會建立本地版本紀錄。修改已暫存的檔案後，需要再次執行 `git add` 才會更新暫存內容。這些是操作範例，不代表本次已建立 commit。

## 查看歷史

Git 指令 `git log --oneline -5` 可查看最近五筆提交摘要。`git commit` 記錄在本機；`git push` 才會將提交傳到已設定的遠端儲存庫，兩者是不同步驟。

## 忽略本地檔案

Git 的 `.gitignore` 用來忽略尚未追蹤的檔案。本專案會忽略 `.venv/`、`__pycache__/` 與 `.env`，避免將虛擬環境、快取或敏感設定加入版本控制；已被 Git 追蹤的檔案不會因新增忽略規則而自動取消追蹤。

參考：[Git 官方入門教學](https://git-scm.com/docs/gittutorial)。
