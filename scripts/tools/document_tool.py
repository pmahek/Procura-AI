import sys
import os

sys.path.insert(
    0,
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

from rag import build_context, generate_answer


def document_tool(query):
    """
    Search procurement documents and generate
    an answer using the RAG pipeline.
    """

    context = build_context(
        query=query,
        top_k=3
    )

    if not context:
        return {
            "status": "error",
            "message": "No relevant procurement documents found."
        }

    answer = generate_answer(
        query=query,
        context=context
    )

    return {
        "status": "success",
        "query": query,
        "answer": answer,
        "context": context
    }


if __name__ == "__main__":

    query = (
        "What are the payment terms, discount, "
        "delivery conditions, and warranty information "
        "in the supplier quotation?"
    )

    result = document_tool(query)

    print("=" * 70)
    print("PROCURA AI — DOCUMENT TOOL")
    print("=" * 70)

    print(f"Status: {result['status']}")

    print("\nQuestion:")
    print(result["query"])

    print("\nAnswer:")
    print(result["answer"])