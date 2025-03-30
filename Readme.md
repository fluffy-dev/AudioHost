# Audio Hosting API Documentation

## Overview

This project implements an asynchronous API for audio hosting, built using FastAPI, SQLAlchemy, PostgreSQL, and Docker. It features user authentication (including OAuth via Yandex), secure token management, and audio file uploads/storage.

---

## Tech Stack

### Backend Framework & Tools:
- **FastAPI** – High-performance asynchronous web framework.
- **SQLAlchemy** (async) – Asynchronous ORM for database interaction.
- **PostgreSQL** – Relational database.
- **Alembic** – Database migration management.
- **Pydantic & Pydantic-Settings** – Data validation and settings management.
- **Asyncpg** – Async PostgreSQL database driver.
- **Docker & Docker Compose** – Containerization and orchestration.

### Authentication:
- **JWT (JSON Web Tokens)** – Authentication & authorization mechanism.
- **Yandex OAuth** – External OAuth provider.

---

## Project Structure

The project follows a modular structure to keep concerns separated:

```
project_root/
├── src/
│   ├── api/                 # API routers
│   │   ├── auth/
│   │   ├── user/
│   │   ├── audio/
│   │   ├── yandex/
│   │   └── routes.py        # Main router configuration
│   ├── apps/                # Application logic, services, repositories
│   │   ├── auth/
│   │   ├── audio/
│   │   └── user/
│   ├── config/              # Configuration management
│   │   ├── database/
│   │   ├── security.py
│   │   ├── jwt_config.py
│   │   ├── yandex.py
│   │   ├── logging.py
│   │   └── project.py
│   ├── libs/                # Shared libraries and utilities
│   ├── app.py               # FastAPI application initialization
│   └── main.py              # Application entry point (uvicorn)
├── uploads/                 # Local storage for audio files
├── alembic.ini              # Alembic migrations configuration
├── Dockerfile               # Container build instructions
├── docker-compose.yml       # Docker-compose orchestration
├── requirements.txt         # Python dependencies
└── .env                     # Environment variables
```

---

## Running Locally with Docker

### Step-by-step setup:

1. **Prepare Environment:**

Create `.env` file:

```dotenv
DB_NAME=audio_host_db
DB_USER=audio_user
DB_PASSWORD=yourpassword
DB_HOST=db
DB_PORT=5432
YANDEX_CLIENT_ID=your_client_id
YANDEX_CLIENT_SECRET=your_client_secret
YANDEX_REDIRECT_URI=http://localhost:8000/v1/auth/yandex/callback
INTERNAL_SECRET=your_internal_secret
INTERNAL_TOKEN_EXPIRE_HOURS=1
AUDIO_STORAGE_PATH=uploads/audio
```

2. **Build and Run Containers:**

```bash
docker-compose up --build
```

3. **Run Migrations:**

Run Alembic migrations inside Docker:

```bash
docker-compose run --rm app alembic upgrade head
```

4. **Access API:**

The API documentation (Swagger UI) will be available at:

```
http://localhost:8000/docs
```

---

## Production Configuration

For production:

- **Secrets & Credentials:** Never expose `.env` publicly. Use secure secret-management solutions.
- **Persistent Storage:** Configure Docker volumes or external storage for persistent audio file storage.
- **SSL/TLS:** Use a reverse proxy (e.g., Nginx, Traefik) with HTTPS.
- **Monitoring & Logging:** Integrate centralized logging and monitoring solutions (ELK, Prometheus, Grafana).

---

## API Endpoints

| Method | Endpoint                        | Description                       | Auth Required |
|--------|---------------------------------|-----------------------------------|---------------|
| POST   | `/v1/auth/registration`         | User registration                 | ❌             |
| POST   | `/v1/auth/login`                | User login                        | ❌             |
| POST   | `/v1/auth/refresh`              | Refresh tokens                    | ✅             |
| POST   | `/v1/auth/logout`               | Logout (cookie clear)             | ✅             |
| GET    | `/v1/auth/me`                   | Get current user info             | ✅             |
| POST   | `/v1/auth/yandex/login`         | Yandex OAuth login redirect       | ❌             |
| GET    | `/v1/auth/yandex/callback`      | Yandex OAuth callback             | ❌             |
| POST   | `/v1/user/get_user`             | Retrieve user data                | ✅ (admin)     |
| PUT    | `/v1/user/update_user`          | Update user data                  | ✅ (admin)     |
| DELETE | `/v1/user/delete_user`          | Delete user                       | ✅ (admin)     |
| GET    | `/v1/audio/`                    | List user's audio files           | ✅             |
| POST   | `/v1/audio/file`                | Upload audio file                 | ✅             |
| GET    | `/v1/audio/file/{pk}`           | Stream audio file                 | ✅             |

---

## Technical Details

### Authentication
- JWT tokens set via secure, HTTP-only cookies.
- Refresh token rotation implemented for security.

### File Handling
- Audio files stored locally in `uploads/audio/`.
- Asynchronous I/O (`aiofiles`) used for efficient file handling.

### Database Migrations
- Managed via Alembic, automated inside Docker container.
- Ensure migrations run before application start.

---

If i have missed something or done something wrong please contact me 