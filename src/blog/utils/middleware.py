from fastapi import HTTPException, Request
from starlette.middleware.base import BaseHTTPMiddleware

from .jwt_blacklist import is_token_blacklisted


class NextMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)

        next_url = request.query_params.get("next")
        if next_url:
            # save next both as cookie and in session so POST login can reliably read it
            response.set_cookie("next", next_url, path="/", max_age=300)
            try:
                # session is available because SessionMiddleware added earlier
                request.session["next"] = next_url
            except Exception:
                pass
        return response


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
