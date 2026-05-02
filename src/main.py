from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import PlainTextResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

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
