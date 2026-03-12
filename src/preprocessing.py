import pandas as pd
from pathlib import Path


def load_single_stock(file_path: str, ticker: str) -> pd.DataFrame:
    df = pd.read_csv(file_path)

    df["Date"] = pd.to_datetime(df["Date"])
    df["Close/Last"] = (
        df["Close/Last"]
        .replace(r"[\$,]", "", regex=True)
        .astype(float)
    )

    df = df[["Date", "Close/Last"]].copy()
    df = df.rename(columns={"Close/Last": ticker})
    df = df.sort_values("Date").reset_index(drop=True)

    return df


def merge_stock_data(file_map: dict) -> pd.DataFrame:
    merged_df = None

    for ticker, file_path in file_map.items():
        stock_df = load_single_stock(file_path, ticker)

        if merged_df is None:
            merged_df = stock_df
        else:
            merged_df = pd.merge(merged_df, stock_df, on="Date", how="inner")

    merged_df = merged_df.sort_values("Date").reset_index(drop=True)
    return merged_df


def compute_returns(price_df: pd.DataFrame) -> pd.DataFrame:
    returns_df = price_df.copy()
    asset_cols = [col for col in returns_df.columns if col != "Date"]

    returns_df[asset_cols] = returns_df[asset_cols].pct_change()
    returns_df = returns_df.dropna().reset_index(drop=True)

    return returns_df


def save_processed_data(price_df: pd.DataFrame, returns_df: pd.DataFrame) -> None:
    processed_dir = Path("data/processed")
    processed_dir.mkdir(parents=True, exist_ok=True)

    price_df.to_csv(processed_dir / "merged_prices.csv", index=False)
    returns_df.to_csv(processed_dir / "returns.csv", index=False)