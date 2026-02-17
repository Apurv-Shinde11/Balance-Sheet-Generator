"""
Selects and structures key balance sheet metrics
into categorized sections for analysis + UI.
"""

# ----------------------------------------
# Metric Mapping (Raw → UI Label + Section)
# ----------------------------------------

METRIC_MAP = {

    # ---------------- ASSETS ----------------
    "Total Assets": ("Total Assets", "assets"),
    "Cash And Cash Equivalents": ("Cash & Cash Equivalents", "assets"),
    "Net PPE": ("Net Property, Plant & Equipment", "assets"),
    "Investments And Advances": ("Investments", "assets"),

    # ---------------- LIABILITIES ----------------
    "Total Liabilities Net Minority Interest": ("Total Liabilities", "liabilities"),
    "Total Debt": ("Borrowings", "liabilities"),
    "Current Debt": ("Short Term Borrowings", "liabilities"),
    "Long Term Debt": ("Long Term Borrowings", "liabilities"),

    # ---------------- EQUITY ----------------
    "Stockholders Equity": ("Total Equity", "equity"),
    "Common Stock": ("Share Capital", "equity"),
    "Retained Earnings": ("Reserves & Surplus", "equity"),
}


# ----------------------------------------
# Core Selector Function
# ----------------------------------------

def select_balance_sheet_metrics(structured_data: dict) -> dict:
    """
    Converts structured data into section-wise JSON
    compatible with analyzer.py

    Includes debug print of available raw metrics.
    """

    periods_list = structured_data.get("periods", [])
    data = structured_data.get("data", {})

    # ----------------------------------------
    # DEBUG: Print available raw metrics
    # ----------------------------------------
    print("\nAvailable metrics in structured data:")
    for key in data.keys():
        print(f" - {key}")
    print("-" * 50)

    # Extract current & previous periods
    current_period = periods_list[0] if len(periods_list) > 0 else None
    previous_period = periods_list[1] if len(periods_list) > 1 else None

    output = {
        "periods": {
            "current": current_period,
            "previous": previous_period
        },
        "assets": [],
        "liabilities": [],
        "equity": []
    }

    # ----------------------------------------
    # Metric Selection
    # ----------------------------------------
    for raw_metric, (ui_label, section) in METRIC_MAP.items():

        if raw_metric in data:
            values = data[raw_metric]
            print(f"✓ Found: {raw_metric}")
        else:
            values = [None] * len(periods_list)
            print(f"✗ Missing: {raw_metric}")

        current_value = values[0] if len(values) > 0 else None
        previous_value = values[1] if len(values) > 1 else None

        metric_object = {
            "label": ui_label,
            "current_value": current_value,
            "previous_value": previous_value
        }

        output[section].append(metric_object)

    print("=" * 60)

    return output