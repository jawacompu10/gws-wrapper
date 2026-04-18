# Implementation Details: gws-wrap

This document outlines the technical architecture and design patterns used in the `gws-wrap` project.

## Architecture: The Adapter Pattern

The core design principle is the **Adapter Pattern**. We wrap the complex, low-level `gws` CLI with higher-level, task-oriented functions.

### 1. Centralized CLI Runner (`adapters/cli.py`)
All interactions with the `gws` CLI go through a single function: `run_gws_command`.
- **Purpose**: Consistent error handling, JSON parsing, logging, and command construction.
- **Key Features**: Supports `--params`, `--json` (body), `--output`, and `--dry-run`.
- **Error Handling**: Translates `subprocess.CalledProcessError` into meaningful application errors.

### 2. Service Adapters (`adapters/*.py`)
Each service (Mail, Calendar, Drive) has its own adapter that:
- Maps application logic to specific `gws` commands.
- Transforms raw JSON dictionaries from `gws` into structured **Pydantic** models.

### 3. Dual Interfaces: CLI & API
The project provides two entry points to the same logic:
- **CLI (Click)**: Located in `cli/*.py`, optimized for human use in the terminal.
- **API (FastAPI)**: Located in `api/main.py` and `api/routes/*.py`, providing RESTful endpoints.
- **Shared Logic**: Both interfaces call the same adapter functions, ensuring consistent behavior across all platforms.

### 4. Data Models (`models/*.py`)
We use **Pydantic V2** to define schemas for all resources.
- **Models**: `GmailMessage`, `CalendarEvent`, `DriveFile`.
- **API Models**: Specialized models in `models/api.py` handle request validation for POST bodies (e.g., `TrashRequest`).

### 5. Configuration (`config.py` & `settings.toml`)
Powered by **Dynaconf**, the configuration system:
- Loads defaults from `settings.toml` (e.g., `default_count`, `default_days`).
- Both CLI and API layers respect these defaults.

## Key Implementation Highlights

- **Archiving Logic**: Archiving is implemented by removing the `INBOX` label via Gmail's `modify` method. Verification confirmed that Gmail treats an email as archived once the `INBOX` label is removed.
- **Gmail Metadata Fetching**: The `mail list` and `mail search` commands fetch the `metadata` format for each message to retrieve headers (From, Subject, Date) efficiently.
- **Multipart Email Body Parsing**: The `mail get-body` command recursively searches MIME parts to extract the first available text part, handling URL-safe base64 decoding.
- **Natural Language Parsing**: Calendar event creation uses `dateparser` to allow intuitive strings like "next Tuesday 10am".
- **Automatic File Naming**: `drive download` fetches file metadata first if an output path isn't provided.

## Testing Strategy
- **Framework**: **pytest** with **pytest-mock**.
- **Mocking**: The `run_gws_command` is patched during tests to return mock JSON, allowing the entire suite to run without a real Google account or the `gws` CLI.
- **Coverage**: Includes unit tests for adapters and integration tests for both CLI and API layers.
