import streamlit as st

from src.plotting import plot_factor_scatter


def render_factor_section(capm_stats) -> None:
    st.subheader("Factor Exposure Analysis")
    st.markdown(
        '<div class="section-note">This section estimates the portfolio’s exposure to the market using a simple CAPM-style regression against SPY.</div>',
        unsafe_allow_html=True
    )

    f1, f2, f3 = st.columns(3)
    f1.metric("Beta", f"{capm_stats['beta']:.2f}")
    f2.metric("Alpha (Annualized)", f"{capm_stats['alpha_annual']:.2%}")
    f3.metric("R-squared", f"{capm_stats['r_squared']:.2f}")

    st.plotly_chart(
        plot_factor_scatter(
            capm_stats["market_returns"],
            capm_stats["portfolio_returns"],
            capm_stats["fitted_returns"],
        ),
        width="stretch"
    )

    st.caption(
        "Beta measures sensitivity to the market. Alpha measures return beyond market exposure. "
        "R-squared shows how much of portfolio movement is explained by the market."
    )