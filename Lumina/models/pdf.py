from database import db
from datetime import datetime

class PDF(db.Model):
    __tablename__ = 'pdf'
    id = db.Column(db.Integer, primary_key=True)
    conversation_id = db.Column(db.Integer, db.ForeignKey('conversation.id'), nullable=False)
    pdf_id = db.Column(db.String, nullable=False)  # We use the dedicated Chroma collection name as pdf_id.
    filename = db.Column(db.String, nullable=True)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
