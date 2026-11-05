document.addEventListener('DOMContentLoaded', () => {
    const historyList = document.getElementById('historyList');
    const searchInput = document.getElementById('searchInput');
    const newChatButton = document.getElementById('newChatButton');

    async function fetchHistory() {
        if (!historyList) return;
        const response = await fetch('/api/conversations');
        const data = await response.json();
        renderHistory(data);
    }

    function renderHistory(items) {
        if (!historyList) return;
        historyList.innerHTML = '';

        if (!items.length) {
            historyList.innerHTML = '<li class="history-item"><span>No conversations yet</span></li>';
            return;
        }

        items.forEach((item) => {
            const li = document.createElement('li');
            li.className = 'history-item';
            if (window.BrainBuxxState && Number(window.BrainBuxxState.selectedConversation) === item.id) {
                li.classList.add('active');
            }

            li.innerHTML = `
                <span data-id="${item.id}">${item.title}</span>
                <button type="button" data-delete="${item.id}">✕</button>
            `;

            li.addEventListener('click', (event) => {
                if (event.target.closest('button')) return;
                loadConversation(item.id);
            });

            historyList.appendChild(li);
        });
    }

    async function loadConversation(id) {
        const response = await fetch(`/api/conversations/${id}`);
        const data = await response.json();
        if (!data.messages) return;

        const chatFeed = document.getElementById('chatFeed');
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
        renderHistory(await (await fetch('/api/conversations')).json());
    }

    if (searchInput) {
        searchInput.addEventListener('input', async (event) => {
            const query = event.target.value.trim();
            if (!query) {
                fetchHistory();
                return;
            }
            const response = await fetch(`/api/conversations/search?q=${encodeURIComponent(query)}`);
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
            const chatFeed = document.getElementById('chatFeed');
            if (chatFeed) chatFeed.innerHTML = '';
            await fetchHistory();
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
            if (window.BrainBuxxState.selectedConversation === id) {
                window.BrainBuxxState.selectedConversation = null;
            }
            fetchHistory();
        }
    });

    fetchHistory();
});
