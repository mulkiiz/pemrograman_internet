from fastapi import FastAPI

from database import create_db_and_tables
from routers.measurements import router as measurements_router
from routers.sensors import router as sensors_router


create_db_and_tables()

app = FastAPI(title="API Pengukuran Sensor Laboratorium")
app.include_router(sensors_router)
app.include_router(measurements_router)


@app.get("/")
def home():
    return {"message": "API pengukuran sensor siap digunakan", "docs": "/docs"}
