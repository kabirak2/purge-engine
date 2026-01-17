import requests
import re

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3"


def call_llm(system_prompt, user_prompt):
    prompt = f"""
{system_prompt}

IMPORTANT RULES:
- Respond with VALID JSON ONLY
- Do NOT include explanations outside JSON
- Do NOT use markdown
- Do NOT add comments

{user_prompt}
"""

    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
        "temperature": 0.2
    }

    response = requests.post(OLLAMA_URL, json=payload)
    response.raise_for_status()

    text = response.json().get("response", "").strip()

    # Extract first JSON object defensively
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        raise ValueError("No JSON object found in LLM output")

    return match.group(0)
