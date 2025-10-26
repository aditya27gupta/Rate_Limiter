FROM python:3.13-alpine
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
WORKDIR /app
COPY . .
RUN uv sync --locked
EXPOSE 9999
CMD ["uv", "run", "main.py"]
