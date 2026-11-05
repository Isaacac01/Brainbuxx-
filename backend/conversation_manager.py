class ContextManager:
    def __init__(self, max_turns=8):
        self.max_turns = max_turns

    def build_context(self, messages):
        recent = list(messages)[-self.max_turns:]
        return [
            {"role": item.role, "content": item.content}
            for item in recent
        ]
