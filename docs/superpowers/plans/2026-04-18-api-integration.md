# FastAPI Integration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement a RESTful API interface for the `gws-wrap` project using FastAPI, reusing existing adapters and Pydantic models.

**Architecture:** The API will consist of service-specific routers (`mail`, `calendar`, `drive`) that directly call the existing adapter functions. A global exception handler will map internal errors to HTTP status codes.

**Tech Stack:** FastAPI, Uvicorn, Pydantic, existing adapters, and Docker.

---

### Task 1: Add Dependencies and API Structure

**Files:**
- Modify: `pyproject.toml`
- Create: `src/gws_wrapper/api/__init__.py`
- Create: `src/gws_wrapper/api/main.py`
- Create: `src/gws_wrapper/api/routes/__init__.py`

- [ ] **Step 1: Add FastAPI and Uvicorn dependencies**
Run: `uv add fastapi uvicorn`

- [ ] **Step 2: Initialize API package structure**
Run: `mkdir -p src/gws_wrapper/api/routes && touch src/gws_wrapper/api/__init__.py src/gws_wrapper/api/routes/__init__.py`

- [ ] **Step 3: Create the main FastAPI application stub**
```python
from fastapi import FastAPI
from loguru import logger

app = FastAPI(title="gws-wrap API")

@app.get("/")
async def root():
    return {"message": "Google Workspace CLI Wrapper API"}

def run():
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```
File: `src/gws_wrapper/api/main.py`

- [ ] **Step 4: Update pyproject.toml with the API entry point**
Modify `pyproject.toml`:
```toml
[project.scripts]
gws-wrap = "gws_wrapper.main:cli"
gws-api = "gws_wrapper.api.main:run"
```

- [ ] **Step 5: Verify the API starts**
Run: `uv run gws-api` (Check for "Uvicorn running on http://0.0.0.0:8000")

- [ ] **Step 6: Commit**
```bash
git add pyproject.toml uv.lock src/gws_wrapper/api
git commit -m "feat: initialize FastAPI structure and dependencies"
```

---

### Task 2: Implement Mail Router (GET /mail and GET /mail/{id})

**Files:**
- Create: `src/gws_wrapper/api/routes/mail.py`
- Modify: `src/gws_wrapper/api/main.py`
- Create: `tests/test_api_mail.py`

- [ ] **Step 1: Create the mail router**
```python
from fastapi import APIRouter, Query, HTTPException
from typing import List, Optional
from gws_wrapper.adapters import gmail
from gws_wrapper.models.gmail import GmailMessage

router = APIRouter(prefix="/mail", tags=["mail"])

@router.get("", response_model=List[GmailMessage])
async def list_or_search_messages(q: Optional[str] = None, count: int = 10):
    try:
        if q:
            return gmail.search_messages(q, count)
        return gmail.list_messages(count)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{message_id}")
async def get_message_body(message_id: str):
    try:
        body = gmail.get_message_body(message_id)
        return {"id": message_id, "body": body}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```
File: `src/gws_wrapper/api/routes/mail.py`

- [ ] **Step 2: Include the mail router in the main app**
Modify `src/gws_wrapper/api/main.py`:
```python
from gws_wrapper.api.routes import mail
app.include_router(mail.router)
```

- [ ] **Step 3: Write a test for the mail list endpoint**
```python
from fastapi.testclient import TestClient
from gws_wrapper.api.main import app
import pytest

client = TestClient(app)

def test_get_mail_list(mocker):
    mock_list = mocker.patch("gws_wrapper.adapters.gmail.list_messages")
    mock_list.return_value = []
    
    response = client.get("/mail?count=5")
    assert response.status_code == 200
    assert response.json() == []
    mock_list.assert_called_once_with(5)
```
File: `tests/test_api_mail.py`

- [ ] **Step 4: Run the test**
Run: `uv run pytest tests/test_api_mail.py`

- [ ] **Step 5: Commit**
```bash
git add src/gws_wrapper/api/routes/mail.py src/gws_wrapper/api/main.py tests/test_api_mail.py
git commit -m "feat: add mail GET endpoints to the API"
```

---

### Task 3: Implement Mail POST and DELETE endpoints

