document.addEventListener("DOMContentLoaded", () => {
    const chatBox = document.getElementById("chat-box");
    const userInput = document.getElementById("user-input");
    const sendButton = document.getElementById("send-button");
    const voiceButton = document.getElementById("voice-button");

    // Speech Recognition Setup
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

    if (!SpeechRecognition) {
        alert("Speech recognition is not supported in this browser. Please use Chrome or Edge.");
        voiceButton.disabled = true; // Disable the voice button if unsupported
        return;
    }

    const recognition = new SpeechRecognition();
    recognition.lang = "en-US";
    recognition.interimResults = false; // Use final results only
    let isProcessing = false; // Prevent duplicate queries

    // Start speech recognition when the voice button is clicked
    voiceButton.addEventListener("click", () => {
        if (isProcessing) return; // Prevent re-triggering if already processing
        appendMessage("System", "Listening...", "bot");
        recognition.start();
    });

    // Capture speech-to-text results
    recognition.onresult = (event) => {
        if (isProcessing) return; // Prevent duplicate queries
        isProcessing = true;

        const transcript = event.results[0][0].transcript;
        userInput.value = transcript; // Autofill the input field with recognized speech
        appendMessage("You", transcript, "user");
        sendQuery(); // Automatically send the query after recognition
    };

    // Reset processing state when recognition ends
    recognition.onend = () => {
        isProcessing = false; // Allow recognition to start again
        appendMessage("System", "Speech recognition ended.", "bot");
    };

    // Handle speech recognition errors
    recognition.onerror = (event) => {
        isProcessing = false; // Reset processing state on error
        appendMessage("System", "Speech recognition error: " + event.error, "bot");
    };

    // Handle the "Send" button click
    sendButton.addEventListener("click", sendQuery);

    // Function to send the query to the backend
    async function sendQuery() {
        const query = userInput.value.trim();
        if (!query) return;

        // Display user message
        appendMessage("You", query, "user");
        userInput.value = "";

        // Send query to server
        try {
            const response = await fetch("/chat", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ query }),
            });
            const data = await response.json();

            // Display bot response
            if (data.response) {
                appendMessage("Bot", data.response, "bot");
                speakResponse(data.response); // Use text-to-speech for the response
            } else {
                appendMessage("Bot", "Sorry, I couldn’t process that.", "bot");
            }
        } catch (error) {
            appendMessage("Bot", "An error occurred. Please try again later.", "bot");
        }
    }

    // Function to display messages in the chat box
    function appendMessage(sender, message, className) {
        const messageElement = document.createElement("p");
        messageElement.className = className;
        messageElement.innerHTML = `<strong>${sender}:</strong> ${message}`;
        chatBox.appendChild(messageElement);
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    // Text-to-Speech for bot responses
    function speakResponse(text) {
        const speech = new SpeechSynthesisUtterance(text);
        speech.lang = "en-US";
        speech.rate = 1; // Adjust the rate for natural speech
        window.speechSynthesis.speak(speech);
    }
});