from pathlib import Path
import json

import faiss
from sentence_transformers import SentenceTransformer

from document_extraction import extract_text_from_pdf
from document_chunking import chunk_text


MODEL_NAME = "all-MiniLM-L6-v2"

PDF_PATH = Path("data/documents/quotation_SUP001.pdf")

VECTOR_STORE_DIR = Path("outputs/vector_store")
INDEX_PATH = VECTOR_STORE_DIR / "procurement.index"
CHUNKS_PATH = VECTOR_STORE_DIR / "chunks.json"


def build_vector_store():

    print("=" * 60)
    print("PROCURA AI — FAISS VECTOR STORE")
    print("=" * 60)

    # ---------------------------------------------------------
    # 1. Extract document text
    # ---------------------------------------------------------

    print("\nExtracting document text...")

    text = extract_text_from_pdf(PDF_PATH)

    # ---------------------------------------------------------
    # 2. Create chunks
    # ---------------------------------------------------------

    print("Creating document chunks...")

    chunks = chunk_text(text)

    print(f"Number of chunks: {len(chunks)}")

    # ---------------------------------------------------------
    # 3. Load embedding model
    # ---------------------------------------------------------

    print("\nLoading embedding model...")

    model = SentenceTransformer(MODEL_NAME)

    print("Embedding model loaded.")

    # ---------------------------------------------------------
    # 4. Generate embeddings
    # ---------------------------------------------------------

    print("\nGenerating embeddings...")

    embeddings = model.encode(
        chunks,
        convert_to_numpy=True,
        normalize_embeddings=True
    )

    print(f"Embedding shape: {embeddings.shape}")

    # ---------------------------------------------------------
    # 5. Create FAISS index
    # ---------------------------------------------------------

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatIP(dimension)

    index.add(embeddings)

    print(f"\nFAISS index created.")
    print(f"Number of vectors in index: {index.ntotal}")

    # ---------------------------------------------------------
    # 6. Create output directory
    # ---------------------------------------------------------

    VECTOR_STORE_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    # ---------------------------------------------------------
    # 7. Save FAISS index
    # ---------------------------------------------------------

    faiss.write_index(
        index,
        str(INDEX_PATH)
    )

    # ---------------------------------------------------------
    # 8. Save chunk text
    # ---------------------------------------------------------

    chunk_data = []

    for index_number, chunk in enumerate(chunks):

        chunk_data.append(
            {
                "chunk_id": index_number,
                "source": str(PDF_PATH),
                "text": chunk
            }
        )

    with open(
        CHUNKS_PATH,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            chunk_data,
            file,
            indent=4,
            ensure_ascii=False
        )

    print("\nVector store saved.")

    print(f"FAISS index: {INDEX_PATH}")
    print(f"Chunk metadata: {CHUNKS_PATH}")

    print("\n" + "=" * 60)
    print("FAISS VECTOR STORE CREATED SUCCESSFULLY")
    print("=" * 60)


if __name__ == "__main__":
    build_vector_store()