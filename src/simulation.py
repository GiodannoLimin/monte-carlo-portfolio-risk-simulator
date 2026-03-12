import numpy as np
import pandas as pd


def estimate_parameters(returns_df: pd.DataFrame):
    asset_cols = [col for col in returns_df.columns if col != "Date"]

    mu = returns_df[asset_cols].mean().values
    sigma = returns_df[asset_cols].std().values

    return mu, sigma, asset_cols


def simulate_gbm_paths(
    initial_prices: np.ndarray,
    mu: np.ndarray,
    sigma: np.ndarray,
    weights: np.ndarray,
    n_days: int = 252,
    n_sims: int = 10000,
    dt: float = 1 / 252,
    seed: int = 42
):
    np.random.seed(seed)

    n_assets = len(initial_prices)
    simulated_prices = np.zeros((n_days + 1, n_sims, n_assets))
    simulated_prices[0] = initial_prices

    for t in range(1, n_days + 1):
        z = np.random.normal(size=(n_sims, n_assets))
        growth = (mu - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * z
        simulated_prices[t] = simulated_prices[t - 1] * np.exp(growth)

    portfolio_values = np.sum(simulated_prices * weights, axis=2)
    return simulated_prices, portfolio_values


def portfolio_returns_from_values(portfolio_values: np.ndarray) -> np.ndarray:
    initial_values = portfolio_values[0]
    final_values = portfolio_values[-1]
    returns = (final_values - initial_values) / initial_values
    return returns


def simulate_portfolio_growth(
    initial_investment: float,
    monthly_contribution: float,
    portfolio_returns: np.ndarray,
    years: float
):
    """
    Uses the simulated final portfolio returns over the full chosen horizon.
    We apply the same total simulated return to the initial investment and
    approximate recurring contributions as being invested evenly through time.
    """

    years = float(years)
    n_months = int(round(years * 12))

    initial_future_values = initial_investment * (1 + portfolio_returns)

    if monthly_contribution > 0 and n_months > 0:
        # Approximation: average contribution is invested for half the horizon.
        half_horizon_growth = np.power(1 + portfolio_returns, 0.5)
        contribution_future_values = monthly_contribution * n_months * half_horizon_growth
    else:
        contribution_future_values = 0.0

    total_future_values = initial_future_values + contribution_future_values
    total_contributions = initial_investment + monthly_contribution * n_months
    pnl = total_future_values - total_contributions

    return {
        "final_values": total_future_values,
        "total_contributions": total_contributions,
        "pnl": pnl,
    }