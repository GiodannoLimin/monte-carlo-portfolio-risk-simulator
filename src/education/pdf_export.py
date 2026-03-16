from __future__ import annotations

import shutil
import subprocess
import tempfile
from pathlib import Path

from .report_latex import build_handbook_tex


def _find_latex_engine() -> str:
    for cmd in ("latexmk", "pdflatex", "xelatex"):
        if shutil.which(cmd):
            return cmd
    raise RuntimeError(
        "No LaTeX engine found. Install TinyTeX, TeX Live, or MiKTeX, then restart your terminal."
    )


def build_education_pdf_bytes() -> bytes:
    print("USING LATEX PDF EXPORT")

    engine = _find_latex_engine()

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        tex_path = tmp_path / "main.tex"
        pdf_path = tmp_path / "main.pdf"

        tex_path.write_text(build_handbook_tex(), encoding="utf-8")

        if engine == "latexmk":
            commands = [
                ["latexmk", "-pdf", "-interaction=nonstopmode", "-halt-on-error", "main.tex"]
            ]
        elif engine == "xelatex":
            commands = [
                ["xelatex", "-interaction=nonstopmode", "-halt-on-error", "main.tex"],
                ["xelatex", "-interaction=nonstopmode", "-halt-on-error", "main.tex"],
            ]
        else:
            commands = [
                ["pdflatex", "-interaction=nonstopmode", "-halt-on-error", "main.tex"],
                ["pdflatex", "-interaction=nonstopmode", "-halt-on-error", "main.tex"],
            ]

        for cmd in commands:
            result = subprocess.run(
                cmd,
                cwd=tmp_path,
                capture_output=True,
                text=True,
            )
            if result.returncode != 0:
                log_path = tmp_path / "main.log"
                log_text = (
                    log_path.read_text(encoding="utf-8", errors="ignore")
                    if log_path.exists()
                    else ""
                )
                raise RuntimeError(
                    "LaTeX PDF generation failed.\n\n"
                    f"Command: {' '.join(cmd)}\n\n"
                    f"STDOUT:\n{result.stdout}\n\n"
                    f"STDERR:\n{result.stderr}\n\n"
                    f"LOG:\n{log_text}"
                )

        if not pdf_path.exists():
            raise RuntimeError("LaTeX compilation finished but main.pdf was not created.")

        return pdf_path.read_bytes()