document.addEventListener('DOMContentLoaded', () => {
    const sidebar = document.querySelector('.sidebar');
    const menuToggle = document.getElementById('sidebarToggle');

    if (menuToggle && sidebar) {
        menuToggle.addEventListener('click', () => {
            sidebar.classList.toggle('open');
        });
    }

    const loginForm = document.querySelector('.auth-form');
    if (loginForm) {
        const message = document.querySelector('.flash-message.error');
        if (message) {
            message.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        }
    }
});
