# 📄 PDF Chatbot with Retrieval-Augmented Generation (RAG)

A **ChatGPT-like AI assistant** that allows users to **upload PDFs**, extract their content using **Gemini AI**, convert the extracted text into **embeddings using ChromaDB**, and **query** the document to receive intelligent responses.

This project consists of:

- **Backend (Flask API)**: Handles file uploads, text extraction, embeddings, and querying.
- **Frontend (ReactJS UI)**: A sleek ChatGPT-inspired interface for user interaction.

---

## 🚀 Features

✅ **Chat Session Management**  
✅ **PDF Upload & Text Extraction** (via Gemini)  
✅ **Embeddings with ChromaDB** (for efficient retrieval)  
✅ **Query Handling with Retrieval-Augmented Generation (RAG)**  
✅ **ChatGPT-like UI** (scrollable history, file upload integration)  
✅ **Markdown Support** (for formatted responses)  
✅ **Typing & Uploading Animations**  

---

## 📁 Project Structure

```
pdf-chatbot/
│── lumina/                  # Backend (Flask)
│   ├── app.py               # Main backend entry point
│   ├── database.py          # Database setup (SQLAlchemy)
│   ├── routes/              # API Endpoints
│   │   ├── chat.py          # Chat message handling (RAG, retrieval, LLM response)
│   │   ├── pdf.py           # PDF file upload & embedding storage
│   ├── utils/               # Helper utilities
│   │   ├── gemini_utils.py  # Google Gemini AI integration
│   │   ├── pdf_utils.py     # PDF text extraction & chunking
│   │   ├── embedding_utils.py # ChromaDB embedding storage/retrieval
│   │   ├── translation_utils.py # Query translation (English <-> Nepali)
│   ├── models/              # Database Models
│   │   ├── conversation.py  # Chat sessions & messages
│   │   ├── pdf.py           # Uploaded PDFs
│── pdf-chatbot-frontend/    # Frontend (React)
│   ├── src/
│   │   ├── components/
│   │   │   ├── Sidebar.jsx  # Sidebar with chat list & actions
│   │   │   ├── ChatArea.jsx # Chat window (messages, file uploads)
│   │   │   ├── ChatInput.jsx # Input box (text & file upload)
│   │   ├── services/api.js  # API calls to Flask backend
│   │   ├── App.js           # Main React App component
│── requirements.txt         # Python dependencies
│── README.md                # Documentation
```

---

## ⚙️ Setup & Installation

### 📌 Prerequisites

- **Backend**
  - Python 3.8+
  - Flask, Flask-CORS
  - Google Gemini API Key
  - ChromaDB
  - Sentence Transformers (`paraphrase-multilingual-MiniLM-L12-v2`)

- **Frontend**
  - Node.js v14+
  - React.js

---

### 🔥 Backend Setup (Flask)

1️⃣ **Clone the repository**  
```bash
git clone https://github.com/yourusername/pdf-chatbot.git
cd pdf-chatbot/lumina
```

2️⃣ **Create a virtual environment & install dependencies**  
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3️⃣ **Set up environment variables**  
Create a `.env` file:
```
GOOGLE_API_KEY=your_google_gemini_api_key
CHROMA_DB_PATH=chroma_db/
UPLOAD_FOLDER=uploads/
```

4️⃣ **Run the backend**  
```bash
python app.py
```
The backend will start at `http://127.0.0.1:5000`.

---

### 🎨 Frontend Setup (React)

1️⃣ **Navigate to the frontend folder**  
```bash
cd ../pdf-chatbot-frontend
```

2️⃣ **Install dependencies**  
```bash
npm install
```

3️⃣ **Run the frontend**  
```bash
npm start
```
The frontend will be available at `http://localhost:3000`.

---

## 📡 API Endpoints (Backend)

### 📌 **Chat Endpoints**
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/chat/new` | Creates a new chat session |
| `POST` | `/chat` | Sends a message and gets AI response |
| `GET`  | `/history?session_id=XYZ` | Retrieves chat history |
| `GET`  | `/conversations` | Gets all conversations |

### 📌 **PDF Upload & Querying**
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/pdf/upload` | Uploads a PDF file & extracts embeddings |
| `POST` | `/chat` | Queries the document with RAG |

---

## 🛠 Usage Instructions

1️⃣ **Start a New Chat**  
   - Click **+ New Chat** (sidebar).  
   - Chats are auto-named based on **date** (e.g., "Tue Mar 14 2025, Chat #1").  

2️⃣ **Upload a PDF**  
   - Click 📎 **Attach File** in input box.  
   - File uploads show **“Uploading... 🤔”** status, followed by confirmation.  

3️⃣ **Ask a Question**  
   - Type a message and press **Enter**.  
   - The chatbot retrieves relevant chunks and generates an AI response.  

4️⃣ **Chat History & UI**  
   - Scroll to see past messages, **formatted with Markdown**.  
   - Uploaded files appear **above the first query** like in ChatGPT.  

---

## 🎨 Frontend Enhancements

- **📝 File Uploads Appear in Chat Window** (not just in input box).  
- **⌛ Upload Status is Lightweight** (animated subtle message).  
- **🌀 Typing Animation Like ChatGPT** (`...` dots effect while bot thinks).  
- **🖼 Markdown Support for AI Replies** (renders properly formatted text).  
- **📜 Long Scrollable Query & Response Area** (for better readability).  

---

## 🛠 Troubleshooting

### ❌ Backend Issues
✅ Check if Flask server is running (`http://127.0.0.1:5000`).  
✅ Ensure **Google API Key** is correct in `.env`.  
✅ Run `flask db upgrade` if facing database issues.  

### ❌ Frontend Issues
✅ Run `npm install` again if dependencies are missing.  
✅ Ensure **API Base URL** is correct in `api.js`.  
✅ Check browser **Console** for CORS or network errors.  

---

## 🤝 Contributing

🚀 Contributions are welcome! Fork this repository and submit a PR.  

---

## 📜 License

📝 MIT License.  
Use freely, modify, and share.  

---

💡 **Built with Flask, React, and ChromaDB for smarter PDF interactions.** 🎉

