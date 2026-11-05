.launch-screen {
    position: fixed;
    inset: 0;
    display: grid;
    place-items: center;
    background: radial-gradient(circle at top, rgba(85,181,255,0.2), rgba(6, 17, 28, 0.95) 38%, rgba(3, 12, 20, 0.98));
    z-index: 30;
    opacity: 1;
    transition: opacity 1.2s ease, visibility 1.2s ease;
}

.launch-screen.hidden {
    opacity: 0;
    visibility: hidden;
    pointer-events: none;
}

.launch-content {
    text-align: center;
    display: grid;
    gap: 0.8rem;
}

.launch-brand {
    font-size: clamp(2rem, 4vw, 3.8rem);
    letter-spacing: 0.22rem;
    font-weight: 700;
    color: #eef6ff;
    text-shadow: 0 0 16px rgba(93, 177, 255, 0.55);
    opacity: 0;
    animation: fadeUp 1s ease forwards 0.35s;
}

.launch-name {
    display: inline-flex;
    gap: 0.08em;
    font-size: clamp(2.2rem, 4.5vw, 4.2rem);
    font-weight: 700;
    letter-spacing: 0.06em;
    color: #edf7ff;
    text-shadow: 0 0 18px rgba(93, 177, 255, 0.6);
    min-height: 1.2em;
}

.launch-name .letter {
    opacity: 0;
    transform: translateY(10px);
    animation: revealLetter 0.7s ease forwards;
}

.launch-subtitle {
    font-size: clamp(1rem, 2vw, 1.5rem);
    color: rgba(237, 246, 255, 0.78);
    opacity: 0;
    animation: fadeUp 1.2s ease forwards 2.3s;
    min-height: 1.5em;
}

.launch-tagline {
    color: rgba(219, 239, 255, 0.74);
    font-style: italic;
    opacity: 0;
    animation: fadeUp 1.2s ease forwards 2.7s;
}

@keyframes revealLetter {
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@keyframes fadeUp {
    from {
        opacity: 0;
        transform: translateY(16px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}
