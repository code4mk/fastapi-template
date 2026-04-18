from collections.abc import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker
from app.config.settings import settings

# Get database connection details from environment variables
db_connection = settings.db_connection
db_host = settings.db_host
db_port = settings.db_port
db_user = settings.db_user
db_password = settings.db_password
db_name = settings.db_name
db_sslmode = settings.db_sslmode

# Construct database URL
# example: postgresql://user:password@host:port/database?sslmode=prefer
SQLALCHEMY_DATABASE_URL = (
    f"{db_connection}://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}?sslmode={db_sslmode}"
)

# Create the SQLAlchemy engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create a session maker bound to the engine
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Declarative base class for database models
Base = declarative_base()


# Dependency function to get a database session
def get_db_session() -> Generator[Session, None, None]:
    """Get a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
