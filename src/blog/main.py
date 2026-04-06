import os

from ariadne.asgi import GraphQL
from authlib.integrations.starlette_client import OAuth
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from starlette.middleware.sessions import SessionMiddleware

from blog.admin.setup import setup_admin
from blog.database import engine, sessionlocal
from blog.oauth2 import oauth
from blog.token import create_jwt
from blog.typing import schema

from . import models
from .limiter import RateLimitExceeded, _rate_limit_exceeded_handler, limiter
from .router import authentication, blog, user

load_dotenv()
# إنشاء الجداول لو مش موجودة
models.Base.metadata.create_all(engine)

app = FastAPI(title="Blog FastAPI GraphQL")

# Context middleware لإضافة db لكل request


async def get_context_value(request):
    db = sessionlocal()
    try:
        return {"request": request, "db": db}
    finally:
        pass  # session هيتقفل بعد الـ commit في resolver


app.add_route("/graphql", GraphQL(schema, context_value=get_context_value))
app.add_websocket_route("/graphql", GraphQL(schema, context_value=get_context_value))


app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

SECRET_KEY = os.getenv("SECRET_KEY")
app.add_middleware(SessionMiddleware, SECRET_KEY)

setup_admin(app)


# المسارات اللي مش عايزين نتحقق فيها من blacklist
exempt_routes = ["/login", "/user", "/user/forgot-password", "/user/reset-password"]

# app.add_middleware(CustomJWTMiddleware, exempt_paths=exempt_routes)

app.include_router(blog.router)
app.include_router(user.user_router)
app.include_router(authentication.auth_router)


# --- Endpoints ---

#  Handling Social authentication
# إعداد الـ OAuth
oauth = OAuth()
GITHUB_CLIENT_ID = "Ov23liuwcIQ10VofHCnp"
GITHUB_CLIENT_SECRET = "77f9d50fb85c7c2d84f79c08b2f93d758a43fa36"
# Google provider
oauth.register(
    name="google",
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)
# GitHub provider
oauth.register(
    name="github",
    client_id=GITHUB_CLIENT_ID,
    client_secret=GITHUB_CLIENT_SECRET,
    access_token_url="https://github.com/login/oauth/access_token",
    authorize_url="https://github.com/login/oauth/authorize",
    api_base_url="https://api.github.com/",
    client_kwargs={"scope": "user:email"},
)


@app.get("/login/{provider_name}")
async def login(provider_name: str, request: Request):
    client = getattr(oauth, provider_name, None)
    if not client:
        raise HTTPException(status_code=400, detail="Provider not supported")

    redirect_uri = request.url_for("auth_callback", provider_name=provider_name)
    print(request.url_for("auth_callback", provider_name="github"))
    return await client.authorize_redirect(request, redirect_uri)


@app.get("/auth/{provider_name}/callback")
async def auth_callback(provider_name: str, request: Request):
    client = getattr(oauth, provider_name, None)
    if not client:
        raise HTTPException(status_code=400, detail="Provider not supported")

    token = await client.authorize_access_token(request)

    # مثال Google
    if provider_name == "google":
        user_info = await client.parse_id_token(request, token)
        user_info["provider"] = "google"
    # مثال GitHub
    elif provider_name == "github":
        resp = await client.get("user", token=token)
        profile = resp.json()
        email_resp = await client.get("user/emails", token=token)
        emails = email_resp.json()
        primary_email = next((e["email"] for e in emails if e["primary"]), None)
        user_info = {
            "email": primary_email,
            "name": profile.get("name") or profile.get("login"),
            "provider": "github",
        }
        print("user github info ", user_info)

    jwt_token = create_jwt(user_info)
    return JSONResponse({"access_token": jwt_token, "user": user_info})
