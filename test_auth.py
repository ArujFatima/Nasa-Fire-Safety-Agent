import os
from groq import Groq
from dotenv import load_dotenv

# Load credentials from .env
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

print(f"Loaded API Key: {api_key[:6]}...[HIDDEN]") # Safe print to check if it exists

try:
    client = Groq(api_key=api_key)
    response = client.chat.completions.create(
        messages=[{"role": "user", "content": "Say 'API Connection Successful!'"}],
        model="llama-3.3-70b-versatile",
    )
    print("✅ AUTHENTICATION PASSED:", response.choices.message.content)
except Exception as e:
    print("❌ AUTHENTICATION FAILED:", str(e))