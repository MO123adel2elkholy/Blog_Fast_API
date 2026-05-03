import asyncio
import json

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

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


from fastapi.responses import HTMLResponse


@server_sent_event_router.get("/response", response_class=HTMLResponse)
def home():
    return """
<!DOCTYPE html>
<html>
<head>
    <title>SSE Demo</title>
</head>
<body>

<h2>Live Notifications</h2>
<ul id="list"></ul>

<script>
const eventSource = new EventSource("http://127.0.0.1:8000/server/stream");

eventSource.onmessage = function(event) {
    const data = JSON.parse(event.data);

    const li = document.createElement("li");
    li.innerText = data.type + " - " + JSON.stringify(data.data);

    document.getElementById("list").appendChild(li);
};
</script>

</body>
</html>
"""
