LEARN_CONTENT = [
    {
        "title": "1. What does this simulator do?",
        "body": """
This app explores **possible future outcomes** for a portfolio of stocks or ETFs.

Instead of giving one fixed prediction, it simulates **many possible future scenarios**
based on historical return patterns.

This helps you understand:

- how a portfolio might grow or decline
- the range of possible outcomes
- downside risk and upside potential
- how results change across different investment horizons
        """
    },
    {
        "title": "2. What is Monte Carlo simulation?",
        "body": """
Monte Carlo simulation is a method for modeling **uncertainty**.

Rather than assuming there is only one future path, the app generates many random
possible paths for the portfolio.

For example, if the app runs 8,000 simulations, it creates 8,000 different
possible market scenarios.

By studying all of them together, we can estimate typical, bad, and good outcomes.
        """
    },
    {
        "title": "3. What do portfolio weights mean?",
        "body": """
Portfolio weight is how much of your portfolio is allocated to each asset.

Example:
- 40% AAPL
- 30% MSFT
- 20% NVDA
- 10% SPY

If one asset has a larger weight, it has a larger influence on the portfolio result.

In this app, raw weights are normalized automatically so they always sum to 100%.
        """
    },
    {
        "title": "4. Why are there many lines in the simulation chart?",
        "body": """
Each line represents **one possible future path** for the portfolio.

Some paths may rise steadily.
Some may fluctuate.
Some may decline.

The chart is not trying to show the exact future.
It is showing the **range of plausible outcomes** under the model.
        """
    },
    {
        "title": "5. What are Expected Return and Volatility?",
        "body": """
**Expected Return** is the average simulated portfolio return over the selected horizon.

**Volatility** measures how much portfolio returns tend to fluctuate.

In simple terms:
- higher expected return means higher average growth
- higher volatility means more uncertainty and larger swings
        """
    },
    {
        "title": "6. What is VaR?",
        "body": """
VaR stands for **Value at Risk**.

It is a downside threshold from the simulated return distribution.

Example:
if VaR = -1.5% at 95% confidence, then about 5% of simulated outcomes
are worse than -1.5%.

VaR helps summarize downside risk in one number.
        """
    },
    {
        "title": "7. What is CVaR?",
        "body": """
CVaR stands for **Conditional Value at Risk**.

While VaR gives a cutoff point, CVaR looks at what happens **beyond** that cutoff.

It measures the **average loss in the worst tail of outcomes**.

So:
- VaR tells you where the bad tail begins
- CVaR tells you how bad the worst cases are on average
        """
    },
    {
        "title": "8. Why are portfolio risk and investment outcomes separated?",
        "body": """
Because they answer different questions.

- **Portfolio Risk Simulation** studies how the modeled portfolio behaves in percentage terms.
- **Investment Outcome Projection** applies those simulated returns to your own money settings.

This separation makes the dashboard easier to interpret.

A portfolio can have a certain return distribution, while your own final dollar outcome
also depends on:
- your initial investment
- your monthly contributions
- your chosen investment horizon
        """
    },
    {
        "title": "9. Why does the simulator use 252 days per year?",
        "body": """
Financial models usually use **trading days**, not calendar days.

Markets are open about **252 trading days per year** after excluding weekends
and holidays.

Because this simulator works with **daily returns**, the time horizon must also
be measured in trading days.

Examples:
- 0.5 years ≈ 126 trading days
- 1 year ≈ 252 trading days
- 2 years ≈ 504 trading days
- 3 years ≈ 756 trading days
        """
    },
    {
        "title": "10. Is this predicting the future?",
        "body": """
No.

This tool is better understood as **scenario analysis**, not guaranteed prediction.

It uses historical data and mathematical assumptions to explore what *could* happen,
not what *will* happen.

Real markets can behave differently because of:
- economic shocks
- policy changes
- company news
- changing market regimes
        """
    },
]