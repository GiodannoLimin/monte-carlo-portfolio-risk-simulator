import numpy as np
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

from src.config import PAGE_TITLE, PAGE_LAYOUT, APP_TITLE, APP_CAPTION
from src.styles import inject_global_styles
from src.app_text import DISCLAIMER_TEXT
from src.sidebar import render_sidebar, render_weight_sliders
from src.data_source import download_price_data
from src.preprocessing import compute_returns, save_processed_data
from src.simulation import (
    estimate_parameters,
    simulate_gbm_paths,
    portfolio_returns_from_values,
    simulate_portfolio_growth,
)
from src.risk_metrics import summarize_risk
from src.optimization import (
    generate_random_portfolios,
    get_max_sharpe_portfolio,
    get_min_vol_portfolio,
    compute_portfolio_return,
    compute_portfolio_volatility,
    compute_portfolio_sharpe,
)
from src.stress_testing import run_stress_scenarios
from src.backtesting import (
    compute_historical_portfolio_series,
    compute_backtest_summary,
)
from src.factor_analysis import compute_portfolio_returns, compute_capm_stats
from src.tabs.dashboard_tab import render_dashboard_tab
from src.tabs.explorer_tab import render_explorer_tab
from src.tabs.learn_tab import render_learn_tab
from src.education import (
    build_education_html,
    build_education_html_bytes,
    build_education_pdf_bytes,
)

st.set_page_config(
    page_title=PAGE_TITLE,
    layout=PAGE_LAYOUT,
)

inject_global_styles()


@st.cache_data(ttl=3600, show_spinner=False)
def get_prices(tickers: tuple[str, ...], period: str) -> pd.DataFrame:
    with st.spinner("Fetching latest market data..."):
        return download_price_data(list(tickers), period=period, interval="1d")

@st.cache_data(show_spinner=False)
def get_education_html() -> str:
    return build_education_html(pdf_mode=False)


@st.cache_data(show_spinner=False)
def get_education_html_bytes() -> bytes:
    return build_education_html_bytes(pdf_mode=False)


@st.cache_data(show_spinner=False)
def get_education_pdf_bytes() -> bytes:
    with st.spinner("Generating PDF handbook..."):
        return build_education_pdf_bytes()

