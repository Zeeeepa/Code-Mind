"""Models for code generation and analysis."""

from enum import Enum
from typing import Dict, List, Optional, Union

from pydantic import BaseModel, Field


class ProgrammingLanguage(str, Enum):
    PYTHON = "python"
    JAVASCRIPT = "javascript"
    TYPESCRIPT = "typescript"
    JAVA = "java"
    CSHARP = "csharp"
    GO = "go"
    RUST = "rust"
    CPP = "cpp"
    OTHER = "other"


class CodeGenerationRequest(BaseModel):
    prompt: str = Field(..., description="Natural language prompt for code generation")
    language: ProgrammingLanguage = Field(
        default=ProgrammingLanguage.PYTHON, description="Target programming language"
    )
    context: Optional[str] = Field(
        default=None, description="Additional context for code generation"
    )
    max_tokens: int = Field(
        default=1000, description="Maximum number of tokens to generate"
    )
    temperature: float = Field(
        default=0.7, description="Sampling temperature (0.0 to 1.0)"
    )
    model: Optional[str] = Field(
        default=None, description="Model to use for generation (overrides default)"
    )


class CodeGenerationResponse(BaseModel):
    code: str = Field(..., description="Generated code")
    language: ProgrammingLanguage = Field(..., description="Programming language")
    model_used: str = Field(..., description="Model used for generation")
    execution_time_ms: int = Field(..., description="Execution time in milliseconds")
    token_count: int = Field(..., description="Number of tokens in the generated code")
    explanation: Optional[str] = Field(
        default=None, description="Explanation of the generated code"
    )


class CodeAnalysisRequest(BaseModel):
    code: str = Field(..., description="Code to analyze")
    language: ProgrammingLanguage = Field(
        default=ProgrammingLanguage.PYTHON, description="Programming language"
    )
    analysis_type: List[str] = Field(
        default=["quality", "security", "performance"],
        description="Types of analysis to perform",
    )
    model: Optional[str] = Field(
        default=None, description="Model to use for analysis (overrides default)"
    )


class CodeAnalysisResponse(BaseModel):
    code: str = Field(..., description="Analyzed code")
    language: ProgrammingLanguage = Field(..., description="Programming language")
    model_used: str = Field(..., description="Model used for analysis")
    execution_time_ms: int = Field(..., description="Execution time in milliseconds")
    analysis_results: Dict[str, List[Dict[str, Union[str, int]]]] = Field(
        ..., description="Analysis results by category"
    )
    suggestions: List[Dict[str, Union[str, int]]] = Field(
        ..., description="Improvement suggestions"
    )
