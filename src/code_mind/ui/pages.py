"""UI pages for Code-Mind."""
import json
import time
from typing import Any, Dict, List, Optional, Union
import requests
import streamlit as st
from code_mind.ui.components import (
    render_analysis_form,
    render_analysis_results,
    render_project_form,
    render_project_info,
    render_reflection_form,
    render_reflection_results,
    render_requirement_form,
)
from code_mind.utils.config import get_settings
from code_mind.utils.logger import get_logger
logger = get_logger(__name__)

def projects_page() -> None:
    """Render the projects page."""
    st.title("Projects")
    # Initialize session state
    if "projects" not in st.session_state:
        st.session_state.projects = []
    if "current_project" not in st.session_state:
        st.session_state.current_project = None
    # Sidebar
    with st.sidebar:
        st.header("Projects")
        if st.session_state.projects:
            project_names = [project["name"] for project in st.session_state.projects]
            selected_project = st.selectbox(
                "Select a project", project_names, key="selected_project"
            )
            if selected_project:
                st.session_state.current_project = next(
                    (
                        project
                        for project in st.session_state.projects
                        if project["name"] == selected_project
                    ),
                    None,
                )
        else:
            st.info("No projects available. Create a new project to get started.")
        if st.button("Create New Project"):
            st.session_state.current_project = None
            st.experimental_rerun()
    # Main content
    if st.session_state.current_project:
        render_project_info(st.session_state.current_project)
        with st.expander("Add Requirement"):
            render_requirement_form(st.session_state.current_project)
    else:
        render_project_form()

def analysis_page() -> None:
    """Render the analysis page."""
    st.title("Analysis")
    # Initialize session state
    if "current_project" not in st.session_state:
        st.session_state.current_project = None
    if "analysis_results" not in st.session_state:
        st.session_state.analysis_results = None
    # Sidebar
    with st.sidebar:
        st.header("Projects")
        if "projects" in st.session_state and st.session_state.projects:
            project_names = [project["name"] for project in st.session_state.projects]
            selected_project = st.selectbox(
                "Select a project", project_names, key="selected_project"
            )
            if selected_project:
                st.session_state.current_project = next(
                    (
                        project
                        for project in st.session_state.projects
                        if project["name"] == selected_project
                    ),
                    None,
                )
        else:
            st.info("No projects available. Create a new project to get started.")
    # Main content
    if not st.session_state.current_project:
        st.warning("Please select a project first.")
        return
    render_analysis_form(st.session_state.current_project)
    if st.session_state.analysis_results:
        render_analysis_results(st.session_state.analysis_results)

def reflection_page() -> None:
    """Render the reflection page."""
    st.title("Reflection")
    # Initialize session state
    if "current_project" not in st.session_state:
        st.session_state.current_project = None
    if "reflection_results" not in st.session_state:
        st.session_state.reflection_results = None
    # Sidebar
    with st.sidebar:
        st.header("Projects")
        if "projects" in st.session_state and st.session_state.projects:
            project_names = [project["name"] for project in st.session_state.projects]
            selected_project = st.selectbox(
                "Select a project", project_names, key="selected_project"
            )
            if selected_project:
                st.session_state.current_project = next(
                    (
                        project
                        for project in st.session_state.projects
                        if project["name"] == selected_project
                    ),
                    None,
                )
        else:
            st.info("No projects available. Create a new project to get started.")
    # Main content
    if not st.session_state.current_project:
        st.warning("Please select a project first.")
        return
    render_reflection_form(st.session_state.current_project)
    if st.session_state.reflection_results:
        render_reflection_results(st.session_state.reflection_results)
