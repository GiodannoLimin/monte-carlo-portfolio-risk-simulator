import pandas as pd
import streamlit as st

from src.overview import render_portfolio_overview
from src.tabs.dashboard_risk_section import render_risk_section
from src.tabs.dashboard_chart_section import render_chart_section
from src.tabs.dashboard_investment_section import render_investment_section


def render_dashboard_tab(
    asset_cols,
    weights,
    horizon_days,
    n_sims,
    confidence_level,
    portfolio_values,
    sim_returns,
    risk_summary,
    latest_prices,
    mu,
    sigma,
    initial_investment,
    monthly_contribution,
    selected_years,
    selected_total_contributions,
    investment_summary,
    selected_final_values,
) -> None:
    render_portfolio_overview(
        asset_cols=asset_cols,
        horizon_days=horizon_days,
        n_sims=n_sims,
        confidence_level=confidence_level,
    )

    st.subheader("Portfolio Configuration")
    st.dataframe(
        pd.DataFrame({"Asset": asset_cols, "Normalized Weight": weights}),
        width="stretch",
        hide_index=True
    )

    st.markdown("---")

    render_risk_section(
        risk_summary=risk_summary,
        confidence_level=confidence_level,
    )

    render_chart_section(
        portfolio_values=portfolio_values,
        sim_returns=sim_returns,
        risk_summary=risk_summary,
    )

    st.markdown("---")

    render_investment_section(
        latest_prices=latest_prices,
        mu=mu,
        sigma=sigma,
        weights=weights,
        initial_investment=initial_investment,
        monthly_contribution=monthly_contribution,
        selected_years=selected_years,
        selected_total_contributions=selected_total_contributions,
        investment_summary=investment_summary,
        selected_final_values=selected_final_values,
    )