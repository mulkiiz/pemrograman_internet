from sqlmodel import Session, SQLModel, create_engine


# Jalankan Uvicorn dari folder cpmk4_fastapi. Database bersama berada satu
# tingkat di atas folder ini, di root pemrogramaninternet.
DATABASE_URL = "sqlite:///../lab_sensor.db"
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=True,
)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
