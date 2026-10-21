from sqlmodel import SQLModel


class SensorCreate(SQLModel):
    code: str
    location: str
    parameter: str


class SensorUpdate(SensorCreate):
    pass


class SensorRead(SensorCreate):
    id: int


class MeasurementCreate(SQLModel):
    sensor_id: int
    value: float
    unit: str
    measured_at: str


class MeasurementUpdate(MeasurementCreate):
    pass


class MeasurementRead(MeasurementCreate):
    id: int
