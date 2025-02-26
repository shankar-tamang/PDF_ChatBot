from langchain.text_splitter import RecursiveCharacterTextSplitter


def chunk_text(text, chunk_size=512, chunk_overlap=50):
    """Splits text into chunks for better embedding storage."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len
    )
    return splitter.split_text(text)
