FROM python:3.13-alpine
WORKDIR /app
ENV UV_SYSTEM_PYTHON=1
COPY pyproject.toml uv.lock* ./
RUN --mount=from=ghcr.io/astral-sh/uv,source=/uv,target=/bin/uv \
    uv --no-cache pip install -r pyproject.toml
COPY . .
CMD ["python", "main.py"]
