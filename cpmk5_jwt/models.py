"""Model tabel untuk pengguna, sensor, dan pengukuran."""

from datetime import datetime

from pydantic import NaiveDatetime
from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    password_hash: str
    role: str = "viewer"
    is_active: bool = True


class Sensor(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    code: str = Field(index=True, unique=True)
    location: str
    parameter: str


class Measurement(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    sensor_id: int = Field(foreign_key="sensor.id", index=True)
    value: float
    unit: str
    # Versi lama (datetime biasa):
    # measured_at: datetime = Field(default_factory=datetime.now)
    # NaiveDatetime dipakai karena waktu praktikum ini disimpan sebagai waktu lokal tanpa zona waktu.
    measured_at: NaiveDatetime = Field(default_factory=datetime.now)
