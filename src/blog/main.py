from ariadne.asgi import GraphQL
from dotenv import load_dotenv
from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware

from blog.admin.setup import setup_admin
from blog.database import engine, sessionlocal
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

import os

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

SECRET_KEY = os.getenv("SECRET_KEY")
app.add_middleware(SessionMiddleware, SECRET_KEY)

setup_admin(app)


app.include_router(blog.router)
app.include_router(user.user_router)
app.include_router(authentication.auth_router)
