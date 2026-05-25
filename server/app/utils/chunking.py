def chunk_text(text: str, chunk_size: int = 450, overlap: int = 60) -> list[str]:
    words = text.split()
    if len(words) <= chunk_size:
        return [text.strip()]

    chunks: list[str] = []
    start = 0
    while start < len(words):
        end = start + chunk_size
        chunks.append(" ".join(words[start:end]).strip())
        start = end - overlap

    return [chunk for chunk in chunks if chunk]
