from datetime import datetime

from flask import Blueprint, jsonify, request
from flask_login import current_user, login_required

from backend.ai_engine import AIEngine
from backend.conversation_manager import ensure_conversation_access, generate_title_from_message, touch_conversation
from backend.database import db
from models.conversation import Conversation
from models.message import Message

chat_bp = Blueprint("chat", __name__)
ai_engine = AIEngine()


@chat_bp.route("/api/chat", methods=["POST"])
@login_required
def send_chat_message():
    payload = request.get_json(silent=True) or {}
    text = (payload.get("message") or "").strip()
    conversation_id = payload.get("conversation_id")

    if not text:
        return jsonify({"error": "Message is required."}), 400

    conversation = None
    if conversation_id:
        conversation = ensure_conversation_access(conversation_id, current_user.id)

    if conversation is None:
        conversation = Conversation(title=generate_title_from_message(text), user_id=current_user.id)
        db.session.add(conversation)
        db.session.commit()

    user_message = Message(conversation_id=conversation.id, role="user", content=text)
    db.session.add(user_message)
    db.session.commit()

    response, intent = ai_engine.process_message(text, conversation)

    assistant_message = Message(conversation_id=conversation.id, role="assistant", content=response)
    db.session.add(assistant_message)

    conversation.title = conversation.title if conversation.title and conversation.title != "New chat" else generate_title_from_message(text)
    conversation.updated_at = datetime.utcnow()
    db.session.commit()

    return jsonify({
        "response": response,
        "conversation_id": conversation.id,
        "intent": intent.get("intent"),
        "title": conversation.title,
    })


@chat_bp.route("/api/conversations", methods=["GET", "POST"])
@login_required
def conversations():
    if request.method == "POST":
        conversation = Conversation(title="New chat", user_id=current_user.id)
        db.session.add(conversation)
        db.session.commit()
        return jsonify({"id": conversation.id, "title": conversation.title})

    conversations_list = Conversation.query.filter_by(user_id=current_user.id).order_by(Conversation.updated_at.desc()).all()
    payload = [
        {
            "id": item.id,
            "title": item.title,
            "created_at": item.created_at.isoformat(),
            "updated_at": item.updated_at.isoformat(),
        }
        for item in conversations_list
    ]
    return jsonify(payload)


@chat_bp.route("/api/conversations/search", methods=["GET"])
@login_required
def search_conversations():
    query = (request.args.get("q") or "").strip().lower()
    results = Conversation.query.filter_by(user_id=current_user.id).all()
    filtered = []
    for item in results:
        if query in item.title.lower():
            filtered.append({"id": item.id, "title": item.title})
    return jsonify(filtered)


@chat_bp.route("/api/conversations/<int:conversation_id>", methods=["GET", "PATCH", "DELETE"])
@login_required
def conversation_detail(conversation_id):
    conversation = ensure_conversation_access(conversation_id, current_user.id)
    if conversation is None:
        return jsonify({"error": "Conversation not found."}), 404

    if request.method == "GET":
        messages = [
            {"id": msg.id, "role": msg.role, "content": msg.content, "created_at": msg.created_at.isoformat()}
            for msg in conversation.messages
        ]
        return jsonify({"id": conversation.id, "title": conversation.title, "messages": messages})

    if request.method == "PATCH":
        payload = request.get_json(silent=True) or {}
        title = (payload.get("title") or "").strip()
        if not title:
            return jsonify({"error": "Title cannot be empty."}), 400
        conversation.title = title
        conversation.updated_at = datetime.utcnow()
        db.session.commit()
        return jsonify({"id": conversation.id, "title": conversation.title})

    db.session.delete(conversation)
    db.session.commit()
    return jsonify({"deleted": True, "id": conversation.id})
