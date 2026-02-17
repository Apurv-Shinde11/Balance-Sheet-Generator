import yfinance as yf
import pandas as pd


def get_balance_sheet(ticker: str, period: str = "annual") -> pd.DataFrame:
    """
    Fetch raw balance sheet from Yahoo Finance.

    Parameters:
        ticker (str): Stock ticker (e.g., HDFCBANK.NS)
        period (str): 'annual' or 'quarterly'

    Returns:
        pd.DataFrame: Raw balance sheet DataFrame
    """

    ticker = ticker.upper()
    stock = yf.Ticker(ticker)

    if period == "annual":
        df = stock.balance_sheet
    elif period == "quarterly":
        df = stock.quarterly_balance_sheet
    else:
        raise ValueError("Period must be 'annual' or 'quarterly'")

    if df is None or df.empty:
        raise ValueError(f"No balance sheet data found for {ticker}")

    return df