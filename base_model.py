from pydantic import BaseModel


class Notes(BaseModel):
    id: int
    user_token: str
