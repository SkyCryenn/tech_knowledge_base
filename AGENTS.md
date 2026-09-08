# AGENTS.md

## Project Goal

建立一個個人技術知識庫（Tech Knowledge Base）。

使用者可以透過網頁輸入自然語言問題，
系統讀取本地技術筆記，並透過本地 Ollama 模型產生回答。

第一階段以可運作的 MVP 為目標。

## Communication

- Communicate with the user in Traditional Chinese (繁體中文).
- Explanations, summaries, plans, and status updates should be written in Traditional Chinese.
- Code, filenames, commands, API names, variable names, and technical terms may remain in English when appropriate.
- Do not switch to English unless the user explicitly requests it.

## Tech Stack

- Python
- FastAPI
- HTML
- CSS
- JavaScript
- Ollama
- Markdown knowledge files

## Development Principles

- Keep the project simple.
- Keep the code beginner-readable.
- Prefer small and clear functions.
- Avoid unnecessary abstractions.
- Avoid unnecessary dependencies.
- Do not introduce complex frameworks unless requested.
- Explain important architectural decisions before making large changes.

## MVP Scope

The MVP should include:

- Simple Web UI
- Question input
- FastAPI backend
- Local Markdown knowledge files
- Ollama integration
- Answer generation
- Display the source of retrieved knowledge

## Out of Scope for MVP

Do not add these unless explicitly requested:

- Vector database
- User login
- Cloud deployment
- React / Vue / other frontend frameworks
- PostgreSQL / MySQL
- Docker
- Kubernetes
- Complex AI Agent systems

## Coding Style

- Use clear variable and function names.
- Prefer readable code over clever code.
- Keep files reasonably small.
- Add comments only when they improve understanding.
- Do not over-engineer.

## Change Policy

Before making large structural changes:

1. Explain what will change.
2. Explain why it is needed.
3. Keep changes focused on the current task.
4. Do not modify unrelated files.

## Git

- Keep commits focused.
- Use clear commit messages.
- Do not commit secrets, API keys, virtual environments, or generated files.
