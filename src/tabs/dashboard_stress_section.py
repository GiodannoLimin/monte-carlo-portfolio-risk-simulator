import pandas as pd
import streamlit as st

from src.plotting import plot_stress_test_results


def render_stress_section(stress_results) -> None:
    st.subheader("Stress Testing")
    st.markdown(
        '<div class="section-note">This section tests how the portfolio behaves under adverse market scenarios.</div>',
        unsafe_allow_html=True
    )

    st.plotly_chart(
        plot_stress_test_results(stress_results),
        width="stretch"
    )

    df = pd.DataFrame(stress_results).copy()
    df["Expected Return"] = df["Expected Return"].map(lambda x: f"{x:.2%}")
    df["Volatility"] = df["Volatility"].map(lambda x: f"{x:.2%}")
    df["VaR"] = df["VaR"].map(lambda x: f"{x:.2%}")
    df["CVaR"] = df["CVaR"].map(lambda x: f"{x:.2%}")

    st.dataframe(df, hide_index=True, width="stretch")