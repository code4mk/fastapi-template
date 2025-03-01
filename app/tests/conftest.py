import pytest
import os
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

from app.database.database import Base, get_db_session
from app.main import create_application

load_dotenv()

# Test database URL
TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/postgres")

# Create test engine
engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    # Print all table names and their columns
    inspector = inspect(engine)
    table_names = inspector.get_table_names()
    print("\nDatabase Schema:")
    print("=" * 50)
    for index, table in enumerate(table_names, 1):
        print(f"\n{index}: {table}")
    print("\n" + "=" * 50)
    
    yield
    # Drop all tables after all tests
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="session")
def app():
    # Set up
    app = create_application()

    # Override the get_db_session dependency
    def override_get_db_session():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db_session] = override_get_db_session
    return app


@pytest.fixture(scope="session")
def client(app):
    return TestClient(app)


@pytest.fixture(scope="function")
def db():
    try:        
        # Get database session
        db = TestingSessionLocal()
        yield db
    finally:
        pass
        db.close()
