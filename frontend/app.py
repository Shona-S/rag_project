import sys
import os
import base64
import time
import streamlit as st
import fitz  # PyMuPDF

# allow backend imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.rag.pipeline import build_rag
from backend.provenance.highlight_pdf import highlight_text_in_pdf


st.set_page_config(page_title="Enterprise Document Assistant", layout="wide")

st.title("Enterprise Document Assistant")


# -------------------------------
# Sidebar Mode Selection
# -------------------------------
mode = st.sidebar.selectbox(
    "Choose Mode",
    ["Enterprise Policy", "Legal Document"]
)


# -------------------------------
# PDF Viewer Function (PNG Rendered)
# -------------------------------
def display_pdf(file_path):
    try:
        doc = fitz.open(file_path)
        num_pages = len(doc)
        
        # Page selector widget
        page_num = st.number_input("Page", min_value=1, max_value=num_pages, value=1, key="pdf_page_selector")
        
        # Render the selected page as PNG
        page = doc[page_num - 1]
        pix = page.get_pixmap(dpi=150)
        img_bytes = pix.tobytes("png")
        
        st.image(img_bytes, use_container_width=True)
    except Exception as e:
        st.error(f"Error rendering PDF: {e}")


# -------------------------------
# Upload PDF
# -------------------------------
uploaded_file = st.file_uploader("Upload PDF", type="pdf")


if uploaded_file:

    file_path = f"backend/data/{uploaded_file.name}"

    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success("PDF uploaded successfully")


    # -------------------------------
    # Build RAG Pipeline
    # -------------------------------
    if "rag_pipeline" not in st.session_state or st.session_state.get("rag_file_path") != file_path:
        try:
            retriever, llm = build_rag(file_path)
            st.session_state["rag_pipeline"] = (retriever, llm)
            st.session_state["rag_file_path"] = file_path
        except ValueError as ve:
            st.error(str(ve))
            st.stop()
        except Exception as e:
            st.error(f"Failed to process PDF: {e}")
            st.stop()

    retriever, llm = st.session_state["rag_pipeline"]


    # -------------------------------
    # Layout configuration
    # -------------------------------
    col1, col2 = st.columns([1, 1])

    with col1:
        # -------------------------------
        # Ask Question
        # -------------------------------
        question = st.text_input("Ask a question")

        if question:

            docs = retriever.invoke(question)

            context = "\n".join([d.page_content for d in docs])

            prompt = f"""
You are an assistant answering questions from a document.

Use ONLY the context below.

If the answer is not present say:
Information unavailable.

Context:
{context}

Question:
{question}

Answer:
"""

            response = llm.invoke(prompt)

            st.subheader("Answer")
            st.write(response.content)

            # -------------------------------
            # Highlight Source
            # -------------------------------
            source_texts = [d.page_content for d in docs]

            highlighted_pdf = highlight_text_in_pdf(
                file_path,
                source_texts,
                response.content
            )

    with col2:
        if question and 'highlighted_pdf' in locals():
            st.subheader("Highlighted Source Document")

            display_pdf(highlighted_pdf)

            # -------------------------------
            # Download Button
            # -------------------------------
            with open(highlighted_pdf, "rb") as f:
                st.download_button(
                    "Download highlighted PDF",
                    f,
                    file_name="highlighted.pdf"
                )