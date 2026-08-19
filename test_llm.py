import os
from dotenv import load_dotenv
from google import genai

load_dotenv() # Load environment variables from .env file

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Explain what RAG (Retrieval-Augmented Generation) is in simple terms."
)

print(response.text)