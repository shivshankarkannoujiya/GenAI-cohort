from dotenv import load_dotenv
from google import genai
from google.genai import types
import os

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)
response = client.models.generate_content(
    model="gemini-2.0-flash-001",
    contents=["why is the sky blue?"]
)

print(response.text)