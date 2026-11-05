import re
from typing import Dict


class RasaClient:
    def __init__(self, enabled: bool = False):
        self.enabled = enabled

    def classify_intent(self, message: str) -> Dict[str, object]:
        text = message.lower().strip()

        intents = {
            "greeting": ["hello", "hi", "hey", "good morning", "good evening"],
            "general_knowledge": ["what is", "who is", "why does", "how does"],
            "education": ["teach me", "explain", "learn", "study"],
            "math": ["solve", "calculate", "equation", "sum", "factor", "derivative"],
            "science": ["science", "physics", "chemistry", "biology", "astronomy"],
            "coding": ["code", "python", "javascript", "debug", "function", "api", "algorithm"],
            "business": ["strategy", "business", "marketing", "productivity", "plan"],
            "creative": ["write", "story", "poem", "creative", "brainstorm"],
            "follow_up": ["what about", "continue", "more on", "tell me more"],
        }

        for intent, keywords in intents.items():
            if any(keyword in text for keyword in keywords):
                confidence = 0.82 if intent == "greeting" else 0.75
                return {"intent": intent, "confidence": confidence, "entities": []}

        if re.search(r"[0-9]", text):
            return {"intent": "math", "confidence": 0.6, "entities": []}

        return {"intent": "unknown", "confidence": 0.18, "entities": []}

    def generate_response(self, message: str) -> Dict[str, object]:
        if not self.enabled:
            return {"intent": "fallback", "response": "Rasa is offline in this session."}
        return {"intent": "fallback", "response": f"Rasa handled: {message}"}
