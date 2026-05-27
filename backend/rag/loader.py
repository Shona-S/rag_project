from langchain_community.document_loaders import PyPDFLoader

def load_documents(path: str):
    loader = PyPDFLoader(path)
    documents = loader.load()
    return documents