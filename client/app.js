const API_BASE_URL = "http://localhost:8000";
const messagesEl = document.querySelector("#messages");
const formEl = document.querySelector("#chat-form");
const inputEl = document.querySelector("#message-input");
const sendButtonEl = document.querySelector("#send-button");
const statusEl = document.querySelector("#status");
const newChatEl = document.querySelector("#new-chat");

function getSessionId() {
  let sessionId = localStorage.getItem("ragSessionId");
  if (!sessionId) {
    sessionId = crypto.randomUUID();
    localStorage.setItem("ragSessionId", sessionId);
  }
  return sessionId;
}

function appendMessage(role, text) {
  const item = document.createElement("article");
  item.className = `message ${role}`;

  const bubble = document.createElement("div");
  bubble.className = "bubble";
  bubble.textContent = text;

  item.appendChild(bubble);
  messagesEl.appendChild(item);
  messagesEl.scrollTop = messagesEl.scrollHeight;
}

function setLoading(isLoading) {
  sendButtonEl.disabled = isLoading;
  inputEl.disabled = isLoading;
  statusEl.textContent = isLoading ? "Searching knowledge base..." : "";
}

function resizeInput() {
  inputEl.style.height = "auto";
  inputEl.style.height = `${inputEl.scrollHeight}px`;
}

inputEl.addEventListener("input", resizeInput);

formEl.addEventListener("submit", async (event) => {
  event.preventDefault();
  const message = inputEl.value.trim();
  if (!message) return;

  appendMessage("user", message);
  inputEl.value = "";
  resizeInput();
  setLoading(true);

  try {
    const response = await fetch(`${API_BASE_URL}/api/chat`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        sessionId: getSessionId(),
        message,
      }),
    });

    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.detail || data.error || "Request failed");
    }

    appendMessage("assistant", data.reply);
  } catch (error) {
    appendMessage("assistant", `Error: ${error.message}`);
  } finally {
    setLoading(false);
    inputEl.focus();
  }
});

newChatEl.addEventListener("click", () => {
  localStorage.removeItem("ragSessionId");
  getSessionId();
  messagesEl.innerHTML = "";
  appendMessage(
    "assistant",
    "New chat started. Ask me about the knowledge base."
  );
  inputEl.focus();
});

getSessionId();
