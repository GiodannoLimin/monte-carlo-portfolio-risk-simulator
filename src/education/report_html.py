from __future__ import annotations

import base64
import html
import io
import re
from typing import Iterable

import matplotlib.pyplot as plt

from .report_charts import build_chart_payload
from .report_sections import GUIDE_SECTIONS
from .report_styles import get_report_styles


SECTION_GROUPS = [
    (
        "Foundations",
        "Beginner intuition and core portfolio concepts.",
        [
            "Quick Start: How to Use This Simulator",
            "What This App Does",
            "Glossary",
            "Portfolio Basics",
            "Risk and Return",
            "Why Monte Carlo Simulation Is Useful",
            "How the Simulation Works in Plain English",
        ],
    ),
    (
        "Reading the Outputs",
        "How to interpret charts, distributions, and portfolio results.",
        [
            "How to Read the Simulated Portfolio Paths Chart",
            "How to Read the Return Distribution",
            "How to Read the Terminal Value Distribution",
            "Understanding Expected Return and Volatility",
            "Understanding VaR and CVaR",
        ],
    ),
    (
        "Methodology",
        "The mathematical and modeling foundation of the simulator.",
        [
            "Portfolio Construction Mathematics",
            "Geometric Brownian Motion (GBM) Foundation",
            "Parameter Estimation",
            "Monte Carlo Engine Logic",
            "Portfolio Optimization",
            "How to Read the Efficient Frontier",
        ],
    ),
    (
        "Validation and Extensions",
        "Historical context, factor interpretation, stress testing, and projections.",
        [
            "Historical Backtesting",
            "Benchmark Comparison",
            "CAPM / Market Factor Analysis",
            "How to Read the CAPM Scatter Plot",
            "Stress Testing",
            "Investment Outcome Projections",
            "How to Interpret Projection Results",
        ],
    ),
    (
        "Cautions and Practice",
        "Common mistakes, assumptions, limitations, and practical interpretation.",
        [
            "Common Portfolio Analysis Mistakes",
            "Model Assumptions and Limitations",
            "FAQ",
        ],
    ),
]


def _formula_map() -> dict[str, list[str]]:
    return {
        "Understanding Expected Return and Volatility": [
            r"\mathbb{E}[R_p] = w^\top \mu",
            r"\sigma_p = \sqrt{w^\top \Sigma w}",
        ],
        "Understanding VaR and CVaR": [
            r"\mathrm{VaR}_{\alpha}(R) = Q_{1-\alpha}(R)",
            r"\mathrm{CVaR}_{\alpha}(R) = \mathbb{E}[R \mid R \leq \mathrm{VaR}_{\alpha}(R)]",
        ],
        "Portfolio Construction Mathematics": [
            r"R_p = \sum_{i=1}^{n} w_i R_i",
            r"\mathbb{E}[R_p] = w^\top \mu",
            r"\mathrm{Var}(R_p) = w^\top \Sigma w",
        ],
        "Geometric Brownian Motion (GBM) Foundation": [
            r"dS_t = \mu S_t \, dt + \sigma S_t \, dW_t",
            r"S_{t+\Delta t} = S_t \exp[(\mu - \frac{1}{2}\sigma^2)\Delta t + \sigma \sqrt{\Delta t} Z]",
        ],
        "Portfolio Optimization": [
            r"\mathrm{Sharpe} = \frac{\mathbb{E}[R_p] - R_f}{\sigma_p}",
        ],
        "Historical Backtesting": [
            r"V_t = \prod_{s=1}^{t}(1 + R_s)",
        ],
        "CAPM / Market Factor Analysis": [
            r"R_p - R_f = \alpha + \beta (R_m - R_f) + \varepsilon",
        ],
    }


def _slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9\s-]", "", text)
    text = re.sub(r"\s+", "-", text)
    text = re.sub(r"-+", "-", text)
    return text.strip("-")


def _escape(text: str) -> str:
    return html.escape(text, quote=True)


def _level_label(level: str) -> str:
    return str(level).upper()


def _level_color(level: str) -> str:
    palette = {
        "guide": "#9ef0d1",
        "core": "#8bb8ff",
        "intermediate": "#ffd89c",
        "advanced": "#f6b0ff",
    }
    return palette.get(level.lower(), "#9ef0d1")


def _group_title_to_id(group_title: str) -> str:
    return f"group-{_slugify(group_title)}"


