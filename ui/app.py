import sys
import os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import streamlit as st
from ui.helpers import inject_global_styles

from ui.versemind_panel import render as versemind
from ui.timeline_panel import render as timeline
from ui.rule_editor import render as rules
from ui.validation_panel import render as validation
from ui.analytics_panel import render as analytics
from ui.debugger_panel import render as debugger
from ui.canon_panel import render as canon
from ui.paradox_panel import render as paradox
from ui.project_panel import render as project

def main():
    st.set_page_config(page_title="PURGE Console", layout="centered")
    inject_global_styles()

    st.markdown("## PURGE AI Console")
    st.caption("Internal research & narrative intelligence system")

    panel = st.sidebar.radio(
    "Tools",
        [
            "Project",
            "Rules",
            "VerseMind",
            "Paradox",
            "Debugger",
            "Analytics",
            "Validation",
            "Canon",
            "Timeline"
        ],
    )


    if panel == "VerseMind":
        versemind()
    elif panel == "Timeline":
        timeline()
    elif panel == "Rules":
        rules()
    elif panel == "Validation":
        validation()
    elif panel == "Analytics":
        analytics()
    elif panel == "Debugger":
        debugger()
    elif panel == "Canon":
        canon()
    elif panel == "Paradox":
        paradox()
    elif panel == "Project":
        project()

if __name__ == "__main__":
    main()
