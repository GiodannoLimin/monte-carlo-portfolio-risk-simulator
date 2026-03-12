# Monte Carlo Portfolio Risk Simulator

An interactive finance dashboard that uses historical stock data and Monte Carlo simulation to explore possible future portfolio outcomes.

## Features

- Portfolio weight controls for AAPL, MSFT, NVDA, and SPY
- Monte Carlo simulation using Geometric Brownian Motion
- Risk metrics: expected return, volatility, VaR, and CVaR
- Historical stock explorer
- Multi-horizon investment scenario analysis
- Optional recurring monthly contribution
- Beginner-friendly Learn page
- Mathematical Theory page

## Methods

The project estimates drift and volatility from historical daily returns and uses a Geometric Brownian Motion model to simulate future price paths.

Key concepts:
- Daily returns
- Drift and volatility estimation
- Geometric Brownian Motion
- Value at Risk (VaR)
- Expected Shortfall (CVaR)

## Important Disclaimer

This project is for educational purposes only.

It simulates possible outcomes under simplifying assumptions and does not provide guaranteed forecasts or professional financial advice.

## Run locally

```bash
pip install -r requirements.txt
python -m streamlit run app.py