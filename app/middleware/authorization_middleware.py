from collections.abc import Callable, Awaitable
from datetime import datetime, UTC
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from fastapi_pundra.common.jwt_utils import decode_token
from fastapi_pundra.rest.exceptions import UnauthorizedException
from jose import JWTError
from starlette.middleware.base import BaseHTTPMiddleware

from app.config.authorization import EXCLUDE_PATHS
from app.lib.auth_path_utils import excluded_path_checker

_path_skips_auth = excluded_path_checker(EXCLUDE_PATHS)


class AuthorizationMiddleware(BaseHTTPMiddleware):
    """Authorization middleware."""

    def __init__(self, app: FastAPI) -> None:
        """Initialize the middleware."""
        super().__init__(app)

    def verify_access_token(self, request: Request) -> dict | None:
        """Verify the access token."""
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            raise UnauthorizedException(message="No authorization header")

        try:
            scheme, token = auth_header.split()
            if scheme.lower() != "bearer":
                raise UnauthorizedException(message="Invalid authentication scheme")

            return decode_token(token)

        except JWTError as err:
            raise UnauthorizedException(message="Invalid token") from err

    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        """Dispatch the middleware."""
        try:
            # Skip token verification for configured paths (exact, prefix /*, segment *)
            if _path_skips_auth(request.url.path):
                return await call_next(request)

            # Verify the token and get payload
            payload = self.verify_access_token(request)
            # Add the payload to request state for use in route handlers
            request.state.user = payload

            # Set additional state variables
            request.state.auth_user_id = payload.get("user_id")

            return await call_next(request)

        except UnauthorizedException as exc:
            error_response = exc.to_dict()
            error_response["path"] = request.url.path
            error_response["type"] = exc.__class__.__name__
            error_response["timestamp"] = datetime.now(UTC).isoformat()

            return JSONResponse(content=error_response, status_code=exc.status_code)
