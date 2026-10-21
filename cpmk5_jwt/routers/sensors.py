"""Endpoint sensor. Peran admin diperlukan untuk mengubah data."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

import crud
from database import get_session
from models import User
from schemas import MeasurementRead, SensorCreate, SensorRead, SensorUpdate
from security import get_current_user, require_roles

router = APIRouter(prefix="/sensors", tags=["Sensors"])


@router.post("/", response_model=SensorRead, status_code=status.HTTP_201_CREATED)
def create_sensor(
    data: SensorCreate,
    session: Session = Depends(get_session),
    _admin: User = Depends(require_roles("admin")),
) -> SensorRead:
    return crud.create_sensor(session, data)


@router.get("/", response_model=list[SensorRead])
def read_sensors(
    session: Session = Depends(get_session),
    _user: User = Depends(get_current_user),
) -> list[SensorRead]:
    return crud.get_sensors(session)


@router.get("/{sensor_id}/measurements", response_model=list[MeasurementRead])
def read_measurements_for_sensor(
    sensor_id: int,
    session: Session = Depends(get_session),
    _user: User = Depends(get_current_user),
) -> list[MeasurementRead]:
    if crud.get_sensor(session, sensor_id) is None:
        raise HTTPException(status_code=404, detail="Sensor tidak ditemukan")
    return crud.get_measurements_for_sensor(session, sensor_id)


@router.get("/{sensor_id}", response_model=SensorRead)
def read_sensor(
    sensor_id: int,
    session: Session = Depends(get_session),
    _user: User = Depends(get_current_user),
) -> SensorRead:
    sensor = crud.get_sensor(session, sensor_id)
    if sensor is None:
        raise HTTPException(status_code=404, detail="Sensor tidak ditemukan")
    return sensor


@router.put("/{sensor_id}", response_model=SensorRead)
def update_sensor(
    sensor_id: int,
    data: SensorUpdate,
    session: Session = Depends(get_session),
    _admin: User = Depends(require_roles("admin")),
) -> SensorRead:
    sensor = crud.get_sensor(session, sensor_id)
    if sensor is None:
        raise HTTPException(status_code=404, detail="Sensor tidak ditemukan")
    return crud.update_sensor(session, sensor, data)


@router.delete("/{sensor_id}")
def delete_sensor(
    sensor_id: int,
    session: Session = Depends(get_session),
    _admin: User = Depends(require_roles("admin")),
) -> dict[str, bool]:
    sensor = crud.get_sensor(session, sensor_id)
    if sensor is None:
        raise HTTPException(status_code=404, detail="Sensor tidak ditemukan")
    if crud.sensor_has_measurements(session, sensor_id):
        raise HTTPException(
            status_code=409,
            detail="Hapus pengukuran sensor terlebih dahulu",
        )
    crud.delete_sensor(session, sensor)
    return {"ok": True}
