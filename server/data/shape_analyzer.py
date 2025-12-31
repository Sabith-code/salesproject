from typing import Any, Dict, List


def _col_type_samples(rows: List[Dict]) -> Dict[str, str]:
    types: Dict[str, str] = {}

    for row in rows:
        for k, v in row.items():
            if k in types:
                continue

            k_lower = k.lower()

            # Name semantics FIRST
            if any(sub in k_lower for sub in ["date", "day", "time"]):
                types[k] = "TIME"
            elif isinstance(v, (int, float)):
                types[k] = "METRIC"
            else:
                types[k] = "CATEGORY"

    return types


def analyze_shape(rows: List[Dict]) -> Dict[str, Any]:
    """
    Analyze query result rows and classify data shape.

    Returns:
      {
        shape: str,
        columns: {column_name: type},
        sample_rows: [...]
      }
    """

    if not rows:
        return {
            "shape": "TABULAR",
            "columns": {},
            "sample_rows": []
        }

    cols = _col_type_samples(rows)

    metrics = [c for c, t in cols.items() if t == "METRIC"]
    times = [c for c, t in cols.items() if t == "TIME"]
    cats = [c for c, t in cols.items() if t == "CATEGORY"]

    # -------------------------
    # Optimization detection
    # -------------------------
    if any("recommend" in k.lower() for k in cols.keys()):
        shape = "OPTIMIZATION_RESULT"

    # -------------------------
    # KPI: single metric, categories allowed
    # -------------------------
    elif len(metrics) == 1 and not times:
        shape = "KPI_SINGLE"

    # -------------------------
    # Time series
    # -------------------------
    elif times and metrics:
        shape = "TIME_SERIES"

    # -------------------------
    # Category comparison
    # -------------------------
    elif cats and metrics:
        shape = "CATEGORY_COMPARE"

    else:
        shape = "TABULAR"

    return {
        "shape": shape,
        "columns": cols,
        "sample_rows": rows[:5]
    }
