# ctp-backend

FastAPI project for the CTP backend.

## Prerequisites

- Python 3.7+
- `pip` (Python package installer)

## Getting Started on a New Machine

Follow these steps to set up and run the project:

### 1. Clone the Repository
```bash
git clone <repository-url>
cd ctp-backend
```

### 2. Create a Virtual Environment
It is recommended to use a virtual environment to manage dependencies.
```bash
python3 -m venv .venv
```

### 3. Activate the Virtual Environment
- **Mac/Linux:**
  ```bash
  source .venv/bin/activate
  ```
- **Windows:**
  ```bash
  .venv\Scripts\activate
  ```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Run the Application
Start the development server:
```bash
uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.
You can view the interactive documentation at `http://127.0.0.1:8000/docs`.

## Project Structure
- `main.py`: Entry point of the FastAPI application.
- `api/`: Contains the API route definitions.
- `requirements.txt`: List of Python dependencies.