import os

from dotenv import load_dotenv
from google import genai

# Load environment variables
load_dotenv()

# Get Gemini API key
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY was not found in .env")

print("API key found:", True)
print("API key prefix:", api_key[:10])

# Create Gemini client
client = genai.Client(api_key=api_key)

# Generate response using the current Interactions API
interaction = client.interactions.create(
    model="gemini-3.8-flash",
    input="Explain machine learning in simple words."
)

print("\nGemini Response:")
print(interaction.output_text)