from sqlmodel import Session, select

from models import Measurement, Sensor
from schemas import MeasurementCreate, MeasurementUpdate, SensorCreate, SensorUpdate


def create_sensor(session: Session, data: SensorCreate) -> Sensor:
    sensor = Sensor.model_validate(data)
    session.add(sensor)
    session.commit()
    session.refresh(sensor)
    return sensor


def get_sensors(session: Session) -> list[Sensor]:
    statement = select(Sensor).order_by(Sensor.id)
    return session.exec(statement).all()


def get_sensor(session: Session, sensor_id: int) -> Sensor | None:
    return session.get(Sensor, sensor_id)


def update_sensor(
    session: Session, sensor: Sensor, data: SensorUpdate
) -> Sensor:
    for key, value in data.model_dump().items():
        setattr(sensor, key, value)
    session.add(sensor)
    session.commit()
    session.refresh(sensor)
    return sensor


def sensor_has_measurements(session: Session, sensor_id: int) -> bool:
    statement = select(Measurement.id).where(Measurement.sensor_id == sensor_id)
    return session.exec(statement).first() is not None


def delete_sensor(session: Session, sensor: Sensor) -> None:
    session.delete(sensor)
    session.commit()


def create_measurement(session: Session, data: MeasurementCreate) -> Measurement:
    measurement = Measurement.model_validate(data)
    session.add(measurement)
    session.commit()
    session.refresh(measurement)
    return measurement


def get_measurements(session: Session) -> list[Measurement]:
    statement = select(Measurement).order_by(Measurement.id)
    return session.exec(statement).all()


def get_measurement(session: Session, measurement_id: int) -> Measurement | None:
    return session.get(Measurement, measurement_id)


def get_measurements_for_sensor(
    session: Session, sensor_id: int
) -> list[Measurement]:
    statement = (
        select(Measurement)
        .where(Measurement.sensor_id == sensor_id)
        .order_by(Measurement.id)
    )
    return session.exec(statement).all()


def update_measurement(
    session: Session, measurement: Measurement, data: MeasurementUpdate
) -> Measurement:
    for key, value in data.model_dump().items():
        setattr(measurement, key, value)
    session.add(measurement)
    session.commit()
    session.refresh(measurement)
    return measurement


def delete_measurement(session: Session, measurement: Measurement) -> None:
    session.delete(measurement)
    session.commit()
