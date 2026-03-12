import streamlit as st

from src.theory import THEORY_TEXT


def render_theory_tab() -> None:
    st.subheader("Mathematical Theory")
    st.markdown(THEORY_TEXT)