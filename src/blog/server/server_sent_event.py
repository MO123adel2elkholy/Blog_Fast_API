import asyncio
import json

from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from starlette.responses import FileResponse

clients = []


server_sent_event_router = APIRouter(
    tags=["sever-sent-evevnt"],
    prefix="/server",
)


@server_sent_event_router.get("/stream")
async def stream():
    async def event_generator():
        queue = asyncio.Queue()
        clients.append(queue)

        try:
            while True:
                data = await queue.get()
                yield f"data: {json.dumps(data)}\n\n"
        except asyncio.CancelledError:
            clients.remove(queue)

    return StreamingResponse(event_generator(), media_type="text/event-stream")


async def send_event(message: dict):
    for client in clients:
        await client.put(message)


@server_sent_event_router.get("/response", response_class=FileResponse)
def home():
    htmlpath = "static/html/sse.html"
    return FileResponse(path=htmlpath, status_code=200)
