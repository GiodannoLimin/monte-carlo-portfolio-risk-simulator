from __future__ import annotations

import base64
from html import escape
from io import BytesIO
import re

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from src.app_text import DISCLAIMER_TEXT


def build_education_html() -> str:
    sim_chart = _simulation_chart_base64()
    frontier_chart = _frontier_chart_base64()
    risk_chart = _risk_chart_base64()

    sections = [
        {
            "id": "overview",
            "eyebrow": "Platform Overview",
            "title": "What this simulator is designed to do",
            "lead": (
                "The Monte Carlo Portfolio Risk Simulator is a portfolio analytics dashboard "
                "built to help users explore uncertainty, understand downside risk, compare "
                "allocation choices, and interpret investment outcomes in a more disciplined way."
            ),
            "cards": [
                {
                    "title": "Simulation engine",
                    "body": (
                        "Projects many possible future portfolio paths instead of assuming one fixed outcome. "
                        "This helps users think in distributions, not single-point guesses."
                    ),
                },
                {
                    "title": "Risk analytics",
                    "body": (
                        "Summarizes volatility, drawdown intuition, Value at Risk, and tail-risk style metrics "
                        "so downside scenarios are easier to evaluate."
                    ),
                },
                {
                    "title": "Portfolio decision support",
                    "body": (
                        "Includes optimization, backtesting, factor-style thinking, stress analysis, "
                        "and projection tools to support better portfolio comparisons."
                    ),
                },
            ],
        },
        {
            "id": "monte-carlo",
            "eyebrow": "Core Idea",
            "title": "How Monte Carlo simulation works in finance",
            "lead": (
                "Monte Carlo simulation creates many plausible future scenarios for asset or portfolio values. "
                "Instead of trying to predict one exact future price, it asks what a wide range of reasonable futures might look like."
            ),
            "body": """
A traditional forecast often produces **one expected path**, but markets do not move that way in reality.

Monte Carlo methods generate **many possible paths** by repeatedly introducing random shocks into a model of returns.  
This is useful because investors care about:
- the range of possible outcomes
- the chance of loss
- the severity of bad scenarios
- the trade-off between upside and downside

In a simplified continuous-time setting, a common model is:

$$
dS_t = \mu S_t dt + \sigma S_t dW_t
$$

where:
- $S_t$ is the asset value
- $\mu$ is expected growth
- $\sigma$ is volatility
- $dW_t$ is a random shock term

This does **not** mean the simulator knows the future.  
It means the simulator creates a structured set of scenarios under a chosen model.
""",
        },
        {
            "id": "reading-charts",
            "eyebrow": "Chart Interpretation",
            "title": "How to read the main outputs",
            "lead": (
                "The dashboard becomes much more useful once the charts are read correctly. "
                "Each visualization answers a different portfolio question."
            ),
            "body": """
**Simulation paths** show many possible future portfolio trajectories.  
A wide fan of paths usually suggests higher uncertainty.

**Return distributions** summarize how outcomes are spread across good, average, and bad scenarios.

**Terminal value charts** focus on where the portfolio may end, rather than how it gets there.

**Efficient frontier views** compare expected return versus volatility across different portfolio weights.

When interpreting results, ask:
- Is the portfolio highly dispersed?
- How bad are the worst cases?
- Is the expected reward large enough relative to the risk taken?
- Does a different allocation improve the trade-off?
""",
        },
        {
            "id": "risk",
            "eyebrow": "Risk Concepts",
            "title": "The most important metrics in plain language",
            "lead": (
                "Good dashboards do not just show numbers. They help the user understand what those numbers mean for decisions."
            ),
            "body": """
**Volatility** measures how much returns fluctuate.  
Higher volatility usually means less predictable outcomes.

**Sharpe ratio** measures return per unit of risk.  
A higher Sharpe ratio generally indicates more efficient risk-taking.

**Value at Risk (VaR)** estimates a loss threshold over a chosen horizon and confidence level.  
For example, if one-day $VaR_{0.95} = -2.1\\%$, that means roughly the worst 5% of days are expected to be worse than -2.1%.

**Conditional Value at Risk (CVaR)** goes further by asking:  
once we are already in the bad tail, how severe are those losses on average?

A useful intuition is:
- VaR tells you **where the tail begins**
- CVaR tells you **how painful the tail is**
""",
        },
        {
            "id": "optimization",
            "eyebrow": "Allocation Logic",
            "title": "Why optimization matters",
            "lead": (
                "Portfolio construction is not just about picking strong assets. "
                "It is also about combining them intelligently."
            ),
            "body": """
Different weights can produce very different portfolio behavior, even when the same assets are used.

Optimization helps answer questions like:
- Which allocation gives the highest expected risk-adjusted return?
- Which allocation minimizes volatility?
- How much diversification benefit is actually present?

A common objective is to compare portfolios in the risk-return plane.

If expected return is written as $E[R_p]$ and volatility as $\\sigma_p$, one popular summary is:

$$
\\text{Sharpe Ratio} = \\frac{E[R_p] - R_f}{\\sigma_p}
$$

where $R_f$ is the risk-free rate.

In practice, optimization is helpful, but it should not be treated as perfect truth.  
Outputs depend on assumptions, input estimates, and the model itself.
""",
        },
        {
            "id": "stress-backtest",
            "eyebrow": "Robustness",
            "title": "Why stress testing and backtesting matter",
            "lead": (
                "A portfolio may look attractive under average assumptions but fragile under market stress. "
                "That is why robustness tools matter."
            ),
            "body": """
**Stress testing** asks what happens if conditions become unusually bad:
- a market shock
- a volatility spike
- a large drawdown
- a correlation jump across risky assets

**Backtesting** asks how a strategy or allocation would have behaved on historical data.

These tools do not guarantee future performance.  
However, they help reveal whether a portfolio is overly dependent on calm conditions.

A useful mindset is:
- simulation explores possible futures
- stress testing explores adverse futures
- backtesting inspects historical behavior
""",
        },
        {
            "id": "limitations",
            "eyebrow": "Decision Quality",
            "title": "What this tool can and cannot do",
            "lead": (
                "A strong finance tool is honest about model limitations. "
                "This makes the analysis more credible, not less."
            ),
            "body": """
This simulator is valuable for **education, scenario analysis, and portfolio comparison**.

It is not a machine that predicts exact future returns.

Important limitations include:
- parameter estimates may be unstable
- market regimes can change
- real returns may not follow simple model assumptions
- correlations may behave differently during crises
- optimization outputs can be sensitive to inputs

So the right use is not:
**\"the simulator told me exactly what will happen\"**

The right use is:
**\"the simulator helps me reason more carefully about uncertainty, risk, and allocation trade-offs\"**
""",
        },
    ]

    overview_html = _render_overview_section(sections[0])
    content_html = "".join(_render_content_section(section) for section in sections[1:])
    disclaimer_html = _render_markdownish_html(DISCLAIMER_TEXT)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Monte Carlo Portfolio Risk Simulator — Guide</title>

  <script>
    window.MathJax = {{
      tex: {{
        inlineMath: [['$', '$'], ['\\\\(', '\\\\)']],
        displayMath: [['$$', '$$'], ['\\\\[', '\\\\]']]
      }},
      svg: {{ fontCache: 'global' }}
    }};
  </script>
  <script defer src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js"></script>

  <style>
    :root {{
      --bg-1: #060816;
      --bg-2: #0d1433;
      --bg-3: #1e2155;
      --panel: rgba(255,255,255,0.08);
      --panel-strong: rgba(255,255,255,0.12);
      --border: rgba(255,255,255,0.14);
      --text: #f8fafc;
      --muted: #c9d2e3;
      --soft: #a9bad7;
      --brand: #8eb7ff;
      --brand-2: #c7d8ff;
      --accent: #9ee7d7;
      --warning-bg: rgba(255, 214, 102, 0.10);
      --warning-border: rgba(255, 214, 102, 0.30);
      --shadow: 0 18px 60px rgba(0,0,0,0.28);
      --radius-xl: 30px;
      --radius-lg: 22px;
      --radius-md: 16px;
      --maxw: 1120px;
    }}

    * {{
      box-sizing: border-box;
    }}

    html {{
      scroll-behavior: smooth;
    }}

    body {{
      margin: 0;
      color: var(--text);
      font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      line-height: 1.72;
      background:
        radial-gradient(circle at top left, rgba(80,120,255,0.22), transparent 30%),
        radial-gradient(circle at top right, rgba(0,210,255,0.10), transparent 28%),
        linear-gradient(135deg, var(--bg-1) 0%, var(--bg-2) 48%, var(--bg-3) 100%);
      min-height: 100vh;
    }}

    a {{
      color: var(--brand-2);
    }}

    .shell {{
      max-width: var(--maxw);
      margin: 0 auto;
      padding: 28px 22px 70px;
    }}

    .hero {{
      position: relative;
      overflow: hidden;
      border: 1px solid var(--border);
      background: linear-gradient(135deg, rgba(255,255,255,0.08), rgba(255,255,255,0.04));
      backdrop-filter: blur(14px);
      border-radius: var(--radius-xl);
      padding: 38px;
      box-shadow: var(--shadow);
    }}

    .hero::before {{
      content: "";
      position: absolute;
      inset: auto -80px -80px auto;
      width: 240px;
      height: 240px;
      background: radial-gradient(circle, rgba(142,183,255,0.18), transparent 68%);
      pointer-events: none;
    }}

    .badges {{
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      margin-bottom: 20px;
    }}

    .badge {{
      padding: 8px 12px;
      border-radius: 999px;
      font-size: 12px;
      font-weight: 700;
      letter-spacing: 0.04em;
      text-transform: uppercase;
      background: rgba(255,255,255,0.08);
      border: 1px solid rgba(255,255,255,0.14);
      color: #eaf2ff;
    }}

    .hero h1 {{
      margin: 0;
      font-size: 54px;
      line-height: 1.02;
      letter-spacing: -0.03em;
      max-width: 820px;
    }}

    .hero .subtitle {{
      margin-top: 16px;
      max-width: 820px;
      font-size: 18px;
      color: var(--muted);
    }}

    .hero-grid {{
      display: grid;
      grid-template-columns: 1.05fr 0.95fr;
      gap: 20px;
      margin-top: 28px;
      align-items: stretch;
    }}

    .glass-card {{
      background: var(--panel);
      border: 1px solid var(--border);
      border-radius: var(--radius-lg);
      padding: 22px;
    }}

    .glass-card h3 {{
      margin: 0 0 10px;
      font-size: 18px;
      color: #ffffff;
    }}

    .glass-card p {{
      margin: 0;
      color: var(--muted);
      font-size: 15px;
    }}

    .mini-grid {{
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 16px;
    }}

    .chart-card {{
      padding: 14px;
      border-radius: 20px;
      background: rgba(255,255,255,0.06);
      border: 1px solid var(--border);
    }}

    .chart-card img {{
      width: 100%;
      display: block;
      border-radius: 14px;
      background: white;
    }}

    .nav {{
      position: sticky;
      top: 0;
      z-index: 20;
      margin: 22px 0 28px;
      padding: 14px 18px;
      border: 1px solid var(--border);
      border-radius: 18px;
      backdrop-filter: blur(14px);
      background: rgba(8, 11, 24, 0.62);
      box-shadow: 0 10px 30px rgba(0,0,0,0.18);
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
    }}

    .nav a {{
      text-decoration: none;
      color: var(--brand-2);
      font-size: 14px;
      font-weight: 700;
      padding: 8px 12px;
      border-radius: 999px;
      background: rgba(255,255,255,0.06);
      border: 1px solid rgba(255,255,255,0.10);
    }}

    .overview {{
      margin-top: 26px;
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 18px;
    }}

    .overview-card {{
      background: var(--panel);
      border: 1px solid var(--border);
      border-radius: 22px;
      padding: 24px;
      box-shadow: 0 12px 34px rgba(0,0,0,0.14);
    }}

    .overview-card h3 {{
      margin: 0 0 10px;
      font-size: 20px;
      color: #fff;
    }}

    .overview-card p {{
      margin: 0;
      color: var(--muted);
      font-size: 15px;
    }}

    .section {{
      margin: 44px 0;
      padding: 30px;
      border: 1px solid var(--border);
      border-radius: 28px;
      background: linear-gradient(180deg, rgba(255,255,255,0.07), rgba(255,255,255,0.04));
      box-shadow: var(--shadow);
    }}

    .eyebrow {{
      display: inline-block;
      margin-bottom: 10px;
      font-size: 12px;
      font-weight: 800;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      color: var(--accent);
    }}

    .section h2 {{
      margin: 0;
      font-size: 38px;
      line-height: 1.1;
      letter-spacing: -0.025em;
    }}

    .lead {{
      margin-top: 12px;
      font-size: 17px;
      color: var(--muted);
      max-width: 900px;
    }}

    .content {{
      margin-top: 22px;
      font-size: 17px;
      color: #eef3ff;
    }}

    .content p {{
      margin: 0 0 14px;
    }}

    .content ul {{
      margin: 12px 0 18px 22px;
      padding: 0;
    }}

    .content li {{
      margin: 8px 0;
      color: #eef3ff;
    }}

    .formula {{
      margin: 18px 0;
      padding: 18px 20px;
      border-radius: 18px;
      border: 1px solid rgba(255,255,255,0.14);
      background: rgba(7, 14, 36, 0.52);
      overflow-x: auto;
    }}

    .formula-label {{
      display: block;
      margin-bottom: 8px;
      font-size: 12px;
      font-weight: 800;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      color: var(--soft);
    }}

    .highlight {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 18px;
      margin-top: 24px;
    }}

    .callout {{
      border-radius: 20px;
      padding: 20px;
      background: rgba(255,255,255,0.06);
      border: 1px solid var(--border);
    }}

    .callout strong {{
      color: white;
    }}

    .disclaimer {{
      background: var(--warning-bg);
      border: 1px solid var(--warning-border);
    }}

    .footer {{
      margin-top: 30px;
      color: var(--soft);
      font-size: 14px;
      text-align: center;
    }}

    code {{
      font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
      font-size: 0.95em;
      background: rgba(255,255,255,0.09);
      border: 1px solid rgba(255,255,255,0.12);
      border-radius: 8px;
      padding: 2px 6px;
      color: #fff;
    }}

    strong {{
      color: white;
    }}

    em {{
      color: #dfe9ff;
    }}

    @media (max-width: 940px) {{
      .hero h1 {{
        font-size: 42px;
      }}

      .hero-grid,
      .overview,
      .highlight {{
        grid-template-columns: 1fr;
      }}
    }}

    @media (max-width: 700px) {{
      .shell {{
        padding: 18px 14px 50px;
      }}

      .hero,
      .section {{
        padding: 22px;
      }}

      .section h2 {{
        font-size: 30px;
      }}

      .content {{
        font-size: 16px;
      }}
    }}

    @media print {{
      body {{
        background: white !important;
        color: #111827;
      }}

      .hero, .section, .overview-card, .glass-card, .nav {{
        background: white !important;
        color: #111827 !important;
        box-shadow: none !important;
        border: 1px solid #d1d5db !important;
        backdrop-filter: none !important;
      }}

      .subtitle, .lead, .overview-card p, .glass-card p, .content, .content li, .footer {{
        color: #374151 !important;
      }}

      .nav {{
        display: none;
      }}

      .topic, .section {{
        break-inside: avoid;
      }}

      code {{
        color: #111827 !important;
        background: #f3f4f6 !important;
        border-color: #e5e7eb !important;
      }}
    }}
  </style>
