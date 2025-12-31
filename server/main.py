import json
from typing import Any, Dict

from flask import Request

# -------------------------
# Internal imports
# -------------------------
from server.speech.recognize import transcribe_audio
from server.nlp.translate import translate_text
from server.nlp.intent import classify_intent
from server.nlp.sql_generator import generate_sql_guarded
from server.data.bigquery_client import dry_run_sql, execute_sql
from server.data.shape_analyzer import analyze_shape
from server.viz.decision import decide_charts_and_layout
from server.optimization.solver import run_optimization_if_needed
from server.utils.validators import validate_request


# -------------------------
# Safe fallback responses
# -------------------------
def _safe_blueprint(page_context: str, summary: str) -> Dict[str, Any]:
    return {
        "page_context": page_context,
        "query_summary": summary,
        "layout": "FULL",
        "slots": [
            {
                "title": "No data",
                "chart_type": "TEXT",
                "data": [],
                "description": "An error occurred or no data is available."
            }
        ],
    }


def _clarification_response(page_context: str, message: str, missing_fields):
    return {
        "page_context": page_context,
        "query_summary": "Clarification needed",
        "layout": "FULL",
        "clarification": {
            "message": message,
            "missing_fields": missing_fields
        },
        "slots": [
            {
                "title": "Clarification required",
                "chart_type": "TEXT",
                "data": [],
                "description": message
            }
        ]
    }


# -------------------------
# Cloud Function entry
# -------------------------
def main(request: Request):
    try:

        payload = request.get_json(silent=True)
        if payload is None:
            return json.dumps(
                _safe_blueprint("UNKNOWN", "Invalid JSON request")
            ), 400, {"Content-Type": "application/json"}


        # -------------------------
        # Validation
        # -------------------------
        ok, error = validate_request(payload)
        if not ok:
            return json.dumps(
                _safe_blueprint(payload.get("page_context", "UNKNOWN"), error)
            ), 400, {"Content-Type": "application/json"}


        audio_b64 = payload["audio_blob"]
        page_context = payload["page_context"]
        language = payload["language"]
        store_id = payload["store_id"]

        # -------------------------
        # Speech → Text
        # -------------------------
        stt = transcribe_audio(audio_b64, language)

        if stt.get("retry_needed"):
            return json.dumps({
                "page_context": page_context,
                "query_summary": "Low speech confidence",
                "layout": "FULL",
                "slots": [
                    {
                        "title": "Retry",
                        "chart_type": "TEXT",
                        "data": [],
                        "description": "Speech confidence too low. Please retry."
                    }
                ]
            }), 200, {"Content-Type": "application/json"}

        transcript = stt.get("transcript", "")
        detected_lang = stt.get("detected_language", language)

        # -------------------------
        # Translate → English
        # -------------------------
        translation = translate_text(transcript, detected_lang, "en")

        normalized_transcript = translation.get(
            "translated_text", transcript
        )

        # -------------------------
        # Intent classification
        # -------------------------
        intent = classify_intent(normalized_transcript)
        if intent.page and intent.page.upper() != page_context:
            page_context = intent.page.upper()

        # Clarification path
        missing_fields = getattr(intent, "missing_fields", [])
        if missing_fields:
            return json.dumps(
                _clarification_response(
                    page_context,
                    "Please clarify your request.",
                    missing_fields
                )
            ), 200, {"Content-Type": "application/json"}

        # -------------------------
        # Handle OPTIMIZATION intents
        # -------------------------
        if intent.intent_type == "OPTIMIZATION":
            return json.dumps({
                "page_context": page_context,
                "query_summary": normalized_transcript,
                "layout": "FULL",
                "slots": [
                    {
                        "title": "Optimization Query",
                        "chart_type": "TEXT",
                        "data": [],
                        "description": "Optimization queries require manual analysis."
                    }
                ]
            }), 200, {"Content-Type": "application/json"}

        # -------------------------
        # SQL generation (ANALYTICS only)
        # -------------------------
        sql = generate_sql_guarded(
            normalized_transcript,
            intent.intent_type,
            page_context,
            store_id
        )

        # -------------------------
        # Dry run
        # -------------------------
        dry_ok, dry_msg = dry_run_sql(sql)

        if not dry_ok:
            return json.dumps(
                _safe_blueprint(page_context, "SQL dry-run failed")
            ), 200, {"Content-Type": "application/json"}

        # -------------------------
        # Execute SQL
        # -------------------------
        exec_ok, rows_or_msg = execute_sql(sql)

        if not exec_ok:
            return json.dumps(
                _safe_blueprint(page_context, "SQL execution failed")
            ), 200, {"Content-Type": "application/json"}

        rows = rows_or_msg

        # -------------------------
        # Shape analysis
        # -------------------------
        shape = analyze_shape(rows)

        # -------------------------
        # Visualization decision
        # -------------------------
        blueprint = decide_charts_and_layout(page_context, shape)

        # -------------------------
        # Final response
        # -------------------------
        blueprint["query_summary"] = normalized_transcript
        blueprint["page_context"] = page_context

        return json.dumps(blueprint), 200, {
            "Content-Type": "application/json"
        }

    except Exception as e:
        print("❌ INTERNAL ERROR:", str(e))
        return json.dumps(
            _safe_blueprint(
                payload.get("page_context", "UNKNOWN")
                if "payload" in locals() else "UNKNOWN",
                "Internal error"
            )
        ), 200, {"Content-Type": "application/json"}


# -------------------------
# Local Flask runner
# -------------------------
if __name__ == "__main__":
    from flask import Flask, request

    app = Flask(__name__)

    @app.route("/", methods=["POST"])
    def root():
        return main(request)

    app.run(port=8080, debug=True)
