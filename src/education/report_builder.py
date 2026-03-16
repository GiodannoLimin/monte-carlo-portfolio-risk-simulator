from datetime import datetime

from .report_charts import build_chart_payload
from .report_sections import GUIDE_SECTIONS
from .report_styles import get_report_styles
from .report_utils import level_badge, render_rich_text


def _build_mathjax() -> str:
    return """
    <script>
      window.MathJax = {
        tex: {
          inlineMath: [['$', '$'], ['\\\\(', '\\\\)']],
          displayMath: [['$$', '$$'], ['\\\\[', '\\\\]']]
        },
        svg: {
          fontCache: 'global'
        },
        options: {
          skipHtmlTags: ['script', 'noscript', 'style', 'textarea', 'pre', 'code']
        }
      };
    </script>
    <script defer src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js"></script>
    """


def _build_anchor_fix_script() -> str:
    return """
    <script>
      document.addEventListener("DOMContentLoaded", function () {
        function handleInternalLinkClick(event) {
          const anchor = event.target.closest('a[href^="#"]');
          if (!anchor) return;

          const href = anchor.getAttribute("href");
          if (!href || href === "#") return;

          const targetId = href.slice(1);
          const target = document.getElementById(targetId);
          if (!target) return;

          event.preventDefault();

          target.scrollIntoView({
            behavior: "smooth",
            block: "start"
          });

          try {
            history.replaceState(null, "", "#" + targetId);
          } catch (err) {
            // ignore
          }
        }

        document.addEventListener("click", handleInternalLinkClick);
      });
    </script>
    """


def _build_header() -> str:
    return """
    <section class="hero">
        <div class="eyebrow">Education Guide · Monte Carlo Portfolio Risk Simulator</div>
        <h1>Portfolio Analytics Handbook</h1>
        <p>
            This guide explains the simulator from both an intuitive and technical perspective.
            It is designed to function as a standalone learning document: part beginner handbook,
            part quantitative reference, and part product-style methodology note.
        </p>
    </section>
    """


def _build_summary_panel() -> str:
    return """
    <div class="panel">
        <h2>What You Will Learn</h2>
        <p>
            This handbook covers the full logic of the simulator, from basic portfolio intuition
            to model assumptions, mathematical foundations, optimization, stress testing,
            and interpretation of outputs.
        </p>

        <div class="summary-grid">
            <div class="metric-card">
                <div class="label">Simulation Core</div>
                <div class="value">GBM + Monte Carlo</div>
            </div>
            <div class="metric-card">
                <div class="label">Risk Lens</div>
                <div class="value">Volatility, VaR, CVaR</div>
            </div>
            <div class="metric-card">
                <div class="label">Allocation Lens</div>
                <div class="value">Optimization + Frontier</div>
            </div>
            <div class="metric-card">
                <div class="label">Validation Lens</div>
                <div class="value">Backtest + CAPM + Stress</div>
            </div>
        </div>
    </div>
    """


def _build_toc_panel() -> str:
    links = []
    for section in GUIDE_SECTIONS:
        links.append(f'<a href="#{section["id"]}">{section["title"]}</a>')

    return f"""
    <div class="panel">
        <h2>Guide Outline</h2>
        <div class="toc">
            {"".join(links)}
        </div>
    </div>
    """


def _build_top_grid() -> str:
    return f"""
    <section class="top-grid">
        {_build_summary_panel()}
        {_build_toc_panel()}
    </section>
    """


def _build_charts() -> str:
    cards = []
    for chart in build_chart_payload():
        cards.append(
            f"""
            <article class="chart-card">
                <h3>{chart["title"]}</h3>
                <p>{chart["caption"]}</p>
                <img src="data:image/png;base64,{chart["image_base64"]}" alt="{chart["title"]}">
            </article>
            """
        )

    return f"""
    <section class="charts-grid">
        {''.join(cards)}
    </section>
    """


def _build_sections() -> str:
    html_parts = []

    for i, section in enumerate(GUIDE_SECTIONS):
        extra_classes = ["section"]

        if i in {0, 2, 4, 6, 8}:
            extra_classes.append("major-section")

        html_parts.append(
            f"""
            <section class="{' '.join(extra_classes)}" id="{section["id"]}">
                <div class="section-header">
                    <h2>{section["title"]}</h2>
                    {level_badge(section.get("level", "guide"))}
                </div>
                {render_rich_text(section["body"])}
            </section>
            """
        )

    return "\n".join(html_parts)


def _build_footer() -> str:
    generated = datetime.now().strftime("%Y-%m-%d %H:%M")
    return f"""
    <div class="footer-note">
        Generated on {generated}. This guide is educational and analytical in nature and should not be interpreted as personalized financial advice.
    </div>
    """


def build_education_html(pdf_mode: bool = False) -> str:
    styles = get_report_styles(pdf_mode=pdf_mode)
    mathjax = _build_mathjax()
    anchor_fix = "" if pdf_mode else _build_anchor_fix_script()
    header = _build_header()
    top_grid = _build_top_grid()
    charts = _build_charts()
    sections = _build_sections()
    footer = _build_footer()

    body_class = "pdf-mode" if pdf_mode else "preview-mode"

    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <title>Portfolio Analytics Handbook</title>
        {styles}
        {mathjax}
        {anchor_fix}
    </head>
    <body class="{body_class}">
        <main class="page-shell">
            {header}
            {top_grid}
            {charts}
            {sections}
            {footer}
        </main>
    </body>
    </html>
    """


def build_education_html_bytes(pdf_mode: bool = False) -> bytes:
    return build_education_html(pdf_mode=pdf_mode).encode("utf-8")