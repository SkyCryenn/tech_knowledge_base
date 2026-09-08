import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import main
from knowledge_search import CHUNK_SIZE, MAX_CHUNKS, find_context


class KnowledgeTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.directory = Path(self.temp.name)

    def test_chinese_english_ranking_and_reload(self):
        note = self.directory / "note.md"
        note.write_text("Python 有很多用途。\n\nPython 虛擬環境隔離套件。", encoding="utf-8")
        self.assertTrue(find_context("Python 虛擬環境", self.directory).startswith("Python 虛擬環境"))
        self.assertIn("隔離套件", find_context("虛擬環境", self.directory))
        note.write_text("Python 虛擬環境更新內容。", encoding="utf-8")
        self.assertIn("更新內容", find_context("PYTHON", self.directory))

    def test_missing_empty_unrelated_and_invalid_files(self):
        self.assertEqual(find_context("DNS", self.directory / "missing"), "")
        self.assertEqual(find_context("DNS", self.directory), "")
        (self.directory / "empty.md").write_text("")
        (self.directory / "ignore.txt").write_text("DNS")
        (self.directory / "broken.md").write_bytes(b"\xff")
        (self.directory / "note.md").write_text("Python list", encoding="utf-8")
        with self.assertLogs("knowledge_search", level="WARNING"):
            self.assertEqual(find_context("DNS", self.directory), "")

    def test_nested_notes_and_context_limit(self):
        nested = self.directory / "python"
        nested.mkdir()
        (nested / "notes.MD").write_text(("Python " * 600 + "\n\n") * 4)
        context = find_context("python", self.directory)
        self.assertIn("Python", context)
        self.assertLessEqual(len(context), CHUNK_SIZE * MAX_CHUNKS + 7 * (MAX_CHUNKS - 1))

    def test_reference_reaches_ollama_without_source_fields(self):
        (self.directory / "note.md").write_text("Maple 使用連接埠 8765。", encoding="utf-8")
        for question, expected in [("Maple 的連接埠？", "8765"), ("DNS 是什麼？", None)]:
            with self.subTest(question=question):
                with patch("main.find_context", side_effect=lambda q: find_context(q, self.directory)):
                    with patch("main.urlopen", return_value=io.BytesIO(b'{"response":"ok"}')) as request:
                        result = main.ask_question(main.QuestionRequest(question=question, model="qwen3:4b"))
                payload = json.loads(request.call_args.args[0].data)
                self.assertEqual(payload["model"], "qwen3:4b")
                self.assertEqual(set(result), {"answer", "model"})
                if expected:
                    self.assertIn(expected, payload["prompt"])
                    self.assertIn(question, payload["prompt"])
                else:
                    self.assertEqual(payload["prompt"], question)


if __name__ == "__main__":
    unittest.main()
