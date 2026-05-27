import fitz  # PyMuPDF
import re

def highlight_text_in_pdf(pdf_path, texts, answer_text=None):

    doc = fitz.open(pdf_path)

    if isinstance(texts, str):
        texts = [texts]

    phrases = []

    def normalize(t):
        return re.sub(r'[^a-zA-Z0-9\s]', '', t.lower()).strip()

    normalized_answer = normalize(answer_text) if answer_text else None

    for text in texts:
        # Split text primarily by newlines to respect the document's line breaks
        raw_lines = text.split('\n')

        for line in raw_lines:
            line = line.strip()
            if not line:
                continue
                
            # Split by 2 or more spaces to avoid massive quad boxes across visual gaps
            parts = re.split(r'\s{2,}', line)
            for part in parts:
                part = re.sub(r'\s+', ' ', part.strip())
                
                if len(part) < 8:
                    continue

                if normalized_answer:
                    norm_part = normalize(part)
                    if not norm_part:
                        continue
                    if norm_part in normalized_answer or normalized_answer in norm_part:
                        phrases.append(part)
                else:
                    # Fallback to highlighting all lines in the chunk if no answer is provided
                    if 10 <= len(part) <= 120:
                        phrases.append(part)

    for page in doc:

        for phrase in phrases:

            # quads=True creates polygons tightly wrapping the text matched
            areas = page.search_for(phrase, quads=True)

            for area in areas:
                highlight = page.add_highlight_annot(area)
                highlight.update()

    output_path = "backend/data/highlighted.pdf"

    doc.save(output_path)

    return output_path
