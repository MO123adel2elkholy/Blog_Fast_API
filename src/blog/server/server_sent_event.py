import asyncio
import json

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import StreamingResponse
from starlette.responses import FileResponse

clients = []

router = APIRouter()


async def admin_required(request: Request):
    if "user" not in request.session:
        raise HTTPException(
            status_code=status.HTTP_303_SEE_OTHER, headers={"Location": "/admin/login"}
        )
    return True


# @router.get("/server/stream")
# async def stream(user=Depends(admin_required)):

#     async def event_generator():
#         while True:
#             data = {"type": "ADMIN", "data": "secret"}

#             yield f"data: {json.dumps(data)}\n\n"

#             await asyncio.sleep(2)

#     return StreamingResponse(event_generator(), media_type="text/event-stream")

server_sent_event_router = APIRouter(
    tags=["sever-sent-evevnt"],
    prefix="/server",
)


@server_sent_event_router.get("/stream", dependencies=[Depends(admin_required)])
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


@server_sent_event_router.get(
    "/response", response_class=FileResponse, dependencies=[Depends(admin_required)]
)
def home():
    htmlpath = "static/html/sse.html"
    return FileResponse(path=htmlpath, status_code=200)
