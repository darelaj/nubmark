# Nubmark backend

Fondasi Flask untuk layanan cloud opsional Nubmark. Saat ini hanya tersedia
health endpoint dan penanganan error JSON. Belum ada database, migrasi,
autentikasi, API koleksi, atau sinkronisasi Android.

## Menjalankan dengan Docker

Jalankan Docker Desktop dalam mode Linux containers. Dari root repository:

```powershell
docker compose up --build -d --wait
Invoke-RestMethod http://127.0.0.1:8000/api/v1/health
docker compose logs -f backend
```

Backend tersedia di `http://127.0.0.1:8000`, dengan respons health
`{"status":"ok"}`. Container menggunakan Gunicorn, berjalan sebagai user non-root,
dan memiliki health check HTTP. Dependency produksi dipasang dari `uv.lock`;
virtual environment lokal, tes, dan file `.env` tidak masuk build context.
PostgreSQL belum dijalankan karena fondasi backend belum memakai database.

Untuk mengganti port, set `$env:NUBMARK_BACKEND_PORT = "8080"` sebelum menjalankan
Compose. Batas request dapat diatur melalui `$env:NUBMARK_MAX_CONTENT_LENGTH`.
Port hanya dipublikasikan pada loopback perangkat lokal.

Setelah mengubah kode, jalankan kembali `docker compose up --build -d --wait`.
Tidak ada bind mount atau auto-reload pada konfigurasi ini.
Hentikan container dengan `docker compose down` dari root repository.

Dockerfile juga dapat digunakan langsung dari root repository:

```powershell
docker build -t nubmark-backend ./backend
docker run --rm -p 127.0.0.1:8000:8000 nubmark-backend
```

## Pengembangan lokal

Gunakan Python 3.12+ dan jalankan perintah dari folder `backend/`.
Dengan `uv`:

```powershell
uv sync --extra dev --locked
uv run --locked flask --app app:create_app run --debug
```

Server lokal tersedia di `http://127.0.0.1:5000`.
`GET /api/v1/health` mengembalikan `{"status":"ok"}`.
Endpoint ini memeriksa liveness proses, belum memeriksa koneksi database.

Alternatif menggunakan virtual environment dan pip:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e '.[dev]'
.\.venv\Scripts\python.exe -m flask --app app:create_app run --debug
```

Flag `--debug` hanya untuk pengembangan lokal. Konfigurasi menggunakan environment
variable dengan prefix `NUBMARK_`, misalnya `NUBMARK_MAX_CONTENT_LENGTH=1048576`
untuk batas body request 1 MiB. Nilai dibaca sebagai JSON bila valid. File
`.env.example` mendokumentasikan konfigurasi; `.env` tidak dimuat otomatis.
Belum ada fitur yang memerlukan secret atau kredensial database.

## Verifikasi

```powershell
uv run --locked pytest -q
uv run --locked ruff check .
uv run --locked ruff format --check .
```

## WSGI

Entrypoint WSGI adalah `wsgi:app`. Pada Linux, gunakan environment produksi:

```sh
uv sync --extra production --locked
uv run --locked gunicorn --bind 127.0.0.1:8000 wsgi:app
```

Gunicorn tidak mendukung Windows secara native. Deployment publik tetap
memerlukan reverse proxy HTTPS dan konfigurasi operasional tersendiri.

## Kontrak API

[OpenAPI](../docs/openapi.yaml) mendokumentasikan endpoint yang tersedia.
Error berisi `code`, `message`, dan `requestId`; semua respons memiliki header
`X-Request-ID` yang dibuat server. Tidak ada kebijakan CORS terbuka.

Implementasi mengikuti [PLAN.md](../docs/PLAN.md) dan [AGENTS.md](../AGENTS.md).
