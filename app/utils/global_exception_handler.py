from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.utils.exceptions import BaseAPIException
  
def setup_exception_handlers(app: FastAPI):
    @app.exception_handler(BaseAPIException)
    async def api_exception_handler(request: Request, exc: BaseAPIException):
        return JSONResponse(
            status_code=exc.status_code,
            content=exc.to_dict()
        )