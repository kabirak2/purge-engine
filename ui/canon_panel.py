import streamlit as st
from core.canon import get_canon

def render():
    st.markdown("### Canon")
    st.caption("Current ground truth")

    canon = get_canon()
    st.json(canon.to_dict())
