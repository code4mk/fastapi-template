from fastapi import HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from jose import JWTError, jwt
from typing import Optional
from app.utils.jwt_utils import decode_token
from app.config.authorization import EXCLUDE_PATHS
from fastapi_pundra.rest.exceptions import UnauthorizedException

class AuthorizationMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        

    def verify_access_token(self, request) -> Optional[dict]:
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            raise UnauthorizedException(message="No authorization header")

        try:
            scheme, token = auth_header.split()
            if scheme.lower() != "bearer":
                raise UnauthorizedException(message="Invalid authentication scheme")
            
            return decode_token(token)
            
        except JWTError:
            raise UnauthorizedException(message="Invalid token")

    async def dispatch(self, request, call_next):
        try:
            # Skip token verification for certain paths (optional)
            request_path = request.url.path.rstrip('/')  # Remove trailing slash if present
            if any(request_path == excluded.rstrip('/') for excluded in EXCLUDE_PATHS):
                return await call_next(request)

            # Verify the token and get payload
            payload = self.verify_access_token(request)
            # Add the payload to request state for use in route handlers
            request.state.user = payload
            
            # Set additional state variables
            request.state.auth_user_id = payload.get("user_id")
            
            
            response = await call_next(request)
            return response
            
        except HTTPException as exc:
            return JSONResponse(content={"detail": exc.detail}, status_code=exc.status_code)
        except Exception as exc:
            return JSONResponse(content={"detail": f"Error: {str(exc)}"}, status_code=500)