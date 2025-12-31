from typing import Dict


def translate_text(text: str, source_lang: str, target_lang: str = "en") -> Dict:
    """
    Language normalization layer.

    NOTE:
    - Gemini can handle multilingual input directly.
    - We keep this function to preserve the pipeline and metadata.
    - No fake translation is performed.
    """

    if not text:
        return {
            "translated_text": "",
            "original_text": text,
            "source_lang": source_lang,
            "target_lang": target_lang,
            "translated": False
        }

    # If already English or target language, passthrough
    if source_lang and source_lang.lower().startswith(target_lang):
        return {
            "translated_text": text,
            "original_text": text,
            "source_lang": source_lang,
            "target_lang": target_lang,
            "translated": False
        }

    # DO NOT fake translation
    # Let Gemini handle multilingual understanding
    return {
        "translated_text": text,
        "original_text": text,
        "source_lang": source_lang,
        "target_lang": target_lang,
        "translated": False
    }
