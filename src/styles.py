import streamlit as st


def inject_global_styles() -> None:
    st.markdown(
        """
        <style>
        /* ===== App-wide gradient background ===== */
        html, body, #root, .stApp {
            background: linear-gradient(135deg, #060816 0%, #0c1230 45%, #211a52 100%) !important;
            color: white !important;
        }

        body {
            overflow-x: hidden;
        }

        /* Main app containers */
        [data-testid="stAppViewContainer"] {
            background: linear-gradient(135deg, #060816 0%, #0c1230 45%, #211a52 100%) !important;
        }

        [data-testid="stMain"] {
            background: transparent !important;
        }

        [data-testid="stMainBlockContainer"] {
            background: transparent !important;
            padding-top: 2rem;
            padding-bottom: 6rem;
            max-width: 1400px;
        }

        /* Extra wrappers Streamlit sometimes uses */
        .main,
        .block-container,
        .stApp > div,
        .stAppViewContainer,
        .appview-container,
        section.main {
            background: transparent !important;
        }

        /* Force bottom filler area to dark background */
        div[data-testid="stVerticalBlock"] {
            background: transparent !important;
        }

        div[data-testid="stVerticalBlockBorderWrapper"] {
            background: transparent !important;
        }

        div[data-testid="element-container"] {
            background: transparent !important;
        }

        /* Header / toolbar */
        [data-testid="stHeader"],
        [data-testid="stToolbar"],
        header {
            background: transparent !important;
        }

        footer {
            background: transparent !important;
        }

        /* Sidebar */
        section[data-testid="stSidebar"] {
            background: rgba(10, 14, 40, 0.95) !important;
            border-right: 1px solid rgba(255,255,255,0.08);
        }

        /* Text */
        h1, h2, h3, h4, h5, h6, p, label, span {
            color: white !important;
        }

        /* Metric cards */
        [data-testid="stMetric"] {
            background: rgba(255,255,255,0.05) !important;
            border: 1px solid rgba(255,255,255,0.10);
            padding: 14px;
            border-radius: 16px;
        }

        /* Tables */
        [data-testid="stDataFrame"],
        [data-testid="stTable"] {
            background: rgba(255,255,255,0.03) !important;
            border-radius: 14px;
            overflow: hidden;
        }

        /* Tabs */
        [data-baseweb="tab-list"] {
            gap: 8px;
        }

        [data-baseweb="tab"] {
            background: rgba(255,255,255,0.04) !important;
            border-radius: 12px 12px 0 0;
            color: white !important;
            padding: 10px 18px;
        }

        [aria-selected="true"] {
            background: rgba(255,255,255,0.10) !important;
        }

        /* Inputs */
        .stTextInput input,
        .stNumberInput input,
        .stTextArea textarea {
            background-color: rgba(255,255,255,0.04) !important;
            color: white !important;
        }

        .stSelectbox div[data-baseweb="select"],
        .stMultiSelect div[data-baseweb="select"] {
            background-color: rgba(255,255,255,0.04) !important;
            color: white !important;
        }

        /* Buttons */
        .stButton > button {
            border-radius: 12px;
            border: 1px solid rgba(255,255,255,0.12);
            background: rgba(255,255,255,0.06);
            color: white;
        }

        .stButton > button:hover {
            border-color: rgba(255,255,255,0.25);
            background: rgba(255,255,255,0.10);
            color: white;
        }

        /* Custom cards */
        .overview-card {
            padding: 18px;
            border-radius: 18px;
            background: rgba(255,255,255,0.05);
            border: 1px solid rgba(255,255,255,0.10);
            margin-bottom: 18px;
        }

        .section-note {
            font-size: 0.95rem;
            opacity: 0.9;
            margin-top: -4px;
            margin-bottom: 12px;
        }

        /* Plotly containers */
        div[data-testid="stPlotlyChart"] {
            background: rgba(255,255,255,0.03) !important;
            padding: 14px !important;
            border-radius: 14px;
            border: 1px solid rgba(255,255,255,0.06);
            overflow: visible !important;
        }

        /* Prevent chart clipping */
        div[data-testid="stPlotlyChart"] > div {
            overflow: visible !important;
        }

        .js-plotly-plot,
        .plotly,
        .plot-container,
        .svg-container {
            overflow: visible !important;
        }

        /* Expanders */
        details {
            background: rgba(255,255,255,0.03);
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 14px;
            padding: 8px 12px;
        }

        /* Hide any accidental white fullscreen area below content */
        .stApp::before {
            content: "";
            position: fixed;
            inset: 0;
            background: linear-gradient(135deg, #060816 0%, #0c1230 45%, #211a52 100%);
            z-index: -9999;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )