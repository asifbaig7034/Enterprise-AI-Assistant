import os

from dotenv import load_dotenv
from google import genai
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY was not found in .env")


client = genai.Client(api_key=api_key)


def create_embedding(text: str):

    result = client.models.embed_content(
        model="gemini-embedding-2",
        contents=text,
    )

    return result.embeddings[0].values


def load_documents():

    with open(
        "data/documents/company_policies.txt",
        "r",
        encoding="utf-8"
    ) as f:
        document = f.read()

    chunks = [
        chunk.strip()
        for chunk in document.split("\n\n")
        if chunk.strip()
    ]

    return chunks


def build_vector_store():

    qdrant = QdrantClient(":memory:")

    collection_name = "company_policies"

    first_embedding = create_embedding(
        "company policy"
    )

    qdrant.create_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(
            size=len(first_embedding),
            distance=Distance.COSINE,
        ),
    )

    chunks = load_documents()

    points = []

    for index, chunk in enumerate(chunks):

        embedding = create_embedding(chunk)

        points.append(
            PointStruct(
                id=index,
                vector=embedding,
                payload={
                    "text": chunk
                },
            )
        )

    qdrant.upsert(
        collection_name=collection_name,
        points=points,
    )

    return qdrant, collection_name


def retrieve_context(question: str, top_k: int = 3):

    qdrant, collection_name = build_vector_store()

    query_embedding = create_embedding(question)

    results = qdrant.query_points(
        collection_name=collection_name,
        query=query_embedding,
        limit=top_k,
    ).points

    contexts = []

    for result in results:
        contexts.append(result.payload["text"])

    return "\n\n".join(contexts)
