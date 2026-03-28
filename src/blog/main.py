
from blog.database import Base, engine
from blog.typing import schema
from . import models
from fastapi import FastAPI
from .router import blog, user, authentication
from .limiter import limiter, RateLimitExceeded, _rate_limit_exceeded_handler
from ariadne.asgi import GraphQL

from blog.database import sessionlocal

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
app.add_websocket_route(
    "/graphql", GraphQL(schema, context_value=get_context_value))


app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


app.include_router(blog.router)
app.include_router(user.user_router)
app.include_router(authentication.auth_router)
