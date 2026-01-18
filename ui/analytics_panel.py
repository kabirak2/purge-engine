import streamlit as st
from core.analytics import get_metrics
from core.canon import get_canon

def render():
    st.markdown("### Analytics")
    st.caption("Narrative metrics")

    canon = get_canon()
    metrics = get_metrics(canon)

    st.json(metrics)
