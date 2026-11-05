import re


class ResponseFormatter:
    @staticmethod
    def normalize(text: str) -> str:
        cleaned = text.strip()
        if not cleaned:
            return "I’m here to help. Tell me what you’d like to work on."
        return cleaned

    @staticmethod
    def markdown_to_html(text: str) -> str:
        replacements = [
            (r"### (.*)", r"<h3>\1</h3>"),
            (r"## (.*)", r"<h2>\1</h2>"),
            (r"# (.*)", r"<h1>\1</h1>"),
            (r"\*\*(.*)\*\*", r"<strong>\1</strong>"),
            (r"\*(.*)\*", r"<em>\1</em>"),
            (r"`([^`]+)`", r"<code>\1</code>"),
            (r"\n- (.*)", r"\n<li>\1</li>"),
        ]
        html = text
        for pattern, replacement in replacements:
            html = re.sub(pattern, replacement, html)
        html = html.replace("\n", "<br>")
        return html
