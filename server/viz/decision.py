from typing import Any, Dict, List


SHAPE_TO_CHART = {
    "KPI_SINGLE": ["KPI"],
    "TIME_SERIES": ["LINE"],
    "CATEGORY_COMPARE": ["BAR"],
    "TABULAR": ["TABLE"],
    "OPTIMIZATION_RESULT": ["TEXT", "BAR"],
}


def decide_charts_and_layout(
    page_context: str,
    shape_info: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Deterministic, rule-based decision of chart types and layout.

    Returns a blueprint partial with:
    - layout
    - slots (title, chart_type, data, description)
    """

    shape = shape_info.get("shape", "TABULAR")
    charts = SHAPE_TO_CHART.get(shape, ["TABLE"])
    sample_rows = shape_info.get("sample_rows", [])

    slots: List[Dict[str, Any]] = []

    for c in charts:
        title, description = _build_slot_metadata(
            page_context, shape, c
        )

        slots.append({
            "title": title,
            "chart_type": c,
            "data": sample_rows,
            "description": description,
        })

    # -------------------------
    # Layout rules
    # -------------------------
    n = len(slots)
    if n == 1:
        layout = "FULL"
    elif n == 2:
        layout = "SPLIT"
    else:
        layout = "GRID"

    return {
        "layout": layout,
        "slots": slots
    }


# --------------------------------------------------
# Slot metadata helpers
# --------------------------------------------------
def _build_slot_metadata(
    page_context: str,
    shape: str,
    chart_type: str
) -> (str, str):

    page_label = page_context.capitalize()

    if shape == "KPI_SINGLE":
        return (
            f"{page_label} KPI",
            f"Key performance indicator for {page_context}."
        )

    if shape == "TIME_SERIES":
        return (
            f"{page_label} Trend",
            f"Trend over time for {page_context}."
        )

    if shape == "CATEGORY_COMPARE":
        return (
            f"{page_label} Comparison",
            f"Comparison across categories for {page_context}."
        )

    if shape == "OPTIMIZATION_RESULT":
        if chart_type == "TEXT":
            return (
                "Optimization Recommendation",
                "Suggested action based on current data."
            )
        return (
            "Optimization Support Data",
            "Data supporting the optimization recommendation."
        )

    # Default / TABULAR
    return (
        f"{page_label} Data",
        f"Detailed data view for {page_context}."
    )
