import uuid
from flask import Blueprint, request, jsonify
from models.conversation import Conversation, Message
from database import db
from utils.translation_utils import translate_text, translate_to_english
from utils.gemini_utils import generate_answer_with_llm
from utils.embedding_utils import get_chroma_client, get_chroma_collection, retrieve_relevant_chunks
import markdown2

chat_bp = Blueprint('chat', __name__)

def get_or_create_conversation(session_id):
    conversation = Conversation.query.filter_by(session_id=session_id).first()
    if conversation is None:
        conversation = Conversation(session_id=session_id)
        db.session.add(conversation)
        db.session.commit()
    return conversation

@chat_bp.route('/chat/new', methods=['POST'])
def new_chat():
    data = request.get_json()
    session_id = data.get("session_id") or ("sess-" + str(uuid.uuid4()))
    conversation = Conversation(session_id=session_id)
    db.session.add(conversation)
    db.session.commit()
    return jsonify({"session_id": session_id, "created_at": conversation.created_at.isoformat()})

@chat_bp.route('/chat', methods=['POST'])
def chat_message():
    data = request.get_json()
    session_id = data.get("session_id")
    user_message = data.get("user_message")
    if not session_id or not user_message:
        return jsonify({"error": "Missing session_id or user_message"}), 400

    # Retrieve (or create) conversation
    conversation = get_or_create_conversation(session_id)

    # Store user's message
    user_msg = Message(conversation_id=conversation.id, sender="user", content=user_message)
    db.session.add(user_msg)
    db.session.commit()

    # Retrieve context from PDFs associated with this conversation.
    # For each PDF, use its stored collection name to get its dedicated Chroma collection.
    context_parts = []
    
    translated_query = translate_text(user_message, target_lang="ne")
    for pdf in conversation.pdfs:
        # pdf.pdf_id contains the dedicated collection name.
        client = get_chroma_client()
        collection = get_chroma_collection(client, pdf.pdf_id)
        chunks = retrieve_relevant_chunks(translated_query, collection)
        if chunks:
            context_parts.append("\n".join(chunks))
    context = "\n".join(context_parts) if context_parts else ""

    # Translate the user's message to Nepali for improved LLM processing.

    # Construct prompt: include context if available.
    if context:
        prompt = f"Given the following context:\n{context}\n\nAnswer the following query:\n{user_message}"
    else:
        prompt = f"Answer: {translated_query}"

    # Generate answer via Gemini LLM.
    raw_answer = generate_answer_with_llm(prompt)
    answer_html = markdown2.markdown(raw_answer)


    # Store bot's response.
    bot_msg = Message(conversation_id=conversation.id, sender="bot", content=answer_html)
    db.session.add(bot_msg)
    db.session.commit()

    return jsonify({"bot_reply": answer_html})

@chat_bp.route('/history', methods=['GET'])
def history():
    session_id = request.args.get("session_id")
    if not session_id:
        return jsonify({"error": "Missing session_id"}), 400
    conversation = Conversation.query.filter_by(session_id=session_id).first()
    if not conversation:
        return jsonify({"messages": []})
    messages = Message.query.filter_by(conversation_id=conversation.id).order_by(Message.timestamp).all()
    message_list = [
        {"sender": msg.sender, "content": msg.content, "timestamp": msg.timestamp.isoformat()}
        for msg in messages
    ]
    return jsonify({"messages": message_list})

@chat_bp.route('/conversations', methods=['GET'])
def conversations():
    convs = Conversation.query.order_by(Conversation.created_at.desc()).all()
    conversation_list = []
    for conv in convs:
        pdfs = [
            {"pdf_id": pdf.pdf_id, "filename": pdf.filename, "uploaded_at": pdf.uploaded_at.isoformat()}
            for pdf in conv.pdfs
        ]
        conversation_list.append({
            "session_id": conv.session_id,
            "created_at": conv.created_at.isoformat(),
            "pdfs": pdfs
        })
    return jsonify({"conversations": conversation_list})