def _section_title_to_id(section_title: str) -> str:
    return f"section-{_slugify(section_title)}"


def _render_formula_svg_data_uri(formula: str, *, fontsize: int = 17) -> str:
    """
    Render LaTeX-like math to SVG using matplotlib and return a data URI.

    This is much sharper in HTML/WeasyPrint than low-res PNG.
    """
    fig = plt.figure(figsize=(0.01, 0.01))
    fig.patch.set_alpha(0.0)

    text = fig.text(
        0.0,
        0.0,
        f"${formula}$",
        fontsize=fontsize,
        color="white",
    )

    fig.canvas.draw()
    bbox = text.get_window_extent(renderer=fig.canvas.get_renderer()).expanded(1.06, 1.28)

    width_in = max(bbox.width / fig.dpi, 0.1)
    height_in = max(bbox.height / fig.dpi, 0.1)
    fig.set_size_inches(width_in, height_in)

    text.set_position((0.02, 0.08))

    svg_buffer = io.StringIO()
    fig.savefig(
        svg_buffer,
        format="svg",
        transparent=True,
        bbox_inches="tight",
        pad_inches=0.03,
    )
    plt.close(fig)

    svg_text = svg_buffer.getvalue()

    # Force dark text in the SVG for PDF mode readability.
    svg_text = svg_text.replace("white", "#111111")
    svg_text = svg_text.replace("#ffffff", "#111111")
    svg_text = svg_text.replace("#fff", "#111111")

    encoded = base64.b64encode(svg_text.encode("utf-8")).decode("ascii")
    return f"data:image/svg+xml;base64,{encoded}"


def _render_formula_block(formula: str) -> str:
    try:
        svg_uri = _render_formula_svg_data_uri(formula)
        return (
            '<div class="math-block">'
            f'<img src="{svg_uri}" alt="{_escape(formula)}" '
            'style="display:block; max-width:100%; height:auto; margin:0;" />'
            "</div>"
        )
    except Exception:
        # Fallback if formula rendering fails
        return f'<div class="math-block"><code>{_escape(formula)}</code></div>'


def _render_paragraph(text: str) -> str:
    return f"<p>{_escape(text)}</p>"


def _render_list(items: Iterable[str]) -> str:
    lis = "".join(f"<li>{_escape(item)}</li>" for item in items)
    return f"<ul>{lis}</ul>"


def _render_callout(title: str, body: str) -> str:
    return (
        '<div class="callout">'
        f"<strong>{_escape(title)}.</strong> {_escape(body)}"
        "</div>"
    )


def _body_to_html(section: dict) -> str:
    body = section["body"].strip()
    lines = [line.rstrip() for line in body.splitlines()]

    blocks: list[str] = []
    bullets: list[str] = []

    def flush_bullets():
        nonlocal bullets
        if bullets:
            blocks.append(_render_list(bullets))
            bullets = []

    for raw in lines:
        line = raw.strip()

        if not line:
            flush_bullets()
            continue

        if line.startswith("- "):
            bullets.append(line[2:].strip())
            continue

        flush_bullets()

        if line.startswith("Example:"):
            blocks.append(_render_callout("Example", line.replace("Example:", "", 1).strip()))
        elif line.startswith("Important:"):
            blocks.append(_render_callout("Important", line.replace("Important:", "", 1).strip()))
        else:
            blocks.append(_render_paragraph(line))

    flush_bullets()

    for formula in _formula_map().get(section["title"], []):
        blocks.append(_render_formula_block(formula))

    return "\n".join(blocks)


def _render_toc_panel() -> str:
    links: list[str] = []

    for group_title, _group_subtitle, titles in SECTION_GROUPS:
        group_id = _group_title_to_id(group_title)
        links.append(f'<a href="#{group_id}"><strong>{_escape(group_title)}</strong></a>')

        for title in titles:
            section_id = _section_title_to_id(title)
            links.append(
                f'<a href="#{section_id}" style="padding-left: 20px;">{_escape(title)}</a>'
            )

    return (
        '<section class="panel">'
        "<h2>Table of Contents</h2>"
        '<div class="toc">'
        + "".join(links)
        + "</div>"
        "</section>"
    )


