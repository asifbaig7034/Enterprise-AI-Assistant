import os

from dotenv import load_dotenv
from google import genai
from pydantic import BaseModel
from typing import Literal

load_dotenv("../step1_llm/.env")

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY was not found in .env")

client = genai.Client(api_key=api_key)


class EmployeeRequest(BaseModel):
    intent: Literal[
        "leave_balance",
        "leave_policy",
        "employee_details",
        "unknown"
    ]
    employee_id: str
    requires_tool: bool


user_question = "How many vacation days does EMP001 have?"

response = client.models.generate_content(
    model="gemini-3.8-flash",
    contents=user_question,
    config={
        "response_mime_type": "application/json",
        "response_schema": EmployeeRequest,
    },
)

print("=" * 60)
print("RAW MODEL RESPONSE")
print("=" * 60)

print(response.text)


print("\n" + "=" * 60)
print("STRUCTURED OUTPUT")
print("=" * 60)

request = EmployeeRequest.model_validate_json(response.text)

print("Intent:", request.intent)
print("Employee ID:", request.employee_id)
print("Requires Tool:", request.requires_tool)


print("\n" + "=" * 60)
print("PYDANTIC OBJECT")
print("=" * 60)

print(request)