# Architecture Notes

This document explains the server-side pipeline, guardrails, and frontend integration contract for the voice-driven analytics Cloud Function.

Overview
- Single Cloud Function entrypoint: `main` in `server/main.py`.
- Pipeline (fixed order): Speech -> Language normalize -> Intent classify -> SQL generate -> SQL dry-run -> BigQuery execute -> Data shape analyze -> Visualization decision -> Optimization (optional) -> Blueprint response

Key guardrails
- All SQL generated is SELECT-only and scoped to page-specific tables defined in `server/config/schema.py`.
- Every query includes a `store_id` filter.
- Dry-run is performed before execution; failures return a safe blueprint.
- Visualization decisions are rule-based (no AI choosing charts).

Determinism and safety
- The scaffold provides deterministic fallbacks when external services (Speech, BigQuery, Gemini, OR-Tools) are not available.
- The Cloud Function never returns raw exceptions or internal traces. Errors map to a safe blueprint JSON.

Output contract (strict)
- The function returns exactly one JSON object with the required fields:
  - `page_context`, `query_summary`, `layout`, `slots[]` and optional `recommendation`.
- Each slot includes `title`, `chart_type`, `data`, and optional `description`.

Frontend integration
- The frontend can POST an HTTP request with JSON body containing `audio_blob` (base64), `page_context`, `language`, and `store_id`.
- The response is a deterministic blueprint; the frontend should render charts using the provided `chart_type` and `data` without relying on additional instructions.

Extensibility
- Replace `server/speech/recognize.py` implementation with real Google Speech-to-Text (Chirp 3) call.
- Replace `server/nlp/intent.py` classifier to call Gemini — keep the classifier limited to intent classification only.
- Replace `server/data/bigquery_client.py` simulated behavior by setting `BQ_REAL=1` and ensuring the function's service account has BigQuery permissions.