# -----------------------------
# Header
# -----------------------------
st.markdown(
    f"""
    <div style="
        padding: 24px;
        border-radius: 18px;
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.08);
        margin-bottom: 12px;
    ">
        <h1 style="margin-bottom: 8px;">{APP_TITLE}</h1>
        <p style="color:#9aa4b2; margin-bottom:0; font-size: 1.05rem;">
            {APP_CAPTION}
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.caption("View Mode")
mode = st.radio(
    "View Mode",
    ["Beginner", "Professional"],
    horizontal=True,
    label_visibility="collapsed",
)

st.divider()

st.info(
    "👈 Use the sidebar to select tickers, adjust portfolio weights, and configure simulation settings."
)


# -----------------------------
# Sidebar inputs
# -----------------------------
sidebar_state = render_sidebar()

tickers = [
    t.strip().upper()
    for t in sidebar_state["tickers_text"].split(",")
    if t.strip()
]

if len(tickers) == 0:
    st.error("Please enter at least one ticker.")
    st.stop()

if sidebar_state["refresh"]:
    st.cache_data.clear()


# -----------------------------
# Download and validate data
# -----------------------------
try:
    price_df = get_prices(tuple(tickers), sidebar_state["selected_period"])
except Exception as e:
    st.error(f"Could not download data: {e}")
    st.stop()

if price_df.empty:
    st.error("No data returned for the selected tickers or time period. Please try again.")
    st.stop()

returns_df = compute_returns(price_df).tail(252 * 10)
save_processed_data(price_df, returns_df)

mu, sigma, asset_cols = estimate_parameters(returns_df)

if len(asset_cols) == 0:
    st.error("No valid asset columns were found in the downloaded data.")
    st.stop()

missing_cols = [col for col in asset_cols if col not in price_df.columns]
if missing_cols:
    st.error(
        f"Downloaded data is missing expected asset columns: {', '.join(missing_cols)}"
    )
    st.stop()

if price_df[asset_cols].empty:
    st.error("Downloaded price data is empty after filtering valid asset columns.")
    st.stop()

latest_prices = price_df[asset_cols].iloc[-1].values


# -----------------------------
# Portfolio weights
# -----------------------------
weights_input = render_weight_sliders(asset_cols)
weights = np.array(weights_input, dtype=float)

if weights.sum() == 0:
    st.error("Portfolio weights cannot all be zero.")
    st.stop()

weights = weights / weights.sum()


# -----------------------------
# Historical backtesting
# -----------------------------
historical_portfolio_returns = compute_historical_portfolio_series(
    returns_df,
    asset_cols,
    weights,
)
backtest_summary = compute_backtest_summary(historical_portfolio_returns)

if "SPY" in asset_cols:
    benchmark_returns = returns_df["SPY"].values
else:
    benchmark_returns = returns_df[asset_cols].mean(axis=1).values

benchmark_summary = compute_backtest_summary(benchmark_returns)


# -----------------------------
# Factor analysis (CAPM)
# -----------------------------
portfolio_factor_returns = compute_portfolio_returns(
    returns_df,
    asset_cols,
    weights,
)

if "SPY" in asset_cols:
    market_factor_returns = returns_df["SPY"].values
else:
    market_factor_returns = returns_df[asset_cols].mean(axis=1).values

capm_stats = compute_capm_stats(
    portfolio_returns=portfolio_factor_returns,
    market_returns=market_factor_returns,
)


# -----------------------------
# Portfolio optimization
# -----------------------------
frontier_data = generate_random_portfolios(returns_df, asset_cols)

mean_returns = frontier_data["mean_returns"]
cov_matrix = frontier_data["cov_matrix"]

current_portfolio = {
    "return": compute_portfolio_return(weights, mean_returns),
    "volatility": compute_portfolio_volatility(weights, cov_matrix),
    "sharpe": compute_portfolio_sharpe(weights, mean_returns, cov_matrix),
    "weights": weights,
}

max_sharpe_portfolio = get_max_sharpe_portfolio(frontier_data)
min_vol_portfolio = get_min_vol_portfolio(frontier_data)


# -----------------------------
# Stress testing
# -----------------------------
stress_results = run_stress_scenarios(
    latest_prices=latest_prices,
    mu=mu,
    sigma=sigma,
    weights=weights,
    horizon_days=sidebar_state["horizon_days"],
    n_sims=sidebar_state["n_sims"],
    confidence_level=sidebar_state["confidence_level"],
)


# -----------------------------
# Monte Carlo simulation
# -----------------------------
simulated_prices, portfolio_values = simulate_gbm_paths(
    initial_prices=latest_prices,
    mu=mu,
    sigma=sigma,
    weights=weights,
    n_days=sidebar_state["horizon_days"],
    n_sims=sidebar_state["n_sims"],
)

sim_returns = portfolio_returns_from_values(portfolio_values)
selected_years = sidebar_state["horizon_days"] / 252

risk_summary = summarize_risk(
    sim_returns,
    confidence_level=sidebar_state["confidence_level"],
    portfolio_values=portfolio_values,
    years=selected_years,
)


# -----------------------------
# Investment projection
# -----------------------------
growth_result = simulate_portfolio_growth(
    initial_investment=sidebar_state["initial_investment"],
    monthly_contribution=sidebar_state["monthly_contribution"],
    portfolio_returns=sim_returns,
    years=selected_years,
)

final_values = growth_result["final_values"]
total_contributions = growth_result["total_contributions"]
pnl = growth_result["pnl"]

investment_summary = {
    "median_final_value": float(np.median(final_values)),
    "mean_final_value": float(np.mean(final_values)),
    "p5_final_value": float(np.percentile(final_values, 5)),
    "p95_final_value": float(np.percentile(final_values, 95)),
    "median_pnl": float(np.median(pnl)),
    "mean_pnl": float(np.mean(pnl)),
}



# -----------------------------
# Tabs
# -----------------------------
tab_dashboard, tab_explorer, tab_learn = st.tabs(
    ["Dashboard", "Stock Explorer", "Learn"]
)


# -----------------------------
# Dashboard tab
# -----------------------------
with tab_dashboard:
    render_dashboard_tab(
        asset_cols=asset_cols,
        weights=weights,
        horizon_days=sidebar_state["horizon_days"],
        n_sims=sidebar_state["n_sims"],
        confidence_level=sidebar_state["confidence_level"],
        portfolio_values=portfolio_values,
        sim_returns=sim_returns,
        risk_summary=risk_summary,
        latest_prices=latest_prices,
        mu=mu,
        sigma=sigma,
        initial_investment=sidebar_state["initial_investment"],
        monthly_contribution=sidebar_state["monthly_contribution"],
        selected_years=selected_years,
        selected_total_contributions=total_contributions,
        investment_summary=investment_summary,
        selected_final_values=final_values,
        mode=mode,
        frontier_data=frontier_data,
        current_portfolio=current_portfolio,
        max_sharpe_portfolio=max_sharpe_portfolio,
        min_vol_portfolio=min_vol_portfolio,
        stress_results=stress_results,
        backtest_summary=backtest_summary,
        benchmark_summary=benchmark_summary,
        backtest_dates=returns_df["Date"],
        capm_stats=capm_stats,
    )


# -----------------------------
# Explorer tab
# -----------------------------
with tab_explorer:
    render_explorer_tab(
        asset_cols=asset_cols,
        price_df=price_df,
        returns_df=returns_df,
        weights=weights,
        selected_period=sidebar_state["selected_period"],
    )

# -----------------------------
# Learn tab
# -----------------------------
with tab_learn:
    render_learn_tab(mode=mode)

    st.divider()

    education_html = get_education_html()
    education_html_bytes = get_education_html_bytes()

    st.subheader("Interactive Portfolio Analytics Handbook")
    st.markdown(
        """
This handbook combines the beginner guide and technical reference into one
polished learning document. You can preview it below or download it as HTML or PDF.
        """
    )

    preview_tab, export_tab = st.tabs(["Preview", "Export"])

    with preview_tab:
        components.html(education_html, height=950, scrolling=True)

    with export_tab:
        st.markdown(
            """
Choose a format:

- **HTML** keeps the handbook interactive in a browser
- **PDF** gives you a dedicated report-style export with a designed layout
            """
        )

        col1, col2 = st.columns(2)

        with col1:
            st.download_button(
                label="Download Handbook (HTML)",
                data=education_html_bytes,
                file_name="portfolio_analytics_handbook.html",
                mime="text/html",
                use_container_width=True,
            )

        with col2:
            try:
                pdf_bytes = get_education_pdf_bytes()

                st.download_button(
                    label="Download Handbook (PDF)",
                    data=pdf_bytes,
                    file_name="portfolio_analytics_handbook.pdf",
                    mime="application/pdf",
                    use_container_width=True,
                )
            except Exception as e:
                st.error(f"PDF generation failed: {e}")

        st.caption(
            "The PDF is generated from the handbook pipeline for a cleaner report-style export."
        )
# -----------------------------
# Footer disclaimer
# -----------------------------
st.divider()

with st.expander("⚠️ Important Disclaimer", expanded=False):
    st.markdown(DISCLAIMER_TEXT)