from pathlib import Path

from sentence_transformers import SentenceTransformer

from document_extraction import extract_text_from_pdf
from document_chunking import chunk_text


def create_embeddings(chunks, model):
    """
    Convert document chunks into numerical vectors.
    """
    embeddings = model.encode(
        chunks,
        convert_to_numpy=True,
        normalize_embeddings=True
    )

    return embeddings


if __name__ == "__main__":

    pdf_path = Path("data/documents/quotation_SUP001.pdf")

    print("=" * 60)
    print("PROCURA AI — DOCUMENT EMBEDDINGS")
    print("=" * 60)

    # Step 1: Extract text
    text = extract_text_from_pdf(pdf_path)

    # Step 2: Create chunks
    chunks = chunk_text(text)

    print(f"\nDocument: {pdf_path}")
    print(f"Number of chunks: {len(chunks)}")

    # Step 3: Load embedding model
    print("\nLoading embedding model...")

    model = SentenceTransformer("all-MiniLM-L6-v2")

    print("Embedding model loaded.")

    # Step 4: Generate embeddings
    embeddings = create_embeddings(chunks, model)

    print(f"\nEmbedding shape: {embeddings.shape}")

    # Step 5: Display information
    for index, embedding in enumerate(embeddings, start=1):

        print("\n" + "-" * 60)
        print(f"CHUNK {index}")
        print("-" * 60)

        print(f"Text preview: {chunks[index - 1][:150]}...")
        print(f"Vector dimensions: {len(embedding)}")
        print(f"First 10 values: {embedding[:10]}")

    print("\n" + "=" * 60)
    print("EMBEDDINGS CREATED SUCCESSFULLY")
    print("=" * 60)