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
- **TaskIQ** - Distributed task queue
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
- `REDIS_URL` - Redis connection for taskiq

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
├── _docs/*                         # Documentation files
├── alembic/*                       # Database migration management
├── app/                            # Main application directory
│   ├── api/                        # API routes
│   │   ├── v1/
│   │   │   ├── task_schedule_sample.py
│   │   │   └── user.py
│   │   ├── health.py
│   │   ├── root_index.py
│   │   └── router.py
│   ├── config/                     # Application configuration
│   │   ├── authorization.py
│   │   └── cors.py
│   ├── lib/                        # Library modules
│   │   ├── database.py
│   │   └── tskq/*                   # TaskIQ utilities
│   ├── middleware/                 # Custom middleware
│   │   └── authorization_middleware.py
│   ├── models/                     # Database models
│   │   └── users.py
│   ├── schemas/                    # Pydantic schemas
│   │   └── user_schema.py
│   ├── serializers/                # Data serializers
│   │   └── user_serializer.py
│   ├── services/                   # Business logic services
│   │   ├── scheduler_service.py
│   │   └── user_service.py
│   ├── sql_files/                  # SQL query files
│   │   └── users/
│   │       ├── fetch-all-users.sql
│   │       └── fetch-single-user.sql
│   ├── tasks/
│   │   ├── my_schedule_task.py
│   │   └── my_task.py
│   ├── templates/                  # HTML templates
│   │   ├── mails/
│   │   │   ├── css/
│   │   │   │   └── mail.css
│   │   │   └── welcome_email.html
│   │   └── user.html
│   ├── tests/*                       # Test files
│   ├── utils/                      # Utility functions
│   │   ├── base.py
│   │   └── logger.py
│   ├── cli.py                      # CLI commands
│   ├── main.py                     # Application entry point
│   └── taskiq.py                   # TaskIQ configuration
├── docker/*                         # Docker configuration
├── scripts/*                       # Utility scripts
├── alembic.ini                     # Alembic configuration
├── pyproject.toml                  # Project dependencies and metadata
├── README.md                       # This file
├── ruff.toml                       # Ruff linter configuration
└── uv.lock                         # UV lock file
```

> [!NOTE]  
> This project needs python 3.12 or higher

## postman collection documentation

* [postman collection documentation](https://documenter.getpostman.com/view/9920489/2sAYQZGBNJ)

## docs
* [linting and formatting](_docs/lint-formatting.md)
* [testing](_docs/testing.md)
* [task scheduler](_docs/task_scheduler.md)
* [mailing](_docs/mailing.md)
* [containerization](_docs/containerization.md)
