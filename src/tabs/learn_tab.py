import streamlit as st

from src.ui_text import LEARN_CONTENT


def render_learn_tab() -> None:
    st.subheader("Beginner Guide")
    st.markdown(
        """
This section explains the simulator in simple language for beginners.
You do not need a finance background to follow it.
        """
    )

    for item in LEARN_CONTENT:
        with st.expander(item["title"]):
            st.write(item["body"])