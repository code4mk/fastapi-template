import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pundra.rest.global_exception_handler import setup_exception_handlers
from fastapi_pundra.rest.openapi import discover_schemas, generate_openapi_schema
from app.middleware.authorization_middleware import AuthorizationMiddleware
from app.api.router import router as api_router
from app.config.cors import CORS_CONFIG


# Load .env file
load_dotenv()


def create_application() -> FastAPI:
    """Create the FastAPI application."""
    application = FastAPI()

    # Setup global exception handler
    setup_exception_handlers(application)

    # Setup authorization middleware
    application.add_middleware(AuthorizationMiddleware)

    # Auto-include all API routes from app.api folder
    application.include_router(api_router)

    # CORS middleware
    application.add_middleware(
        CORSMiddleware,
        **CORS_CONFIG,
    )

    # Set custom OpenAPI schema with auto-discovered schemas
    schemas = discover_schemas("app.schemas")
    application.openapi = lambda: generate_openapi_schema(application, schemas)

    return application


# Create the FastAPI application
app = create_application()


def run() -> None:
    """Run the FastAPI application with uvicorn."""
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000)  # noqa: S104


def run_dev() -> None:
    """Run the FastAPI application with uvicorn in development mode."""
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)  # noqa: S104
