import pandas as pd
import plotly.express as px
import streamlit as st

from src.plotting import plot_projection_table_bars
from src.projections import build_projection_df


def render_investment_section(
    latest_prices,
    mu,
    sigma,
    weights,
    initial_investment,
    monthly_contribution,
    selected_years,
    selected_total_contributions,
    investment_summary,
    selected_final_values,
) -> None:
    st.subheader("Investment Outcome Projection")
    st.markdown(
        '<div class="section-note">This section applies the simulated portfolio returns to your chosen '
        'initial investment and optional recurring monthly contribution.</div>',
        unsafe_allow_html=True
    )

    i1, i2, i3, i4 = st.columns(4)
    i1.metric("Median Final Investment Value", f"${investment_summary['median_final_value']:,.2f}")
    i2.metric("Mean Final Investment Value", f"${investment_summary['mean_final_value']:,.2f}")
    i3.metric("5th Percentile Value", f"${investment_summary['p5_final_value']:,.2f}")
    i4.metric("95th Percentile Value", f"${investment_summary['p95_final_value']:,.2f}")

    j1, j2, j3 = st.columns(3)
    j1.metric("Initial + Recurring Contributions", f"${selected_total_contributions:,.2f}")
    j2.metric("Median Profit / Loss", f"${investment_summary['median_pnl']:,.2f}")
    j3.metric("Mean Profit / Loss", f"${investment_summary['mean_pnl']:,.2f}")

    st.info(
        f"""
**Investment interpretation**

For the selected horizon (**{selected_years:.1f} years**), the simulation applies the modeled portfolio returns
to your investment settings:

- **Initial investment:** ${initial_investment:,.2f}
- **Monthly contribution:** ${monthly_contribution:,.2f}
- **Total contributions over this selected horizon:** ${selected_total_contributions:,.2f}

The **median final investment value** is **${investment_summary['median_final_value']:,.2f}**.
        """
    )

    projection_df = build_projection_df(
        latest_prices=latest_prices,
        mu=mu,
        sigma=sigma,
        weights=weights,
        initial_investment=initial_investment,
        monthly_contribution=monthly_contribution,
    )

    display_df = projection_df[
        [
            "Horizon",
            "Total Contributions",
            "Median Profit/Loss",
            "5th Percentile Profit/Loss",
            "95th Percentile Profit/Loss",
        ]
    ].copy()

    display_df["Total Contributions"] = display_df["Total Contributions"].map(lambda x: f"${x:,.0f}")
    display_df["Median Profit/Loss"] = display_df["Median Profit/Loss"].map(lambda x: f"${x:,.0f}")
    display_df["5th Percentile Profit/Loss"] = display_df["5th Percentile Profit/Loss"].map(lambda x: f"${x:,.0f}")
    display_df["95th Percentile Profit/Loss"] = display_df["95th Percentile Profit/Loss"].map(lambda x: f"${x:,.0f}")

    display_df = display_df.rename(columns={
        "Total Contributions": "Contributions",
        "Median Profit/Loss": "Median P/L",
        "5th Percentile Profit/Loss": "Worst 5%",
        "95th Percentile Profit/Loss": "Best 5%",
    })

    st.caption("Quick summary of typical, downside, and upside projected profit/loss by investment horizon.")

    st.dataframe(display_df, width="stretch", hide_index=True)

    st.markdown("")
    st.markdown("### Projected Profit/Loss by Investment Horizon")

    st.plotly_chart(
        plot_projection_table_bars(projection_df),
        width="stretch"
    )

    st.markdown("")
    st.markdown("### Distribution of Simulated Final Values")

    final_values_df = pd.DataFrame({
        "Final Value": selected_final_values
    })

    fig_final_values = px.histogram(
        final_values_df,
        x="Final Value",
        nbins=40,
        title=None,
    )

    fig_final_values.update_layout(
        xaxis_title="Final Portfolio Value ($)",
        yaxis_title="Frequency",
        bargap=0.05,
    )

    st.plotly_chart(fig_final_values, width="stretch")