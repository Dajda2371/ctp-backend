# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a FastAPI backend project for CTP. The codebase uses Python 3.7+ with FastAPI as the web framework and Pydantic for data validation.

## Essential Commands

### Setup
```bash
# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
source .venv/bin/activate  # Mac/Linux
.venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```

### Development
```bash
# Run development server with auto-reload
uvicorn main:app --reload

# The API will be available at http://127.0.0.1:8000
# Interactive docs at http://127.0.0.1:8000/docs
```

## Architecture

### Application Structure

The application follows a modular routing architecture:

- **Entry Point**: `main.py` initializes the FastAPI app and registers routers
- **Routing Pattern**: Endpoints are organized by HTTP method, then by feature area
  - Structure: `api/{http_method}/{feature}/{endpoint}.py`
  - Example: `api/post/auth/login.py` contains POST endpoints for authentication
  - Each endpoint module exports a router that gets included in the main app with appropriate prefixes

### Router Registration Pattern

In `main.py`, routers are registered using:
```python
app.include_router(module.router, prefix="/prefix")
```

The prefix combines with the router's endpoint paths to create the full URL path. For example:
- Router in `api/post/auth/login.py` with `@router.post("/login")`
- Registered with `prefix="/auth"`
- Results in endpoint: `POST /auth/login`

### Request/Response Models

- Use Pydantic `BaseModel` classes for request/response validation
- Define models in the same file as the endpoint that uses them
- Example: `UserLogin` model in `api/post/auth/login.py`

## Adding New Endpoints

1. Create a new file under `api/{http_method}/{feature}/`
2. Define an `APIRouter` instance: `router = APIRouter()`
3. Create Pydantic models for request/response validation
4. Define endpoint handler(s) with appropriate decorators
5. Import and register the router in `main.py` with `app.include_router()`
