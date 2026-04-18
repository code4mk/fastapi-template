# FastAPI Project Template

A modern, production-ready FastAPI template with built-in features for rapid development and deployment.

## Features & Tech Stack

### Core Framework
- **FastAPI** - Modern, fast web framework for building APIs with automatic OpenAPI documentation
- **FastAPI Pundra** - Productivity companion for FastAPI (global exception handling, OpenAPI schema discovery, `auto_bind_router` for API modules)
- **Auto Route Discovery** - Routers under `app.api` are discovered and mounted automatically

### Database & ORM
- **PostgreSQL** - Default target database (connection built from settings; `psycopg2-binary` driver)
- **SQLAlchemy** - SQL toolkit and ORM
- **Alembic** - Database migration management and version control

### Configuration & Validation
- **Pydantic** - Request/response models and validation
- **Pydantic Settings** - Typed configuration from environment variables (`app/config/settings.py`)
- **Schema Layer** - Organized schemas under `app.schemas` with OpenAPI discovery
- **Custom Serializers** - Flexible data transformation under `app/serializers`

### Task Management
- **TaskIQ** - Async task queue for background jobs
- **taskiq-redis** - Redis broker for TaskIQ
- **Task Scheduling** - Sample scheduled tasks and scheduler scripts under `scripts/`

### Security & Authentication
- **JWT Authentication** - Bearer tokens via `fastapi-pundra` JWT utilities
- **Authorization Middleware** - Validates JWT on protected routes; public routes are configured in `EXCLUDE_PATHS` (`app/config/authorization.py`)
- **Path Rules** - Prefix, segment-wildcard, and exact path matching for public routes (`app/lib/auth_path_utils.py`)

### HTTP & Integrations
- **HTTPX** - Async-friendly HTTP client; shared helpers in `app/lib/httpx_client.py`

### Development & Tools
- **UV** - Python package manager and lockfile (`uv.lock`)
- **Pytest** - Tests with `pytest-asyncio`, `pytest-cov`, factories (`factory-boy` / `faker`), and `app/tests/conftest.py`
- **Ruff** - Linter/formatter (`ruff.toml`; also run via pre-commit)
- **Pre-commit** - Git hooks (install with `uv run pre-commit-install` or use `uv run lint` to run hooks on all files)
- **Docker** - Sample app Dockerfile and supervisor config under `docker/`

### Additional Features
- **Email** - `fastapi-mail`, Jinja2 templates, and premailer/inline CSS under `app/templates/mails/`
- **SQL File Management** - Raw SQL files under `app/sql_files/`
- **Structured Logging** - **Loguru**-based logging (`app/utils/logger.py`)

## Prerequisites

- Python 3.12 or higher
- [UV](https://github.com/astral-sh/uv) package manager (recommended)
- **PostgreSQL** (or adjust `db_*` settings in `.env` to match your database)

## Quick Start

### 1. Setup Project

Clone the repository and install dependencies:

```bash
# Install dependencies
uv sync

# Install with development dependencies (recommended for development)
uv sync --extra dev
```

> **Note**: The `--extra dev` flag installs testing tools, Ruff, pre-commit, and related dev dependencies.

### 2. Environment Configuration

Create your environment configuration:

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env: database host/user/password/name, SSL mode, project port, test DB URL, etc.
# Settings are loaded in app/config/settings.py (Pydantic Settings).
```

### 3. Database Setup

This project uses **Alembic** for database schema management and migrations.

Initialize and upgrade your database:

```bash
# Run database migrations
uv run db-upgrade

# Create a new database revision (message in quotes)
uv run db-revision "Initial database setup"
```

### 4. Run the Application

Start the development server:

```bash
# Development: auto-reload (port from settings, default 8000)
uv run start-server-dev

# Production-style: no reload
uv run start-server
```

The API will be available at (host/port depend on your settings; defaults shown):

- **API**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### 5. Optional: Git hooks & tests

```bash
# Install pre-commit hooks (once per clone)
uv run pre-commit-install

# Run the full lint pipeline (pre-commit on all files)
uv run lint

# Tests with coverage (project script enforces coverage thresholds)
bash scripts/test.sh

# Or run pytest directly (see pyproject.toml for default pytest options)
uv run pytest
```

## Project CLI entry points

Defined in `pyproject.toml` under `[project.scripts]`:

| Command | Purpose |
|--------|---------|
| `uv run start-server` | Run the app with Uvicorn (no reload) |
| `uv run start-server-dev` | Run with reload |
| `uv run db-upgrade` | `alembic upgrade head` |
| `uv run db-revision "message"` | `alembic revision --autogenerate` |
| `uv run lint` | Run pre-commit on all files |
| `uv run pre-commit-install` | `pre-commit install` |

## Directory structure

```text
├── _docs/                          # Extra documentation (see below)
├── alembic/                        # Alembic env and migration versions
├── app/
│   ├── api/                        # HTTP routes (auto-bound from app.api)
│   │   ├── v1/
│   │   │   ├── task_schedule_sample.py
│   │   │   └── user.py
│   │   ├── health.py
│   │   ├── root_index.py
│   │   └── router.py
│   ├── config/                     # Settings, CORS, authorization lists
│   │   ├── authorization.py       # EXCLUDE_PATHS (JWT not required)
│   │   ├── cors.py
│   │   └── settings.py            # Pydantic Settings / env
│   ├── lib/
│   │   ├── auth_path_utils.py     # Public-path matching for middleware
│   │   ├── database.py            # Engine, session, Base
│   │   ├── dot_env_loader.py
│   │   ├── httpx_client.py
│   │   └── tskq/                  # TaskIQ broker, scheduler helpers, invoker
│   ├── middleware/
│   │   └── authorization_middleware.py
│   ├── models/
│   │   └── users.py
│   ├── schemas/
│   │   └── user_schema.py
│   ├── serializers/
│   │   └── user_serializer.py
│   ├── services/
│   │   ├── scheduler_service.py
│   │   └── user_service.py
│   ├── sql_files/users/           # Example raw SQL
│   ├── tasks/                     # TaskIQ task modules
│   ├── templates/                 # Jinja (e.g. mail HTML)
│   ├── tests/                     # pytest: unit/, integration/, factories/, fixtures/
│   ├── utils/
│   │   ├── base.py
│   │   └── logger.py              # Loguru setup
│   ├── cli.py                     # db-upgrade, db-revision, lint, pre-commit-install
│   ├── main.py                    # FastAPI app factory
│   └── taskiq.py                  # TaskIQ app/broker wiring
├── docker/
│   ├── config/supervisor/
│   └── dockerfiles/
├── scripts/                       # test.sh, lint.sh, format.sh, taskiq-*.sh, deploy.sh, etc.
├── .coveragerc
├── .pre-commit-config.yaml
├── alembic.ini
├── pyproject.toml
├── ruff.toml
├── uv.lock
└── README.md
```

> [!NOTE]  
> This project requires Python 3.12 or higher.

## Postman collection documentation

* [Postman collection documentation](https://documenter.getpostman.com/view/9920489/2sAYQZGBNJ)

## Docs

* [Linting and formatting](_docs/lint-formatting.md)
* [Testing](_docs/testing.md)
* [Authorization & public paths](_docs/authorization.md)
* [HTTPX client](_docs/httpx-client.md)
* [Task scheduler](_docs/task_scheduler.md)
* [Mailing](_docs/mailing.md)
* [Containerization](_docs/containerization.md)
