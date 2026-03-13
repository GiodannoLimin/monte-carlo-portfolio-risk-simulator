import numpy as np
import pandas as pd
import streamlit as st

from src.config import PAGE_TITLE, PAGE_LAYOUT, APP_TITLE, APP_CAPTION
from src.styles import inject_global_styles
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
from src.tabs.dashboard_tab import render_dashboard_tab
from src.tabs.explorer_tab import render_explorer_tab
from src.tabs.learn_tab import render_learn_tab
from src.tabs.theory_tab import render_theory_tab


st.set_page_config(
    page_title=PAGE_TITLE,
    layout=PAGE_LAYOUT,
)

inject_global_styles()


@st.cache_data(ttl=3600, show_spinner=False)
def get_prices(tickers: tuple[str, ...], period: str) -> pd.DataFrame:
    with st.spinner("Fetching latest market data..."):
        return download_price_data(list(tickers), period=period, interval="1d")


st.title(APP_TITLE)
st.caption(APP_CAPTION)

st.info("👈 Tip: Open the sidebar (>>) to change tickers, weights, investment settings, and simulation parameters.")

sidebar_state = render_sidebar()

tickers = [t.strip().upper() for t in sidebar_state["tickers_text"].split(",") if t.strip()]
if len(tickers) == 0:
    st.error("Please enter at least one ticker.")
    st.stop()

if sidebar_state["refresh"]:
    st.cache_data.clear()

try:
    price_df = get_prices(tuple(tickers), sidebar_state["selected_period"])
except Exception as e:
    st.error(f"Could not download data: {e}")
    st.stop()

returns_df = compute_returns(price_df)
save_processed_data(price_df, returns_df)

mu, sigma, asset_cols = estimate_parameters(returns_df)
latest_prices = price_df[asset_cols].iloc[-1].values

weights_input = render_weight_sliders(asset_cols)
weights = np.array(weights_input, dtype=float)

if weights.sum() == 0:
    st.error("Portfolio weights cannot all be zero.")
    st.stop()

weights = weights / weights.sum()

simulated_prices, portfolio_values = simulate_gbm_paths(
    initial_prices=latest_prices,
    mu=mu,
    sigma=sigma,
    weights=weights,
    n_days=sidebar_state["horizon_days"],
    n_sims=sidebar_state["n_sims"],
)

sim_returns = portfolio_returns_from_values(portfolio_values)
risk_summary = summarize_risk(sim_returns, sidebar_state["confidence_level"])

selected_years = sidebar_state["horizon_days"] / 252
selected_growth_result = simulate_portfolio_growth(
    initial_investment=sidebar_state["initial_investment"],
    monthly_contribution=sidebar_state["monthly_contribution"],
    portfolio_returns=sim_returns,
    years=selected_years,
)

selected_final_values = selected_growth_result["final_values"]
selected_total_contributions = selected_growth_result["total_contributions"]
selected_pnl = selected_growth_result["pnl"]

investment_summary = {
    "median_final_value": float(np.median(selected_final_values)),
    "mean_final_value": float(np.mean(selected_final_values)),
    "p5_final_value": float(np.percentile(selected_final_values, 5)),
    "p95_final_value": float(np.percentile(selected_final_values, 95)),
    "median_pnl": float(np.median(selected_pnl)),
    "mean_pnl": float(np.mean(selected_pnl)),
}

tab_dashboard, tab_explorer, tab_learn, tab_theory = st.tabs(
    ["Dashboard", "Stock Explorer", "Learn", "Theory"]
)

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
        selected_total_contributions=selected_total_contributions,
        investment_summary=investment_summary,
        selected_final_values=selected_final_values,
    )

with tab_explorer:
    render_explorer_tab(
        asset_cols=asset_cols,
        price_df=price_df,
        returns_df=returns_df,
    )

with tab_learn:
    render_learn_tab()

with tab_theory:
    render_theory_tab()