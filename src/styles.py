import streamlit as st


def inject_global_styles() -> None:
    st.markdown(
        """
        <style>
        .stApp {
            background: linear-gradient(135deg, #060816 0%, #0c1230 45%, #211a52 100%);
            color: white;
        }
        [data-testid="stMetric"] {
            background: rgba(255,255,255,0.05);
            border: 1px solid rgba(255,255,255,0.10);
            padding: 14px;
            border-radius: 16px;
        }
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
        </style>
        """,
        unsafe_allow_html=True
    )