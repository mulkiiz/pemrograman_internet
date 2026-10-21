from sqlmodel import Field, Relationship, SQLModel


class Sensor(SQLModel, table=True):
    __tablename__ = "sensor"

    id: int | None = Field(default=None, primary_key=True)
    code: str = Field(index=True, unique=True)
    location: str
    parameter: str
    measurements: list["Measurement"] = Relationship(back_populates="sensor")


class Measurement(SQLModel, table=True):
    __tablename__ = "measurement"

    id: int | None = Field(default=None, primary_key=True)
    sensor_id: int = Field(foreign_key="sensor.id")
    value: float
    unit: str
    measured_at: str
    sensor: Sensor | None = Relationship(back_populates="measurements")