</head>
<body>
  <div class="shell">
    <header class="hero">
      <div class="badges">
        <span class="badge">Monte Carlo</span>
        <span class="badge">Portfolio Analytics</span>
        <span class="badge">Risk Education</span>
      </div>

      <h1>Monte Carlo Portfolio Risk Simulator</h1>
      <p class="subtitle">
        A polished guide to the ideas behind simulation, risk measurement, optimization,
        stress testing, and portfolio interpretation.
      </p>

      <div class="hero-grid">
        <div class="glass-card">
          <h3>What this report is for</h3>
          <p>
            This guide explains the dashboard as a finance product, not just a set of charts.
            It focuses on intuition, decision quality, and model interpretation.
          </p>

          <div class="mini-grid" style="margin-top: 16px;">
            <div class="chart-card">
              <img src="data:image/png;base64,{sim_chart}" alt="Illustrative simulation paths" />
            </div>
            <div class="chart-card">
              <img src="data:image/png;base64,{frontier_chart}" alt="Illustrative efficient frontier" />
            </div>
          </div>
        </div>

        <div class="glass-card">
          <h3>What the dashboard helps answer</h3>
          <p>
            What could happen to a portfolio? How risky is it? How bad can the downside become?
            Does a different allocation improve the risk-return trade-off?
          </p>

          <div class="chart-card" style="margin-top: 16px;">
            <img src="data:image/png;base64,{risk_chart}" alt="Illustrative risk distribution" />
          </div>
        </div>
      </div>
    </header>

    <nav class="nav">
      <a href="#overview">Overview</a>
      <a href="#monte-carlo">Simulation</a>
      <a href="#reading-charts">Chart Reading</a>
      <a href="#risk">Risk Metrics</a>
      <a href="#optimization">Optimization</a>
      <a href="#stress-backtest">Robustness</a>
      <a href="#limitations">Limitations</a>
      <a href="#disclaimer">Disclaimer</a>
    </nav>

    {overview_html}
    {content_html}

    <section class="section" id="disclaimer">
      <span class="eyebrow">Important Note</span>
      <h2>Disclaimer</h2>
      <p class="lead">
        This dashboard is best used for education, exploration, and portfolio reasoning.
      </p>
      <div class="content disclaimer" style="padding: 22px; border-radius: 20px; margin-top: 20px;">
        {disclaimer_html}
      </div>
    </section>

    <div class="footer">
      For the cleanest export, open the HTML in a browser and use Print → Save as PDF.
    </div>
  </div>
