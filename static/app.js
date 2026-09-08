const form = document.querySelector("#question-form");
const questionInput = document.querySelector("#question");
const status = document.querySelector("#status");

form.addEventListener("submit", (event) => {
  event.preventDefault();

  if (!questionInput.value.trim()) {
    status.textContent = "請先輸入問題。";
    questionInput.focus();
    return;
  }

  status.textContent = "v0.1 尚未提供回答功能。你的問題未傳送或儲存。";
});

questionInput.addEventListener("input", () => {
  status.textContent = "";
});
