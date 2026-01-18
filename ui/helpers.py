import streamlit as st

THEME = {
    "bg": "#0E0E10",
    "surface": "#151518",
    "border": "#26262B",
    "text_primary": "#EDEDED",
    "text_secondary": "#A1A1AA",
    "text_muted": "#71717A",
    "accent": "#10A37F",
}

def inject_global_styles():
    st.markdown(
        f"""
        <style>
        html, body, [class*="css"] {{
            background-color: {THEME['bg']};
            color: {THEME['text_primary']};
            font-family: Inter, -apple-system, BlinkMacSystemFont, Segoe UI, sans-serif;
        }}

        .block-container {{
            max-width: 760px;
            padding-top: 2rem;
        }}

        textarea, input {{
            background-color: {THEME['surface']} !important;
            color: {THEME['text_primary']} !important;
            border: 1px solid {THEME['border']} !important;
        }}

        button {{
            background-color: {THEME['accent']} !important;
            color: #0E0E10 !important;
            border-radius: 6px !important;
            font-weight: 500 !important;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )