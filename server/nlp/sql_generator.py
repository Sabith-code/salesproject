from typing import List

from server.config.schema import PAGE_TABLES


class UnsafeSQLError(Exception):
    pass


# -------------------------------
# Safety guards
# -------------------------------
def _ensure_select_only(sql: str):
    forbidden = [";", "delete", "update", "insert", "drop", "alter", "create"]
    for token in forbidden:
        if token.lower() in sql.lower():
            raise UnsafeSQLError("Only SELECT queries are allowed")


# -------------------------------
# Time filter builder
# -------------------------------
def _build_time_clause(time_range) -> str:
    if not time_range:
        return "1=1"

    if time_range.keyword == "last_month":
        return (
            "date >= DATE_SUB(CURRENT_DATE(), INTERVAL 1 MONTH) "
            "AND date < CURRENT_DATE()"
        )

    if time_range.keyword == "last_week":
        return (
            "date >= DATE_SUB(CURRENT_DATE(), INTERVAL 7 DAY) "
            "AND date < CURRENT_DATE()"
        )

    if time_range.keyword == "today":
        return "date = CURRENT_DATE()"

    return "1=1"


# -------------------------------
# Main SQL generator
# -------------------------------
def generate_sql_guarded(transcript: str, intent_type: str, page_context: str, store_id: str) -> str:
    """
    Deterministically generate a SELECT-only SQL query from a validated Intent.
    """

    if intent_type != "ANALYTICS":
        raise ValueError("SQL generation only supported for ANALYTICS intent")

    if page_context not in PAGE_TABLES:
        raise ValueError("Unknown page")

    table_cfg = PAGE_TABLES[page_context]
    table = table_cfg["table"]

    # For now, return a safe default query
    # In production, would parse the transcript more thoroughly
    select_parts = table_cfg.get("default_columns", ["*"])

    where_parts: List[str] = [f"store_id = '{store_id}'"]

    sql = (
        f"SELECT {', '.join(select_parts)} "
        f"FROM `{table}` "
        f"WHERE {' AND '.join(where_parts)} "
        f"LIMIT 1000"
    )

    _ensure_select_only(sql)
    return sql
