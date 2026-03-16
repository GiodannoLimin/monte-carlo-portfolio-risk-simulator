import pandas as pd
import streamlit as st

from src.overview import render_portfolio_overview
from src.tabs.dashboard_risk_section import render_risk_section
from src.tabs.dashboard_chart_section import render_chart_section
from src.tabs.dashboard_investment_section import render_investment_section
from src.tabs.dashboard_optimization_section import render_optimization_section
from src.tabs.dashboard_stress_section import render_stress_section
from src.tabs.dashboard_backtest_section import render_backtest_section
from src.tabs.dashboard_factor_section import render_factor_section


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
    mode,
    frontier_data,
    current_portfolio,
    max_sharpe_portfolio,
    min_vol_portfolio,
    stress_results,
    backtest_summary,
    benchmark_summary,
    backtest_dates,
    capm_stats,
) -> None:
    # ---------------------------------
    # Jump navigation
    # ---------------------------------
    st.markdown("### Jump to Section")

    if mode == "Beginner":
        nav_links = """
[📊 Portfolio Overview](#portfolio-overview) •
[⚠️ Risk Metrics](#risk-metrics) •
[🎲 Monte-carlo-simulation](#monte-carlo-simulation) •
[💰 Investment Projection](#investment-projection)
"""
    else:
        nav_links = """
[📊 Portfolio Overview](#portfolio-overview) •
[⚠️ Risk Metrics](#risk-metrics) •
[🎲 Monte-carlo-simulation](#monte-carlo-simulation) •
[💰 Investment Projection](#investment-projection) •
[📈 Portfolio Optimization](#portfolio-optimization) •
[🧪 Stress Testing](#stress-testing) •
[📉 Historical Backtest](#historical-backtest) •
[📐 Factor Analysis](#factor-analysis-capm)
"""

    st.markdown(nav_links)
    st.divider()

    # ---------------------------------
    # Portfolio overview
    # ---------------------------------
    st.markdown("## 📊 Portfolio Overview")

    render_portfolio_overview(
        asset_cols=asset_cols,
        horizon_days=horizon_days,
        n_sims=n_sims,
        confidence_level=confidence_level,
    )

    st.markdown("#### Portfolio Configuration")

    weights_df = pd.DataFrame(
        {
            "Asset": asset_cols,
            "Normalized Weight": [f"{w:.2%}" for w in weights],
        }
    )

    st.dataframe(
        weights_df,
        width="stretch",
        hide_index=True,
    )

    st.markdown("[Back to top](#jump-to-section)")
    st.divider()

    # ---------------------------------
    # Risk metrics
    # ---------------------------------
    st.markdown("## ⚠️ Risk Metrics")

    render_risk_section(
        risk_summary=risk_summary,
        confidence_level=confidence_level,
        mode=mode,
    )

    st.markdown("[Back to top](#jump-to-section)")
    st.divider()

    # ---------------------------------
    # Monte Carlo simulation
    # ---------------------------------
    st.markdown("## 🎲 Monte Carlo Simulation")

    render_chart_section(
        portfolio_values=portfolio_values,
        sim_returns=sim_returns,
        risk_summary=risk_summary,
    )

    st.markdown("[Back to top](#jump-to-section)")
    st.divider()

    # ---------------------------------
    # Investment projection
    # ---------------------------------
    st.markdown("## 💰 Investment Projection")

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

    st.markdown("[Back to top](#jump-to-section)")

    # ---------------------------------
    # Professional-only sections
    # ---------------------------------
    if mode == "Professional":
        st.divider()
        st.markdown("## 📈 Portfolio Optimization")

        render_optimization_section(
            asset_cols=asset_cols,
            frontier_data=frontier_data,
            current_portfolio=current_portfolio,
            max_sharpe_portfolio=max_sharpe_portfolio,
            min_vol_portfolio=min_vol_portfolio,
        )

        st.markdown("[Back to top](#jump-to-section)")
        st.divider()

        st.markdown("## 🧪 Stress Testing")

        render_stress_section(stress_results)

        st.markdown("[Back to top](#jump-to-section)")
        st.divider()

        st.markdown("## 📉 Historical Backtest")

        render_backtest_section(
            backtest_summary=backtest_summary,
            benchmark_summary=benchmark_summary,
            date_index=backtest_dates,
        )

        st.markdown("[Back to top](#jump-to-section)")
        st.divider()

        st.markdown("## 📐 Factor Analysis (CAPM)")

        render_factor_section(capm_stats)

        st.markdown("[Back to top](#jump-to-section)")