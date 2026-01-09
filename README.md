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

## Database
The project uses SQLite for storage. The database file is located at `data/data.db`.
- **Passwords** are stored as salted hashes using `bcrypt` (via `passlib`).
- **Data folder** is ignored by git (see `.gitignore`).

## Endpoints
- `POST /auth/register`: Register a new user with email and password.
- `POST /auth/login`: Authenticate and receive a token.
# User Management & Roles - API Documentation

## Status: Implemented

### Roles Supported
- `admin`
- `property_manager`
- `facility_manager`
- `technician`
- `cleaning`

### API Endpoints

#### 1. Fetch User List
- **Endpoint**: `GET /users`
- **Authentication**: Required (Bearer `authenticated_access_token`)
- **Response**: Array of user objects including `id`, `email`, `role`, and `name`.

#### 2. Update User Role
- **Endpoint**: `PATCH /users/{id}/role`
- **Authentication**: Required (Bearer `authenticated_access_token`)
- **Body**: `{ "role": "admin" | "property_manager" | ... }`
- **Response**: Updated user object.

#### 3. Current User Role
- **Endpoint**: `GET /auth/me`
- **Authentication**: Required (Bearer `authenticated_access_token`)
- **Response**: User object for the current session.

### Role Permissions (Frontend Planning)
| Role | Access to User Management | Access to Site Management | Access to Tasks |
| :--- | :--- | :--- | :--- |
| Admin | Yes | Yes | Yes |
| Property Manager | No | Yes | Yes |
| Facility Manager | No | Yes | Yes |
| Technician | No | No | Yes |
| Cleaning | No | No | Yes |

# Sites & Tasks - API Documentation

## Status: Implemented

### Sites
- **GET /sites**: List all sites. (Auth Required)
- **GET /sites/{id}**: Get details for a specific site. (Auth Required)
- **POST /sites**: Create a new site. (Auth Required)
  - Body: `{ "name": "...", "address": "...", "coordinator": "..." }`
- **PATCH /sites/{id}**: Update site details. (Auth Required)
  - Body: `{ "name": "...", "address": "...", "coordinator": "..." }` (All fields optional)
- **DELETE /sites/{id}**: Delete a site. (Auth Required)
  - Note: Site cannot be deleted if it has associated tasks.

### Tasks
- **GET /tasks**: List all tasks. Supports filtering by `site_id` and `status`. (Auth Required)
- **GET /tasks/{id}**: Get task details. (Auth Required)
- **POST /tasks**: Create a new task. (Auth Required)
  - Body: `{ "site_id": 1, "title": "...", "description": "...", "status": "TODO", "priority": "MEDIUM", "assignee": "...", "photos": [] }`

## Project Structure
- `main.py`: Entry point of the FastAPI application.
- `database.py`: SQLAlchemy database configuration.
- `models.py`: Database models (User).
- `auth_utils.py`: Password hashing utilities.
- `api/`: Route definitions.
- `requirements.txt`: Python package dependencies.