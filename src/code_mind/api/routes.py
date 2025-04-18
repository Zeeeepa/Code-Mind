"""API routes for Code-Mind."""

from fastapi import FastAPI

from code_mind.utils.logger import get_logger

logger = get_logger(__name__)

app = FastAPI(title="Code-Mind API", description="API for Code-Mind")


@app.get("/")
async def root():
    """Root endpoint.

    Returns:
        A welcome message.
    """
    return {"message": "Welcome to Code-Mind API"}


@app.get("/health")
async def health():
    """Health check endpoint.

    Returns:
        The health status of the API.
    """
    return {"status": "healthy"}
