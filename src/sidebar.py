import streamlit as st


def render_sidebar() -> dict:
    with st.sidebar:
        st.header("Control Panel")

        st.write("**Market Data**")
        tickers_text = st.text_input(
            "Tickers (comma separated)",
            value="AAPL,MSFT,NVDA,SPY"
        )
        selected_period = st.selectbox(
            "Historical lookback",
            options=["5y", "10y", "max"],
            index=1
        )
        refresh = st.button("Refresh Market Data")

        st.write("---")
        st.write("**Simulation Settings**")

        horizon_days = st.selectbox(
            "Time horizon (days)",
            options=[126, 252, 378, 504, 630, 756],
            index=0,
            help="126 ≈ 0.5 years, 252 ≈ 1 year, ..., 756 ≈ 3 years."
        )

        n_sims = st.slider(
            "Number of simulations",
            1000, 20000, 8000, 1000
        )

        confidence_level = st.slider(
            "Confidence level",
            0.90, 0.99, 0.95, 0.01
        )

        initial_investment = st.number_input(
            "Initial investment ($)",
            min_value=0.0,
            value=10000.0,
            step=500.0
        )

        monthly_contribution = st.number_input(
            "Recurring monthly contribution ($)",
            min_value=0.0,
            value=0.0,
            step=100.0
        )

        st.write("---")
        st.write("**Portfolio Weights**")
        st.caption("Raw weights are normalized automatically.")

        # Temporary placeholder. app.py will overwrite with the real asset sliders later if needed.
        # But to keep the app working as-is, this file only returns base settings first.
        return {
            "tickers_text": tickers_text,
            "selected_period": selected_period,
            "refresh": refresh,
            "horizon_days": horizon_days,
            "n_sims": n_sims,
            "confidence_level": confidence_level,
            "initial_investment": initial_investment,
            "monthly_contribution": monthly_contribution,
            "weights_input": [],
        }


def render_weight_sliders(asset_cols) -> list[float]:
    weights_input = []
    with st.sidebar:
        st.write("---")
        st.write("**Portfolio Weights**")
        st.caption("Raw weights are normalized automatically.")

        for ticker in asset_cols:
            w = st.slider(
                f"{ticker} weight",
                min_value=0.0,
                max_value=1.0,
                value=float(1 / len(asset_cols)),
                step=0.05
            )
            weights_input.append(w)

    return weights_input