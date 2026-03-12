LEARN_CONTENT = [
    {
        "title": "What do portfolio weights mean?",
        "body": """
Portfolio weight is how much of your portfolio is allocated to each stock.

Example:
- 40% AAPL
- 30% MSFT
- 20% NVDA
- 10% SPY
        """
    },
    {
        "title": "What are the many lines in the simulation chart?",
        "body": """
Each line represents one possible future path for the portfolio.

Because the future is uncertain, the model simulates many possible scenarios
instead of showing only one outcome.
        """
    },
    {
        "title": "What is VaR?",
        "body": """
VaR (Value at Risk) is a downside threshold from the simulated return distribution.

Example:
if VaR = -1.5% at 95% confidence, then about 5% of simulated outcomes
are worse than -1.5%.
        """
    },
    {
        "title": "What is CVaR?",
        "body": """
CVaR (Conditional Value at Risk) is the average loss in the worst cases
beyond the VaR cutoff.

It helps show how severe the bad outcomes are on average.
        """
    },
    {
        "title": "Why are portfolio risk and investment outcomes separated?",
        "body": """
Because they answer different questions.

- **Portfolio risk simulation** asks how the modeled portfolio behaves.
- **Investment outcome projection** asks what your own money could become if those simulated returns are applied to it.

Separating them makes the dashboard easier to understand.
        """
    },
    {
        "title": "Is this live prediction?",
        "body": """
Not exactly.

This app downloads recent historical market data and uses it to simulate
possible future scenarios.

So it is better understood as scenario analysis, not a guaranteed prediction.
        """
    },
    {
        "title": "Why does the simulator use 252 days per year?",
        "body": """
Financial models usually measure time using **trading days instead of calendar days**.

Stock markets are open about **252 days per year**, after removing weekends and holidays.

Because this simulator models **daily returns**, the investment horizon must be converted
from years into trading days.

Example:

- 0.5 years ≈ 126 trading days
- 1 year ≈ 252 trading days
- 2 years ≈ 504 trading days
- 3 years ≈ 756 trading days

Using trading days ensures the simulation is consistent with the **historical return data**
used to estimate volatility and expected returns.
        """
    },
]

DISCLAIMER_TEXT = """
This tool simulates possible outcomes based on historical data and mathematical assumptions.

It is **not professional financial advice** and does **not guarantee future performance**.

Important assumptions:
- historical drift and volatility are informative
- prices follow Geometric Brownian Motion
- volatility is treated as approximately constant
- real market shocks and regime changes may not be captured

Use this project for **education and exploration**, not as a sole basis for real investment decisions.
"""