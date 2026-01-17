import json
from core.llm_client import call_llm
from core.versemind_prompt import build_prompt
from core.versemind_schema import validate_proposal_schema
from core.validator import validate_action


def fallback(reason):
    return {
        "type": "suggestion",
        "payload": {},
        "explanation": reason,
        "confidence": 0.05
    }


def propose(canon, intent_text):
    try:
        system_prompt, user_prompt = build_prompt(canon, intent_text)
        raw = call_llm(system_prompt, user_prompt)
        proposal = json.loads(raw)
    except Exception as e:
        return fallback(f"LLM failure: {e}")

    if not validate_proposal_schema(proposal):
        return fallback("Invalid proposal schema")

    # Dry-run validation for events
    if proposal["type"] == "event":
        blocked = validate_action(
            action={
                "type": "event",
                "value": proposal["payload"].get("name", "")
            },
            canon=canon,
            context={
                "act": proposal["payload"].get("act", 0)
            }
        )

        if blocked:
            proposal["confidence"] *= 0.5
            proposal["explanation"] += (
                "\n⚠ Conflicts with existing canon rules."
            )

    return proposal
