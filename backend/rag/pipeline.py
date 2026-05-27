from langchain_groq import ChatGroq

from backend.config import GROQ_API_KEY, MODEL_NAME
from backend.rag.loader import load_documents
from backend.rag.splitter import split_documents
from backend.rag.embeddings import get_embeddings
from backend.rag.vectorstore import create_vectorstore


def build_rag(pdf_path):

    print("Loading PDF...")
    docs = load_documents(pdf_path)

    print("Splitting text...")
    chunks = split_documents(docs)

    print(f"Chunks created: {len(chunks)}")
    
    if not chunks:
        raise ValueError(
            "No selectable text could be extracted from the PDF. "
            "Please ensure the PDF is not empty and is not a scanned image (requires digital text)."
        )

    print("Creating embeddings...")
    embeddings = get_embeddings()

    print("Building vector database...")
    vectorstore = create_vectorstore(chunks, embeddings)

    retriever = vectorstore.as_retriever(search_kwargs={"k": 2})

    print("Connecting to Groq...")
    llm = ChatGroq(
        groq_api_key=GROQ_API_KEY,
        model_name=MODEL_NAME
    )

    print("RAG Ready [OK]")

    return retriever, llm