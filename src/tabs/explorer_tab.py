import streamlit as st

from src.plotting import plot_historical_stock


def render_explorer_tab(asset_cols, price_df, returns_df) -> None:
    st.subheader("Stock Explorer")

    selected_ticker = st.selectbox(
        "Choose a stock",
        options=asset_cols
    )

    st.plotly_chart(
        plot_historical_stock(price_df, selected_ticker),
        use_container_width=True
    )

    stock_returns = returns_df[selected_ticker]
    stock_last_price = price_df[selected_ticker].iloc[-1]
    stock_mu = stock_returns.mean()
    stock_sigma = stock_returns.std()

    e1, e2, e3 = st.columns(3)
    e1.metric("Latest Price", f"${stock_last_price:,.2f}")
    e2.metric("Average Daily Return", f"{stock_mu:.3%}")
    e3.metric("Daily Volatility", f"{stock_sigma:.3%}")

    st.caption("This chart refreshes whenever the app fetches updated market data.")