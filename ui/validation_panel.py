import streamlit as st
from core.validator import validate_state
from core.canon import get_canon

def render():
    st.markdown("### Validation")
    st.caption("Canon integrity checks")

    canon = get_canon()

    if st.button("Run Validation"):
        result = validate_state(canon)

        st.markdown(f"**Status:** {result['status']}")

        if result["blocked"]:
            st.error("Blocked rules")
            st.json(result["blocked"])

        if result["warned"]:
            st.warning("Warnings")
            st.json(result["warned"])

        if not result["blocked"] and not result["warned"]:
            st.success("Canon is consistent")
