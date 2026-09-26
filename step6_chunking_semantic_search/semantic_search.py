import os

from dotenv import load_dotenv
from google import genai

from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct
)


load_dotenv("../step1_llm/.env")

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY was not found")


client = genai.Client(api_key=api_key)

qdrant = QdrantClient(":memory:")

collection_name = "company_documents"


# --------------------------------------------------
# 1. Documents
# --------------------------------------------------

documents = [
    {
        "id": 1,
        "text": "Employees receive 20 annual vacation days every calendar year.",
        "department": "HR"
    },
    {
        "id": 2,
        "text": "Employees can work remotely two days per week with manager approval.",
        "department": "HR"
    },
    {
        "id": 3,
        "text": "Employees must change their company password every 90 days.",
        "department": "IT"
    },
    {
        "id": 4,
        "text": "Passwords must contain uppercase letters, lowercase letters, numbers, and special characters.",
        "department": "IT"
    }
]


# --------------------------------------------------
# 2. Create first embedding
# --------------------------------------------------

first_embedding = client.models.embed_content(
    model="gemini-embedding-2",
    contents=documents[0]["text"]
)

vector_size = len(first_embedding.embeddings[0].values)

print("Embedding dimensions:", vector_size)


# --------------------------------------------------
# 3. Create Qdrant collection
# --------------------------------------------------

qdrant.create_collection(
    collection_name=collection_name,
    vectors_config=VectorParams(
        size=vector_size,
        distance=Distance.COSINE
    )
)


# --------------------------------------------------
# 4. Generate embeddings and store documents
# --------------------------------------------------

points = []

for document in documents:

    result = client.models.embed_content(
        model="gemini-embedding-2",
        contents=document["text"]
    )

    vector = result.embeddings[0].values

    points.append(
        PointStruct(
            id=document["id"],
            vector=vector,
            payload={
                "text": document["text"],
                "department": document["department"]
            }
        )
    )


qdrant.upsert(
    collection_name=collection_name,
    points=points
)


# --------------------------------------------------
# 5. User query
# --------------------------------------------------

query = "How many days of annual leave do employees receive?"


query_result = client.models.embed_content(
    model="gemini-embedding-2",
    contents=query
)

query_vector = query_result.embeddings[0].values


# --------------------------------------------------
# 6. Semantic search
# --------------------------------------------------

results = qdrant.query_points(
    collection_name=collection_name,
    query=query_vector,
    limit=2
).points


# --------------------------------------------------
# 7. Display results
# --------------------------------------------------

print("\n" + "=" * 60)
print("SEMANTIC SEARCH RESULTS")
print("=" * 60)

print("\nQuery:")
print(query)

for i, result in enumerate(results, start=1):

    print(f"\nResult {i}")

    print("Score:", result.score)

    print("Department:",
          result.payload["department"])

    print("Text:",
          result.payload["text"])