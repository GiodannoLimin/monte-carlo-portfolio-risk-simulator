import streamlit as st

from src.ui_text import DISCLAIMER_TEXT


def render_risk_section(risk_summary, confidence_level) -> None:
    st.subheader("Portfolio Risk Simulation")
    st.markdown(
        '<div class="section-note">This section analyzes simulated portfolio returns and risk. '
        'It is based on modeled portfolio behavior, not directly on your investment amount.</div>',
        unsafe_allow_html=True
    )

    m1, m2, m3, m4 = st.columns(4)
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
    m4.metric(
        "CVaR",
        f"{risk_summary['cvar']:.2%}",
        help="Average return in the worst tail beyond VaR."
    )

    st.info(
        f"""
**Interpretation**

- Average simulated portfolio return over the selected horizon: **{risk_summary['expected_return']:.2%}**
- **VaR** at **{confidence_level:.0%}** confidence: **{risk_summary['var']:.2%}**
- **CVaR**: **{risk_summary['cvar']:.2%}**
- These figures describe **portfolio risk and return behavior**, not directly the dollar value of your personal investment.
        """
    )

    with st.expander("⚠️ Important Disclaimer"):
        st.write(DISCLAIMER_TEXT)