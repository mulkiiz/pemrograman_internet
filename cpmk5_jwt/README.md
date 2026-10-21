# Praktikum CPMK-5: REST API Sensor dengan JWT

Proyek lanjutan dari praktikum CPMK-4. API ini menggunakan Python, FastAPI, SQLModel, dan SQLite. Mahasiswa mempraktikkan login JWT, hash password, dan otorisasi berbasis peran pada API pemantauan sensor tegangan dan arus.

Peringatan: akun dan password di bawah hanya untuk praktikum lokal. Jangan gunakan konfigurasi demo ini untuk layanan produksi atau jaringan publik.

## Isi folder

```text
cpmk5_jwt/
|-- main.py                 # Membuat aplikasi dan memasang router
|-- config.py               # Membaca secret, masa token, dan URL database
|-- database.py             # Engine SQLite, tabel, dan dependency sesi
|-- models.py               # Model User, Sensor, dan Measurement
|-- schemas.py              # Bentuk request dan response API
|-- crud.py                 # Operasi Create, Read, Update, Delete
|-- security.py             # Hash password, JWT, identitas, dan pemeriksaan role
|-- seed.py                 # Akun dan data contoh untuk praktikum lokal
|-- routers/
|   |-- auth.py             # Login token dan profil pengguna aktif
|   |-- sensors.py          # Endpoint CRUD sensor dan riwayat pengukuran
|   `-- measurements.py     # Endpoint CRUD pengukuran
|-- requirements.txt
|-- .env.example            # Template konfigurasi lokal
|-- praktikum_cpmk5.postman_collection.json
|-- praktikum_cpmk5.postman_environment.json
`-- Modul_Praktikum_CPMK5_Python_JWT.pdf
```

File `lab_sensor_secure.db` dibuat otomatis saat aplikasi pertama kali dijalankan. File `.env` dan database lokal tidak untuk diunggah ke repository.

## Kebutuhan

- Python 3.10 atau lebih baru
- PowerShell pada Windows
- Internet untuk memasang paket Python pada langkah pertama
- Browser untuk Swagger UI (`/docs`); Postman bersifat opsional

XAMPP tidak menjalankan FastAPI melalui Apache atau PHP. Folder `htdocs` hanya menjadi tempat menyimpan proyek; server API dijalankan oleh Uvicorn.

## Menjalankan aplikasi

Buka PowerShell, masuk ke folder proyek, lalu buat lingkungan virtual:

```powershell
cd C:\xampp\htdocs\pemrogramaninternet\cpmk5_jwt
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Buat file `.env` dari template:

```powershell
Copy-Item .env.example .env
```

Buat secret acak untuk menandatangani JWT:

```powershell
py -c "import secrets; print(secrets.token_urlsafe(32))"
```

Buka `.env` dengan editor teks dan ganti nilai `SECRET_KEY` menggunakan hasil perintah. Jangan membagikan secret ini. Baris lain dapat dibiarkan:

```text
SECRET_KEY=isi_dengan_hasil_secret_acak
ACCESS_TOKEN_EXPIRE_MINUTES=30
DATABASE_URL=sqlite:///./lab_sensor_secure.db
```

Jalankan server dari folder proyek:

```powershell
.\.venv\Scripts\python.exe -m uvicorn main:app --reload
```

Buka `http://127.0.0.1:8000/docs`. Biarkan terminal server tetap terbuka selama praktikum.

## Akun latihan dan peran

Akun berikut dibuat otomatis pada awal aplikasi. Password disimpan sebagai hash Argon2 di SQLite, bukan sebagai teks asli.

| Username | Password latihan | Peran | Hak akses utama |
|---|---|---|---|
| `admin` | `AdminLab!2026` | admin | Membaca dan mengelola sensor serta pengukuran |
| `operator` | `OperatorLab!2026` | operator | Membaca sensor/pengukuran dan menambah pengukuran |
| `viewer` | `ViewerLab!2026` | viewer | Hanya membaca sensor dan pengukuran |

## Alur percobaan di Swagger

Ada dua cara untuk login dan memakai endpoint yang dilindungi. Pilih salah satu.

### Cara A — Form login Swagger

1. Klik **Authorize** di bagian atas Swagger.
2. Pada skema `OAuth2PasswordBearer`, isi username dan password. Contoh: `operator` dan `OperatorLab!2026`. Biarkan `client_id`, `client_secret`, dan `scope` kosong.
3. Klik **Authorize**, lalu **Close**. Swagger otomatis mengirim kredensial ke `POST /auth/token`, menyimpan token, dan melampirkannya ke request berikutnya.

### Cara B — Jalankan `POST /auth/token` sendiri

1. Buka endpoint `POST /auth/token`, klik **Try it out**, isi `username` dan `password`, lalu klik **Execute**. Response `200` berisi `access_token`.
2. Salin nilai `access_token` saja (tanpa tanda kutip). Klik **Authorize**, pilih skema `ManualBearerToken`, lalu tempel token tersebut. Jangan tambahkan awalan `Bearer `; Swagger yang menambahkannya.
3. Klik **Authorize**, lalu **Close**. Sekarang Swagger melampirkan token itu ke request berikutnya.

Untuk kedua cara, coba `GET /auth/me` untuk melihat pengguna aktif, lalu `GET /sensors/` atau `GET /sensors/1/measurements` untuk membaca data sensor.

Sebagai `operator`, jalankan `POST /measurements/` dengan body berikut. Ganti `sensor_id` bila ID sensor di response Anda berbeda:

