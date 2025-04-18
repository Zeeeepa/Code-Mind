"""Streamlit UI for Code-Mind."""

import json
import requests
from typing import Dict, Any, List

import streamlit as st

from code_mind.models.code_generation import ProgrammingLanguage
from code_mind.utils.logger import get_logger

logger = get_logger(__name__)

# Set page configuration
st.set_page_config(
    page_title="Code-Mind",
    page_icon="🧠",
    layout="wide",
)

# API URL (default to localhost if running locally)
API_URL = "http://localhost:8000"


def call_api(endpoint: str, method: str = "GET", data: Dict[str, Any] = None) -> Dict[str, Any]:
    """Call the Code-Mind API.
    
    Args:
        endpoint: API endpoint to call.
        method: HTTP method to use.
        data: Data to send in the request body.
        
    Returns:
        API response as a dictionary.
    """
    url = f"{API_URL}/{endpoint.lstrip('/')}"
    
    try:
        if method.upper() == "GET":
            response = requests.get(url)
        elif method.upper() == "POST":
            response = requests.post(url, json=data)
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")
        
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"API call failed: {str(e)}")
        st.error(f"API call failed: {str(e)}")
        return {"error": str(e)}


def main():
    """Main function for the Streamlit app."""
    st.title("Code-Mind")
    st.subheader("Codegen engine driven by itself")
    
    # Create tabs for different functionality
    tab1, tab2, tab3 = st.tabs(["Code Generation", "Code Analysis", "About"])
    
    # Code Generation Tab
    with tab1:
        st.header("Generate Code from Natural Language")
        
        # Input form for code generation
        with st.form("code_generation_form"):
            prompt = st.text_area(
                "Describe what you want to build",
                placeholder="E.g., Create a function that calculates the Fibonacci sequence",
                height=100,
            )
            
            col1, col2 = st.columns(2)
            
            with col1:
                language = st.selectbox(
                    "Programming Language",
                    options=[lang.value for lang in ProgrammingLanguage],
                    index=0,
                )
            
            with col2:
                model = st.selectbox(
                    "Model",
                    options=["gpt-4", "gpt-3.5-turbo", "codellama-34b"],
                    index=0,
                )
            
            advanced_options = st.expander("Advanced Options")
            
            with advanced_options:
                max_tokens = st.slider(
                    "Maximum Tokens",
                    min_value=100,
                    max_value=4000,
                    value=1000,
                    step=100,
                )
                
                temperature = st.slider(
                    "Temperature",
                    min_value=0.0,
                    max_value=1.0,
                    value=0.7,
                    step=0.1,
                )
                
                context = st.text_area(
                    "Additional Context",
                    placeholder="Any additional context to help with code generation",
                    height=100,
                )
            
            submitted = st.form_submit_button("Generate Code")
        
        if submitted and prompt:
            with st.spinner("Generating code..."):
                # Prepare request data
                request_data = {
                    "prompt": prompt,
                    "language": language,
                    "max_tokens": max_tokens,
                    "temperature": temperature,
                    "model": model,
                }
                
                if context:
                    request_data["context"] = context
                
                # Call the API
                try:
                    response = call_api("generate", method="POST", data=request_data)
                    
                    if "error" not in response:
                        st.success("Code generated successfully!")
                        
                        # Display the generated code
                        st.code(response["code"], language=language)
                        
                        # Display metadata
                        col1, col2, col3 = st.columns(3)
                        col1.metric("Model Used", response["model_used"])
                        col2.metric("Execution Time", f"{response['execution_time_ms']} ms")
                        col3.metric("Token Count", response["token_count"])
                        
                        # Display explanation if available
                        if response.get("explanation"):
                            st.subheader("Explanation")
                            st.write(response["explanation"])
                    else:
                        st.error(f"Error: {response['error']}")
                except Exception as e:
                    st.error(f"Failed to generate code: {str(e)}")
                    logger.error(f"Code generation failed: {str(e)}")
    
    # Code Analysis Tab
    with tab2:
        st.header("Analyze Code Quality, Security, and Performance")
        
        # Input form for code analysis
        with st.form("code_analysis_form"):
            code = st.text_area(
                "Enter code to analyze",
                placeholder="Paste your code here...",
                height=200,
            )
            
            col1, col2 = st.columns(2)
            
            with col1:
                analysis_language = st.selectbox(
                    "Programming Language",
                    options=[lang.value for lang in ProgrammingLanguage],
                    index=0,
                    key="analysis_language",
                )
            
            with col2:
                analysis_model = st.selectbox(
                    "Model",
                    options=["gpt-4", "gpt-3.5-turbo", "codellama-34b"],
                    index=0,
                    key="analysis_model",
                )
            
            analysis_types = st.multiselect(
                "Analysis Types",
                options=["quality", "security", "performance"],
                default=["quality", "security", "performance"],
            )
            
            analyze_button = st.form_submit_button("Analyze Code")
        
        if analyze_button and code:
            with st.spinner("Analyzing code..."):
                # Prepare request data
                request_data = {
                    "code": code,
                    "language": analysis_language,
                    "analysis_type": analysis_types,
                    "model": analysis_model,
                }
                
                # Call the API
                try:
                    response = call_api("analyze", method="POST", data=request_data)
                    
                    if "error" not in response:
                        st.success("Code analyzed successfully!")
                        
                        # Display metadata
                        col1, col2 = st.columns(2)
                        col1.metric("Model Used", response["model_used"])
                        col2.metric("Execution Time", f"{response['execution_time_ms']} ms")
                        
                        # Display analysis results
                        st.subheader("Analysis Results")
                        
                        for category, issues in response["analysis_results"].items():
                            with st.expander(f"{category.title()} ({len(issues)} issues)"):
                                for issue in issues:
                                    severity_emoji = "🟢" if issue["severity"] == 1 else "🟠" if issue["severity"] == 2 else "🔴"
                                    st.markdown(f"{severity_emoji} **{issue['type']}** (Line {issue['line']}): {issue['message']}")
                        
                        # Display suggestions
                        st.subheader("Suggestions")
                        for suggestion in response["suggestions"]:
                            severity_emoji = "🟢" if suggestion["severity"] == 1 else "🟠" if suggestion["severity"] == 2 else "🔴"
                            st.markdown(f"{severity_emoji} **{suggestion['type']}** (Line {suggestion['line']}): {suggestion['message']}")
                    else:
                        st.error(f"Error: {response['error']}")
                except Exception as e:
                    st.error(f"Failed to analyze code: {str(e)}")
                    logger.error(f"Code analysis failed: {str(e)}")
    
    # About Tab
    with tab3:
        st.header("About Code-Mind")
        
        st.write(
            """
            Code-Mind is a self-improving code generation engine built with Python, FastAPI, and Streamlit.
            
            ### Features
            
            - Generate code from natural language descriptions
            - Analyze code for quality, security, and performance issues
            - Support for multiple programming languages
            - Integration with state-of-the-art language models
            
            ### How It Works
            
            Code-Mind uses large language models to understand natural language prompts and generate
            high-quality code. It can also analyze existing code to identify issues and suggest improvements.
            
            ### Getting Started
            
            To use Code-Mind, simply:
            
            1. Navigate to the "Code Generation" tab to create new code
            2. Navigate to the "Code Analysis" tab to analyze existing code
            3. Explore the various options to customize the output
            
            ### API Access
            
            Code-Mind also provides a REST API for programmatic access. The API documentation is available at:
            
            ```
            http://localhost:8000/docs
            ```
            """
        )


# Add a sidebar
with st.sidebar:
    st.header("Options")
    
    # API URL configuration
    api_url = st.text_input("API URL", value=API_URL)
    if api_url != API_URL:
        API_URL = api_url
        st.success(f"API URL updated to: {API_URL}")
    
    # Check API connection
    if st.button("Check API Connection"):
        try:
            response = call_api("health")
            if response.get("status") == "healthy":
                st.success("API connection successful!")
            else:
                st.error("API connection failed!")
        except Exception as e:
            st.error(f"API connection failed: {str(e)}")
    
    st.divider()
    
    # About section in sidebar
    st.write("Code-Mind v0.1.0")
    st.write("A Codegen engine driven by itself")


if __name__ == "__main__":
    main()
