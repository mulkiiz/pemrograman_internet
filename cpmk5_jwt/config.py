"""Konfigurasi sederhana dari file .env."""

import os

from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "")
if not SECRET_KEY or SECRET_KEY.startswith("GANTI_"):
    raise RuntimeError(
        "SECRET_KEY belum diatur. Salin .env.example menjadi .env "
        "dan isi SECRET_KEY dengan nilai acak."
    )

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./lab_sensor_secure.db")
