document.addEventListener('DOMContentLoaded', () => {
    const searchInput = document.querySelector('.search-input');
    const list = document.querySelector('.history-list');
    const newChatButton = document.querySelector('.new-chat-btn');
    const chatFeed = document.getElementById('chatFeed');

    async function fetchConversations() {
        const response = await fetch('/api/conversations', { headers: { 'X-CSRFToken': document.body.dataset.csrf || '' } });
        const data = await response.json();
        renderHistory(data);
    }

    function renderHistory(items) {
        if (!list) return;
        list.innerHTML = '';

        if (!items.length) {
            list.innerHTML = '<li class="history-item"><span>No conversations yet</span></li>';
            return;
        }

        items.forEach((item) => {
            const li = document.createElement('li');
            li.className = 'history-item';
            li.innerHTML = `<span data-id="${item.id}">${item.title}</span><button data-delete="${item.id}">✕</button>`;
            li.addEventListener('click', (event) => {
                if (event.target.matches('button')) return;
                loadConversation(item.id);
            });
            list.appendChild(li);
        });
    }

    async function loadConversation(id) {
        const response = await fetch(`/api/conversations/${id}`);
        const data = await response.json();
        if (!data.messages) return;

        if (chatFeed) {
            chatFeed.innerHTML = '';
            data.messages.forEach((msg) => {
                const row = document.createElement('div');
                row.className = `message-row ${msg.role === 'assistant' ? 'assistant' : 'user'}`;
                const bubble = document.createElement('div');
                bubble.className = 'message-bubble';
                bubble.innerHTML = msg.content;
                row.appendChild(bubble);
                chatFeed.appendChild(row);
            });
        }

        window.BrainBuxxState.selectedConversation = id;
        const active = document.querySelectorAll('.history-item');
        active.forEach((i) => i.classList.remove('active'));
        const item = [...document.querySelectorAll('.history-item span')].find((span) => Number(span.dataset.id) === id)?.closest('.history-item');
        if (item) item.classList.add('active');
    }

    if (searchInput) {
        searchInput.addEventListener('input', async (e) => {
            const q = e.target.value.trim();
            if (!q) {
                fetchConversations();
                return;
            }
            const response = await fetch(`/api/conversations/search?q=${encodeURIComponent(q)}`);
            const data = await response.json();
            renderHistory(data);
        });
    }

    if (newChatButton) {
        newChatButton.addEventListener('click', async () => {
            const response = await fetch('/api/conversations', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json', 'X-CSRFToken': document.body.dataset.csrf || '' }
            });
            const data = await response.json();
            window.BrainBuxxState.selectedConversation = data.id;
            if (chatFeed) chatFeed.innerHTML = '';
            await fetchConversations();
        });
    }

    document.addEventListener('click', async (event) => {
        const deleteButton = event.target.closest('[data-delete]');
        if (!deleteButton) return;
        const id = Number(deleteButton.dataset.delete);
        const response = await fetch(`/api/conversations/${id}`, {
            method: 'DELETE',
            headers: { 'X-CSRFToken': document.body.dataset.csrf || '' }
        });
        if (response.ok) {
            fetchConversations();
            if (window.BrainBuxxState.selectedConversation === id) {
                window.BrainBuxxState.selectedConversation = null;
                if (chatFeed) chatFeed.innerHTML = '';
            }
        }
    });

    fetchConversations();
});
