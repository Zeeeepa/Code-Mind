"""UI components for Code-Mind."""
import json
import time
from typing import Any, Dict, List, Optional, Union
import requests
import streamlit as st
from code_mind.utils.config import get_settings
from code_mind.utils.logger import get_logger

logger = get_logger(__name__)
settings = get_settings()

def render_project_form() -> None:
    """Render the project creation form."""
    st.header("Create New Project")
    with st.form("project_form"):
        name = st.text_input("Project Name", key="project_name")
        description = st.text_area("Project Description", key="project_description")
        submit = st.form_submit_button("Create Project")
        
        if submit and name:
            try:
                # Create project via API
                response = requests.post(
                    f"{settings.api_url}/projects",
                    json={"name": name, "description": description},
                    timeout=10,
                )
                response.raise_for_status()
                project = response.json()
                
                # Update session state
                if "projects" not in st.session_state:
                    st.session_state.projects = []
                st.session_state.projects.append(project)
                st.session_state.current_project = project
                st.success(f"Project '{name}' created successfully!")
                time.sleep(1)
                st.experimental_rerun()
            except Exception as e:
                logger.error(f"Error creating project: {e}")
                st.error(f"Error creating project: {str(e)}")

def render_project_info(project: Dict[str, Any]) -> None:
    """Render project information."""
    st.header(project["name"])
    st.write(project["description"])
    
    # Display requirements if any
    if "requirements" in project and project["requirements"]:
        st.subheader("Requirements")
        for i, req in enumerate(project["requirements"]):
            with st.expander(f"{i+1}. {req['title']}"):
                st.write(req["description"])
                st.caption(f"Priority: {req['priority']}")

def render_requirement_form(project: Dict[str, Any]) -> None:
    """Render the requirement creation form."""
    with st.form("requirement_form"):
        title = st.text_input("Requirement Title", key="req_title")
        description = st.text_area("Requirement Description", key="req_description")
        priority = st.selectbox(
            "Priority", 
            options=["Low", "Medium", "High", "Critical"],
            index=1,
            key="req_priority"
        )
        submit = st.form_submit_button("Add Requirement")
        
        if submit and title:
            try:
                # Create requirement via API
                response = requests.post(
                    f"{settings.api_url}/projects/{project['id']}/requirements",
                    json={
                        "title": title,
                        "description": description,
                        "priority": priority
                    },
                    timeout=10,
                )
                response.raise_for_status()
                updated_project = response.json()
                
                # Update session state
                for i, p in enumerate(st.session_state.projects):
                    if p["id"] == project["id"]:
                        st.session_state.projects[i] = updated_project
                        break
                st.session_state.current_project = updated_project
                st.success(f"Requirement '{title}' added successfully!")
                time.sleep(1)
                st.experimental_rerun()
            except Exception as e:
                logger.error(f"Error adding requirement: {e}")
                st.error(f"Error adding requirement: {str(e)}")

def render_analysis_form(project: Dict[str, Any]) -> None:
    """Render the code analysis form."""
    st.header(f"Analyze Project: {project['name']}")
    
    with st.form("analysis_form"):
        repo_url = st.text_input("Repository URL", key="repo_url")
        analysis_type = st.selectbox(
            "Analysis Type",
            options=["Code Quality", "Architecture", "Security", "Comprehensive"],
            index=3,
            key="analysis_type"
        )
        submit = st.form_submit_button("Start Analysis")
        
        if submit and repo_url:
            with st.spinner("Analyzing code..."):
                try:
                    # Request analysis via API
                    response = requests.post(
                        f"{settings.api_url}/projects/{project['id']}/analyze",
                        json={
                            "repo_url": repo_url,
                            "analysis_type": analysis_type
                        },
                        timeout=60,  # Longer timeout for analysis
                    )
                    response.raise_for_status()
                    results = response.json()
                    
                    # Update session state
                    st.session_state.analysis_results = results
                    st.success("Analysis completed successfully!")
                except Exception as e:
                    logger.error(f"Error during analysis: {e}")
                    st.error(f"Error during analysis: {str(e)}")

def render_analysis_results(results: Dict[str, Any]) -> None:
    """Render code analysis results."""
    st.header("Analysis Results")
    
    # Summary
    st.subheader("Summary")
    st.write(results.get("summary", "No summary available."))
    
    # Metrics
    if "metrics" in results:
        st.subheader("Metrics")
        metrics = results["metrics"]
        cols = st.columns(len(metrics))
        for i, (key, value) in enumerate(metrics.items()):
            with cols[i]:
                st.metric(label=key.replace("_", " ").title(), value=value)
    
    # Findings
    if "findings" in results:
        st.subheader("Findings")
        for category, items in results["findings"].items():
            with st.expander(f"{category.replace('_', ' ').title()} ({len(items)})"):
                for item in items:
                    st.markdown(f"**{item['title']}**")
                    st.write(item["description"])
                    if "location" in item:
                        st.code(f"{item['location']['file']}:{item['location']['line']}")
                    st.markdown("---")

def render_reflection_form(project: Dict[str, Any]) -> None:
    """Render the reflection form."""
    st.header(f"Project Reflection: {project['name']}")
    
    with st.form("reflection_form"):
        reflection_type = st.selectbox(
            "Reflection Type",
            options=["Requirements Analysis", "Implementation Strategy", "Technology Stack", "Custom"],
            index=0,
            key="reflection_type"
        )
        
        custom_prompt = ""
        if reflection_type == "Custom":
            custom_prompt = st.text_area(
                "Custom Reflection Prompt", 
                key="custom_prompt",
                help="Enter a specific question or topic for reflection"
            )
        
        submit = st.form_submit_button("Generate Reflection")
        
        if submit:
            with st.spinner("Generating reflection..."):
                try:
                    # Request reflection via API
                    payload = {
                        "reflection_type": reflection_type,
                    }
                    if custom_prompt:
                        payload["custom_prompt"] = custom_prompt
                        
                    response = requests.post(
                        f"{settings.api_url}/projects/{project['id']}/reflect",
                        json=payload,
                        timeout=30,
                    )
                    response.raise_for_status()
                    results = response.json()
                    
                    # Update session state
                    st.session_state.reflection_results = results
                    st.success("Reflection generated successfully!")
                except Exception as e:
                    logger.error(f"Error generating reflection: {e}")
                    st.error(f"Error generating reflection: {str(e)}")

def render_reflection_results(results: Dict[str, Any]) -> None:
    """Render reflection results."""
    st.header("Reflection Results")
    
    # Main reflection
    st.markdown(results.get("reflection", "No reflection available."))
    
    # Recommendations
    if "recommendations" in results:
        st.subheader("Recommendations")
        for rec in results["recommendations"]:
            with st.expander(rec["title"]):
                st.write(rec["description"])
                if "action_items" in rec:
                    st.subheader("Action Items")
                    for item in rec["action_items"]:
                        st.markdown(f"- {item}")
