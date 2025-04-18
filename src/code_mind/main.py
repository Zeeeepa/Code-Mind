"""Main entry point for Code-Mind."""

import argparse
import os
import subprocess
import sys
import threading
from typing import Any, Dict, List, Optional, Union

import uvicorn

from code_mind.api.routes import app as api_app
from code_mind.utils.logger import get_logger, setup_logging

logger = get_logger(__name__)

# Set up logging
setup_logging()


def parse_args() -> argparse.Namespace:
    """Parse command line arguments.

    Returns:
        argparse.Namespace: The parsed arguments.
    """
    parser = argparse.ArgumentParser(description="Code-Mind: Codegen engine driven by itself")
    parser.add_argument(
        "--api", action="store_true", help="Run the API server"
    )
    parser.add_argument(
        "--ui", action="store_true", help="Run the UI server"
    )
    parser.add_argument(
        "--host", type=str, default="0.0.0.0", help="Host to bind to"
    )
    parser.add_argument(
        "--api-port", type=int, default=8000, help="Port to run the API server on"
    )
    parser.add_argument(
        "--ui-port", type=int, default=8501, help="Port to run the UI server on"
    )
    parser.add_argument(
        "--reload", action="store_true", help="Enable auto-reload"
    )
    return parser.parse_args()


def run_api(host: str, port: int, reload: bool) -> None:
    """Run the API server.

    Args:
        host: The host to bind to.
        port: The port to run the server on.
        reload: Whether to enable auto-reload.
    """
    logger.info(f"Starting API server on {host}:{port}")
    uvicorn.run(
        "code_mind.api.routes:app",
        host=host,
        port=port,
        reload=reload,
    )


def run_ui(host: str, port: int, reload: bool) -> None:
    """Run the UI server using Streamlit.

    Args:
        host: The host to bind to.
        port: The port to run the server on.
        reload: Whether to enable auto-reload.
    """
    logger.info(f"Starting UI server on {host}:{port}")
    
    # Construct the command to run Streamlit
    cmd = [
        "streamlit", "run", 
        os.path.join(os.path.dirname(__file__), "ui", "app.py"),
        "--server.address", host,
        "--server.port", str(port)
    ]
    
    # Add reload flag if specified
    if reload:
        cmd.append("--server.runOnSave=true")
    
    # Run Streamlit as a subprocess
    try:
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
        )
        
        # Log Streamlit output
        for line in process.stdout:
            logger.info(f"Streamlit: {line.strip()}")
            
    except Exception as e:
        logger.error(f"Error starting Streamlit: {e}")
        raise


def main() -> None:
    """Run the application."""
    args = parse_args()

    if not args.api and not args.ui:
        # Default to running both if no flags are specified
        args.api = True
        args.ui = True

    # Run API and UI in separate threads if both are requested
    if args.api and args.ui:
        api_thread = threading.Thread(
            target=run_api,
            args=(args.host, args.api_port, args.reload),
            daemon=True
        )
        api_thread.start()
        
        # Run UI in the main thread
        run_ui(args.host, args.ui_port, args.reload)
    elif args.api:
        # Run just the API
        run_api(args.host, args.api_port, args.reload)
    elif args.ui:
        # Run just the UI
        run_ui(args.host, args.ui_port, args.reload)


if __name__ == "__main__":
    main()
