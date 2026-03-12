import numpy as np
import pandas as pd

from src.simulation import (
    simulate_gbm_paths,
    portfolio_returns_from_values,
    simulate_portfolio_growth,
)


def build_projection_df(
    latest_prices,
    mu,
    sigma,
    weights,
    initial_investment,
    monthly_contribution,
) -> pd.DataFrame:
    horizon_map = {
        "0.5 years": 126,
        "1 year": 252,
        "1.5 years": 378,
        "2 years": 504,
        "2.5 years": 630,
        "3 years": 756,
    }

    projection_rows = []

    for label, days in horizon_map.items():
        _, proj_values = simulate_gbm_paths(
            initial_prices=latest_prices,
            mu=mu,
            sigma=sigma,
            weights=weights,
            n_days=days,
            n_sims=4000,
        )
        proj_returns = portfolio_returns_from_values(proj_values)

        years = days / 252
        growth_result = simulate_portfolio_growth(
            initial_investment=initial_investment,
            monthly_contribution=monthly_contribution,
            portfolio_returns=proj_returns,
            years=years,
        )

        final_values = growth_result["final_values"]
        total_contributions = growth_result["total_contributions"]
        pnl = growth_result["pnl"]

        projection_rows.append({
            "Horizon": label,
            "Total Contributions": round(float(total_contributions), 2),
            "Median Final Value": round(float(np.median(final_values)), 2),
            "Mean Final Value": round(float(np.mean(final_values)), 2),
            "5th Percentile Value": round(float(np.percentile(final_values, 5)), 2),
            "95th Percentile Value": round(float(np.percentile(final_values, 95)), 2),
            "Median Profit/Loss": round(float(np.median(pnl)), 2),
            "5th Percentile Profit/Loss": round(float(np.percentile(pnl, 5)), 2),
            "95th Percentile Profit/Loss": round(float(np.percentile(pnl, 95)), 2),
        })

    return pd.DataFrame(projection_rows)