document.addEventListener('DOMContentLoaded', () => {
    const urlInput = document.getElementById("urlInput");
    const analyzeButton = document.getElementById("analyzeButton");
    const chatSection = document.getElementById("chatSection");
    const chatInput = document.getElementById("chatInput");
    const sendButton = document.getElementById("sendButton");
    const loading = document.getElementById("loading");
    const errorMessage = document.getElementById("errorMessage");
    const chatWindow = document.getElementById("chatWindow");

    // Repository Analyze
    analyzeButton.addEventListener("click", async () => {
        const url = urlInput.value.trim();
        if (!url) {
            showError("Please enter a GitHub repository URL.");
            return;
        }

        loading.classList.remove("hidden");
        errorMessage.classList.add("hidden");

        try {
            const response = await fetch("/chatbot", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ url: url })
            });

            const data = await response.json();
            loading.classList.add("hidden");

            if (response.ok) {
                chatSection.classList.remove("hidden");
            } else {
                showError(data.error || "Something went wrong.");
            }
        } catch (error) {
            showError("Could not connect to server.");
            loading.classList.add("hidden");
        }
    });

    // Send Chat Message
    sendButton.addEventListener("click", sendMessage);
    chatInput.addEventListener("keypress", e => {
        if (e.key === "Enter") sendMessage();
    });

    async function sendMessage() {
        const msg = chatInput.value.trim();
        if (!msg) return;

        appendChat("You", msg);
        chatInput.value = "";

        try {
            const response = await fetch("/get", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ msg: msg })
            });

            const data = await response.json();
            appendChat("Bot", data.answer || data.error || "No response");
        } catch (error) {
            appendChat("Bot", "Error: Could not connect to the server.");
        }
    }

    function appendChat(sender, message) {
        const msgEl = document.createElement("div");
        msgEl.innerHTML = `<strong>${sender}:</strong> ${message}`;
        chatWindow.appendChild(msgEl);
        chatWindow.scrollTop = chatWindow.scrollHeight;
    }

    function showError(msg) {
        errorMessage.textContent = msg;
        errorMessage.classList.remove("hidden");
    }
});
