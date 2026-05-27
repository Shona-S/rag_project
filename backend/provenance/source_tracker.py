def extract_sources(docs):
    """
    Extract document name and page numbers
    from retrieved chunks.
    """

    sources = []

    for doc in docs:
        metadata = doc.metadata

        source = metadata.get("source", "unknown document")
        page = metadata.get("page", "unknown page")

        sources.append(f"{source} | Page {page}")

    return list(set(sources))