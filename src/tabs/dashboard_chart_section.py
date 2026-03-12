import streamlit as st

from src.plotting import (
    plot_simulated_portfolio_paths,
    plot_return_distribution,
    plot_terminal_value_distribution,
)


def render_chart_section(portfolio_values, sim_returns, risk_summary) -> None:
    st.subheader("Charts")

    with st.expander("Simulated Portfolio Paths", expanded=True):
        st.plotly_chart(
            plot_simulated_portfolio_paths(portfolio_values, max_lines=20),
            width="stretch"
        )
        st.caption("Each line is one possible simulated future path of the portfolio.")

    with st.expander("Return Distribution", expanded=True):
        st.plotly_chart(
            plot_return_distribution(sim_returns, risk_summary["var"], risk_summary["cvar"]),
            width="stretch"
        )
        st.caption("Histogram of simulated portfolio returns. VaR and CVaR mark downside tail risk.")

    with st.expander("Terminal Portfolio Value Distribution", expanded=False):
        st.plotly_chart(
            plot_terminal_value_distribution(portfolio_values[-1]),
            width="stretch"
        )
        st.caption(
            "This shows the simulated distribution of the portfolio model's terminal value "
            "based on weighted asset prices. It is separate from your personal investment amount."
        )