</body>
</html>
"""


def build_education_html_bytes() -> bytes:
    return build_education_html().encode("utf-8")


def _render_overview_section(section: dict) -> str:
    cards_html = "".join(
        f"""
        <article class="overview-card">
          <h3>{escape(card["title"])}</h3>
          <p>{escape(card["body"])}</p>
        </article>
        """
        for card in section["cards"]
    )

    return f"""
    <section class="section" id="{escape(section["id"])}">
      <span class="eyebrow">{escape(section["eyebrow"])}</span>
      <h2>{escape(section["title"])}</h2>
      <p class="lead">{escape(section["lead"])}</p>
      <div class="overview">
        {cards_html}
      </div>
    </section>
    """


def _render_content_section(section: dict) -> str:
    body_html = _render_markdownish_html(section["body"])

    extra = ""
    if section["id"] == "risk":
        extra = """
        <div class="highlight">
          <div class="callout">
            <strong>Decision use:</strong><br>
            VaR is useful for setting a downside threshold, while CVaR is more informative
            when the user wants to understand tail severity.
          </div>
          <div class="callout">
            <strong>Interpretation caution:</strong><br>
            A portfolio can have an acceptable average outcome and still contain a very
            uncomfortable tail. That is why distribution thinking matters.
          </div>
        </div>
        """

    return f"""
    <section class="section" id="{escape(section["id"])}">
      <span class="eyebrow">{escape(section["eyebrow"])}</span>
      <h2>{escape(section["title"])}</h2>
      <p class="lead">{escape(section["lead"])}</p>
      <div class="content">
        {body_html}
      </div>
      {extra}
    </section>
    """


def _render_markdownish_html(text: str) -> str:
    blocks = _parse_blocks(text)
    html_parts: list[str] = []

    for block_type, value in blocks:
        if block_type == "paragraph":
            html_parts.append(f"<p>{_format_inline_html(value)}</p>")
        elif block_type == "bullets":
            html_parts.append("<ul>")
            for item in value:
                html_parts.append(f"<li>{_format_inline_html(item)}</li>")
            html_parts.append("</ul>")
        elif block_type == "formula":
            html_parts.append(
                f"""
                <div class="formula">
                  <span class="formula-label">Formula</span>
                  $$ {value} $$
                </div>
                """
            )

    return "".join(html_parts)


def _parse_blocks(text: str) -> list[tuple[str, str | list[str]]]:
    lines = text.strip().splitlines()

    blocks: list[tuple[str, str | list[str]]] = []
    paragraph_lines: list[str] = []
    bullet_lines: list[str] = []
    formula_lines: list[str] = []
    in_formula = False

    def flush_paragraph() -> None:
        nonlocal paragraph_lines
        if paragraph_lines:
            paragraph = " ".join(line.strip() for line in paragraph_lines if line.strip())
            if paragraph:
                blocks.append(("paragraph", paragraph))
            paragraph_lines = []

    def flush_bullets() -> None:
        nonlocal bullet_lines
        if bullet_lines:
            blocks.append(("bullets", bullet_lines[:]))
            bullet_lines = []

    def flush_formula() -> None:
        nonlocal formula_lines
        if formula_lines:
            formula = "\n".join(formula_lines).strip()
            if formula:
                blocks.append(("formula", formula))
            formula_lines = []

    for raw in lines:
        stripped = raw.strip()

        if stripped == "$$":
            flush_paragraph()
            flush_bullets()
            if in_formula:
                flush_formula()
                in_formula = False
            else:
                in_formula = True
            continue

        if in_formula:
            formula_lines.append(raw.rstrip())
            continue

        if not stripped:
            flush_paragraph()
            flush_bullets()
            continue

        if stripped.startswith("- "):
            flush_paragraph()
            bullet_lines.append(stripped[2:].strip())
            continue

        flush_bullets()
        paragraph_lines.append(stripped)

    flush_paragraph()
    flush_bullets()
    flush_formula()

    return blocks


def _format_inline_html(text: str) -> str:
    token_pattern = re.compile(r"(\$\$.*?\$\$|\$.*?\$|\*\*.*?\*\*|\*.*?\*|`.*?`)")
    parts: list[str] = []
    pos = 0

    for match in token_pattern.finditer(text):
        start, end = match.span()

        if start > pos:
            parts.append(escape(text[pos:start]))

        token = match.group(0)

        if token.startswith("$$") and token.endswith("$$"):
            expr = token[2:-2].strip()
            parts.append(f"$${expr}$$")
        elif token.startswith("$") and token.endswith("$"):
            expr = token[1:-1].strip()
            parts.append(f"${expr}$")
        elif token.startswith("**") and token.endswith("**") and len(token) >= 4:
            parts.append(f"<strong>{escape(token[2:-2])}</strong>")
        elif token.startswith("*") and token.endswith("*") and len(token) >= 2:
            parts.append(f"<em>{escape(token[1:-1])}</em>")
        elif token.startswith("`") and token.endswith("`") and len(token) >= 2:
            parts.append(f"<code>{escape(token[1:-1])}</code>")
        else:
            parts.append(escape(token))

        pos = end

    if pos < len(text):
        parts.append(escape(text[pos:]))

    return "".join(parts)


def _simulation_chart_base64() -> str:
    np.random.seed(7)
    n_days = 140
    n_paths = 42
    dt = 1 / 252
    mu = 0.11
    sigma = 0.24

    fig, ax = plt.subplots(figsize=(6.8, 3.4), dpi=180)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")

    for _ in range(n_paths):
        shocks = np.random.normal(size=n_days)
        log_returns = (mu - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * shocks
        path = 100 * np.exp(np.cumsum(log_returns))
        ax.plot(path, linewidth=1.0, alpha=0.45)

    ax.set_title("Illustrative Monte Carlo Paths", fontsize=12, pad=10)
    ax.set_xlabel("Trading Days", fontsize=9)
    ax.set_ylabel("Portfolio Value", fontsize=9)
    ax.grid(alpha=0.22)
    ax.tick_params(labelsize=8)
    for spine in ax.spines.values():
        spine.set_alpha(0.25)

    return _fig_to_base64(fig)


def _frontier_chart_base64() -> str:
    np.random.seed(11)

    vols = np.linspace(0.08, 0.32, 140)
    frontier = 0.04 + 0.78 * vols - 0.62 * (vols - 0.20) ** 2

    scatter_x = np.random.uniform(0.08, 0.32, 160)
    scatter_y = (
        0.025
        + 0.66 * scatter_x
        - 0.95 * (scatter_x - 0.21) ** 2
        + np.random.normal(0, 0.009, 160)
    )

    fig, ax = plt.subplots(figsize=(6.8, 3.4), dpi=180)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")

    ax.scatter(scatter_x, scatter_y, s=14, alpha=0.38)
    ax.plot(vols, frontier, linewidth=2.0)
    ax.scatter([0.16], [0.12], s=46, marker="o", label="Current")
    ax.scatter([0.22], [0.18], s=58, marker="*", label="Max Sharpe")
    ax.scatter([0.10], [0.09], s=46, marker="s", label="Min Vol")

    ax.set_title("Illustrative Efficient Frontier", fontsize=12, pad=10)
    ax.set_xlabel("Volatility", fontsize=9)
    ax.set_ylabel("Expected Return", fontsize=9)
    ax.grid(alpha=0.22)
    ax.tick_params(labelsize=8)
    ax.legend(fontsize=7, frameon=False, loc="lower right")
    for spine in ax.spines.values():
        spine.set_alpha(0.25)

    return _fig_to_base64(fig)


def _risk_chart_base64() -> str:
    np.random.seed(23)
    samples = np.random.normal(loc=0.006, scale=0.028, size=6000)

    fig, ax = plt.subplots(figsize=(6.8, 3.4), dpi=180)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")

    ax.hist(samples, bins=45, alpha=0.80, density=True)
    var_95 = np.quantile(samples, 0.05)
    cvar_95 = samples[samples <= var_95].mean()

    ax.axvline(var_95, linestyle="--", linewidth=1.8, label="VaR 95%")
    ax.axvline(cvar_95, linestyle=":", linewidth=2.0, label="CVaR 95%")

    ax.set_title("Illustrative Return Distribution", fontsize=12, pad=10)
    ax.set_xlabel("Portfolio Return", fontsize=9)
    ax.set_ylabel("Density", fontsize=9)
    ax.grid(alpha=0.20)
    ax.tick_params(labelsize=8)
    ax.legend(fontsize=7, frameon=False)
    for spine in ax.spines.values():
        spine.set_alpha(0.25)

    return _fig_to_base64(fig)


def _fig_to_base64(fig) -> str:
    buffer = BytesIO()
    fig.tight_layout()
    fig.savefig(buffer, format="png", bbox_inches="tight", pad_inches=0.08)
    plt.close(fig)
    buffer.seek(0)
    return base64.b64encode(buffer.read()).decode("utf-8")