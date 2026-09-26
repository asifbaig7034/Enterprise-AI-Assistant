import os
import json

from dotenv import load_dotenv
from google import genai


load_dotenv("../step1_llm/.env")

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError(
        "GEMINI_API_KEY was not found."
    )


client = genai.Client(
    api_key=api_key
)


question = """
How many annual vacation days do employees receive?
"""


context = """
Employees receive 24 annual vacation days every calendar year.
"""


answer = """
Employees receive 24 annual vacation days.
"""


evaluation_prompt = f"""
You are an evaluator for an enterprise RAG system.

Evaluate the answer using ONLY the provided context.

Question:
{question}

Context:
{context}

Generated Answer:
{answer}

Evaluate:

1. Faithfulness:
Is every factual claim supported by the context?

2. Answer relevance:
Does the answer directly answer the question?

3. Correctness:
Is the answer factually correct according to the context?

Return JSON with this structure:

{{
    "faithfulness": true,
    "answer_relevance": true,
    "correctness": true,
    "score": 1,
    "reason": "short explanation"
}}
"""


response = client.models.generate_content(
    model="gemini-3.5-flash",
    contents=evaluation_prompt,
    config={
        "response_mime_type": "application/json"
    }
)


print("=" * 60)
print("LLM-AS-A-JUDGE")
print("=" * 60)

print(response.text)