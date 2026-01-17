import json

def build_prompt(canon, intent_text):
    canon_summary = {
        "meta": canon.meta,
        "truths": canon.truths,
        "rules": canon.rules[-5:],   # last 5 rules only
        "recent_events": canon.events[-5:]
    }

    system_prompt = """
You are VerseMind, an AI narrative architect.

Rules:
- You NEVER modify canon directly
- You ONLY propose structured changes
- Output VALID JSON ONLY
- Follow the exact schema
- Respect canon truths and rules
- If intent conflicts with canon, lower confidence and explain
- If uncertain, return type = "suggestion"

Allowed types:
- event
- rule
- suggestion
"""

    user_prompt = f"""
CANON SUMMARY:
{json.dumps(canon_summary, indent=2)}

USER INTENT:
\"{intent_text}\"

OUTPUT FORMAT (JSON ONLY):

{{
  "type": "event | rule | suggestion",
  "payload": {{}},
  "explanation": "string",
  "confidence": 0.0
}}
"""

    return system_prompt.strip(), user_prompt.strip()
