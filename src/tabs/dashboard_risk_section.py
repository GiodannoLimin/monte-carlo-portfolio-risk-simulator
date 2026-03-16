import streamlit as st

from src.app_text import DISCLAIMER_TEXT


def render_risk_section(risk_summary, confidence_level, mode="Professional") -> None:
    st.subheader("Portfolio Risk Simulation")
    st.markdown(
        '<div class="section-note">This section analyzes simulated portfolio returns and risk. '
        'It is based on modeled portfolio behavior, not directly on your investment amount.</div>',
        unsafe_allow_html=True
    )

    if mode == "Beginner":
        m1, m2, m3 = st.columns(3)
        m1.metric(
            "Expected Return",
            f"{risk_summary['expected_return']:.2%}",
            help="Average simulated portfolio return over the selected horizon."
        )
        m2.metric(
            "Volatility",
            f"{risk_summary['volatility']:.2%}",
            help="Typical fluctuation size of simulated portfolio returns."
        )
        m3.metric(
            "VaR",
            f"{risk_summary['var']:.2%}",
            help="Downside threshold from the simulated return distribution at the chosen confidence level."
        )

        st.info(
            f"""
**Interpretation**

- Average simulated portfolio return over the selected horizon: **{risk_summary['expected_return']:.2%}**
- **VaR** at **{confidence_level:.0%}** confidence: **{risk_summary['var']:.2%}**
- These figures summarize the portfolio's simulated return and downside risk.
            """
        )

    else:
        m1, m2, m3, m4 = st.columns(4)
        m5, m6, m7 = st.columns(3)

        m1.metric("Expected Return", f"{risk_summary['expected_return']:.2%}")
        m2.metric("Volatility", f"{risk_summary['volatility']:.2%}")
        m3.metric("VaR", f"{risk_summary['var']:.2%}")
        m4.metric("CVaR", f"{risk_summary['cvar']:.2%}")
        m5.metric("Sharpe Ratio", f"{risk_summary['sharpe_ratio']:.2f}")
        m6.metric("Sortino Ratio", f"{risk_summary['sortino_ratio']:.2f}")
        m7.metric("Max Drawdown", f"{risk_summary['max_drawdown']:.2%}")

        st.info(
            f"""
**Interpretation**

- Average simulated portfolio return over the selected horizon: **{risk_summary['expected_return']:.2%}**
- **VaR** at **{confidence_level:.0%}** confidence: **{risk_summary['var']:.2%}**
- **CVaR**: **{risk_summary['cvar']:.2%}**
- **Sharpe ratio**: **{risk_summary['sharpe_ratio']:.2f}**
- **Sortino ratio**: **{risk_summary['sortino_ratio']:.2f}**
- **Maximum drawdown** of the median simulated path: **{risk_summary['max_drawdown']:.2%}**
            """
        )