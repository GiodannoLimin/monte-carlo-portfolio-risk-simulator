import numpy as np


def compute_var(returns: np.ndarray, confidence_level: float = 0.95) -> float:
    percentile = (1 - confidence_level) * 100
    return np.percentile(returns, percentile)


def compute_cvar(returns: np.ndarray, confidence_level: float = 0.95) -> float:
    var = compute_var(returns, confidence_level)
    tail_losses = returns[returns <= var]
    return tail_losses.mean() if len(tail_losses) > 0 else var


def summarize_risk(returns: np.ndarray, confidence_level: float = 0.95) -> dict:
    return {
        "expected_return": float(np.mean(returns)),
        "volatility": float(np.std(returns)),
        "var": float(compute_var(returns, confidence_level)),
        "cvar": float(compute_cvar(returns, confidence_level)),
        "median_return": float(np.median(returns)),
        "p5": float(np.percentile(returns, 5)),
        "p95": float(np.percentile(returns, 95)),
    }


def summarize_final_values(final_values: np.ndarray) -> dict:
    return {
        "mean_final_value": float(np.mean(final_values)),
        "median_final_value": float(np.median(final_values)),
        "p5_final_value": float(np.percentile(final_values, 5)),
        "p95_final_value": float(np.percentile(final_values, 95)),
    }