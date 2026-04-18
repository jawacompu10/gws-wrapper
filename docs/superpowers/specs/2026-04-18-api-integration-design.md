# Spec: FastAPI Integration for gws-wrap

This document specifies the design for adding a RESTful API interface to the `gws-wrap` project using FastAPI.

## 1. Architectural Overview

The API will serve as a parallel interface to the existing CLI, both sitting on top of the same `adapters` layer.

```
[ User ]
    |
    +---- [ CLI (Click) ] ----+
    |                         |
    +---- [ API (FastAPI) ] --+--> [ Adapters ] --> [ gws CLI ]
```

### Key Components
- **API Main**: `src/gws_wrapper/api/main.py` (App initialization and routing).
- **Routers**: `src/gws_wrapper/api/routes/*.py` (Service-specific endpoints).
- **Request Models**: `src/gws_wrapper/models/api.py` (Input validation for POST bodies).
- **Dockerfile**: For containerized deployment.

## 2. API Design (RESTful)

### Base URL: `/`

| Resource | Method | Path | Description | Params/Body |
| :--- | :--- | :--- | :--- | :--- |
| **Mail** | `GET` | `/mail` | List/Search messages | `q` (string), `count` (int) |
| | `GET` | `/mail/{id}` | Get message body | (ID in path) |
| | `POST` | `/mail/trash` | Bulk move to trash | `{"message_ids": [...]}` |
| | `DELETE` | `/mail/{id}` | Permanent delete | (ID in path) |
| **Calendar** | `GET` | `/calendar` | List upcoming events | `days` (int, default: 7) |
| | `POST` | `/calendar` | Create a new event | `{"summary": "...", "start": "...", "duration": 30, ...}` |
| **Drive** | `GET` | `/drive` | Search for files | `q` (string), `limit` (int) |
| | `GET` | `/drive/{id}` | Download file | (ID in path, returns stream) |

## 3. Implementation Details

### Model Reuse
- All `GET` endpoints will return the existing Pydantic models from `src/gws_wrapper/models/`.
- New `Request` models will be added for `POST` operations in `src/gws_wrapper/models/api.py`.

### Error Handling
- A global exception handler will map `RuntimeError` from the adapters to appropriate HTTP status codes (401 for auth, 404 for missing resources, 500 for CLI failures).
- Error responses will follow a consistent JSON format: `{"error": "string", "detail": "string"}`.

### Configuration
- The API will respect the same `settings.toml` and environment variables as the CLI via the existing `dynaconf` setup.

## 4. Deployment

### Scripts
A new entry point will be added to `pyproject.toml`:
```toml
[project.scripts]
gws-api = "gws_wrapper.api.main:run"
```

### Docker
A multi-stage `Dockerfile` will be provided:
1. **Builder**: Uses `uv` to install dependencies.
2. **Runner**: 
   - Installs the `gws` CLI.
   - Copies the virtual environment and source code.
   - Exposes port 8000 and runs `uvicorn`.

## 5. Security Note
- The API currently assumes local execution and shares the host's `gws` credentials. 
- In Docker, the `~/.config/gws` directory should be mounted as a volume to provide authentication.
- No additional API-level authentication (like API keys) is included in this initial spec.
