GUIDE_SECTIONS = [
    {
        "id": "quick-start",
        "title": "Quick Start: How to Use This Simulator",
        "level": "beginner",
        "body": """
This simulator helps you explore how a portfolio might behave under many possible future scenarios.

A practical workflow:
1. Choose the assets you want in the portfolio.
2. Set portfolio weights.
3. Choose simulation settings such as time horizon and number of paths.
4. Review the outputs:
   - simulated portfolio paths
   - return distribution
   - terminal value distribution
   - risk metrics
   - optimization results
   - historical backtesting
   - factor analysis
   - stress testing
   - investment projections

This app does not predict one exact future.
Instead, it builds many possible futures under a statistical model so you can study ranges, risks, and trade-offs.
        """,
    },
    {
        "id": "what-this-app-does",
        "title": "What This App Does",
        "level": "beginner",
        "body": """
This dashboard combines several portfolio analytics tools in one place:

- Monte Carlo simulation for future portfolio scenarios
- risk analysis using volatility, VaR, and CVaR
- portfolio optimization and efficient frontier analysis
- backtesting against historical data
- benchmark comparison
- CAPM-style market factor analysis
- stress testing under adverse assumptions
- long-term investment outcome projection

The goal is not only to compute numbers, but to help users understand what those numbers mean.
        """,
    },
    {
        "id": "glossary",
        "title": "Glossary",
        "level": "beginner",
        "body": """
Portfolio:
A collection of assets held together as one investment.

Weight:
The proportion of the portfolio allocated to a particular asset.

Return:
The percentage gain or loss over a period.

Expected Return:
The model-based average return across scenarios.

Volatility:
A measure of how much returns fluctuate.

Covariance:
A measure of how two assets move together.

Correlation:
A standardized version of co-movement between assets.

Monte Carlo Simulation:
A method that generates many random future scenarios.

Benchmark:
A reference portfolio or market index used for comparison, such as SPY.

VaR (Value at Risk):
A lower-tail threshold for losses.

CVaR (Conditional Value at Risk):
The average loss in the worst tail beyond VaR.

Sharpe Ratio:
A measure of return relative to risk.

Beta:
Sensitivity of a portfolio to market movements.

Alpha:
Return not explained by market exposure alone.

R²:
The fraction of portfolio return variation explained by the factor model.

Terminal Value:
The ending portfolio value at the end of the simulation horizon.

Efficient Frontier:
A set of portfolios representing attractive return-risk combinations under the model.
        """,
    },
    {
        "id": "portfolio-basics",
        "title": "Portfolio Basics",
        "level": "beginner",
        "body": """
A portfolio is a weighted combination of assets such as stocks or ETFs.

Example:
- 50% SPY
- 30% QQQ
- 20% NVDA

Portfolio behavior depends on:
- the expected return of each asset
- the volatility of each asset
- the correlation structure across assets
- the weights chosen by the investor

A strong portfolio is not simply a list of good assets.
It is a design problem: how assets are combined matters just as much as which assets are selected.
        """,
    },
    {
        "id": "risk-return",
        "title": "Risk and Return",
        "level": "beginner",
        "body": """
In investing, return and risk must be analyzed together.

Return tells you how much a portfolio may grow.
Risk tells you how uncertain, unstable, or fragile that growth may be.

Two portfolios can have similar average returns but very different downside behavior.

Example:
- Portfolio A may grow more steadily with smaller drawdowns.
- Portfolio B may have higher upside but much deeper losses in weak scenarios.

This simulator helps visualize both:
- upside potential
- downside tail risk
- uncertainty of final outcomes
        """,
    },
    {
        "id": "why-monte-carlo",
        "title": "Why Monte Carlo Simulation Is Useful",
        "level": "beginner",
        "body": """
A single forecast is often misleading because markets are uncertain.

Monte Carlo simulation addresses this by generating many possible future paths instead of only one path.

This helps answer questions such as:
- What is the range of plausible outcomes?
- How often do poor outcomes occur?
- How severe are bad outcomes?
- How uncertain is final wealth?

This is especially useful in portfolio analysis because investors do not only care about the average case.
They also care about tail risk, dispersion, and robustness.
        """,
    },
    {
        "id": "plain-english-simulation",
        "title": "How the Simulation Works in Plain English",
        "level": "beginner",
        "body": """
At a high level, the app works like this:

1. It downloads historical price data.
2. It converts prices into returns.
3. It estimates statistical inputs such as expected return, volatility, and covariance.
4. It generates many random future asset paths.
5. It combines those simulated asset paths using your chosen portfolio weights.
6. It summarizes the simulated outcomes using charts and metrics.

Important:
This process is model-based.
It is useful for scenario exploration, learning, and structured risk analysis.
It is not a guarantee of future performance.
        """,
    },
    {
        "id": "chart-paths",
        "title": "How to Read the Simulated Portfolio Paths Chart",
        "level": "beginner",
        "body": """
This chart shows many possible portfolio trajectories over time.

How to interpret it:
- each line represents one simulated future
- a narrow cloud suggests more stable outcomes
- a wide cloud suggests more uncertainty
- downward paths reveal possible drawdown scenarios
- upward paths illustrate upside potential

What to look for:
- the overall spread of paths
- whether severe downside scenarios appear
- whether growth appears steady or highly unstable
- whether uncertainty widens quickly as the horizon increases
        """,
    },
    {
        "id": "chart-return-dist",
        "title": "How to Read the Return Distribution",
        "level": "beginner",
        "body": """
The return distribution summarizes simulated portfolio returns.

It helps you see:
- the center of likely outcomes
- the spread of outcomes
- the downside tail
- the upside tail

Interpretation:
- a distribution shifted to the right suggests stronger expected performance
- a wider distribution suggests more uncertainty
- a heavy left tail suggests larger downside risk
- an asymmetric distribution may indicate uneven upside versus downside behavior
        """,
    },
    {
        "id": "chart-terminal",
        "title": "How to Read the Terminal Value Distribution",
        "level": "beginner",
        "body": """
The terminal value distribution focuses on ending wealth.

This is important because many investors care more about:
- what their portfolio may be worth at the end
- how bad poor endings may be
- how wide the gap is between weak and strong scenarios

Interpretation:
- the middle mass shows typical outcomes
- the left tail shows poor endings
- the right tail shows strong upside scenarios
- a wide distribution means final wealth is highly uncertain
        """,
    },
    {
        "id": "metrics-core",
        "title": "Understanding Expected Return and Volatility",
        "level": "intermediate",
        "body": r"""
Two of the most fundamental portfolio statistics are expected return and volatility.

Expected return:
$$
\mathbb{E}[R_p] = w^\top \mu
$$

Volatility:
$$
\sigma_p = \sqrt{w^\top \Sigma w}
$$

where:
- $w$ is the portfolio weight vector
- $\mu$ is the expected return vector
- $\Sigma$ is the covariance matrix

Interpretation:
- higher expected return suggests stronger average modeled growth
- higher volatility means outcomes fluctuate more and are less predictable

A portfolio should not be judged by return alone.
The return-risk trade-off is central.
        """,
    },
    {
        "id": "var-cvar",
        "title": "Understanding VaR and CVaR",
        "level": "intermediate",
        "body": r"""
Value at Risk (VaR) measures a downside threshold.

For return $R$ and confidence level $\alpha$:
$$
\mathrm{VaR}_{\alpha}(R) = Q_{1-\alpha}(R)
$$

Example:
If 95% VaR is -3%, then only about 5% of simulated outcomes are worse than -3%.

Conditional Value at Risk (CVaR) goes further:
$$
\mathrm{CVaR}_{\alpha}(R) = \mathbb{E}[R \mid R \le \mathrm{VaR}_{\alpha}(R)]
$$

Interpretation:
- VaR gives the cutoff for bad outcomes
- CVaR gives the average severity once you are already in that bad tail

CVaR is often more informative because it captures tail depth, not only the threshold.
        """,
    },
    {
        "id": "portfolio-construction",
        "title": "Portfolio Construction Mathematics",
        "level": "technical",
        "body": r"""
Let the portfolio weights be:
$$
w = (w_1, w_2, \dots, w_n)
$$

For a fully invested portfolio:
$$
\sum_{i=1}^{n} w_i = 1
$$

Portfolio return:
$$
R_p = \sum_{i=1}^{n} w_i R_i
$$

Expected portfolio return:
$$
\mathbb{E}[R_p] = w^\top \mu
$$

Portfolio variance:
$$
\mathrm{Var}(R_p) = w^\top \Sigma w
$$

These formulas form the mathematical foundation of portfolio analysis in the app.

Key insight:
Even if two assets are risky individually, combining them can reduce overall portfolio risk if their movements are not perfectly aligned.
        """,
    },
    {
        "id": "gbm-foundation",
        "title": "Geometric Brownian Motion (GBM) Foundation",
        "level": "technical",
        "body": r"""
The simulator models asset prices using Geometric Brownian Motion (GBM):

$$
dS_t = \mu S_t \, dt + \sigma S_t \, dW_t
$$

where:
- $S_t$ is asset price at time $t$
- $\mu$ is drift
- $\sigma$ is volatility
- $W_t$ is Brownian motion

A common discrete-time simulation form is:
$$
S_{t+\Delta t} = S_t \exp\left[
\left(\mu - \frac{1}{2}\sigma^2\right)\Delta t
+ \sigma \sqrt{\Delta t} Z
\right]
$$

where:
- $\Delta t$ is the time step
- $Z \sim N(0,1)$

Why GBM is commonly used:
- it keeps prices positive
- it is mathematically tractable
- it scales well for simulation
- it is a standard baseline model in finance

Why it is imperfect:
- it assumes constant parameters
- it may understate extreme events
- it does not capture all real market dynamics
        """,
    },
    {
        "id": "parameter-estimation",
        "title": "Parameter Estimation",
        "level": "technical",
        "body": r"""
The simulator estimates model inputs from historical return data.

Typical estimated quantities:
- expected return vector $\mu$
- volatility
- covariance matrix $\Sigma$

These estimates drive:
- simulation
- portfolio risk metrics
- optimization
- projection outputs

Important caution:
Historical estimates are noisy.
Future market behavior may differ from the past.

This means the app should be interpreted as:
- a structured approximation
- a decision-support tool
- a learning framework

not as a certainty engine.
        """,
    },
    {
        "id": "mc-logic",
        "title": "Monte Carlo Engine Logic",
        "level": "technical",
        "body": r"""
Monte Carlo simulation generates many random future scenarios.

For each simulation path, the engine:
1. draws random shocks
2. propagates asset prices forward using the model
3. computes portfolio values using the selected weights
4. records path-level and terminal outcomes

If there are $M$ simulated paths, the output is an empirical distribution across those $M$ scenarios.

This allows the app to estimate:
- expected return
- volatility
- quantiles
- VaR and CVaR
- terminal wealth percentiles
- projection outcomes under repeated contributions

The power of Monte Carlo lies in studying the distribution of outcomes, not only a single expected value.
        """,
    },
    {
        "id": "optimization",
        "title": "Portfolio Optimization",
        "level": "intermediate",
        "body": r"""
Portfolio optimization studies how different allocations change the return-risk trade-off.

The app highlights common candidate portfolios such as:
- current portfolio
- maximum Sharpe portfolio
- minimum volatility portfolio

Sharpe ratio:
$$
\mathrm{Sharpe} = \frac{\mathbb{E}[R_p] - R_f}{\sigma_p}
$$

where:
- $\mathbb{E}[R_p]$ is expected portfolio return
- $R_f$ is the risk-free rate
- $\sigma_p$ is portfolio volatility

Interpretation:
- higher Sharpe suggests stronger risk-adjusted return
- minimum volatility focuses on stability
- your current portfolio may or may not be efficient relative to alternatives

Optimization does not reveal one universally correct portfolio.
It reveals how assumptions and allocations shape the opportunity set.
        """,
    },
    {
        "id": "efficient-frontier",
        "title": "How to Read the Efficient Frontier",
        "level": "intermediate",
        "body": r"""
The efficient frontier is the set of portfolios that offer:
- the highest expected return for a given volatility, or
- the lowest volatility for a given expected return

The app approximates this by generating many candidate portfolios and plotting:
- x-axis: volatility
- y-axis: expected return

Highlighted portfolios often include:
- Current Portfolio
- Max Sharpe Portfolio
- Min Volatility Portfolio

Interpretation:
- points further left are lower risk
- points higher up are higher return
- points below attractive alternatives may be inefficient under the model assumptions

The frontier helps users compare design choices rather than focusing only on one allocation.
        """,
    },
    {
        "id": "backtesting",
        "title": "Historical Backtesting",
        "level": "intermediate",
        "body": r"""
Backtesting applies the chosen portfolio weights to realized historical returns.

This helps answer:
- how the portfolio would have behaved historically
- whether it outperformed or underperformed a benchmark
- whether historical performance was smooth or volatile

A common cumulative growth representation is:
$$
V_t = \prod_{s=1}^{t} (1 + R_s)
$$

where $R_s$ is the portfolio return in period $s$.

Backtesting is useful because it adds historical context.
But it must not be confused with future certainty.
A strategy that looked strong historically may still perform poorly going forward.
        """,
    },
    {
        "id": "benchmarking",
        "title": "Benchmark Comparison",
        "level": "beginner",
        "body": """
A benchmark provides context for performance.

A portfolio gaining 8% may sound good in isolation.
But if a simple benchmark gained 15% with similar or lower risk, the result looks less impressive.

Common reasons to compare against a benchmark:
- evaluate active choices fairly
- determine whether complexity added value
- understand if performance is mostly just market exposure

A broad-market ETF such as SPY is often used as a reference benchmark.
        """,
    },
    {
        "id": "factor-analysis",
        "title": "CAPM / Market Factor Analysis",
        "level": "technical",
        "body": r"""
A simple market factor model is:
$$
R_p - R_f = \alpha + \beta (R_m - R_f) + \varepsilon
$$

where:
- $R_p$ is portfolio return
- $R_m$ is market return
- $R_f$ is risk-free rate
- $\alpha$ is alpha
- $\beta$ is beta
- $\varepsilon$ is the residual component

Interpretation:
- $\beta$ measures market sensitivity
- $\alpha$ measures return not explained by market exposure alone
- $R^2$ measures how much of return variation is explained by the model

This helps distinguish between:
- market-driven behavior
- portfolio-specific behavior
        """,
    },
    {
        "id": "capm-scatter",
        "title": "How to Read the CAPM Scatter Plot",
        "level": "intermediate",
        "body": """
Each point in the CAPM scatter plot represents one observation period.

Axes:
- x-axis: market return
- y-axis: portfolio return

The fitted line summarizes the average relationship.

Interpretation:
- steeper slope means higher beta
- tighter clustering around the line means higher R²
- wider scatter means more idiosyncratic behavior
- a positive intercept suggests positive alpha under the fitted model

This chart helps users understand whether the portfolio behaves mostly like the market or has distinct return dynamics.
        """,
    },
    {
        "id": "stress-testing",
        "title": "Stress Testing",
        "level": "intermediate",
        "body": """
Stress testing asks how the portfolio behaves under adverse assumptions.

Examples:
- lower expected returns
- higher volatility
- market shock scenarios
- crash-style drawdowns
- worse-than-normal environments

Why it matters:
A portfolio can appear strong in normal conditions but fail badly under stress.

Stress testing helps reveal:
- fragility
- downside sensitivity
- robustness
- concentration risk
- dependence on favorable assumptions
        """,
    },
    {
        "id": "investment-projections",
        "title": "Investment Outcome Projections",
        "level": "beginner",
        "body": """
This section translates portfolio return assumptions into practical long-term investing outcomes.

Typical inputs:
- initial investment
- monthly contribution
- time horizon

Typical outputs:
- median final value
- mean final value
- pessimistic outcomes
- optimistic outcomes
- range of plausible final wealth

This makes the app more practical because investors often care about future wealth paths, not just abstract return distributions.
        """,
    },
    {
        "id": "projection-interpretation",
        "title": "How to Interpret Projection Results",
        "level": "beginner",
        "body": """
Median Final Value:
The middle outcome. Half of simulations end above it and half below it.

Mean Final Value:
The average outcome. This can be pulled upward by a relatively small number of strong scenarios.

5th Percentile:
A pessimistic threshold representing weak outcomes.

95th Percentile:
An optimistic threshold representing strong outcomes.

Best practice:
- use the median as a practical central case
- use low percentiles for risk planning
- use high percentiles to understand upside potential
        """,
    },
    {
        "id": "common-mistakes",
        "title": "Common Portfolio Analysis Mistakes",
        "level": "beginner",
        "body": """
Common mistakes include:
- focusing only on expected return
- ignoring downside tail risk
- treating historical averages as certainty
- overtrusting optimization output
- ignoring benchmark comparison
- forgetting concentration risk
- assuming a smooth chart means low real-world risk
- confusing model output with financial advice

A better habit is to combine:
- simulation
- risk metrics
- historical context
- stress testing
- judgment
        """,
    },
    {
        "id": "limitations",
        "title": "Model Assumptions and Limitations",
        "level": "technical",
        "body": """
Important limitations of this framework include:

- GBM assumes constant drift and volatility
- correlations may change over time
- historical estimates can be unstable
- regime shifts are difficult to capture
- extreme events may be more severe than modeled
- transaction costs may be ignored
- taxes may be ignored
- rebalancing rules may not be fully modeled
- future market structure may differ from the estimation window

Therefore, the simulator should be used as:
- a learning tool
- a scenario engine
- a structured approximation

It should not be interpreted as certainty or personal financial advice.
        """,
    },
    {
        "id": "faq",
        "title": "FAQ",
        "level": "beginner",
        "body": """
Q: Does this app predict the future exactly?
A: No. It generates many possible futures under model assumptions.

Q: Why do results change from run to run?
A: Because random simulation is part of Monte Carlo analysis.

Q: Is higher expected return always better?
A: No. Risk, dispersion, and tail behavior also matter.

Q: Why compare with SPY?
A: It provides market context.

Q: Should I trust the max-Sharpe portfolio automatically?
A: No. Optimization depends heavily on estimated inputs and assumptions.

Q: Why are VaR and CVaR useful?
A: They summarize downside threshold and tail severity.

Q: Does strong backtest performance guarantee future success?
A: No. Historical evidence is informative, but never a guarantee.

Q: Why can terminal wealth vary so much?
A: Because compounding magnifies differences over time, especially under volatility.
        """,
    },
]