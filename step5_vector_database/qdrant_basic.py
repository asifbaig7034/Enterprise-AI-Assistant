from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

client = QdrantClient(":memory:")

collection_name = "test_collection"

client.create_collection(
    collection_name=collection_name,
    vectors_config=VectorParams(
        size=4,
        distance=Distance.COSINE
    )
)

print("Qdrant collection created successfully.")

collections = client.get_collections()

print("\nCollections:")
print(collections)