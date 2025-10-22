from collections.abc import Callable

import uvicorn
from fastapi import FastAPI, Request, Response, status

from base_model import Notes
from rate_limiter import rate_limit

app = FastAPI()


@app.middleware("http")
async def check_rate_limit(request: Request, call_next: Callable) -> Response:
    user_token = request.headers.get("user-token")
    if not user_token:
        return Response(
            content="Please provide user token for the request",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
    check, time_left = rate_limit(user_token=user_token)
    if check:
        return await call_next(request)
    return Response(content=f"Wait for {time_left} seconds", status_code=status.HTTP_400_BAD_REQUEST)


@app.get("/", status_code=status.HTTP_200_OK)
def read_root() -> dict:
    return {"Hello": "World"}


@app.get("/notes", status_code=status.HTTP_200_OK)
def get_notes(notes: Notes) -> dict:
    return {"note": "abc"}


@app.post("/notes", status_code=status.HTTP_201_CREATED)
def create_notes(notes: Notes) -> bool:
    return True


@app.delete("/notes", status_code=status.HTTP_202_ACCEPTED)
def delete_notes(notes: Notes) -> None:
    pass


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=9999, reload=True)
