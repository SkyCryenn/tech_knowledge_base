import logging
import re
from pathlib import Path


KNOWLEDGE_DIR = Path(__file__).resolve().parent / "knowledge"
CHUNK_SIZE = 2000
MAX_CHUNKS = 3
STOP_WORDS = {"the", "a", "an", "is", "of", "to", "and", "what", "how",
              "請問", "請用", "如何", "什麼", "甚麼", "說明", "可以", "一個", "繁體", "中文"}
logger = logging.getLogger(__name__)


def search_terms(text: str) -> set[str]:
    terms = set(re.findall(r"[a-z0-9_]+", text.lower()))
    # 中文通常沒有空格，使用相鄰兩字作為簡單搜尋單位。
    for phrase in re.findall(r"[\u4e00-\u9fff]+", text):
        terms.update(phrase[index:index + 2] for index in range(len(phrase) - 1))
    return terms - STOP_WORDS


def find_context(
    question: str,
    directory: Path = KNOWLEDGE_DIR,
    *,
    include_sources: bool = False,
) -> str | list[dict[str, str]]:
    """預設回傳 context 文字；include_sources=True 時回傳各段內容與來源。"""
    terms = search_terms(question)
    if not terms or not directory.is_dir():
        return [] if include_sources else ""

    ranked_chunks = []
    for path in sorted(directory.rglob("*")):
        if path.suffix.lower() != ".md" or not path.is_file():
            continue
        # 不讀取以符號連結指向 knowledge/ 外部的檔案。
        if not path.resolve().is_relative_to(directory.resolve()):
            continue
        try:
            content = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError):
            logger.warning("略過無法讀取的 Markdown：%s", path.name)
            continue
        for paragraph in re.split(r"\n\s*\n", content):
            for start in range(0, len(paragraph), CHUNK_SIZE):
                chunk = paragraph[start:start + CHUNK_SIZE].strip()
                score = len(terms & search_terms(chunk))
                if score:
                    ranked_chunks.append((score, {
                        "content": chunk,
                        "source": path.relative_to(directory).as_posix(),
                    }))

    ranked_chunks.sort(key=lambda item: item[0], reverse=True)
    chunks = [chunk for _, chunk in ranked_chunks[:MAX_CHUNKS]]
    if include_sources:
        return chunks
    return "\n\n---\n\n".join(chunk["content"] for chunk in chunks)
