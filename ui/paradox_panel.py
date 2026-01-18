import streamlit as st
from core.paradox import detect_paradoxes
from core.canon import get_canon

def render():
    st.markdown("### Paradox Detector")
    st.caption("Logical inconsistencies")

    canon = get_canon()
    paradoxes = detect_paradoxes(canon)

    if not paradoxes:
        st.success("No paradoxes detected")
    else:
        st.warning(f"{len(paradoxes)} paradoxes found")
        st.json(paradoxes)
