# Google Workspace CLI Wrapper (gws-wrap)

A focused, user-friendly Python wrapper around the [Google Workspace CLI (gws)](https://github.com/googleworkspace/cli). This tool provides simplified adapters for common tasks like fetching recent emails, managing calendar events, and searching/downloading files from Drive.

## Features

### 📧 Mail (Gmail)
- **List**: Get recent messages with metadata (From, Subject, Date).
- **Search**: Search messages using Gmail query syntax (e.g., `from:me`, `is:unread`).
- **Get Body**: Retrieve the full text content of a message by ID.
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
- **Click**: For a robust CLI interface.
- **Pydantic**: Structured data models for all Google Workspace resources.
- **Dynaconf**: Configuration management (settings.toml).
- **Loguru**: Clean, structured logging.
- **dateparser**: Flexible natural language date parsing.

## Installation

1. Ensure you have the [gws CLI](https://github.com/googleworkspace/cli) installed and authenticated (`gws auth login`).
2. Clone this repository.
3. Install dependencies using uv:
   ```bash
   uv sync
   ```

## Usage

All commands are prefixed with `uv run gws-wrap`.

### Mail Examples
```bash
# List 10 most recent emails
uv run gws-wrap mail list

# Search for specific emails
uv run gws-wrap mail search "from:noreply@github.com"

# View email body
uv run gws-wrap mail get-body <MESSAGE_ID>

# Move multiple messages to trash
uv run gws-wrap mail trash <ID1> <ID2>
```

### Calendar Examples
```bash
# List upcoming events for next 7 days
uv run gws-wrap calendar list

# Create an event with natural language
uv run gws-wrap calendar create "Lunch with Team" --start "tomorrow 12pm" --duration 60
```

### Drive Examples
```bash
# Search for a file
uv run gws-wrap drive search "Project Proposal"

# Download a file (auto-detects filename)
uv run gws-wrap drive download <FILE_ID>
```

## API

The project also includes a FastAPI-based REST API that exposes the same functionality.

### Running the API
```bash
uv run gws-api
```
The API will be available at `http://localhost:8000`.

### Documentation
Once the API is running, you can access the interactive documentation at:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## Docker Support

A `Dockerfile` is provided for containerized deployment.

```bash
docker build -t gws-wrap .
docker run -p 8000:8000 gws-wrap
```

## Global Options
- `-h`, `--help`: Show help for any command.
- `--json-output`: Most list/search commands support raw JSON output for piping.
