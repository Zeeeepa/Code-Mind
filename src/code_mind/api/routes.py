"""API routes for Code-Mind."""

from fastapi import FastAPI, Depends, HTTPException

from code_mind.core.analyzer import CodeAnalyzer
from code_mind.core.generator import CodeGenerator
from code_mind.models.code_generation import (
    CodeGenerationRequest,
    CodeGenerationResponse,
    CodeAnalysisRequest,
    CodeAnalysisResponse,
)
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


@app.post("/generate", response_model=CodeGenerationResponse)
async def generate_code(request: CodeGenerationRequest):
    """Generate code based on a natural language prompt.

    Args:
        request: Code generation request.

    Returns:
        Generated code and metadata.
    """
    logger.info(f"Received code generation request: {request.prompt}")
    
    try:
        generator = CodeGenerator()
        response = await generator.generate(request)
        return response
    except Exception as e:
        logger.error(f"Error generating code: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error generating code: {str(e)}")


@app.post("/analyze", response_model=CodeAnalysisResponse)
async def analyze_code(request: CodeAnalysisRequest):
    """Analyze code for quality, security, and performance issues.

    Args:
        request: Code analysis request.

    Returns:
        Analysis results and suggestions.
    """
    logger.info(f"Received code analysis request for {request.language} code")
    
    try:
        analyzer = CodeAnalyzer()
        response = await analyzer.analyze(request)
        return response
    except Exception as e:
        logger.error(f"Error analyzing code: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error analyzing code: {str(e)}")


@app.get("/models")
async def list_models():
    """List available models for code generation and analysis.

    Returns:
        List of available models.
    """
    # This is a placeholder implementation
    # In a real system, this would query available models from the LLM provider
    return {
        "models": [
            {
                "id": "gpt-4",
                "name": "GPT-4",
                "description": "Most capable model for code generation and analysis",
                "max_tokens": 8192,
            },
            {
                "id": "gpt-3.5-turbo",
                "name": "GPT-3.5 Turbo",
                "description": "Fast and efficient model for code generation",
                "max_tokens": 4096,
            },
            {
                "id": "codellama-34b",
                "name": "CodeLlama 34B",
                "description": "Open source model specialized for code generation",
                "max_tokens": 8192,
            },
        ]
    }
