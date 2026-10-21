# Pemrograman Internet — Modul Praktikum

Repositori ini memuat materi dan proyek praktikum berbasis Python untuk mata kuliah Pemrograman Internet.

- `cpmk4_fastapi/` — CRUD REST API sensor dengan FastAPI, SQLModel, dan SQLite.
- `cpmk5_jwt/` — REST API sensor dengan autentikasi JWT, role, dan contoh request Postman.

Setiap folder memiliki README dan `requirements.txt` masing-masing. File `.env`, database lokal, virtualenv, cache Python, dan log dikecualikan dari Git.

Kedua aplikasi memakai satu database lokal `lab_sensor.db` di folder utama ini. File tersebut tidak masuk Git. CPMK-4 tidak memakai login, jadi endpoint CPMK-4 dapat mengubah data yang juga dibaca CPMK-5; jalankan keduanya hanya untuk praktikum lokal dan jangan mengekspos CPMK-4 ke jaringan.
