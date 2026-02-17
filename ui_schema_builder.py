import json

# ----------------------------------------
# Number Formatting
# ----------------------------------------

def format_currency(value, currency="INR"):
    """
    Converts raw numbers into Crores for Indian companies
    Example: 44560480400000 -> ₹4,45,604.80 Cr
    """

    if value is None:
        return "—"

    crore_value = value / 10_000_000  # 1 crore = 10 million
    return f"₹{crore_value:,.2f} Cr"


def format_percentage(value):
    if value is None:
        return "—"
    return f"{value:.2f}%"


# ----------------------------------------
# Build UI Metric Object
# ----------------------------------------

def build_metric_ui(metric):
    """
    Converts analyzed metric into UI-ready metric object
    """

    return {
        "label": metric.get("label"),
        "current": format_currency(metric.get("current_value")),
        "previous": format_currency(metric.get("previous_value")),
        "change_pct": format_percentage(metric.get("change_pct")),
        "trend": metric.get("trend"),
        "signal": metric.get("signal")
    }


# ----------------------------------------
# Build Final UI Schema
# ----------------------------------------

def build_ui_schema(analyzed_json):
    """
    Converts analyzed balance sheet JSON
    into UI-ready schema for rendering.
    """

    # ✅ periods is now a dict (NOT a list)
    raw_periods = analyzed_json.get("periods", {})

    periods = {
        "current": raw_periods.get("current"),
        "previous": raw_periods.get("previous")
    }

    ui_schema = {
        "company": analyzed_json.get("company"),
        "periods": periods,
        "sections": []
    }

    # Build sections
    for section_name in ["assets", "liabilities", "equity"]:

        section_metrics = analyzed_json.get(section_name, [])

        ui_section = {
            "section_title": section_name.capitalize(),
            "metrics": [build_metric_ui(metric) for metric in section_metrics]
        }

        ui_schema["sections"].append(ui_section)

    return ui_schema


# ----------------------------------------
# Optional: Save JSON
# ----------------------------------------

def save_ui_json(ui_schema, output_path="data/ui_balance_sheet.json"):
    with open(output_path, "w") as f:
        json.dump(ui_schema, f, indent=4)

    print(f"UI schema saved to {output_path}")