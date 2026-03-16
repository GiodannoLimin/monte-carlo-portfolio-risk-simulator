import pandas as pd
import streamlit as st

from src.data_source import download_price_data
from src.preprocessing import compute_returns
from src.plotting import (
    plot_historical_stock,
    plot_correlation_heatmap,
    plot_benchmark_comparison,
)
from src.simulation import (
    compute_historical_portfolio_returns,
    compute_equal_weight_returns,
    compute_cumulative_growth,
)


@st.cache_data(show_spinner=False)
def get_custom_ticker_data(ticker: str, period: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    price_df = download_price_data([ticker], period=period, interval="1d")
    if price_df.empty or ticker not in price_df.columns:
        return pd.DataFrame(), pd.DataFrame()

    returns_df = compute_returns(price_df)
    return price_df, returns_df


def render_explorer_tab(asset_cols, price_df, returns_df, weights, selected_period) -> None:
    st.subheader("Stock Explorer")

    st.markdown("Explore one of your portfolio tickers or enter another ticker manually.")

    col1, col2 = st.columns([2, 1])

    with col1:
        selected_portfolio_ticker = st.selectbox(
            "Choose a stock from your portfolio list",
            options=asset_cols,
        )

    with col2:
        custom_ticker = st.text_input(
            "Or enter any ticker",
            value="",
            placeholder="e.g. NVDA",
        ).strip().upper()

    use_custom_ticker = bool(custom_ticker)

    if use_custom_ticker:
        with st.spinner(f"Loading {custom_ticker}..."):
            custom_price_df, custom_returns_df = get_custom_ticker_data(
                custom_ticker,
                selected_period,
            )

        if custom_price_df.empty or custom_ticker not in custom_price_df.columns:
            st.error(f"Could not load data for {custom_ticker}.")
            return

        selected_ticker = custom_ticker
        selected_price_df = custom_price_df
        selected_returns_df = custom_returns_df
        st.caption(
            f"Showing standalone data for {selected_ticker}. "
            "Correlation and portfolio comparison below still use your portfolio tickers."
        )
    else:
        selected_ticker = selected_portfolio_ticker
        selected_price_df = price_df
        selected_returns_df = returns_df

    st.plotly_chart(
        plot_historical_stock(selected_price_df, selected_ticker),
        width="stretch",
    )

    stock_returns = selected_returns_df[selected_ticker].dropna()
    stock_last_price = selected_price_df[selected_ticker].dropna().iloc[-1]
    stock_mu = stock_returns.mean()
    stock_sigma = stock_returns.std()

    e1, e2, e3 = st.columns(3)
    e1.metric("Latest Price", f"${stock_last_price:,.2f}")
    e2.metric("Average Daily Return", f"{stock_mu:.3%}")
    e3.metric("Daily Volatility", f"{stock_sigma:.3%}")

    st.caption("This chart refreshes whenever the app fetches updated market data.")

    st.subheader("Correlation Between Assets")

    st.plotly_chart(
        plot_correlation_heatmap(returns_df, asset_cols),
        width="stretch",
    )

    st.caption(
        "Correlation measures how assets move together. "
        "Lower correlations help diversification."
    )

    st.subheader("Portfolio vs Benchmark Comparison")

    aligned_returns_df = returns_df.copy()

    user_portfolio_returns = compute_historical_portfolio_returns(
        aligned_returns_df, asset_cols, weights
    )

    equal_weight_returns = compute_equal_weight_returns(
        aligned_returns_df, asset_cols
    )

    if "SPY" in asset_cols:
        spy_returns = aligned_returns_df["SPY"].values
    else:
        spy_returns = equal_weight_returns

    user_growth = compute_cumulative_growth(user_portfolio_returns)
    equal_weight_growth = compute_cumulative_growth(equal_weight_returns)
    spy_growth = compute_cumulative_growth(spy_returns)

    st.plotly_chart(
        plot_benchmark_comparison(
            aligned_returns_df["Date"],
            user_growth,
            equal_weight_growth,
            spy_growth,
        ),
        width="stretch",
    )

    c1, c2, c3 = st.columns(3)
    c1.metric("User Portfolio Final Growth", f"{user_growth[-1]:.2f}x")
    c2.metric("Equal-Weight Final Growth", f"{equal_weight_growth[-1]:.2f}x")
    c3.metric("SPY Final Growth", f"{spy_growth[-1]:.2f}x")

    st.caption(
        "This compares how your chosen portfolio weights performed historically "
        "against an equal-weight allocation and SPY."
    )