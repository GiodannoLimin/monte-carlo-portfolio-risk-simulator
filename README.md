# Monte Carlo Portfolio Risk Simulator

An interactive financial dashboard that explores possible portfolio outcomes using Monte Carlo simulation, Geometric Brownian Motion (GBM), and risk metrics such as Value at Risk (VaR) and Conditional Value at Risk (CVaR).

The simulator generates thousands of potential market scenarios to help visualize how a portfolio might perform across different investment horizons.

--------------------------------------------------

FEATURES

• Monte Carlo simulation of portfolio price paths  
• Geometric Brownian Motion asset modeling  
• Interactive portfolio allocation with customizable weights  
• Risk metrics including Expected Return, Volatility, VaR, and CVaR  
• Investment outcome projections with optional monthly contributions  
• Distribution of possible portfolio outcomes across different time horizons  
• Interactive financial charts built with Plotly  
• Beginner-friendly Learn tab explaining financial concepts  
• Theory section describing the mathematical models behind the simulator

--------------------------------------------------

DASHBOARD OVERVIEW

The dashboard allows users to:

• Select assets using real market data  
• Adjust portfolio weights  
• Choose simulation parameters  
• Explore risk metrics  
• Project potential investment outcomes  

Monte Carlo simulation generates many possible future price paths, allowing users to visualize both typical outcomes and extreme scenarios.

--------------------------------------------------

MATHEMATICAL MODEL

The simulator models asset prices using Geometric Brownian Motion (GBM).

dS_t = μ S_t dt + σ S_t dW_t

Future prices are simulated using the discrete-time update:

S_{t+1} = S_t exp((μ − 0.5σ²)Δt + σ√Δt Z_t)

where

μ = drift (expected return)  
σ = volatility  
Z_t ~ N(0,1)

Thousands of simulated paths are generated to estimate the distribution of portfolio outcomes.

--------------------------------------------------

TECH STACK

Python  
Streamlit  
NumPy  
Pandas  
Plotly  
yfinance  

--------------------------------------------------

INSTALLATION

Clone the repository

git clone https://github.com/GiodannoLimin/monte-carlo-portfolio-risk-simulator.git

Move into the project folder

cd monte-carlo-portfolio-risk-simulator

Install dependencies

pip install -r requirements.txt

Run the application

streamlit run app.py

--------------------------------------------------

PROJECT STRUCTURE

src/

simulation.py        Monte Carlo simulation engine  
risk_metrics.py      Risk metric calculations  
projections.py       Investment outcome projections  
plotting.py          Chart generation  
data_source.py       Market data download  
preprocessing.py     Data preparation  

tabs/

dashboard_tab.py  
explorer_tab.py  
learn_tab.py  
theory_tab.py  

ui_text.py           Educational explanations  
theory.py            Mathematical theory behind the model  

--------------------------------------------------

DISCLAIMER

This simulator is intended for educational purposes only.

It uses simplified financial models and historical data to explore possible scenarios. The results do not guarantee future performance and should not be considered financial advice.

--------------------------------------------------