def normalize_prompt(text: str) -> str:
    return (text or "").strip()


def safe_truncate(value: str, length: int = 80) -> str:
    if not value:
        return ""
    return value if len(value) <= length else value[: length - 3] + "..."


def as_int(value, default=0):
    try:
        return int(value)
    except (TypeError, ValueError):
        return default
