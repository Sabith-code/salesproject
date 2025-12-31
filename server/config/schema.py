"""
Page-scoped table and column definitions used to guard SQL generation.
All keys are canonical, lowercase, internal identifiers.
"""

PAGE_TABLES = {
    "sales": {
        "table": "project.dataset.sales_table",
        "default_columns": ["date", "value", "category"],
    },
    "inventory": {
        "table": "project.dataset.inventory_table",
        "default_columns": ["item", "stock"],
    },
    "employees": {
        "table": "project.dataset.workforce_table",
        "default_columns": ["date", "hours_worked", "employee"],
    },
}
