import streamlit as st
from core.versemind import run_versemind
from core.canon import get_canon, save_current_canon
from core.snapshot import record_snapshot

def render():
    st.markdown("### VerseMind")
    st.caption("Narrative proposal engine")

    canon = get_canon()

    intent = st.text_area(
        "Describe intent",
        height=140,
        placeholder="Describe what should happen in the story…"
    )

    if st.button("Propose"):
        if not intent.strip():
            st.warning("Please enter an intent.")
            return

        with st.spinner("Reasoning…"):
            proposal = run_versemind(intent, canon)

        st.markdown("#### Proposal")
        st.json(proposal)

        if proposal.get("type") == "event":
            payload = proposal.get("payload", {})
            canon.add_event(payload)
            record_snapshot(canon, payload.get("act", 0))
            save_current_canon()
            st.success("Event committed and saved.")
        else:
            st.info("Suggestion generated (not committed).")
