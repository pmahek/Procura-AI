import os

from dotenv import load_dotenv
from google import genai

from semantic_search import search_documents


load_dotenv()


def build_context(query, top_k=3):

    results = search_documents(
        query=query,
        top_k=top_k
    )

    context_parts = []

    for result in results:

        context_parts.append(
            f"""
Source: {result['source']}
Chunk ID: {result['chunk_id']}

{result['text']}
"""
        )

    return "\n".join(context_parts)


def generate_answer(query, context):

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY was not found in the .env file."
        )

    client = genai.Client(
        api_key=api_key
    )

    prompt = f"""
You are ProcuraAI, an AI procurement assistant.

Answer the user's question using ONLY the procurement
context provided below.

Rules:
1. Do not invent information.
2. If the answer is not present in the context,
   say that the information was not found.
3. Keep the answer concise and business-focused.
4. Preserve procurement values such as prices,
   dates, quantities, warranty periods and discounts.
5. Mention the source document when useful.

PROCUREMENT CONTEXT
-------------------
{context}
-------------------

USER QUESTION
-------------
{query}

Provide the procurement answer.
"""

    interaction = client.interactions.create(
        model="gemini-3.8-flash",
        input=prompt
    )

    return interaction.output_text

if __name__ == "__main__":

    print("=" * 60)
    print("PROCURA AI — RAG")
    print("=" * 60)

    query = input(
        "\nEnter your procurement question: "
    )

    print("\nRetrieving relevant documents...")

    context = build_context(query)

    print("Generating answer...")

    answer = generate_answer(
        query=query,
        context=context
    )

    print("\nProcuraAI Answer:")
    print("-" * 60)
    print(answer)

    print("\n" + "=" * 60)