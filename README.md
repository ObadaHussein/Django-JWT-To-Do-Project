# Django JWT To-Do API

This project is a Django REST API that allows authenticated users to manage their own to-do tasks. It features JWT authentication, custom middleware for logging, and secure task management endpoints.

---

## Root Directory

- `manage.py` — Django's command-line utility for administrative tasks.
- `requirements.txt` — Lists Python dependencies for the project.
- `README.md` — This documentation file.
- `task_requests.log` — Log file for task-related API requests (auto-generated).

---

## todo_project/

This is the **Django project configuration** folder.

- `__init__.py` — Marks the folder as a Python package.
- `settings.py` — Django settings/configuration including JWT and DRF setup.
- `urls.py` — Root URL configurations including JWT token endpoints.
- `wsgi.py` — Entry point for WSGI-compatible web servers.

---

## tasks/

This is the main **Django application** containing the task management logic.

- `__init__.py` — Marks the folder as a Python package.
- `admin.py` — Django admin registration for Task model.
- `apps.py` — App-specific configurations.
- `models.py` — Task model definition with user relationships.
- `views.py` — API views for task operations and health checks.
- `serializers.py` — DRF serializers for Task model.
- `urls.py` — URL routing for task-related endpoints.
- `middleware.py` — Custom logging middleware for task requests.
- `migrations/` — Database schema migration files.
- `tests.py` — Comprehensive test suite for the application.

---

## API Architecture

### Authentication System
The application uses JWT (JSON Web Tokens) for stateless authentication:

- **Access Tokens**: Short-lived tokens (60 minutes) for API access
- **Refresh Tokens**: Long-lived tokens (7 days) for obtaining new access tokens
- **Token Rotation**: Enabled for enhanced security (optional)

### Security Features
- User isolation: Users can only access their own tasks
- JWT token validation on all protected endpoints
- Custom middleware logging for monitoring
- Input validation and sanitization

---

## Installation and Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### 1. Clone and Setup Environment

```bash
git clone <repository-url>
cd jwt
python -m venv venv
```

### 2. Activate Virtual Environment

**Windows:**
```bash
venv\Scripts\activate
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install django djangorestframework djangorestframework-simplejwt
pip freeze > requirements.txt
```

### 4. Database Setup

Run the following commands to create your database tables:

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create Admin User

```bash
python manage.py createsuperuser
```

Fill in the required information to create an admin account for accessing the Django admin panel.

### 6. Run Development Server

```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000`

---

## Authentication Flow

### Step 1: Register a User

Create users through Django admin panel or shell:

```bash
python manage.py shell
```

```python
from django.contrib.auth.models import User
user = User.objects.create_user(username='ahmad', password='Test@1234')
```

### Step 2: Obtain JWT Tokens

**Request:**
```bash
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d "{\"username\": \"ahmad\", \"password\": \"Test@1234\"}"
```

**Response:**
```json
{
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

### Step 3: Use Access Token

Include the access token in the Authorization header for protected endpoints:

```
Authorization: Bearer <access_token>
```

### Step 4: Refresh Tokens

When the access token expires, use the refresh token to get a new one:

```bash
curl -X POST http://localhost:8000/api/token/refresh/ \
  -H "Content-Type: application/json" \
  -d "{\"refresh\": \"<refresh_token>\"}"
```

---

## API Endpoints

### Authentication Endpoints

| Method | Endpoint | Description | Authentication |
|--------|----------|-------------|----------------|
| POST | `/api/token/` | Login and receive tokens | Public |
| POST | `/api/token/refresh/` | Refresh access token | Public |

### Task Management Endpoints

| Method | Endpoint | Description | Authentication |
|--------|----------|-------------|----------------|
| GET | `/tasks/` | List user's tasks | Required |
| POST | `/tasks/` | Create new task | Required |
| PATCH | `/tasks/<id>/complete/` | Mark task as completed | Required |

### Health Check

| Method | Endpoint | Description | Authentication |
|--------|----------|-------------|----------------|
| GET | `/ping/` | Health check endpoint | Public |

---

## Sample API Requests

### Create a Task

**Request:**
```bash
curl -X POST http://localhost:8000/tasks/ \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d "{\"title\": \"Buy groceries\", \"description\": \"Milk, bread, eggs\"}"
```

**Response:**
```json
{
  "id": 1,
  "title": "Buy groceries",
  "description": "Milk, bread, eggs",
  "is_done": false,
  "created_at": "2025-07-21T00:15:30.123456Z",
  "updated_at": "2025-07-21T00:15:30.123456Z",
  "completed_at": null
}
```

### List Tasks

**Request:**
```bash
curl -X GET http://localhost:8000/tasks/ \
  -H "Authorization: Bearer <access_token>"
```

**Response:**
```json
[
  {
    "id": 1,
    "title": "Buy groceries",
    "description": "Milk, bread, eggs",
    "is_done": false,
    "created_at": "2025-07-21T00:15:30.123456Z",
    "updated_at": "2025-07-21T00:15:30.123456Z",
    "completed_at": null
  }
]
```

### Filter Tasks

**Request (Completed tasks):**
```bash
curl -X GET "http://localhost:8000/tasks/?is_done=true" \
  -H "Authorization: Bearer <access_token>"
```

### Complete a Task

**Request:**
```bash
curl -X PATCH http://localhost:8000/tasks/1/complete/ \
  -H "Authorization: Bearer <access_token>"
```

**Response:**
```json
{
  "id": 1,
  "title": "Buy groceries",
  "description": "Milk, bread, eggs",
  "is_done": true,
  "created_at": "2025-07-21T00:15:30.123456Z",
  "updated_at": "2025-07-21T00:20:45.789012Z",
  "completed_at": "2025-07-21T00:20:45.789012Z"
}
```

### Health Check

**Request:**
```bash
curl -X GET http://localhost:8000/ping/
```

**Response:**
```json
{
  "status": "OK"
}
```
