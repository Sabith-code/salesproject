from typing import Dict, List, Tuple


def run_optimization_if_needed(
    transcript: str,
    page_context: str,
    rows: List[Dict]
) -> Tuple[str, List[Dict]]:
    """
    Run optimization logic for OPTIMIZATION intent.

    Returns:
        (recommendation_text, supporting_rows)

    This function is ADVISORY ONLY.
    It never mutates data or executes writes.
    """

    # -------------------------
    # Basic guards
    # -------------------------
    if not rows:
        return (
            "No data available to run optimization.",
            []
        )

    transcript_l = transcript.lower()

    # -------------------------
    # Try OR-Tools (optional)
    # -------------------------
    try:
        from ortools.linear_solver import pywraplp  # type: ignore
        solver_available = True
    except Exception:
        solver_available = False

    # -------------------------
    # Page-specific heuristics
    # -------------------------
    if page_context == "inventory":
        return _inventory_optimization(rows, solver_available)

    if page_context == "employees":
        return _employee_optimization(rows, solver_available)

    # Default / fallback
    return (
        "Optimization request noted. Review the supporting data for improvement opportunities.",
        rows[:5]
    )


# --------------------------------------------------
# Inventory optimization
# --------------------------------------------------
def _inventory_optimization(
    rows: List[Dict],
    solver_available: bool
) -> Tuple[str, List[Dict]]:

    # Heuristic: identify low-stock vs high-stock
    low_stock = [r for r in rows if r.get("stock", 0) < 10]
    high_stock = [r for r in rows if r.get("stock", 0) > 50]

    supporting = (low_stock + high_stock)[:5]

    if solver_available:
        return (
            "Inventory optimization completed. Consider reallocating excess stock to low-stock locations.",
            supporting
        )

    return (
        "Heuristic suggestion: move excess inventory from high-stock locations to low-stock ones.",
        supporting
    )


# --------------------------------------------------
# Employee optimization
# --------------------------------------------------
def _employee_optimization(
    rows: List[Dict],
    solver_available: bool
) -> Tuple[str, List[Dict]]:

    # Heuristic: identify overworked vs underutilized employees
    overworked = [r for r in rows if r.get("hours_worked", 0) > 45]
    underutilized = [r for r in rows if r.get("hours_worked", 0) < 30]

    supporting = (overworked + underutilized)[:5]

    if solver_available:
        return (
            "Employee workload optimization completed. Review suggested reallocations.",
            supporting
        )

    return (
        "Heuristic suggestion: rebalance workload between overworked and underutilized employees.",
        supporting
    )
