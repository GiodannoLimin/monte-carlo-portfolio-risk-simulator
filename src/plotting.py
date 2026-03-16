import numpy as np
import pandas as pd
import plotly.graph_objects as go


def _apply_base_layout(
    fig: go.Figure,
    title: str,
    xaxis_title: str = "",
    yaxis_title: str = "",
    height: int = 420,
    margin: dict | None = None,
    plot_bgcolor: str = "rgba(255,255,255,0.03)",
    paper_bgcolor: str = "rgba(0,0,0,0)",
) -> go.Figure:
    if margin is None:
        margin = dict(l=80, r=50, t=80, b=80)

    fig.update_layout(
        title=title,
        xaxis_title=xaxis_title,
        yaxis_title=yaxis_title,
        template="none",
        height=height,
        margin=margin,
        paper_bgcolor=paper_bgcolor,
        plot_bgcolor=plot_bgcolor,
        font=dict(color="white"),
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            borderwidth=0,
        ),
    )

    fig.update_xaxes(
        automargin=True,
        showgrid=True,
        gridcolor="rgba(255,255,255,0.10)",
        zeroline=False,
        color="white",
    )
    fig.update_yaxes(
        automargin=True,
        showgrid=True,
        gridcolor="rgba(255,255,255,0.10)",
        zeroline=False,
        color="white",
    )

    return fig


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

    return _apply_base_layout(
        fig,
        title=f"Historical Price Chart: {ticker}",
        xaxis_title="Date",
        yaxis_title="Price",
        height=360,
    )


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
                opacity=0.35,
                showlegend=False,
            )
        )

    return _apply_base_layout(
        fig,
        title="Sample Simulated Portfolio Paths",
        xaxis_title="Days",
        yaxis_title="Portfolio Value",
        height=360,
    )


def plot_return_distribution(returns, var: float, cvar: float):
    fig = go.Figure()

    fig.add_trace(
        go.Histogram(
            x=returns,
            nbinsx=50,
            opacity=0.85,
            marker=dict(
                color="rgba(102, 153, 255, 0.75)",
                line=dict(width=0),
            ),
            name="Returns",
        )
    )

    fig.add_vline(
        x=var,
        line_width=2,
        line_dash="dash",
        annotation_text="VaR",
        annotation_position="top right",
    )

    fig.add_vline(
        x=cvar,
        line_width=2,
        line_dash="dot",
        annotation_text="CVaR",
        annotation_position="top left",
    )

    return _apply_base_layout(
        fig,
        title="Distribution of Simulated Portfolio Returns",
        xaxis_title="Return",
        yaxis_title="Frequency",
        height=360,
    )


def plot_terminal_value_distribution(final_values):
    fig = go.Figure()

    fig.add_trace(
        go.Histogram(
            x=final_values,
            nbinsx=45,
            opacity=0.85,
            marker=dict(
                color="rgba(140, 180, 220, 0.85)",
                line=dict(width=0),
            ),
            name="Final Values",
        )
    )

    return _apply_base_layout(
        fig,
        title="Distribution of Simulated Final Values",
        xaxis_title="Final Portfolio Value ($)",
        yaxis_title="Frequency",
        height=420,
    )


def plot_projection_table_bars(df):
    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=df["Horizon"],
            y=df["Median Profit/Loss"],
            name="Median Profit/Loss",
            text=[f"${v:,.0f}" for v in df["Median Profit/Loss"]],
            textposition="outside",
            cliponaxis=False,
            marker=dict(
                color="rgba(120, 120, 255, 0.85)",
                line=dict(width=0),
            ),
        )
    )

    fig.add_trace(
        go.Scatter(
            x=df["Horizon"],
            y=df["5th Percentile Profit/Loss"],
            mode="lines+markers",
            name="5th Percentile",
            line=dict(width=2),
        )
    )

    fig.add_trace(
        go.Scatter(
            x=df["Horizon"],
            y=df["95th Percentile Profit/Loss"],
            mode="lines+markers",
            name="95th Percentile",
            line=dict(width=2),
        )
    )

    fig.update_layout(
        legend_title="Scenario",
    )

    return _apply_base_layout(
        fig,
        title="Projected Profit/Loss by Investment Horizon",
        xaxis_title="Investment Horizon",
        yaxis_title="Profit / Loss ($)",
        height=520,
        margin=dict(l=80, r=90, t=90, b=80),
    )


def plot_correlation_heatmap(returns_df, asset_cols):
    corr = returns_df[asset_cols].corr()

    fig = go.Figure(
        data=go.Heatmap(
            z=corr.values,
            x=corr.columns,
            y=corr.columns,
            colorscale="RdBu",
            zmin=-1,
            zmax=1,
            colorbar=dict(title="Correlation"),
            text=corr.round(2).values,
            texttemplate="%{text}",
        )
    )

    return _apply_base_layout(
        fig,
        title="Asset Return Correlation Heatmap",
        height=450,
        margin=dict(l=80, r=80, t=80, b=80),
    )


