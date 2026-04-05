from fastapi import HTTPException, Request
from starlette.middleware.base import BaseHTTPMiddleware

from .jwt_blacklist import is_token_blacklisted


class CustomJWTMiddleware(BaseHTTPMiddleware):
    def init(self, app, exempt_paths=None):
        print("🔥 NEW MIDDLEWARE LOADED")
        super().init(app)
        self.exempt_paths = exempt_paths or []

    async def dispatch(self, request: Request, call_next):
        if request.url.path in self.exempt_paths:
            return await call_next(request)

        auth_header = request.headers.get("Authorization")

        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]

            if is_token_blacklisted(token):
                raise HTTPException(status_code=401, detail="Token revoked")
        else:
            raise HTTPException(status_code=401, detail="Unauthorized")

        return await call_next(request)
