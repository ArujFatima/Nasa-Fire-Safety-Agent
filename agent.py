import os
from groq import Groq
from dotenv import load_dotenv
from config import SAFETY_SYSTEM_PROMPT, NASA_INVESTIGATION_METADATA

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

MODELS = ["openai/gpt-oss-120b", "openai/gpt-oss-20b"]

def run_safety_agent(user_query: str):
    prompt = SAFETY_SYSTEM_PROMPT.format(
        title=NASA_INVESTIGATION_METADATA["title"],
        id=NASA_INVESTIGATION_METADATA["id"],
        platform=NASA_INVESTIGATION_METADATA["platform"],
        summary=NASA_INVESTIGATION_METADATA["summary"],
        user_query=user_query
    )

    last_error = None
    for model in MODELS:
        try:
            chat_completion = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=model,
                temperature=0,
            )
            return {
                "response": chat_completion.choices[0].message.content,
                "model_used": model,
                "doi": NASA_INVESTIGATION_METADATA["doi"],
                "portal_url": NASA_INVESTIGATION_METADATA["portal_url"],
                "pub_link": NASA_INVESTIGATION_METADATA["pub_link"]
            }
        except Exception as e:
            last_error = e

    return {"error": f"Telemetry Error: {last_error}"}