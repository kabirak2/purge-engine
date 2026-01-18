import streamlit as st
from core.replay import replay_last
from core.canon import get_canon

def render():
    st.markdown("### Debugger")
    st.caption("Replay and inspection")

    canon = get_canon()

    if st.button("Replay Last Commit"):
        result = replay_last(canon)
        st.json(result)
