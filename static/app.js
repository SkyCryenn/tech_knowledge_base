const form = document.querySelector("#question-form");
const questionInput = document.querySelector("#question");
const status = document.querySelector("#status");
const submitButton = form.querySelector("button");
const answerSection = document.querySelector("#answer-section");
const answer = document.querySelector("#answer");
const modelSelect = document.querySelector("#model");
const currentModel = document.querySelector("#current-model");
const answerModel = document.querySelector("#answer-model");
const answerSources = document.querySelector("#answer-sources");
const elapsed = document.querySelector("#elapsed");
let isLoading = false;

modelSelect.addEventListener("change", () => {
  currentModel.textContent = `目前選擇的模型：${modelSelect.value || "gemma3:latest"}`;
});

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  if (isLoading) return;

  const question = questionInput.value.trim();
  if (!question) {
    status.textContent = "請先輸入問題。";
    questionInput.focus();
    return;
  }

  const model = modelSelect.value || "gemma3:latest";
  const startedAt = performance.now();
  const updateElapsed = () => {
    elapsed.textContent = `處理時間：${((performance.now() - startedAt) / 1000).toFixed(1)} 秒`;
  };
  updateElapsed();
  const elapsedTimer = setInterval(updateElapsed, 100);
  modelSelect.disabled = true;
  isLoading = true;
  submitButton.disabled = true;
  questionInput.disabled = true;
  submitButton.textContent = "回答中…";
  form.setAttribute("aria-busy", "true");
  status.textContent = "正在等待本機 Ollama 回答，首次載入模型可能需要較久時間…";
  status.classList.remove("error");
  answerSection.hidden = true;
  answer.textContent = "";
  answerSources.textContent = "";

  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 150000);
  try {
    const response = await fetch("/api/ask", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question, model }),
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
    answerModel.textContent = `回答使用的模型：${data.model}`;
    const sources = Array.isArray(data.sources) ? [...new Set(data.sources)] : [];
    for (const source of sources.length ? sources : ["無本地筆記"]) {
      const item = document.createElement("li");
      item.textContent = source;
      answerSources.appendChild(item);
    }
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
    clearInterval(elapsedTimer);
    updateElapsed();
    modelSelect.disabled = false;
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
