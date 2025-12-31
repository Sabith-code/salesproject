import base64
import os
from typing import Dict


USE_REAL_STT = os.environ.get("USE_REAL_STT", "0") == "1"


def _mock_transcribe(audio_bytes: bytes, language_hint: str) -> Dict:
    """
    Deterministic mock transcription.

    The transcript content is stable but realistic,
    making downstream intent testing meaningful.
    """
    length = len(audio_bytes)

    if length % 3 == 0:
        transcript = "show last month sales by region"
        confidence = 0.94
    elif length % 3 == 1:
        transcript = "optimize inventory allocation"
        confidence = 0.90
    else:
        transcript = "show employee performance"
        confidence = 0.88

    return {
        "transcript": transcript,
        "confidence": confidence,
        "detected_language": language_hint,
        "retry_needed": confidence < 0.75,
    }


def transcribe_audio(audio_b64: str, language: str) -> Dict:
    """
    Transcribe audio blob (base64).

    If USE_REAL_STT=1 and Google Speech-to-Text is available,
    this function can be extended to call the real API.
    Otherwise, a deterministic mock is returned.
    """
    try:
        audio_bytes = base64.b64decode(audio_b64)
    except Exception:
        return {
            "transcript": "",
            "confidence": 0.0,
            "detected_language": language,
            "retry_needed": True,
        }

    # Explicit mock path (current default)
    if not USE_REAL_STT:
        return _mock_transcribe(audio_bytes, language)

    # Placeholder for real STT integration
    # (intentionally not implemented here)
    return _mock_transcribe(audio_bytes, language)
