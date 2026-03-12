import numpy as np
import pandas as pd
import plotly.graph_objects as go


def plot_historical_stock(price_df: pd.DataFrame, ticker: str):
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=price_df["Date"],
            y=price_df[ticker],
            mode="lines",
            name=ticker
        )
    )

    fig.update_layout(
        title=f"Historical Closing Prices: {ticker}",
        xaxis_title="Date",
        yaxis_title="Price",
        template="plotly_dark",
        height=360,
        margin=dict(l=30, r=30, t=60, b=30),
    )
    return fig


def plot_simulated_portfolio_paths(portfolio_values: np.ndarray, max_lines: int = 25):
    fig = go.Figure()

    n_sims = portfolio_values.shape[1]
    n_lines = min(max_lines, n_sims)

    for i in range(n_lines):
        fig.add_trace(
            go.Scatter(
                y=portfolio_values[:, i],
                mode="lines",
                line=dict(width=1),
                opacity=0.45,
                showlegend=False
            )
        )

    fig.update_layout(
        title="Sample Simulated Portfolio Paths",
        xaxis_title="Days",
        yaxis_title="Portfolio Value",
        template="plotly_dark",
        height=360,
        margin=dict(l=30, r=30, t=60, b=30),
    )
    return fig


def plot_return_distribution(returns: np.ndarray, var: float, cvar: float):
    fig = go.Figure()

    fig.add_trace(
        go.Histogram(
            x=returns,
            nbinsx=50,
            name="Portfolio Returns",
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
        height=360,
        margin=dict(l=30, r=30, t=60, b=30),
    )
    return fig


def plot_terminal_value_distribution(final_values: np.ndarray):
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
        height=360,
        margin=dict(l=30, r=30, t=60, b=30),
    )
    return fig


def plot_projection_table_bars(projection_df: pd.DataFrame):
    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=projection_df["Horizon"],
            y=projection_df["Median Final Value"],
            name="Median Final Value"
        )
    )

    fig.update_layout(
        title="Median Final Value by Horizon",
        xaxis_title="Horizon",
        yaxis_title="Value",
        template="plotly_dark",
        height=340,
        margin=dict(l=30, r=30, t=60, b=30),
    )
    return fig