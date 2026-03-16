# Monte Carlo Portfolio Risk Simulator

An interactive portfolio analytics dashboard built with Python and Streamlit for exploring portfolio risk, return, and long-term investment outcomes.

This project combines Monte Carlo simulation, Geometric Brownian Motion (GBM), portfolio optimization, historical backtesting, benchmark comparison, CAPM-style factor analysis, stress testing, and an integrated finance handbook with HTML preview and LaTeX PDF export.

--------------------------------------------------

FEATURES

• Monte Carlo simulation of portfolio paths
• Geometric Brownian Motion asset modeling
• Custom portfolio construction with adjustable weights
• Risk metrics including:
  - expected return
  - volatility
  - Value at Risk (VaR)
  - Conditional Value at Risk (CVaR)
• Efficient frontier and portfolio optimization
• Historical backtesting
• Benchmark comparison
• CAPM / market factor analysis
• Stress testing under adverse scenarios
• Long-term investment projections with monthly contributions
• Stock Explorer for individual asset analysis
• Interactive financial charts built with Plotly
• Integrated education handbook:
  - interactive HTML preview inside the app
  - downloadable HTML handbook
  - professional LaTeX-based PDF export

--------------------------------------------------

DASHBOARD OVERVIEW

The application allows users to:

• select assets using real market data
• adjust portfolio weights
• configure simulation settings
• analyze simulated portfolio outcomes
• compare portfolio performance historically
• evaluate benchmark-relative behavior
• inspect factor exposure and CAPM statistics
• stress test assumptions
• project long-term investment outcomes
• learn the financial theory behind the analytics

The goal is not only to compute numbers, but to help users interpret them.

--------------------------------------------------

MATHEMATICAL FOUNDATION

The simulator models asset prices using Geometric Brownian Motion (GBM):

dS_t = μ S_t dt + σ S_t dW_t

A common discrete-time simulation form is:

S_{t+Δt} = S_t exp[(μ − 0.5σ²)Δt + σ√Δt Z]

where:

μ = drift
σ = volatility
Z ~ N(0,1)

Portfolio analytics are also based on standard portfolio theory, including:

E[R_p] = w^T μ

σ_p = sqrt(w^T Σ w)

The simulator generates many possible future scenarios to estimate the distribution of portfolio outcomes rather than relying on a single forecast.

--------------------------------------------------

TECH STACK

Python
Streamlit
NumPy
Pandas
Plotly
yfinance
LaTeX / TinyTeX for PDF handbook export

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

Optional: PDF Handbook Export

To enable LaTeX PDF export for the handbook, install a LaTeX distribution such as:

• TinyTeX
• TeX Live
• MiKTeX

The app uses LaTeX to generate a cleaner math-heavy PDF handbook.

--------------------------------------------------

PROJECT STRUCTURE

app.py

src/
    app_text.py
    backtesting.py
    config.py
    data_source.py
    factor_analysis.py
    optimization.py
    plotting.py
    preprocessing.py
    risk_metrics.py
    sidebar.py
    simulation.py
    stress_testing.py
    styles.py

    tabs/
        dashboard_tab.py
        explorer_tab.py
        learn_tab.py

    education/
        __init__.py
        pdf_export.py
        report_builder.py
        report_charts.py
        report_latex.py
        report_sections.py
        report_styles.py
        report_utils.py

--------------------------------------------------

EDUCATIONAL HANDBOOK

A built-in handbook explains the simulator from both beginner and technical perspectives.

It includes topics such as:

• portfolio basics
• risk and return
• Monte Carlo intuition
• reading charts and distributions
• VaR and CVaR
• GBM foundations
• portfolio optimization
• backtesting
• CAPM analysis
• stress testing
• model limitations

The handbook can be:

• previewed inside the app
• downloaded as HTML
• exported as a professionally formatted PDF via LaTeX

--------------------------------------------------

DISCLAIMER

This simulator is intended for educational and analytical purposes only.

It uses simplified financial models and historical data to explore possible scenarios. Results do not guarantee future performance and should not be interpreted as financial advice.