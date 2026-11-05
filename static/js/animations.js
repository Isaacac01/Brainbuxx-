document.addEventListener('DOMContentLoaded', () => {
    const chatForm = document.getElementById('chatForm');
    const userInput = document.getElementById('userInput');
    const chatFeed = document.getElementById('chatFeed');
    const sendButton = document.getElementById('sendButton');
    const regenerateButton = document.getElementById('regenerateButton');
    const copyButton = document.getElementById('copyButton');
    const clearButton = document.getElementById('clearButton');

    window.BrainBuxxState = window.BrainBuxxState || { selectedConversation: null };

    function addMessage(role, text) {
        const row = document.createElement('div');
        row.className = `message-row ${role}`;
        const bubble = document.createElement('div');
        bubble.className = 'message-bubble';

        if (role === 'assistant') {
            const typing = document.createElement('div');
            typing.className = 'typing-indicator';
            typing.innerHTML = '<span></span><span></span><span></span>';
            bubble.appendChild(typing);
            row.appendChild(bubble);
            chatFeed.appendChild(row);
            chatFeed.scrollTop = chatFeed.scrollHeight;
            return bubble;
        }

        bubble.innerHTML = text;
        row.appendChild(bubble);
        chatFeed.appendChild(row);
        chatFeed.scrollTop = chatFeed.scrollHeight;
        return bubble;
    }

    function typeWriter(element, text, speed = 16) {
        let index = 0;
        element.innerHTML = '';

        const tick = () => {
            if (index <= text.length) {
                element.innerHTML = text.slice(0, index);
                index += 1;
                chatFeed.scrollTop = chatFeed.scrollHeight;
                setTimeout(tick, speed);
            }
        };

        tick();
    }

    async function sendMessage() {
        const message = (userInput.value || '').trim();
        if (!message || !chatFeed) return;

        addMessage('user', message);
        userInput.value = '';
        const bubble = addMessage('assistant', '');
        bubble.classList.add('assistant-loading');

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
                bubble.textContent = data.error || 'Something went wrong.';
                return;
            }

            window.BrainBuxxState.selectedConversation = data.conversation_id;
            const rendered = data.response || 'I’m here to help.';
            bubble.innerHTML = '';
            typeWriter(bubble, rendered);
            const event = new CustomEvent('conversationChanged', { detail: { conversationId: data.conversation_id } });
            document.dispatchEvent(event);
        } catch (error) {
            bubble.textContent = 'Failed to connect to BrainBuxx. Please try again.';
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

    if (clearButton) {
        clearButton.addEventListener('click', () => {
            if (chatFeed) chatFeed.innerHTML = '';
        });
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
            if (userInput) {
                userInput.focus();
            }
        });
    }

    userInput?.addEventListener('keydown', (event) => {
        if (event.key === 'Enter' && !event.shiftKey) {
            event.preventDefault();
            sendMessage();
        }
    });
});
