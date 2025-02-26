import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
import numpy as np
import os

# Define ChromaDB storage path and collection name
CHROMA_DB_PATH = os.path.join(os.getcwd(), "chroma_db")
CHROMA_COLLECTION_NAME = "pdf_embeddings"
SENTENCE_TRANSFORMER_MODEL = 'paraphrase-multilingual-MiniLM-L12-v2'

def get_chroma_client():
    """Initializes and returns a ChromaDB client."""
    return chromadb.PersistentClient(path=CHROMA_DB_PATH, settings=Settings(allow_reset=True))

def get_chroma_collection(client, collection_name=CHROMA_COLLECTION_NAME):
    """Gets or creates a ChromaDB collection with persistence."""
    return client.get_or_create_collection(name=collection_name)

def store_chunks_in_chroma(chunks, filename, chroma_collection):
    """Stores chunked text embeddings in ChromaDB."""
    model = SentenceTransformer(SENTENCE_TRANSFORMER_MODEL)
    
    for idx, chunk in enumerate(chunks):
        embedding = model.encode(chunk, convert_to_tensor=False).tolist()
        doc_id = f"{filename}_{idx}"

        chroma_collection.add(
            ids=[doc_id],
            documents=[chunk],
            metadatas=[{"filename": filename, "chunk_id": idx}],
            embeddings=[embedding]
        )

    # No need to call persist() explicitly when using PersistentClient
    print(f"Stored {len(chunks)} chunks for {filename}.")

def retrieve_relevant_chunks(query, chroma_collection, top_k=5):
    """Retrieves the most relevant text chunks from ChromaDB along with their source filenames."""
    model = SentenceTransformer(SENTENCE_TRANSFORMER_MODEL)
    query_embedding = model.encode(query, convert_to_tensor=False).tolist()

    results = chroma_collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        include=["documents", "metadatas"]
    )

    documents = results.get('documents', [[]])
    metadata = results.get('metadatas', [[]])

    # Ensure we return both the document text and metadata
    retrieved_chunks = []
    for doc, meta in zip(documents[0], metadata[0]):
        retrieved_chunks.append({"text": doc, "filename": meta.get("filename", "Unknown")})

    return retrieved_chunks
