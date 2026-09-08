import io
import json
import unittest
from unittest.mock import patch
from urllib.error import HTTPError, URLError

from fastapi import HTTPException
from pydantic import ValidationError

import main


class AskQuestionTests(unittest.TestCase):
    def setUp(self):
        search = patch("main.find_context", return_value="")
        search.start()
        self.addCleanup(search.stop)

    def test_model_is_per_request_and_defaults_when_empty(self):
        models = ["gemma4:latest", "qwen3:4b", "gemma3:latest", None, "", "   "]
        for model in models:
            with self.subTest(model=model):
                response = io.BytesIO(b'{"response": "ok"}')
                with patch("main.urlopen", return_value=response) as open_request:
                    result = main.ask_question(main.QuestionRequest(question="test", model=model))
                expected = (model or "").strip() or "gemma3:latest"
                self.assertEqual(json.loads(open_request.call_args.args[0].data)["model"], expected)
                self.assertEqual(result["model"], expected)
                self.assertEqual(main.DEFAULT_MODEL, "gemma3:latest")

    def test_missing_model_error_names_requested_model(self):
        error = HTTPError(main.OLLAMA_URL, 404, "missing", {}, None)
        with patch("main.urlopen", side_effect=error):
            with self.assertRaises(HTTPException) as caught:
                main.ask_question(main.QuestionRequest(question="test", model="missing-model"))
        self.assertIn("missing-model", caught.exception.detail)
        self.assertIn("下拉選單", caught.exception.detail)

    def test_success_sends_prompt_and_returns_answer(self):
        response = io.BytesIO(json.dumps({"response": "  測試回答  "}).encode())
        with patch("main.urlopen", return_value=response) as open_request:
            result = main.ask_question(main.QuestionRequest(question="  測試問題  "))
        self.assertEqual(result, {"answer": "測試回答", "model": "gemma3:latest"})
        request = open_request.call_args.args[0]
        payload = json.loads(request.data)
        self.assertEqual(request.full_url, "http://127.0.0.1:11434/api/generate")
        self.assertEqual(request.method, "POST")
        self.assertEqual(payload["prompt"], "測試問題")
        self.assertEqual(payload["model"], main.DEFAULT_MODEL)
        self.assertIs(payload["stream"], False)
        self.assertEqual(open_request.call_args.kwargs["timeout"], 120)

    def test_whitespace_rejected_without_calling_ollama(self):
        with patch("main.urlopen") as open_request:
            with self.assertRaises(HTTPException) as caught:
                main.ask_question(main.QuestionRequest(question=" \n "))
        self.assertEqual(caught.exception.status_code, 400)
        open_request.assert_not_called()

    def test_invalid_inputs(self):
        for question in ("", 123, None, "a" * 10001):
            with self.subTest(question_type=type(question).__name__):
                with self.assertRaises(ValidationError):
                    main.QuestionRequest(question=question)

    def test_connection_and_model_errors(self):
        cases = [
            (URLError("connection refused"), 503, "ollama serve"),
            (ConnectionResetError(), 503, "連線中斷"),
            (TimeoutError(), 504, "逾時"),
            (URLError(TimeoutError()), 504, "逾時"),
            (HTTPError(main.OLLAMA_URL, 404, "missing", {}, None), 502, "ollama pull"),
            (HTTPError(main.OLLAMA_URL, 500, "failed", {}, None), 502, "模型"),
        ]
        for error, status_code, message in cases:
            with self.subTest(error=repr(error)):
                with patch("main.urlopen", side_effect=error):
                    with self.assertRaises(HTTPException) as caught:
                        main.generate_answer("測試")
                self.assertEqual(caught.exception.status_code, status_code)
                self.assertIn(message, caught.exception.detail)

    def test_invalid_ollama_responses(self):
        for body in (b"not json", b"[]", b"{}", b'{"response": " "}',
                     b'{"response": 123}', b'{"error": "failed"}'):
            with self.subTest(body=body):
                with patch("main.urlopen", return_value=io.BytesIO(body)):
                    with self.assertRaises(HTTPException) as caught:
                        main.generate_answer("測試")
                self.assertEqual(caught.exception.status_code, 502)


if __name__ == "__main__":
    unittest.main()
