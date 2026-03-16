import base64
from io import BytesIO

import matplotlib.pyplot as plt
import numpy as np


def _fig_to_base64(fig) -> str:
    buffer = BytesIO()
    fig.savefig(buffer, format="png", dpi=180, bbox_inches="tight", facecolor=fig.get_facecolor())
    buffer.seek(0)
    encoded = base64.b64encode(buffer.read()).decode("utf-8")
    plt.close(fig)
    return encoded


def _style_axis(ax) -> None:
    ax.set_facecolor("#0f1730")
    for spine in ax.spines.values():
        spine.set_color("#66708d")
    ax.tick_params(colors="#eaf0ff", labelsize=9)
    ax.xaxis.label.set_color("#eef3ff")
    ax.yaxis.label.set_color("#eef3ff")
    ax.title.set_color("#ffffff")
    ax.grid(True, alpha=0.18)


def generate_monte_carlo_chart_base64(seed: int = 42) -> str:
    rng = np.random.default_rng(seed)
    steps = 120
    n_paths = 35
    dt = 1 / 252
    mu = 0.10
    sigma = 0.22

    fig, ax = plt.subplots(figsize=(6.2, 4.2), facecolor="#0b1329")
    time = np.arange(steps + 1)

    for _ in range(n_paths):
        shocks = rng.normal(0, 1, steps)
        log_returns = (mu - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * shocks
        prices = 100 * np.exp(np.cumsum(np.insert(log_returns, 0, 0.0)))
        ax.plot(time, prices, alpha=0.55, linewidth=1.1)

    _style_axis(ax)
    ax.set_title("Illustrative Simulated Portfolio Paths", fontsize=12, weight="bold")
    ax.set_xlabel("Time Step")
    ax.set_ylabel("Portfolio Value Index")
    return _fig_to_base64(fig)


def generate_efficient_frontier_chart_base64(seed: int = 7) -> str:
    rng = np.random.default_rng(seed)
    n = 250
    vols = rng.uniform(0.08, 0.34, n)
    returns = 0.04 + 0.55 * vols - 0.55 * (vols - 0.18) ** 2 + rng.normal(0, 0.012, n)

    max_sharpe_idx = np.argmax((returns - 0.02) / vols)
    min_vol_idx = np.argmin(vols)
    current_idx = 80

    fig, ax = plt.subplots(figsize=(6.2, 4.2), facecolor="#0b1329")
    ax.scatter(vols, returns, alpha=0.65, s=28)
    ax.scatter(vols[max_sharpe_idx], returns[max_sharpe_idx], s=90, marker="*", label="Max Sharpe")
    ax.scatter(vols[min_vol_idx], returns[min_vol_idx], s=70, marker="s", label="Min Vol")
    ax.scatter(vols[current_idx], returns[current_idx], s=70, marker="D", label="Current")

    frontier_idx = np.argsort(vols)
    ax.plot(np.sort(vols), returns[frontier_idx], alpha=0.7, linewidth=1.2)

    _style_axis(ax)
    ax.set_title("Illustrative Efficient Frontier", fontsize=12, weight="bold")
    ax.set_xlabel("Volatility")
    ax.set_ylabel("Expected Return")
    legend = ax.legend(frameon=True)
    legend.get_frame().set_alpha(0.2)

    return _fig_to_base64(fig)


def generate_distribution_chart_base64(seed: int = 21) -> str:
    rng = np.random.default_rng(seed)
    data = rng.normal(0.08, 0.16, 3000)

    fig, ax = plt.subplots(figsize=(6.2, 4.2), facecolor="#0b1329")
    ax.hist(data, bins=40, alpha=0.85)
    ax.axvline(np.quantile(data, 0.05), linestyle="--", linewidth=1.5, label="5th percentile")
    ax.axvline(np.mean(data), linestyle="-", linewidth=1.5, label="Mean")

    _style_axis(ax)
    ax.set_title("Illustrative Return Distribution", fontsize=12, weight="bold")
    ax.set_xlabel("Simulated Return")
    ax.set_ylabel("Frequency")
    legend = ax.legend(frameon=True)
    legend.get_frame().set_alpha(0.2)

    return _fig_to_base64(fig)


def build_chart_payload() -> list[dict]:
    return [
        {
            "title": "Simulated Paths",
            "caption": "A stylized example of how many possible portfolio futures can diverge over time under Monte Carlo simulation.",
            "image_base64": generate_monte_carlo_chart_base64(),
        },
        {
            "title": "Efficient Frontier",
            "caption": "A conceptual risk-return map showing candidate portfolios and key highlighted allocations.",
            "image_base64": generate_efficient_frontier_chart_base64(),
        },
        {
            "title": "Return Distribution",
            "caption": "A stylized distribution view showing central tendency, dispersion, and downside thresholds.",
            "image_base64": generate_distribution_chart_base64(),
        },
    ]