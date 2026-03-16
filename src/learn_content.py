LEARN_CONTENT = [
    {
        "title": "Quick Start: How to Use This Simulator",
        "body": """
This app helps you explore how a portfolio might behave under many possible future scenarios.

A simple workflow:
1. Choose the assets you want in the portfolio.
2. Set portfolio weights for each asset.
3. Choose simulation settings such as horizon and number of paths.
4. Review the dashboard outputs:
   - simulated portfolio paths
   - return distribution
   - terminal value distribution
   - risk metrics
   - optimization results
   - backtesting
   - stress testing
   - investment outcome projections

This simulator does not predict the exact future.
Instead, it generates many possible futures using a statistical model.
        """,
    },
    {
        "title": "Glossary",
        "body": """
Portfolio:
A collection of assets held together as one investment.

Weight:
The fraction of your portfolio allocated to an asset.
For example, a 40% weight in AAPL means 40% of your capital is invested in AAPL.

Return:
The percentage gain or loss of an investment over a period.

Volatility:
A measure of how much returns fluctuate.
Higher volatility means more uncertainty.

Monte Carlo Simulation:
A method that generates many random future scenarios to study possible outcomes.

Benchmark:
A reference portfolio or market index used for comparison, such as SPY.

VaR (Value at Risk):
A downside threshold. For example, a daily 95% VaR of -2% means the portfolio is expected to lose more than 2% only about 5% of the time.

CVaR (Conditional Value at Risk):
The average loss in the worst cases beyond VaR.

Sharpe Ratio:
A measure of return relative to risk. Higher is generally better.

Beta:
How sensitive the portfolio is to market movements.

Alpha:
Return unexplained by market exposure alone.

R²:
How much of portfolio return variation is explained by the market in the factor model.
        """,
    },
    {
        "title": "Portfolio Basics",
        "body": """
A portfolio is a mix of assets such as stocks or ETFs.

The key idea is allocation:
how much you place into each asset.

Example:
- 50% SPY
- 30% QQQ
- 20% NVDA

Portfolio performance depends on:
- the return of each asset
- the weight assigned to each asset
- how the assets move together

A portfolio is not just about picking good assets.
It is also about combining them in a way that balances growth and risk.
        """,
    },
    {
        "title": "Risk and Return",
        "body": """
In investing, higher expected return usually comes with higher risk.

Return tells you how much you may gain.
Risk tells you how uncertain or unstable the outcome may be.

Two portfolios can have the same average return but very different risk.

Example:
- Portfolio A: stable but slower growth
- Portfolio B: higher growth potential but larger losses in bad scenarios

This app helps visualize both sides:
- upside opportunity
- downside risk
        """,
    },
    {
        "title": "What Monte Carlo Simulation Does",
        "body": """
Monte Carlo simulation creates many possible future paths for asset prices.

Instead of assuming one future outcome, the model generates thousands of random scenarios.

Why this is useful:
- real markets are uncertain
- a single forecast is often misleading
- distributions of outcomes are more informative than one number

In this app, each line in the simulation chart is one possible future path.

Looking at many paths helps answer questions like:
- How wide is the range of outcomes?
- How bad could losses be?
- How strong could growth be?
- How often do extreme outcomes happen?
        """,
    },
    {
        "title": "How the Simulation Works in Plain English",
        "body": """
The model estimates return and volatility from historical data.

Then it uses those estimates to generate random future asset movements.

Those simulated asset paths are combined using your portfolio weights.

From that, the app computes:
- simulated portfolio value paths
- simulated portfolio returns
- risk metrics
- possible final investment outcomes

Important:
This is a model, not reality.
It is useful for exploration, scenario analysis, and intuition building.
        """,
    },
    {
        "title": "How to Read the Simulated Portfolio Paths Chart",
        "body": """
This chart shows many possible future portfolio trajectories.

How to interpret it:
- each line = one simulated future path
- the wider the spread, the greater the uncertainty
- if most paths trend upward, the portfolio has positive expected growth under the model
- if paths spread very widely, outcomes are less predictable

What to look for:
- whether paths are tightly grouped or highly dispersed
- whether some paths show severe drawdowns
- whether growth is steady or highly unstable
        """,
    },
    {
        "title": "How to Read the Return Distribution",
        "body": """
This chart shows the distribution of simulated returns.

It helps you see:
- the center of likely outcomes
- the spread of outcomes
- the downside tail
- the upside tail

Interpretation:
- a distribution shifted to the right suggests higher expected return
- a wider distribution suggests higher uncertainty
- a heavier left tail suggests more severe downside risk
        """,
    },
    {
        "title": "How to Read the Terminal Value Distribution",
        "body": """
This chart shows the range of possible ending portfolio values after the simulation horizon.

It is useful because investors often care about final wealth, not just period-by-period returns.

Interpretation:
- the middle of the distribution shows typical ending outcomes
- the left side shows poor outcomes
- the right side shows strong outcomes
- a very wide distribution means final wealth is highly uncertain
        """,
    },
    {
        "title": "Understanding Expected Return and Volatility",
        "body": """
Expected Return:
The average simulated return across scenarios.

Volatility:
The degree of fluctuation in returns.

Together they summarize the basic trade-off:
- higher expected return can be attractive
- higher volatility means more uncertainty

A good portfolio is not necessarily the one with the highest return.
It may be the one with a more attractive balance of return and risk.
        """,
    },
    {
        "title": "Understanding VaR and CVaR",
        "body": """
VaR measures a downside threshold.

Example:
If 95% VaR is -3%, that means only about 5% of simulated outcomes are worse than -3%.

CVaR goes further.
It asks:
when things are already in the worst tail, how bad are they on average?

So:
- VaR = threshold
- CVaR = average severity beyond that threshold

CVaR is often more informative because it captures the magnitude of tail losses.
        """,
    },
    {
        "title": "Portfolio Optimization",
        "body": """
Portfolio optimization helps identify allocations that improve the trade-off between return and risk.

This app visualizes an efficient frontier based on many candidate portfolios.

Common highlighted portfolios:
- current portfolio
- maximum Sharpe portfolio
- minimum volatility portfolio

Maximum Sharpe portfolio:
Seeks the highest return per unit of risk.

Minimum volatility portfolio:
Seeks the lowest overall volatility.

Optimization does not tell you the one perfect portfolio.
It shows how portfolio design affects the risk-return balance.
        """,
    },
    {
        "title": "How to Read the Efficient Frontier",
        "body": """
The efficient frontier shows how expected return changes with volatility across different portfolios.

Interpretation:
- each point is a portfolio
- points further left have lower volatility
- points higher up have higher expected return

Important highlighted points:
- Current Portfolio: your chosen allocation
- Max Sharpe: strong risk-adjusted candidate
- Min Vol: lowest-volatility candidate

If your current portfolio lies far below good alternatives, it may be inefficient under the model assumptions.
        """,
    },
    {
        "title": "Historical Backtesting",
        "body": """
Backtesting compares how the portfolio would have performed historically.

This app compares your portfolio with:
- a benchmark like SPY
- an equal-weight portfolio

The growth-of-$1 chart is especially useful.

Example:
If one line ends at 1.80, then $1 became $1.80 over the backtest window.

Backtesting helps answer:
- did the portfolio historically outperform or underperform?
- was the ride smooth or volatile?
- how does the strategy compare with a simple benchmark?
        """,
    },
    {
        "title": "Benchmark Comparison",
        "body": """
A benchmark gives context.

A portfolio gaining 8% may sound good, but not if the benchmark gained 15% with similar risk.

Common reasons to compare against a benchmark:
- judge performance fairly
- understand whether active choices added value
- see whether complexity is worth it

SPY is often used as a broad market benchmark.
        """,
    },
    {
        "title": "Factor Analysis (CAPM)",
        "body": """
Factor analysis studies how portfolio returns relate to market returns.

In the CAPM view, three common outputs are:

Beta:
How strongly the portfolio tends to move with the market.
- beta > 1: moves more than the market
- beta < 1: moves less than the market

Alpha:
Return not explained by market exposure alone.
Positive alpha suggests performance above what beta alone would predict.

R²:
How much of the portfolio's return variation is explained by the market.

The scatter plot helps visualize this relationship.
        """,
    },
    {
        "title": "How to Read the CAPM Scatter Plot",
        "body": """
Each point represents one time period of:
- market return on the x-axis
- portfolio return on the y-axis

The fitted line summarizes the relationship.

Interpretation:
- steeper slope = higher beta
- points tightly clustered around the line = higher R²
- points far from the line = more idiosyncratic variation

This chart helps you understand whether the portfolio behaves like the market or has distinct behavior.
        """,
    },
    {
        "title": "Stress Testing",
        "body": """
Stress testing asks:
what happens under bad or unusual market conditions?

Examples:
- market crash
- high-volatility environment
- lower expected returns

Why this matters:
A portfolio can look strong in normal simulations but fail badly in stressed scenarios.

Stress testing helps reveal:
- fragility
- downside sensitivity
- robustness under adverse conditions
        """,
    },
    {
        "title": "Investment Outcome Projection",
        "body": """
This section translates simulated returns into a personal investing plan.

Inputs usually include:
- initial investment
- monthly contribution
- time horizon

Outputs help answer:
- what final value is typical?
- what happens in weaker scenarios?
- what happens in stronger scenarios?

This makes the simulation more practical because users care about long-term wealth outcomes, not just abstract returns.
        """,
    },
    {
        "title": "How to Interpret Projection Results",
        "body": """
Median Final Value:
The middle outcome. Half of simulations end above it, half below.

Mean Final Value:
The average outcome. This can be pulled upward by strong best-case scenarios.

5th Percentile:
A pessimistic outcome threshold.

95th Percentile:
An optimistic outcome threshold.

Use these together:
- median for a typical case
- 5th percentile for downside planning
- 95th percentile for upside potential
        """,
    },
    {
        "title": "Model Limitations",
        "body": """
This simulator is useful, but it has limitations.

Important limitations:
- Geometric Brownian Motion assumes constant drift and volatility
- real markets can change regimes
- extreme events may be more severe than the model implies
- transaction costs are usually ignored
- taxes are ignored
- rebalancing may not be modeled
- future parameters may differ from the past

So the simulator should be used as a decision-support and learning tool, not as a guarantee.
        """,
    },
    {
        "title": "FAQ",
        "body": """
Q: Does this app predict the future exactly?
A: No. It generates many possible futures under model assumptions.

Q: Is a higher return always better?
A: Not necessarily. Risk matters too.

Q: Why compare with SPY?
A: It provides market context for evaluating performance.

Q: Why do simulated results change?
A: Because randomness is part of Monte Carlo simulation.

Q: Should I trust only the optimization result?
A: No. Optimization depends on assumptions and estimated inputs.

Q: Why are VaR and CVaR important?
A: They help quantify downside and tail risk.

Q: Can historical performance guarantee future performance?
A: No. Backtesting is informative, but not predictive certainty.
        """,
    },
]