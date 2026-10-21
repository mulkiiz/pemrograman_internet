"""Endpoint pengukuran. Operator dapat mencatat data, admin mengelola semuanya."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

import crud
from database import get_session
from models import User
from schemas import MeasurementCreate, MeasurementRead, MeasurementUpdate
from security import get_current_user, require_roles

router = APIRouter(prefix="/measurements", tags=["Measurements"])


@router.post("/", response_model=MeasurementRead, status_code=status.HTTP_201_CREATED)
def create_measurement(
    data: MeasurementCreate,
    session: Session = Depends(get_session),
    _operator: User = Depends(require_roles("admin", "operator")),
) -> MeasurementRead:
    if crud.get_sensor(session, data.sensor_id) is None:
        raise HTTPException(status_code=404, detail="Sensor tidak ditemukan")
    return crud.create_measurement(session, data)


@router.get("/", response_model=list[MeasurementRead])
def read_measurements(
    session: Session = Depends(get_session),
    _user: User = Depends(get_current_user),
) -> list[MeasurementRead]:
    return crud.get_measurements(session)


@router.get("/{measurement_id}", response_model=MeasurementRead)
def read_measurement(
    measurement_id: int,
    session: Session = Depends(get_session),
    _user: User = Depends(get_current_user),
) -> MeasurementRead:
    measurement = crud.get_measurement(session, measurement_id)
    if measurement is None:
        raise HTTPException(status_code=404, detail="Pengukuran tidak ditemukan")
    return measurement


@router.put("/{measurement_id}", response_model=MeasurementRead)
def update_measurement(
    measurement_id: int,
    data: MeasurementUpdate,
    session: Session = Depends(get_session),
    _admin: User = Depends(require_roles("admin")),
) -> MeasurementRead:
    measurement = crud.get_measurement(session, measurement_id)
    if measurement is None:
        raise HTTPException(status_code=404, detail="Pengukuran tidak ditemukan")
    if crud.get_sensor(session, data.sensor_id) is None:
        raise HTTPException(status_code=404, detail="Sensor tidak ditemukan")
    return crud.update_measurement(session, measurement, data)


@router.delete("/{measurement_id}")
def delete_measurement(
    measurement_id: int,
    session: Session = Depends(get_session),
    _admin: User = Depends(require_roles("admin")),
) -> dict[str, bool]:
    measurement = crud.get_measurement(session, measurement_id)
    if measurement is None:
        raise HTTPException(status_code=404, detail="Pengukuran tidak ditemukan")
    crud.delete_measurement(session, measurement)
    return {"ok": True}
