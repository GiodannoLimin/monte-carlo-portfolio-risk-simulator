import streamlit as st


def render_portfolio_overview(asset_cols, horizon_days, n_sims, confidence_level) -> None:
    st.markdown(
        f"""
<div class="overview-card">
    <div style="font-size: 1.08rem; font-weight: 600; margin-bottom: 8px;">
        Portfolio Overview
    </div>
    <div style="opacity: 0.9;">
        Simulating <b>{', '.join(asset_cols)}</b> over <b>{horizon_days}</b> trading days
        using <b>{n_sims:,}</b> Monte Carlo scenarios at <b>{confidence_level:.0%}</b> confidence.
    </div>
</div>
        """,
        unsafe_allow_html=True
    )