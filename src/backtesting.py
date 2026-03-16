import numpy as np
import pandas as pd


def compute_historical_portfolio_series(returns_df: pd.DataFrame, asset_cols, weights: np.ndarray) -> np.ndarray:
    asset_returns = returns_df[asset_cols].values
    return asset_returns @ weights


def compute_backtest_growth(returns: np.ndarray, initial_value: float = 1.0) -> np.ndarray:
    return initial_value * np.cumprod(1 + returns)


def compute_backtest_summary(returns: np.ndarray) -> dict:
    growth = compute_backtest_growth(returns)

    annual_return = float(np.mean(returns) * 252)
    annual_volatility = float(np.std(returns) * np.sqrt(252))

    if annual_volatility == 0:
        sharpe_ratio = 0.0
    else:
        sharpe_ratio = annual_return / annual_volatility

    running_max = np.maximum.accumulate(growth)
    drawdown = (growth - running_max) / running_max
    max_drawdown = float(np.min(drawdown))

    total_return = float(growth[-1] - 1)

    return {
        "total_return": total_return,
        "annual_return": annual_return,
        "annual_volatility": annual_volatility,
        "sharpe_ratio": sharpe_ratio,
        "max_drawdown": max_drawdown,
        "growth": growth,
    }