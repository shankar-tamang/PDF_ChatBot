import os, uuid
from flask import Blueprint, request, render_template, jsonify
from werkzeug.utils import secure_filename
from utils.embedding_utils import get_chroma_client, get_chroma_collection, store_chunks_in_chroma
from utils.pdf_utils import chunk_text
from utils.gemini_utils import gemini_text_extraction
from models.conversation import Conversation
from models.pdf import PDF
from database import db
from flask import current_app




pdf_bp = Blueprint('pdf', __name__)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'pdf'

# Global Chroma client instance
from utils.embedding_utils import get_chroma_client
chroma_client = get_chroma_client()
# Dictionary mapping chat_id to dedicated Chroma collections
chat_collections = {}

@pdf_bp.route('/pdf/upload', methods=['POST'])
def upload_pdf():
    """
    Endpoint to upload a PDF file. Expects a form field 'chat_id' to associate the file with a chat session.
    The file is processed via Gemini for text extraction, split into chunks, embedded, and stored in a dedicated
    Chroma collection for that chat.
    """
    chat_id = request.form.get("chat_id")
    if not chat_id:
        return jsonify({"error": "Missing chat session ID."}), 400

    file = request.files.get("file")
    if not file or not allowed_file(file.filename):
        return jsonify({"error": "Invalid file format."}), 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)

    file.save(filepath)

    # Extract text from PDF using Gemini
    extracted_text = gemini_text_extraction(filepath)
    if extracted_text:
        chunks = chunk_text(extracted_text)
        # Create or get dedicated Chroma collection for this chat.
        if chat_id not in chat_collections:
            collection_name = f"chat_{chat_id}"
            chat_collections[chat_id] = get_chroma_collection(chroma_client, collection_name)
        collection = chat_collections[chat_id]
        store_chunks_in_chroma(chunks, filename, collection)
    os.remove(filepath)

    # Create a PDF record in the database associated with the chat.
    conversation = Conversation.query.filter_by(session_id=chat_id).first()
    if not conversation:
        # Auto-create a new conversation
        conversation = Conversation(session_id=chat_id)
        db.session.add(conversation)
        db.session.commit()

    pdf_record = PDF(
        conversation_id=conversation.id,
        pdf_id=collection.name,  # Using collection name as identifier
        filename=filename
    )
    db.session.add(pdf_record)
    db.session.commit()

    return jsonify({"pdf_id": collection.name, "num_chunks": len(chunks)})
