# 🧪 FastAPI Lab

This repository contains hands-on exercises and examples from **Parts 5 to 7** of FastAPI course. These sections focus on building more robust APIs using key FastAPI features like:

- Request validation
- Response customization
- Dependency injection
- Database integration with SQLite
- etc

## 📁 Project Structure

The project is divided into multiple directories, each focusing on a specific topic:

```
.
├── basic-api/                  # Basic FastAPI setup and endpoints
├── fastapi-di/                 # Dependency Injection examples
├── request-validation-response/ # Request validation and response handling using Pydantic
├── task-management-app-db/     # Task management app with database integration
├── task_management/            # Core task management logic or models
├── tasks.db                    # SQLite database file (if used)
├── pyproject.toml              # Project configuration for uv/Pip/Poetry
├── uv.lock                     # Lock file for uv package manager
└── README.md                   # This file
```

## 🛠️ Tools Used

- **[FastAPI](https://fastapi.tiangolo.com/)** – High-performance web framework for building APIs.
- **[uv](https://github.com/astral-sh/uv)** – Fast Python package manager and virtual environment tool.
- **[Pydantic](https://docs.pydantic.dev/latest/)** – Data validation and settings management.
- **SQLite** (`tasks.db`) – Lightweight database used in task management examples.

## 🚀 Getting Started

### 1. Install Dependencies

Make sure you have [`uv`](https://github.com/astral-sh/uv) installed.

```bash
uv sync
```

Or install FastAPI and Uvicorn manually:

```bash
uv pip install fastapi uvicorn
```

For development tools like linting and type checking:

```bash
uv pip install ruff mypy
```

### 2. Run an App

Navigate into any subdirectory (e.g., `basic-api`) and run:

```bash
uvicorn main:app --reload
```

Then visit [http://localhost:8000/docs](http://localhost:8000/docs) to see the interactive API documentation.

---

## 🧪 Development Tools

Run linter:

```bash
ruff check .
```

Run type checker:

```bash
mypy .
```

---

## 📝 Folder Descriptions

| Folder | Description |
|-------|-------------|
| `basic-api` | Introduction to creating simple FastAPI routes and responses. |
| `fastapi-di` | Demonstrates dependency injection patterns in FastAPI. |
| `request-validation-response` | Covers Pydantic models for request validation and custom responses. |
| `task-management-app-db` | Full CRUD application with database integration. |
| `task_management` | Reusable models or core logic for task management. |
| `tasks.db` | SQLite database used by task management apps. |
```