def plot_benchmark_comparison(date_index, user_growth, equal_weight_growth, spy_growth):
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=date_index,
            y=user_growth,
            mode="lines",
            name="User Portfolio",
            line=dict(width=3),
        )
    )

    fig.add_trace(
        go.Scatter(
            x=date_index,
            y=equal_weight_growth,
            mode="lines",
            name="Equal-Weight Portfolio",
            line=dict(width=2, dash="dash"),
        )
    )

    fig.add_trace(
        go.Scatter(
            x=date_index,
            y=spy_growth,
            mode="lines",
            name="SPY Benchmark",
            line=dict(width=2, dash="dot"),
        )
    )

    return _apply_base_layout(
        fig,
        title="Historical Portfolio vs Benchmark Comparison",
        xaxis_title="Date",
        yaxis_title="Growth of $1",
        height=420,
    )


def plot_efficient_frontier(
    frontier_data,
    current_portfolio,
    max_sharpe_portfolio,
    min_vol_portfolio,
):
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=frontier_data["volatilities"],
            y=frontier_data["returns"],
            mode="markers",
            marker=dict(
                size=5,
                color=frontier_data["sharpes"],
                colorscale="Viridis",
                opacity=0.7,
                colorbar=dict(
                    title="Sharpe",
                    x=1.02,
                    y=0.68,
                    len=0.48,
                    thickness=16,
                    outlinewidth=0,
                ),
            ),
            name="Random Portfolios",
            text=[f"Sharpe: {s:.2f}" for s in frontier_data["sharpes"]],
            hovertemplate="Volatility: %{x:.2%}<br>Return: %{y:.2%}<br>%{text}<extra></extra>",
        )
    )

    fig.add_trace(
        go.Scatter(
            x=[current_portfolio["volatility"]],
            y=[current_portfolio["return"]],
            mode="markers",
            marker=dict(
                size=13,
                symbol="x",
                line=dict(width=1, color="white"),
            ),
            name="Current Portfolio",
        )
    )

    fig.add_trace(
        go.Scatter(
            x=[max_sharpe_portfolio["volatility"]],
            y=[max_sharpe_portfolio["return"]],
            mode="markers",
            marker=dict(
                size=16,
                symbol="star",
                line=dict(width=1, color="white"),
            ),
            name="Max Sharpe",
        )
    )

    fig.add_trace(
        go.Scatter(
            x=[min_vol_portfolio["volatility"]],
            y=[min_vol_portfolio["return"]],
            mode="markers",
            marker=dict(
                size=14,
                symbol="diamond",
                line=dict(width=1, color="white"),
            ),
            name="Min Volatility",
        )
    )

    fig.update_layout(
        legend=dict(
            x=1.02,
            y=0.33,
            xanchor="left",
            yanchor="top",
            orientation="v",
            bgcolor="rgba(0,0,0,0)",
        )
    )

    return _apply_base_layout(
        fig,
        title="Efficient Frontier",
        xaxis_title="Annualized Volatility",
        yaxis_title="Annualized Return",
        height=460,
        margin=dict(l=80, r=250, t=80, b=80),
    )


def plot_stress_test_results(stress_results):
    df = pd.DataFrame(stress_results)

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=df["Scenario"],
            y=df["Expected Return"],
            name="Expected Return",
        )
    )

    fig.add_trace(
        go.Bar(
            x=df["Scenario"],
            y=df["VaR"],
            name="VaR",
        )
    )

    fig.add_trace(
        go.Bar(
            x=df["Scenario"],
            y=df["CVaR"],
            name="CVaR",
        )
    )

    fig.update_layout(
        barmode="group",
    )

    return _apply_base_layout(
        fig,
        title="Stress Test Scenario Comparison",
        xaxis_title="Scenario",
        yaxis_title="Return",
        height=440,
        margin=dict(l=80, r=60, t=80, b=90),
    )


def plot_backtest_comparison(date_index, portfolio_growth, benchmark_growth):
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=date_index,
            y=portfolio_growth,
            mode="lines",
            name="Portfolio",
            line=dict(width=3),
        )
    )

    fig.add_trace(
        go.Scatter(
            x=date_index,
            y=benchmark_growth,
            mode="lines",
            name="Benchmark (SPY)",
            line=dict(width=2, dash="dash"),
        )
    )

    return _apply_base_layout(
        fig,
        title="Historical Portfolio Backtest (Daily Rebalanced)",
        xaxis_title="Date",
        yaxis_title="Growth of $1",
        height=420,
    )


def plot_factor_scatter(market_returns, portfolio_returns, fitted_returns):
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=market_returns,
            y=portfolio_returns,
            mode="markers",
            name="Daily Returns",
            opacity=0.45,
        )
    )

    order = np.argsort(market_returns)
    fig.add_trace(
        go.Scatter(
            x=np.array(market_returns)[order],
            y=np.array(fitted_returns)[order],
            mode="lines",
            name="CAPM Fit",
            line=dict(width=3),
        )
    )

    return _apply_base_layout(
        fig,
        title="Factor Exposure: Portfolio vs Market",
        xaxis_title="Market Return (SPY)",
        yaxis_title="Portfolio Return",
        height=420,
    )