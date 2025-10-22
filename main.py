from collections.abc import Callable
from typing import Annotated

import uvicorn
from fastapi import FastAPI, Header, Request, Response, status

from base_model import CreateNote
from db import DB
from rate_limiter import rate_limit

app = FastAPI()
db_object = DB()


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


@app.get("/notes/")
def get_notes(user_token: Annotated[str, Header()]) -> Response:
    note = db_object.get_note(user_token)
    if note:
        status_code = status.HTTP_200_OK
    else:
        note = "No Note Found"
        status_code = status.HTTP_200_OK
    return Response(content=note, status_code=status_code)


@app.post("/notes")
def create_notes(notes: CreateNote, user_token: Annotated[str, Header()]) -> Response:
    check = db_object.create_note(token=user_token, user_note=notes.user_note)
    if check:
        content = "Note Created"
        status_code = status.HTTP_201_CREATED
    else:
        content = "Note Creation Failed"
        status_code = status.HTTP_400_BAD_REQUEST
    return Response(content=content, status_code=status_code)


@app.delete("/notes/{note_id}")
def delete_notes(note_id: int, user_token: Annotated[str, Header()]) -> Response:
    check = db_object.delete_note(token=user_token, note_id=note_id)
    if check:
        content = "Note Deleted"
        status_code = status.HTTP_202_ACCEPTED
    else:
        content = "Note not found"
        status_code = status.HTTP_204_NO_CONTENT
    return Response(content=content, status_code=status_code)


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=9999, reload=True)
