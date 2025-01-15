from fastapi import HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from jose import JWTError, jwt
from typing import Optional
from app.utils.jwt_utils import decode_token
from app.config.authorization import EXCLUDE_PATHS

class AuthorizationMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        

    def verify_access_token(self, request) -> Optional[dict]:
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            raise HTTPException(status_code=401, detail="No authorization header")

        try:
            scheme, token = auth_header.split()
            if scheme.lower() != "bearer":
                raise HTTPException(status_code=401, detail="Invalid authentication scheme")
            
            return decode_token(token)
            
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid token")

    async def dispatch(self, request, call_next):
        try:
            # Skip token verification for certain paths (optional)
            if request.url.path in EXCLUDE_PATHS:
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