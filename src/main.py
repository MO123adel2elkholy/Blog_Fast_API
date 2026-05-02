from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.requests import Request
from fastapi.responses import PlainTextResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
from starlette.responses import FileResponse

app = FastAPI()
redis_path = "redis://localhost:6379"
limiter = Limiter(key_func=get_remote_address, storage_uri=redis_path)
app.state.limiter = limiter
# insted of using you can use alimite peroid for all applayed on all ennpoint _rate_limit_exceeded_handler
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


# limited using Slowapi (rate-limiting package )


@app.get("/limited")
@limiter.limit("1/minute")
async def homepage(request: Request):
    return PlainTextResponse("test")


@app.get("/limited2")
@limiter.limit("1/minute")
async def homepage2(request: Request):
    return PlainTextResponse("test")


# @app.get("/celery_task")
# async def celery_task1(request: Request):
#     task = celery_task.delay(1, 3, 4)
#     return PlainTextResponse(f"celery_task result  =>  {task}")


# limited using Fastapi-guard  (rate-limiting package )


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