```json
{
  "sensor_id": 1,
  "value": 221.4,
  "unit": "V",
  "measured_at": "2026-10-21T10:00:00"
}
```

1. Jalankan lagi `GET /sensors/1/measurements`; data pengukuran baru akan muncul.
2. Klik **Authorize**, keluar dari token yang sedang aktif bila perlu, lalu masuk sebagai `viewer`. Coba `POST /measurements/`: response yang diharapkan `403 Forbidden`.
3. Ulangi login sebagai `admin`. Coba membuat sensor dengan `POST /sensors/`, lalu ubah atau hapus data latihan.

## Matriks hak akses

Semua endpoint membutuhkan token, kecuali `POST /auth/token` dan `GET /`.

| Operasi | admin | operator | viewer |
|---|---:|---:|---:|
| Membaca sensor, pengukuran, dan profil sendiri | Ya | Ya | Ya |
| Membuat pengukuran | Ya | Ya | Tidak |
| Membuat, mengubah, dan menghapus sensor | Ya | Tidak | Tidak |
| Mengubah dan menghapus pengukuran | Ya | Tidak | Tidak |

## Daftar endpoint

| Metode | Endpoint | Peran |
|---|---|---|
| POST | `/auth/token` | Publik untuk login |
| GET | `/auth/me` | Semua pengguna yang login |
| POST | `/sensors/` | admin |
| GET | `/sensors/`, `/sensors/{id}` | Semua pengguna yang login |
| PUT, DELETE | `/sensors/{id}` | admin |
| GET | `/sensors/{id}/measurements` | Semua pengguna yang login |
| POST | `/measurements/` | admin, operator |
| GET | `/measurements/`, `/measurements/{id}` | Semua pengguna yang login |
| PUT, DELETE | `/measurements/{id}` | admin |

## Menguji dengan Postman

1. Import `praktikum_cpmk5.postman_collection.json` dan `praktikum_cpmk5.postman_environment.json`.
2. Pilih environment `Praktikum CPMK-5 - Lokal`.
3. Jalankan request `1 - Login operator`. Script pada collection menyimpan token ke environment.
4. Jalankan request `2 - Profil pengguna`, `3 - Daftar sensor`, `4 - Tambah pengukuran`, lalu `5 - Daftar pengukuran`.

Postman hanya salah satu cara uji; Swagger UI sudah cukup untuk mengikuti langkah utama.

## Cara membaca alur keamanan

1. `/auth/token` memeriksa username dan password terhadap user di database.
2. Password dibandingkan dengan hash Argon2. Password asli tidak dikirim kembali atau disimpan.
3. Server membuat JWT bertanda tangan yang memiliki `sub` (username) dan waktu `exp` (kedaluwarsa).
4. Client mengirim token pada header `Authorization: Bearer ...`.
5. `get_current_user()` memverifikasi tanda tangan, masa token, status akun, dan mengambil role terbaru dari database.
6. `require_roles()` mengizinkan atau menolak operasi. `401` berarti autentikasi gagal/tidak ada; `403` berarti sudah login tetapi role tidak berhak.

JWT pada contoh ini ditandatangani, bukan dienkripsi. Jangan memasukkan password, secret, atau data rahasia ke payload token.

## Tugas mahasiswa

1. Gunakan token viewer untuk membuktikan satu endpoint baca berhasil dan satu endpoint tulis ditolak. Catat status HTTP dan jelaskan perbedaan `401` dengan `403`.
2. Tambahkan endpoint `GET /sensors/{sensor_id}/measurements` yang hanya dapat dibuka oleh admin dan operator. Uji ketiga role.
3. Ubah masa berlaku token menjadi 2 menit, login kembali, tunggu token kedaluwarsa, lalu amati response API.
4. Buat satu sensor baru dengan parameter `daya`, lalu catat pengukuran dalam satuan `W` sebagai operator.
5. Jelaskan mengapa client tidak boleh memilih role `admin` sendiri saat mendaftar. Dalam proyek ini role hanya dibuat di `seed.py` agar role tidak dikendalikan oleh pengguna publik.

## Troubleshooting singkat

- **`SECRET_KEY belum diatur`**: pastikan `.env` berada di folder proyek dan nilai `SECRET_KEY` sudah diganti dari placeholder.
- **PowerShell tidak menemukan `py`**: pasang Python dari python.org dan aktifkan pilihan menambahkan Python ke PATH, atau gunakan path `python.exe` yang tersedia.
- **`401 Unauthorized`**: token belum dikirim, password salah, atau token kedaluwarsa. Login ulang melalui `/auth/token`.
- **`403 Forbidden`**: login berhasil, tetapi role tidak memiliki hak endpoint itu. Coba akun dengan peran yang sesuai.
- **`422 Unprocessable Entity`**: periksa field JSON, tipe angka, format waktu ISO, dan `sensor_id`.
- **Data tidak muncul**: periksa `sensor_id` pada body dan gunakan `GET /measurements/` untuk melihat semua pengukuran.
- **File database berbeda**: jalankan Uvicorn dari folder proyek yang sama agar SQLite menggunakan `lab_sensor_secure.db` yang dimaksud.

## Batas praktikum

Contoh ini untuk pembelajaran lokal. Akun latihan dan secret `.env` harus diganti sebelum dibagikan atau di-deploy. Untuk sistem nyata, gunakan HTTPS, pengelolaan secret yang aman, kebijakan rotasi/revokasi token, pencatatan audit, pembatasan percobaan login, dan pengujian keamanan tambahan.
