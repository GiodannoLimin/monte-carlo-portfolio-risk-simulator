import streamlit as st

from src.reference_content import REFERENCE_SECTIONS


def render_reference_tab() -> None:
    st.subheader("Reference")

    st.markdown(
        """
This section contains the technical background behind the simulator.

It is intended for users who want formulas, modeling assumptions,
and quantitative definitions.
"""
    )

    for section in REFERENCE_SECTIONS:
        st.markdown(f"### {section['section']}")

        for item in section["items"]:
            with st.expander(item["title"]):
                st.markdown(item["body"])

        st.markdown("")