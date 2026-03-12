import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def plot_historical_stock(price_df: pd.DataFrame, ticker: str):
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=price_df["Date"],
            y=price_df[ticker],
            mode="lines",
            name=ticker,
            line=dict(width=2),
        )
    )

    fig.update_layout(
        title=f"Historical Price Chart: {ticker}",
        xaxis_title="Date",
        yaxis_title="Price",
        template="plotly_dark",
        height=360,
        margin=dict(l=30, r=30, t=60, b=30),
    )
    return fig


def plot_simulated_portfolio_paths(portfolio_values, max_lines: int = 20):
    fig = go.Figure()

    n_sims = portfolio_values.shape[1]
    n_lines = min(max_lines, n_sims)

    for i in range(n_lines):
        fig.add_trace(
            go.Scatter(
                y=portfolio_values[:, i],
                mode="lines",
                line=dict(width=1),
                opacity=0.40,
                showlegend=False
            )
        )

    fig.update_layout(
        title="Sample Simulated Portfolio Paths",
        xaxis_title="Days",
        yaxis_title="Portfolio Value",
        template="plotly_dark",
        height=340,
        margin=dict(l=30, r=30, t=60, b=30),
    )
    return fig


def plot_return_distribution(returns, var: float, cvar: float):
    fig = go.Figure()

    fig.add_trace(
        go.Histogram(
            x=returns,
            nbinsx=50,
            opacity=0.85
        )
    )

    fig.add_vline(
        x=var,
        line_width=2,
        line_dash="dash",
        annotation_text="VaR",
        annotation_position="top"
    )
    fig.add_vline(
        x=cvar,
        line_width=2,
        line_dash="dot",
        annotation_text="CVaR",
        annotation_position="top"
    )

    fig.update_layout(
        title="Distribution of Simulated Portfolio Returns",
        xaxis_title="Return",
        yaxis_title="Frequency",
        template="plotly_dark",
        height=340,
        margin=dict(l=30, r=30, t=60, b=30),
    )
    return fig


def plot_terminal_value_distribution(final_values):
    fig = go.Figure()

    fig.add_trace(
        go.Histogram(
            x=final_values,
            nbinsx=45,
            opacity=0.85
        )
    )

    fig.update_layout(
        title="Distribution of Final Portfolio Values",
        xaxis_title="Final Portfolio Value",
        yaxis_title="Frequency",
        template="plotly_dark",
        height=340,
        margin=dict(l=30, r=30, t=60, b=30),
    )
    return fig
import plotly.graph_objects as go


def plot_projection_table_bars(df):
    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=df["Horizon"],
            y=df["Median Profit/Loss"],
            name="Median Profit/Loss",
            text=[f"${v:,.0f}" for v in df["Median Profit/Loss"]],
            textposition="outside",
        )
    )

    fig.add_trace(
        go.Scatter(
            x=df["Horizon"],
            y=df["5th Percentile Profit/Loss"],
            mode="lines+markers",
            name="5th Percentile",
        )
    )

    fig.add_trace(
        go.Scatter(
            x=df["Horizon"],
            y=df["95th Percentile Profit/Loss"],
            mode="lines+markers",
            name="95th Percentile",
        )
    )

    fig.update_layout(
        template="plotly_dark",
        xaxis_title="Investment Horizon",
        yaxis_title="Profit / Loss ($)",
        legend_title="Scenario",
    )

    return fig