import numpy as np
import pandas as pd


def compute_portfolio_returns(returns_df: pd.DataFrame, asset_cols, weights: np.ndarray) -> np.ndarray:
    return returns_df[asset_cols].values @ weights


def compute_capm_stats(portfolio_returns: np.ndarray, market_returns: np.ndarray) -> dict:
    x = np.asarray(market_returns)
    y = np.asarray(portfolio_returns)

    if len(x) != len(y):
        n = min(len(x), len(y))
        x = x[:n]
        y = y[:n]

    x_mean = np.mean(x)
    y_mean = np.mean(y)

    cov_xy = np.mean((x - x_mean) * (y - y_mean))
    var_x = np.mean((x - x_mean) ** 2)

    beta = cov_xy / var_x if var_x != 0 else 0.0
    alpha_daily = y_mean - beta * x_mean

    y_hat = alpha_daily + beta * x
    ss_res = np.sum((y - y_hat) ** 2)
    ss_tot = np.sum((y - y_mean) ** 2)
    r_squared = 1 - ss_res / ss_tot if ss_tot != 0 else 0.0

    alpha_annual = alpha_daily * 252

    return {
        "alpha_annual": float(alpha_annual),
        "beta": float(beta),
        "r_squared": float(r_squared),
        "market_returns": x,
        "portfolio_returns": y,
        "fitted_returns": y_hat,
    }