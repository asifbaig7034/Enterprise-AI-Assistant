import os

from dotenv import load_dotenv
from google import genai


# ============================================================
# SETUP
# ============================================================

# Load the .env file from Step 1
load_dotenv("../step1_llm/.env")

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY was not found")

client = genai.Client(api_key=api_key)


def ask_llm(prompt):
    """
    Send a prompt to Gemini and return the response.
    """

    response = client.interactions.create(
        model="gemini-3.8-flash",
        input=prompt
    )

    return response.output_text


# ============================================================
# EXPERIMENT 1
# BASIC PROMPT
# ============================================================

print("\n" + "=" * 70)
print("EXPERIMENT 1: BASIC PROMPT")
print("=" * 70)

prompt = """
Explain machine learning.
"""

response = ask_llm(prompt)

print(response)


# ============================================================
# EXPERIMENT 2
# ROLE PROMPTING
# ============================================================

print("\n" + "=" * 70)
print("EXPERIMENT 2: ROLE PROMPTING")
print("=" * 70)

prompt = """
You are an experienced machine learning instructor.

Explain machine learning.
"""

response = ask_llm(prompt)

print(response)


# ============================================================
# EXPERIMENT 3
# ROLE + CONTEXT + CONSTRAINTS
# ============================================================

print("\n" + "=" * 70)
print("EXPERIMENT 3: ROLE + CONTEXT + CONSTRAINTS")
print("=" * 70)

prompt = """
You are an experienced machine learning instructor.

The student understands basic Python
but has never studied machine learning.

Explain machine learning.

Requirements:
- Use simple English.
- Explain the basic idea.
- Give two real-world examples.
- Explain supervised learning.
- Explain unsupervised learning.
- Keep the answer below 200 words.
"""

response = ask_llm(prompt)

print(response)


# ============================================================
# EXPERIMENT 4
# ZERO-SHOT CLASSIFICATION
# ============================================================

print("\n" + "=" * 70)
print("EXPERIMENT 4: ZERO-SHOT PROMPTING")
print("=" * 70)

prompt = """
Classify the following customer review as:

positive
negative
neutral

Review:
"The product arrived yesterday and works perfectly."

Return only the classification.
"""

response = ask_llm(prompt)

print(response)


# ============================================================
# EXPERIMENT 5
# ONE-SHOT PROMPTING
# ============================================================

print("\n" + "=" * 70)
print("EXPERIMENT 5: ONE-SHOT PROMPTING")
print("=" * 70)

prompt = """
Classify customer reviews as positive, negative, or neutral.

Example:

Review:
"The product is excellent and works perfectly."

Classification:
positive

Now classify:

Review:
"The delivery was late and the packaging was damaged."

Return only the classification.
"""

response = ask_llm(prompt)

print(response)


# ============================================================
# EXPERIMENT 6
# FEW-SHOT PROMPTING
# ============================================================

print("\n" + "=" * 70)
print("EXPERIMENT 6: FEW-SHOT PROMPTING")
print("=" * 70)

prompt = """
Classify customer reviews as positive, negative, or neutral.

Example 1:

Review:
"The product is amazing and works perfectly."

Classification:
positive


Example 2:

Review:
"The product broke after two days."

Classification:
negative


Example 3:

Review:
"The product is okay, nothing special."

Classification:
neutral


Now classify:

Review:
"The delivery was fast and the product quality is excellent."

Return only:
positive
negative
or
neutral
"""

response = ask_llm(prompt)

print(response)


# ============================================================
# EXPERIMENT 7
# OUTPUT FORMAT CONTROL
# ============================================================

print("\n" + "=" * 70)
print("EXPERIMENT 7: OUTPUT FORMAT")
print("=" * 70)

prompt = """
Analyze this customer review:

"The laptop is excellent. The battery lasts a long time,
but the keyboard could be better."

Return exactly this format:

Sentiment: <positive/negative/neutral>
Main Issue: <short answer>
Positive Point: <short answer>
"""

response = ask_llm(prompt)

print(response)


# ============================================================
# EXPERIMENT 8
# JSON OUTPUT INSTRUCTION
# ============================================================

print("\n" + "=" * 70)
print("EXPERIMENT 8: JSON OUTPUT")
print("=" * 70)

prompt = """
Analyze the following customer review:

"The phone has a great camera and excellent battery life,
but it is slightly expensive."

Return ONLY valid JSON.

Required format:

{
    "sentiment": "positive",
    "positive_points": [],
    "negative_points": []
}
"""

response = ask_llm(prompt)

print(response)


# ============================================================
# EXPERIMENT 9
# CONSTRAINTS
# ============================================================

print("\n" + "=" * 70)
print("EXPERIMENT 9: CONSTRAINTS")
print("=" * 70)

prompt = """
Explain deep learning.

Follow these rules:

1. Use exactly 5 bullet points.
2. Each bullet must contain one sentence.
3. Use simple English.
4. Do not use technical jargon.
5. Keep the entire answer below 100 words.
"""

response = ask_llm(prompt)

print(response)


# ============================================================
# EXPERIMENT 10
# DYNAMIC PROMPT TEMPLATE
# ============================================================

print("\n" + "=" * 70)
print("EXPERIMENT 10: PROMPT TEMPLATE")
print("=" * 70)

topic = "Retrieval-Augmented Generation"

audience = "beginner AI/ML student"

prompt = f"""
You are an AI/ML instructor.

Explain the following topic:

Topic:
{topic}

Target audience:
{audience}

Requirements:
- Use simple English.
- Give a definition.
- Explain why it is useful.
- Give one practical example.
- Keep the answer below 150 words.
"""

response = ask_llm(prompt)

print(response)


print("\n" + "=" * 70)
print("ALL EXPERIMENTS COMPLETED")
print("=" * 70)