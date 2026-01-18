import streamlit as st
import os
from core.canon import get_canon, save_current_canon
from core.project_store import DEFAULT_PROJECT

PROJECT_PATH = os.path.join("projects", DEFAULT_PROJECT)

def render():
    st.markdown("### Project")
    st.caption("Persistence and system control")

    canon = get_canon()

    st.markdown("#### Active project")
    st.code(PROJECT_PATH)

    st.divider()

    # ---------------- MANUAL SAVE ----------------
    if st.button("💾 Save project"):
        save_current_canon()
        st.success("Project saved to disk.")

    st.divider()

    # ---------------- RESET PROJECT ----------------
    st.markdown("#### Danger zone")
    st.warning("This will permanently reset the current project.")

    if st.button("🗑 Reset project"):
        if os.path.exists(PROJECT_PATH):
            os.remove(PROJECT_PATH)

        # Reset in-memory canon
        canon.truths.clear()
        canon.rules.clear()
        canon.events.clear()
        canon.event_log.clear()
        canon.snapshots.clear()

        save_current_canon()
        st.success("Project reset.")
