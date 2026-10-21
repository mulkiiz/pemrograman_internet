"""Schema request dan response agar password hash tidak pernah dikirim."""

# from datetime import datetime  # impor versi lama, dipakai saat schema bertipe datetime biasa

from pydantic import BaseModel, ConfigDict, NaiveDatetime


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserPublic(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    role: str
    is_active: bool


class SensorCreate(BaseModel):
    code: str
    location: str
    parameter: str


class SensorUpdate(SensorCreate):
    pass


class SensorRead(SensorCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int


class MeasurementCreate(BaseModel):
    sensor_id: int
    value: float
    unit: str
    # Versi lama (datetime biasa): measured_at: datetime
    measured_at: NaiveDatetime


class MeasurementUpdate(MeasurementCreate):
    pass


class MeasurementRead(MeasurementCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int
