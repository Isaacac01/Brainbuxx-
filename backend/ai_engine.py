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
        html = text
        html = re.sub(r"### (.*)", r"<h3>\1</h3>", html)
        html = re.sub(r"## (.*)", r"<h2>\1</h2>", html)
        html = re.sub(r"# (.*)", r"<h1>\1</h1>", html)
        html = re.sub(r"\*\*(.*)\*\*", r"<strong>\1</strong>", html)
        html = re.sub(r"\*(.*)\*", r"<em>\1</em>", html)
        html = re.sub(r"`([^`]+)`", r"<code>\1</code>", html)
        html = re.sub(r"\n- (.*)", r"\n<li>\1</li>", html)
        html = html.replace("\n", "<br>")
        return html
