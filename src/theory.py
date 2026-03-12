THEORY_TEXT = """
## Mathematical Theory

This simulator combines **historical market data**, **Geometric Brownian Motion (GBM)**,
and **Monte Carlo simulation** to explore possible portfolio outcomes.

It answers two main questions:

1. How might the portfolio behave over the selected horizon?
2. What could happen to a specific investment amount if those simulated returns occur?

---

## 1. Historical Return Estimation

The simulator downloads historical adjusted closing prices for the selected assets.

From prices $P_t$, daily returns are computed as:

$$
r_t = \\frac{P_t}{P_{t-1}} - 1
$$

Using these returns, the simulator estimates:

- **drift ($\\mu$)** — average return  
- **volatility ($\\sigma$)** — standard deviation of returns  

These quantities are used as inputs for the simulation model.

---

## 2. Geometric Brownian Motion (GBM)

Each asset price is modeled using **Geometric Brownian Motion**.

In continuous time:

$$
dS_t = \\mu S_t dt + \\sigma S_t dW_t
$$

where:

- $S_t$ = asset price at time $t$
- $\\mu$ = drift parameter
- $\\sigma$ = volatility parameter
- $W_t$ = standard Brownian motion

This model assumes that proportional price changes are random and that prices remain positive.

---

## 3. Discrete-Time Simulation Formula

Because the app simulates daily paths numerically, it uses the discrete-time GBM update:

$$
S_{t+1} =
S_t \\exp\\left[
(\\mu - \\frac{1}{2}\\sigma^2)\\Delta t
+ \\sigma \\sqrt{\\Delta t} Z_t
\\right]
$$

where:

- $\\Delta t$ is one trading-day step
- $Z_t \\sim N(0,1)$ is a standard normal random variable

This formula is applied repeatedly across the selected horizon to generate simulated price paths.

---

## 4. Monte Carlo Simulation

Monte Carlo simulation generates **many random future scenarios** instead of one forecast.

If the app runs $N$ simulations, it creates $N$ possible portfolio paths.

These simulated paths allow us to estimate:

- average outcomes
- downside risk
- upside potential
- the distribution of possible returns

---

## 5. Portfolio Construction

Suppose the portfolio contains $k$ assets with weights

$$
w_1, w_2, \\dots, w_k
$$

such that

$$
\\sum_{i=1}^{k} w_i = 1
$$

Portfolio return can be written as:

$$
R_p = \\sum_{i=1}^{k} w_i R_i
$$

where:

- $R_p$ = portfolio return  
- $R_i$ = return of asset $i$  
- $w_i$ = portfolio weight of asset $i$

This allows the simulator to combine simulated asset returns into a portfolio result.

---

## 6. Portfolio Risk Metrics

After simulating many portfolio outcomes, the app summarizes the return distribution.

### Expected Return

The mean of simulated portfolio returns:

$$
E[R_p]
$$

### Volatility

The standard deviation of returns:

$$
Vol(R_p) = \\sqrt{Var(R_p)}
$$

### Value at Risk (VaR)

At confidence level $c$, VaR is the lower-tail cutoff of the simulated return distribution.

For example, a **95% VaR** focuses on the worst $5\\%$ of outcomes.

### Conditional Value at Risk (CVaR)

CVaR is the **average loss beyond the VaR threshold**.

It measures the expected loss in the worst tail of the distribution.

---

## 7. Investment Outcome Projection

The portfolio simulation produces return scenarios in percentage terms.

The app then applies those simulated returns to a user-defined investment plan:

- initial investment
- recurring monthly contribution
- selected time horizon

This produces a distribution of **possible final investment values**.

From that distribution we compute:

- median final value
- mean final value
- 5th percentile value
- 95th percentile value
- median profit/loss

---

## 8. Why 252 Trading Days?

Financial models usually use **trading days** rather than calendar days.

A year is approximated as:

$$
252 \\text{ trading days}
$$

So:

- $0.5$ years $\\approx 126$ days
- $1$ year $\\approx 252$ days
- $2$ years $\\approx 504$ days
- $3$ years $\\approx 756$ days

This keeps the simulation consistent with the daily historical return data.

---

## 9. Model Assumptions

This simulator relies on several simplifying assumptions:

1. historical return patterns are informative about the future
2. drift and volatility remain approximately stable
3. asset prices follow GBM dynamics
4. shocks are modeled using normally distributed randomness
5. regime changes and macro events are not explicitly modeled

These assumptions make the model useful for **learning and scenario analysis**, but they also limit realism.

---

## 10. Limitations

Real markets may differ from this model because:

- volatility changes over time
- returns may not follow a normal distribution
- extreme events occur more often than GBM suggests
- asset correlations can shift
- major news and structural breaks are not captured

Therefore the simulator should be interpreted as **a model of possible scenarios**, not a guaranteed forecast.

---

## 11. Interpretation

This app should be viewed as a tool for:

- understanding uncertainty
- exploring portfolio risk
- comparing allocation choices
- visualizing possible investment outcomes

It is **not financial advice** and should not be used as the sole basis for investment decisions.
"""