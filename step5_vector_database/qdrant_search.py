from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

client = QdrantClient(":memory:")

collection_name = "company_documents"

client.create_collection(
    collection_name=collection_name,
    vectors_config=VectorParams(
        size=4,
        distance=Distance.COSINE
    )
)

points = [
    PointStruct(
        id=1,
        vector=[0.1, 0.9, 0.2, 0.8],
        payload={
            "text": "Employees receive 20 vacation days annually.",
            "department": "HR"
        }
    ),

    PointStruct(
        id=2,
        vector=[0.8, 0.1, 0.9, 0.2],
        payload={
            "text": "Employees can work remotely two days per week.",
            "department": "HR"
        }
    ),

    PointStruct(
        id=3,
        vector=[0.2, 0.8, 0.1, 0.9],
        payload={
            "text": "Passwords must be changed every 90 days.",
            "department": "IT"
        }
    )
]

client.upsert(
    collection_name=collection_name,
    points=points
)

query_vector = [0.12, 0.88, 0.18, 0.82]

results = client.query_points(
    collection_name=collection_name,
    query=query_vector,
    limit=2
).points

print("=" * 60)
print("SEARCH RESULTS")
print("=" * 60)

for result in results:
    print("\nID:", result.id)
    print("Score:", result.score)
    print("Text:", result.payload["text"])
    print("Department:", result.payload["department"])