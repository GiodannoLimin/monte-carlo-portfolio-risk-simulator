import pandas as pd
from pathlib import Path


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