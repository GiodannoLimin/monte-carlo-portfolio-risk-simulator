from __future__ import annotations

import os
import re
from pathlib import Path

from .report_sections import GUIDE_SECTIONS

SECTION_GROUPS = [
    (
        "Foundations",
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
        [
            "Common Portfolio Analysis Mistakes",
            "Model Assumptions and Limitations",
            "FAQ",
        ],
    ),
]


def _clean_text(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def _latex_escape(text: str) -> str:
    replacements = {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }
    pattern = re.compile(r"[\\&%#_{}~^]")
    return pattern.sub(lambda m: replacements[m.group()], text)


def _extract_inline_math(text: str) -> tuple[str, dict[str, str]]:
    mapping: dict[str, str] = {}

    def repl(match: re.Match[str]) -> str:
        token = f"INLINEPH{len(mapping)}END"
        mapping[token] = match.group(0)
        return token

    new_text = re.sub(r"(?<!\$)\$(?!\$)(.+?)(?<!\$)\$(?!\$)", repl, text)
    return new_text, mapping


def _restore_inline_math(text: str, mapping: dict[str, str]) -> str:
    for token, math_text in mapping.items():
        text = text.replace(token, math_text)
    return text


def _escape_text_preserving_inline_math(text: str) -> str:
    stripped, mapping = _extract_inline_math(text)
    escaped = _latex_escape(stripped)
    return _restore_inline_math(escaped, mapping)


def _section_level_note(level: str) -> str:
    level = str(level).strip().lower()
    mapping = {
        "guide": "Guide level",
        "core": "Core concept",
        "intermediate": "Intermediate depth",
        "advanced": "Advanced concept",
        "technical": "Technical",
        "beginner": "Beginner",
    }
    return mapping.get(level, level.title())


def _is_glossary_section(section: dict) -> bool:
    return section.get("title", "").strip().lower() == "glossary"


def _is_faq_section(section: dict) -> bool:
    return section.get("title", "").strip().lower() == "faq"


def _normalize_display_math(expr: str) -> str:
    expr = expr.strip()
    expr = re.sub(r"^\s*\\\[\s*", "", expr)
    expr = re.sub(r"\s*\\\]\s*$", "", expr)
    return expr.strip()


def _render_display_math(expr: str) -> str:
    expr = _normalize_display_math(expr)
    return "\n".join(
        [
            r"\begin{equation}",
            expr,
            r"\end{equation}",
        ]
    )


def _split_blocks(body: str) -> list[tuple[str, str]]:
    text = _clean_text(body)
    if not text:
        return []

    pattern = re.compile(r"\$\$(.*?)\$\$", flags=re.DOTALL)
    blocks: list[tuple[str, str]] = []

    last = 0
    for match in pattern.finditer(text):
        before = text[last:match.start()]
        if before.strip():
            for chunk in re.split(r"\n\s*\n", before.strip()):
                if chunk.strip():
                    blocks.append(("paragraph", chunk.strip()))
        blocks.append(("display_math", match.group(1).strip()))
        last = match.end()

    tail = text[last:]
    if tail.strip():
        for chunk in re.split(r"\n\s*\n", tail.strip()):
            if chunk.strip():
                blocks.append(("paragraph", chunk.strip()))

    return blocks


def _render_itemize(items: list[str]) -> str:
    lines = [r"\begin{itemize}"]
    for item in items:
        lines.append(rf"\item {_escape_text_preserving_inline_math(item)}")
    lines.append(r"\end{itemize}")
    return "\n".join(lines)


def _render_enumerate(items: list[str]) -> str:
    lines = [r"\begin{enumerate}"]
    for item in items:
        lines.append(rf"\item {_escape_text_preserving_inline_math(item)}")
    lines.append(r"\end{enumerate}")
    return "\n".join(lines)


def _glossary_body_to_latex(body: str) -> str:
    lines = [line.rstrip() for line in _clean_text(body).splitlines()]
    items: list[tuple[str, str]] = []

    i = 0
    while i < len(lines):
        line = lines[i].strip()

        if not line:
            i += 1
            continue

        if line.endswith(":"):
            term = line[:-1].strip()
            i += 1

            definition_parts: list[str] = []
            while i < len(lines):
                nxt = lines[i].strip()
                if not nxt:
                    if definition_parts:
                        i += 1
                        break
                    i += 1
                    continue
                if nxt.endswith(":") and definition_parts:
                    break
                definition_parts.append(nxt)
                i += 1

            definition = " ".join(definition_parts).strip()
            items.append((term, definition))
        else:
            i += 1

    if not items:
        return _paragraph_style_body_to_latex(body)

    parts = [
        r"\begin{description}[leftmargin=3.4cm, style=nextline, font=\normalfont\bfseries]"
    ]
    for term, definition in items:
        parts.append(
            rf"\item[{_escape_text_preserving_inline_math(term)}] {_escape_text_preserving_inline_math(definition)}"
        )
    parts.append(r"\end{description}")
    return "\n".join(parts)


def _faq_body_to_latex(body: str) -> str:
    lines = [line.rstrip() for line in _clean_text(body).splitlines()]
    parts: list[str] = []
    i = 0

    while i < len(lines):
        line = lines[i].strip()

        if not line:
            i += 1
            continue

        if line.startswith("Q:"):
            question = line[2:].strip()
            answer = ""

            j = i + 1
            while j < len(lines):
                nxt = lines[j].strip()
                if not nxt:
                    j += 1
                    break
                if nxt.startswith("Q:"):
                    break
                if nxt.startswith("A:"):
                    answer = nxt[2:].strip()
                else:
                    answer = (answer + " " + nxt).strip()
                j += 1

            parts.append(r"\begin{callout}")
            parts.append(r"\textbf{Q.} " + _escape_text_preserving_inline_math(question))
            if answer:
                parts.append("")
                parts.append(r"\textbf{A.} " + _escape_text_preserving_inline_math(answer))
            parts.append(r"\end{callout}")
            parts.append("")
            i = j
            continue

        parts.append(_escape_text_preserving_inline_math(line))
        parts.append("")
        i += 1

    return "\n".join(parts).strip()


def _render_paragraph_block(block: str) -> str:
    raw_lines = [line.rstrip() for line in block.splitlines()]
    lines = [line.strip() for line in raw_lines if line.strip()]

    if not lines:
        return ""

    if lines[0] == "Example:":
        content_lines = lines[1:]
        parts = [r"\begin{callout}", r"\textbf{Example.}"]
        if content_lines:
            parts.append("")
            parts.append(_render_paragraph_block("\n".join(content_lines)))
        parts.append(r"\end{callout}")
        return "\n".join(parts)

    if lines[0] == "Important:":
        content_lines = lines[1:]
        parts = [r"\begin{callout}", r"\textbf{Important.}"]
        if content_lines:
            parts.append("")
            parts.append(_render_paragraph_block("\n".join(content_lines)))
        parts.append(r"\end{callout}")
        return "\n".join(parts)

    if all(re.match(r"^-\s+", line) for line in lines):
        items = [re.sub(r"^-\s+", "", line).strip() for line in lines]
        return _render_itemize(items)

    if all(re.match(r"^\d+\.\s+", line) for line in lines):
        items = [re.sub(r"^\d+\.\s+", "", line).strip() for line in lines]
        return _render_enumerate(items)

    if len(lines) == 1 and lines[0].endswith(":"):
        label = _escape_text_preserving_inline_math(lines[0][:-1])
        return r"\textbf{" + label + r".}"

    parts: list[str] = []
    i = 0
    while i < len(lines):
        line = lines[i]

        if re.match(r"^-\s+", line):
            items: list[str] = []
            while i < len(lines) and re.match(r"^-\s+", lines[i]):
                items.append(re.sub(r"^-\s+", "", lines[i]).strip())
                i += 1
            parts.append(_render_itemize(items))
            continue

        if re.match(r"^\d+\.\s+", line):
            items = []
            while i < len(lines) and re.match(r"^\d+\.\s+", lines[i]):
                items.append(re.sub(r"^\d+\.\s+", "", lines[i]).strip())
                i += 1
            parts.append(_render_enumerate(items))
            continue

        if line.endswith(":"):
            label = _escape_text_preserving_inline_math(line[:-1])
            parts.append(r"\textbf{" + label + r".}")
        else:
            parts.append(_escape_text_preserving_inline_math(line))
        i += 1

    return "\n\n".join(parts).strip()


def _paragraph_style_body_to_latex(body: str) -> str:
    blocks = _split_blocks(body)
    rendered: list[str] = []

    for kind, content in blocks:
        if kind == "display_math":
            rendered.append(_render_display_math(content))
        else:
            part = _render_paragraph_block(content)
            if part:
                rendered.append(part)

    return "\n\n".join(rendered).strip()


def _body_to_latex(section: dict) -> str:
    body = section.get("body", "")

    if _is_glossary_section(section):
        return _glossary_body_to_latex(body)

    if _is_faq_section(section):
        return _faq_body_to_latex(body)

    return _paragraph_style_body_to_latex(body)


def _render_section(section: dict) -> str:
    title = _latex_escape(section["title"])
    level_note = _latex_escape(_section_level_note(section.get("level", "guide")))
    body_latex = _body_to_latex(section)

    parts = [
        f"\\section{{{title}}}",
        r"\begin{callout}",
        rf"\textbf{{Level.}} {level_note}",
        r"\end{callout}",
        "",
    ]

    if body_latex:
        parts.append(body_latex)
        parts.append("")

    return "\n".join(parts).strip()


def _document_preamble() -> str:
    return r"""\documentclass[11pt]{report}

\usepackage[a4paper,margin=1in]{geometry}
\usepackage[T1]{fontenc}
\usepackage[utf8]{inputenc}
\usepackage{lmodern}
\usepackage{amsmath}
\usepackage{amssymb}
\usepackage{graphicx}
\usepackage[hidelinks]{hyperref}
\usepackage{titlesec}
\usepackage{fancyhdr}
\usepackage{xcolor}
\usepackage{tcolorbox}
\usepackage{setspace}
\usepackage{enumitem}
\usepackage{parskip}

\onehalfspacing

\definecolor{accent}{RGB}{40,80,160}
\definecolor{soft}{RGB}{240,245,255}

\titleformat{\chapter}
{\Huge\bfseries\color{accent}}
{\thechapter}{20pt}{}

\titleformat{\section}
{\Large\bfseries}
{\thesection}{12pt}{}

\titleformat{\subsection}
{\large\bfseries}
{\thesubsection}{10pt}{}

\pagestyle{fancy}
\fancyhf{}
\fancyhead[L]{Portfolio Analytics Handbook}
\fancyhead[R]{\thepage}

\newtcolorbox{callout}{
colback=soft,
colframe=accent,
boxrule=0.6pt,
arc=4pt
}

\title{
\Huge Portfolio Analytics Handbook\\
\vspace{6pt}
\Large Monte Carlo Portfolio Risk Simulator
}

\author{Portfolio Analytics Project}
\date{\today}

\begin{document}

\maketitle
\clearpage

\tableofcontents
\clearpage
""".strip()


def _document_end() -> str:
    return r"\end{document}"


def build_handbook_tex() -> str:
    section_lookup = {section["title"]: section for section in GUIDE_SECTIONS}
    parts: list[str] = [_document_preamble(), ""]

    for chapter_title, titles in SECTION_GROUPS:
        parts.append(f"\\chapter{{{_latex_escape(chapter_title)}}}")
        parts.append("")

        for title in titles:
            section = section_lookup.get(title)
            if section is None:
                continue
            parts.append(_render_section(section))
            parts.append("")

    parts.append(_document_end())
    return "\n".join(parts).strip() + "\n"


def write_handbook_tex(output_path: str | os.PathLike | None = None) -> Path:
    if output_path is None:
        output_path = Path("handbook") / "main.tex"
    else:
        output_path = Path(output_path)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(build_handbook_tex(), encoding="utf-8")
    return output_path