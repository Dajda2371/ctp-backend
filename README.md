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
- **Authentication**: Required (Bearer `token`)
- **Response**: Array of user objects.

#### 2. Get User Details
- **Endpoint**: `GET /users/{id}`
- **Authentication**: Required (Bearer `token`)
- **Response**: User object including `id`, `email`, `role`, and `name`.

#### 3. Get User Role
- **Endpoint**: `GET /users/{id}/role`
- **Authentication**: Required (Bearer `token`)
- **Response**: `{ "role": "..." }`

#### 4. Get User Email
- **Endpoint**: `GET /users/{id}/email`
- **Authentication**: Required (Bearer `token`)
- **Response**: `{ "email": "..." }`

#### 5. Get User Name
- **Endpoint**: `GET /users/{id}/name`
- **Authentication**: Required (Bearer `token`)
- **Response**: `{ "name": "..." }`

#### 6. Update User Role
- **Endpoint**: `PUT /users/{id}/role`
- **Authentication**: Required (Bearer `token`)
- **Body**: `{ "role": "admin" | "property_manager" | ... }`
- **Response**: Updated user object.

#### 7. Update User Name
- **Endpoint**: `PUT /users/{id}/name`
- **Authentication**: Required (Bearer `token`)
- **Body**: `{ "name": "..." }`
- **Response**: Updated user object.

#### 8. Update User Email
- **Endpoint**: `PUT /users/{id}/email`
- **Authentication**: Required (Bearer `token`)
- **Body**: `{ "email": "..." }`
- **Response**: Updated user object.

#### 9. Current User Context
- **Endpoint**: `GET /auth/me`
- **Authentication**: Required (Bearer `token`)
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
  - Body: `{ "site_id": 1, "title": "...", "description": "...", "status": "TODO", "priority": 3, "assignee": "...", "due_date": "ISO-DATE", "photos": [] }`
    - *Note: Priority is an integer from 1 (lowest) to 5 (highest).*
- **PATCH /tasks/{id}**: Update task details. (Auth Required)
  - Body: `{ "site_id": 1, "title": "...", "description": "...", "status": "...", "priority": 3, "assignee": "...", "due_date": "ISO-DATE", "photos": [] }` (All fields optional)
- **DELETE /tasks/{id}**: Delete a task. (Auth Required)

#### Task Field Updates (PUT/PATCH)
- **PUT /tasks/{id}/site_id**: Update site. Body: `{"site_id": 1}`
- **PUT /tasks/{id}/title**: Update title. Body: `{"title": "..."}`
- **PUT /tasks/{id}/description**: Update description. Body: `{"description": "..."}`
- **PUT /tasks/{id}/status**: Update status. Body: `{"status": "..."}`
- **PUT /tasks/{id}/priority**: Update priority. Body: `{"priority": 3}`
- **PUT /tasks/{id}/assignee**: Update assignee. Body: `{"assignee": "..."}`
- **PUT /tasks/{id}/due_date**: Update due date. Body: `{"due_date": "ISO-DATE"}`
- **POST /tasks/{id}/photos**: Add a photo. Body: `{"url": "..."}`
- **DELETE /tasks/{id}/photos/{photo_index}**: Remove a photo by index.

#### Task Field Queries (GET)
- **GET /tasks/{id}/site_id**: Get site. Response: `{"site_id": "1"}`
- **GET /tasks/{id}/title**: Get title. Response: `{"title": "..."}`
- **GET /tasks/{id}/description**: Get description. Response: `{"description": "..."}`
- **GET /tasks/{id}/status**: Get status. Response: `{"status": "..."}`
- **GET /tasks/{id}/priority**: Get priority. Response: `{"priority": 3}`
- **GET /tasks/{id}/assignee**: Get assignee. Response: `{"assignee": "..."}`
- **GET /tasks/{id}/due_date**: Get due date. Response: `{"due_date": "ISO-DATE"}`
- **GET /tasks/{id}/photos**: Get photos. Response: `{"photos": ["..."]}`

## Project Structure
- `main.py`: Entry point of the FastAPI application.
- `database.py`: SQLAlchemy database configuration.
- `models.py`: Database models (User).
- `auth_utils.py`: Password hashing utilities.
- `api/`: Route definitions.
- `requirements.txt`: Python package dependencies.