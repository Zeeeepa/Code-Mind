"""Streamlit UI for Code-Mind."""
import streamlit as st
from code_mind.ui.pages import projects_page, analysis_page, reflection_page
from code_mind.utils.logger import get_logger

logger = get_logger(__name__)

st.set_page_config(
    page_title="Code-Mind",
    page_icon="🧠",
    layout="wide",
)

# Initialize session state
if "page" not in st.session_state:
    st.session_state.page = "projects"

# Sidebar navigation
with st.sidebar:
    st.title("Code-Mind")
    st.caption("Codegen engine driven by itself")
    
    st.header("Navigation")
    if st.button("Projects", use_container_width=True):
        st.session_state.page = "projects"
    if st.button("Analysis", use_container_width=True):
        st.session_state.page = "analysis"
    if st.button("Reflection", use_container_width=True):
        st.session_state.page = "reflection"
    
    st.divider()

# Render the selected page
if st.session_state.page == "projects":
    projects_page()
elif st.session_state.page == "analysis":
    analysis_page()
elif st.session_state.page == "reflection":
    reflection_page()
