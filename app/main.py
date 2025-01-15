import os
from fastapi import FastAPI
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from app.api import health, root_index
from app.config.cors import CORS_CONFIG
from app.utils.validation import setup_validation_exception_handler
from app.middleware.authorization_middleware import AuthorizationMiddleware

from app.api.v1 import user

# Load .env file
load_dotenv()

def create_application():
    application = FastAPI()

    # Setup validation exception handler
    setup_validation_exception_handler(application)

    application.add_middleware(AuthorizationMiddleware)
    
    # Include the root index and health router
    application.include_router(root_index.router)
    application.include_router(health.router, prefix="/health")

    # Include all the api routes
    application.include_router(user.router, prefix="/api/v1")

    #CORS middleware
    application.add_middleware(
        CORSMiddleware,
        **CORS_CONFIG,
    )
    
    return application

# Create the FastAPI application
app = create_application()