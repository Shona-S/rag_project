import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from backend.rag.loader import load_documents
from backend.rag.splitter import split_documents

docs = load_documents("backend/data/sample.pdf")
chunks = split_documents(docs)

chunk = chunks[0].page_content
print("\n--- RAW CHUNK ---")
print(chunk)

text = chunk.replace('\n', ' ')
sentences = [s.strip() for s in text.split(".") if len(s.strip()) > 20]

print("\n--- SENTENCES TO HIGHLIGHT ---")
for idx, s in enumerate(sentences):
    print(f"[{idx}] {s}")
