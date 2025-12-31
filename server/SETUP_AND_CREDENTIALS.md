# Setup and Credentials

This file documents the minimum steps and environment needed to run the `server/` Cloud Function and connect to Google Cloud services.

1) GCP Services to enable
   - Cloud Functions (2nd gen recommended)
   - Cloud Build (optional for deployments)
   - BigQuery
   - Cloud Storage (if uploading audio blobs separately)

2) IAM Roles
   - Service account used by the Cloud Function should have:
     - BigQuery Job User (`roles/bigquery.jobUser`)
     - BigQuery Data Viewer (`roles/bigquery.dataViewer`) for read-only queries
     - Cloud Functions Invoker as needed for calling endpoints

3) Environment variables (set in Cloud Function configuration)
   - `BQ_REAL` (optional): set to `1` to enable real BigQuery calls with the runtime credentials.
   - `OPENAI_API_KEY` (optional): for Gemini integrations (not included in scaffold). Do NOT store secrets in source.

4) API Keys / Credentials
   - Provide Google credentials to Cloud Functions by using the function's service account. Locally, set `GOOGLE_APPLICATION_CREDENTIALS` to a service account JSON if testing.
   - If integrating with Gemini or other LLMs, create API keys and store them in Secret Manager or as environment variables (follow least privilege).

5) BigQuery setup
   - Create datasets and tables matching `server/config/schema.py` or update `PAGE_TABLES` to reflect your project/dataset/table names.
   - Grant the function's service account `bigquery.dataViewer` and `bigquery.jobUser` on the project/dataset.

6) Deployment notes
   - Use `gcloud functions deploy` with Python runtime and set the entry point to `server.main.main`.
   - Example:

```powershell
gcloud functions deploy analytics_voice --gen2 --region=us-central1 --runtime=python310 --entry-point=main --source=server --set-env-vars=BQ_REAL=0
```

7) Security
   - Do not embed API keys in source. Use Secret Manager and grant access to the function's service account.
   - Limit BigQuery table access using row-level or column-level policies where appropriate.
