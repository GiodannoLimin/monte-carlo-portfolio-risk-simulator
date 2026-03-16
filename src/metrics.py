import numpy as np

def sharpe_ratio(returns):
    return np.mean(returns) / np.std(returns)

def max_drawdown(values):
    peak = np.maximum.accumulate(values)
    drawdown = (values - peak) / peak
    return drawdown.min()