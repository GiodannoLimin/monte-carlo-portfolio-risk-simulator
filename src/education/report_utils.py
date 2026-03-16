import html
import re


def slugify(text: str) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9\s-]", "", text).strip().lower()
    return re.sub(r"[\s\-]+", "-", cleaned)


def format_inline(text: str) -> str:
    """
    Escapes HTML safely, but preserves inline/display LaTeX delimiters
    and supports simple **bold** formatting.
    """
    escaped = html.escape(text)

    # restore escaped dollar signs so MathJax can still see them
    escaped = escaped.replace("&#x24;", "$").replace("&#36;", "$")

    # restore common latex characters if escaped
    escaped = escaped.replace("&amp;", "&")

    # **bold**
    escaped = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", escaped)

    return escaped


def level_badge(level: str) -> str:
    text = (level or "guide").strip().upper()
    return f'<span class="level-badge">{html.escape(text)}</span>'


def _split_into_blocks(text: str) -> list[tuple[str, str]]:
    """
    Parse text into atomic blocks:
    - paragraph
    - ordered_list
    - unordered_list
    - math

    This avoids the earlier bug where a math block got split across lines
    and the closing </div> appeared as text.
    """
    lines = text.strip().splitlines()
    blocks: list[tuple[str, str]] = []

    paragraph_lines: list[str] = []
    list_items: list[str] = []
    list_type: str | None = None

    def flush_paragraph() -> None:
        nonlocal paragraph_lines
        if paragraph_lines:
            content = " ".join(line.strip() for line in paragraph_lines if line.strip())
            if content:
                blocks.append(("paragraph", content))
            paragraph_lines = []

    def flush_list() -> None:
        nonlocal list_items, list_type
        if list_items and list_type:
            blocks.append((list_type, "\n".join(list_items)))
        list_items = []
        list_type = None

    i = 0
    while i < len(lines):
        raw = lines[i]
        stripped = raw.strip()

        if not stripped:
            flush_paragraph()
            flush_list()
            i += 1
            continue

        # display math block
        if stripped == "$$":
            flush_paragraph()
            flush_list()

            math_lines = []
            i += 1
            while i < len(lines) and lines[i].strip() != "$$":
                math_lines.append(lines[i])
                i += 1

            blocks.append(("math", "\n".join(math_lines).strip()))

            # skip closing $$
            if i < len(lines) and lines[i].strip() == "$$":
                i += 1
            continue

        ordered_match = re.match(r"^\d+\.\s+(.*)$", stripped)
        unordered_match = re.match(r"^-\s+(.*)$", stripped)

        if ordered_match:
            flush_paragraph()
            if list_type not in (None, "ordered_list"):
                flush_list()
            list_type = "ordered_list"
            list_items.append(ordered_match.group(1))
            i += 1
            continue

        if unordered_match:
            flush_paragraph()
            if list_type not in (None, "unordered_list"):
                flush_list()
            list_type = "unordered_list"
            list_items.append(unordered_match.group(1))
            i += 1
            continue

        flush_list()
        paragraph_lines.append(stripped)
        i += 1

    flush_paragraph()
    flush_list()

    return blocks


def render_rich_text(text: str) -> str:
    blocks = _split_into_blocks(text)
    rendered: list[str] = []

    for block_type, content in blocks:
        if block_type == "paragraph":
            rendered.append(f"<p>{format_inline(content)}</p>")

        elif block_type == "ordered_list":
            items = "".join(
                f"<li>{format_inline(item)}</li>"
                for item in content.splitlines()
                if item.strip()
            )
            rendered.append(f"<ol>{items}</ol>")

        elif block_type == "unordered_list":
            items = "".join(
                f"<li>{format_inline(item)}</li>"
                for item in content.splitlines()
                if item.strip()
            )
            rendered.append(f"<ul>{items}</ul>")

        elif block_type == "math":
            # keep math raw for MathJax
            rendered.append(f'<div class="math-block">$$\n{content}\n$$</div>')

    return "\n".join(rendered)