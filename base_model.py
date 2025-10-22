from pydantic import BaseModel
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class CreateNote(BaseModel):
    user_note: str



class Base(DeclarativeBase):
    pass


class Notes(Base):
    __tablename__ = "user_notes"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_token: Mapped[str] = mapped_column(String(30))
    user_note: Mapped[str] = mapped_column(String(100))
    active: Mapped[int] = mapped_column(insert_default=1)
