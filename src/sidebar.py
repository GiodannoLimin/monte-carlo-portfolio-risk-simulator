import streamlit as st


POPULAR_TICKERS = {
    "Popular Stocks": {
        "AAPL — Apple": "AAPL",
        "MSFT — Microsoft": "MSFT",
        "NVDA — NVIDIA": "NVDA",
        "AMZN — Amazon": "AMZN",
        "GOOGL — Alphabet": "GOOGL",
        "META — Meta": "META",
        "TSLA — Tesla": "TSLA",
    },
    "Popular ETFs": {
        "SPY — SPDR S&P 500 ETF": "SPY",
        "QQQ — Invesco QQQ Trust": "QQQ",
        "VTI — Vanguard Total Stock Market ETF": "VTI",
        "VOO — Vanguard S&P 500 ETF": "VOO",
        "IVV — iShares Core S&P 500 ETF": "IVV",
        "DIA — SPDR Dow Jones Industrial Average ETF": "DIA",
        "IWM — iShares Russell 2000 ETF": "IWM",
    },
    "Defensive / Income": {
        "JNJ — Johnson & Johnson": "JNJ",
        "PG — Procter & Gamble": "PG",
        "KO — Coca-Cola": "KO",
        "PEP — PepsiCo": "PEP",
        "XLU — Utilities Select Sector SPDR Fund": "XLU",
        "SCHD — Schwab U.S. Dividend Equity ETF": "SCHD",
    },
}


STARTER_PORTFOLIOS = {
    "None": [],
    "Big Tech Basket": ["AAPL", "MSFT", "NVDA", "AMZN", "GOOGL", "META"],
    "US Market ETFs": ["SPY", "QQQ", "VTI", "DIA"],
    "Growth + Broad Market": ["AAPL", "MSFT", "NVDA", "SPY", "QQQ"],
    "Balanced Example": ["SPY", "QQQ", "SCHD", "VNQ", "TLT"],
}


def _deduplicate_preserve_order(items: list[str]) -> list[str]:
    seen = set()
    result = []

    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)

    return result


def _parse_manual_tickers(manual_tickers: str) -> list[str]:
    return [ticker.strip().upper() for ticker in manual_tickers.split(",") if ticker.strip()]


def _build_final_ticker_list(
    manual_tickers: str,
    selected_preset: str,
    selected_popular_labels: list[str],
    popular_category: str,
) -> list[str]:
    manual_list = _parse_manual_tickers(manual_tickers)
    preset_list = STARTER_PORTFOLIOS.get(selected_preset, [])

    category_mapping = POPULAR_TICKERS.get(popular_category, {})
    popular_list = [
        category_mapping[label]
        for label in selected_popular_labels
        if label in category_mapping
    ]

    final_list = manual_list + preset_list + popular_list
    return _deduplicate_preserve_order(final_list)


def render_sidebar() -> dict:
    with st.sidebar:
        st.header("Control Panel")

        # ---------------------------------
        # Market data
        # ---------------------------------
        st.markdown("### Market Data")

        manual_tickers = st.text_input(
            "Tickers (comma separated)",
            value="SPY,QQQ,AAPL,MSFT",
            placeholder="Example: AAPL, MSFT, NVDA, SPY",
            help="A demo portfolio is loaded by default. You can edit it manually or use the starter options below.",
        )

        st.caption("Default demo portfolio loaded. Edit the tickers or use the starter options below.")
        
        st.caption("New to tickers? Use the starter options below.")

        selected_preset = st.selectbox(
            "Starter portfolio",
            options=list(STARTER_PORTFOLIOS.keys()),
            index=0,
            help="Quickly load a beginner-friendly example portfolio.",
        )

        popular_category = st.selectbox(
            "Popular ticker category",
            options=list(POPULAR_TICKERS.keys()),
            index=0,
        )

        popular_options = list(POPULAR_TICKERS[popular_category].keys())

        selected_popular_labels = st.multiselect(
            "Popular tickers",
            options=popular_options,
            default=[],
            help="Add one or more popular stocks or ETFs to the ticker list.",
        )

        final_tickers = _build_final_ticker_list(
            manual_tickers=manual_tickers,
            selected_preset=selected_preset,
            selected_popular_labels=selected_popular_labels,
            popular_category=popular_category,
        )

        tickers_text = ",".join(final_tickers)

        if final_tickers:
            st.caption("Final ticker list:")
            st.code(tickers_text, language=None)
        else:
            st.caption("Final ticker list: none selected yet.")

        selected_period = st.selectbox(
            "Historical lookback",
            options=["5y", "10y", "max"],
            index=1,
            help="How much historical data to use for estimating model inputs.",
        )

        refresh = st.button("Refresh Market Data", use_container_width=True)

        st.divider()

        # ---------------------------------
        # Simulation settings
        # ---------------------------------
        st.markdown("### Simulation Settings")

        horizon_days = st.selectbox(
            "Time horizon (days)",
            options=[126, 252, 378, 504, 630, 756],
            index=0,
            help="126 ≈ 0.5 years, 252 ≈ 1 year, ..., 756 ≈ 3 years.",
        )

        n_sims = st.slider(
            "Number of simulations",
            min_value=1000,
            max_value=20000,
            value=8000,
            step=1000,
            help="More simulations usually give smoother estimates but increase runtime.",
        )

        confidence_level = st.slider(
            "Confidence level",
            min_value=0.90,
            max_value=0.99,
            value=0.95,
            step=0.01,
            help="Used for downside risk metrics such as VaR and CVaR.",
        )

        st.divider()

        # ---------------------------------
        # Investment settings
        # ---------------------------------
        st.markdown("### Investment Settings")

        initial_investment = st.number_input(
            "Initial investment ($)",
            min_value=0.0,
            value=10000.0,
            step=500.0,
        )

        monthly_contribution = st.number_input(
            "Recurring monthly contribution ($)",
            min_value=0.0,
            value=0.0,
            step=100.0,
        )

        st.divider()

        # ---------------------------------
        # Portfolio weights placeholder
        # ---------------------------------
        st.markdown("### Portfolio Weights")
        st.caption("Weights appear after valid tickers are loaded. Raw weights are normalized automatically.")

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
        st.divider()
        st.markdown("### Portfolio Weights")
        st.caption("Raw weights are normalized automatically.")

        default_weight = float(1 / len(asset_cols)) if len(asset_cols) > 0 else 0.0

        for ticker in asset_cols:
            w = st.slider(
                f"{ticker} weight",
                min_value=0.0,
                max_value=1.0,
                value=default_weight,
                step=0.05,
            )
            weights_input.append(w)

    return weights_input