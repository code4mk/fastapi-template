# FastApi project template

## Setup project
```bash
# Activate virtual environment
pipenv shell

# Install dependencies
pipenv install
```

## Add env
* add env file in root directory
* copy from `.env.example`

```bash
.env
```

## Run project

run the project
```bash
uvicorn app.main:app --reload --port 8000
# or
./run-project.sh
```

## Database migration process with Alembic
Alembic is a database migration tool for SQLAlchemy.

### revision (migration)
you can use the following command to create a new migration file.

```bash
alembic revision --autogenerate -m "initial project"
```

this will create a new migration file in the `alembic/versions` directory.

### upgrade (migrate)
you can use the following command to migrate the database.

```bash
alembic upgrade head
```

## Directory structure

```bash
├── app/
│   ├── api/
│   │   ├── v1/
│   │   │   └── user.py
│   │   ├── health.py
│   │   └── root_index.py
│   ├── config/
│   │   ├── authorization.py
│   │   └── cors.py
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
│   ├── templates/
│   │   ├── mails/
│   │   │   ├── css/
│   │   │   │   └── mail.css
│   │   │   └── welcome_email.html
│   │   └── user.html
│   ├── utils/
│   │   ├── mailer/
│   │   │   ├── inline_css.py
│   │   │   ├── mail.py
│   │   │   └── mail_templating.py
│   │   ├── base.py
│   │   ├── jwt_utils.py
│   │   ├── paginate.py
│   │   ├── password.py
│   │   └── validation.py
│   ├── __init__.py
│   └── main.py
├── alembic/*
├── docker/*
├── alembic.ini
├── .env
├── .env.example
├── .gitignore
├── build.sh
├── Pipfile
├── Pipfile.lock
├── README.md
└── run-project.sh
```

> [!NOTE]  
> This project needs python 3.12 or higher

## postman collection documentation

* [postman collection documentation](https://documenter.getpostman.com/view/9920489/2sAYQZGBNJ)

## docs
* [linting and formatting](_docs/lint-formatting.md)
* [testing](_docs/testing.md)
