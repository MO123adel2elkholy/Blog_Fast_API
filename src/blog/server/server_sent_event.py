import asyncio
import json

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import StreamingResponse
from starlette.responses import FileResponse

clients = []

router = APIRouter()


async def admin_required(request: Request):
    if "user" not in request.session:
        # include original path+query as `next` so the admin login page can redirect back
        next_url = request.url.path
        if request.url.query:
            next_url += "?" + request.url.query
        raise HTTPException(
            status_code=status.HTTP_303_SEE_OTHER,
            headers={"Location": f"/admin/login?next={next_url}"},
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
async def stream(request: Request):
    # don't redirect HTML for EventSource (causes HTML to be sent and reconnection loops).
    # return 401 so client can redirect to login once.
    if "user" not in request.session:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized"
        )

    async def event_generator():
        queue = asyncio.Queue()
        clients.append(queue)
        try:
            while True:
                data = await queue.get()
                yield f"data: {json.dumps(data)}\n\n"
        except asyncio.CancelledError:
            pass
        finally:
            if queue in clients:
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
