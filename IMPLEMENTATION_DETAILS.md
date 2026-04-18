# Implementation Details: gws-wrap

This document outlines the technical architecture and design patterns used in the `gws-wrap` project.

## Architecture: The Adapter Pattern

The core design principle is the **Adapter Pattern**. We wrap the complex, low-level `gws` CLI with higher-level, task-oriented functions.

### 1. Centralized CLI Runner (`adapters/cli.py`)
All interactions with the `gws` CLI go through a single function: `run_gws_command`.
- **Purpose**: Consistent error handling, JSON parsing, logging, and command construction.
- **Key Features**: Supports `--params`, `--json` (body), `--output`, and `--dry-run`.
- **Error Handling**: Captures `subprocess.CalledProcessError` and translates it into meaningful application errors.

### 2. Service Adapters (`adapters/*.py`)
Each service (Mail, Calendar, Drive) has its own adapter that:
- Maps application logic (e.g., `list_messages`) to specific `gws` commands.
- Handles multi-step operations (e.g., `list_messages` first gets IDs, then fetches metadata for each ID).
- Transforms raw JSON dictionaries from `gws` into structured **Pydantic** models.

### 3. Data Models (`models/*.py`)
We use **Pydantic V2** to define schemas for all Google Workspace resources.
- **Benefits**: Type safety, field validation, and consistent serialization (via `model_dump()`).
- **Config**: Uses `ConfigDict(from_attributes=True)` for easy transformation from raw data.

### 4. Configuration (`config.py` & `settings.toml`)
Powered by **Dynaconf**, the configuration system:
- Loads defaults from `settings.toml`.
- Supports environment variable overrides (prefixed with `GWS_`).
- Allows for `.secrets.toml` (ignored by git) for sensitive settings.

### 5. CLI Layer (`cli/*.py`)
The user interface is built with **Click**.
- **Context Settings**: Globally enables `-h` as a shorthand for `--help`.
- **Separation of Concerns**: The CLI layer is purely for presentation (formatting output, confirmation prompts). All logic lives in the adapters.

## Key Implementation Highlights

- **Gmail Metadata Fetching**: The `mail list` and `mail search` commands fetch the `metadata` format for each message to retrieve common headers (From, Subject, Date) in a way that's much faster than fetching the `full` message body.
- **Multipart Email Body Parsing**: The `mail get-body` command recursively searches through multipart MIME parts to extract the first available text/plain or text/html body, correctly decoding URL-safe base64 data.
- **Natural Language Parsing**: Calendar event creation uses the `dateparser` library with `PREFER_DATES_FROM: 'future'`, allowing for intuitive strings like "next Tuesday 10am".
- **Automatic File Naming**: The `drive download` command first fetches metadata for the given file ID if an output path isn't provided, ensuring the local file name matches the original name on Google Drive.

## Testing Strategy
We use **pytest** and **pytest-mock** to ensure reliability.
- **Mocking**: We never call the real `gws` CLI during tests. Instead, we patch `run_gws_command` to return sample JSON responses.
- **Coverage**: Tests cover success paths, error handling, and data mapping for all services.
