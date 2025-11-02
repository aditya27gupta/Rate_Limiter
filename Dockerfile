# ---- Builder Stage ----
FROM python:3.13-alpine AS builder
# Install uv from a well-known trusted source
COPY --from=ghcr.io/astral-sh/uv:0.9.7 /uv /uvx /bin/
WORKDIR /app
# Copy dependency files first for better caching
COPY pyproject.toml uv.lock* ./
# Install dependencies – no dev dependencies in production
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

# Copy the rest of the codebase after dependencies
COPY . .

# ---- Runtime Stage ----
FROM python:3.13-alpine
# Create dedicated user & group for security
RUN addgroup -g 1001 appgroup && \
    adduser -D -u 1001 -G appgroup -h /app appuser
WORKDIR /app
# Copy built code and installed deps from builder
COPY --from=builder --chown=appuser:appgroup /app /app
USER appuser
ENV UV_SYSTEM_PYTHON=1 PYTHONUNBUFFERED=1
# Start your app using uv
CMD ["uv", "run", "main.py"]
