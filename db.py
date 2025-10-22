from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from base_model import Base, Notes


class DB:
    def __init__(self) -> None:
        args = {"echo": True, "connect_args": {"check_same_thread": False}, "poolclass": StaticPool}
        self.engine = create_engine("sqlite:///:memory:", **args)
        Base.metadata.create_all(self.engine)

    def create_note(self, token: str, user_note: str) -> bool:
        with Session(self.engine) as session:
            note_entry = Notes(
                user_token=token,
                user_note=user_note,
            )
            session.add(note_entry)
            session.commit()
            return True

    def get_note(self, token: str) -> str | None:
        with Session(self.engine) as session:
            stmt = select(Notes).where(Notes.user_token == token).where(Notes.active == 1)
            results = session.scalars(stmt).all()
            if results:
                return "\n".join([f"Id: {result.id} - Note: {result.user_note}" for result in results])
        return None

    def delete_note(self, token: str, note_id: int) -> bool:
        with Session(self.engine) as session:
            stmt = select(Notes).where(Notes.id == note_id).where(Notes.user_token == token)
            result = session.scalars(stmt).first()
            if result:
                result.active = 0
                session.commit()
                return True
        return False
