# FastAPI Project Template

A modern, production-ready FastAPI template with built-in features for rapid development and deployment.

## Features & Tech Stack

### Core Framework
- **FastAPI** - Modern, fast web framework for building APIs with automatic OpenAPI documentation
- **FastAPI Pundra** - Productivity companion for FastAPI development

### Database & ORM
- **SQLAlchemy** - Powerful SQL toolkit and Object-Relational Mapping (ORM)
- **Alembic** - Database migration management and version control

### Data Validation & Serialization
- **Pydantic** - Built-in DTO (Data Transfer Object) with automatic data validation
- **Schema Layer** - Organized schemas for request/response validation
- **Custom Serializers** - Flexible data transformation and formatting

### Task Management
- **TaskIQ** - Distributed task queue for background job processing
- **Task Scheduling** - Built-in support for scheduled and recurring tasks

### Security & Authentication
- **JWT Authentication** - Secure token-based user authentication
- **Authorization Middleware** - Role-based access control

### Development & Tools
- **UV** - Ultra-fast Python package manager and dependency resolver
- **Pytest** - Comprehensive testing framework with fixtures and factories
- **Ruff** - Lightning-fast Python linter and formatter
- **Docker** - Full containerization support with production-ready configurations

### Additional Features
- **Email Templates** - Built-in email templating system with HTML/CSS support
- **SQL File Management** - Organized raw SQL queries for complex operations
- **Structured Logging** - Built-in logging utilities for debugging and monitoring

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
# Start the FastAPI development server with auto reload
uv run start-server-dev

# Start the FastAPI server
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
