class ContextManager:
    def __init__(self, max_turns=8):
        self.max_turns = max_turns

    def build_context(self, messages):
        recent = list(messages)[-self.max_turns:]
        context = []
        for item in recent:
            if hasattr(item, "role") and hasattr(item, "content"):
                context.append({"role": item.role, "content": item.content})
            elif isinstance(item, dict):
                context.append({"role": item.get("role", "user"), "content": item.get("content", "")})
        return context
