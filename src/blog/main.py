import os

from ariadne.asgi import GraphQL
from dotenv import load_dotenv
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import FileResponse

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


@app.on_event("startup")
async def startup():
    redis = aioredis.from_url("redis://localhost")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")


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


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()


@app.get("/")
async def get():
    htmlpath = "static/html/index.html"
    return FileResponse(path=htmlpath, status_code=200)


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"You wrote: {data}", websocket)
            await manager.broadcast(f"Client #{client_id} says: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} left the chat")
