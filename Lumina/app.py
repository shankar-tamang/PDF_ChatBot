from flask import Flask, request, render_template, jsonify
import os
from werkzeug.utils import secure_filename
from utils.embedding_utils import get_chroma_client
from routes.chat import chat_bp
from routes.pdf import pdf_bp
from database import db
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lumina.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

CORS(app)
db.init_app(app)
with app.app_context():
    db.create_all()

app.register_blueprint(chat_bp)
app.register_blueprint(pdf_bp)

if __name__ == '__main__':
    app.run(debug=True)
