def calculate_change(current, previous):
    if current is None or previous is None:
        return None

    if previous == 0:
        return None

    return round(((current - previous) / abs(previous)) * 100, 2)


def determine_trend(current, previous):
    if current is None or previous is None:
        return "no_data"

    if current > previous:
        return "up"
    elif current < previous:
        return "down"
    else:
        return "flat"


def determine_signal(section, label, change_pct):
    """
    Financial logic for interpreting change
    """

    if change_pct is None:
        return "neutral"

    # ASSETS
    if section == "assets":
        return "positive" if change_pct > 0 else "negative"

    # EQUITY
    if section == "equity":
        return "positive" if change_pct > 0 else "negative"

    # LIABILITIES
    if section == "liabilities":
        if "borrow" in label.lower():
            return "negative" if change_pct > 0 else "positive"
        return "neutral"

    return "neutral"


def analyze_balance_sheet(balance_sheet_json):
    """
    Enhances selected metrics with:
    - change_pct
    - trend
    - signal
    """

    for section in ["assets", "liabilities", "equity"]:
        for item in balance_sheet_json.get(section, []):
            current = item.get("current_value")
            previous = item.get("previous_value")

            change_pct = calculate_change(current, previous)
            trend = determine_trend(current, previous)
            signal = determine_signal(section, item["label"], change_pct)

            item["change_pct"] = change_pct
            item["trend"] = trend
            item["signal"] = signal

    return balance_sheet_json