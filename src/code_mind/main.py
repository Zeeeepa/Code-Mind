"""Main entry point for Code-Mind."""

import argparse
import sys
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


def run_ui(host: str, port: int) -> None:
    """Run the UI server.

    Args:
        host: The host to bind to.
        port: The port to run the server on.
    """
    logger.info(f"Starting UI server on {host}:{port}")
    # Streamlit is run via the command line
    # This is just a placeholder
    logger.info(
        f"To run the UI server, use: streamlit run src/code_mind/ui/app.py --server.address {host} --server.port {port}"
    )


def main() -> None:
    """Run the application."""
    args = parse_args()

    if not args.api and not args.ui:
        logger.error("Please specify at least one of --api or --ui")
        sys.exit(1)

    if args.api:
        run_api(args.host, args.api_port, args.reload)

    if args.ui:
        run_ui(args.host, args.ui_port)


if __name__ == "__main__":
    main()
