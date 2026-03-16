import streamlit as st


def render_learn_tab(mode: str = "Beginner") -> None:
    st.subheader("Learn")

    if mode == "Beginner":
        st.markdown(
            """
This section is a beginner-friendly guide to the simulator and the finance concepts behind it.

You do not need a finance background to follow it.
Start with the overview below, then use the full handbook preview for the complete guide.
            """
        )
    else:
        st.markdown(
            """
This section combines intuitive explanation with technical interpretation.

Use the overview cards for orientation, then read the full handbook below for methodology, formulas, interpretation, and limitations.
            """
        )

    st.markdown("### What this simulator helps you analyze")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            """
- **Monte Carlo simulation** of many possible portfolio futures  
- **Risk metrics** such as volatility, VaR, and CVaR  
- **Portfolio optimization** and efficient frontier comparison  
- **Historical backtesting** against benchmark behavior  
            """
        )

    with col2:
        st.markdown(
            """
- **Factor analysis** using CAPM-style market exposure  
- **Stress testing** under adverse assumptions  
- **Investment projections** with contributions over time  
- **Interpretation support** for charts and output metrics  
            """
        )

    st.markdown("### Suggested reading path")

    st.markdown(
        """
1. **Quick intuition**  
   Understand what the simulator does and why Monte Carlo analysis is useful.

2. **Portfolio basics**  
   Learn how weights, return, risk, and diversification affect outcomes.

3. **Chart interpretation**  
   Read simulated paths, return distributions, terminal value distributions, and frontier plots.

4. **Risk analysis**  
   Understand volatility, VaR, CVaR, downside risk, and tail behavior.

5. **Advanced interpretation**  
   Explore optimization, backtesting, factor analysis, stress testing, and model limitations.
        """
    )

    with st.expander("Who is this guide for?"):
        st.markdown(
            """
This guide is designed for:

- beginners learning portfolio analytics for the first time
- students building intuition about simulation and risk
- users who want to understand what each dashboard output means
- more advanced readers who want formulas and model assumptions in one place
            """
        )

    with st.expander("How should I use the handbook?"):
        st.markdown(
            """
A good approach is:

- first, configure a portfolio in the sidebar
- then review the dashboard outputs
- then open the handbook preview below
- read the sections that match the outputs you are currently looking at

This makes the learning experience much more practical because the concepts are tied directly to your portfolio settings.
            """
        )

    with st.expander("Important mindset when reading results"):
        st.markdown(
            """
The simulator is best used as a **decision-support and learning tool**, not as a certainty engine.

It helps answer questions like:

- What range of outcomes looks plausible under the model?
- How much downside risk appears in weak scenarios?
- How does my portfolio compare with alternatives?
- How sensitive are conclusions to stress assumptions?

It does **not** tell you the exact future.
            """
        )