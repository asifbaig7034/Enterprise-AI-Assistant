import os

from dotenv import load_dotenv
from google import genai

from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct
)


# ============================================================
# 1. Load API key
# ============================================================

load_dotenv("../step1_llm/.env")

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY was not found")


# ============================================================
# 2. Initialize clients
# ============================================================

client = genai.Client(api_key=api_key)

qdrant = QdrantClient(":memory:")

collection_name = "company_knowledge"


# ============================================================
# 3. Load document
# ============================================================

with open(
    "documents/company_policies.txt",
    "r",
    encoding="utf-8"
) as file:

    document = file.read()


# ============================================================
# 4. Simple chunking
# ============================================================

chunks = [
    chunk.strip()
    for chunk in document.split("\n\n")
    if chunk.strip()
]


print("=" * 60)
print("DOCUMENT CHUNKS")
print("=" * 60)

for i, chunk in enumerate(chunks, start=1):

    print(f"\nChunk {i}:")
    print(chunk)


# ============================================================
# 5. Generate first embedding
# ============================================================

first_embedding = client.models.embed_content(
    model="gemini-embedding-2",
    contents=chunks[0]
)

vector_size = len(
    first_embedding.embeddings[0].values
)

print("\nEmbedding dimensions:", vector_size)


# ============================================================
# 6. Create Qdrant collection
# ============================================================

qdrant.create_collection(
    collection_name=collection_name,
    vectors_config=VectorParams(
        size=vector_size,
        distance=Distance.COSINE
    )
)


# ============================================================
# 7. Embed and store chunks
# ============================================================

points = []

for i, chunk in enumerate(chunks, start=1):

    result = client.models.embed_content(
        model="gemini-embedding-2",
        contents=chunk
    )

    vector = result.embeddings[0].values

    points.append(
        PointStruct(
            id=i,
            vector=vector,
            payload={
                "text": chunk,
                "chunk_id": i
            }
        )
    )


qdrant.upsert(
    collection_name=collection_name,
    points=points
)


print("\nDocuments stored in Qdrant.")


# ============================================================
# 8. User question
# ============================================================

question = "How many vacation days do employees receive?"


# ============================================================
# 9. Embed question
# ============================================================

query_result = client.models.embed_content(
    model="gemini-embedding-2",
    contents=question
)

query_vector = query_result.embeddings[0].values


# ============================================================
# 10. Retrieve relevant chunks
# ============================================================

search_results = qdrant.query_points(
    collection_name=collection_name,
    query=query_vector,
    limit=3
).points


print("\n" + "=" * 60)
print("RETRIEVED CONTEXT")
print("=" * 60)

for result in search_results:

    print("\nScore:", result.score)
    print("Chunk:", result.payload["chunk_id"])
    print("Text:")
    print(result.payload["text"])


# ============================================================
# 11. Build RAG prompt
# ============================================================

context = "\n\n".join(
    result.payload["text"]
    for result in search_results
)


rag_prompt = f"""
You are an enterprise AI assistant.

Answer the user's question using ONLY the provided context.

If the answer cannot be found in the context,
say that the information is not available.

Do not invent information.

CONTEXT:
{context}

USER QUESTION:
{question}
"""


# ============================================================
# 12. Generate answer
# ============================================================

response = client.interactions.create(
    model="gemini-3.8-flash",
    input=rag_prompt
)


# ============================================================
# 13. Final answer
# ============================================================

print("\n" + "=" * 60)
print("RAG ANSWER")
print("=" * 60)

print(response.output_text)