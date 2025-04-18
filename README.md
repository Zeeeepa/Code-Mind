# Code-Mind

Code-Mind is a Codegen engine driven by itself - a self-improving code generation system.

## Features

- API server for code generation and analysis
- UI interface for interacting with the system
- Extensible architecture for adding new capabilities

## Installation

```bash
# Clone the repository
git clone https://github.com/Zeeeepa/Code-Mind.git
cd Code-Mind

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Running the API Server

```bash
python -m src.code_mind.main --api --host 0.0.0.0 --api-port 8000 --reload
```

### Running the UI

```bash
python -m src.code_mind.main --ui --host 0.0.0.0 --ui-port 8501
```

Or directly with Streamlit:

```bash
streamlit run src/code_mind/ui/app.py --server.address 0.0.0.0 --server.port 8501
```

### Running Both API and UI

```bash
python -m src.code_mind.main --api --ui --host 0.0.0.0 --api-port 8000 --ui-port 8501 --reload
```

## Project Structure

```
src/
  code_mind/
    api/            # FastAPI routes and endpoints
    ui/             # Streamlit UI components
    utils/          # Utility functions and helpers
    main.py         # Main entry point
```

## License

MIT
