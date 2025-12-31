from dataclasses import dataclass
from typing import List, Optional


@dataclass
class TimeRange:
    keyword: Optional[str] = None
    type: Optional[str] = None
    start: Optional[str] = None
    end: Optional[str] = None


@dataclass
class VisualizationSpec:
    preferred: str = "auto"
    confidence: float = 0.0


@dataclass
class QuerySpec:
    metric: Optional[str] = None
    aggregation: Optional[str] = None
    dimensions: List[str] = None
    filters: List = None
    time_range: Optional[TimeRange] = None
    limit: Optional[int] = 1000
    sort: Optional[dict] = None


@dataclass
class Intent:
    intent_type: str                 # ANALYTICS | OPTIMIZATION
    page: Optional[str] = None       # sales | inventory | employees
    query: Optional[QuerySpec] = None
    visualization: Optional[VisualizationSpec] = None
    confidence: float = 0.0
    raw_text: Optional[str] = None
    language: Optional[str] = None
    missing_fields: Optional[List[str]] = None
