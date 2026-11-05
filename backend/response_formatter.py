import logging

logger = logging.getLogger(__name__)

try:
    import google.generativeai as genai
except ImportError:  # pragma: no cover
    genai = None


class GeminiClient:
    def __init__(self, api_key: str = "", model_name: str = "gemini-1.5-flash"):
        self.api_key = api_key
        self.model_name = model_name
        self.model = None

        if self.api_key and genai is not None:
            try:
                genai.configure(api_key=self.api_key)
                self.model = genai.GenerativeModel(self.model_name)
            except Exception as exc:  # pragma: no cover
                logger.warning("Gemini configuration failed: %s", exc)

    def _fallback_response(self, prompt: str) -> str:
        lower = prompt.lower()
        if "code" in lower or "python" in lower:
            return "Here is a practical approach: break the task into inputs, logic, and output, then test each step before combining them into the final solution."
        if "math" in lower or any(token in lower for token in ["calculate", "solve", "equation"]):
            return "Use a step-by-step method: define what is given, choose the correct formula, substitute values carefully, then verify the result before presenting the final answer."
        if "story" in lower or "creative" in lower:
            return "A strong creative response needs tension, character motivation, and a meaningful turning point. Build the scene, intensify the conflict, and resolve it with a satisfying emotional payoff."
        return "BrainBuxx is ready to help. Tell me your goal, question, or challenge, and I will break it into practical, clear steps with a useful answer."

    def generate_response(self, prompt: str, context=None) -> str:
        if not self.api_key or self.model is None:
            return self._fallback_response(prompt)

        try:
            response = self.model.generate_content(
                prompt,
                generation_config={
                    "temperature": 0.7,
                    "top_p": 0.9,
                    "top_k": 40,
                    "max_output_tokens": 600,
                },
            )
            text = getattr(response, "text", None)
            if text:
                return text.strip()
            return str(response)
        except Exception as exc:  # pragma: no cover
            logger.warning("Gemini call failed: %s", exc)
            return self._fallback_response(prompt)
