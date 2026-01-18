import streamlit as st
from core.snapshot import get_timeline
from core.canon import get_canon

def render():
    st.markdown("### Timeline")
    st.caption("Narrative snapshots")

    canon = get_canon()
# timeline currently stored in snapshot adapter
    timeline = get_timeline()

    if not timeline:
        st.info("No snapshots recorded yet.")
        return

    for snap in timeline:
        st.json(snap)
