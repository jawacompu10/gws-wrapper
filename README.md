# Google Workspace CLI Wrapper (gws-wrap)

A focused, user-friendly Python wrapper around the [Google Workspace CLI (gws)](https://github.com/googleworkspace/cli). This tool provides simplified adapters for common tasks like fetching recent emails, managing calendar events, and searching/downloading files from Drive.

## 🛠 Prerequisites

This project is a wrapper and requires the **Google Workspace CLI** to be installed and authenticated on your system.

1.  **Install gws**: Follow the instructions at [googleworkspace/cli](https://github.com/googleworkspace/cli).
2.  **Authenticate**: Run `gws auth login` to grant access to your Google account.

## Features

### 📧 Mail (Gmail)
- **List**: Get recent messages with metadata (From, Subject, Date).
- **Search**: Search messages using Gmail query syntax (e.g., `from:me`, `is:unread`).
- **Get Body**: Retrieve the full text content of a message by ID.
- **Archive**: Remove the `INBOX` label from messages.
- **Trash/Delete**: Safely move messages to trash or permanently delete them.

### 📅 Calendar
- **List**: View upcoming events for the next N days (default: 7).
- **Create**: Quickly create events using natural language (e.g., "tomorrow at 10am") via `dateparser`.

### 📂 Drive
- **Search**: Find files by name.
- **Download**: Download files by ID with automatic naming based on metadata.

## Tech Stack
- **Python 3.13+**
- **uv**: Project and dependency management.
- **Click**: For the CLI interface.
- **FastAPI**: For the REST API interface.
- **Pydantic**: Structured data models.
- **Dynaconf**: Configuration management.

## Installation

```bash
git clone <repo-url>
cd gws-wrapper
uv sync
```

## Usage (CLI)

All commands are run via `uv run gws-wrap`.

### Mail
```bash
uv run gws-wrap mail list --count 5
uv run gws-wrap mail search "subject:invoice"
uv run gws-wrap mail archive <MESSAGE_ID>
uv run gws-wrap mail trash <ID1> <ID2>
uv run gws-wrap mail get-body <MESSAGE_ID>
```

### Calendar
```bash
uv run gws-wrap calendar list --days 14
uv run gws-wrap calendar create "Team Sync" --start "Monday 10am" --duration 45
```

### Drive
```bash
uv run gws-wrap drive search "Budget"
uv run gws-wrap drive download <FILE_ID>
```

## Usage (API)

The project includes a FastAPI-based REST API.

### Running the API
```bash
uv run gws-api
```
Access the interactive documentation at `http://localhost:8000/docs`.

### Key Endpoints
| Method | Path | Description |
| :--- | :--- | :--- |
| `GET` | `/mail` | List or Search emails (`?q=...`, `?count=N`) |
| `GET` | `/mail/{id}` | Get email body |
| `POST` | `/mail/archive` | Bulk archive (`{"message_ids": [...]}`) |
| `POST` | `/mail/trash` | Bulk move to trash |
| `GET` | `/calendar` | List upcoming events |
| `POST` | `/calendar` | Create event |
| `GET` | `/drive` | Search files |
| `GET` | `/drive/{id}` | Download file |

## Docker Support
```bash
docker build -t gws-wrap .
docker run -p 8000:8000 -v ~/.config/gws:/root/.config/gws gws-wrap
```
*(Note: Volume mounting is required to share your host's gws authentication)*