**Files:**
- Create: `src/gws_wrapper/models/api.py`
- Modify: `src/gws_wrapper/api/routes/mail.py`

- [ ] **Step 1: Create API request models**
```python
from pydantic import BaseModel
from typing import List, Optional

class TrashRequest(BaseModel):
    message_ids: List[str]
```
File: `src/gws_wrapper/models/api.py`

- [ ] **Step 2: Add trash and delete endpoints to the mail router**
Modify `src/gws_wrapper/api/routes/mail.py`:
```python
from gws_wrapper.models.api import TrashRequest

@router.post("/trash")
async def trash_messages(request: TrashRequest):
    try:
        for mid in request.message_ids:
            gmail.trash_message(mid)
        return {"status": "success", "count": len(request.message_ids)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{message_id}")
async def delete_message(message_id: str):
    try:
        gmail.delete_message(message_id)
        return {"status": "success", "message": f"Deleted {message_id}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

- [ ] **Step 3: Test the trash endpoint**
Add to `tests/test_api_mail.py`:
```python
def test_trash_messages(mocker):
    mock_trash = mocker.patch("gws_wrapper.adapters.gmail.trash_message")
    
    response = client.post("/mail/trash", json={"message_ids": ["id1", "id2"]})
    assert response.status_code == 200
    assert response.json()["count"] == 2
    assert mock_trash.call_count == 2
```

- [ ] **Step 4: Run tests**
Run: `uv run pytest tests/test_api_mail.py`

- [ ] **Step 5: Commit**
```bash
git add src/gws_wrapper/models/api.py src/gws_wrapper/api/routes/mail.py tests/test_api_mail.py
git commit -m "feat: add mail POST and DELETE endpoints to the API"
```

---

### Task 4: Implement Calendar Endpoints (GET and POST)

**Files:**
- Modify: `src/gws_wrapper/models/api.py`
- Create: `src/gws_wrapper/api/routes/calendar.py`
- Modify: `src/gws_wrapper/api/main.py`
- Create: `tests/test_api_calendar.py`

- [ ] **Step 1: Add Calendar request model**
Modify `src/gws_wrapper/models/api.py`:
```python
class CreateEventRequest(BaseModel):
    summary: str
    start: Optional[str] = None
    duration: int = 30
    location: Optional[str] = None
    description: Optional[str] = None
```

- [ ] **Step 2: Create the calendar router**
```python
from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
import dateparser
from datetime import datetime, timedelta, timezone
from gws_wrapper.adapters import calendar
from gws_wrapper.models.calendar import CalendarEvent
from gws_wrapper.models.api import CreateEventRequest

router = APIRouter(prefix="/calendar", tags=["calendar"])

@router.get("", response_model=List[CalendarEvent])
async def list_events(days: int = 7):
    try:
        return calendar.list_events(days)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("", response_model=CalendarEvent)
