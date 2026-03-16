def get_report_styles(pdf_mode: bool = False) -> str:
    body_class = "pdf-mode" if pdf_mode else "preview-mode"

    return f"""
    <style>
        :root {{
            --bg-1: #07111f;
            --bg-2: #0d1830;
            --bg-3: #161f46;
            --panel: rgba(255, 255, 255, 0.08);
            --panel-strong: rgba(255, 255, 255, 0.12);
            --border: rgba(255, 255, 255, 0.14);
            --text: #eef3ff;
            --muted: #b8c5e3;
            --soft: #8fa3d2;
            --accent: #8bb8ff;
            --accent-2: #9ef0d1;
            --warning: #ffd89c;
            --shadow: 0 18px 60px rgba(0, 0, 0, 0.28);
            --radius-xl: 24px;
            --radius-lg: 18px;
            --radius-md: 14px;
            --content-width: 1180px;
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
            font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont,
                "Segoe UI", sans-serif;
            background:
                radial-gradient(circle at top left, rgba(77, 123, 255, 0.24), transparent 32%),
                radial-gradient(circle at top right, rgba(78, 224, 195, 0.16), transparent 28%),
                linear-gradient(135deg, var(--bg-1) 0%, var(--bg-2) 48%, var(--bg-3) 100%);
            line-height: 1.65;
        }}

        .page-shell {{
            width: min(var(--content-width), calc(100% - 32px));
            margin: 0 auto;
            padding: 28px 0 60px;
        }}

        .hero {{
            position: relative;
            overflow: hidden;
            border: 1px solid var(--border);
            border-radius: 30px;
            padding: 34px 34px 28px;
            background: linear-gradient(
                135deg,
                rgba(255, 255, 255, 0.10) 0%,
                rgba(255, 255, 255, 0.05) 100%
            );
            backdrop-filter: blur(14px);
            box-shadow: var(--shadow);
            margin-bottom: 22px;
        }}

        .hero::after {{
            content: "";
            position: absolute;
            inset: auto -80px -80px auto;
            width: 220px;
            height: 220px;
            border-radius: 999px;
            background: radial-gradient(circle, rgba(139, 184, 255, 0.28), transparent 68%);
            pointer-events: none;
        }}

        .eyebrow {{
            display: inline-flex;
            align-items: center;
            gap: 8px;
            font-size: 12px;
            font-weight: 700;
            letter-spacing: 0.12em;
            text-transform: uppercase;
            color: var(--accent-2);
            margin-bottom: 14px;
        }}

        .hero h1 {{
            margin: 0 0 12px;
            font-size: clamp(30px, 4vw, 46px);
            line-height: 1.08;
            letter-spacing: -0.03em;
        }}

        .hero p {{
            margin: 0;
            max-width: 900px;
            color: var(--muted);
            font-size: 16px;
        }}

        .top-grid {{
            display: grid;
            grid-template-columns: 1.25fr 0.75fr;
            gap: 18px;
            margin-bottom: 22px;
        }}

        .panel {{
            border: 1px solid var(--border);
            background: var(--panel);
            backdrop-filter: blur(12px);
            border-radius: var(--radius-xl);
            padding: 22px;
            box-shadow: var(--shadow);
        }}

        .panel h2,
        .panel h3 {{
            margin-top: 0;
        }}

        .summary-grid {{
            display: grid;
            grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: 12px;
            margin-top: 14px;
        }}

        .metric-card {{
            border: 1px solid var(--border);
            background: rgba(255, 255, 255, 0.05);
            border-radius: var(--radius-md);
            padding: 14px 16px;
        }}

        .metric-card .label {{
            color: var(--soft);
            font-size: 12px;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            margin-bottom: 6px;
            font-weight: 700;
        }}

        .metric-card .value {{
            font-size: 20px;
            font-weight: 800;
            line-height: 1.1;
        }}

        .toc {{
            display: grid;
            gap: 10px;
        }}

        .toc a {{
            display: block;
            padding: 10px 12px;
            border-radius: 12px;
            text-decoration: none;
            color: var(--text);
            border: 1px solid transparent;
            background: rgba(255, 255, 255, 0.035);
            transition: 0.2s ease;
            font-size: 14px;
        }}

        .toc a:hover {{
            background: rgba(255, 255, 255, 0.07);
            border-color: var(--border);
            transform: translateY(-1px);
        }}

        .charts-grid {{
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 16px;
            margin-bottom: 22px;
        }}

        .chart-card {{
            border: 1px solid var(--border);
            background: var(--panel);
            border-radius: var(--radius-xl);
            padding: 18px;
            box-shadow: var(--shadow);
            break-inside: avoid;
            page-break-inside: avoid;
        }}

        .chart-card h3 {{
            margin: 0 0 10px;
            font-size: 17px;
        }}

        .chart-card p {{
            margin: 0 0 14px;
            color: var(--muted);
            font-size: 14px;
        }}

        .chart-card img {{
            width: 100%;
            border-radius: 16px;
            display: block;
            border: 1px solid rgba(255, 255, 255, 0.08);
            background: rgba(255, 255, 255, 0.03);
        }}

        .section {{
            border: 1px solid var(--border);
            background: var(--panel);
            backdrop-filter: blur(10px);
            border-radius: var(--radius-xl);
            padding: 24px;
            margin-bottom: 18px;
            box-shadow: var(--shadow);
            scroll-margin-top: 18px;
        }}

        .section-header {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 14px;
            margin-bottom: 14px;
            break-after: avoid;
            page-break-after: avoid;
        }}

        .section h2 {{
            margin: 0;
            font-size: clamp(22px, 2.1vw, 30px);
            line-height: 1.15;
            letter-spacing: -0.02em;
        }}

        .level-badge {{
            flex-shrink: 0;
            padding: 7px 12px;
            border-radius: 999px;
            font-size: 12px;
            font-weight: 800;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            border: 1px solid var(--border);
            background: rgba(255, 255, 255, 0.06);
            color: var(--accent-2);
        }}

        .section p {{
            margin: 0 0 12px;
            color: var(--text);
        }}

        .section ul,
        .section ol {{
            margin: 0 0 14px 22px;
            color: var(--text);
        }}

        .section li {{
            margin-bottom: 8px;
        }}

        .section strong {{
            color: #ffffff;
        }}

        .math-block {{
            overflow-x: auto;
            margin: 16px 0;
            padding: 14px 16px;
            border-radius: 14px;
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid var(--border);
            break-inside: avoid;
            page-break-inside: avoid;
        }}

        .callout {{
            border-left: 4px solid var(--accent);
            background: rgba(139, 184, 255, 0.08);
            border-radius: 14px;
            padding: 14px 16px;
            margin: 16px 0;
            color: var(--text);
            break-inside: avoid;
            page-break-inside: avoid;
        }}

        .footer-note {{
            margin-top: 20px;
            color: var(--muted);
            font-size: 14px;
            text-align: center;
        }}

        .page-break {{
            break-before: page;
            page-break-before: always;
        }}

        @media (max-width: 1024px) {{
            .top-grid,
            .charts-grid {{
                grid-template-columns: 1fr;
            }}
        }}

        @media (max-width: 720px) {{
            .page-shell {{
                width: min(calc(100% - 18px), var(--content-width));
                padding-top: 14px;
            }}

            .hero,
            .panel,
            .chart-card,
            .section {{
                padding: 18px;
                border-radius: 20px;
            }}

            .summary-grid {{
                grid-template-columns: 1fr;
            }}

            .section-header {{
                align-items: flex-start;
                flex-direction: column;
            }}
        }}

        @page {{
            size: A4;
            margin: 16mm 14mm 18mm 14mm;

            @bottom-right {{
                content: counter(page);
                color: #d9e4ff;
                font-size: 9pt;
                font-family: Inter, "Segoe UI", sans-serif;
            }}

            @bottom-left {{
                content: "Portfolio Analytics Handbook";
                color: #9fb2d9;
                font-size: 9pt;
                font-family: Inter, "Segoe UI", sans-serif;
            }}
        }}

        body.pdf-mode {{
            margin: 0 !important;
            color: var(--text) !important;
            font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont,
                "Segoe UI", sans-serif !important;
            background:
                radial-gradient(circle at top left, rgba(77, 123, 255, 0.24), transparent 32%),
                radial-gradient(circle at top right, rgba(78, 224, 195, 0.16), transparent 28%),
                linear-gradient(135deg, var(--bg-1) 0%, var(--bg-2) 48%, var(--bg-3) 100%) !important;
            line-height: 1.55 !important;
            -webkit-print-color-adjust: exact;
            print-color-adjust: exact;
        }}

        body.pdf-mode .page-shell {{
            width: 100% !important;
            max-width: none !important;
            margin: 0 !important;
            padding: 0 !important;
        }}

        body.pdf-mode .hero {{
            position: relative !important;
            overflow: hidden !important;
            border: 1px solid rgba(255,255,255,0.14) !important;
            border-radius: 28px !important;
            padding: 18mm 14mm 16mm !important;
            margin: 0 0 10mm 0 !important;
            background:
                radial-gradient(circle at top right, rgba(158, 240, 209, 0.10), transparent 32%),
                linear-gradient(
                    135deg,
                    rgba(255,255,255,0.10) 0%,
                    rgba(255,255,255,0.05) 100%
                ) !important;
            box-shadow: none !important;
            backdrop-filter: none !important;
            break-after: page;
            page-break-after: always;
        }}

        body.pdf-mode .hero::after {{
            content: "";
            position: absolute;
            inset: auto -55px -55px auto;
            width: 170px;
            height: 170px;
            border-radius: 999px;
            background: radial-gradient(circle, rgba(139, 184, 255, 0.24), transparent 68%);
            display: block !important;
        }}

        body.pdf-mode .eyebrow {{
            color: var(--accent-2) !important;
            margin-bottom: 4mm !important;
            font-size: 10pt !important;
        }}

        body.pdf-mode .hero h1 {{
            color: #ffffff !important;
            font-size: 25pt !important;
            line-height: 1.08 !important;
            margin: 0 0 4mm 0 !important;
        }}

        body.pdf-mode .hero p {{
            color: var(--muted) !important;
            font-size: 11pt !important;
            max-width: none !important;
            margin: 0 !important;
        }}

        body.pdf-mode .top-grid {{
            display: grid !important;
            grid-template-columns: 1.2fr 0.8fr !important;
            gap: 8mm !important;
            margin: 0 0 10mm 0 !important;
        }}

        body.pdf-mode .panel,
        body.pdf-mode .chart-card,
        body.pdf-mode .section,
        body.pdf-mode .metric-card {{
            color: var(--text) !important;
            border: 1px solid rgba(255,255,255,0.12) !important;
            background: rgba(255,255,255,0.07) !important;
            border-radius: 18px !important;
            box-shadow: none !important;
            backdrop-filter: none !important;
        }}

        body.pdf-mode .panel {{
            padding: 6mm !important;
            margin: 0 !important;
            break-inside: avoid;
            page-break-inside: avoid;
        }}

        body.pdf-mode .panel h2,
        body.pdf-mode .panel h3 {{
            color: #ffffff !important;
        }}

        body.pdf-mode .summary-grid {{
            display: grid !important;
            grid-template-columns: repeat(2, minmax(0, 1fr)) !important;
            gap: 3mm !important;
            margin-top: 4mm !important;
        }}

        body.pdf-mode .metric-card {{
            padding: 4mm !important;
            margin: 0 !important;
        }}

        body.pdf-mode .metric-card .label {{
            color: var(--soft) !important;
            font-size: 8.5pt !important;
        }}

        body.pdf-mode .metric-card .value {{
            color: #ffffff !important;
            font-size: 12pt !important;
        }}

        body.pdf-mode .toc {{
            display: block !important;
        }}

        body.pdf-mode .toc a {{
            display: block !important;
            padding: 2.2mm 0 !important;
            margin: 0 !important;
            border: none !important;
            background: transparent !important;
            color: var(--text) !important;
            text-decoration: none !important;
            font-size: 10pt !important;
        }}

        body.pdf-mode .toc a::after {{
            content: " .... " target-counter(attr(href), page);
            float: right;
            color: var(--soft);
        }}

        body.pdf-mode .charts-grid {{
            display: grid !important;
            grid-template-columns: 1fr !important;
            gap: 6mm !important;
            margin: 0 0 10mm 0 !important;
            break-before: page;
            page-break-before: always;
        }}

        body.pdf-mode .chart-card {{
            padding: 5mm !important;
            break-inside: avoid;
            page-break-inside: avoid;
        }}

        body.pdf-mode .chart-card h3 {{
            color: #ffffff !important;
            font-size: 12pt !important;
            margin: 0 0 2.5mm 0 !important;
        }}

        body.pdf-mode .chart-card p {{
            color: var(--muted) !important;
            font-size: 9.5pt !important;
            margin: 0 0 3mm 0 !important;
        }}

        body.pdf-mode .chart-card img {{
            width: 100% !important;
            height: auto !important;
            border-radius: 12px !important;
            border: 1px solid rgba(255,255,255,0.10) !important;
            background: rgba(255,255,255,0.03) !important;
            object-fit: contain !important;
        }}

        body.pdf-mode .section {{
            padding: 6mm !important;
            margin: 0 0 6mm 0 !important;
            break-inside: auto !important;
            page-break-inside: auto !important;
        }}

        body.pdf-mode .section.major-section {{
            break-before: page;
            page-break-before: always;
            break-inside: avoid;
            page-break-inside: avoid;
        }}

        body.pdf-mode .section-header {{
            margin-bottom: 4mm !important;
            break-after: avoid;
            page-break-after: avoid;
        }}

        body.pdf-mode .section h2 {{
            color: #ffffff !important;
            font-size: 17pt !important;
            line-height: 1.15 !important;
            margin: 0 !important;
        }}

        body.pdf-mode .section p,
        body.pdf-mode .section li {{
            color: var(--text) !important;
            font-size: 10pt !important;
        }}

        body.pdf-mode .section strong {{
            color: #ffffff !important;
        }}

        body.pdf-mode .level-badge {{
            color: var(--accent-2) !important;
            background: rgba(255,255,255,0.06) !important;
            border: 1px solid rgba(255,255,255,0.12) !important;
        }}

        body.pdf-mode .math-block {{
            overflow: hidden !important;
            margin: 4mm 0 !important;
            padding: 4mm !important;
            border-radius: 14px !important;
            background: rgba(255,255,255,0.05) !important;
            border: 1px solid rgba(255,255,255,0.12) !important;
            break-inside: avoid;
            page-break-inside: avoid;
        }}

        body.pdf-mode .math-block img {{
            display: block !important;
            max-width: 100% !important;
            height: auto !important;
            margin: 0 auto !important;
            filter: none !important;
        }}

        body.pdf-mode .math-block code {{
            color: #ffffff !important;
            font-size: 10pt !important;
            white-space: pre-wrap !important;
            word-break: break-word !important;
        }}

        body.pdf-mode .callout {{
            border-left: 4px solid var(--accent) !important;
            background: rgba(139, 184, 255, 0.10) !important;
            border-radius: 14px !important;
            padding: 4mm !important;
            margin: 4mm 0 !important;
            color: var(--text) !important;
            break-inside: avoid;
            page-break-inside: avoid;
        }}

        body.pdf-mode .footer-note {{
            margin-top: 8mm !important;
            color: var(--muted) !important;
            font-size: 9pt !important;
            text-align: center !important;
        }}

        @media print {{
            body {{
                -webkit-print-color-adjust: exact;
                print-color-adjust: exact;
            }}
        }}
    </style>
    """