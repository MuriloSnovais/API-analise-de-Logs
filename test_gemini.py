import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

key = os.getenv("GEMINI_API_KEY")
print(f"Key Found: {key[:8]}..." if key else "ERROR: No API key found in .env!")

try:
    client = genai.Client(api_key=key)
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents="Respond only with: OK"
    )
    print("Sucess! Response from AI:", response.text)
except Exception as e:
    print("Error returned by Google API:", type(e).__name__, "-", e)