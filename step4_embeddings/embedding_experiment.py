import os

from dotenv import load_dotenv
from google import genai

load_dotenv("../step1_llm/.env")

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY was not found")

client = genai.Client(api_key=api_key)

text = "Machine learning allows computers to learn patterns from data."

result = client.models.embed_content(
    model="gemini-embedding-2",
    contents=text
)

embedding = result.embeddings[0].values

print("=" * 60)
print("EMBEDDING EXPERIMENT")
print("=" * 60)

print("Original text:")
print(text)

print("\nEmbedding dimensions:")
print(len(embedding))

print("\nFirst 10 values:")
print(embedding[:10])