from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pundra.rest.global_exception_handler import setup_exception_handlers

from app.api import health, root_index
from app.api.v1 import user
from app.config.cors import CORS_CONFIG
from app.middleware.authorization_middleware import AuthorizationMiddleware

# Load .env file
load_dotenv()


def create_application() -> FastAPI:
    """Create the FastAPI application."""
    application = FastAPI()

    # Setup global exception handler
    setup_exception_handlers(application)

    # Setup authorization middleware
    application.add_middleware(AuthorizationMiddleware)

    # Include the root index and health router
    application.include_router(root_index.router)
    application.include_router(health.router, prefix="/health")

    # Include all the api routes
    application.include_router(user.router, prefix="/api/v1")

    # CORS middleware
    application.add_middleware(
        CORSMiddleware,
        **CORS_CONFIG,
    )

    return application


# Create the FastAPI application
app = create_application()
