THEORY_TEXT = r"""
## Theory and Method

### 1. Daily Returns

We compute daily simple returns using

$$
r_t = \frac{P_t - P_{t-1}}{P_{t-1}}
$$

where $P_t$ is the asset price at time $t$.

---

### 2. Parameter Estimation

For each asset, we estimate:

- **drift ($\mu$)**: average historical return  
- **volatility ($\sigma$)**: standard deviation of historical returns

$$
\mu = \text{mean}(r_t)
$$

$$
\sigma = \text{std}(r_t)
$$

---

### 3. Geometric Brownian Motion

The stock price follows the stochastic differential equation

$$
dS_t = \mu S_t dt + \sigma S_t dW_t
$$

where

- $S_t$ = asset price  
- $\mu$ = drift  
- $\sigma$ = volatility  
- $W_t$ = Brownian motion  

---

### 4. Discrete Simulation Formula

For Monte Carlo simulation we use

$$
S_{t+1} = S_t \exp\left((\mu - \frac{1}{2}\sigma^2)\Delta t + \sigma\sqrt{\Delta t}Z\right)
$$

where

- $Z \sim N(0,1)$
- $\Delta t$ is the time step

---

### 5. Value at Risk (VaR)

At confidence level $\alpha$,

$$
VaR_\alpha = \text{quantile}_{1-\alpha}(R)
$$

This is a downside threshold from the simulated return distribution.

---

### 6. Expected Shortfall (CVaR)

$$
CVaR = E[R \mid R \le VaR]
$$

This measures the average return in the worst tail of the distribution.

---

### 7. Important Limitations

This project is based on simplifying assumptions:

- historical drift and volatility are informative
- volatility is approximately constant
- returns are driven by Gaussian shocks
- market crashes and structural changes are not modeled directly

So the output should be interpreted as a **scenario simulation**, not certainty.
"""