async def create_event(request: CreateEventRequest):
    try:
        if request.start:
            start_dt = dateparser.parse(request.start, settings={'PREFER_DATES_FROM': 'future'})
            if not start_dt:
                raise HTTPException(status_code=400, detail="Invalid start time format")
            if start_dt.tzinfo is None:
                start_dt = start_dt.astimezone()
        else:
            start_dt = datetime.now(timezone.utc)

        end_dt = start_dt + timedelta(minutes=request.duration)
        
        return calendar.create_event(
            summary=request.summary,
            start_time=start_dt.isoformat(),
            end_time=end_dt.isoformat(),
            location=request.location,
            description=request.description
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```
File: `src/gws_wrapper/api/routes/calendar.py`

- [ ] **Step 2: Include the calendar router in the main app**
Modify `src/gws_wrapper/api/main.py`:
```python
from gws_wrapper.api.routes import calendar
app.include_router(calendar.router)
```

- [ ] **Step 3: Test the calendar list endpoint**
```python
from fastapi.testclient import TestClient
from gws_wrapper.api.main import app
import pytest

client = TestClient(app)

def test_get_calendar_events(mocker):
    mock_list = mocker.patch("gws_wrapper.adapters.calendar.list_events")
    mock_list.return_value = []
    
    response = client.get("/calendar?days=7")
    assert response.status_code == 200
    mock_list.assert_called_once_with(7)
```
File: `tests/test_api_calendar.py`

- [ ] **Step 4: Run tests**
Run: `uv run pytest tests/test_api_calendar.py`

- [ ] **Step 5: Commit**
```bash
git add src/gws_wrapper/api/routes/calendar.py src/gws_wrapper/api/main.py tests/test_api_calendar.py
git commit -m "feat: add calendar endpoints to the API"
```

---

### Task 5: Implement Drive Endpoints (Search and Download)

**Files:**
- Create: `src/gws_wrapper/api/routes/drive.py`
- Modify: `src/gws_wrapper/api/main.py`
- Create: `tests/test_api_drive.py`

- [ ] **Step 1: Create the drive router**
```python
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import FileResponse
from typing import List
import os
import tempfile
from gws_wrapper.adapters import drive
from gws_wrapper.models.drive import DriveFile

router = APIRouter(prefix="/drive", tags=["drive"])

@router.get("", response_model=List[DriveFile])
async def search_files(q: str, limit: int = 10):
    try:
        return drive.search_files(q, limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{file_id}")
async def download_file(file_id: str):
    try:
        file_info = drive.get_file_info(file_id)
        # Create a temporary file to hold the download
        tmp_dir = tempfile.mkdtemp()
        tmp_path = os.path.join(tmp_dir, file_info.name)
        
        drive.download_file(file_id, tmp_path)
        
        return FileResponse(
            path=tmp_path,
            filename=file_info.name,
            media_type="application/octet-stream"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```
File: `src/gws_wrapper/api/routes/drive.py`

- [ ] **Step 2: Include the drive router in the main app**
Modify `src/gws_wrapper/api/main.py`:
```python
from gws_wrapper.api.routes import drive
app.include_router(drive.router)
```

- [ ] **Step 3: Test the drive search endpoint**
```python
from fastapi.testclient import TestClient
from gws_wrapper.api.main import app
import pytest

client = TestClient(app)

def test_drive_search(mocker):
    mock_search = mocker.patch("gws_wrapper.adapters.drive.search_files")
    mock_search.return_value = []
    
    response = client.get("/drive?q=test")
    assert response.status_code == 200
    mock_search.assert_called_once_with("test", 10)
```
File: `tests/test_api_drive.py`

- [ ] **Step 4: Run tests**
Run: `uv run pytest tests/test_api_drive.py`

- [ ] **Step 5: Commit**
```bash
git add src/gws_wrapper/api/routes/drive.py src/gws_wrapper/api/main.py tests/test_api_drive.py
git commit -m "feat: add drive endpoints to the API"
```

---

### Task 6: Implement Global Error Handling and Documentation

**Files:**
- Modify: `src/gws_wrapper/api/main.py`
- Create: `Dockerfile`
- Modify: `README.md`

- [ ] **Step 1: Implement global error handler**
Modify `src/gws_wrapper/api/main.py`:
```python
from fastapi import Request
from fastapi.responses import JSONResponse

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global error: {exc}")
    return JSONResponse(
        status_code=500,
        content={"error": "Internal Server Error", "detail": str(exc)},
    )
```

- [ ] **Step 2: Create Dockerfile**
```dockerfile
FROM python:3.13-slim-bookworm AS builder

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-cache

FROM python:3.13-slim-bookworm

# Install gws CLI (requires curl/bash)
RUN apt-get update && apt-get install -y curl bash && \
    curl -sSL https://raw.githubusercontent.com/googleworkspace/cli/main/install.sh | bash && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY --from=builder /app/.venv /app/.venv
COPY src ./src
COPY settings.toml ./

ENV PATH="/app/.venv/bin:$PATH"
ENV GWS_SETTINGS_MODULE=settings.toml

EXPOSE 8000
CMD ["gws-api"]
```
File: `Dockerfile`

- [ ] **Step 3: Update README.md with API instructions**
Add a new section to `README.md` for the API.

- [ ] **Step 4: Verify the full API and interactive docs**
Run: `uv run gws-api`
Visit: `http://0.0.0.0:8000/docs`

- [ ] **Step 5: Commit**
```bash
git add src/gws_wrapper/api/main.py Dockerfile README.md
git commit -m "feat: add global error handling and docker support"
```
