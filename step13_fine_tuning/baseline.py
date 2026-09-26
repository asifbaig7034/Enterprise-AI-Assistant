import os
from dotenv import load_dotenv
from google import genai

load_dotenv("../step1_llm/.env")

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY was not found")

client = genai.Client(api_key=api_key)


test_questions = [
    "How many vacation days do I have?",
    "What is the company's vacation policy?",
    "Can I work from home?",
    "How often should I change my password?"
]

correct_answers = [
    "leave_balance",
    "leave_policy",
    "remote_work_policy",
    "password_policy"
]


prompt = """
Classify the employee question into exactly one of these intents:

leave_balance
leave_policy
remote_work_policy
password_policy

Return ONLY the intent name.

Question:
"""


correct = 0

for question, expected in zip(test_questions, correct_answers):

    response = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=prompt + question
    )

    predicted = response.text.strip().lower()

    print("=" * 60)
    print("Question:", question)
    print("Predicted:", predicted)
    print("Expected:", expected)

    if predicted == expected:
        correct += 1


accuracy = correct / len(test_questions)

print("=" * 60)
print("BASELINE RESULTS")
print("=" * 60)
print("Correct:", correct)
print("Total:", len(test_questions))
print("Accuracy:", accuracy)