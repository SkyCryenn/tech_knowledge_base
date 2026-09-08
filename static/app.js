const form = document.querySelector("#question-form");
const questionInput = document.querySelector("#question");
const status = document.querySelector("#status");
const submitButton = form.querySelector("button");
const answerSection = document.querySelector("#answer-section");
const answer = document.querySelector("#answer");
let isLoading = false;

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  if (isLoading) return;

  const question = questionInput.value.trim();
  if (!question) {
    status.textContent = "請先輸入問題。";
    questionInput.focus();
    return;
  }

  isLoading = true;
  submitButton.disabled = true;
  questionInput.disabled = true;
  submitButton.textContent = "回答中…";
  form.setAttribute("aria-busy", "true");
  status.textContent = "正在等待本機 Ollama 回答，首次載入模型可能需要較久時間…";
  status.classList.remove("error");
  answerSection.hidden = true;
  answer.textContent = "";

  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 150000);
  try {
    const response = await fetch("/api/ask", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question }),
      signal: controller.signal,
    });
    let data;
    try {
      data = await response.json();
    } catch {
      throw new Error("伺服器回傳的格式不正確，請確認 FastAPI 正常運行後重試。");
    }
    if (!response.ok) {
      throw new Error(
        typeof data?.detail === "string" ? data.detail : "問題格式不正確或服務暫時無法處理，請重試。"
      );
    }
    if (typeof data?.answer !== "string" || !data.answer.trim()) {
      throw new Error("未收到有效回答，請重試。");
    }
    answer.textContent = data.answer;
    answerSection.hidden = false;
    status.textContent = "回答完成。";
  } catch (error) {
    status.classList.add("error");
    if (error.name === "AbortError") {
      status.textContent = "等待回答逾時，請稍後重試或改用較小的模型。";
    } else if (error instanceof TypeError) {
      status.textContent = "無法連線至網頁後端，請確認 FastAPI 已啟動後重試。";
    } else {
      status.textContent = error.message;
    }
  } finally {
    clearTimeout(timeout);
    isLoading = false;
    submitButton.disabled = false;
    questionInput.disabled = false;
    submitButton.textContent = "送出問題";
    form.setAttribute("aria-busy", "false");
  }
});

questionInput.addEventListener("input", () => {
  status.textContent = "";
  status.classList.remove("error");
});
