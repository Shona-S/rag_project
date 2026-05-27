from backend.rag.pipeline import build_rag
from backend.provenance.source_tracker import extract_sources
from backend.provenance.highlight_pdf import highlight_text_in_pdf
from backend.guardrails.validator import validate_question


def main():

    pdf_path = "backend/data/sample.pdf"

    # build rag system
    try:
        retriever, llm = build_rag(pdf_path)
    except Exception as e:
        print(f"Error initializing RAG: {e}")
        return

    while True:

        query = input("\nAsk a question (type exit to quit): ")

        if query.lower() == "exit":
            print("Exiting application...")
            break

        # guardrail validation
        if not validate_question(query):
            print("Invalid question. Please ask a valid query.")
            continue

        # retrieve relevant chunks
        docs = retriever.invoke(query)

        if len(docs) == 0:
            print("\nAI Answer:\n Information unavailable.")
            continue

        # build context
        context = "\n".join([doc.page_content for doc in docs])

        prompt = f"""
You are an AI assistant answering questions from a document.

Use ONLY the provided context.

If the answer is not found, say:
Information unavailable.

Context:
{context}

Question:
{query}

Answer:
"""

        # generate answer
        response = llm.invoke(prompt)

        print("\nAI Answer:\n", response.content)

        # extract provenance
        sources = extract_sources(docs)

        print("\nSource(s):")
        for s in sources:
            print(s)

        # highlight the first relevant chunk
        source_text = docs[0].page_content

        highlighted_pdf = highlight_text_in_pdf(
            pdf_path,
            source_text,
            response.content
        )

        print("\nHighlighted PDF saved at:")
        print(highlighted_pdf)


if __name__ == "__main__":
    main()