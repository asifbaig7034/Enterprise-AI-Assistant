import os

from dotenv import load_dotenv
from google import genai

from app.models.schemas import IntentResponse


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY was not found in .env")


client = genai.Client(api_key=api_key)


def classify_intent(question: str) -> IntentResponse:

    prompt = f"""
You are an intent classification system for an enterprise AI assistant.

Classify the user's question into exactly one of these intents:

- leave_balance
- leave_policy
- remote_work_policy
- password_policy
- unknown

Rules:

1. Use leave_balance when the user asks about their personal remaining leave balance.
2. Use leave_policy when the user asks about company vacation/leave rules.
3. Use remote_work_policy when the user asks about working remotely.
4. Use password_policy when the user asks about password requirements.
5. Use unknown when the question does not match these categories.

If the user asks for a personal leave balance,
extract the employee ID if explicitly provided.

Set requires_tool=true only for leave_balance.

User question:

{question}
"""

    response = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_schema": IntentResponse,
        },
    )

    return IntentResponse.model_validate_json(response.text)
