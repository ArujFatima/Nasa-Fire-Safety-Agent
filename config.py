import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Self-contained metadata so there are no missing keys or dictionary errors
NASA_INVESTIGATION_METADATA = {
    "title": "Flame in Freefall: Microgravity Combustion Investigation (PSI-10)",
    "id": "PSI-10",
    "platform": "ISS Destiny Lab / Combustion Integrated Rack (CIR)",
    "summary": """
    The PSI-10 (Flame in Freefall) investigation studies the combustion behavior of fuels in microgravity. 
    Unlike on Earth where buoyancy drives hot gases upward (creating teardrop-shaped flames and convective currents), 
    microgravity eliminates buoyancy-induced convection. This allows researchers to observe spherical, slow-burning, 
    and near-limit diffusion flames that provide critical insights into soot formation, flame extinction limits, 
    and fire safety protocols for spacecraft exploration.
    """,
    "doi": "10.60555/w4zy-bt45",
    "portal_url": "https://foo.nasa.gov/psi-10",
    "pub_link": "https://doi.org/10.60555/w4zy-bt45"
}

SAFETY_SYSTEM_PROMPT = """
You are an expert AI Governance Assistant and Aerospace Safety Auditor for NASA.
Your mission is to evaluate combustion queries against the official PSI-10 investigation records.

Investigation Title: {title}
Mission ID: {id}
Platform: {platform}
Experiment Summary: {summary}

User Query: {user_query}

Instructions:
1. Provide a rigorous, scientifically accurate response based strictly on the experiment summary above.
2. If the query is unrelated to microgravity combustion or NASA safety protocols, trigger a governance refusal and state that the output is INSUFFICIENT for mission deployment.
3. Use clear markdown headings and comparative tables where applicable.
"""

def run_safety_agent(user_query: str):
    try:
        # Safely pull directly from our local dictionary
        prompt = SAFETY_SYSTEM_PROMPT.format(
            title=NASA_INVESTIGATION_METADATA["title"],
            id=NASA_INVESTIGATION_METADATA["id"],
            platform=NASA_INVESTIGATION_METADATA["platform"],
            summary=NASA_INVESTIGATION_METADATA["summary"],
            user_query=user_query
        )
        
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="openai/gpt-oss-120b",
        )
        
        response_text = chat_completion.choices[0].message.content
        
        return {
            "response": response_text,
            "doi": NASA_INVESTIGATION_METADATA["doi"],
            "portal_url": NASA_INVESTIGATION_METADATA["portal_url"],
            "pub_link": NASA_INVESTIGATION_METADATA["pub_link"]
        }
    except Exception as e:
        return {"error": f"Telemetry Error: {str(e)}"}