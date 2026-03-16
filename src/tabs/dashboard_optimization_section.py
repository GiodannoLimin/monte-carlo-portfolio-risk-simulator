import pandas as pd
import streamlit as st

from src.plotting import plot_efficient_frontier


def render_optimization_section(
    asset_cols,
    frontier_data,
    current_portfolio,
    max_sharpe_portfolio,
    min_vol_portfolio,
) -> None:
    st.subheader("Portfolio Optimization")
    st.markdown(
        '<div class="section-note">This section explores thousands of possible portfolios and compares your current allocation to optimized alternatives.</div>',
        unsafe_allow_html=True
    )

    st.plotly_chart(
        plot_efficient_frontier(
            frontier_data,
            current_portfolio,
            max_sharpe_portfolio,
            min_vol_portfolio,
        ),
        width="stretch"
    )

    o1, o2, o3 = st.columns(3)
    o1.metric("Current Sharpe", f"{current_portfolio['sharpe']:.2f}")
    o2.metric("Max Sharpe", f"{max_sharpe_portfolio['sharpe']:.2f}")
    o3.metric("Min Volatility", f"{min_vol_portfolio['volatility']:.2%}")

    st.markdown("### Optimized Portfolio Weights")

    left, right = st.columns(2)

    with left:
        st.markdown("**Maximum Sharpe Portfolio**")
        st.dataframe(
            pd.DataFrame({
                "Asset": asset_cols,
                "Weight": max_sharpe_portfolio["weights"],
            }),
            hide_index=True,
            width="stretch"
        )

    with right:
        st.markdown("**Minimum Volatility Portfolio**")
        st.dataframe(
            pd.DataFrame({
                "Asset": asset_cols,
                "Weight": min_vol_portfolio["weights"],
            }),
            hide_index=True,
            width="stretch"
        )