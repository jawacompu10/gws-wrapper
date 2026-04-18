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
