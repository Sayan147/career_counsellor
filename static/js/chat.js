const chatMessages = document.getElementById('chatMessages');
const messageInput = document.getElementById('messageInput');
const sendButton = document.getElementById('sendMessage');

// Get base API URL from current hostname
const apiBaseUrl = `${window.location.protocol}//${window.location.host}`;

// Load chat history
async function loadChatHistory() {
    try {
        const response = await fetch(`${apiBaseUrl}/career/chat-history`, {
            headers: {
                'Cache-Control': 'no-cache, no-store, must-revalidate',
                'Pragma': 'no-cache',
                'Expires': '0'
            },
            credentials: 'include'
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const history = await response.json();
        
        history.forEach(msg => {
            appendMessage(msg.message, true);
            appendMessage(msg.response, false);
        });
        
        scrollToBottom();
    } catch (error) {
        console.error('Error loading chat history:', error);
        appendMessage('Error loading chat history. Please refresh the page.', false);
    }
}

// Send message
async function sendMessage() {
    const message = messageInput.value.trim();
    if (!message) return;

    appendMessage(message, true);
    messageInput.value = '';
    scrollToBottom();

    try {
        const response = await fetch(`${apiBaseUrl}/career/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Cache-Control': 'no-cache, no-store, must-revalidate',
                'Pragma': 'no-cache',
                'Expires': '0'
            },
            body: JSON.stringify({ message }),
            credentials: 'include'
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        appendMessage(data.response, false);
    } catch (error) {
        console.error('Error sending message:', error);
        appendMessage('Sorry, there was an error processing your message. Please try again.', false);
    }

    scrollToBottom();
}

// Append message to chat
function appendMessage(text, isUser) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${isUser ? 'user' : 'bot'}`;
    
    if (isUser) {
        messageDiv.textContent = text;
    } else {
        // Use marked.js to render markdown for bot messages
        messageDiv.innerHTML = marked.parse(text);
    }
    
    chatMessages.appendChild(messageDiv);
}

// Scroll to bottom of chat
function scrollToBottom() {
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Event listeners
sendButton.addEventListener('click', sendMessage);

messageInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});

// Load chat history on page load
loadChatHistory(); 