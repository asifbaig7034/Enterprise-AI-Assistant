import os

from dotenv import load_dotenv
from google import genai


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY was not found in .env")


client = genai.Client(api_key=api_key)


def generate_grounded_answer(question: str, context: str) -> str:

    prompt = f"""
You are an enterprise company policy assistant.

Answer the user's question using ONLY the information provided
in the company policy context.

Do not use outside knowledge.

If the answer cannot be found in the context, say:

"I couldn't find this information in the available company policies."

Company policy context:

{context}

User question:

{question}

Answer clearly and concisely.
"""

    response = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=prompt,
    )

    return response.text
