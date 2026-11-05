from datetime import datetime

from backend.database import db


class ConversationMetadata(db.Model):
    __tablename__ = "conversation_metadata"

    id = db.Column(db.Integer, primary_key=True)
    conversation_id = db.Column(db.Integer, db.ForeignKey("conversations.id"), unique=True, nullable=False)
    topic = db.Column(db.String(200), default="General")
    language = db.Column(db.String(30), default="en")
    last_intent = db.Column(db.String(120), default="general")
    summary = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    conversation = db.relationship("Conversation", back_populates="metadata")
