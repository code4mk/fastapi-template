from fastapi import APIRouter
from fastapi_pundra.rest import auto_bind_router

router = APIRouter()

# Auto-discover and bind all routers from app.api package
auto_bind_router(router, "app.api")
