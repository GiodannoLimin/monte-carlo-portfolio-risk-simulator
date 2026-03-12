import numpy as np
import pandas as pd
import streamlit as st

from src.preprocessing import merge_stock_data, compute_returns, save_processed_data
from src.simulation import (
    estimate_parameters,
    simulate_gbm_paths,
    portfolio_returns_from_values,
    simulate_portfolio_growth,
)
from src.risk_metrics import summarize_risk, summarize_final_values
from src.plotting import (
    plot_historical_stock,
    plot_simulated_portfolio_paths,
    plot_return_distribution,
    plot_terminal_value_distribution,
    plot_projection_table_bars,
)
from src.theory import THEORY_TEXT


st.set_page_config(
    page_title="Monte Carlo Portfolio Risk Simulator",
    layout="wide",
)

st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #060816 0%, #0c1230 45%, #211a52 100%);
        color: white;
    }
    [data-testid="stMetric"] {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.10);
        padding: 14px;
        border-radius: 16px;
    }
    .small-text {
        font-size: 0.95rem;
        opacity: 0.9;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ----------------------------
# Load and preprocess data
# ----------------------------
file_map = {
    "AAPL": "data/raw/AAPL.csv",
    "MSFT": "data/raw/MSFT.csv",
    "NVDA": "data/raw/NVDA.csv",
    "SPY": "data/raw/SPY.csv",
}

price_df = merge_stock_data(file_map)
returns_df = compute_returns(price_df)
save_processed_data(price_df, returns_df)

mu, sigma, asset_cols = estimate_parameters(returns_df)
latest_prices = price_df[asset_cols].iloc[-1].values

# ----------------------------
# Header
# ----------------------------
st.title("Monte Carlo Portfolio Risk Simulator")
st.caption(
    "Interactive portfolio scenario analysis using Geometric Brownian Motion, VaR, and CVaR."
)

tab_dashboard, tab_explorer, tab_learn, tab_theory = st.tabs(
    ["Dashboard", "Stock Explorer", "Learn", "Theory"]
)

# ----------------------------
# Dashboard Tab
# ----------------------------
with tab_dashboard:
    left, right = st.columns([1.15, 1.0])

    with left:
        st.subheader("Portfolio Settings")

        c1, c2 = st.columns(2)
        with c1:
            w_aapl = st.slider("AAPL weight", 0.0, 1.0, 0.25, 0.05)
            w_msft = st.slider("MSFT weight", 0.0, 1.0, 0.25, 0.05)
        with c2:
            w_nvda = st.slider("NVDA weight", 0.0, 1.0, 0.25, 0.05)
            w_spy = st.slider("SPY weight", 0.0, 1.0, 0.25, 0.05)

        weights = np.array([w_aapl, w_msft, w_nvda, w_spy], dtype=float)

        if weights.sum() == 0:
            st.error("Portfolio weights cannot all be zero.")
            st.stop()

        weights = weights / weights.sum()

        st.write("**Normalized Weights**")
        st.dataframe(
            pd.DataFrame({"Asset": asset_cols, "Weight": weights}),
            use_container_width=True,
            hide_index=True
        )

    with right:
        st.subheader("Simulation Controls")

        horizon_days = st.selectbox(
            "Time horizon (days)",
            options=[126, 252, 378, 504, 630, 756],
            index=0,
            help="126 ≈ 0.5 years, 252 ≈ 1 year, ..., 756 ≈ 3 years."
        )

        n_sims = st.slider(
            "Number of simulations",
            1000, 20000, 8000, 1000,
            help="More simulations give smoother results but may run a bit slower."
        )

        confidence_level = st.slider(
            "Confidence level",
            0.90, 0.99, 0.95, 0.01,
            help="Used for VaR and CVaR. Example: 0.95 means focusing on the worst 5% tail."
        )

        initial_investment = st.number_input(
            "Initial investment ($)",
            min_value=0.0,
            value=10000.0,
            step=500.0,
            help="This is the amount invested at the start."
        )

        monthly_contribution = st.number_input(
            "Recurring monthly contribution ($)",
            min_value=0.0,
            value=0.0,
            step=100.0,
            help="Optional recurring monthly deposit for scenario analysis."
        )

    simulated_prices, portfolio_values = simulate_gbm_paths(
        initial_prices=latest_prices,
        mu=mu,
        sigma=sigma,
        weights=weights,
        n_days=horizon_days,
        n_sims=n_sims,
    )

    sim_returns = portfolio_returns_from_values(portfolio_values)
    risk_summary = summarize_risk(sim_returns, confidence_level)
    final_value_summary = summarize_final_values(portfolio_values[-1])

    st.subheader("Risk Metrics")

    m1, m2, m3, m4 = st.columns(4)
    m1.metric(
        "Expected Return",
        f"{risk_summary['expected_return']:.2%}",
        help="Average simulated portfolio return over the chosen horizon."
    )
    m2.metric(
        "Volatility",
        f"{risk_summary['volatility']:.2%}",
        help="Typical size of fluctuations in simulated portfolio returns."
    )
    m3.metric(
        "VaR",
        f"{risk_summary['var']:.2%}",
        help="At the chosen confidence level, this is a downside return threshold from the simulated distribution."
    )
    m4.metric(
        "CVaR",
        f"{risk_summary['cvar']:.2%}",
        help="Average return in the worst tail beyond the VaR threshold."
    )

    st.info(
        f"""
**Beginner interpretation**

- The simulation suggests an average return of **{risk_summary['expected_return']:.2%}** over the selected horizon.
- The **VaR** at confidence level **{confidence_level:.0%}** is **{risk_summary['var']:.2%}**.
- The **CVaR** is **{risk_summary['cvar']:.2%}**, meaning the worst tail outcomes are even more negative on average.
        """
    )

    with st.expander("⚠️ Important Disclaimer"):
        st.write(
            """
This tool provides **simulated scenario outcomes** based on historical data and mathematical assumptions.

It does **not** provide guaranteed forecasts or professional financial advice.

Important assumptions and limitations:

- asset returns are modeled using **Geometric Brownian Motion**
- drift and volatility are estimated from historical data
- volatility is treated as approximately constant
- real markets can have shocks, regime changes, and structural breaks not captured here
- past performance does not guarantee future results

Use this project for **education and exploration**, not as a sole basis for real investment decisions.
            """
        )

    st.subheader("Charts")

    ch1, ch2 = st.columns(2)
    with ch1:
        st.plotly_chart(
            plot_simulated_portfolio_paths(portfolio_values, max_lines=25),
            use_container_width=True
        )
        st.caption(
            "Each line is one simulated future path of the portfolio. These are possible scenarios, not certainties."
        )

    with ch2:
        st.plotly_chart(
            plot_return_distribution(sim_returns, risk_summary["var"], risk_summary["cvar"]),
            use_container_width=True
        )
        st.caption(
            "This histogram summarizes all simulations into a return distribution. VaR and CVaR are marked on the left tail."
        )

    st.plotly_chart(
        plot_terminal_value_distribution(portfolio_values[-1]),
        use_container_width=True
    )
    st.caption(
        "This chart shows how the final portfolio value is distributed at the end of the selected horizon."
    )

    st.subheader("Scenario Summary")
    s1, s2, s3, s4 = st.columns(4)
    s1.metric("Median Final Value", f"${final_value_summary['median_final_value']:,.2f}")
    s2.metric("Mean Final Value", f"${final_value_summary['mean_final_value']:,.2f}")
    s3.metric("5th Percentile", f"${final_value_summary['p5_final_value']:,.2f}")
    s4.metric("95th Percentile", f"${final_value_summary['p95_final_value']:,.2f}")

    st.markdown("---")
    st.subheader("Investment Outcome Projection")

    horizon_map = {
        "0.5 years": 126,
        "1 year": 252,
        "1.5 years": 378,
        "2 years": 504,
        "2.5 years": 630,
        "3 years": 756,
    }

    projection_rows = []

    for label, days in horizon_map.items():
        _, proj_values = simulate_gbm_paths(
            initial_prices=latest_prices,
            mu=mu,
            sigma=sigma,
            weights=weights,
            n_days=days,
            n_sims=4000,
        )
        proj_returns = portfolio_returns_from_values(proj_values)

        years = days / 252
        growth_result = simulate_portfolio_growth(
            initial_investment=initial_investment,
            monthly_contribution=monthly_contribution,
            portfolio_returns=proj_returns,
            years=years,
        )

        final_values = growth_result["final_values"]
        total_contributions = growth_result["total_contributions"]
        pnl = growth_result["pnl"]

        projection_rows.append({
            "Horizon": label,
            "Total Contributions": round(float(total_contributions), 2),
            "Median Final Value": round(float(np.median(final_values)), 2),
            "Mean Final Value": round(float(np.mean(final_values)), 2),
            "5th Percentile Value": round(float(np.percentile(final_values, 5)), 2),
            "95th Percentile Value": round(float(np.percentile(final_values, 95)), 2),
            "Median Profit/Loss": round(float(np.median(pnl)), 2),
        })

    projection_df = pd.DataFrame(projection_rows)

    p1, p2 = st.columns([1.2, 1.0])
    with p1:
        st.dataframe(projection_df, use_container_width=True, hide_index=True)
    with p2:
        st.plotly_chart(plot_projection_table_bars(projection_df), use_container_width=True)

# ----------------------------
# Stock Explorer Tab
# ----------------------------
with tab_explorer:
    st.subheader("Stock Explorer")

    selected_ticker = st.selectbox(
        "Choose a stock to view",
        options=asset_cols,
        help="Shows the historical closing price chart for the selected asset."
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

    st.info(
        f"""
**How to read this**

- This chart shows the historical closing prices of **{selected_ticker}**.
- The latest available price is **${stock_last_price:,.2f}**.
- The average daily return and daily volatility are estimated from the uploaded data.
        """
    )

# ----------------------------
# Learn Tab
# ----------------------------
with tab_learn:
    st.subheader("Beginner-Friendly Guide")

    with st.expander("What does portfolio weight mean?"):
        st.write(
            """
Portfolio weight means how much of your portfolio is allocated to each asset.

Example:
- 50% AAPL
- 25% MSFT
- 15% NVDA
- 10% SPY

These weights are normalized automatically in the dashboard.
            """
        )

    with st.expander("What do the many simulation lines mean?"):
        st.write(
            """
Each line is one possible simulated future for the portfolio.

The model does not know the exact future, so it generates many possible scenarios.
The purpose is to understand the range of outcomes, not to claim certainty.
            """
        )

    with st.expander("What is Value at Risk (VaR)?"):
        st.write(
            """
VaR is a downside threshold from the simulated return distribution.

Example:
if VaR = -1.36% at 95% confidence, then the model suggests that losses worse than 1.36%
are in roughly the worst 5% of simulated cases.
            """
        )

    with st.expander("What is CVaR?"):
        st.write(
            """
CVaR is the average return in the worst tail beyond VaR.

So if VaR tells you where the bad tail begins, CVaR tells you how bad those worst cases are on average.
            """
        )

    with st.expander("Is this a prediction?"):
        st.write(
            """
Not in a guaranteed sense.

This is a **simulation under assumptions**, based on historical drift and volatility.
It is better to call the outputs projected scenarios or simulated outcomes.
            """
        )

# ----------------------------
# Theory Tab
# ----------------------------
with tab_theory:
    st.subheader("Mathematical Theory")
    st.markdown(THEORY_TEXT)