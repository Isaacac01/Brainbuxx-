import re
from datetime import datetime
from typing import Optional

from backend.database import db
from models.conversation import Conversation


def generate_title_from_message(message: str) -> str:
    cleaned = re.sub(r"\s+", " ", message).strip()
    if not cleaned:
        return "New chat"
    words = cleaned.split(" ")[:6]
    title = " ".join(words)
    return title if len(title) <= 50 else title[:47] + "..."


def ensure_conversation_access(conversation_id: int, user_id: int) -> Optional[Conversation]:
    return Conversation.query.filter_by(id=conversation_id, user_id=user_id).first()


def touch_conversation(conversation: Conversation):
    conversation.updated_at = datetime.utcnow()
    db.session.add(conversation)
