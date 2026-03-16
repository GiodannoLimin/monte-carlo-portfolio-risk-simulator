import streamlit as st

from src.plotting import plot_backtest_comparison


def render_backtest_section(backtest_summary, benchmark_summary, date_index) -> None:
    st.subheader("Historical Backtest")
    st.markdown(
        '<div class="section-note">This section shows how the selected portfolio would have performed historically using actual past returns.</div>',
        unsafe_allow_html=True
    )

    st.plotly_chart(
        plot_backtest_comparison(
            date_index,
            backtest_summary["growth"],
            benchmark_summary["growth"],
        ),
        width="stretch"
    )

    b1, b2, b3, b4 = st.columns(4)
    b1.metric("Portfolio Total Return", f"{backtest_summary['total_return']:.2%}")
    b2.metric("Portfolio Annual Return", f"{backtest_summary['annual_return']:.2%}")
    b3.metric("Portfolio Sharpe", f"{backtest_summary['sharpe_ratio']:.2f}")
    b4.metric("Portfolio Max Drawdown", f"{backtest_summary['max_drawdown']:.2%}")

    c1, c2 = st.columns(2)
    c1.metric("Benchmark Total Return", f"{benchmark_summary['total_return']:.2%}")
    c2.metric("Benchmark Annual Return", f"{benchmark_summary['annual_return']:.2%}")