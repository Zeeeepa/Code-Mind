# Code-Mind

Code-Mind is a Codegen engine driven by itself. It provides a platform for analyzing, reflecting on, and improving codebases using AI-powered insights.

## Features

- **Project Management**: Create and manage coding projects with requirements tracking
- **Code Analysis**: Analyze repositories for code quality, architecture, and security issues
- **Project Reflection**: Generate AI-powered reflections on project requirements, implementation strategies, and technology stack recommendations

## Architecture

Code-Mind consists of two main components:

1. **FastAPI Backend**: Provides RESTful API endpoints for project management, code analysis, and reflection generation
2. **Streamlit Frontend**: Offers an intuitive UI for interacting with the Code-Mind features

## Getting Started

### Prerequisites

- Python 3.8+
- pip

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Zeeeepa/Code-Mind.git
   cd Code-Mind
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python -m src.code_mind.main
   ```

   This will start both the API server (on port 8000) and the UI server (on port 8501).

   You can also run them separately:
   ```bash
   # Run just the API
   python -m src.code_mind.main --api

   # Run just the UI
   python -m src.code_mind.main --ui
   ```

4. Access the UI in your browser at `http://localhost:8501`

## Project Structure

```
src/
  code_mind/
    api/            # FastAPI routes and endpoints
    ui/             # Streamlit UI components
    utils/          # Utility functions and helpers
    main.py         # Main entry point
```

## Configuration

Code-Mind can be configured using environment variables or a `.env` file:

```
CODE_MIND_API_URL=http://localhost:8000
CODE_MIND_OPENAI_API_KEY=your_openai_api_key
CODE_MIND_MODEL_NAME=gpt-4
CODE_MIND_DEBUG=False
CODE_MIND_LOG_LEVEL=INFO
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.
