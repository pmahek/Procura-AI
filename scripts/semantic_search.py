from pathlib import Path
import json

import faiss
from sentence_transformers import SentenceTransformer


MODEL_NAME = "all-MiniLM-L6-v2"

VECTOR_STORE_DIR = Path("outputs/vector_store")

INDEX_PATH = VECTOR_STORE_DIR / "procurement.index"
CHUNKS_PATH = VECTOR_STORE_DIR / "chunks.json"


def load_vector_store():

    index = faiss.read_index(
        str(INDEX_PATH)
    )

    with open(
        CHUNKS_PATH,
        "r",
        encoding="utf-8"
    ) as file:

        chunks = json.load(file)

    return index, chunks


def search_documents(query, top_k=3):

    # Load FAISS index and chunk metadata
    index, chunks = load_vector_store()

    # Load embedding model
    model = SentenceTransformer(MODEL_NAME)

    # Convert user question into an embedding
    query_embedding = model.encode(
        [query],
        convert_to_numpy=True,
        normalize_embeddings=True
    )

    # Search FAISS
    scores, indices = index.search(
        query_embedding,
        min(top_k, index.ntotal)
    )

    results = []

    for score, index_number in zip(
        scores[0],
        indices[0]
    ):

        if index_number == -1:
            continue

        results.append(
            {
                "score": float(score),
                "chunk_id": chunks[index_number]["chunk_id"],
                "source": chunks[index_number]["source"],
                "text": chunks[index_number]["text"]
            }
        )

    return results


if __name__ == "__main__":

    print("=" * 60)
    print("PROCURA AI — SEMANTIC SEARCH")
    print("=" * 60)

    query = input(
        "\nEnter your procurement question: "
    )

    results = search_documents(query)

    print("\nSearch results:")

    for rank, result in enumerate(
        results,
        start=1
    ):

        print("\n" + "-" * 60)
        print(f"RESULT {rank}")
        print("-" * 60)

        print(f"Similarity score: {result['score']:.4f}")
        print(f"Chunk ID: {result['chunk_id']}")

        print("\nText:")
        print(result["text"])

    print("\n" + "=" * 60)