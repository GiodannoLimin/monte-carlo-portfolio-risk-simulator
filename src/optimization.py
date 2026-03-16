import numpy as np
import pandas as pd


def compute_portfolio_return(weights: np.ndarray, mean_returns: np.ndarray) -> float:
    return float(np.dot(weights, mean_returns))


def compute_portfolio_volatility(weights: np.ndarray, cov_matrix: np.ndarray) -> float:
    return float(np.sqrt(weights.T @ cov_matrix @ weights))


def compute_portfolio_sharpe(
    weights: np.ndarray,
    mean_returns: np.ndarray,
    cov_matrix: np.ndarray,
    risk_free_rate: float = 0.02,
) -> float:
    port_return = compute_portfolio_return(weights, mean_returns)
    port_vol = compute_portfolio_volatility(weights, cov_matrix)

    if port_vol == 0:
        return 0.0

    return float((port_return - risk_free_rate) / port_vol)


def generate_random_portfolios(
    returns_df: pd.DataFrame,
    asset_cols,
    n_portfolios: int = 3000,
    risk_free_rate: float = 0.02,
    seed: int = 42,
):
    np.random.seed(seed)

    asset_returns = returns_df[asset_cols]
    mean_returns = asset_returns.mean().values * 252
    cov_matrix = asset_returns.cov().values * 252

    results = []
    weights_list = []

    n_assets = len(asset_cols)

    for _ in range(n_portfolios):
        weights = np.random.random(n_assets)
        weights = weights / weights.sum()

        port_return = compute_portfolio_return(weights, mean_returns)
        port_vol = compute_portfolio_volatility(weights, cov_matrix)
        sharpe = compute_portfolio_sharpe(weights, mean_returns, cov_matrix, risk_free_rate)

        results.append((port_return, port_vol, sharpe))
        weights_list.append(weights)

    results = np.array(results)

    return {
        "returns": results[:, 0],
        "volatilities": results[:, 1],
        "sharpes": results[:, 2],
        "weights": weights_list,
        "mean_returns": mean_returns,
        "cov_matrix": cov_matrix,
    }


def get_max_sharpe_portfolio(frontier_data):
    idx = int(np.argmax(frontier_data["sharpes"]))
    return {
        "return": float(frontier_data["returns"][idx]),
        "volatility": float(frontier_data["volatilities"][idx]),
        "sharpe": float(frontier_data["sharpes"][idx]),
        "weights": frontier_data["weights"][idx],
    }


def get_min_vol_portfolio(frontier_data):
    idx = int(np.argmin(frontier_data["volatilities"]))
    return {
        "return": float(frontier_data["returns"][idx]),
        "volatility": float(frontier_data["volatilities"][idx]),
        "sharpe": float(frontier_data["sharpes"][idx]),
        "weights": frontier_data["weights"][idx],
    }