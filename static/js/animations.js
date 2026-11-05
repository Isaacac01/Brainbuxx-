document.addEventListener('DOMContentLoaded', () => {
    const chatForm = document.getElementById('chatForm');
    const userInput = document.getElementById('userInput');
    const chatFeed = document.getElementById('chatFeed');
    const sendButton = document.getElementById('sendButton');
    const copyButton = document.getElementById('copyButton');
    const regenerateButton = document.getElementById('regenerateButton');
    const clearButton = document.getElementById('clearButton');

    window.BrainBuxxState = window.BrainBuxxState || { selectedConversation: null };

    function addUserMessage(text) {
        const row = document.createElement('div');
        row.className = 'message-row user';
        const bubble = document.createElement('div');
        bubble.className = 'message-bubble';
        bubble.textContent = text;
        row.appendChild(bubble);
        chatFeed.appendChild(row);
        chatFeed.scrollTop = chatFeed.scrollHeight;
    }

    function addAssistantLoading() {
        const row = document.createElement('div');
        row.className = 'message-row assistant';
        const bubble = document.createElement('div');
        bubble.className = 'message-bubble';
        const typing = document.createElement('div');
        typing.className = 'typing-indicator';
        typing.innerHTML = '<span></span><span></span><span></span>';
        bubble.appendChild(typing);
        row.appendChild(bubble);
        chatFeed.appendChild(row);
        chatFeed.scrollTop = chatFeed.scrollHeight;
        return bubble;
    }

    function typeWriter(element, text, speed = 18) {
        let index = 0;
        element.innerHTML = '';

        const render = () => {
            if (index <= text.length) {
                element.innerHTML = text.slice(0, index);
                index += 1;
                chatFeed.scrollTop = chatFeed.scrollHeight;
                setTimeout(render, speed);
            }
        };

        render();
    }

    async function sendMessage() {
        const message = (userInput.value || '').trim();
        if (!message || !chatFeed) return;

        addUserMessage(message);
        userInput.value = '';
        const assistantBubble = addAssistantLoading();

        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': document.body.dataset.csrf || '',
                },
                body: JSON.stringify({
                    message,
                    conversation_id: window.BrainBuxxState.selectedConversation,
                })
            });

            const data = await response.json();
            if (!response.ok) {
                assistantBubble.textContent = data.error || 'Something went wrong.';
                return;
            }

            window.BrainBuxxState.selectedConversation = data.conversation_id;
            typeWriter(assistantBubble, data.response || 'I’m here to help.');
            const historyEvent = new CustomEvent('conversationChanged');
            document.dispatchEvent(historyEvent);
            if (document.getElementById('searchInput')) {
                document.getElementById('searchInput').value = '';
            }
        } catch (error) {
            assistantBubble.textContent = 'Failed to connect to BrainBuxx. Please try again.';
        }
    }

    if (chatForm) {
        chatForm.addEventListener('submit', (event) => {
            event.preventDefault();
            sendMessage();
        });
    }

    if (sendButton) {
        sendButton.addEventListener('click', sendMessage);
    }

    if (copyButton) {
        copyButton.addEventListener('click', async () => {
            const lastAssistant = document.querySelector('.message-row.assistant .message-bubble:last-child');
            if (!lastAssistant) return;
            await navigator.clipboard.writeText(lastAssistant.innerText.trim());
        });
    }

    if (regenerateButton) {
        regenerateButton.addEventListener('click', () => {
            userInput.focus();
        });
    }

    if (clearButton) {
        clearButton.addEventListener('click', () => {
            if (chatFeed) chatFeed.innerHTML = '';
        });
    }

    userInput?.addEventListener('keydown', (event) => {
        if (event.key === 'Enter' && !event.shiftKey) {
            event.preventDefault();
            sendMessage();
        }
    });
});
