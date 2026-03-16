import numpy as np

from src.simulation import simulate_gbm_paths, portfolio_returns_from_values
from src.risk_metrics import summarize_risk


def run_stress_scenarios(
    latest_prices,
    mu,
    sigma,
    weights,
    horizon_days,
    n_sims,
    confidence_level,
):
    scenarios = {
        "Baseline": {"mu_shift": 0.0, "sigma_mult": 1.0},
        "Market Crash": {"mu_shift": -0.20, "sigma_mult": 1.2},
        "High Volatility": {"mu_shift": 0.0, "sigma_mult": 1.8},
        "Bear Market": {"mu_shift": -0.10, "sigma_mult": 1.5},
    }

    results = []

    for scenario_name, params in scenarios.items():
        stressed_mu = mu + params["mu_shift"]
        stressed_sigma = sigma * params["sigma_mult"]

        _, stressed_portfolio_values = simulate_gbm_paths(
            initial_prices=latest_prices,
            mu=stressed_mu,
            sigma=stressed_sigma,
            weights=weights,
            n_days=horizon_days,
            n_sims=n_sims,
        )

        stressed_returns = portfolio_returns_from_values(stressed_portfolio_values)
        stressed_summary = summarize_risk(
            stressed_returns,
            confidence_level=confidence_level,
            portfolio_values=stressed_portfolio_values,
            years=horizon_days / 252,
        )

        results.append({
            "Scenario": scenario_name,
            "Expected Return": stressed_summary["expected_return"],
            "Volatility": stressed_summary["volatility"],
            "VaR": stressed_summary["var"],
            "CVaR": stressed_summary["cvar"],
        })

    return results