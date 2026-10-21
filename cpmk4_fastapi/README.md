# Praktikum Sensor - FastAPI, SQLModel, SQLite

Contoh proyek modular untuk CPMK-4 Pemrograman Internet. API menyimpan data sensor dan pengukuran dengan relasi satu-ke-banyak.

Modul langkah demi langkah dalam format PDF disertakan di folder ini sebagai `Modul_Praktikum_CPMK4_Python_FastAPI_SQLModel.pdf`.

## Struktur proyek

```text
cpmk4_fastapi/
|-- main.py                 # Membuat aplikasi dan memasang router
|-- database.py             # Engine SQLite, pembuatan tabel, sesi database
|-- models.py               # Model ORM Sensor dan Measurement
|-- schemas.py              # Bentuk data request dan response API
|-- crud.py                 # Fungsi akses data Create, Read, Update, Delete
|-- requirements.txt        # Paket Python
|-- routers/
|   |-- __init__.py
|   |-- sensors.py          # Endpoint sensor dan pengukuran per sensor
|   `-- measurements.py     # Endpoint CRUD pengukuran
`-- lab_sensor.db           # Dibuat otomatis saat aplikasi dijalankan
```

## Menjalankan di Windows

Buka PowerShell di folder proyek, lalu jalankan:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m uvicorn main:app --reload
```

Buka `http://127.0.0.1:8000/docs` untuk mencoba endpoint. Server API berjalan dengan Uvicorn; folder `htdocs` XAMPP dipakai sebagai lokasi file proyek, bukan untuk menjalankan FastAPI melalui Apache/PHP.

## Endpoint utama

| Metode | Endpoint | Operasi |
|---|---|---|
| POST | `/sensors/` | Membuat sensor |
| GET | `/sensors/` | Membaca semua sensor |
| GET | `/sensors/{sensor_id}` | Membaca satu sensor |
| PUT | `/sensors/{sensor_id}` | Mengganti data sensor |
| DELETE | `/sensors/{sensor_id}` | Menghapus sensor jika tidak punya pengukuran |
| GET | `/sensors/{sensor_id}/measurements` | Membaca pengukuran milik sensor |
| POST | `/measurements/` | Membuat pengukuran |
| GET | `/measurements/` | Membaca semua pengukuran |
| GET | `/measurements/{measurement_id}` | Membaca satu pengukuran |
| PUT | `/measurements/{measurement_id}` | Mengganti data pengukuran |
| DELETE | `/measurements/{measurement_id}` | Menghapus pengukuran |

## Contoh request

Sensor:

```json
{
  "code": "S-01",
  "location": "Panel Praktikum A",
  "parameter": "tegangan"
}
```

Pengukuran (gunakan `sensor_id` dari response pembuatan sensor):

```json
{
  "sensor_id": 1,
  "value": 220.5,
  "unit": "V",
  "measured_at": "2026-10-21T09:30:00"
}
```

Data tersimpan pada `lab_sensor.db` di folder kerja saat Uvicorn dijalankan. Pengukuran dihapus terlebih dahulu sebelum sensor yang memilikinya dapat dihapus.
