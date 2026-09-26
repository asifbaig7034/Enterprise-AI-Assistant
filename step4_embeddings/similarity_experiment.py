import os
import math

from dotenv import load_dotenv
from google import genai

load_dotenv("../step1_llm/.env")

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY was not found")

client = genai.Client(api_key=api_key)

texts = [
    "How can I reset my password?",
    "I forgot my password and want to change it.",
    "What is the weather like today?"
]

def get_embedding(text):
    result = client.models.embed_content(
        model="gemini-embedding-2",
        contents=text
    )

    return result.embeddings[0].values


def cosine_similarity(a, b):
    dot_product = sum(x * y for x, y in zip(a, b))

    magnitude_a = math.sqrt(sum(x * x for x in a))
    magnitude_b = math.sqrt(sum(y * y for y in b))

    return dot_product / (magnitude_a * magnitude_b)


print("Generating embeddings...")

embeddings = [get_embedding(text) for text in texts]

similarity_01 = cosine_similarity(
    embeddings[0],
    embeddings[1]
)

similarity_02 = cosine_similarity(
    embeddings[0],
    embeddings[2]
)

print("\n" + "=" * 60)
print("SEMANTIC SIMILARITY")
print("=" * 60)

print("\nText 1:")
print(texts[0])

print("\nText 2:")
print(texts[1])

print("\nSimilarity between Text 1 and Text 2:")
print(similarity_01)

print("\nText 3:")
print(texts[2])

print("\nSimilarity between Text 1 and Text 3:")
print(similarity_02)