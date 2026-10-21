"""Titik masuk aplikasi FastAPI."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlmodel import Session

from database import create_db_and_tables, engine
from routers import auth, measurements, sensors
from seed import seed_demo_data


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    with Session(engine) as session:
        seed_demo_data(session)
    yield


app = FastAPI(
    title="API Pemantauan Sensor Aman",
    description="Praktikum CPMK-5: REST API, JWT, dan otorisasi berbasis peran.",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(auth.router)
app.include_router(sensors.router)
app.include_router(measurements.router)


@app.get("/", tags=["Info"])
def home() -> dict[str, str]:
    return {
        "message": "API aktif. Buka /docs untuk mencoba endpoint.",
        "docs": "/docs",
    }
