import json
import os

import google.generativeai as genai

from server.nlp.intent_schema import Intent, QuerySpec, TimeRange


# --------------------------------------------------
# Gemini configuration
# --------------------------------------------------
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    MODEL = genai.GenerativeModel("gemini-1.5-flash")
else:
    MODEL = None


# --------------------------------------------------
# Prompt (STRICT JSON ONLY)
# --------------------------------------------------
INTENT_PROMPT = """
You are an intent classification engine for a business analytics dashboard.

Return ONLY valid JSON. Do not explain anything.

Allowed intent_type:
- ANALYTICS
- OPTIMIZATION

Allowed page:
- sales
- inventory
- workforce
- null

Rules:
- If the user asks to optimize, allocate, rebalance, or recommend → OPTIMIZATION
- If the user asks to show, analyze, trend, compare → ANALYTICS
- Do NOT guess missing information
- If something is missing, list it under missing_fields

JSON schema:
{
  "intent_type": "ANALYTICS | OPTIMIZATION",
  "page": "sales | inventory | workforce | null",
  "time_range": "last_week | last_month | null",
  "missing_fields": []
}

User query:
\"\"\"{query}\"\"\"
"""


# --------------------------------------------------
# Gemini-based extractor
# --------------------------------------------------
def gemini_extract_intent(transcript: str, language: str = "en") -> Intent:
    if not MODEL:
        raise RuntimeError("Gemini not configured")

    prompt = INTENT_PROMPT.format(query=transcript)

    response = MODEL.generate_content(
        prompt,
        generation_config={
            "temperature": 0,
            "response_mime_type": "application/json",
        },
    )

    data = json.loads(response.text)

    # Time range (optional)
    time_range = None
    if data.get("time_range"):
        time_range = TimeRange(keyword=data["time_range"])

    query = None
    if time_range:
        query = QuerySpec(time_range=time_range)

    print("🤖 Gemini intent extraction used")

    return Intent(
        intent_type=data["intent_type"],
        page=data.get("page"),
        query=query,
        missing_fields=data.get("missing_fields", []),
        confidence=0.9,
    )


# --------------------------------------------------
# Deterministic fallback (NO LLM)
# --------------------------------------------------
def fallback_classify_intent(transcript: str, language: str = "en") -> Intent:
    t = transcript.lower() if transcript else ""

    # OPTIMIZATION
    if any(w in t for w in ["optimize", "allocate", "rebalance", "recommend"]):
        return Intent(
            intent_type="OPTIMIZATION",
            page=_infer_page(t),
            confidence=0.7,
        )

    # ANALYTICS
    time_range = None
    if "last month" in t:
        time_range = TimeRange(keyword="last_month")
    elif "last week" in t:
        time_range = TimeRange(keyword="last_week")

    query = QuerySpec(time_range=time_range) if time_range else None

    return Intent(
        intent_type="ANALYTICS",
        page=_infer_page(t),
        query=query,
        confidence=0.7,
    )


def _infer_page(text: str):
    if "inventory" in text or "stock" in text:
        return "inventory"
    if "employee" in text or "workforce" in text:
        return "workforce"
    if "sale" in text or "revenue" in text:
        return "sales"
    return None


# --------------------------------------------------
# Public entry point (YOU DID THIS RIGHT)
# --------------------------------------------------
def classify_intent(transcript: str, language: str = "en") -> Intent:
    try:
        return gemini_extract_intent(transcript, language)
    except Exception:
        return fallback_classify_intent(transcript, language)
