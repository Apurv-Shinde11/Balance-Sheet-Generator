from pathlib import Path
import json

from data_fetcher import get_balance_sheet
from preprocessor import preprocess_balance_sheet
from metric_selector import select_balance_sheet_metrics
from analyzer import analyze_balance_sheet
from ui_schema_builder import build_ui_schema
from html_renderer import main as render_html


# -----------------------------------------
# CONFIG
# -----------------------------------------

OUTPUT_JSON_PATH = Path("data/ui_balance_sheet.json")
OUTPUT_HTML_PATH = Path("data/balance_sheet.html")


# -----------------------------------------
# PIPELINE
# -----------------------------------------

def run_pipeline(ticker: str) -> str:
    """
    Runs the full balance sheet generation pipeline
    and returns the path to the generated HTML file.
    """

    ticker = ticker.strip().upper()

    print("Step 1: Fetching balance sheet...")
    raw_df = get_balance_sheet(ticker)

    print("Step 2: Preprocessing...")
    clean_df = preprocess_balance_sheet(raw_df)

    print("Step 3: Selecting core metrics...")
    selected_df = select_balance_sheet_metrics(clean_df)

    print("Step 4: Analyzing trends...")
    analyzed_df = analyze_balance_sheet(selected_df)

    print("Step 5: Building UI schema...")

    analyzed_df["company"] = {
        "name": ticker,
        "ticker": ticker,
        "currency": "INR"
    }

    ui_json = build_ui_schema(analyzed_df)

    OUTPUT_JSON_PATH.parent.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(ui_json, f, indent=4)

    print("UI JSON saved.")

    print("Step 6: Rendering HTML...")
    render_html()   # This should generate data/balance_sheet.html

    print("Balance Sheet Generation Completed Successfully.")

    return str(OUTPUT_HTML_PATH)


# -----------------------------------------
# ENTRY (Terminal Mode)
# -----------------------------------------

if __name__ == "__main__":
    user_ticker = input("Enter company ticker (e.g., AAPL, HDFCBANK.NS): ")
    run_pipeline(user_ticker)