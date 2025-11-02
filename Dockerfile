FROM python:3.13-alpine as builder
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
WORKDIR /app
COPY . .
ENV UV_SYSTEM_PYTHON=1
RUN uv sync --locked
EXPOSE 9999
CMD ["uv", "run", "main.py"]
