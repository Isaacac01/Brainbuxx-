from config import Config
from backend.context_manager import ContextManager
from backend.gemini_client import GeminiClient
from backend.rasa_client import RasaClient


class AIEngine:
    def __init__(self, rasa_client=None, gemini_client=None, context_manager=None):
        self.rasa_client = rasa_client or RasaClient(enabled=Config.RASA_ENABLED)
        self.gemini_client = gemini_client or GeminiClient(
            api_key=Config.GEMINI_API_KEY,
            model_name=Config.GEMINI_MODEL,
        )
        self.context_manager = context_manager or ContextManager(max_turns=8)

    def process_message(self, user_message: str, conversation=None, history=None):
        intent = self.rasa_client.classify_intent(user_message)
        if history is None and conversation is not None:
            history = conversation.messages
        context = self.context_manager.build_context(history or [])

        system_prompt = (
            "You are BrainBuxx, an intelligent assistant developed by VHS Science and Innovation. "
            "Answer helpfully, clearly, and with practical, professional language. "
            "Maintain context and provide insightful responses."
        )

        prompt = (
            f"{system_prompt}\n\n"
            f"User intent: {intent.get('intent')}\n\n"
            f"Conversation context: {context}\n\n"
            f"User message: {user_message}\n\n"
            "Provide a concise, helpful response with markdown formatting when useful."
        )

        response = self.gemini_client.generate_response(prompt, context)
        return response, intent
