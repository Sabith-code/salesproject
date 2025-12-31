import os
from typing import Any, Tuple, List


MAX_ROWS = 1000


def dry_run_sql(sql: str) -> Tuple[bool, str]:
    """
    Attempt a dry-run. If BigQuery client is not configured,
    return simulated success with basic safety checks.
    """
    sql_l = sql.lower()

    # Hard safety checks (even in mock mode)
    if "information_schema" in sql_l:
        return False, "Access to information_schema is disallowed"

    if " cross join " in sql_l:
        return False, "CROSS JOIN is disallowed"

    if os.environ.get("BQ_REAL") == "1":
        try:
            from google.cloud import bigquery
            client = bigquery.Client()
            job_config = bigquery.QueryJobConfig(
                dry_run=True,
                use_query_cache=False
            )
            client.query(sql, job_config=job_config)
            return True, "dry-run ok"
        except Exception as e:
            return False, str(e)

    return True, "dry-run simulated ok"


def execute_sql(sql: str) -> Tuple[bool, Any]:
    """
    Execute SQL against BigQuery.

    Returns:
        (ok, rows | error_message)

    In mock mode, returns deterministic rows with consistent schema.
    """
    if os.environ.get("BQ_REAL") == "1":
        try:
            from google.cloud import bigquery
            client = bigquery.Client()
            job = client.query(sql)
            rows = [dict(r) for r in job][:MAX_ROWS]
            return True, rows
        except Exception as e:
            return False, str(e)

    # -------------------------
    # Deterministic mock results
    # -------------------------
    sql_l = sql.lower()

    if "sales" in sql_l or "revenue" in sql_l:
        rows = [
            {"date": "2025-12-01", "value": 1000, "category": "A"},
            {"date": "2025-12-02", "value": 1100, "category": "B"},
        ]

    elif "inventory" in sql_l or "stock" in sql_l:
        rows = [
            {"item": "widget", "stock": 120},
            {"item": "gadget", "stock": 30},
        ]

    elif "employee" in sql_l or "workforce" in sql_l:
        rows = [
            {"employee": "Alice", "hours_worked": 48},
            {"employee": "Bob", "hours_worked": 32},
        ]

    else:
        rows = [
            {"value": 1}
        ]

    return True, rows[:MAX_ROWS]
