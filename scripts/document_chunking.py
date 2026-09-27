from pathlib import Path

from document_extraction import extract_text_from_pdf


def chunk_text(text, chunk_size=500, overlap=100):
    """
    Split document text into chunks while trying to preserve
    complete lines and paragraphs.
    """

    if not text:
        return []

    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size")

    lines = [line.strip() for line in text.splitlines() if line.strip()]

    chunks = []
    current_chunk = ""

    for line in lines:

        if len(current_chunk) + len(line) + 1 <= chunk_size:
            current_chunk += line + "\n"

        else:
            if current_chunk.strip():
                chunks.append(current_chunk.strip())

            overlap_text = current_chunk[-overlap:].strip()

            current_chunk = overlap_text + "\n" + line + "\n"

    if current_chunk.strip():
        chunks.append(current_chunk.strip())

    return chunks


if __name__ == "__main__":

    pdf_path = Path("data/documents/quotation_SUP001.pdf")

    text = extract_text_from_pdf(pdf_path)

    chunks = chunk_text(text)

    print("=" * 60)
    print("PROCURA AI — DOCUMENT CHUNKING")
    print("=" * 60)

    print(f"\nDocument: {pdf_path}")
    print(f"Characters extracted: {len(text)}")
    print(f"Number of chunks: {len(chunks)}")

    for index, chunk in enumerate(chunks, start=1):

        print("\n" + "-" * 60)
        print(f"CHUNK {index}")
        print("-" * 60)

        print(chunk)

    print("\n" + "=" * 60)