# FastAPI Project Template

A modern, production-ready FastAPI template with built-in features for rapid development and deployment.

## Features

- **FastAPI** - Modern, fast web framework for building APIs
- **FastAPI Pundra** - FastAPI Companion for Productivity
- **SQLAlchemy** - Powerful SQL toolkit and ORM
- **Alembic** - Database migration management
- **Pytest** - Comprehensive testing framework
- **UV** - Ultra-fast Python package manager
- **Email Templates** - Built-in email templating system
- **JWT Authentication** - Secure user authentication
- **Docker** - Containerization support
- **Celery** - Distributed task queue
- **Ruff** - Lightning-fast Python linter and formatter

## Prerequisites

- Python 3.12 or higher
- UV package manager (recommended)

## Quick Start

### 1. Setup Project

Clone the repository and install dependencies:

```bash
# Install dependencies
uv sync

# Install with development dependencies (recommended for development)
uv sync --extra dev
```

> **Note**: The `--extra dev` flag installs additional development tools like testing frameworks, linters, and formatters.

### 2. Environment Configuration

Create your environment configuration:

```bash
# Copy the example environment file
cp .env.example .env

# Edit the .env file with your specific configuration
# Configure database URL, secret keys, email settings, etc.
```

**Important environment variables to configure:**
- `DATABASE_URL` - Your database connection string
- `SECRET_KEY` - JWT secret key for authentication
- `SMTP_*` - Email configuration for notifications
- `REDIS_URL` - Redis connection for Celery (if using background tasks)

### 3. Database Setup

This project uses **Alembic** for database schema management and migrations.

Initialize and upgrade your database:

```bash
# Run database migrations
uv run db-upgrade

# create a new database revision
uv run db-revision "Initial database setup"
```

### 4. Run the Application

Start the development server:

```bash
# Start the FastAPI development server
uv run start-server
```

The API will be available at:
- **API**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Directory structure

```bash
├── _docs/
│   ├── celery.md
│   ├── containerization.md
│   ├── lint-formatting.md
│   ├── mailing.md
│   └── testing.md
├── alembic/
│   ├── env.py
│   ├── README
│   ├── script.py.mako
│   └── versions/
├── app/
│   ├── api/
│   │   ├── v1/
│   │   │   └── user.py
│   │   ├── health.py
│   │   └── root_index.py
│   ├── config/
│   │   ├── authorization.py
│   │   ├── cors.py
│   │   └── scheduler.py
│   ├── database/
│   │   └── database.py
│   ├── middleware/
│   │   └── authorization_middleware.py
│   ├── models/
│   │   └── users.py
│   ├── schemas/
│   │   └── user_schema.py
│   ├── serializers/
│   │   └── user_serializer.py
│   ├── services/
│   │   └── user_service.py
│   ├── sql_files/
│   │   └── users/
│   │       ├── fetch-all-users.sql
│   │       └── fetch-single-user.sql
│   ├── tasks/
│   │   └── my_task.py
│   ├── templates/
│   │   ├── mails/
│   │   │   ├── css/
│   │   │   │   └── mail.css
│   │   │   └── welcome_email.html
│   │   └── user.html
│   ├── tests/
│   │   ├── conftest.py
│   │   ├── factories/
│   │   │   └── user_factory.py
│   │   ├── fixtures/
│   │   │   └── common.py
│   │   ├── integration/
│   │   │   ├── test_health.py
│   │   │   └── test_user.py
│   │   └── unit/
│   │       ├── test_user_services.py
│   │       └── test_users_models.py
│   ├── utils/
│   │   ├── base.py
│   │   └── logger.py
│   ├── celery.py
│   ├── cli.py
│   └── main.py
├── docker/
│   ├── config/
│   │   ├── nginx/
│   │   │   └── app.conf
│   │   └── supervisor/
│   │       └── supervisord.conf
│   └── dockerfiles/
│       └── app.Dockerfile
├── fastapi-pundra/
│   ├── deploy.sh
│   ├── fastapi_pundra/
│   │   ├── common/
│   │   ├── gql_berry/
│   │   └── rest/
│   ├── README.md
│   └── setup.py
├── logs/
│   └── app.log
├── scripts/
│   ├── deploy.sh
│   ├── docker_image_build.sh
│   ├── format.sh
│   ├── lint.sh
│   └── test.sh
├── alembic.ini
├── pyproject.toml
├── README.md
├── ruff.toml
└── uv.lock
```

> [!NOTE]  
> This project needs python 3.12 or higher

## postman collection documentation

* [postman collection documentation](https://documenter.getpostman.com/view/9920489/2sAYQZGBNJ)

## docs
* [linting and formatting](_docs/lint-formatting.md)
* [testing](_docs/testing.md)
