import pandas as pd


# ----------------------------------------
# Step 1: Clean metric names
# ----------------------------------------
def clean_metric_names(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.index = (
        df.index.astype(str)
        .str.replace("_", " ")
        .str.strip()
    )
    return df


# ----------------------------------------
# Step 2: Sort periods descending (latest first)
# ----------------------------------------
def sort_periods(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = pd.to_datetime(df.columns)
    df = df.sort_index(axis=1, ascending=False)
    return df


# ----------------------------------------
# Step 3: Select latest N periods
# ----------------------------------------
def select_periods(df: pd.DataFrame, n_periods: int = 2) -> pd.DataFrame:
    return df.iloc[:, :n_periods]


# ----------------------------------------
# Step 4: Convert to structured dictionary
# ----------------------------------------
def to_structured_dict(df: pd.DataFrame) -> dict:
    periods = [
        col.strftime("%Y-%m")
        for col in df.columns
    ]

    data = {}

    for metric in df.index:
        values = df.loc[metric].tolist()
        data[metric] = values

    return {
        "periods": periods,
        "data": data
    }


# ----------------------------------------
# Full Pipeline Wrapper
# ----------------------------------------
def preprocess_balance_sheet(raw_df: pd.DataFrame, n_periods: int = 2) -> dict:
    """
    Complete preprocessing pipeline
    """
    if raw_df is None or raw_df.empty:
        raise ValueError("Empty balance sheet DataFrame")

    df = clean_metric_names(raw_df)
    df = sort_periods(df)
    df = select_periods(df, n_periods)

    return to_structured_dict(df)