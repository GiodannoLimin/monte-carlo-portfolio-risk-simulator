import pandas as pd
import yfinance as yf


def download_price_data(
    tickers: list[str],
    period: str = "10y",
    interval: str = "1d"
) -> pd.DataFrame:
    """
    Download historical adjusted closing prices for multiple tickers.

    Returns a dataframe:
    Date | AAPL | MSFT | NVDA | SPY | ...
    """
    data = yf.download(
        tickers=tickers,
        period=period,
        interval=interval,
        auto_adjust=True,
        progress=False,
        group_by="column",
        threads=True,
    )

    if data.empty:
        raise ValueError("No data was returned from yfinance.")

    if "Close" not in data:
        raise ValueError("Downloaded data does not contain Close prices.")

    close_df = data["Close"].copy()

    # If only one ticker, yfinance may return a Series
    if isinstance(close_df, pd.Series):
        close_df = close_df.to_frame(name=tickers[0])

    close_df = close_df.reset_index()
    close_df = close_df.rename(columns={"Date": "Date"})
    close_df["Date"] = pd.to_datetime(close_df["Date"])

    # Drop rows with missing values across chosen assets
    close_df = close_df.dropna().sort_values("Date").reset_index(drop=True)

    return close_df