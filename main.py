import json
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field


BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"
OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
DEFAULT_MODEL = "gemma3:latest"
OLLAMA_TIMEOUT = 120

app = FastAPI(title="Tech Knowledge Base", version="0.2.1")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/", response_class=FileResponse)
def homepage():
    return FileResponse(STATIC_DIR / "index.html")


class QuestionRequest(BaseModel):
    question: str = Field(min_length=1, max_length=10000)
    model: str | None = Field(default=None, max_length=200)


def generate_answer(question: str, model: str = DEFAULT_MODEL) -> str:
    payload = {
        "model": model,
        "prompt": question,
        "system": "請使用繁體中文回答使用者的問題。",
        "stream": False,
    }
    request = Request(
        OLLAMA_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urlopen(request, timeout=OLLAMA_TIMEOUT) as response:
            result = json.load(response)
    except HTTPError as error:
        if error.code == 404:
            message = (
                f"找不到模型 {model}。請先執行 ollama pull {model}，"
                "或在下拉選單選擇已安裝的模型後重試。"
            )
        else:
            message = "Ollama 暫時無法產生回答，模型可能無法載入或記憶體不足。請檢查 Ollama 後重試。"
        raise HTTPException(status_code=502, detail=message) from error
    except TimeoutError as error:
        raise HTTPException(
            status_code=504, detail="等待 Ollama 回答逾時，請縮短問題或改用較小的模型後重試。"
        ) from error
    except URLError as error:
        if isinstance(error.reason, TimeoutError):
            raise HTTPException(
                status_code=504, detail="連線至 Ollama 逾時，請確認服務狀態後重試。"
            ) from error
        raise HTTPException(
            status_code=503,
            detail="無法連線至本機 Ollama。請開啟 Ollama App 或執行 ollama serve 後重試。",
        ) from error
    except (ValueError, UnicodeError) as error:
        raise HTTPException(status_code=502, detail="Ollama 回傳的格式不正確，請重試。") from error
    except OSError as error:
        raise HTTPException(status_code=503, detail="與 Ollama 的連線中斷，請確認服務仍在運行後重試。") from error

    answer = result.get("response") if isinstance(result, dict) else None
    if not isinstance(answer, str) or not answer.strip() or result.get("error"):
        raise HTTPException(status_code=502, detail="Ollama 未回傳有效回答，請確認模型可正常使用後重試。")
    return answer.strip()


@app.post("/api/ask")
def ask_question(body: QuestionRequest):
    question = body.question.strip()
    if not question:
        raise HTTPException(status_code=400, detail="請先輸入問題。")
    # 同步路由由 FastAPI 的執行緒池處理，避免等待 Ollama 時阻塞事件迴圈。
    model = (body.model or "").strip() or DEFAULT_MODEL
    return {"answer": generate_answer(question, model), "model": model}
