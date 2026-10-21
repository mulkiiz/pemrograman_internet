"""Membuat akun dan data demo satu kali saat aplikasi pertama dijalankan."""

from datetime import datetime

from sqlmodel import Session, select

import crud
from models import Measurement, Sensor
from security import hash_password

DEMO_ACCOUNTS = [
    ("admin", "AdminLab!2026", "admin"),
    ("operator", "OperatorLab!2026", "operator"),
    ("viewer", "ViewerLab!2026", "viewer"),
]


def seed_demo_data(session: Session) -> None:
    """Akun demo hanya untuk latihan lokal, bukan untuk deployment."""
    for username, password, role in DEMO_ACCOUNTS:
        if crud.get_user_by_username(session, username) is None:
            crud.create_user(session, username, hash_password(password), role)

    if session.exec(select(Sensor)).first() is None:
        session.add_all(
            [
                Sensor(code="S-01", location="Panel Praktikum A", parameter="tegangan"),
                Sensor(code="S-02", location="Panel Praktikum B", parameter="arus"),
            ]
        )
        session.commit()

    if session.exec(select(Measurement)).first() is None:
        sensor = session.exec(select(Sensor).where(Sensor.code == "S-01")).first()
        if sensor is not None and sensor.id is not None:
            session.add(
                Measurement(
                    sensor_id=sensor.id,
                    value=220.5,
                    unit="V",
                    measured_at=datetime(2026, 10, 21, 9, 30),
                )
            )
            session.commit()
