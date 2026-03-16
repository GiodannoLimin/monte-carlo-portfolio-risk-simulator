import numpy as np


def compute_var(returns: np.ndarray, confidence_level: float = 0.95) -> float:
    percentile = (1 - confidence_level) * 100
    return np.percentile(returns, percentile)


def compute_cvar(returns: np.ndarray, confidence_level: float = 0.95) -> float:
    var = compute_var(returns, confidence_level)
    tail_losses = returns[returns <= var]
    return tail_losses.mean() if len(tail_losses) > 0 else var


def compute_sharpe_ratio(returns: np.ndarray, risk_free_rate: float = 0.02, years: float = 1.0) -> float:
    if len(returns) == 0:
        return 0.0

    horizon_rf = (1 + risk_free_rate) ** years - 1
    excess_returns = returns - horizon_rf
    volatility = np.std(returns)

    if volatility == 0:
        return 0.0

    return float(np.mean(excess_returns) / volatility)


def compute_max_drawdown(portfolio_values: np.ndarray) -> float:
    if portfolio_values.ndim == 1:
        running_max = np.maximum.accumulate(portfolio_values)
        drawdowns = (portfolio_values - running_max) / running_max
        return float(np.min(drawdowns))

    # if shape is (time, sims), use median path across simulations
    median_path = np.median(portfolio_values, axis=1)
    running_max = np.maximum.accumulate(median_path)
    drawdowns = (median_path - running_max) / running_max
    return float(np.min(drawdowns))


def summarize_risk(
    returns: np.ndarray,
    confidence_level: float = 0.95,
    portfolio_values: np.ndarray | None = None,
    risk_free_rate: float = 0.02,
    years: float = 1.0,
) -> dict:
    summary = {
        "expected_return": float(np.mean(returns)),
        "volatility": float(np.std(returns)),
        "var": float(compute_var(returns, confidence_level)),
        "cvar": float(compute_cvar(returns, confidence_level)),
        "median_return": float(np.median(returns)),
        "p5": float(np.percentile(returns, 5)),
        "p95": float(np.percentile(returns, 95)),
        "sharpe_ratio": float(compute_sharpe_ratio(returns, risk_free_rate, years)),
        "sortino_ratio": float(compute_sortino_ratio(returns, risk_free_rate, years)),
    }

    if portfolio_values is not None:
        summary["max_drawdown"] = float(compute_max_drawdown(portfolio_values))
    else:
        summary["max_drawdown"] = 0.0

    return summary


def summarize_final_values(final_values: np.ndarray) -> dict:
    return {
        "mean_final_value": float(np.mean(final_values)),
        "median_final_value": float(np.median(final_values)),
        "p5_final_value": float(np.percentile(final_values, 5)),
        "p95_final_value": float(np.percentile(final_values, 95)),
    }
def compute_sortino_ratio(returns: np.ndarray, risk_free_rate: float = 0.02, years: float = 1.0) -> float:
    if len(returns) == 0:
        return 0.0

    horizon_rf = (1 + risk_free_rate) ** years - 1
    excess_returns = returns - horizon_rf

    downside_returns = excess_returns[excess_returns < 0]
    if len(downside_returns) == 0:
        return 0.0

    downside_std = np.std(downside_returns)
    if downside_std == 0:
        return 0.0

    return float(np.mean(excess_returns) / downside_std)