def _render_summary_panel() -> str:
    metrics = [
        ("Simulation Core", "GBM + Monte Carlo"),
        ("Risk Lens", "Volatility, VaR, CVaR"),
        ("Allocation Lens", "Optimization + Frontier"),
        ("Validation Lens", "Backtesting + CAPM + Stress"),
    ]

    metric_cards = "".join(
        (
            '<div class="metric-card">'
            f'<div class="label">{_escape(label)}</div>'
            f'<div class="value">{_escape(value)}</div>'
            "</div>"
        )
        for label, value in metrics
    )

    return (
        '<section class="panel">'
        "<h2>What this handbook covers</h2>"
        "<p>"
        "This guide moves from intuitive portfolio ideas to simulation logic, "
        "risk metrics, optimization, historical validation, and interpretation."
        "</p>"
        f'<div class="summary-grid">{metric_cards}</div>'
        "</section>"
    )


def _render_hero() -> str:
    return """
    <header class="hero">
        <div class="eyebrow">Portfolio Analytics Handbook</div>
        <h1>Monte Carlo Portfolio Risk Simulator</h1>
        <p>
            A standalone educational guide covering simulation, risk metrics,
            optimization, backtesting, factor analysis, stress testing, and
            model interpretation.
        </p>
    </header>
    """


def _render_chart_section() -> str:
    charts = build_chart_payload()

    cards: list[str] = []
    for chart in charts:
        image_base64 = chart["image_base64"]
        image_src = f"data:image/png;base64,{image_base64}"

        cards.append(
            (
                '<article class="chart-card">'
                f"<h3>{_escape(chart['title'])}</h3>"
                f"<p>{_escape(chart['caption'])}</p>"
                f'<img src="{image_src}" alt="{_escape(chart["title"])}" />'
                "</article>"
            )
        )

    return (
        '<section class="panel" id="visual-overview">'
        "<h2>Visual Overview</h2>"
        "<p>"
        "These visual examples summarize the core concepts behind simulation, "
        "allocation, and portfolio risk."
        "</p>"
        "</section>"
        f'<section class="charts-grid">{"".join(cards)}</section>'
    )


def _render_group_intro(group_title: str, group_subtitle: str) -> str:
    group_id = _group_title_to_id(group_title)
    return (
        f'<section class="section major-section" id="{group_id}">'
        '<div class="section-header">'
        f"<h2>{_escape(group_title)}</h2>"
        '<span class="level-badge" style="color:#9ef0d1;">GROUP</span>'
        "</div>"
        f"<p>{_escape(group_subtitle)}</p>"
        "</section>"
    )


def _render_section(section: dict) -> str:
    title = section["title"]
    level = section.get("level", "guide")
    section_id = _section_title_to_id(title)
    level_color = _level_color(level)

    return (
        f'<section class="section" id="{section_id}">'
        '<div class="section-header">'
        f"<h2>{_escape(title)}</h2>"
        f'<span class="level-badge" style="color:{level_color};">{_escape(_level_label(level))}</span>'
        "</div>"
        f"{_body_to_html(section)}"
        "</section>"
    )


def _render_sections() -> str:
    section_lookup = {section["title"]: section for section in GUIDE_SECTIONS}

    html_parts: list[str] = []
    for group_title, group_subtitle, titles in SECTION_GROUPS:
        html_parts.append(_render_group_intro(group_title, group_subtitle))

        for title in titles:
            section = section_lookup.get(title)
            if section is None:
                continue
            html_parts.append(_render_section(section))

    return "\n".join(html_parts)


def build_report_html(pdf_mode: bool = False) -> str:
    """
    Returns a full HTML document string for preview or WeasyPrint PDF.

    pdf_mode=False:
        Intended for browser / Streamlit preview.

    pdf_mode=True:
        Intended for WeasyPrint rendering.
    """
    body_class = "pdf-mode" if pdf_mode else "preview-mode"
    styles = get_report_styles(pdf_mode=pdf_mode)

    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Portfolio Analytics Handbook</title>
    {styles}
</head>
<body class="{body_class}">
    <main class="page-shell">
        {_render_hero()}

        <section class="top-grid">
            {_render_summary_panel()}
            {_render_toc_panel()}
        </section>

        {_render_chart_section()}

        {_render_sections()}

        <div class="footer-note">
            This handbook is educational material for interpreting portfolio simulation
            outputs. It is not investment advice.
        </div>
    </main>
</body>
</html>
    """.strip()