from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

import crud
from database import get_session
from schemas import MeasurementCreate, MeasurementRead, MeasurementUpdate


router = APIRouter(prefix="/measurements", tags=["Measurements"])


@router.post("/", response_model=MeasurementRead, status_code=201)
def create_measurement(
    data: MeasurementCreate,
    session: Session = Depends(get_session),
):
    sensor = crud.get_sensor(session, data.sensor_id)
    if sensor is None:
        raise HTTPException(status_code=404, detail="Sensor tidak ditemukan")
    return crud.create_measurement(session, data)


@router.get("/", response_model=list[MeasurementRead])
def read_measurements(session: Session = Depends(get_session)):
    return crud.get_measurements(session)


@router.get("/{measurement_id}", response_model=MeasurementRead)
def read_measurement(
    measurement_id: int,
    session: Session = Depends(get_session),
):
    measurement = crud.get_measurement(session, measurement_id)
    if measurement is None:
        raise HTTPException(status_code=404, detail="Pengukuran tidak ditemukan")
    return measurement


@router.put("/{measurement_id}", response_model=MeasurementRead)
def update_measurement(
    measurement_id: int,
    data: MeasurementUpdate,
    session: Session = Depends(get_session),
):
    measurement = crud.get_measurement(session, measurement_id)
    if measurement is None:
        raise HTTPException(status_code=404, detail="Pengukuran tidak ditemukan")
    sensor = crud.get_sensor(session, data.sensor_id)
    if sensor is None:
        raise HTTPException(status_code=404, detail="Sensor tidak ditemukan")
    return crud.update_measurement(session, measurement, data)


@router.delete("/{measurement_id}")
def delete_measurement(
    measurement_id: int,
    session: Session = Depends(get_session),
):
    measurement = crud.get_measurement(session, measurement_id)
    if measurement is None:
        raise HTTPException(status_code=404, detail="Pengukuran tidak ditemukan")
    crud.delete_measurement(session, measurement)
    return {"ok": True}
