import os

from dotenv import load_dotenv
from google import genai

load_dotenv("../step1_llm/.env")

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY was not found")

client = genai.Client(api_key=api_key)

prompt = """
Explain RAG in simple English.
Give exactly three bullet points.
"""

response = client.interactions.create(
    model="gemini-3.8-flash",
    input=prompt
)

print("=" * 60)
print("MODEL RESPONSE")
print("=" * 60)

print(response.output_text)

print("\n" + "=" * 60)
print("RESPONSE INFORMATION")
print("=" * 60)

print(response)