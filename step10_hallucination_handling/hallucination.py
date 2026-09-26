import os

from dotenv import load_dotenv
from google import genai


# --------------------------------------------------
# Load API key
# --------------------------------------------------

load_dotenv("../step1_llm/.env")

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY was not found in .env")


# --------------------------------------------------
# Gemini client
# --------------------------------------------------

client = genai.Client(api_key=api_key)


# --------------------------------------------------
# Company knowledge
# --------------------------------------------------

company_context = """
COMPANY LEAVE POLICY

Employees receive 24 annual vacation days every calendar year.

Employees should submit vacation requests through their manager
at least five working days before the requested leave.

Unused vacation days can be carried forward to the following year,
subject to company approval.

REMOTE WORK POLICY

Employees can work remotely up to two days per week with manager
approval.

Employees working remotely must remain available during normal
working hours.

Employees must attend important meetings regardless of whether
they are working remotely.

PASSWORD SECURITY POLICY

Employees must change their company password every 90 days.

Passwords must contain uppercase letters, lowercase letters,
numbers, and special characters.

Employees must never share their passwords with another person.
"""


# --------------------------------------------------
# User question
# --------------------------------------------------

question = "Does the company provide dental insurance?"


# --------------------------------------------------
# Grounded prompt
# --------------------------------------------------

prompt = f"""
You are an enterprise company assistant.

Your job is to answer employee questions using ONLY
the company information provided below.

Rules:

1. Use only the provided company information.
2. Do not use outside knowledge.
3. Do not invent company policies.
4. Do not guess.
5. If the answer is not explicitly supported by the
   company information, say exactly:

"I couldn't find this information in the available company policies."

Company information:

{company_context}


Employee question:

{question}
"""


# --------------------------------------------------
# Generate response
# --------------------------------------------------

response = client.models.generate_content(
    model="gemini-3.5-flash",
    contents=prompt,
)


# --------------------------------------------------
# Display result
# --------------------------------------------------

print("=" * 60)
print("QUESTION")
print("=" * 60)

print(question)

print("\n" + "=" * 60)
print("MODEL RESPONSE")
print("=" * 60)

print(response.text)