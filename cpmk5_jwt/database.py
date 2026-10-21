"""Koneksi SQLite dan dependency sesi database."""

from collections.abc import Generator

from sqlmodel import Session, SQLModel, create_engine

from config import DATABASE_URL

connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, echo=False, connect_args=connect_args)


def create_db_and_tables() -> None:
    """Membuat tabel dari model yang terdaftar."""
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    """Menyediakan satu sesi database untuk satu request API."""
    with Session(engine) as session:
        yield session
