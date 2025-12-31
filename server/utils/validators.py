from typing import Any, Dict, Tuple


ALLOWED_PAGES = {
    "sales": "sales",
    "inventory": "inventory",
    "workforce": "employees",   # map external → internal
    "employees": "employees"
}


def validate_request(payload: Dict[str, Any]) -> Tuple[bool, str]:
    required = ["audio_blob", "page_context", "language", "store_id"]
    for r in required:
        if r not in payload:
            return False, f"Missing required field: {r}"

    # -------------------------
    # Normalize page_context
    # -------------------------
    page_raw = payload.get("page_context")
    if not isinstance(page_raw, str):
        return False, "page_context must be a string"

    page_norm = page_raw.strip().lower()
    if page_norm not in ALLOWED_PAGES:
        return False, "Invalid page_context"

    # Mutate payload safely (canonical form)
    payload["page_context"] = ALLOWED_PAGES[page_norm]

    # -------------------------
    # audio_blob validation
    # -------------------------
    audio_blob = payload.get("audio_blob")
    if not isinstance(audio_blob, str) or len(audio_blob) < 10:
        return False, "audio_blob appears invalid"

    # -------------------------
    # language validation (light)
    # -------------------------
    lang = payload.get("language")
    if not isinstance(lang, str) or len(lang) < 2:
        return False, "Invalid language code"

    # -------------------------
    # store_id validation
    # -------------------------
    store_id = payload.get("store_id")
    if not isinstance(store_id, str) or not store_id:
        return False, "Invalid store_id"

    return True, "ok"
