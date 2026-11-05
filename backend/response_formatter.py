import logging
from typing import Optional

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
        prompt_lower = prompt.lower()
        if "code" in prompt_lower or "python" in prompt_lower:
            return "Here is a practical approach: break the problem into inputs, logic, and outputs. Write small functions, test each step, and verify edge cases before finalizing the solution."
        if "math" in prompt_lower or any(token in prompt_lower for token in ["calculate", "solve", "equation"]):
            return "Use a clear step-by-step method: identify the known values, determine the formula, substitute the values, and verify the result before presenting the final answer."
        if "story" in prompt_lower or "creative" in prompt_lower:
            return "A strong story begins with a compelling desire, an obstacle, and a turning point. Build tension carefully, let the character change, and end with a satisfying emotional resolution."
        return "BrainBuxx is ready to help. I can assist with learning, analysis, writing, planning, coding, and creative ideation. Share your goal and I will break it down into practical next steps."

    def generate_response(self, prompt: str, context: Optional[list] = None) -> str:
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
                request_options={"timeout": 30},
            )
            text = getattr(response, "text", None)
            if text:
                return text.strip()
            return str(response)
        except Exception as exc:  # pragma: no cover
            logger.warning("Gemini call failed: %s", exc)
            return self._fallback_response(prompt)
